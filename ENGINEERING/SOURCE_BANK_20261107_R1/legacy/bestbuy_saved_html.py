#!/usr/bin/env python3
"""Extract Best Buy product cards from a locally saved page HTML snapshot.

No network calls. Not a live inventory check, historical sale-price source, or
permission for automated collection of additional pages.

Requires: pip install beautifulsoup4 lxml
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup

MONEY = re.compile(r'\$\s*([\d,]+(?:\.\d{2})?)')
PERCENT = re.compile(r'(\d+(?:\.\d+)?)\s*%\s*off', re.I)
PRODUCT_ID = re.compile(r'/product/[^/?#]+/([^/?#]+)')
SKU = re.compile(r'/sku/(\d+)(?:/|$)')
SOURCE_PAGE = 'https://www.bestbuy.com/black-friday'


def first_money(element):
    if element is None:
        return None
    match = MONEY.search(element.get_text(' ', strip=True))
    if not match:
        return None
    return str(Decimal(match.group(1).replace(',', '')).quantize(Decimal('.01')))


def extract(path):
    p = Path(path)
    soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'lxml')
    cards = soup.select('[data-testid="product-card"]')
    extracted_at = datetime.now(timezone.utc).isoformat()
    records = {}
    for card in cards:
        title_container = card.select_one('[data-testid="product-card-title-link"]')
        if title_container is None:
            continue
        # Best Buy uses both <a data-testid=...> and a <div data-testid=...>
        # containing <a data-testid="ProductCard-ProductCardTitle-TestID">.
        title_link = title_container if title_container.name == 'a' and title_container.has_attr('href') else title_container.select_one('a[href]')
        if title_link is None:
            continue
        url = title_link.get('href', '').strip()
        if not url.startswith('https://www.bestbuy.com/product/'):
            continue
        pid_match = PRODUCT_ID.search(urlsplit(url).path)
        if not pid_match:
            continue
        pid = pid_match.group(1)
        sku_match = SKU.search(urlsplit(url).path)
        percent_tag = card.select_one('[data-testid="product-card-percent-off"]')
        percent_match = PERCENT.search(percent_tag.get_text(' ', strip=True)) if percent_tag else None
        rec = {
            'retailer': 'Best Buy',
            'product_id': pid,
            'sku': sku_match.group(1) if sku_match else None,
            'title': title_link.get('aria-label') or title_link.get_text(' ', strip=True),
            'url': url,
            'price_usd': first_money(card.select_one('[data-testid="price-block-customer-price"]')),
            'previous_price_usd': first_money(card.select_one('[data-testid="price-block-regular-price"]')),
            'advertised_discount_percent': float(percent_match.group(1)) if percent_match else None,
            'price_complete': False,
            'source_page': SOURCE_PAGE,
            'source_kind': 'locally_saved_html_snapshot',
            'source_file': p.name,
            'extracted_at_utc': extracted_at,
            'card_occurrences': 1,
        }
        rec['price_complete'] = rec['price_usd'] is not None and rec['previous_price_usd'] is not None
        if pid not in records:
            records[pid] = rec
            continue
        old = records[pid]
        old['card_occurrences'] += 1
        # Preserve priced variant when the same product appears multiple times.
        if rec['price_complete'] and not old['price_complete']:
            for field in ('price_usd', 'previous_price_usd', 'price_complete'):
                old[field] = rec[field]
        if old['sku'] is None and rec['sku'] is not None:
            old['sku'] = rec['sku']
            old['url'] = rec['url']
        if old['advertised_discount_percent'] is None:
            old['advertised_discount_percent'] = rec['advertised_discount_percent']
    return cards, list(records.values())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--file', required=True, help='Saved Best Buy .html file (no network)')
    ap.add_argument('--output', required=True, help='Output JSONL, one record per unique product')
    args = ap.parse_args()
    cards, records = extract(args.file)
    target = Path(args.output)
    with target.open('w', encoding='utf-8') as out:
        for rec in records:
            out.write(json.dumps(rec, ensure_ascii=False) + '\n')
    priced = sum(x['price_complete'] for x in records)
    print(f'Cards found: {len(cards)}')
    print(f'Unique products: {len(records)}')
    print(f'Duplicate cards removed: {len(cards)-len(records)}')
    print(f'Unique products with both current and previous prices: {priced}')
    print(f'Unique products with incomplete prices: {len(records)-priced}')
    print(f'Output: {target}')
    print('CAUTION: Saved-page historical snapshot, not a fresh checkout/stock check.')


if __name__ == '__main__':
    main()
