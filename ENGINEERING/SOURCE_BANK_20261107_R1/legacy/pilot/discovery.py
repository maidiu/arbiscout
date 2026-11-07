#!/usr/bin/env python3
"""ArbiScout $0 source discovery pilot. No eBay, payments, logins or bypasses.

Modes:
  rss        One public RSS/Atom feed -> JSONL discovery leads, not verified purchases.
  html-file  Parse an already saved HTML page with explicit CSS selectors.
  crawl      Bounded public HTML collection ONLY for a source whose permission
             you have verified. Checks robots.txt and stops on server errors.

Dependency for HTML parsing: beautifulsoup4 (open-source, free).
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

USER_AGENT = 'ArbiScout-Research-Pilot/0.1 (single-purpose low-rate crawler)'
PRICE_RE = re.compile(r'(?<!\w)\$\s*(\d{1,5}(?:,\d{3})*(?:\.\d{1,2})?)(?!\d)')
MAX_BYTES = 3_000_000


def now():
    return datetime.now(timezone.utc).isoformat()


def money(text):
    if not text:
        return None
    match = PRICE_RE.search(str(text))
    if not match:
        return None
    return float(match.group(1).replace(',', ''))


def plain(elem, path):
    node = elem.find(path)
    return ''.join(node.itertext()).strip() if node is not None else ''


def parse_rss(xml_data, source_url, limit=100):
    """Never call this an original retailer price or a merchant-verified discount."""
    root = ET.fromstring(xml_data)
    items = root.findall('.//channel/item')
    if not items:
        items = root.findall('.//{http://www.w3.org/2005/Atom}entry')
    out = []
    for item in items[:limit]:
        is_atom = item.tag.endswith('entry')
        if is_atom:
            ns = '{http://www.w3.org/2005/Atom}'
            title = plain(item, ns + 'title')
            links = item.findall(ns + 'link')
            link = next((n.attrib.get('href','') for n in links if n.attrib.get('rel','alternate')=='alternate'), '')
            if not link and links: link = links[0].attrib.get('href','')
            published = plain(item, ns + 'updated') or plain(item, ns + 'published')
        else:
            title = plain(item, 'title')
            link = plain(item, 'link')
            published = plain(item, 'pubDate')
        if not title or not link:
            continue
        out.append({'source_kind':'curated_deal_feed', 'source_url':source_url,
                    'original_title':title, 'original_link':link,
                    'published':published or None, 'observed_at':now(),
                    'price_hint_from_title_usd':money(title),
                    'merchant_verified_price_usd':None,
                    'mpn':None,'gtin':None,'condition':None,
                    'suitable_for_ebay_match':False,
                    'reason':'lead only; exact item and original merchant purchase price not verified'})
    return out


def _value(node, selector, attr=None):
    if not selector:
        return None
    found = node.select_one(selector)
    if found is None:
        return None
    return (found.get(attr) if attr else found.get_text(' ', strip=True)) or None


def parse_cards(html, page_url, config):
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise RuntimeError('Run: python3 -m pip install beautifulsoup4') from exc
    soup = BeautifulSoup(html, 'html.parser')
    selector = config['card_selector']
    cards = []
    for card in soup.select(selector):
        title = _value(card,config.get('title_selector'))
        product_link = _value(card,config.get('link_selector'),config.get('link_attribute','href'))
        if not title or not product_link:
            continue
        product_link = urllib.parse.urljoin(page_url,product_link)
        if urllib.parse.urlsplit(product_link).scheme not in ('http','https'):
            continue
        sale = money(_value(card,config.get('sale_price_selector')))
        regular = money(_value(card,config.get('regular_price_selector')))
        mpn = _value(card,config.get('mpn_selector'),config.get('mpn_attribute'))
        gtin = _value(card,config.get('gtin_selector'),config.get('gtin_attribute'))
        is_discount = bool(sale is not None and regular is not None and regular > sale > 0)
        cards.append({'source_kind':'retailer_html', 'source_url':page_url,
                      'original_title':title, 'original_link':product_link,
                      'observed_at':now(), 'price_hint_from_page_usd':sale,
                      'regular_price_on_page_usd':regular,
                      'verified_markdown_on_page':is_discount,
                      'merchant_verified_price_usd':None,
                      'mpn':mpn,'gtin':gtin,'condition':None,
                      'suitable_for_ebay_match':False,
                      'reason':'observed page, not original checkout verification or eBay match'})
    nxt = _value(soup,config.get('next_selector'),'href')
    next_url = urllib.parse.urljoin(page_url,nxt) if nxt else None
    if next_url and urllib.parse.urlsplit(next_url).netloc != urllib.parse.urlsplit(page_url).netloc:
        next_url = None
    return cards,next_url


def fetch(url, timeout=15):
    urlbits = urllib.parse.urlsplit(url)
    if urlbits.scheme != 'https' or not urlbits.netloc:
        raise ValueError('Only HTTPS URLs are supported for live retrieval')
    req = urllib.request.Request(url,headers={'User-Agent':USER_AGENT,'Accept':'application/rss+xml,application/atom+xml,application/xml,text/html,*/*'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f'HTTP {resp.status}: stop')
        final = resp.geturl()
        if urllib.parse.urlsplit(final).netloc != urlbits.netloc:
            raise RuntimeError('Cross-host redirects not allowed for this pilot')
        body = resp.read(MAX_BYTES+1)
        if len(body)>MAX_BYTES:
            raise RuntimeError('Response exceeds 3 MB cap')
        return body


def assert_robots_allowed(url):
    parsed=urllib.parse.urlsplit(url)
    robots=urllib.parse.urlunsplit((parsed.scheme,parsed.netloc,'/robots.txt','',''))
    # Explicitly refuse a missing/failed robots retrieval rather than treating it as permission.
    try:
        raw=fetch(robots).decode('utf-8','replace')
    except Exception as exc:
        raise RuntimeError(f'Cannot verify robots.txt ({exc}); stop') from exc
    rp=urllib.robotparser.RobotFileParser()
    rp.parse(raw.splitlines())
    if not rp.can_fetch(USER_AGENT,url):
        raise RuntimeError('robots.txt does not permit this URL for our user agent; stop')
    return rp.crawl_delay(USER_AGENT)


def crawl(url,config,max_pages,delay):
    origin=urllib.parse.urlsplit(url).netloc
    seen=set(); results=[]; pages=0
    while url and pages < max_pages:
        if url in seen: break
        if urllib.parse.urlsplit(url).netloc != origin: break
        seen.add(url)
        robot_delay=assert_robots_allowed(url)
        if robot_delay is not None: delay=max(delay,robot_delay)
        if pages: time.sleep(delay)
        body=fetch(url)
        rows,url=parse_cards(body,url,config)
        results.extend(rows); pages+=1
    return results


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    sub=p.add_subparsers(dest='mode',required=True)
    r=sub.add_parser('rss',help='Read one public RSS/Atom feed')
    r.add_argument('--url',required=True);r.add_argument('--max-items',type=int,default=100)
    h=sub.add_parser('html-file',help='Parse a locally saved retailer HTML file')
    h.add_argument('--file',required=True);h.add_argument('--url',required=True);h.add_argument('--config',required=True)
    c=sub.add_parser('crawl',help='Bounded, robots-checked live HTML crawl, permission required')
    c.add_argument('--url',required=True);c.add_argument('--config',required=True)
    c.add_argument('--max-pages',type=int,default=2);c.add_argument('--delay',type=float,default=2)
    c.add_argument('--i-verified-permission',action='store_true')
    p.add_argument('--output',default='candidates.jsonl')
    a=p.parse_args()
    if a.mode=='rss':
        rows=parse_rss(fetch(a.url),a.url,limit=max(1,min(a.max_items,500)))
    elif a.mode=='html-file':
        config=json.loads(Path(a.config).read_text())
        rows,_=parse_cards(Path(a.file).read_text(encoding='utf-8'),a.url,config)
    else:
        if not a.i_verified_permission:
            p.error('Live HTML crawls require --i-verified-permission; review site terms first')
        config=json.loads(Path(a.config).read_text())
        rows=crawl(a.url,config,max_pages=max(1,min(a.max_pages,5)),delay=max(1.5,a.delay))
    seen=set();unique=[]
    for row in rows:
        key=(row['source_kind'],row['original_link'])
        if key not in seen:
            unique.append(row);seen.add(key)
    with open(a.output,'w',encoding='utf-8') as fp:
        for row in unique:
            fp.write(json.dumps(row,ensure_ascii=False)+'\n')
    print(f'{len(unique)} leads -> {a.output}; 0 checkout-confirmed / 0 eBay-verified',file=sys.stderr)

if __name__=='__main__':
    main()
