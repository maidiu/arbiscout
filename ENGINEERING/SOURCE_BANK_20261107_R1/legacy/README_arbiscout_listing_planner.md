# ArbiScout — listing-first crawl planner

**Local HTML snapshot prototype; zero HTTP requests and zero LLM calls.**

This is a deterministic offline planner made from the November 7, 2026 saved Best Buy Black Friday HTML. It turns a saved retailer deals page into:

1. `next_listing_pages.csv` — candidate next pages, prioritized as targeted deal/search listings, Top Deals, departments, Outlet, then promo pages. These are **links explicitly present in the saved page**, not invented URLs or proof that any destination contains products.
2. `products.jsonl` — product records deduplicated by Best Buy product-family ID, with current/previous price, percent-off label, source page, title, SKU where supplied, and whether price is complete.
3. `product_page_fallbacks.csv` — exact product URLs **only where no current price is available in any supplied snapshot**. This is a deferred queue, NOT a request to fetch all 94 product pages immediately.
4. `summary.json` — counts, next-page types, and quality caveats.

## Install once

```sh
python3 -m pip install beautifulsoup4 lxml
```

## Analyze the uploaded Best Buy page

Place `arbiscout_crawl_planner.py` in the same folder as your saved Best Buy HTML and run:

```sh
python3 arbiscout_crawl_planner.py \
  --snapshot 'Best Buy Black Friday 2026 is Nov. 26–27.html::https://www.bestbuy.com/black-friday' \
  --outdir crawl_plan
```

Open `crawl_plan/next_listing_pages.csv`. For an initial experiment, manually visit one or two *listing* URLs from that file, allow the listing to load normally, then save each as HTML on your Mac. Do not save a merely empty/blocked page and assume it has product data.

## Add more listing-page snapshots

```sh
python3 arbiscout_crawl_planner.py \
  --snapshot 'Best Buy Black Friday 2026 is Nov. 26–27.html::https://www.bestbuy.com/black-friday' \
  --snapshot 'saved-top-deals.html::https://www.bestbuy.com/site/top-deals/top-100-deals-this-season/pcmcat1765308864276.c?id=pcmcat1765308864276' \
  --outdir crawl_plan
```

The tool merges identical product IDs across snapshots, retains the list of pages where seen, and uses a later snapshot's non-null current price to complete an otherwise unpriced product. It **flags** conflicting prices across source pages. Multiple conflicting explicit SKU variants under one product family ID are blocked from price-complete status, pending exact-variant handling. One product-family ID or title alone does **not** establish a valid exact eBay SKU match.

## Current snapshot audit

- Product cards: 152; unique product-family IDs: 131.
- Current + previous price pairs: 37; missing **current** price: 94.
- Of those 94 unpriced, 69 carry an advertised percentage-off label (not a recoverable dollar price without a verified baseline).
- 49 useful unique next listing URLs found: 4 filtered-deal, 3 Top Deals, 23 on-sale departments, 2 Outlet, 17 promotional collections.
- These 49 are **suggested links**; none were downloaded or tested from this planner.

## Intended eventual unattended architecture

`permitted initial page/download → parse navigation links → rank department/deal pages → obtain permitted list pages → extract product ID/SKU/price and source → reconcile products across pages → fetch specific product pages ONLY for unresolved high-value records → exact-product eBay historical sale lookup → conservative price gap → daily report`

Implement network downloading as a separate **permitted-source adapter** with site-specific access authorization, low request ceilings, backoff on ordinary errors, no evasion, robots inspection where applicable, and cache/freshness control. This prototype intentionally does **not** make HTTP requests or run Playwright. HTML saved in Chrome can already contain JavaScript-rendered content and is not proof that `requests.get()` would retrieve identical content automatically.

**No LLM necessary** for the document-tree navigation, product extraction, pagination, deduplication, missing-value tracking, scheduling or price arithmetic. LLMs might eventually be useful for ambiguous model matching; if uncertain the pipeline should reject instead of guessing.

## Test

```sh
python3 -m unittest -v test_crawl_planner
```

Five tests verify link selection, price completion after a second saved listing, variant-conflict refusal, external-domain refusal and listing-page prioritization.

## Scope and limitations

- `product_page_fallbacks.csv` is a *last resort* queue after relevant listing pages have been tried, not an instruction to browse every SKU.
- Product-family ID may not be equivalent to exact variation identity. Validate SKU/GTIN/MPN and condition before eBay comparisons.
- Percent-off badge is a marketing label, not reliable actual purchase cost or eBay value.
- Different stores, signed-in status, local ZIP, coupons, shipping and tax may change the actual purchasable price.
- No live crawling authorization, dynamic pricing completeness, product availability or comparative eBay accuracy is proved by this offline run.
