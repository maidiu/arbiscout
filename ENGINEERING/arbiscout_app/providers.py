#!/usr/bin/env python3
"""API adapters for Meh, Woot, and Kroger.

Reads keys from .env or the environment, fetches live deals, and writes the
same products.json/crawl_log.json/index.html layout used by the crawler.
No key is printed or stored by this program.
"""
from __future__ import annotations
import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import ssl
import sys
import time
from urllib.parse import quote, urlencode, urljoin
from urllib.request import Request, urlopen

import arbiscout as app

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

USER_AGENT = "ArbiScoutPersonal/0.2 (provider adapter; read-only research)"
ROOT = Path(__file__).resolve().parent


def load_env(path=ROOT / ".env"):
    if not Path(path).is_file():
        return
    for raw in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[7:].strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key, value)


def env(*names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value.strip()
    return ""


def http_json(url, headers=None, method="GET", body=None, timeout=30):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json",
                                    **(headers or {})}, method=method)
    if body is not None:
        request.data = body.encode("utf-8") if isinstance(body, str) else body
    with urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
        payload = response.read(8_000_001)
        if len(payload) > 8_000_000:
            raise RuntimeError("Provider response larger than safe maximum")
        return json.loads(payload.decode("utf-8", errors="replace"))


def number(*values):
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            return round(float(value), 2)
        if isinstance(value, str):
            match = re.search(r"\d[\d,]*(?:\.\d+)?", value)
            if match:
                try:
                    return round(float(match.group().replace(",", "")), 2)
                except ValueError:
                    continue
    return None


def variant_text(item):
    attributes = item.get("attributes") or item.get("Attributes") or {}
    pairs = []
    if isinstance(attributes, dict):
        pairs = [f"{k}: {v}" for k, v in attributes.items()]
    elif isinstance(attributes, list):
        pairs = [f"{a.get('key') or a.get('Key')}: {a.get('value') or a.get('Value')}"
                 for a in attributes if isinstance(a, dict)]
    return ", ".join(str(p) for p in pairs if p and "None" not in p)


def build_records(raw):
    store = app.Store()
    for entry in raw:
        record = app._make_record(
            entry["url"], entry["title"], entry.get("source", entry["url"]), 0,
            entry.get("kind", "api"), entry.get("current"), entry.get("regular"),
            entry.get("percent"), entry.get("model"), entry.get("brand"),
            entry.get("sku"), entry.get("condition"))
        if record:
            record["category"] = entry.get("category")
            store.add([record])
    return store.records()


WOOT_CATEGORIES = {
    "computers": "Computers & Tablets",
    "pc": "Computers & Tablets",
    "tech": "Electronics",
    "electronics": "Electronics",
    "home": "Home & Outdoor",
    "tools": "Home & Outdoor",
    "sports": "Sports & Outdoors",
    "sport": "Sports & Outdoors",
    "shirts": "Apparel",
    "shirt": "Apparel",
    "gourmet": "Grocery & Household",
    "clearance": "Clearance",
    "featured": "Featured",
    "wootoff": "Woot Off",
    "all": "",
    "woot": "",
}


def woot_category(categories):
    if not categories:
        return None
    top = str(categories[0]).split("/")[0].strip().lower()
    return WOOT_CATEGORIES.get(top) or None


def woot_price(value):
    if isinstance(value, dict):
        return number(value.get("Minimum"), value.get("Maximum"))
    return number(value)


def woot_condition(variant, feed_item, detail):
    attributes = variant.get("Attributes") or []
    if isinstance(attributes, list):
        for attribute in attributes:
            if isinstance(attribute, dict) and str(attribute.get("Key", "")).lower() == "condition":
                return attribute.get("Value")
    return feed_item.get("Condition") or detail.get("Condition")


def fetch_meh():
    key = env("MEH_API_KEY", "MEH_KEY")
    if not key:
        raise SystemExit("Missing MEH_API_KEY in .env or the environment.")
    url = "https://meh.com/api/1/current.json?" + urlencode({"apikey": key})
    data = http_json(url)
    deal = data.get("deal") or data
    if deal.get("soldOutAt"):
        return [], "https://meh.com", "Current Meh deal is sold out"
    base_url = urljoin("https://meh.com", deal.get("url") or "/")
    title = deal.get("title") or "Meh deal"
    items = deal.get("items") or []
    raw = []
    for item in items:
        if not isinstance(item, dict):
            continue
        current = number(item.get("price"), item.get("salePrice"), item.get("currentPrice"),
                         deal.get("price"), deal.get("salePrice"))
        regular = number(item.get("msrp"), item.get("listPrice"), item.get("regularPrice"),
                         deal.get("msrp"), deal.get("listPrice"))
        if current is None:
            continue
        if regular is not None and regular <= current:
            regular = None
        sku = item.get("id") or item.get("sku")
        suffix = variant_text(item)
        item_title = item.get("title") or title
        if suffix and suffix.lower() not in item_title.lower():
            item_title = f"{item_title} - {suffix}"
        item_url = base_url + (("&" if "?" in base_url else "?") + "item=" + quote(str(sku)) if sku else "")
        raw.append({"url": item_url, "title": item_title, "current": current, "regular": regular,
                    "sku": sku, "condition": item.get("condition"), "source": "https://meh.com",
                    "kind": "meh_api", "brand": None, "model": None, "category": "Daily Deal"})
    if not raw:
        current = number(deal.get("price"), deal.get("salePrice"))
        regular = number(deal.get("msrp"), deal.get("listPrice"))
        if current is not None:
            if regular is not None and regular <= current:
                regular = None
            raw.append({"url": base_url, "title": title, "current": current, "regular": regular,
                        "source": "https://meh.com", "kind": "meh_api", "category": "Daily Deal"})
    return raw, url.split("?")[0], f"Meh current deal: {len(raw)} item(s)"


def fetch_woot(feed="All", limit=500):
    key = env("WOOT_API_KEY", "WOOT_KEY")
    if not key:
        raise SystemExit("Missing WOOT_API_KEY in .env or the environment.")
    feed = feed or "All"
    url = f"https://developer.woot.com/feed/{quote(feed)}"
    data = http_json(url, headers={"x-api-key": key})
    feed_items = [item for item in (data.get("Items") or [])
                  if isinstance(item, dict) and not item.get("IsSoldOut")]
    if limit and len(feed_items) > limit:
        def feed_score(item):
            sale = woot_price(item.get("SalePrice"))
            listing = woot_price(item.get("ListPrice"))
            discount = ((listing - sale) / listing * 100) if sale and listing and listing > sale else None
            savings = (listing - sale) if sale and listing and listing > sale else None
            return (-(discount if discount is not None else -1),
                    -(savings if savings is not None else 0))
        feed_items.sort(key=feed_score)
        feed_items = feed_items[:limit]
    details = {}
    offer_ids = [item.get("OfferId") for item in feed_items if item.get("OfferId")]
    for start in range(0, len(offer_ids), 25):
        batch = offer_ids[start:start + 25]
        try:
            offers = http_json("https://developer.woot.com/getoffers",
                               headers={"x-api-key": key,
                                        "Content-Type": "application/json"},
                               method="POST", body=json.dumps(batch))
            for offer in offers or []:
                if isinstance(offer, dict) and offer.get("Id"):
                    details[offer["Id"]] = offer
        except Exception as exc:
            print(f"Woot detail enrichment failed for {len(batch)} offers: {exc}",
                  file=sys.stderr)
        if start + 25 < len(offer_ids):
            time.sleep(1.1)
    raw = []
    for item in feed_items:
        offer_id = item.get("OfferId")
        detail = details.get(offer_id) or {}
        category = woot_category(item.get("Categories"))
        base_url = item.get("Url") or detail.get("Url")
        variants = [variant for variant in (detail.get("Items") or [])
                    if isinstance(variant, dict)]
        if variants:
            groups = {}
            for variant in variants:
                current = woot_price(variant.get("SalePrice"))
                regular = woot_price(variant.get("ListPrice"))
                if current is None:
                    continue
                if regular is not None and regular <= current:
                    regular = None
                if len(variants) == 1:
                    base_title = (item.get("Title") or detail.get("FullTitle")
                                  or variant.get("Title") or "Woot offer")
                else:
                    base_title = (variant.get("Title") or detail.get("FullTitle")
                                  or item.get("Title") or "Woot offer")
                groups.setdefault((base_title, current, regular), []).append(variant)
            title_counts = {}
            for base_title, _current, _regular in groups:
                title_counts[base_title] = title_counts.get(base_title, 0) + 1
            for (base_title, current, regular), group in groups.items():
                variant = group[0]
                title = base_title
                suffix = variant_text(variant)
                if title_counts.get(base_title, 0) > 1 and suffix and suffix.lower() not in title.lower():
                    title = f"{title} - {suffix}"
                sku = variant.get("Id") or offer_id
                variant_url = base_url + (("&" if "?" in base_url else "?")
                                          + "variant=" + quote(str(sku)) if sku else "")
                raw.append({"url": variant_url, "title": title,
                            "current": current, "regular": regular, "sku": sku,
                            "condition": woot_condition(variant, item, detail),
                            "source": "https://woot.com", "kind": "woot_api",
                            "brand": None, "model": None, "category": category})
            continue
        sale = item.get("SalePrice")
        listing = item.get("ListPrice")
        current = woot_price(sale)
        regular = woot_price(listing)
        if current is None:
            continue
        if regular is not None and regular <= current:
            regular = None
        raw.append({"url": base_url, "title": item.get("Title") or "Woot offer",
                    "current": current, "regular": regular, "sku": offer_id,
                    "condition": item.get("Condition"), "source": "https://woot.com",
                    "kind": "woot_api", "brand": None, "model": None,
                    "category": category})
    return raw, url, f"Woot feed {feed}: {len(raw)} live item(s) from {len(feed_items)} offer(s)"


def kroger_token(client_id, client_secret):
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urlencode({"grant_type": "client_credentials", "scope": "product.compact"})
    data = http_json("https://api.kroger.com/v1/connect/oauth2/token",
                     headers={"Authorization": "Basic " + basic,
                              "Content-Type": "application/x-www-form-urlencoded"},
                     method="POST", body=body)
    token = data.get("access_token")
    if not token:
        raise SystemExit("Kroger token request failed: " + json.dumps(data)[:300])
    return token


def kroger_location(token, location_id="", zip_code=""):
    if location_id:
        return location_id
    if not zip_code:
        raise SystemExit("Set KROGER_LOCATION_ID or KROGER_ZIP (or pass --location-id/--zip).")
    url = "https://api.kroger.com/v1/locations?" + urlencode(
        {"filter.zipCode.near": zip_code, "filter.limit": 1})
    data = http_json(url, headers={"Authorization": "Bearer " + token})
    locations = data.get("data") or []
    if not locations:
        raise SystemExit("Kroger found no store for ZIP " + zip_code)
    return locations[0].get("locationId")


def fetch_kroger(terms, location_id="", zip_code="", limit=50):
    client_id = env("KROGER_CLIENT_ID")
    client_secret = env("KROGER_CLIENT_SECRET", "KROGER_SECRET")
    if not client_id or not client_secret:
        raise SystemExit("Missing KROGER_CLIENT_ID or KROGER_CLIENT_SECRET in .env.")
    if not terms:
        raise SystemExit("Set KROGER_TERMS (comma-separated) or pass --terms.")
    token = kroger_token(client_id, client_secret)
    location_id = kroger_location(token, location_id, zip_code or env("KROGER_ZIP"))
    source_url = "https://api.kroger.com/v1/products"
    raw = []
    seen = set()
    for term in terms:
        url = "https://api.kroger.com/v1/products?" + urlencode(
            {"filter.term": term, "filter.locationId": location_id, "filter.limit": limit})
        data = http_json(url, headers={"Authorization": "Bearer " + token})
        for product in data.get("data") or []:
            product_id = product.get("productId") or product.get("upc")
            if not product_id or product_id in seen:
                continue
            uri = product.get("productPageURI")
            if not uri:
                continue
            chosen = None
            for item in product.get("items") or []:
                price = item.get("price") or {}
                regular = number(price.get("regular"))
                promo = number(price.get("promo"))
                if regular is None:
                    continue
                current = promo if promo and 0 < promo < regular else regular
                if current is None or current >= regular:
                    continue
                chosen = (current, regular, item)
                break
            if not chosen:
                continue
            seen.add(product_id)
            current, regular, item = chosen
            categories = product.get("categories") or ["Grocery"]
            raw.append({"url": urljoin("https://www.kroger.com", uri),
                        "title": product.get("description") or "Kroger product",
                        "current": current, "regular": regular, "sku": product_id,
                        "brand": product.get("brand"), "condition": "New",
                        "source": "https://www.kroger.com", "kind": "kroger_api",
                        "model": None, "category": str(categories[0]).title()})
        time.sleep(0.4)
    return raw, source_url, f"Kroger search: {len(raw)} promoted product(s)"


def write_output(output, products, source, source_url, message):
    output = Path(output)
    retailer = output / "retailer"
    retailer.mkdir(parents=True, exist_ok=True)
    log = [{"url": source_url, "depth": 0, "type": "api", "status": "OK",
            "products": len(products), "links": 0, "message": message}]
    settings = {"source": source, "url": source_url,
                "fetched_at": datetime.now(timezone.utc).isoformat()}
    (retailer / "products.json").write_text(
        json.dumps(products, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (retailer / "crawl_log.json").write_text(
        json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (retailer / "next_pages.json").write_text("[]\n", encoding="utf-8")
    app.write_csv(retailer / "products.csv", products)
    (retailer / "index.html").write_text(
        app.render_dashboard(products, log, {}, settings), encoding="utf-8")
    print(f"{source}: {len(products)} products with prices")
    print("Dashboard:", (retailer / "index.html").resolve())
    return products


def main(argv=None):
    load_env()
    parser = argparse.ArgumentParser(description="Fetch deals from Meh, Woot, or Kroger")
    parser.add_argument("--source", required=True, choices=["meh", "woot", "kroger"])
    parser.add_argument("--output", help="Output folder (default: <source>_live)")
    parser.add_argument("--feed", default="All", help="Woot feed name (default: All)")
    parser.add_argument("--terms", help="Kroger search terms, comma-separated")
    parser.add_argument("--location-id", help="Kroger location ID")
    parser.add_argument("--zip", help="Kroger ZIP code used to find a store")
    parser.add_argument("--limit", type=int, default=50, help="Kroger results per term")
    parser.add_argument("--max-products", type=int, default=500,
                        help="Cap products written to the dashboard (default 500)")
    args = parser.parse_args(argv)
    output = args.output or (args.source + "_live")
    if args.source == "meh":
        raw, source_url, message = fetch_meh()
    elif args.source == "woot":
        raw, source_url, message = fetch_woot(args.feed, args.max_products)
    else:
        terms = [t.strip() for t in (args.terms or env("KROGER_TERMS")).split(",") if t.strip()]
        raw, source_url, message = fetch_kroger(terms, args.location_id, args.zip, args.limit)
    products = build_records(raw)
    if args.max_products and len(products) > args.max_products:
        products.sort(key=lambda r: (-(r.get("discount_percent") or 0),
                                     -(r.get("savings") or 0), r.get("title", "")))
        products = products[:args.max_products]
    write_output(output, products, args.source, source_url, message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
