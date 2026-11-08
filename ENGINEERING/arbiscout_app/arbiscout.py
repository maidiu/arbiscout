#!/usr/bin/env python3
"""ArbiScout: bounded, listing-first retailer price discovery and local HTML dashboard.

Dependencies: beautifulsoup4. Optional: playwright for normal browser rendering.
No AI API, eBay scraping, checkout or purchase automation. Respect robots.txt.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import html
import ipaddress
import json
from pathlib import Path
import re
import socket
import ssl
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler
from urllib import robotparser
from collections import Counter

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('Missing BeautifulSoup. Run: python3 -m pip install beautifulsoup4', file=sys.stderr)
    raise SystemExit(2)

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

USER_AGENT = 'ArbiScoutPersonal/0.2 (bounded read-only research crawler)'
MONEY = re.compile(r'\$\s*([\d,]+(?:\.\d{1,2})?)')
PERCENT = re.compile(r'(\d+(?:\.\d+)?)\s*%\s*off', re.I)
BESTBUY_ID = re.compile(r'/product/[^/?#]+/([^/?#]+)', re.I)
BESTBUY_SKU = re.compile(r'/sku/(\d+)(?:/|$)', re.I)
CANDIDATE = re.compile(r'\b(sale|sales|deals?|discount|clearance|outlet|doorbuster|black[ -]?friday|coupon|specials?|top 100|refurbished)\b', re.I)
SKIP_NAV = re.compile(r'(signin|log[ -]?in|account|privacy|contact|support|policy|cart|checkout|gift.card|financing|reward|membership|help|recall|tracking|order.status|careers|credit.card|facebook|instagram|youtube|tiktok|pinterest|twitter)', re.I)
PRODUCT_SELECTORS = ('[data-testid="product-card"]', '[itemtype*="schema.org/Product"]', '[data-product-id]', '.product-item', '.product-card', 'li.product', '.product-grid-item')
MAX_BYTES = 9_000_000


def is_safe_http(url):
    p=urlsplit(url)
    if p.scheme not in ('http','https') or not p.hostname or p.username or p.password:
        return False
    h=p.hostname.strip('.').lower()
    if h in ('localhost','localhost.localdomain') or h.endswith('.localhost') or h.endswith('.local'):
        return False
    try:
        ip=ipaddress.ip_address(h)
        return ip.is_global
    except ValueError:
        return True


def canonical(url):
    p=urlsplit(url)
    # Preserve query parameters, but remove common tracking noise.
    query=[(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True)
           if not k.lower().startswith(('utm_','fbclid','gclid','mc_')) and k.lower() not in ('ref','lid')]
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip('/') or '/',urlencode(query),'')).replace('www.bestbuy.com:443','www.bestbuy.com')


def same_site(url, root):
    a=urlsplit(url).hostname or ''
    b=urlsplit(root).hostname or ''
    return a.lower().removeprefix('www.') == b.lower().removeprefix('www.')


def price_from_node(node):
    if node is None:return None
    m=MONEY.search(node.get_text(' ',strip=True))
    if not m: return None
    try:return round(float(Decimal(m.group(1).replace(',',''))),2)
    except InvalidOperation:return None


def first_select(node, selectors):
    for s in selectors:
        found=node.select_one(s)
        if found is not None:return found
    return None


def node_price(node, selectors):
    return price_from_node(first_select(node, selectors))


def product_key(url, seed_url):
    p=urlsplit(url)
    if 'bestbuy.com' in (p.hostname or ''):
        m=BESTBUY_ID.search(p.path)
        if m:return 'bestbuy:'+m.group(1).lower()
    for term in ('/dp/','/p/','/products/','/product/'):
        if term in p.path.lower():
            return (p.hostname or '')+p.path.lower().split('?')[0]
    return canonical(url)


def ebay_query(title, product=None):
    """Conservative editable keyword query. Retailer SKU alone is not an eBay product match."""
    if product:
        model=product.get('model') or product.get('mpn')
        brand=product.get('brand')
        if model and brand:return f'{brand} {model}'
        if model:return str(model)
    s=html.unescape(title or '')
    s=re.sub(r'\b(?:save \$\d+|\d+% off|free shipping|limited time)\b',' ',s,flags=re.I)
    s=re.sub(r'\s+-\s+(?=\b(?:color|finish|with free|includes)\b).*','',s,flags=re.I)
    s=re.sub(r'[^\w\s.+\-"/]', ' ', s)
    s=re.sub(r'\s+',' ',s).strip()
    words=s.split(' ')
    return ' '.join(words[:17])[:125]


def ebay_sold_url(query):
    return 'https://www.ebay.com/sch/i.html?'+urlencode({
        '_nkw':query, 'LH_Sold':'1','LH_Complete':'1','_sop':'13','_ipg':'240'})


def get_links(soup, source, root):
    seen={}
    container=soup.select_one('main') or soup
    for link in container.select('a[href]'):
        href=link.get('href','').strip()
        if not href or href.startswith(('#','javascript:','mailto:','tel:')):continue
        url=canonical(urljoin(source,href))
        if not is_safe_http(url) or not same_site(url,root) or url==canonical(source):continue
        label=link.get_text(' ',strip=True)[:130]
        parent=link.find_parent(['section','nav','article','div'])
        ctx=''
        if parent:
            heading=parent.find(['h1','h2','h3'])
            if heading:ctx=heading.get_text(' ',strip=True)[:90]
        s=score_link(url,label,ctx)
        if s<=0:continue
        if url not in seen or seen[url]['score']<s:
            seen[url]={'url':url,'score':s,'label':label,'context':ctx,'found_on':source}
    return list(seen.values())


def score_link(url,label='',context=''):
    p=urlsplit(url)
    path=p.path.lower()
    if (BESTBUY_ID.search(path) or any(x in path for x in ('/product/','/products/','/dp/'))) and not ('on-sale' in path):return 0
    if SKIP_NAV.search(path+' '+label):return 0
    if re.search(r'\.(?:pdf|jpg|webp|png|gif|js|css|xml|svg)$',path):return 0
    test=path.replace('-',' ')+' '+label+' '+context
    if not CANDIDATE.search(test):return 0
    score=25
    if re.search(r'top.deals|top.100|deal.of.the.day|doorbuster',test,re.I):score+=40
    if re.search(r'clearance|outlet|50%.off',test,re.I):score+=30
    if re.search(r'cameras|computers|laptop|smart.home|network|tools|gaming|electronics',test,re.I):score+=12
    if re.search(r'black.friday',test,re.I):score+=10
    if re.search(r'/searchpage|/search\?',path):score-=5
    if re.search(r'credit.card|trade.in|gift',test,re.I):score-=30
    return max(0,score)


def _make_record(url,title,source,depth,kind,current=None,regular=None,discount_label=None,model=None,brand=None,sku=None,condition=None):
    title=re.sub(r'\s+',' ',title or '').strip()[:300]
    if not title or not is_safe_http(url):return None
    return {'key':product_key(url,source),'title':title,'url':canonical(url),'source_page':source,
            'source_depth':depth,'source_kind':kind,'current_price':current,'regular_price':regular,
            'advertised_percent':discount_label,'model':model,'brand':brand,'sku':sku,
            'condition':condition,'observed_at':datetime.now(timezone.utc).isoformat()}


def extract_bestbuy_cards(soup,source,depth):
    out=[]
    for card in soup.select('[data-testid="product-card"]'):
        tc=card.select_one('[data-testid="product-card-title-link"]')
        if not tc:continue
        a=tc if tc.name=='a' and tc.get('href') else tc.select_one('a[href]')
        if not a:continue
        url=urljoin(source,a['href'])
        if not BESTBUY_ID.search(urlsplit(url).path):continue
        title=a.get('aria-label') or a.get_text(' ',strip=True)
        percent=card.select_one('[data-testid="product-card-percent-off"]')
        m=PERCENT.search(percent.get_text(' ',strip=True)) if percent else None
        cur=node_price(card,['[data-testid="price-block-customer-price"]'])
        reg=node_price(card,['[data-testid="price-block-regular-price"]'])
        match=BESTBUY_SKU.search(urlsplit(url).path)
        rec=_make_record(url,title,source,depth,'bestbuy_listing_card',cur,reg,float(m.group(1)) if m else None,sku=match.group(1) if match else None)
        if rec:out.append(rec)
    return out


def extract_bestbuy_offers(soup,source,depth):
    out=[]
    for card in soup.select('.wf-offer'):
        a=card.select_one('h3.product-title a[href]') or card.select_one('a.wf-offer-link[href]')
        if not a:continue
        url=urljoin(source,a['href'])
        if not BESTBUY_ID.search(urlsplit(url).path):continue
        title=a.get_text(' ',strip=True)
        cur=node_price(card,['[data-testid="price-block-customer-price"]'])
        reg=node_price(card,['[data-testid="price-block-regular-price"]'])
        percent=card.select_one('[data-testid="price-block-percent-off"]')
        m=PERCENT.search(percent.get_text(' ',strip=True)) if percent else None
        match=BESTBUY_SKU.search(urlsplit(url).path)
        rec=_make_record(url,title,source,depth,'bestbuy_offer_card',cur,reg,
                         float(m.group(1)) if m else None,sku=match.group(1) if match else None)
        if rec:out.append(rec)
    return out


def _schema_product(data):
    if not isinstance(data,dict):return []
    results=[]
    dtype=data.get('@type',[])
    if isinstance(dtype,str):dtype=[dtype]
    if 'Product' in dtype:results.append(data)
    for child in data.values():
        if isinstance(child,(dict,list)):results.extend(_schema_walk(child))
    return results


def _schema_walk(obj):
    if isinstance(obj,list):
        out=[]
        for x in obj:out.extend(_schema_walk(x))
        return out
    if not isinstance(obj,dict):return []
    typ=obj.get('@type',[])
    typ=[typ] if isinstance(typ,str) else typ
    out=[obj] if 'Product' in typ else []
    for k,v in obj.items():
        if isinstance(v,(dict,list)):out.extend(_schema_walk(v))
    return out


def extract_schema(soup,source,depth):
    out=[]
    for script in soup.select('script[type="application/ld+json"]'):
        try:data=json.loads(script.string or script.get_text())
        except (ValueError,TypeError):continue
        for prod in _schema_walk(data):
            if not isinstance(prod,dict):continue
            url=prod.get('url')
            if not url and depth>0:continue
            url=urljoin(source,url or source)
            if not is_safe_http(url) or not same_site(url,source):continue
            title=prod.get('name')
            if not isinstance(title,str) or not title:continue
            offer=prod.get('offers') or {}
            if isinstance(offer,list):offer=next((i for i in offer if isinstance(i,dict)),{})
            if not isinstance(offer,dict):offer={}
            try:cur=round(float(offer['price']),2) if offer.get('price') is not None else None
            except (ValueError,TypeError):cur=None
            rec=_make_record(url,title,source,depth,'jsonld',cur,None,None,
                model=prod.get('model') or prod.get('mpn'),brand=(prod.get('brand') or {}).get('name') if isinstance(prod.get('brand'),dict) else prod.get('brand'),
                sku=prod.get('sku'),condition=offer.get('itemCondition'))
            if rec:out.append(rec)
    return out


def extract_generic_cards(soup,source,depth):
    out=[]
    candidates=[]
    for selector in PRODUCT_SELECTORS[1:]:
        candidates=soup.select(selector)
        if candidates:break
    for card in candidates[:600]:
        if card.find_parent('[data-testid="product-card"]'):continue
        a=first_select(card,['a[href*="/product/"]','a[href*="/products/"]','a[href*="/dp/"]','a[href]'])
        if not a:continue
        url=urljoin(source,a.get('href',''))
        if not is_safe_http(url) or not same_site(url,source):continue
        name=first_select(card,['[itemprop="name"]','.product-title','.product-name','h3','h2'])
        title=(name.get_text(' ',strip=True) if name else a.get('title') or a.get('aria-label') or a.get_text(' ',strip=True))
        current=node_price(card,['[data-testid*="customer-price"]','[data-testid*="current-price"]','[itemprop="price"]','.sale-price','.price-current','.price--sale','.price'])
        regular=node_price(card,['[data-testid*="regular-price"]','.regular-price','.original-price','.was-price','.compare-at-price','del'])
        disc=PERCENT.search(card.get_text(' ',strip=True))
        rec=_make_record(url,title,source,depth,'generic_listing_card',current,regular,float(disc.group(1)) if disc else None)
        if rec:out.append(rec)
    return out


def extract_product_page(soup,source,depth):
    # Only supplement from a specific product URL, not a listing with sidebar products.
    p=urlsplit(source).path.lower()
    if not ('/product/' in p or '/products/' in p or '/dp/' in p):return []
    name=first_select(soup,['[data-testid="product-title"]','[data-testid="product-name"]','h1'])
    title=name.get_text(' ',strip=True) if name else None
    if not title:
        meta=soup.select_one('meta[property="og:title"]')
        title=meta.get('content') if meta else None
    if not title:return []
    cur=node_price(soup,['[data-testid="price-block-customer-price"]','[data-testid="customer-price"]','[itemprop="price"]','.price-current','.price--sale'])
    reg=node_price(soup,['[data-testid="price-block-regular-price"]','.was-price','.regular-price','del'])
    rec=_make_record(source,title,source,depth,'product_page',cur,reg)
    return [rec] if rec else []


def extract(soup,source,depth):
    rows=extract_bestbuy_cards(soup,source,depth)
    rows+=extract_bestbuy_offers(soup,source,depth)
    # Also read grid/list cards; current Best Buy pages often render prices only there.
    rows+=extract_generic_cards(soup,source,depth)
    # JSON-LD adds product-page information where available, and helps generic stores.
    rows+=extract_schema(soup,source,depth)
    # Always supplement a real product URL, even when JSON-LD or sidebar cards already matched.
    rows+=extract_product_page(soup,source,depth)
    # Avoid extracting generic Product JSON-LD unrelated to listing current product when name is blank.
    return rows


class Store:
    def __init__(self):self.products={};self.raw_observations=0
    def add(self,obs):
        for row in obs:
            self.raw_observations+=1
            key=row['key']
            if key not in self.products:
                self.products[key]={**row,'seen_on':[row['source_page']],'observation_count':1,
                  'price_conflict':False,'variant_conflict':False, 'observations':[self.slim(row)]}
                continue
            p=self.products[key]
            p['observation_count']+=1
            if row['source_page'] not in p['seen_on']:p['seen_on'].append(row['source_page'])
            p['observations'].append(self.slim(row))
            if p.get('sku') and row.get('sku') and p['sku']!=row['sku']:p['variant_conflict']=True
            # Reject mixed old/current prices from unrelated snapshots. Adopt as one pair.
            if row.get('current_price') is not None:
                if p.get('current_price') is not None and p['current_price']!=row['current_price']:
                    p['price_conflict']=True
                if p.get('current_price') is None or (
                    row.get('regular_price') is not None and p.get('regular_price') is None):
                    p['current_price']=row['current_price']
                    p['regular_price']=row.get('regular_price')
                    p['source_page']=row['source_page']
                    p['source_kind']=row['source_kind']
            if p.get('advertised_percent') is None and row.get('advertised_percent') is not None:
                p['advertised_percent']=row['advertised_percent']
            for field in ('brand','model','sku','condition'):
                if not p.get(field) and row.get(field):p[field]=row[field]
    @staticmethod
    def slim(row):
        return {k:row.get(k) for k in ('source_page','source_kind','current_price','regular_price','advertised_percent','sku','observed_at')}
    def records(self):
        out=[]
        for p in self.products.values():
            d=dict(p)
            if d['variant_conflict']:
                d['current_price']=None; d['regular_price']=None
            current,regular=d['current_price'],d['regular_price']
            d['savings']=round(regular-current,2) if current is not None and regular is not None and regular>current else None
            d['discount_percent']=round(d['savings']/regular*100,1) if d['savings'] is not None and regular else None
            d['ebay_query']=ebay_query(d['title'],d)
            d['ebay_url']=ebay_sold_url(d['ebay_query'])
            d['price_complete']=current is not None and regular is not None
            out.append(d)
        return out


class Fetcher:
    def __init__(self,root,delay=1.3,mode='http',timeout=20,visible=False):
        self.root=root;self.delay=max(delay,0.7);self.mode=mode;self.timeout=timeout;self.visible=visible
        self.robots={};self.last=0;self.browser=None;self.pw=None;self.page=None
    def __enter__(self):
        if self.mode=='browser':
            try:from playwright.sync_api import sync_playwright
            except ImportError:raise RuntimeError('Browser mode needs: python3 -m pip install playwright (then install Chromium, or use an installed Chrome)')
            self.pw=sync_playwright().start()
            try:
                # Prefer an already-installed Chrome so no extra browser download is needed.
                self.browser=self.pw.chromium.launch(headless=not self.visible,channel='chrome')
            except Exception:
                try:self.browser=self.pw.chromium.launch(headless=not self.visible)
                except Exception as exc:
                    self.pw.stop();self.pw=None
                    raise RuntimeError('No usable Chrome/Chromium for browser mode ('+str(exc)[:160]+'). Install Chromium with: python3 -m playwright install chromium')
            # Keep the real browser identity here; some retailers reject custom agent strings on product pages.
            self.page=self.browser.new_page()
        return self
    def __exit__(self,*_):
        if self.page:self.page.close()
        if self.browser:self.browser.close()
        if self.pw:self.pw.stop()
    def _http(self,url,limit=MAX_BYTES):
        req=Request(url,headers={'User-Agent':USER_AGENT,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.5'})
        with urlopen(req,timeout=self.timeout,context=SSL_CONTEXT) as r:
            if not is_safe_http(r.geturl()) or not same_site(r.geturl(),self.root):
                raise RuntimeError('Redirected off selected retailer; refusing')
            status=r.status
            if status!=200:raise RuntimeError('HTTP '+str(status))
            if not any(ct in (r.headers.get('Content-Type') or '').lower() for ct in ('text/html','application/xhtml+xml')):
                raise RuntimeError('Not an HTML page')
            raw=r.read(limit+1)
            if len(raw)>limit:raise RuntimeError('Page exceeds size limit')
            return raw.decode(r.headers.get_content_charset() or 'utf-8',errors='replace')
    def check_robots(self,url):
        p=urlsplit(url)
        key=f'{p.scheme}://{p.netloc}'
        if key not in self.robots:
            robots=robotparser.RobotFileParser()
            robots.set_url(key+'/robots.txt')
            if self.mode=='browser':
                # Fetch robots.txt through the same real browser; some retailers drop plain HTTP clients.
                try:
                    resp=self.page.goto(key+'/robots.txt',wait_until='domcontentloaded',timeout=self.timeout*1000)
                    if resp and resp.status==404:
                        robots.parse([]);self.robots[key]=robots
                        return
                    if not resp or resp.status!=200:
                        raise RuntimeError('HTTP '+str(resp.status if resp else '?'))
                    data=self.page.inner_text('body')
                    robots.parse(data.splitlines())
                    self.robots[key]=robots
                except Exception as exc:
                    raise RuntimeError(f'robots.txt unavailable ({exc}); stopping')
            else:
                try:
                    # Use standard parser; network errors must fail closed.
                    req=Request(key+'/robots.txt',headers={'User-Agent':USER_AGENT})
                    with urlopen(req,timeout=self.timeout,context=SSL_CONTEXT) as r:
                        data=r.read(1_000_000).decode('utf-8',errors='replace')
                    robots.parse(data.splitlines())
                    self.robots[key]=robots
                except HTTPError as exc:
                    if exc.code==404:
                        robots.parse([]);self.robots[key]=robots
                    else:raise RuntimeError(f'robots.txt unavailable (HTTP {exc.code}); stopping')
                except Exception as exc:raise RuntimeError(f'robots.txt unavailable ({exc}); stopping')
        if not self.robots[key].can_fetch(USER_AGENT,url):
            raise RuntimeError('robots.txt disallows this URL for the crawler')
    def get(self,url):
        if not is_safe_http(url) or not same_site(url,self.root):raise RuntimeError('Off-site or unsafe URL')
        self.check_robots(url)
        elapsed=time.monotonic()-self.last
        if self.last and elapsed<self.delay:time.sleep(self.delay-elapsed)
        self.last=time.monotonic()
        if self.mode=='browser':
            resp=self.page.goto(url,wait_until='domcontentloaded',timeout=self.timeout*1000)
            if not resp or resp.status>=400:raise RuntimeError('Browser HTTP '+str(resp.status if resp else '?'))
            if not same_site(self.page.url,self.root):raise RuntimeError('Browser redirected off selected retailer')
            # Let ordinary client-side price/product rendering finish; scroll to trigger lazy loading.
            try:self.page.wait_for_load_state('load',timeout=min(8000,self.timeout*1000))
            except Exception:pass
            try:
                stable=0
                for _ in range(40):
                    before=self.page.evaluate('document.body.scrollHeight')
                    self.page.evaluate('window.scrollBy(0,1200)')
                    self.page.wait_for_timeout(800)
                    after=self.page.evaluate('document.body.scrollHeight')
                    at_bottom=self.page.evaluate('window.scrollY+window.innerHeight>=document.body.scrollHeight-5')
                    if after==before and at_bottom:
                        stable+=1
                        if stable>=2:break
                    else:stable=0
            except Exception:pass
            # Price widgets hydrate after entering the viewport; wait until the count stops changing.
            try:
                last=-1;stable=0
                deadline=time.monotonic()+min(30,self.timeout)
                while time.monotonic()<deadline:
                    count=self.page.evaluate(
                        "() => document.querySelectorAll('[data-testid=\"price-block-customer-price\"],"
                        "[data-testid*=\"customer-price\"],.product-list-item [class*=price]').length")
                    if count==last:
                        stable+=1
                        if stable>=3:break
                    else:
                        stable=0;last=count
                    self.page.wait_for_timeout(1000)
            except Exception:pass
            self.page.wait_for_timeout(500)
            return self.page.content()
        return self._http(url)


def analyze_snapshot(page_html,url,depth,store):
    soup=BeautifulSoup(page_html,'html.parser')
    rows=extract(soup,url,depth)
    store.add(rows)
    return rows,get_links(soup,url,url)


def crawl(args):
    root=args.url
    store=Store();log=[];nav={};visited=set();queue=[]
    if args.snapshot:
        path=Path(args.snapshot)
        if not path.is_file():raise RuntimeError('Saved HTML file does not exist: '+str(path))
        source=args.snapshot_url or root
        if not source:raise RuntimeError('Offline snapshot requires --url or --snapshot-url')
        page_html=path.read_text(encoding='utf-8',errors='replace')
        rows,links=analyze_snapshot(page_html,source,0,store)
        log.append({'url':source,'depth':0,'type':'snapshot','status':'OK','products':len(rows),'links':len(links),'message':'Locally saved HTML; not live prices'})
        visited.add(canonical(source))
        for link in links:nav[link['url']]=link
        queue=[(x['url'],1,'listing',x['score']) for x in sorted(links,key=lambda x:-x['score'])]
        if args.offline:return store,log,nav
        root=source
    else:
        if not is_safe_http(root):raise RuntimeError('Please supply a public http(s) retailer URL')
        queue=[(root,0,'listing',999)]
    failed=[]
    saved_dir=Path(args.outdir)/'raw_pages'
    if args.save_html:saved_dir.mkdir(parents=True,exist_ok=True)
    with Fetcher(root,args.delay,args.mode,args.timeout,getattr(args,'browser_visible',False)) as fetcher:
        while queue:
            queue.sort(key=lambda x:(x[1],-x[3]))
            url,depth,kind,score=queue.pop(0)
            if canonical(url) in visited or not same_site(url,root):continue
            if depth>args.depth or (depth>0 and sum(x['type']=='listing' and x['status']=='OK' for x in log)>=args.max_listings):continue
            if sum(x['type']=='listing' for x in log)>=args.max_listings+1:break
            visited.add(canonical(url))
            try:
                page_html=fetcher.get(url)
                if args.save_html:
                    name=hashlib.sha256(url.encode('utf-8')).hexdigest()[:15]+'.html'
                    (saved_dir/name).write_text(page_html,encoding='utf-8')
                soup=BeautifulSoup(page_html,'html.parser')
                rows=extract(soup,url,depth)
                links=get_links(soup,url,root)
                store.add(rows)
                log.append({'url':url,'depth':depth,'type':'listing','status':'OK','products':len(rows),'links':len(links),'message':''})
                for link in links:
                    if link['url'] not in nav or link['score']>nav[link['url']]['score']:nav[link['url']]=link
                    if depth<args.depth and canonical(link['url']) not in visited:
                        queue.append((link['url'],depth+1,'listing',link['score']))
            except Exception as exc:
                log.append({'url':url,'depth':depth,'type':'listing','status':'BLOCKED/FAILED','products':0,'links':0,'message':str(exc)[:450]})
                failed.append(str(exc))
                if depth==0 and not args.snapshot:break
        # Product-page fallback AFTER all selected listings; skip if price already complete.
        if args.max_products>0:
            candidates=sorted([p for p in store.records() if not p['price_complete'] or (args.enrich_models and not p.get('model'))],
                key=lambda p:(p['current_price'] is not None, -(p.get('advertised_percent') or 0),p['title']))
            for p in candidates[:args.max_products]:
                url=p['url']
                if canonical(url) in visited or not same_site(url,root):continue
                visited.add(canonical(url))
                try:
                    page_html=fetcher.get(url)
                    if args.save_html:
                        name=hashlib.sha256(url.encode('utf-8')).hexdigest()[:15]+'.html'
                        (saved_dir/name).write_text(page_html,encoding='utf-8')
                    soup=BeautifulSoup(page_html,'html.parser')
                    rows=extract(soup,url,args.depth+1)
                    store.add(rows)
                    log.append({'url':url,'depth':args.depth+1,'type':'product','status':'OK','products':len(rows),'links':0,'message':''})
                except Exception as exc:
                    log.append({'url':url,'depth':args.depth+1,'type':'product','status':'BLOCKED/FAILED','products':0,'links':0,'message':str(exc)[:450]})
    return store,log,nav


def write_csv(path,rows):
    if not rows:return
    cols=[k for k in rows[0] if k!='observations']
    with path.open('w',newline='',encoding='utf-8') as file:
        w=csv.DictWriter(file,fieldnames=cols,extrasaction='ignore');w.writeheader()
        for rec in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in rec.items()})


def render_dashboard(products,log,nav,settings):
    data=json.dumps(products,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    logs=json.dumps(log,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e')
    meta=json.dumps(settings,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e')
    # HTML is intentionally self-contained and works from file:// (no HTTP server required).
    template=r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ArbiScout · Local deal dashboard</title>
<style>
:root{color-scheme:light;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f3f5f8;color:#172333}
*{box-sizing:border-box}body{margin:0}header{background:#0c2544;color:#fff;padding:28px max(24px,calc((100vw - 1300px)/2))}header h1{margin:0;font-size:29px;letter-spacing:-.6px}header p{color:#c1d5ea;margin:6px 0 0;font-size:14px}
.wrap{max-width:1350px;padding:23px;margin:auto}.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.kpi{background:#fff;padding:18px;border:1px solid #e2e8f0;border-radius:12px}.kpi strong{font-size:29px;display:block}.kpi span{color:#62748a;font-size:12px}
.note{background:#fff9e6;border:1px solid #f1d38d;border-radius:9px;padding:13px 15px;color:#644a1a;font-size:13px;margin:18px 0}.controls{display:flex;flex-wrap:wrap;gap:9px;margin:16px 0;align-items:center}.controls input,.controls select{padding:11px;border-radius:8px;border:1px solid #cfd9e4;background:#fff;min-height:42px;font-size:14px}.controls input[type=search]{flex:1;min-width:200px}.controls label{display:flex;align-items:center;gap:6px;color:#45566e;font-size:13px}.controls label input{min-height:auto}
.btn{display:inline-block;padding:9px 13px;border-radius:7px;text-decoration:none;font-size:13px;font-weight:650;background:#1261bd;color:#fff;white-space:nowrap}.btn.ebay{background:#fff;border:1px solid #b9cce2;color:#17508d}.btn:hover{filter:brightness(.94)}
.tablewrap{overflow:auto;border:1px solid #e2e8f0;border-radius:12px;background:#fff}table{border-collapse:collapse;width:100%;min-width:1100px}th{background:#eaf0f8;font-size:12px;color:#50617a;position:sticky;top:0;padding:12px;text-align:left;white-space:nowrap}td{border-top:1px solid #e9edf3;padding:13px 12px;vertical-align:top;font-size:13px}tbody tr:hover{background:#f8fbff}.product{min-width:320px;max-width:480px}.product b{display:block;font-size:14px;line-height:1.45}.sub{color:#7a8898;font-size:11px;margin-top:6px;overflow-wrap:anywhere}.money{font-weight:700;font-size:15px;white-space:nowrap}.good{color:#08734a;font-weight:750}.muted{color:#8290a0}.warn{color:#9a630e;font-size:12px}.query{display:block;width:225px;border:1px solid #d6e0ea;padding:7px;margin-bottom:7px;border-radius:6px;font-size:12px}.small{font-size:11px;color:#738197}.diag{margin-top:28px;background:#fff;border:1px solid #dae4ef;border-radius:12px;padding:20px}.diag summary{cursor:pointer;font-weight:700}.diag pre{white-space:pre-wrap;font-size:12px;background:#f6f8fa;padding:12px;border-radius:6px;max-height:400px;overflow:auto}.count{color:#6b798c;font-size:13px}footer{color:#7d8da0;font-size:12px;padding:18px 0}
@media(max-width:760px){.kpis{grid-template-columns:repeat(2,1fr)}header{padding:24px}.wrap{padding:12px}.controls{align-items:stretch}.controls label{padding:4px}}
</style></head><body>
<header><h1>ArbiScout <span style="font-weight:400;color:#97bce7">/ Deal Explorer</span></h1><p>Local, deterministic price-discovery report · __CREATED__</p></header>
<main class="wrap">
<div class="kpis"><div class="kpi"><strong id="kTotal">0</strong><span>Unique products</span></div><div class="kpi"><strong id="kPriced">0</strong><span>With current price</span></div><div class="kpi"><strong id="kPaired">0</strong><span>With retail comparison price</span></div><div class="kpi"><strong id="kPages">0</strong><span>Successful pages analyzed</span></div></div>
<div class="note"><strong>Price meaning:</strong> “Savings” and “% off” compare the retailer's displayed current and regular prices; they are <em>not</em> eBay margins. eBay buttons open sold listings, newest first (typically up to 90 days). eBay does not expose a verified URL-only 30-day sold filter: inspect the most recent 30 days manually. Best Offer headline prices may differ from amounts actually paid. Prices may be stale, region-specific, or incomplete; verify before purchasing.</div>
<div class="controls"><input id="q" type="search" placeholder="Filter by product name, model, price…" aria-label="Filter products"><select id="sort"><option value="pct">Highest % off</option><option value="savings">Highest dollar savings</option><option value="price">Lowest current price</option><option value="price_desc">Highest current price</option><option value="title">Product name A–Z</option></select><label><input type="checkbox" id="complete"> Show only products with both prices</label><span id="displayCount" class="count"></span></div>
<div class="tablewrap"><table><thead><tr><th>Product</th><th>Current retail</th><th>Regular retail</th><th>% off</th><th>Retail savings</th><th>Product link</th><th>eBay sold search · editable</th></tr></thead><tbody id="rows"></tbody></table></div>
<div class="diag"><details><summary>Crawl log and incomplete-page diagnostics</summary><p class="small">A failed page is not an empty category; examine errors below. Saved HTML is a snapshot, not a live price check.</p><div id="logTable"></div></details></div>
<footer>Generated locally by ArbiScout. No LLM calls. No automatic purchasing. Query text is editable before opening eBay.</footer>
</main><script>
const data=__DATA__;const logs=__LOGS__;const settings=__META__;
const $=id=>document.getElementById(id);
const money=v=>v===null||v===undefined?'—':new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(v);
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');
const soldUrl=q=>'https://www.ebay.com/sch/i.html?'+new URLSearchParams({_nkw:q,LH_Sold:'1',LH_Complete:'1',_sop:'13',_ipg:'240'}).toString();
function updateEbay(input,id){const a=$(id);if(a)a.href=soldUrl(input.value.trim())}
function render(){let q=$('q').value.toLowerCase().trim();let rows=data.filter(x=>!q||[x.title,x.brand,x.model,x.sku,x.url].join(' ').toLowerCase().includes(q));if($('complete').checked)rows=rows.filter(x=>x.price_complete);
const sort=$('sort').value;rows.sort((a,b)=>{const num=(v,dir=1)=>(v===null||v===undefined?-Infinity:Number(v))*dir;let d=0;
if(sort==='pct')d=num(b.discount_percent)-num(a.discount_percent);if(sort==='savings')d=num(b.savings)-num(a.savings);if(sort==='price')d=(a.current_price??Infinity)-(b.current_price??Infinity);if(sort==='price_desc')d=num(b.current_price)-num(a.current_price);if(sort==='title')d=a.title.localeCompare(b.title);return d||a.title.localeCompare(b.title)});
$('displayCount').textContent=`Showing ${rows.length} of ${data.length}`;
$('rows').innerHTML=rows.map((r,i)=>{let id='eb'+i;let pct=r.discount_percent!==null?`${r.discount_percent.toFixed(1)}%`:r.advertised_percent!==null?`${r.advertised_percent.toFixed(1)}%*`:'—';let caution=[];if(r.variant_conflict)caution.push('Conflicting variant identities');if(r.price_conflict)caution.push('Multiple different prices observed');if(!r.price_complete)caution.push('Incomplete retail price comparison');return `<tr><td class="product"><b>${esc(r.title)}</b><div class="sub">${esc(r.key)} · found on ${r.seen_on.length} page(s)</div>${caution.length?`<div class="warn">${esc(caution.join(' · '))}</div>`:''}</td><td class="money">${money(r.current_price)}</td><td>${money(r.regular_price)}</td><td class="good">${esc(pct)}${r.discount_percent===null&&r.advertised_percent!==null?'<div class="small">*advertised only</div>':''}</td><td class="good">${money(r.savings)}</td><td><a class="btn" href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">View at store ↗</a></td><td><input class="query" id="inp${i}" aria-label="Edit eBay product query" value="${esc(r.ebay_query)}" oninput="updateEbay(this,'${id}')"><a class="btn ebay" id="${id}" href="${esc(r.ebay_url)}" target="_blank" rel="noopener noreferrer">eBay sold items ↗</a><div class="small">Newest first; review last 30 days</div></td></tr>`}).join('')||'<tr><td colspan="7" style="padding:40px;text-align:center">No matching products. Check crawl diagnostics or adjust filters.</td></tr>';
}
$('kTotal').textContent=data.length;$('kPriced').textContent=data.filter(x=>x.current_price!==null).length;$('kPaired').textContent=data.filter(x=>x.price_complete).length;$('kPages').textContent=logs.filter(x=>x.status==='OK').length;
$('logTable').innerHTML='<pre>'+esc(logs.map(x=>`[${x.status}] ${x.type} depth=${x.depth} products=${x.products} ${x.url}\n${x.message||''}`).join('\n\n'))+'</pre>';
for(const id of ['q','sort','complete'])$(id).addEventListener(id==='q'?'input':'change',render);render();
</script></body></html>'''
    return template.replace('__DATA__',data).replace('__LOGS__',logs).replace('__META__',meta).replace('__CREATED__',html.escape(datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')))


def main(argv=None):
    p=argparse.ArgumentParser(description='ArbiScout: crawl retailer sale pages and create a local sortable HTML report.')
    p.add_argument('url_pos',nargs='?',help='Sale/deals page URL')
    p.add_argument('--url',help='Sale/deals page URL')
    p.add_argument('--snapshot',help='Existing saved HTML file (starts from your file instead of requesting landing page)')
    p.add_argument('--snapshot-url',help='Original source page URL for --snapshot')
    p.add_argument('--offline',action='store_true',help='Read only --snapshot, no network access')
    p.add_argument('--save-html',action='store_true',help='Archive each downloaded HTML page to raw_pages/ for debugging')
    p.add_argument('--depth',type=int,default=2,help='Listing link depth (default: 2)')
    p.add_argument('--max-listings',type=int,default=12,help='Maximum secondary/tertiary listing pages (default: 12)')
    p.add_argument('--max-products',type=int,default=12,help='Maximum individual product page fallbacks (default: 12)')
    p.add_argument('--enrich-models',action='store_true',help='Also visit priced product pages lacking explicit model IDs')
    p.add_argument('--delay',type=float,default=1.5,help='Minimum seconds between fetches, >=0.7 (default 1.5)')
    p.add_argument('--timeout',type=int,default=20,help='Per-request timeout in seconds')
    p.add_argument('--mode',choices=['http','browser'],default='http',help='HTTP or optional Playwright-rendered browser')
    p.add_argument('--browser-visible',action='store_true',help='Show the browser window (some retailers serve product pages only to visible browsers)')
    p.add_argument('--outdir',default='arbiscout_output',help='Output directory')
    args=p.parse_args(argv)
    args.url=args.url or args.url_pos or args.snapshot_url
    if not args.url:p.error('Supply a sale-page URL, or --snapshot FILE --snapshot-url URL')
    if not is_safe_http(args.url):p.error('URL must be a public http(s) URL')
    if args.offline and not args.snapshot:p.error('--offline requires --snapshot')
    for k in ('depth','max_listings','max_products'):
        if getattr(args,k)<0:p.error(k+' must not be negative')
    print('ArbiScout crawling:',args.url,flush=True)
    try:store,log,nav=crawl(args)
    except RuntimeError as e:
        print('ERROR:',e,file=sys.stderr);return 2
    products=store.records()
    output=Path(args.outdir);output.mkdir(parents=True,exist_ok=True)
    (output/'index.html').write_text(render_dashboard(products,log,nav,vars(args)),encoding='utf-8')
    (output/'products.json').write_text(json.dumps(products,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (output/'crawl_log.json').write_text(json.dumps(log,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (output/'next_pages.json').write_text(json.dumps(sorted(nav.values(),key=lambda r:-r['score']),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    write_csv(output/'products.csv',products)
    ok=sum(x['status']=='OK' for x in log)
    print(f'Done: {len(products)} unique products; {sum(x["price_complete"] for x in products)} with retail price pairs; {ok} successful pages; {len(log)-ok} failed pages.')
    print('Open:',(output/'index.html').resolve())
    if len(log)>0 and any(x['status']!='OK' for x in log):print('See crawl_log.json for blocked or failed pages.')
    return 0

if __name__=='__main__':raise SystemExit(main())
