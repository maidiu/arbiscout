#!/usr/bin/env python3
"""ArbiScout: bounded 30-day eBay SOLD evidence and retail purchase-price gap.

Never equate an accepted Best Offer's struck-through list price with paid price.
No login automation, CAPTCHA bypass, third-party proxy, or hidden eBay API.
Saved eBay search HTML is supported; live collection is opt-in, robots checked,
normal HTTP only, and may fail due to eBay's authentication/access restrictions.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation
from html import escape
import json
from pathlib import Path
import re
from statistics import median
from urllib.parse import urljoin, quote
from urllib.request import Request, urlopen
from urllib import robotparser
import time

from bs4 import BeautifulSoup

EBAY = 'https://www.ebay.com'
AGENT = 'ArbiScoutResearch/0.3 (read-only personal research)'
PRICE = re.compile(r'\$\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)')
DATE = re.compile(r'\b(?:sold|ended)\s*(?:on\s*)?((?:[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4})|(?:\d{1,2}/\d{1,2}/\d{2,4}))',re.I)
BEST_OFFER = re.compile(r'best\s+offer\s+accepted|accepted\s+(?:a\s+)?best\s+offer|original\s+asking\s+price',re.I)
BAD_MATCH = re.compile(r'\b(?:case only|for parts|repair only|empty box|replacement parts|no console|no laptop|read description|damaged|lot of \d+|bundle of \d+)\b',re.I)
IGNORE_MODELS={'2026','2025','2024','2023','1080','2160','512gb','256gb','128gb','16gb','32gb','64gb','55inch','65inch','120hz','2k','4k','8k','wifi6'}
MONEY_TOLERANCE=0.00001


def money(value):
    if value is None:return '—'
    return '${:,.2f}'.format(value)


def search_url(query):
    from urllib.parse import urlencode
    return EBAY+'/sch/i.html?'+urlencode({'_nkw':query,'LH_Sold':'1','LH_Complete':'1','_sop':'13','_ipg':'240'})


def choose_deals(records,n=20,order='percent'):
    """Only genuine observed current+reference retail prices; no advertised-only discount."""
    goods=[r for r in records if r.get('current_price') is not None and
           r.get('regular_price') is not None and r.get('current_price')>0 and
           r.get('regular_price')>r.get('current_price') and
           not r.get('variant_conflict') and not r.get('price_conflict')]
    field='savings' if order=='dollars' else 'discount_percent'
    return sorted(goods,key=lambda r:(-(r.get(field) or 0),-(r.get('savings') or 0),r.get('title','')))[:n]


def model_candidates(title):
    # Extract model-like tokens, never a guarantee of identity.
    words=re.findall(r'(?<!\w)[A-Za-z0-9]+(?:[-.][A-Za-z0-9]+)*(?!\w)',title or '')
    out=[]
    for w in words:
        w=w.lower()
        if len(w)<4 or w in IGNORE_MODELS or not re.search(r'[a-z]',w) or not re.search(r'\d',w):continue
        if re.fullmatch(r'(?:\d+gb|\d+tb|\d+hz|\d+mp|\d+mah|\d+k)',w):continue
        if w not in out:out.append(w)
    return out


def model_match(retail,sale_title):
    title=(retail.get('title') or '').lower()
    sold=(sale_title or '').lower()
    if BAD_MATCH.search(sold):return False,'mismatched_condition_or_bundle'
    model=str(retail.get('model') or retail.get('mpn') or '').lower().strip()
    if model and len(model)>=3:
        return (model in sold,'model_match' if model in sold else 'model_missing')
    candidates=model_candidates(title)
    if not candidates:return False,'no_verified_model_identifier'
    # Require at least one discriminating model token; not a substitute for variant check.
    common=[c for c in candidates if re.search(r'(?<!\w)'+re.escape(c)+r'(?!\w)',sold)]
    if not common:return False,'no_matching_model_token'
    # Extra checking for other distinct model-looking tokens to prevent obvious substitutions.
    if len(candidates)>1 and not all(c in sold for c in candidates[:2]):
        return False,'model_variant_ambiguous'
    return True,'tentative_model_token_match'


def parse_date(s):
    if not s:return None
    m=DATE.search(s)
    if not m:return None
    value=m.group(1).replace('  ',' ').strip()
    for fmt in ('%b %d, %Y','%B %d, %Y','%b %d %Y','%B %d %Y','%m/%d/%Y','%m/%d/%y'):
        try:return datetime.strptime(value,fmt).replace(tzinfo=timezone.utc)
        except ValueError:continue
    return None


def price(s):
    m=PRICE.search(s or '')
    if not m:return None
    try:
        v=Decimal(m.group(1).replace(',',''))
        return float(v) if 0<v<Decimal('10000000') else None
    except InvalidOperation:return None


def parse_ebay_sold_html(html,query_url):
    soup=BeautifulSoup(html,'html.parser')
    body=soup.get_text(' ',strip=True)[:3000].lower()
    if ('sign in' in body and ('please sign in' in body or 'sign in to view' in body)) or 'captcha' in body[:1200]:
        return [],'AUTHENTICATION_OR_CHALLENGE'
    nodes=soup.select('li.s-item,li.s-card,div.s-item__wrapper,div.s-card__info')
    seen=set();rows=[]
    for node in nodes:
        anchor=node.select_one('a.s-item__link,a.s-card__link,a[href*="/itm/"]')
        if not anchor or not anchor.get('href'):continue
        link=urljoin(EBAY,anchor['href'].split('?')[0]);im=re.search(r'/itm/(?:[^/]+/)?(\d{9,15})',link)
        if not im or im.group(1) in seen:continue
        seen.add(im.group(1))
        tnode=node.select_one('.s-item__title,.s-card__title,h3')
        title=(tnode or anchor).get_text(' ',strip=True)
        if not title or title.lower() in ('shop on ebay','sponsored'):continue
        pnode=node.select_one('.s-item__price,.s-card__price')
        if not pnode:continue
        raw_price=pnode.get_text(' ',strip=True)
        date_node=node.select_one('.s-item__ended-date,.s-item__endedDate,.s-item__caption--signal,.s-card__caption,.s-item__title--tagblock')
        date_text=(date_node.get_text(' ',strip=True) if date_node else '')
        if not parse_date(date_text):
            # Date in other inline text is allowed only if explicitly sold/ended.
            date_text=node.get_text(' ',strip=True)[-500:]
        when=parse_date(date_text)
        full=node.get_text(' ',strip=True)
        best=bool(BEST_OFFER.search(full)) or bool(pnode.select('s,del,strike'))
        # Price ranges, multiple currencies and crossed-out figures are not valid paid amounts.
        ambiguous=bool(re.search(r'\$\s*\d[\d.,]*\s*(?:to|-|–)\s*\$',raw_price,re.I))
        v=price(raw_price) if not best and not ambiguous else None
        rows.append({'item_id':im.group(1),'title':title,'item_url':link,'sold_at':when.isoformat() if when else None,
                     'displayed_price':price(raw_price),'paid_price':v,
                     'price_status':'UNKNOWN_ACCEPTED_OFFER' if best else 'AMBIGUOUS_RANGE' if ambiguous else 'DISPLAYED_SOLD',
                     'date_status':'KNOWN' if when else 'UNKNOWN','source_url':query_url})
    return rows,'PARSED' if rows else 'NO_SOLD_ROWS_PARSED'


def qualify(retail,observations,as_of=None,min_sales=3):
    as_of=as_of or datetime.now(timezone.utc)
    start=as_of-timedelta(days=30)
    diag={'returned':len(observations),'dated_in_window':0,'unknown_best_offer':0,'model_rejected':0,
          'date_rejected':0,'unknown_paid':0,'usable':0}
    good=[]
    for o in observations:
        try:d=datetime.fromisoformat(o.get('sold_at') or '')
        except ValueError:d=None
        if d is None or not start<=d.astimezone(timezone.utc)<=as_of:
            diag['date_rejected']+=1;continue
        diag['dated_in_window']+=1
        match,_=model_match(retail,o.get('title',''))
        if not match:diag['model_rejected']+=1;continue
        if o.get('price_status')=='UNKNOWN_ACCEPTED_OFFER':diag['unknown_best_offer']+=1;continue
        v=o.get('paid_price')
        if v is None or not 0<float(v)<1e7:
            diag['unknown_paid']+=1;continue
        good.append(float(v))
    diag['usable']=len(good)
    retail_price=retail.get('current_price')
    if len(good)<min_sales:
        return {'status':'INSUFFICIENT_VERIFIED_SALES','historical_median':None,'gap':None,'gap_percent':None,'sample_count':len(good),'diagnostics':diag}
    if retail_price is None or retail_price<=0:
        return {'status':'RETAIL_PRICE_UNKNOWN','historical_median':None,'gap':None,'gap_percent':None,'sample_count':len(good),'diagnostics':diag}
    baseline=round(median(good),2)
    gap=round(baseline-float(retail_price),2)
    return {'status':'PROVISIONAL_SOLD_DISPLAY_COMPARISON','historical_median':baseline,'gap':gap,
            'gap_percent':round(100*gap/baseline,1) if baseline else None,
            'sample_count':len(good),'diagnostics':diag}


def fetch_live(query_url,timeout=18,delay=2.5):
    """Opt-in direct HTTP; no sign-in replay, blocking circumvention or proxies."""
    rp=robotparser.RobotFileParser();rp.set_url(EBAY+'/robots.txt')
    req=Request(EBAY+'/robots.txt',headers={'User-Agent':AGENT})
    with urlopen(req,timeout=timeout) as r:
        if r.status!=200:raise RuntimeError('robots policy unavailable')
        rp.parse(r.read(500_000).decode('utf-8',errors='replace').splitlines())
    if not rp.can_fetch(AGENT,query_url):raise RuntimeError('robots policy denies automated eBay sold search')
    time.sleep(max(1,delay))
    req=Request(query_url,headers={'User-Agent':AGENT,'Accept':'text/html'})
    with urlopen(req,timeout=timeout) as r:
        final=r.geturl()
        if 'ebay.com' not in (final.split('/')[2]).lower() or '/signin' in final:
            raise RuntimeError('eBay requires sign-in or redirected away from sold search')
        data=r.read(6_000_001)
        if len(data)>6_000_000:raise RuntimeError('eBay response larger than safe maximum')
        return data.decode('utf-8',errors='replace')


def compare_top20(retail_json,output,top=20,order='percent',fixture_dir=None,live=False,min_sales=3,as_of=None):
    deals=choose_deals(json.loads(Path(retail_json).read_text(encoding='utf-8')),top,order)
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    records=[];all_sales=[]
    for i,p in enumerate(deals):
        query=p.get('ebay_query') or p.get('title','')
        url=search_url(query)
        status='NOT_FETCHED';observations=[]
        try:
            if fixture_dir:
                fixture=Path(fixture_dir)/f'{i+1:02d}.html'
                if fixture.exists():html=fixture.read_text(encoding='utf-8');observations,status=parse_ebay_sold_html(html,url)
                else:status='NO_FIXTURE_FOR_PRODUCT'
            elif live:
                html=fetch_live(url);observations,status=parse_ebay_sold_html(html,url)
        except Exception as exc:
            status='ACCESS_FAILED: '+str(exc)[:180]
        evidence=qualify(p,observations,as_of,min_sales)
        records.append({'retailer':p,'ebay_search_url':url,'ebay_status':status,'comparison':evidence})
        all_sales.extend([{**s,'retailer_key':p['key']} for s in observations])
    records.sort(key=lambda r:(r['comparison']['gap'] is None,-(r['comparison']['gap'] or 0),-(r['comparison']['gap_percent'] or 0)))
    (output/'comparisons.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
    (output/'sold_observations.json').write_text(json.dumps(all_sales,indent=2,ensure_ascii=False),encoding='utf-8')
    (output/'index.html').write_text(dashboard(records),encoding='utf-8')
    return records


def dashboard(records):
    payload=json.dumps(records,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ArbiScout · 30-day eBay comparison</title><style>
:root{font:14px system-ui,-apple-system,Segoe UI,sans-serif;color:#17202b;background:#f4f7fa}body{margin:0 auto;max-width:1500px;padding:25px}header{display:flex;justify-content:space-between;gap:14px;align-items:center;flex-wrap:wrap}h1{margin:0;font-size:29px}p{color:#536071;max-width:1050px;line-height:1.5}.metrics{display:flex;gap:10px;margin:15px 0}.metric{background:#fff;border:1px solid #dce4eb;border-radius:12px;padding:12px 20px}.metric b{font-size:22px}select,input{padding:10px;border:1px solid #bccbd8;border-radius:8px;background:#fff}.tablewrap{overflow:auto;background:#fff;border:1px solid #dce4eb;border-radius:12px}table{border-collapse:collapse;width:100%;min-width:1120px}th,td{padding:13px 11px;border-bottom:1px solid #e7ecf1;text-align:left;vertical-align:top}th{font-size:12px;color:#5a6470;background:#eef2f6;position:sticky;top:0}td.n{white-space:nowrap;font-variant-numeric:tabular-nums}td.item{min-width:250px}small{color:#697887}a{color:#125ca3;text-decoration:none}a:hover{text-decoration:underline}.good{color:#177645;font-weight:bold}.bad{color:#8b4626}.unknown{color:#a46619}.btn{display:inline-block;padding:7px 9px;border:1px solid #cedce8;border-radius:8px;margin-bottom:4px}.foot{font-size:12px}
</style></head><body><header><h1>ArbiScout · 30-day eBay comparison</h1><div><label>Sort <select id="sort"><option value="gap">Largest eBay gap</option><option value="pct">Largest relative eBay gap</option><option value="discount">Largest retailer discount</option><option value="savings">Largest retailer savings</option></select></label> <input id="filter" placeholder="Search products"></div></header>
<p>This is a purchase-price reference, <strong>not projected resale profit</strong>. Only dated records within the last 30 days enter the historical sample. Best Offer amounts not proven paid are excluded. Unverified product matches, missing sale dates, inaccessible eBay pages and insufficient observations produce NO RANK rather than invented savings. Even accepted results need independent checking of identity, condition, shipping, and displayed-price fidelity.</p><div class="metrics" id="metrics"></div><div class="tablewrap"><table><thead><tr><th>Product</th><th>Retail<br>current</th><th>Retail<br>was</th><th>Retail<br>discount</th><th>30d eBay<br>median*</th><th>eBay gap</th><th>Valid<br>sales</th><th>Evidence status</th><th>Open links</th></tr></thead><tbody id="rows"></tbody></table></div><p class="foot">*Provisional median from usable displayed sold results. No accepted Best Offer's crossed-out asking price is counted. Sold-results pages can omit transactions, and strict product matching may yield false negatives. This is not the official eBay Product Research dataset.</p><script>
const data=__DATA__;const $=id=>document.getElementById(id);const esc=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));const usd=v=>v==null?'—':('$'+Number(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}));
function render(){const q=$('filter').value.toLowerCase().trim(),sort=$('sort').value;let rows=data.filter(x=>x.retailer.title.toLowerCase().includes(q));rows.sort((a,b)=>{const key=sort==='gap'?'gap':sort==='pct'?'gap_percent':null;const v=x=>key?x.comparison[key]:sort==='discount'?x.retailer.discount_percent:x.retailer.savings;const av=v(a),bv=v(b);if(av==null)return bv==null?0:1;if(bv==null)return -1;return bv-av});$('metrics').innerHTML=`<div class="metric"><b>${data.length}</b><br>Retail deals checked</div><div class="metric"><b>${data.filter(x=>x.comparison.gap!==null).length}</b><br>Provisional 30d comparisons</div><div class="metric"><b>${data.filter(x=>x.ebay_status.startsWith('ACCESS_FAILED')).length}</b><br>Source failures</div>`;$('rows').innerHTML=rows.map(x=>{let p=x.retailer,c=x.comparison;return `<tr><td class="item"><strong>${esc(p.title)}</strong><br><small>${esc(p.key)}</small></td><td class="n">${usd(p.current_price)}</td><td class="n">${usd(p.regular_price)}</td><td class="n">${p.discount_percent??'—'}%</td><td class="n">${usd(c.historical_median)}</td><td class="n ${c.gap>0?'good':c.gap<0?'bad':'unknown'}">${usd(c.gap)} ${c.gap_percent===null?'':`(${c.gap_percent}%)`}</td><td class="n">${c.sample_count}</td><td><strong>${esc(c.status)}</strong><br><small>${esc(x.ebay_status)}</small><br><small>matched: ${c.diagnostics.usable}; rejected: ${c.diagnostics.model_rejected}; unknown offers: ${c.diagnostics.unknown_best_offer}</small></td><td><a class="btn" target="_blank" rel="noopener noreferrer" href="${esc(p.url)}">At retailer</a><br><a class="btn" target="_blank" rel="noopener noreferrer" href="${esc(x.ebay_search_url)}">eBay sold</a></td></tr>`}).join('')||'<tr><td colspan="9">No matching products.</td></tr>'}
$('sort').onchange=render;$('filter').oninput=render;render();</script></body></html>'''.replace('__DATA__',payload)


def main(argv=None):
    p=argparse.ArgumentParser(description='Compare selected retailer deals with 30-day dated eBay sold observations')
    p.add_argument('--retail-json',required=True)
    p.add_argument('--outdir',default='arbiscout_ebay_comparison')
    p.add_argument('--top',type=int,default=20)
    p.add_argument('--sort-retailer',choices=['percent','dollars'],default='percent')
    p.add_argument('--ebay-fixtures',help='Directory with 01.html, 02.html... saved sold-search pages for selected products')
    p.add_argument('--ebay-live',action='store_true',help='Opt in to direct robots-checked eBay requests; may be forbidden or require sign-in')
    p.add_argument('--min-sales',type=int,default=3)
    p.add_argument('--as-of',help='ISO date YYYY-MM-DD for repeatable fixture tests')
    a=p.parse_args(argv)
    if a.top<1 or a.top>100 or a.min_sales<1:p.error('top must be 1..100 and min-sales >= 1')
    if a.ebay_live and a.ebay_fixtures:p.error('choose live OR fixtures')
    at=datetime.fromisoformat(a.as_of).replace(tzinfo=timezone.utc) if a.as_of else None
    rows=compare_top20(a.retail_json,a.outdir,a.top,a.sort_retailer,a.ebay_fixtures,a.ebay_live,a.min_sales,at)
    print(f'Wrote {a.outdir}/index.html; {len(rows)} retailer candidates; '+str(sum(r['comparison']['gap'] is not None for r in rows))+' provisional eBay gaps')

if __name__=='__main__':main()
