#!/usr/bin/env python3
"""Shared category, filter/sort and dashboard code for the unified catalog."""
from __future__ import annotations
import json
import re
from urllib.parse import urlparse

CATEGORY_RULES = [
    ("TV & Home Theater", r"\b(tv|television|oled|qled|soundbar|projector|roku|fire tv|smart tv)\b"),
    ("Computers & Tablets", r"\b(laptop|macbook|chromebook|desktop|monitor|tablet|ipad|notebook|computer)\b"),
    ("Cameras & Drones", r"\b(camera|camcorder|lens|drone|gopro|webcam)\b"),
    ("Video Games", r"\b(gaming|console|controller|playstation|xbox|nintendo|video game)\b"),
    ("Audio & Headphones", r"\b(headphones?|earbuds?|airpods?|speaker|headset)\b"),
    ("Appliances", r"\b(refrigerator|fridge|washer|dryer|oven|range|dishwasher|freezer|microwave|vacuum|air fryer|blender|coffee maker|instant pot|cookware)\b"),
    ("Phones & Wearables", r"\b(phone|iphone|galaxy|pixel|smartwatch|wearable)\b"),
    ("Grocery & Household", r"\b(milk|bread|eggs?|coffee|chicken|grocery|food|detergent|paper towel|toilet paper|cleaning|batteries|battery|light bulb|toothpaste|shampoo|diapers|pet food|vitamins|snack|soda|water)\b"),
    ("Home & Outdoor", r"\b(furniture|lighting|lights?|patio|grill|storage|tools?|bedding|mattress|kitchen|home)\b"),
    ("Sports & Outdoors", r"\b(bike|tent|camping|fitness|yoga|sports?|outdoor)\b"),
    ("Toys & Games", r"\b(toy|lego|puzzle|craft)\b"),
    ("Apparel", r"\b(shirt|pants|shoes|sneakers|jacket|apparel|clothing)\b"),
]
PAGE_CATEGORIES = [
    ("tv-home-theater", "TV & Home Theater"),
    ("computers-tablets", "Computers & Tablets"),
    ("laptop-computers", "Computers & Tablets"),
    ("video-games", "Video Games"),
    ("appliances", "Appliances"),
    ("headphones", "Audio & Headphones"),
    ("cameras-camcorders-drones", "Cameras & Drones"),
    ("wearable-technology", "Phones & Wearables"),
    ("cell-phones", "Phones & Wearables"),
    ("home-furniture-office", "Home & Outdoor"),
    ("outdoor-living", "Home & Outdoor"),
    ("toys-games-crafts", "Toys & Games"),
    ("smart-home-security-wi-fi", "Smart Home"),
    ("car-electronics", "Car Electronics"),
    ("fitness-sports-outdoor", "Sports & Outdoors"),
    ("health-wellness-personal-care", "Health & Personal Care"),
]


def source_label(product, fallback=""):
    host = (urlparse(product.get("url") or "").hostname or "").lower()
    if "bestbuy.com" in host:
        return "Best Buy"
    if "meh.com" in host:
        return "Meh"
    if "woot.com" in host:
        return "Woot"
    if "kroger.com" in host:
        return "Kroger"
    return fallback or product.get("source") or "Other"


def infer_category(product):
    existing = str(product.get("category") or "").strip()
    if existing:
        return existing.title()
    page = (product.get("source_page") or "").lower()
    for needle, category in PAGE_CATEGORIES:
        if needle in page:
            return category
    text = ((product.get("title") or "") + " " + page).lower()
    for category, pattern in CATEGORY_RULES:
        if re.search(pattern, text):
            return category
    return "Other"


def normalize(product, source):
    row = dict(product)
    row["source"] = source or source_label(product)
    row["category"] = infer_category(product)
    row["title"] = row.get("title") or ""
    row["url"] = row.get("url") or ""
    return row


def filter_sort(products, sources=None, categories=None, query="", both_prices=False,
                sort="discount", top=None):
    rows = list(products)
    if sources:
        allowed = set(sources)
        rows = [r for r in rows if r.get("source") in allowed]
    if categories:
        allowed = set(categories)
        rows = [r for r in rows if r.get("category") in allowed]
    query = (query or "").strip().lower()
    if query:
        rows = [r for r in rows if query in (r.get("title") or "").lower()
                or query in (r.get("category") or "").lower()
                or query in (r.get("source") or "").lower()]
    if both_prices:
        rows = [r for r in rows if r.get("current_price") is not None
                and r.get("regular_price") is not None]

    def value(row, field):
        return row.get(field)

    if sort == "savings":
        rows.sort(key=lambda r: (-(value(r, "savings") or -1), r.get("title", "").casefold()))
    elif sort == "price":
        rows.sort(key=lambda r: (value(r, "current_price") is None,
                                 value(r, "current_price") or 0, r.get("title", "").casefold()))
    elif sort == "price_desc":
        rows.sort(key=lambda r: (value(r, "current_price") is None,
                                 -(value(r, "current_price") or 0), r.get("title", "").casefold()))
    elif sort == "title":
        rows.sort(key=lambda r: r.get("title", "").casefold())
    elif sort == "source":
        rows.sort(key=lambda r: (r.get("source", ""), r.get("title", "").casefold()))
    elif sort == "category":
        rows.sort(key=lambda r: (r.get("category", ""), r.get("title", "").casefold()))
    else:
        rows.sort(key=lambda r: (-(value(r, "discount_percent") or -1),
                                 -(value(r, "savings") or 0), r.get("title", "").casefold()))
    if top:
        rows = rows[:max(1, int(top))]
    return rows


def render_dashboard(payload, live=False):
    data = json.dumps({**payload, "live": bool(live)}, ensure_ascii=False)
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ArbiScout · unified catalog</title><style>
:root{color-scheme:light;font:14px system-ui,-apple-system,Segoe UI,sans-serif;color:#172333;background:#f3f5f8}
*{box-sizing:border-box}body{margin:0}header{background:#0c2544;color:#fff;padding:24px max(20px,calc((100vw - 1500px)/2))}
header h1{margin:0;font-size:27px}header p{color:#c1d5ea;margin:6px 0 0;font-size:13px}
.wrap{max-width:1500px;padding:18px;margin:auto}.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.kpi{background:#fff;padding:14px;border:1px solid #e2e8f0;border-radius:11px}.kpi strong{font-size:24px;display:block}.kpi span{color:#62748a;font-size:12px}
.controls{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0;align-items:center}
.controls input,.controls select{padding:9px;border-radius:8px;border:1px solid #cfd9e4;background:#fff;font-size:13px;min-height:38px}
.controls input[type=search]{flex:1;min-width:210px}.controls input[type=number]{width:80px}
.controls label{display:flex;align-items:center;gap:6px;color:#45566e;font-size:13px}
button,.btn{display:inline-block;padding:9px 13px;border-radius:8px;border:0;background:#1261bd;color:#fff;font-weight:650;text-decoration:none;cursor:pointer;font-size:13px}
.btn.alt{background:#fff;color:#17508d;border:1px solid #b9cce2}.sources{display:flex;gap:8px;flex-wrap:wrap;align-items:center;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:9px 12px}
.sources strong{font-size:12px;color:#50617a}.sources label{font-size:13px;color:#2d3f52}.note{background:#fff9e6;border:1px solid #f1d38d;border-radius:9px;padding:11px 14px;color:#644a1a;font-size:13px;margin:12px 0}
.tablewrap{overflow:auto;border:1px solid #e2e8f0;border-radius:11px;background:#fff}
table{border-collapse:collapse;width:100%;min-width:1050px}th{background:#eaf0f8;font-size:11px;color:#50617a;position:sticky;top:0;padding:10px;text-align:left;white-space:nowrap}
td{border-top:1px solid #e9edf3;padding:10px;vertical-align:top;font-size:12px}tbody tr:hover{background:#f8fbff}
td.n{white-space:nowrap;font-variant-numeric:tabular-nums}.item{min-width:300px}.good{color:#08734a;font-weight:750}.bad{color:#8b4626}
small{color:#738197}.badge{display:inline-block;padding:2px 7px;border-radius:999px;background:#eaf0f8;color:#31506f;font-size:11px;font-weight:650}
.savedpanel{background:#fff;border:1px solid #e2e8f0;border-radius:11px;padding:12px 14px;margin:12px 0}
.savedpanel h3{margin:0 0 8px;font-size:15px;display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
.saveditem{display:flex;gap:10px;align-items:center;justify-content:space-between;border-top:1px solid #eef2f6;padding:7px 0;font-size:12px}
.saveditem small{display:block}.savebtn{padding:6px 9px;font-size:11px}
.count{color:#6b798c;font-size:13px}@media(max-width:760px){.kpis{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header><h1>ArbiScout <span style="font-weight:400;color:#97bce7">/ unified catalog</span></h1>
<p>Filter by source and category, sort by discount or savings, then build a top-N selection for the eBay comparison and capture console.</p></header>
<main class="wrap">
<div class="kpis"><div class="kpi"><strong id="kTotal">0</strong><span>All products</span></div>
<div class="kpi"><strong id="kFiltered">0</strong><span>After filters</span></div>
<div class="kpi"><strong id="kSources">0</strong><span>Sources present</span></div>
<div class="kpi"><strong id="kTop">20</strong><span>Selection size</span></div></div>
<div class="sources" id="sources"></div>
<div class="savedpanel" id="savedPanel"></div>
<div class="controls">
  <input id="q" type="search" placeholder="Search product, category or source…">
  <select id="category"><option value="">All categories</option></select>
  <select id="sort">
    <option value="discount">Highest % off</option>
    <option value="savings">Highest dollar savings</option>
    <option value="price">Lowest current price</option>
    <option value="price_desc">Highest current price</option>
    <option value="title">Product name A–Z</option>
    <option value="source">Source A–Z</option>
    <option value="category">Category A–Z</option>
  </select>
  <label><input type="checkbox" id="complete"> Both prices only</label>
  <label><input type="checkbox" id="savedOnly"> Saved only</label>
  <label>Top <input id="top" type="number" min="1" max="500" value="20"></label>
  <button id="build">Build top N selection</button>
  <button id="buildSaved" class="btn alt">Build eBay run from saved</button>
  <span id="msg" class="count"></span>
</div>
<div class="note" id="modeNote"></div>
<div class="tablewrap"><table><thead><tr><th>Source</th><th>Category</th><th>Product</th><th>Current</th><th>Regular</th><th>% off</th><th>Savings</th><th>Save</th><th>Open</th></tr></thead><tbody id="rows"></tbody></table></div>
</main>
<script>
const DATA=__DATA__;const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
const usd=v=>v==null?'—':('$'+Number(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}));
const SOURCES=[...new Set(DATA.products.map(p=>p.source))].sort();
const CATEGORIES=[...new Set(DATA.products.map(p=>p.category))].sort();
let SAVED_ITEMS=[];
const saveKey=p=>p.key||p.url||p.title;
const isSaved=p=>SAVED_ITEMS.some(s=>saveKey(s)===saveKey(p));
async function loadSaved(){
  if(DATA.live){try{const r=await fetch('/api/saved');const j=await r.json();SAVED_ITEMS=j.items||[];}catch(e){SAVED_ITEMS=[];}}
  else{try{SAVED_ITEMS=JSON.parse(localStorage.getItem('arbiscout_saved_items')||'[]');}catch(e){SAVED_ITEMS=[];}}
  renderSaved();
}
function persistSaved(){if(!DATA.live)localStorage.setItem('arbiscout_saved_items',JSON.stringify(SAVED_ITEMS));}
async function toggleSave(p){
  const key=saveKey(p),saved=!isSaved(p);
  if(DATA.live){
    const r=await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key,product:p,saved})});
    const j=await r.json();SAVED_ITEMS=j.items||[];
  }else{
    if(saved)SAVED_ITEMS.push(p);else SAVED_ITEMS=SAVED_ITEMS.filter(s=>saveKey(s)!==key);
    persistSaved();
  }
  renderSaved();render();
}
function renderSaved(){
  const n=SAVED_ITEMS.length;
  $('savedPanel').innerHTML=`<h3>Saved (${n}) <button class="btn alt" id="buildSaved2">Build eBay run from saved</button></h3>`+
    (n?SAVED_ITEMS.map(p=>`<div class="saveditem"><span><b>${esc(p.title)}</b><small>${esc(p.source)} · ${esc(p.category)} · ${usd(p.current_price)} · ${p.discount_percent==null?'—':p.discount_percent+'% off'}</small></span><button class="btn alt savebtn" data-remove="${esc(saveKey(p))}">Remove</button></div>`).join(''):'<small>No saved items yet. Use Save on any row.</small>');
  const b=$('buildSaved2');if(b)b.onclick=buildSaved;
}
async function buildSaved(){
  if(!SAVED_ITEMS.length){alert('Save at least one product first.');return;}
  if(DATA.live){
    $('msg').textContent='Building from saved…';
    try{const r=await fetch('/api/use-saved',{method:'POST'});const j=await r.json();
      $('msg').innerHTML=`Saved run: ${j.selected} products. <a href="/selected/" target="_blank">Top-10 report</a> · <a href="/selected/comparisons/" target="_blank">All comparisons</a><br><small>${j.capture}</small>`;
    }catch(e){$('msg').textContent='Saved run failed: '+e;}
  }else{
    const blob=new Blob([JSON.stringify({products:SAVED_ITEMS},null,2)],{type:'application/json'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='saved.json';a.click();
    $('msg').textContent='Downloaded saved.json. Run ./run_selected.command saved.json';
  }
}
function sourceBoxes(){
  $('sources').innerHTML='<strong>Sources</strong>'+SOURCES.map((s,i)=>`<label><input type="checkbox" value="${esc(s)}" checked> ${esc(s)}</label>`).join('')+
    `<button class="btn alt" id="all">All</button><button class="btn alt" id="woot">Woot only</button><button class="btn alt" id="notwoot">Except Woot</button><button class="btn alt" id="none">Clear</button>`;
  $('all').onclick=()=>document.querySelectorAll('#sources input').forEach(x=>x.checked=true),render();
  $('none').onclick=()=>document.querySelectorAll('#sources input').forEach(x=>x.checked=false),render();
  $('woot').onclick=()=>{document.querySelectorAll('#sources input').forEach(x=>x.checked=x.value==='Woot');render();};
  $('notwoot').onclick=()=>{document.querySelectorAll('#sources input').forEach(x=>x.checked=x.value!=='Woot');render();};
}
function activeSources(){return [...document.querySelectorAll('#sources input:checked')].map(x=>x.value);}
function filtered(applyTop){
  let rows=DATA.products.filter(p=>activeSources().includes(p.source));
  const cat=$('category').value;if(cat)rows=rows.filter(p=>p.category===cat);
  const q=$('q').value.toLowerCase().trim();if(q)rows=rows.filter(p=>((p.title||'')+' '+(p.category||'')+' '+(p.source||'')).toLowerCase().includes(q));
  if($('complete').checked)rows=rows.filter(p=>p.current_price!=null&&p.regular_price!=null);
  if($('savedOnly').checked)rows=rows.filter(isSaved);
  const s=$('sort').value;
  const num=(v,d)=>v==null?d:v;
  rows.sort((a,b)=>{
    if(s==='savings')return (num(b.savings,-1)-num(a.savings,-1))||(a.title||'').localeCompare(b.title||'');
    if(s==='price')return (num(a.current_price,1e12)-num(b.current_price,1e12))||(a.title||'').localeCompare(b.title||'');
    if(s==='price_desc')return (num(b.current_price,-1)-num(a.current_price,-1))||(a.title||'').localeCompare(b.title||'');
    if(s==='title')return (a.title||'').localeCompare(b.title||'');
    if(s==='source')return (a.source||'').localeCompare(b.source||'')||(a.title||'').localeCompare(b.title||'');
    if(s==='category')return (a.category||'').localeCompare(b.category||'')||(a.title||'').localeCompare(b.title||'');
    return (num(b.discount_percent,-1)-num(a.discount_percent,-1))||(num(b.savings,0)-num(a.savings,0))||(a.title||'').localeCompare(b.title||'');
  });
  if(applyTop){const n=Math.max(1,parseInt($('top').value)||20);rows=rows.slice(0,n);}
  return rows;
}
function render(){
  const rows=filtered(true);
  $('kTotal').textContent=DATA.products.length;$('kFiltered').textContent=filtered(false).length;
  $('kSources').textContent=SOURCES.length;$('kTop').textContent=$('top').value||20;
  $('rows').innerHTML=rows.map(p=>`<tr><td><span class="badge">${esc(p.source)}</span></td><td>${esc(p.category)}</td>
    <td class="item"><a href="${esc(p.url)}" target="_blank" rel="noopener noreferrer"><b>${esc(p.title)}</b></a></td>
    <td class="n">${usd(p.current_price)}</td><td class="n">${usd(p.regular_price)}</td>
    <td class="n">${p.discount_percent==null?'—':p.discount_percent+'%'}</td><td class="n">${usd(p.savings)}</td>
    <td><button class="btn alt savebtn" data-key="${esc(saveKey(p))}">${isSaved(p)?'Saved':'Save'}</button></td>
    <td><a class="btn" href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">Open</a></td></tr>`).join('')||'<tr><td colspan="9">No products match the current filters.</td></tr>';
}
async function build(){
  const body={sources:activeSources(),category:$('category').value,query:$('q').value,both_prices:$('complete').checked,sort:$('sort').value,top:Math.max(1,parseInt($('top').value)||20)};
  if(DATA.live){
    $('msg').textContent='Building…';
    try{const r=await fetch('/api/select',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const j=await r.json();
      $('msg').innerHTML=`Selected ${j.selected} products. <a href="/selected/" target="_blank">Top-10 report</a> · <a href="/selected/comparisons/" target="_blank">All comparisons</a><br><small>Capture eBay pages: ./watch_ebay.command ebay_saved --output catalog/selected --keep-selection</small>`;
    }catch(e){$('msg').textContent='Selection failed: '+e;}
  }else{
    const rows=filtered(true);const blob=new Blob([JSON.stringify({filters:body,products:rows},null,2)],{type:'application/json'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='selected.json';a.click();
    $('msg').textContent='Downloaded selected.json. Save it and run ./run_selected.command selected.json';
  }
}
$('q').oninput=render;$('sort').onchange=render;$('category').onchange=render;$('complete').onchange=render;$('savedOnly').onchange=render;$('top').oninput=render;$('build').onclick=build;$('buildSaved').onclick=buildSaved;
$('rows').addEventListener('click',e=>{const b=e.target.closest('.savebtn');if(!b)return;const p=DATA.products.find(x=>saveKey(x)===b.dataset.key);if(p)toggleSave(p);});
$('savedPanel').addEventListener('click',e=>{const b=e.target.closest('[data-remove]');if(!b)return;const p=SAVED_ITEMS.find(x=>saveKey(x)===b.dataset.remove);if(p)toggleSave(p);});
sourceBoxes();
$('category').innerHTML='<option value="">All categories</option>'+CATEGORIES.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join('');
$('modeNote').textContent=DATA.live?'Selection runs locally and writes catalog/selected. Use Save on individual rows for a hand-picked eBay run.':'Static view: Build downloads selected.json. Start ./run_catalog.command for one-click selection and a persistent saved list.';
loadSaved();render();
</script></body></html>""".replace("__DATA__", data)
