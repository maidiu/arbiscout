#!/usr/bin/env python3
"""Local server for the unified catalog and top-N selection."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
import webbrowser

import catalog_ui
import run_test

PAYLOAD = {}
LOCK = threading.Lock()
OUTPUT = Path("catalog")


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _file(self, path):
        target = Path(path)
        if not target.is_file():
            return self._send(404, "Not generated yet.")
        self._send(200, target.read_bytes())

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, catalog_ui.render_dashboard(PAYLOAD, live=True))
        if self.path == "/api/catalog":
            return self._send(200, json.dumps(PAYLOAD, ensure_ascii=False),
                              "application/json; charset=utf-8")
        if self.path == "/selected/":
            return self._file(OUTPUT / "selected" / "index.html")
        if self.path == "/selected/comparisons/":
            return self._file(OUTPUT / "selected" / "comparisons" / "index.html")
        if self.path == "/selected/retailer/":
            return self._file(OUTPUT / "selected" / "retailer" / "index.html")
        if self.path == "/selected/selection.json":
            return self._file(OUTPUT / "selected" / "selection.json")
        return self._send(404, "Not found.")

    def do_POST(self):
        if self.path != "/api/select":
            return self._send(404, "Not found.")
        try:
            length = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(length) or b"{}")
            sources = body.get("sources") or None
            categories = [body["category"]] if body.get("category") else None
            rows = catalog_ui.filter_sort(
                PAYLOAD.get("products", []), sources=sources, categories=categories,
                query=body.get("query", ""), both_prices=bool(body.get("both_prices")),
                sort=body.get("sort", "discount"), top=body.get("top", 20))
            if not rows:
                return self._send(400, json.dumps({"error": "No products match those filters."}),
                                  "application/json; charset=utf-8")
            selected_dir = OUTPUT / "selected"
            retailer = selected_dir / "retailer"
            retailer.mkdir(parents=True, exist_ok=True)
            (selected_dir / "selection.json").write_text(
                json.dumps({"filters": body, "selected": len(rows), "products": rows},
                           indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            (retailer / "products.json").write_text(
                json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            run_test.execute(ebay_pages=None, reuse_retailer=True, keep_selection=True,
                             output=str(selected_dir), as_of=datetime.now(timezone.utc))
            result = {"selected": len(rows), "output": str(selected_dir.resolve()),
                      "top10": "/selected/", "comparisons": "/selected/comparisons/",
                      "capture": "./watch_ebay.command ebay_saved --output catalog/selected --keep-selection"}
            return self._send(200, json.dumps(result, ensure_ascii=False),
                              "application/json; charset=utf-8")
        except Exception as exc:
            return self._send(500, json.dumps({"error": str(exc)[:300]}),
                              "application/json; charset=utf-8")

    def log_message(self, *_args):
        pass


def main(argv=None):
    global PAYLOAD, OUTPUT
    parser = argparse.ArgumentParser(description="Serve the unified catalog and selection API")
    parser.add_argument("--catalog", default="catalog", help="Catalog folder")
    parser.add_argument("--output", default="catalog", help="Selection output folder")
    parser.add_argument("--port", type=int, default=8770)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args(argv)
    catalog_file = Path(args.catalog) / "catalog.json"
    if not catalog_file.is_file():
        raise SystemExit("No catalog.json. Run ./run_catalog.command or build_catalog.py first.")
    PAYLOAD = json.loads(catalog_file.read_text(encoding="utf-8"))
    OUTPUT = Path(args.output)
    port = args.port
    server = None
    for candidate in range(args.port, args.port + 15):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate), Handler)
            port = candidate
            break
        except OSError:
            continue
    if server is None:
        raise SystemExit("Could not find a free local port.")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/"
    print("Unified catalog:", url)
    print("Selection output:", (OUTPUT / "selected").resolve())
    print("Press Ctrl+C to stop.")
    if not args.no_open:
        webbrowser.open(url)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
