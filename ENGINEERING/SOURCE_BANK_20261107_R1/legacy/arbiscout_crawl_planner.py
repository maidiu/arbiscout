#!/usr/bin/env python3
"""ArbiScout local snapshot graph planner (NO NETWORK CALLS).

Input: one or more saved HTML pages with source URL labels.
Output: deduped retailer product records; prioritized links for next listing pages;
        product-page fallbacks ONLY for products not priced across supplied pages.

No automated requests, authorization checks, or dynamic rendering are performed.
Usage:
 python3 arbiscout_crawl_planner.py \
   --snapshot 'Best Buy Black Friday 2026 is Nov. 26–27.html::https://www.bestbuy.com/black-friday' \
   --outdir plans
"""
from __future__ import annotations

import argparse, csv, json, re
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs

from bs4 import BeautifulSoup

MONEY = re.compile(r'\$\s*([0-9,]+(?:\.\d{2})?)')
PERCENT = re.compile(r'(\d+(?:\.\d+)?)\s*%\s*off',re.I)
PRODUCT_ID = re.compile(r'/product/[^/?#]+/([^/?#]+)')
SKU = re.compile(r'/sku/(\d+)(?:/|$)')
BESTBUY_HOST = 'www.bestbuy.com'

@dataclass
class Snapshot:
    path: Path
    url: str


def money(node):
    if not node:return None
    m=MONEY.search(node.get_text(' ',strip=True))
    return str(Decimal(m.group(1).replace(',','')).quantize(Decimal('0.01'))) if m else None


def key_url(url):
    p=urlparse(url)
    return urlunparse((p.scheme.lower(),p.netloc.lower(),p.path.rstrip('/') or '/', '',p.query,''))


def link_type(url):
    u=urlparse(url)
    if u.netloc.lower() != BESTBUY_HOST: return None
    p=u.path.lower()
    if '/product/' in p:return 'product'
    if p.startswith('/site/searchpage.jsp') and any(x in u.query.lower() for x in ['discount','sale','browsedcategory','currentprice']): return 'filtered_deals'
    if p.startswith('/site/top-deals/') or 'deal-of-the-day' in p: return 'top_deals'
    if '/outlet-' in p or 'clearance' in p or '/refurbished-' in p:return 'outlet'
    if p.startswith('/site/all-electronics-on-sale/') or p.startswith('/site/all-appliances-on-sale/'):return 'sale_department'
    if p.startswith('/site/promo/'):return 'promotion'
    if p.startswith('/site/electronics/black-friday'):return 'event_landing'
    return None


def priority(url,typ):
    # Deterministic heuristic about where to inspect, NOT inferred yield.
    low=url.lower()
    score={'top_deals':95,'filtered_deals':90,'outlet':85,'sale_department':70,'promotion':55,'event_landing':20}.get(typ,0)
    for needle,extra in [('top-100',5),('50%25',6),('discount_facet',5),('all-electronics-on-sale',5),('cameras',14),('computers',12),('smart-home',10),('audio',9),('collectibles',9),('video-games',8),('headphones',7),('refurbished',-15),('gift-cards',-30),('appliances',-5)]:
        if needle in low:score+=extra
    return max(0,score)


def read_snapshot(snapshot):
    soup=BeautifulSoup(snapshot.path.read_text(encoding='utf-8',errors='replace'),'lxml')
    product_obs=[]
    for card in soup.select('[data-testid="product-card"]'):
        node=card.select_one('[data-testid="product-card-title-link"]')
        if node is None:continue
        a=node if node.name=='a' and node.get('href') else node.select_one('a[href]')
        if a is None:continue
        url=urljoin(snapshot.url,a['href'])
        if urlparse(url).netloc.lower()!=BESTBUY_HOST:continue
        m=PRODUCT_ID.search(urlparse(url).path)
        if not m:continue
        sid=SKU.search(urlparse(url).path)
        disc=card.select_one('[data-testid="product-card-percent-off"]')
        pct=PERCENT.search(disc.get_text(' ',strip=True)) if disc else None
        current=money(card.select_one('[data-testid="price-block-customer-price"]'))
        previous=money(card.select_one('[data-testid="price-block-regular-price"]'))
        h=card.find_previous('h2')
        section=h.get_text(' ',strip=True)[:120] if h else None
        product_obs.append({'product_id':m.group(1), 'sku':sid.group(1) if sid else None,
           'title':a.get('aria-label') or a.get_text(' ',strip=True),
           'product_url':key_url(url), 'source_page':snapshot.url,
           'section':section,'current_price_usd':current,'previous_price_usd':previous,
           'discount_percent_label':float(pct.group(1)) if pct else None,
           'price_available':current is not None,'price_pair_complete':current is not None and previous is not None})
    nav={}
    for a in soup.select('main a[href]'):
        url=key_url(urljoin(snapshot.url,a['href']))
        typ=link_type(url)
        if typ is None or typ=='product':continue
        # Exclude same page, and source-page alias; no first-page re-fetch loops.
        if key_url(url)==key_url(snapshot.url):continue
        label=a.get_text(' ',strip=True)
        prev_heading=a.find_previous('h2')
        section=prev_heading.get_text(' ',strip=True)[:120] if prev_heading else ''
        row={'url':url,'type':typ,'priority':priority(url,typ),'label':label or 'Unnamed link', 'found_under':section, 'discovered_from':snapshot.url}
        if url not in nav or (row['priority'],len(row['label']))>(nav[url]['priority'],len(nav[url]['label'])):nav[url]=row
    return product_obs, list(nav.values())


def merge(observations):
    products={}
    for row in observations:
        pid=row['product_id']
        if pid not in products:
            products[pid]={**row,'seen_on_pages':[row['source_page']], 'sections_seen':[row['section']] if row['section'] else [],'different_price_observations':False,'variant_conflict':False,'variant_identity_unverified':False, 'observation_count':1}
            continue
        d=products[pid]
        d['observation_count']+=1
        if row['source_page'] not in d['seen_on_pages']:d['seen_on_pages'].append(row['source_page'])
        if row['section'] and row['section'] not in d['sections_seen']:d['sections_seen'].append(row['section'])
        if d['sku'] is not None and row['sku'] is not None and d['sku']!=row['sku']:
            d['variant_conflict']=True
        if (d['sku'] is None) != (row['sku'] is None):
            d['variant_identity_unverified']=True
        if d['sku'] is None and row['sku'] is not None:d['sku']=row['sku']
        if d['discount_percent_label'] is None and row['discount_percent_label'] is not None:d['discount_percent_label']=row['discount_percent_label']
        if row['current_price_usd'] is not None:
            if d['current_price_usd'] is not None and d['current_price_usd']!=row['current_price_usd']:
                d['different_price_observations']=True
            if d['current_price_usd'] is None:
                d['current_price_usd']=row['current_price_usd']
                d['source_page']=row['source_page']
        if row['previous_price_usd'] is not None and d['previous_price_usd'] is None:d['previous_price_usd']=row['previous_price_usd']
        d['price_available']=d['current_price_usd'] is not None
        d['price_pair_complete']=d['current_price_usd'] is not None and d['previous_price_usd'] is not None
    # A product family ID is not proof that all SKU variants are identical.
    # Conflicted variant observations are never treated as fully priced.
    for d in products.values():
        if d['variant_conflict']:
            d['current_price_usd']=None
            d['previous_price_usd']=None
            d['price_available']=False
            d['price_pair_complete']=False
    return list(products.values())


def write_jsonl(path,rows):
    with path.open('w',encoding='utf-8') as f:
        for x in rows:f.write(json.dumps(x,ensure_ascii=False)+'\n')


def write_csv(path,rows,cols):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot',action='append',required=True,help='path::https://www.bestbuy.com/source-page (repeatable)')
    parser.add_argument('--outdir',default='crawl_plan',help='Output directory; no HTTP requests are made')
    args=parser.parse_args()
    snapshots=[]
    for spec in args.snapshot:
        if '::' not in spec:parser.error('--snapshot requires file::https://source-url')
        path,url=spec.rsplit('::',1)
        if urlparse(url).netloc !=BESTBUY_HOST:parser.error('This adapter is for www.bestbuy.com saved pages only')
        if not Path(path).is_file():parser.error('Missing local saved file: '+path)
        snapshots.append(Snapshot(Path(path),url))
    all_observations=[]; nav={}
    for snap in snapshots:
        obs,links=read_snapshot(snap);all_observations+=obs
        for link in links:
            if link['url'] not in nav or link['priority']>nav[link['url']]['priority']:nav[link['url']]=link
    products=merge(all_observations)
    seen_urls={key_url(x.url) for x in snapshots}
    frontier=sorted([x for x in nav.values() if key_url(x['url']) not in seen_urls],key=lambda x:(-x['priority'],x['url']))
    missing=sorted([p for p in products if p['current_price_usd'] is None],key=lambda x: (-(x['discount_percent_label'] or 0),x['title']))
    completion=[]
    for p in missing:
        completion.append({'product_id':p['product_id'],'sku':p['sku'],'title':p['title'],'discount_label':p['discount_percent_label'],
          'seen_on_pages':'; '.join(p['seen_on_pages']), 'product_url':p['product_url'],
          'why_next':'Check remaining relevant listing pages first; product page only if still unpriced',
          'conditional_priority': 'higher' if p['discount_percent_label'] is not None and p['discount_percent_label']>=35 else 'normal'})
    out=Path(args.outdir);out.mkdir(parents=True,exist_ok=True)
    write_jsonl(out/'products.jsonl',products)
    write_csv(out/'next_listing_pages.csv',frontier,['priority','type','label','url','found_under','discovered_from'])
    write_csv(out/'product_page_fallbacks.csv',completion,['conditional_priority','product_id','sku','title','discount_label','seen_on_pages','product_url','why_next'])
    per_section=defaultdict(lambda:Counter())
    for p in products:
        for section in p['sections_seen']:
            per_section[section]['unique_products']+=1
            if p['current_price_usd'] is None:per_section[section]['missing_current_price']+=1
    summary={'source_snapshots':len(snapshots),'raw_product_cards_observed':len(all_observations),'unique_products':len(products),
       'complete_current_prices':sum(p['current_price_usd'] is not None for p in products),
       'complete_price_pairs':sum(p['price_pair_complete'] for p in products),
       'missing_current_prices':len(missing),
       'missing_price_with_percent_discount_label':sum(p['discount_percent_label'] is not None for p in missing),
       'variant_conflicts_needing_manual_review':sum(p['variant_conflict'] for p in products),
       'source_price_conflicts_needing_review':sum(p['different_price_observations'] for p in products),
       'candidate_listing_pages':len(frontier),
       'candidate_listing_page_types':dict(Counter(x['type'] for x in frontier)),
       'product_page_fallbacks_if_no_crosslisting_completions':len(missing),
       'sections':dict(sorted(per_section.items())),
       'limits':['This process only analyzes HTML files supplied by the user; it does not crawl the web.',
                 'A link is a potential next page, not proof it has any particular products or prices.',
                 'No exact model/GTIN match, stock verification, final purchase cost, source access permission, or live availability is asserted.',
                 'Different observations can have different prices: see different_price_observations; investigate rather than overwriting.']}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='sections' and k!='limits'},indent=2))
    print('Wrote:',*(str(out/f) for f in ['next_listing_pages.csv','product_page_fallbacks.csv','products.jsonl','summary.json']),sep='\n  ')

if __name__=='__main__':main()
