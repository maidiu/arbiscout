# ARB-020-F1 — Actual source-free parser technical proof; no site scraping
**Executed 2026-10-31 in verified container runner, Python 3.13.5.** `python3 -m unittest -v arb020_f1_fixture_proof`: **8/8 PASS, 0.001 sec**. This execution used **hand-authored synthetic fixtures only**. No credentials, HTTP requests, paid calls, website product pages, real GTINs, retailer inventory, checkout or robots-limited targets were accessed. The actual standalone test file is also attached in this conversation as `arb020_f1_fixture_proof.py`; container path `/mnt/data/arb020_f1_fixture_proof.py` during execution. It is not represented as a deployed Mac integration.

## Four parser cases (minimum three required)
1. **Official Best Buy JSON product list**: `products[]`, SKU, UPC, modelNumber, `salePrice`, `regularPrice`, `onSale`, onlineAvailability; normalize synthetic values. Require actual sale price < regular price, neither MSRP nor a boolean flag alone establishes markdown. No live API entitlement claimed.
2. **WooCommerce Store API JSON**: `GET /wp-json/wc/store/v1/products?on_sale=true&page=1&per_page=100`, `prices.price` and `prices.regular_price` are **currency minor units** and must be converted using `currency_minor_unit`; `sku`, `is_in_stock`, `permalink`. GTIN is optional and **null by default** unless documented separately. In reality check `X-WP-TotalPages` and `Link` headers; no network access in test.
3. **Approved affiliate/merchant feed CSV**: parse `merchant_product_id,product_name,mpn,ean,sale_price,regular_price,currency,stock,product_url`. Vendor mappings vary, so a mapping layer is required; permission and fee unresolved.
4. **Permitted merchant HTML with JSON-LD**: synthetic `<script type="application/ld+json">` Product/Offer; parse `name,sku,mpn,gtin13,price,priceCurrency,availability,url`. Missing historical regular price means `on_sale=null` (do **not** fabricate markdown). JSON-LD may be SEO lagging and is not checkout truth. HTML scraping disabled unless site/merchant grants use and robots allows target path.

## Live gates in all outputs
All four parsers force `purchase_total=null`, `identity_accepted=false` and `authorized_for_live_reuse=false` even on well-shaped synthetic responses. Prices stay separate from taxes/shipping. Declaring a source permitted is independent of parsing. The source code contains **no requests.get(), page.goto(), URL fetch, anti-bot handling, account access or hidden API probing**.

## Eight executed unit tests
```
test_bestbuy_sale_and_null                  PASS
test_csv_missing_gtin_and_outstock         PASS
test_dedupe                                PASS
test_html_jsonld_separate_not_sale         PASS
test_invalid_jsonld_nonproduct             PASS
test_invalid_numeric                       PASS
test_no_price_or_false_authorization       PASS
test_woo_minor_unit_and_false_markdown     PASS

Ran 8 tests in 0.001s — OK
```

The tests check null/missing price and UPC, incorrect markdowns, prices in cents, false stock availability, duplicate same-SKU rows, invalid/negative/NaN price, and nulling unsupported authorization/identity. **Not tested:** real retailer markup changes, auth/429/robots, region/coupon/price/availability timestamps, order checkout, rate limits, legal licence, source data completeness, a real Mac launchd run, or eBay reference.

## Three representative acquisition designs, none activated
- `bestbuy_official_api` with a key in local Keychain/environment only after granted purpose: use documented API `onSale` or category pagination, limited page count and 5req/sec ceiling, store source URL/timestamp, strictly expire raw cached content under Best Buy 72h policy.
- `approved_bulk_feed` after advertiser-specific access: download updated CSV/FTP only on published cadence, verify content hash/header version and minimum fields, stream/parse locally; do not repeatedly hit merchant website or store confidential raw feed forever.
- `consented_woocommerce_store` for one named merchant: `on_sale=true` with page size <=100, stop at advertised `X-WP-TotalPages`; external GET allowed **only** after explicit merchant/site permission and robots check; stop on 403/429/challenge, do not switch user-agents or proxies.

**Why no live scraper demonstration?** No large US retailer in the target set was positively verified to grant our exact purchase-index scraping use without account/approval; five have explicit restrictive terms. A framework having publicly reachable data cannot confer the individual merchant's permission. A local fixture is a honest parser feasibility proof, not a legal entitlement or live operational scanner.

## Reproduction
From this conversation's included standalone Python attachment, execute in a clean Python 3.13+ environment:
```sh
python3 -m unittest -v arb020_f1_fixture_proof
```
Only Python standard library is required. `beautifulsoup4`/lxml, Scrapy and Playwright may later be used on approved content but are not dependencies of this proof. Independently corroborate the exact artifact and test output; this worker's self-report is not hostile review.
