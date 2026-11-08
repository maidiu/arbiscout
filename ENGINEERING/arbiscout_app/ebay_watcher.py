#!/usr/bin/env python3
"""Local eBay capture console: watch user-saved sold pages and update results.

The user opens each eBay sold page with the console button and saves it. This
program only reads files the user saved; it never fetches eBay itself. New
files are copied into a staging folder, parsed, and the reports regenerated.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import signal
import threading
import time
import webbrowser

import run_test

STATE = {"folder": "", "downloads": "", "staging": "", "output": "",
         "candidates": [], "captured": 0, "total": 0, "pending": [],
         "updated": "", "message": ""}
LOCK = threading.Lock()


def load_state(output):
    path = Path(output) / "comparisons" / "comparisons.json"
    if not path.is_file():
        return {"candidates": [], "captured": 0, "total": 0}
    rows = json.loads(path.read_text(encoding="utf-8"))
    candidates = []
    for row in rows:
        c = row["comparison"]
        p = row["retailer"]
        candidates.append({
            "fixture_index": row.get("fixture_index"),
            "fixture_file": row.get("fixture_file"),
            "title": p.get("title"),
            "retail_url": p.get("url"),
            "retail_current": p.get("current_price"),
            "retail_regular": p.get("regular_price"),
            "retail_discount": p.get("discount_percent"),
            "retail_savings": p.get("savings"),
            "ebay_url": row.get("ebay_search_url"),
            "ebay_status": row.get("ebay_status"),
            "status": c.get("status"),
            "sample_count": c.get("sample_count"),
            "sold_low": c.get("sold_low"),
            "sold_high": c.get("sold_high"),
            "sold_mean": c.get("sold_mean"),
            "median": c.get("historical_median"),
            "typical_low": c.get("typical_low"),
            "typical_high": c.get("typical_high"),
            "below_low": c.get("retail_below_low"),
            "below_median": c.get("retail_below_median"),
            "gap": c.get("gap"),
            "gap_percent": c.get("gap_percent"),
        })
    candidates.sort(key=lambda x: (x["fixture_index"] is None, x["fixture_index"] or 999))
    captured = sum(1 for x in candidates if (x["sample_count"] or 0) > 0)
    return {"candidates": candidates, "captured": captured, "total": len(candidates)}


def update_state(folder, downloads, staging, output, pending, message=""):
    data = load_state(output)
    with LOCK:
        STATE.update({"folder": str(Path(folder).resolve()),
                      "downloads": str(Path(downloads).resolve()) if downloads else "",
                      "staging": str(Path(staging).resolve()),
                      "output": str(Path(output).resolve()),
                      "candidates": data["candidates"], "captured": data["captured"],
                      "total": data["total"], "pending": sorted(pending),
                      "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      "message": message})


CONSOLE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ArbiScout · eBay capture console</title><style>
:root{color-scheme:light;font:14px system-ui,-apple-system,Segoe UI,sans-serif;color:#172333;background:#f3f5f8}
*{box-sizing:border-box}body{margin:0}header{background:#0c2544;color:#fff;padding:22px max(20px,calc((100vw - 1600px)/2))}
header h1{margin:0;font-size:26px}header p{color:#c1d5ea;margin:6px 0 0;font-size:13px}
.wrap{max-width:1600px;padding:18px;margin:auto}.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.kpi{background:#fff;padding:14px;border:1px solid #e2e8f0;border-radius:11px}.kpi strong{font-size:24px;display:block}.kpi span{color:#62748a;font-size:12px}
.note{background:#fff9e6;border:1px solid #f1d38d;border-radius:9px;padding:11px 14px;color:#644a1a;font-size:13px;margin:14px 0;word-break:break-word}
.controls{display:flex;flex-wrap:wrap;gap:9px;margin:14px 0;align-items:center}
.controls input,.controls select{padding:9px;border-radius:8px;border:1px solid #cfd9e4;background:#fff;font-size:13px;min-height:38px}
.controls input[type=search]{flex:1;min-width:200px}.controls label{display:flex;align-items:center;gap:6px;color:#45566e;font-size:13px}
button,.btn{display:inline-block;padding:9px 13px;border-radius:8px;border:0;background:#1261bd;color:#fff;font-weight:650;text-decoration:none;cursor:pointer;font-size:13px}
.btn.alt{background:#fff;color:#17508d;border:1px solid #b9cce2}.tablewrap{overflow:auto;border:1px solid #e2e8f0;border-radius:11px;background:#fff}
table{border-collapse:collapse;width:100%;min-width:1500px}th{background:#eaf0f8;font-size:11px;color:#50617a;position:sticky;top:0;padding:10px;text-align:left;white-space:nowrap}
td{border-top:1px solid #e9edf3;padding:10px;vertical-align:top;font-size:12px}tbody tr:hover{background:#f8fbff}
td.n{white-space:nowrap;font-variant-numeric:tabular-nums}.item{min-width:260px}.good{color:#08734a;font-weight:750}.bad{color:#8b4626}.wait{color:#9a630e}
small{color:#738197}.money{font-weight:700;white-space:nowrap}.count{color:#6b798c;font-size:13px}
@media(max-width:760px){.kpis{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header><h1>ArbiScout <span style="font-weight:400;color:#97bce7">/ eBay capture</span></h1>
<p>Click <b>Open next waiting eBay page</b>, save the completed-listing page, and the row updates automatically. The app never fetches eBay itself.</p></header>
<main class="wrap">
<div class="kpis"><div class="kpi"><strong id="kCap">0</strong><span>Captured / candidates</span></div>
<div class="kpi"><strong id="kLow">0</strong><span>Best Buy below eBay low</span></div>
<div class="kpi"><strong id="kMed">0</strong><span>Best Buy below eBay median</span></div>
<div class="kpi"><strong id="kPend">0</strong><span>Files being read</span></div></div>
<div class="note" id="paths"></div>
<div class="controls">
  <button id="next">Open next waiting eBay page</button>
  <input id="q" type="search" placeholder="Filter by product name, model, price…">
  <select id="sort">
    <option value="discount">Highest % off</option>
    <option value="savings">Highest dollar savings</option>
    <option value="price">Lowest current price</option>
    <option value="price_desc">Highest current price</option>
    <option value="title">Product name A–Z</option>
    <option value="gap">Largest eBay gap</option>
    <option value="sold_low">Lowest eBay sold price</option>
  </select>
  <select id="view"><option value="all">All candidates</option><option value="below_low">Best Buy below eBay low</option><option value="below_median">Best Buy below eBay median</option></select>
  <label><input type="checkbox" id="complete"> Only products with both retail prices</label>
  <span id="msg" class="count"></span>
  <a class="btn alt" href="/retailer" target="_blank">Best Buy dashboard</a>
  <a class="btn alt" href="/top10" target="_blank">Top 10 report</a>
  <a class="btn alt" href="/comparisons" target="_blank">All comparisons</a>
</div>
<div class="tablewrap"><table><thead><tr>
<th>#</th><th>Product</th><th>Current</th><th>Regular</th><th>% off</th><th>Savings</th>
<th>eBay sold low</th><th>eBay sold high</th><th>Mean</th><th>Median</th><th>Typical 50%</th>
<th>Best Buy vs eBay</th><th>Sales</th><th>File / status</th><th>Open</th>
</tr></thead><tbody id="rows"></tbody></table></div>
</main>
<script>
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
const usd=v=>v==null?'—':('$'+Number(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}));
let state={candidates:[],captured:0,total:0,pending:[]};
function cmpNull(a,b,dir){if(a==null&&b==null)return 0;if(a==null)return 1;if(b==null)return -1;return dir*(a-b);}
function render(){
  const q=$('q').value.toLowerCase().trim(),sort=$('sort').value,view=$('view').value;
  $('kCap').textContent=state.captured+' / '+state.total;
  $('kLow').textContent=state.candidates.filter(x=>x.below_low===true).length;
  $('kMed').textContent=state.candidates.filter(x=>x.below_median===true).length;
  $('kPend').textContent=state.pending.length;
  $('msg').textContent=state.message||'';
  $('paths').innerHTML='<b>Save into either:</b> '+esc(state.folder)+(state.downloads?' &nbsp;or&nbsp; '+esc(state.downloads):'')+
    '<br><small>Any filename works; pages are matched by their eBay search query. Working copies: '+esc(state.staging)+'</small>';
  let rows=state.candidates.filter(x=>(x.title||'').toLowerCase().includes(q));
  if($('complete').checked)rows=rows.filter(x=>x.retail_current!=null&&x.retail_regular!=null);
  if(view==='below_low')rows=rows.filter(x=>x.below_low===true);
  if(view==='below_median')rows=rows.filter(x=>x.below_median===true);
  rows.sort((a,b)=>{
    if(sort==='discount')return (b.retail_discount??-1)-(a.retail_discount??-1);
    if(sort==='savings')return (b.retail_savings??-1)-(a.retail_savings??-1);
    if(sort==='price')return cmpNull(a.retail_current,b.retail_current,1);
    if(sort==='price_desc')return cmpNull(a.retail_current,b.retail_current,-1);
    if(sort==='title')return (a.title||'').localeCompare(b.title||'');
    if(sort==='gap')return cmpNull(a.gap,b.gap,-1);
    if(sort==='sold_low')return cmpNull(a.sold_low,b.sold_low,1);
    return 0;
  });
  $('rows').innerHTML=rows.map(x=>{
    const waiting=x.ebay_status==='NO_FIXTURE_FOR_PRODUCT'||x.ebay_status==='NO_MATCHING_FIXTURE';
    const has=(x.sample_count||0)>0;
    const vs=x.below_low===true?'<span class="good">Below eBay low</span>':x.below_median===true?'<span class="good">Below eBay median</span>':x.below_median===false?'<span class="bad">At/above eBay median</span>':'—';
    const file=waiting?'<span class="wait">Waiting for file</span>':esc(x.fixture_file||'');
    return `<tr><td class="n">${x.fixture_index??''}</td>
      <td class="item"><a href="${esc(x.retail_url)}" target="_blank" rel="noopener noreferrer"><b>${esc(x.title)}</b></a></td>
      <td class="n">${usd(x.retail_current)}</td><td class="n">${usd(x.retail_regular)}</td>
      <td class="n">${x.retail_discount==null?'—':x.retail_discount+'%'}</td><td class="n">${usd(x.retail_savings)}</td>
      <td class="n">${usd(x.sold_low)}</td><td class="n">${usd(x.sold_high)}</td><td class="n">${usd(x.sold_mean)}</td><td class="n">${usd(x.median)}</td>
      <td class="n">${x.typical_low==null?'—':usd(x.typical_low)+' – '+usd(x.typical_high)}</td>
      <td>${vs}</td><td class="n">${x.sample_count??0}</td>
      <td><small>${file}</small><br><small>${esc(x.status||'')}</small><br><small>${esc(x.ebay_status||'')}</small></td>
      <td><a class="btn" href="${esc(x.ebay_url)}" target="_blank" rel="noopener noreferrer">Open eBay</a></td></tr>`;
  }).join('')||'<tr><td colspan="15">No matching products.</td></tr>';
}
async function poll(){try{const r=await fetch('/api/state',{cache:'no-store'});state=await r.json();render();}catch(e){}}
$('next').onclick=()=>{
  const x=state.candidates.find(c=>c.ebay_status==='NO_FIXTURE_FOR_PRODUCT'||c.ebay_status==='NO_MATCHING_FIXTURE')
       ||state.candidates.find(c=>(c.sample_count||0)===0);
  if(x)window.open(x.ebay_url,'_blank');else alert('All candidates have captured files.');
};
$('q').oninput=render;$('sort').onchange=render;$('view').onchange=render;$('complete').onchange=render;
poll();setInterval(poll,1500);
</script></body></html>"""


def is_ebay_saved(path):
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            head = handle.read(400_000).lower()
    except OSError:
        return False
    return "ebay" in head and ("_nkw" in head or "lh_sold" in head or "s-item" in head or "s-card" in head)


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
            return self._send(200, CONSOLE)
        if self.path == "/api/state":
            with LOCK:
                body = json.dumps(STATE, ensure_ascii=False)
            return self._send(200, body, "application/json; charset=utf-8")
        if self.path == "/top10":
            return self._file(Path(STATE["output"]) / "index.html")
        if self.path == "/comparisons":
            return self._file(Path(STATE["output"]) / "comparisons" / "index.html")
        if self.path == "/retailer":
            return self._file(Path(STATE["output"]) / "retailer" / "index.html")
        return self._send(404, "Not found.")

    def log_message(self, *_args):
        pass


def main(argv=None):
    p = argparse.ArgumentParser(description="Watch user-saved eBay sold HTML files")
    p.add_argument("--folder", default="ebay_saved", help="Primary watch folder (default: ebay_saved)")
    p.add_argument("--output", default="bestbuy_live", help="Existing ArbiScout output folder")
    p.add_argument("--downloads", action="store_true", default=True, help="Also watch ~/Downloads")
    p.add_argument("--no-downloads", dest="downloads", action="store_false")
    p.add_argument("--downloads-dir", help="Watch this folder instead of ~/Downloads")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--delete-on-exit", action="store_true",
                   help="Delete working copies and NN.html files in the primary folder when you stop")
    p.add_argument("--no-open", action="store_true", help="Do not open the console browser tab")
    p.add_argument("--keep-selection", action="store_true",
                   help="Preserve the selected products in file order instead of re-selecting top 20")
    a = p.parse_args(argv)

    def stop(_signum, _frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)

    folder = Path(a.folder)
    output = Path(a.output)
    if a.downloads_dir:
        downloads = Path(a.downloads_dir)
    else:
        downloads = Path.home() / "Downloads" if a.downloads else None
    staging = output / "comparisons" / ".ebay_staging"
    if not (output / "retailer" / "products.json").is_file():
        raise SystemExit("No Best Buy candidates yet. Run ./run_live.command first.")
    folder.mkdir(parents=True, exist_ok=True)
    staging.mkdir(parents=True, exist_ok=True)
    for old in staging.glob("*.html"):
        try:
            old.unlink()
        except OSError:
            pass

    port = a.port
    server = None
    for candidate_port in range(a.port, a.port + 15):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate_port), Handler)
            port = candidate_port
            break
        except OSError:
            continue
    if server is None:
        raise SystemExit("Could not find a free local port.")
    threading.Thread(target=server.serve_forever, daemon=True).start()

    try:
        run_test.execute(ebay_pages=str(staging), reuse_retailer=True,
                         output=str(output), as_of=datetime.now(timezone.utc),
                         ebay_auto_match=True, keep_selection=a.keep_selection)
    except Exception as exc:
        print("Initial processing error:", exc)
    update_state(folder, downloads, staging, output, [], "Watching for saved files...")

    url = f"http://127.0.0.1:{port}/"
    print("eBay capture console:", url)
    print("Watching:", folder.resolve(), "and", downloads.resolve() if downloads else "(Downloads off)")
    print("Press Ctrl+C to stop.")
    if not a.no_open:
        webbrowser.open(url)

    seen = {}
    pending = {}
    content_cache = {}
    last_message = "Watching for saved files..."
    watch_dirs = [folder] + ([downloads] if downloads and downloads.is_dir() else [])
    try:
        while True:
            current = {}
            for directory in watch_dirs:
                if not directory.is_dir():
                    continue
                for path in sorted(directory.glob("*.html")):
                    try:
                        stat = path.stat()
                    except OSError:
                        continue
                    key = str(path.resolve())
                    signature = (stat.st_mtime_ns, stat.st_size)
                    if key in content_cache and content_cache[key][0] == signature:
                        ebay_page = content_cache[key][1]
                    else:
                        ebay_page = is_ebay_saved(path)
                        content_cache[key] = (signature, ebay_page)
                    if ebay_page:
                        current[key] = (signature, path)
            for key, (signature, path) in current.items():
                if seen.get(key) != signature and (key not in pending or pending[key][0] != signature):
                    pending[key] = (signature, time.monotonic(), path)
            ready = [k for k, (_sig, when, _p) in pending.items() if time.monotonic() - when >= 1.5]
            if ready:
                try:
                    copied = []
                    for key in ready:
                        signature, _when, source = pending[key]
                        digest = hashlib.sha1(key.encode()).hexdigest()[:6]
                        destination = staging / f"{digest}_{source.name}"
                        destination.write_bytes(source.read_bytes())
                        copied.append((key, signature))
                    run_test.execute(ebay_pages=str(staging), reuse_retailer=True,
                                     output=str(output), as_of=datetime.now(timezone.utc),
                                     ebay_auto_match=True, keep_selection=a.keep_selection)
                    for key, signature in copied:
                        seen[key] = signature
                        pending.pop(key, None)
                    last_message = "Processed: " + ", ".join(sorted(Path(k).name for k in ready))
                except Exception as exc:
                    last_message = "Processing error: " + str(exc)[:180]
                    for key in ready:
                        if key in pending:
                            signature, _when, source = pending[key]
                            pending[key] = (signature, time.monotonic(), source)
            update_state(folder, downloads, staging, output, [Path(k).name for k in pending], last_message)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.shutdown()
        if a.delete_on_exit:
            removed = 0
            for target in list(staging.glob("*.html")) + list(folder.glob("*.html")):
                try:
                    target.unlink()
                    removed += 1
                except OSError:
                    pass
            print("Deleted", removed, "working HTML file(s).")


if __name__ == "__main__":
    main()
