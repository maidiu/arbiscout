#!/usr/bin/env python3
"""Merge Best Buy, Meh, Woot and Kroger products into one catalog."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import catalog_ui

DEFAULT_INPUTS = [
    ("Best Buy", "bestbuy_live"),
    ("Meh", "meh_live"),
    ("Woot", "woot_live"),
    ("Kroger", "kroger_live"),
]


def products_path(path):
    target = Path(path)
    if target.is_file():
        return target
    candidate = target / "retailer" / "products.json"
    return candidate if candidate.is_file() else None


def load_source(label, path, max_per_source):
    target = products_path(path)
    if target is None:
        print(f"skip {label}: no retailer/products.json at {path}")
        return []
    rows = json.loads(target.read_text(encoding="utf-8"))
    normalized = []
    seen = set()
    for row in rows:
        key = row.get("key") or row.get("url") or row.get("title")
        if key in seen:
            continue
        seen.add(key)
        normalized.append(catalog_ui.normalize(row, label))
    if max_per_source and len(normalized) > max_per_source:
        normalized = catalog_ui.filter_sort(normalized, sort="discount", top=max_per_source)
    print(f"{label}: {len(normalized)} products from {target}")
    return normalized


def build(inputs, output, max_per_source):
    products = []
    for label, path in inputs:
        products.extend(load_source(label, path, max_per_source))
    products.sort(key=lambda p: (-(p.get("discount_percent") or -1),
                                 -(p.get("savings") or 0), p.get("title", "").casefold()))
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "products": products,
        "sources": sorted({p["source"] for p in products}),
        "categories": sorted({p["category"] for p in products}),
    }
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "catalog.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "index.html").write_text(
        catalog_ui.render_dashboard(payload, live=False), encoding="utf-8")
    print(f"Catalog: {len(products)} products across {len(payload['sources'])} sources")
    print("Dashboard:", (output / "index.html").resolve())
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description="Merge retailer/provider outputs into one catalog")
    parser.add_argument("--input", action="append", default=[],
                        metavar="LABEL=PATH", help="Source label and folder (repeatable)")
    parser.add_argument("--output", default="catalog")
    parser.add_argument("--max-per-source", type=int, default=2000,
                        help="Cap products per source (default 2000; 0 = no cap)")
    args = parser.parse_args(argv)
    inputs = []
    for item in args.input:
        if "=" not in item:
            raise SystemExit("--input must be LABEL=PATH")
        label, path = item.split("=", 1)
        inputs.append((label.strip(), path.strip()))
    if not inputs:
        inputs = [(label, path) for label, path in DEFAULT_INPUTS if products_path(path)]
    if not inputs:
        raise SystemExit("No source outputs found. Run ./run_live.command or ./run_api.command first.")
    build(inputs, args.output, args.max_per_source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
