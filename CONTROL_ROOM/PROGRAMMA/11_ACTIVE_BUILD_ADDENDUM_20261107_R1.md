# Active build addendum — 2026-11-07 R1

**Status: LOCAL_PROTOTYPE_DRAFT / USER-SAVED EBAY PAGES / BOUNDED LIVE BEST BUY LISTING RUN / NO AUTOMATED EBAY SOLD FETCH / NO INDEPENDENT REVIEW / NOT MERGED.**

This addendum records the active local build on `work/arbiscout-local-build`. It is additive to the historical 20-to-10 receipt and does not upgrade any live-evidence or rights claim.

## What is runnable

- **Browser-mode retailer fetch:** installed Chrome, lazy-price settling, raw-page capture and no individual product-page fallback. A bounded Best Buy listing run on 2026-11-07 produced **137 unique products, 74 complete price pairs, 12 listing pages and 0 failed pages**.
- **eBay evidence intake:** a local watcher reads only HTML the user manually saves into `ebay_saved/` or `~/Downloads`, matches pages to retailer candidates by the eBay search query, parses them and regenerates reports. It never fetches eBay. Probe: **25 saved files, 20 matched, 8 positive provisional gaps**.
- **Distribution output:** sold low, high, mean, median and middle-50% range, plus whether the current retailer price is below the sold low or median.
- **Unified catalog:** merges Best Buy, Meh, Woot and Kroger outputs with source and category filters, discount/savings/price sorting and a top-N selection written to `catalog/selected/`.
- **Provider adapters:** `providers.py` supports Meh, Woot and Kroger with user-supplied keys. Local execution produced: Meh **1 current item**; Woot feed `All` **~5000 live offers** (capped to 500); Kroger **6 promoted products** for milk/eggs/bread at ZIP 29072.
- **Non-food Kroger probe:** at ZIP 29072, batteries and LED bulbs returned promoted prices; air fryer, headphones, vacuum, storage bins, cookware, LEGO, printer and power bank returned no promoted products. This is one location, not a national category claim.
- **Tests:** 21 executed, 20 passed, 1 skipped (private Best Buy snapshot).

## Evidence limits

- Displayed eBay sold prices remain provisional; accepted Best Offers are excluded and actual paid amounts are unverified.
- Gaps are **gross only**: eBay fees, shipping, tax, returns and net margin are not included.
- Provider credentials are local, `.env` is ignored, `.env.example` lists names only, and keys are not printed or committed. Provider terms, coverage and research-use permission are not independently reviewed.
- Automated eBay `/sch/` retrieval remains disallowed by robots. The watcher is a local file reader, not an eBay client.

## PROGRAMMA effects

- Work registry: `ARB-100`–`ARB-105` added; `ARB-020`, `ARB-031`, `ARB-040`, `ARB-050`, `ARB-051`, `ARB-060`, `ARB-071`, `ARB-080`, `ARB-081` updated.
- Source registry: `E-MEH-API`, `E-WOOT-API`, `E-KROGER-API`, `E-EBAY-SAVED-SOLD` added.
- Acceptance matrix: `A03`–`A07`, `A12` updated; `A13` and `A14` added.
