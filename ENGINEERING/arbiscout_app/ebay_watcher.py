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
import subprocess
import sys
import threading
import time
import webbrowser
from urllib.parse import urlparse

import run_test

STATE = {"folder": "", "downloads": "", "staging": "", "output": "",
         "candidates": [], "captured": 0, "total": 0, "pending": [],
         "armed": [], "files": [], "updated": "", "message": ""}
REFINE = {"status": "idle", "message": "", "started": None, "finished": None, "result": None}
ARMED = set()
MANUAL = {}
KEEP_SELECTION = False
REPROCESSING = False
LOCK = threading.Lock()


def source_label(product):
    host = (urlparse(product.get("url") or "").hostname or "").lower()
    if "bestbuy.com" in host:
        return "Best Buy"
    if "meh.com" in host:
        return "Meh"
    if "woot.com" in host:
        return "Woot"
    if "kroger.com" in host:
        return "Kroger"
    return product.get("source") or product.get("source_label") or product.get("source_kind") or "Other"


def load_state(output):
    path = Path(output) / "comparisons" / "comparisons.json"
    if not path.is_file():
        return {"candidates": [], "captured": 0, "total": 0}
    rows = json.loads(path.read_text(encoding="utf-8"))
    candidates = []
    for row in rows:
        c = row["comparison"]
        p = row["retailer"]
        refinement = row.get("llm_refinement") or {}
        checked = bool(row.get("llm_checked") or refinement)
        summary_parts = []
        if refinement.get("exact") is not None:
            summary_parts.append(f"{refinement.get('exact')} exact")
        if refinement.get("removed") is not None:
            summary_parts.append(f"{refinement.get('removed')} removed")
        if c.get("sample_count") is not None:
            summary_parts.append(f"{c.get('sample_count')} usable sales")
        if c.get("historical_median") is not None:
            summary_parts.append(f"median ${c.get('historical_median'):,.2f}")
        if c.get("gap") is not None:
            summary_parts.append(f"gap ${c.get('gap'):,.2f}")
        llm_summary = " · ".join(summary_parts)
        def stats_summary(n, median, gap):
            parts = []
            if n is not None:
                parts.append(f"n={n}")
            if median is not None:
                parts.append(f"median ${median:,.2f}")
            if gap is not None:
                parts.append(f"gap ${gap:,.2f}")
            return " · ".join(parts)
        llm_pre_summary = stats_summary(refinement.get("before_sample_count"),
                                        refinement.get("before_median"),
                                        refinement.get("before_gap"))
        llm_post_summary = stats_summary(refinement.get("after_sample_count", c.get("sample_count")),
                                         refinement.get("after_median", c.get("historical_median")),
                                         refinement.get("after_gap", c.get("gap")))
        candidates.append({
            "fixture_index": row.get("fixture_index"),
            "fixture_file": row.get("fixture_file"),
            "key": p.get("key") or p.get("url"),
            "llm_refined": checked,
            "llm_checked": checked,
            "llm_summary": llm_summary,
            "llm_pre_summary": llm_pre_summary,
            "llm_post_summary": llm_post_summary,
            "title": p.get("title"),
            "retail_url": p.get("url"),
            "observed_at": p.get("observed_at"),
            "source": source_label(p),
            "category": p.get("category"),
            "variant_count": p.get("variant_count"),
            "kroger_zip": p.get("kroger_zip"),
            "kroger_location_id": p.get("kroger_location_id"),
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
            "diagnostics": c.get("diagnostics"),
        })
    candidates.sort(key=lambda x: (x["fixture_index"] is None, x["fixture_index"] or 999))
    captured = sum(1 for x in candidates if (x["sample_count"] or 0) > 0)
    return {"candidates": candidates, "captured": captured, "total": len(candidates)}


def run_refine_thread(folder, downloads, staging, output, keys=None):
    global REFINE
    label = f"{len(keys)} selected candidate(s)" if keys is not None else "saved listings"
    with LOCK:
        REFINE.update({"status": "running", "message": f"Refining {label} with DeepSeek...",
                       "started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       "finished": None, "result": None})
    try:
        args = [sys.executable, str(Path(__file__).with_name("llm_refine.py")),
                "--output", str(output), "--json"]
        if keys is not None:
            keys_path = Path(output) / "comparisons" / "llm_run_keys.json"
            keys_path.parent.mkdir(parents=True, exist_ok=True)
            keys_path.write_text(json.dumps({"keys": sorted(keys)}, indent=2) + "\n",
                                 encoding="utf-8")
            args += ["--keys-file", str(keys_path)]
        proc = subprocess.run(
            args, cwd=str(Path(__file__).resolve().parent), capture_output=True, text=True,
            timeout=900)
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "LLM refinement failed").strip()
            raise RuntimeError(detail[-500:])
        lines = [line for line in proc.stdout.splitlines() if line.strip()]
        result = json.loads(lines[-1]) if lines else {}
        message = (f"Refined: {result.get('exact', 0)} exact / "
                   f"{result.get('removed', 0)} removed")
        with LOCK:
            REFINE.update({"status": "success", "message": message,
                           "finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                           "result": result})
        update_state(folder, downloads, staging, output, [], message)
    except Exception as exc:
        with LOCK:
            REFINE.update({"status": "failed", "message": str(exc)[:500],
                           "finished": datetime.now(timezone.utc).isoformat(timespec="seconds")})


def load_manual(output):
    path = Path(output) / "manual_matches.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {str(key): str(value) for key, value in data.items() if key and value} if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_manual(output):
    if not output:
        return
    path = Path(output) / "manual_matches.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(MANUAL, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def manual_files(folder, downloads):
    files = {}
    for directory in (folder, downloads):
        if not directory:
            continue
        target = Path(directory)
        if not target.is_dir():
            continue
        for path in sorted(target.glob("*.html")):
            files[path.name] = str(path.resolve())
    return files


def reprocess_thread(folder, downloads, staging, output):
    global REPROCESSING
    with LOCK:
        REPROCESSING = True
        STATE["message"] = "Reprocessing manual match..."
    try:
        run_test.execute(ebay_pages=str(staging), reuse_retailer=True,
                         output=str(output), as_of=datetime.now(timezone.utc),
                         ebay_auto_match=True, keep_selection=KEEP_SELECTION,
                         manual_matches=MANUAL)
        merge_llm_refinement(output)
        update_state(folder, downloads, staging, output, [], "Manual match applied")
    except Exception as exc:
        update_state(folder, downloads, staging, output, [], "Manual match failed: " + str(exc)[:300])
    finally:
        with LOCK:
            REPROCESSING = False


def observations_fingerprint(observations):
    payload = [{key: observation.get(key) for key in
                ("item_id", "title", "displayed_price", "sold_at", "price_status")}
               for observation in observations]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False)
                          .encode("utf-8")).hexdigest()


def merge_llm_refinement(output):
    current_path = Path(output) / "comparisons" / "comparisons.json"
    llm_path = Path(output) / "comparisons" / "comparisons_llm.json"
    observations_path = Path(output) / "comparisons" / "sold_observations.json"
    if not (current_path.is_file() and llm_path.is_file() and observations_path.is_file()):
        return
    try:
        current = json.loads(current_path.read_text(encoding="utf-8"))
        refined = json.loads(llm_path.read_text(encoding="utf-8"))
        observations = json.loads(observations_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    refined_by_key = {row.get("retailer", {}).get("key"): row for row in refined}
    by_retailer = {}
    for observation in observations:
        by_retailer.setdefault(observation.get("retailer_key"), []).append(observation)
    changed = False
    for row in current:
        key = row.get("retailer", {}).get("key")
        candidate = refined_by_key.get(key)
        if not candidate or not candidate.get("llm_checked"):
            continue
        stored = (candidate.get("llm_refinement") or {}).get("evidence_fingerprint")
        if stored and stored != observations_fingerprint(by_retailer.get(key, [])):
            continue
        row.update(candidate)
        changed = True
    if changed:
        current_path.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")


def reset_llm_record(output, key):
    current_path = Path(output) / "comparisons" / "comparisons.json"
    raw_path = Path(output) / "comparisons" / "comparisons_raw.json"
    if not current_path.is_file():
        return False
    try:
        current = json.loads(current_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    raw_by_key = {}
    if raw_path.is_file():
        try:
            for row in json.loads(raw_path.read_text(encoding="utf-8")):
                raw_by_key[row.get("retailer", {}).get("key")] = row
        except (OSError, ValueError):
            raw_by_key = {}
    found = False
    for index, row in enumerate(current):
        if row.get("retailer", {}).get("key") != key:
            continue
        found = True
        if key in raw_by_key:
            current[index] = raw_by_key[key]
        else:
            row.pop("llm_checked", None)
            row.pop("llm_refinement", None)
        break
    if found:
        current_path.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")
    return found


def load_armed(output):
    path = Path(output) / "llm_armed.json"
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        keys = data.get("keys", []) if isinstance(data, dict) else data
        return {str(key) for key in keys if key}
    except (OSError, ValueError):
        return set()


def save_armed(output):
    if not output:
        return
    path = Path(output) / "llm_armed.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"keys": sorted(ARMED)}, indent=2) + "\n", encoding="utf-8")


def update_state(folder, downloads, staging, output, pending, message=""):
    data = load_state(output)
    with LOCK:
        files = manual_files(folder, downloads)
        for candidate in data.get("candidates", []):
            candidate["manual_file"] = Path(MANUAL.get(candidate.get("key"), "")).name if MANUAL.get(candidate.get("key")) else ""
        STATE.update({"folder": str(Path(folder).resolve()),
                      "armed": sorted(ARMED),
                      "files": [{"name": name, "path": path} for name, path in sorted(files.items())],
                      "downloads": str(Path(downloads).resolve()) if downloads else "",
                      "staging": str(Path(staging).resolve()),
                      "output": str(Path(output).resolve()),
                      "candidates": data["candidates"], "captured": data["captured"],
                      "total": data["total"], "pending": sorted(pending),
                      "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      "message": message})


CONSOLE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ArbiScout · Results</title><style>
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
td.n{white-space:nowrap;font-variant-numeric:tabular-nums}.item{min-width:260px}.good{color:#08734a;font-weight:750}.bad{color:#8b4626}.wait{color:#9a630e}td select{padding:5px;font-size:11px;max-width:220px}button.reset-llm{padding:2px 6px;font-size:10px;background:#fff;color:#17508d;border:1px solid #b9cce2;border-radius:5px;cursor:pointer}
small{color:#738197}.money{font-weight:700;white-space:nowrap}.count{color:#6b798c;font-size:13px}.sources{display:flex;gap:8px;flex-wrap:wrap;align-items:center;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:9px 12px;margin:10px 0}.sources strong{font-size:12px;color:#50617a}.sources label{font-size:13px;color:#2d3f52}
@media(max-width:760px){.kpis{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header><h1>ArbiScout <span style="font-weight:400;color:#97bce7">/ Results</span></h1>
<p>Capture and results in one page. Click <b>Open next waiting eBay page</b>, save the completed-listing page, and the row updates automatically. The app never fetches eBay itself.</p></header>
<main class="wrap">
<div class="kpis"><div class="kpi"><strong id="kCap">0</strong><span>Captured / candidates</span></div>
<div class="kpi"><strong id="kLow">0</strong><span>Retailer below eBay low</span></div>
<div class="kpi"><strong id="kMed">0</strong><span>Retailer below eBay median</span></div>
<div class="kpi"><strong id="kPend">0</strong><span>Files being read</span></div></div>
<div class="note" id="paths"></div>
<div class="controls">
  <button id="next">Open next waiting eBay page</button>
  <button id="refineSelected">Run selected with DeepSeek</button>
  <button id="refineNew">Run all new with DeepSeek</button><span id="refineMsg" class="count"></span>
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
  <select id="view"><option value="all">All candidates</option><option value="top10">Top 10 positive gaps</option><option value="below_low">Retailer below eBay low</option><option value="below_median">Retailer below eBay median</option><option value="waiting">Waiting for eBay file</option><option value="captured">With eBay evidence</option></select>
  <div class="sources" id="sources"></div>
  <select id="category"><option value="">All categories</option></select>
  <select id="dateRange">
    <option value="today">Today</option>
    <option value="24h">Last 24 hours</option>
    <option value="7d">Last 7 days</option>
    <option value="30d" selected>Last 30 days</option>
    <option value="all">All dates</option>
    <option value="custom">Custom…</option>
  </select>
  <span id="customDates" style="display:none"><input id="dateFrom" type="date"> – <input id="dateTo" type="date"></span>
  <label><input type="checkbox" id="complete"> Only products with both retail prices</label>
  <span id="msg" class="count"></span>
  <a class="btn alt" href="http://127.0.0.1:8800/">Control room</a>
  <a class="btn alt" href="http://127.0.0.1:8800/deals">Deals</a>
  <a class="btn alt" href="http://127.0.0.1:8800/settings">Settings</a>
</div>
<div class="tablewrap"><table><thead><tr>
<th>#</th><th>Product</th><th>Current</th><th>Regular</th><th>% off</th><th>Savings</th>
<th>eBay sold low</th><th>eBay sold high</th><th>Mean</th><th>Median</th><th>Typical 50%</th>
<th>Retailer vs eBay</th><th>Sales</th><th>Observed</th><th>File / status</th><th>Match</th><th>LLM</th><th>Open</th>
</tr></thead><tbody id="rows"></tbody></table></div>
</main>
<script>
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
const usd=v=>v==null?'—':('$'+Number(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}));
let state={candidates:[],captured:0,total:0,pending:[],armed:[]};
let visible=[];
function cmpNull(a,b,dir){if(a==null&&b==null)return 0;if(a==null)return 1;if(b==null)return -1;return dir*(a-b);}
function dateBounds(){
  const range=$('dateRange').value,now=new Date();
  const startOfDay=d=>new Date(d.getFullYear(),d.getMonth(),d.getDate()).getTime();
  let after=null,before=null;
  if(range==='today')after=new Date(startOfDay(now)).toISOString();
  else if(range==='24h')after=new Date(Date.now()-24*3600*1000).toISOString();
  else if(range==='7d')after=new Date(Date.now()-7*24*3600*1000).toISOString();
  else if(range==='30d')after=new Date(Date.now()-30*24*3600*1000).toISOString();
  else if(range==='custom'){
    if($('dateFrom').value)after=new Date($('dateFrom').value+'T00:00:00').toISOString();
    if($('dateTo').value)before=new Date($('dateTo').value+'T23:59:59.999').toISOString();
  }
  return {after,before};
}
function inRange(x,bounds){
  if(!bounds.after&&!bounds.before)return true;
  if(!x.observed_at)return false;
  const t=new Date(x.observed_at);
  if(bounds.after&&t<new Date(bounds.after))return false;
  if(bounds.before&&t>new Date(bounds.before))return false;
  return true;
}
const SOURCE_ORDER=['Best Buy','Dell','LEGO','Meh','Woot','Kroger'];
let sourceChecked={};
function activeSources(){return Object.keys(sourceChecked).filter(k=>sourceChecked[k]);}
function populateSources(){
  const counts={};state.candidates.forEach(x=>{if(x.source)counts[x.source]=(counts[x.source]||0)+1;});
  const sources=[...new Set([...SOURCE_ORDER,...Object.keys(counts)])];
  $('sources').innerHTML='<strong>Sources</strong>'+sources.map(s=>{
    if(!(s in sourceChecked))sourceChecked[s]=true;
    return `<label><input type="checkbox" value="${esc(s)}" ${sourceChecked[s]?'checked':''}> ${esc(s)} (${counts[s]||0})</label>`;
  }).join('')+'<button class="btn alt" id="allSources">All</button><button class="btn alt" id="noSources">Clear</button>';
  $('allSources').onclick=()=>{sources.forEach(s=>sourceChecked[s]=true);populateSources();render();};
  $('noSources').onclick=()=>{sources.forEach(s=>sourceChecked[s]=false);populateSources();render();};
}
function populateCategories(){
  const categories=[...new Set(state.candidates.map(x=>x.category).filter(Boolean))].sort();
  const cs=$('category'),cv=cs.value;
  cs.innerHTML='<option value="">All categories</option>'+categories.map(v=>`<option>${esc(v)}</option>`).join('');
  cs.value=cv;
}
function render(){
  const q=$('q').value.toLowerCase().trim(),sort=$('sort').value,view=$('view').value,bounds=dateBounds();
  const category=$('category').value,active=activeSources();
  $('kCap').textContent=state.captured+' / '+state.total;
  $('kPend').textContent=state.pending.length;
  $('msg').textContent=state.message||'';
  let rows=state.candidates.filter(x=>(x.title||'').toLowerCase().includes(q)&&inRange(x,bounds));
  if(active.length)rows=rows.filter(x=>active.includes(x.source));else rows=[];
  if(category)rows=rows.filter(x=>x.category===category);
  if($('complete').checked)rows=rows.filter(x=>x.retail_current!=null&&x.retail_regular!=null);
  if(view==='below_low')rows=rows.filter(x=>x.below_low===true);
  if(view==='below_median')rows=rows.filter(x=>x.below_median===true);
  if(view==='waiting')rows=rows.filter(x=>['NO_FIXTURE_FOR_PRODUCT','NO_MATCHING_FIXTURE'].includes(x.ebay_status)||(x.sample_count||0)===0);
  if(view==='captured')rows=rows.filter(x=>(x.sample_count||0)>0);
  if(view==='top10'){
    rows=rows.filter(x=>x.gap!=null&&x.gap>0&&(x.sample_count||0)>=3);
    rows.sort((a,b)=>cmpNull(a.gap,b.gap,-1));
    rows=rows.slice(0,10);
  }else{
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
  }
  $('kLow').textContent=rows.filter(x=>x.below_low===true).length;
  $('kMed').textContent=rows.filter(x=>x.below_median===true).length;
  $('paths').innerHTML='<b>Save into either:</b> '+esc(state.folder)+(state.downloads?' &nbsp;or&nbsp; '+esc(state.downloads):'')+
    '<br><small>Showing '+rows.length+' of '+state.total+' candidates · LLM checked '+state.candidates.filter(x=>x.llm_checked).length+' · output: '+esc(state.output)+'</small>'+
    '<br><small>Any filename works; pages are matched by their eBay search query. Working copies: '+esc(state.staging)+'</small>';
  visible=rows;
  $('rows').innerHTML=rows.map((x,index)=>{
    const waiting=x.ebay_status==='NO_FIXTURE_FOR_PRODUCT'||x.ebay_status==='NO_MATCHING_FIXTURE';
    const vs=x.below_low===true?'<span class="good">Below eBay low</span>':x.below_median===true?'<span class="good">Below eBay median</span>':x.below_median===false?'<span class="bad">At/above eBay median</span>':'—';
    const file=waiting?'<span class="wait">Waiting for file</span>':esc(x.fixture_file||'');
    const obs=x.observed_at?new Date(x.observed_at).toLocaleString():'—';
    const rank=view==='top10'?index+1:(x.fixture_index??'');
    const armed=(state.armed||[]).includes(x.key);
    const llmCell=x.llm_checked
      ? `<span class="good">POST-LLM</span> <button class="reset-llm" data-key="${esc(x.key)}">Reset</button><br><small>pre ${esc(x.llm_pre_summary||'—')}</small><br><small>post ${esc(x.llm_post_summary||'—')}</small><br><small>${esc(x.llm_summary||'')}</small>`
      : `<span class="wait">PRE-LLM</span><br><label><input type="checkbox" class="arm" data-key="${esc(x.key)}" ${armed?'checked':''}> arm</label>`;
    const manual=x.manual_file||'';
    const fileOptions=(state.files||[]).map(f=>`<option value="${esc(f.name)}" ${manual===f.name?'selected':''}>${esc(f.name)}</option>`).join('');
    const matchCell=`<select class="manual" data-key="${esc(x.key)}"><option value="">Auto</option>${fileOptions}</select>`;
    const diag=x.diagnostics?`matched ${x.diagnostics.usable??0}; rejected ${x.diagnostics.model_rejected??0}; unknown offers ${x.diagnostics.unknown_best_offer??0}${x.diagnostics.llm_exact!=null?`; LLM exact ${x.diagnostics.llm_exact}, removed ${x.diagnostics.llm_removed}`:''}`:'';
    return `<tr><td class="n">${rank}</td>
      <td class="item"><a href="${esc(x.retail_url)}" target="_blank" rel="noopener noreferrer"><b>${esc(x.title)}</b></a>${x.source?'<br><small>'+esc(x.source)+'</small>':''}${x.category?'<br><small>'+esc(x.category)+'</small>':''}${x.variant_count>1?'<br><small>'+x.variant_count+' variants</small>':''}${x.kroger_zip?'<br><small>ZIP '+esc(x.kroger_zip)+'</small>':''}</td>
      <td class="n">${usd(x.retail_current)}</td><td class="n">${usd(x.retail_regular)}</td>
      <td class="n">${x.retail_discount==null?'—':x.retail_discount+'%'}</td><td class="n">${usd(x.retail_savings)}</td>
      <td class="n">${usd(x.sold_low)}</td><td class="n">${usd(x.sold_high)}</td><td class="n">${usd(x.sold_mean)}</td><td class="n">${usd(x.median)}</td>
      <td class="n">${x.typical_low==null?'—':usd(x.typical_low)+' – '+usd(x.typical_high)}</td>
      <td>${vs}</td><td class="n">${x.sample_count??0}</td><td class="obs">${esc(obs)}</td>
      <td><small>${file}</small><br><small>${esc(x.status||'')}</small><br><small>${esc(x.ebay_status||'')}</small>${diag?'<br><small>'+esc(diag)+'</small>':''}</td>
      <td>${matchCell}</td>
      <td>${llmCell}</td>
      <td><a class="btn" href="${esc(x.ebay_url)}" target="_blank" rel="noopener noreferrer">Open eBay</a></td></tr>`;
  }).join('')||'<tr><td colspan="18">No candidates match the current filters. Try All dates or a different view.</td></tr>';
}
async function poll(){try{const r=await fetch('/api/state',{cache:'no-store'});state=await r.json();populateSources();populateCategories();render();}catch(e){}}
async function refineStatus(){try{const r=await fetch('/api/refine/status',{cache:'no-store'});const j=await r.json();const running=j.status==='running';$('refineSelected').disabled=running;$('refineNew').disabled=running;$('refineMsg').textContent=running?'Refining…':(j.message||'');if(j.status==='success')poll();}catch(e){}}
async function runRefine(mode){const r=await fetch('/api/refine',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode})});const j=await r.json();if(j.error)alert(j.error);else $('refineMsg').textContent='Refining…';refineStatus();}
$('refineSelected').onclick=()=>runRefine('selected');
$('refineNew').onclick=()=>runRefine('new');
$('rows').addEventListener('change',async e=>{
  if(e.target.matches('.arm')){
    const key=e.target.dataset.key,armed=e.target.checked;
    const r=await fetch('/api/arm',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key,armed})});
    const j=await r.json();
    if(j.error){alert(j.error);e.target.checked=!armed;}else{state.armed=j.armed||[];render();}
  }
  if(e.target.matches('.manual')){
    const key=e.target.dataset.key,file=e.target.value;
    const r=await fetch('/api/manual-map',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key,file})});
    const j=await r.json();
    if(j.error)alert(j.error);else{$('refineMsg').textContent='Manual match applied…';setTimeout(poll,1200);}
  }
  if(e.target.matches('.reset-llm')){
    const key=e.target.dataset.key;
    const r=await fetch('/api/llm-reset',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key})});
    const j=await r.json();
    if(j.error)alert(j.error);else{$('refineMsg').textContent='LLM check reset';poll();}
  }
});
$('next').onclick=()=>{
  const x=visible.find(c=>c.ebay_status==='NO_FIXTURE_FOR_PRODUCT'||c.ebay_status==='NO_MATCHING_FIXTURE')
       ||visible.find(c=>(c.sample_count||0)===0);
  if(x)window.open(x.ebay_url,'_blank');else alert('No waiting candidates in this view.');
};
$('q').oninput=render;$('sort').onchange=render;$('view').onchange=render;$('complete').onchange=render;
$('category').onchange=render;
$('dateRange').onchange=()=>{$('customDates').style.display=$('dateRange').value==='custom'?'inline-flex':'none';render();};
$('dateFrom').onchange=render;$('dateTo').onchange=render;
$('sources').addEventListener('change',e=>{if(e.target.matches('input[type=checkbox]')){sourceChecked[e.target.value]=e.target.checked;render();}});
poll();refineStatus();setInterval(poll,1500);setInterval(refineStatus,2000);
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
        if self.path == "/api/refine/status":
            with LOCK:
                body = json.dumps(REFINE, ensure_ascii=False)
            return self._send(200, body, "application/json; charset=utf-8")
        if self.path == "/top10":
            return self._file(Path(STATE["output"]) / "index.html")
        if self.path == "/comparisons":
            return self._file(Path(STATE["output"]) / "comparisons" / "index.html")
        if self.path == "/retailer":
            return self._file(Path(STATE["output"]) / "retailer" / "index.html")
        return self._send(404, "Not found.")

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            body = {}
        if self.path == "/api/arm":
            key = str(body.get("key") or "").strip()
            if not key:
                return self._send(400, json.dumps({"error": "Missing candidate key."}),
                                  "application/json; charset=utf-8")
            with LOCK:
                candidate = next((c for c in STATE.get("candidates", [])
                                  if c.get("key") == key), None)
                if body.get("armed") and candidate and candidate.get("llm_checked"):
                    return self._send(400, json.dumps(
                        {"error": "This candidate is already LLM-checked."}),
                        "application/json; charset=utf-8")
                if body.get("armed"):
                    ARMED.add(key)
                else:
                    ARMED.discard(key)
                save_armed(STATE.get("output"))
                armed = sorted(ARMED)
            return self._send(200, json.dumps({"ok": True, "armed": armed},
                                              ensure_ascii=False),
                              "application/json; charset=utf-8")
        if self.path == "/api/llm-reset":
            key = str(body.get("key") or "").strip()
            if not key:
                return self._send(400, json.dumps({"error": "Missing candidate key."}),
                                  "application/json; charset=utf-8")
            with LOCK:
                output = STATE.get("output")
                folder = STATE.get("folder")
                downloads = STATE.get("downloads") or None
                staging = STATE.get("staging")
            if not output or not reset_llm_record(output, key):
                return self._send(404, json.dumps({"error": "Candidate not found."}),
                                  "application/json; charset=utf-8")
            update_state(folder, downloads, staging, output, [], "LLM check reset")
            return self._send(200, json.dumps({"ok": True}), "application/json; charset=utf-8")
        if self.path == "/api/manual-map":
            key = str(body.get("key") or "").strip()
            filename = str(body.get("file") or "").strip()
            if not key:
                return self._send(400, json.dumps({"error": "Missing candidate key."}),
                                  "application/json; charset=utf-8")
            with LOCK:
                folder = STATE.get("folder")
                downloads = STATE.get("downloads") or None
                staging = STATE.get("staging")
                output = STATE.get("output")
                busy = REPROCESSING
            if busy:
                return self._send(409, json.dumps({"error": "Reprocessing already running."}),
                                  "application/json; charset=utf-8")
            if filename:
                files = manual_files(folder, downloads)
                if filename not in files:
                    return self._send(400, json.dumps({"error": "HTML file not found in the watched folders."}),
                                      "application/json; charset=utf-8")
                MANUAL[key] = files[filename]
            else:
                MANUAL.pop(key, None)
            save_manual(output)
            threading.Thread(target=reprocess_thread,
                             args=(folder, downloads, staging, output), daemon=True).start()
            return self._send(200, json.dumps({"ok": True, "file": filename,
                                               "manual": MANUAL.get(key, "")},
                                              ensure_ascii=False),
                              "application/json; charset=utf-8")
        if self.path == "/api/refine":
            mode = str(body.get("mode") or "selected").lower()
            with LOCK:
                if REFINE.get("status") == "running":
                    return self._send(409, json.dumps({"error": "Refinement already running."}),
                                      "application/json; charset=utf-8")
                output = STATE.get("output")
                folder = STATE.get("folder")
                downloads = STATE.get("downloads") or None
                staging = STATE.get("staging")
                candidates = list(STATE.get("candidates", []))
                armed = set(ARMED)
            if not output or not folder:
                return self._send(400, json.dumps({"error": "No selected output is ready."}),
                                  "application/json; charset=utf-8")
            if mode == "selected":
                keys = [c.get("key") for c in candidates
                        if c.get("key") in armed and not c.get("llm_checked")
                        and (c.get("sample_count") or 0) > 0]
                label = "armed"
            elif mode in ("new", "all_new", "all"):
                keys = [c.get("key") for c in candidates
                        if c.get("key") and not c.get("llm_checked")
                        and not c.get("llm_refined")
                        and (c.get("sample_count") or 0) > 0]
                label = "new"
            else:
                return self._send(400, json.dumps({"error": "Unknown refinement mode."}),
                                  "application/json; charset=utf-8")
            keys = [key for key in keys if key]
            if not keys:
                return self._send(400, json.dumps(
                    {"error": f"No {label} candidates with eBay evidence."}),
                    "application/json; charset=utf-8")
            threading.Thread(target=run_refine_thread,
                             args=(folder, downloads, staging, output, keys), daemon=True).start()
            return self._send(202, json.dumps({"ok": True, "mode": mode, "keys": len(keys)}),
                              "application/json; charset=utf-8")
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
                   help="Delete working copies when you stop (your saved source files are kept)")
    p.add_argument("--no-open", action="store_true", help="Do not open the console browser tab")
    p.add_argument("--keep-selection", action="store_true",
                   help="Preserve the selected products in file order instead of re-selecting top 20")
    a = p.parse_args(argv)
    global KEEP_SELECTION
    KEEP_SELECTION = a.keep_selection

    def stop(_signum, _frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)

    folder = Path(a.folder)
    output = Path(a.output)
    ARMED.clear()
    ARMED.update(load_armed(output))
    MANUAL.clear()
    MANUAL.update(load_manual(output))
    if a.downloads_dir:
        downloads = Path(a.downloads_dir)
    else:
        downloads = Path.home() / "Downloads" if a.downloads else None
    staging = output / "comparisons" / ".ebay_staging"
    if not (output / "retailer" / "products.json").is_file():
        raise SystemExit("No retailer candidates yet. Run a source first.")
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

    watch_dirs = [folder] + ([downloads] if downloads and downloads.is_dir() else [])
    seen = {}
    initial_pages = []
    for directory in watch_dirs:
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.html")):
            if not is_ebay_saved(path):
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            digest = hashlib.sha1(str(path.resolve()).encode()).hexdigest()[:6]
            destination = staging / f"{digest}_{path.name}"
            destination.write_bytes(path.read_bytes())
            seen[str(path.resolve())] = (stat.st_mtime_ns, stat.st_size)
            initial_pages.append(path)
    try:
        run_test.execute(ebay_pages=str(staging), reuse_retailer=True,
                         output=str(output), as_of=datetime.now(timezone.utc),
                         ebay_auto_match=True, keep_selection=a.keep_selection,
                         manual_matches=MANUAL)
        merge_llm_refinement(output)
    except Exception as exc:
        print("Initial processing error:", exc)
    initial_message = (f"Processed {len(initial_pages)} saved page(s) at startup"
                       if initial_pages else "Watching for saved files...")
    update_state(folder, downloads, staging, output, [], initial_message)

    url = f"http://127.0.0.1:{port}/"
    print("eBay capture console:", url, flush=True)
    print("Watching:", folder.resolve(), "and", downloads.resolve() if downloads else "(Downloads off)")
    print("Press Ctrl+C to stop.")
    if not a.no_open:
        webbrowser.open(url)

    pending = {}
    content_cache = {}
    last_message = initial_message
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
                                     ebay_auto_match=True, keep_selection=a.keep_selection,
                                     manual_matches=MANUAL)
                    merge_llm_refinement(output)
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
            for target in list(staging.glob("*.html")):
                try:
                    target.unlink()
                    removed += 1
                except OSError:
                    pass
            print("Deleted", removed, "working copy file(s). Saved source files were kept.")


if __name__ == "__main__":
    main()
