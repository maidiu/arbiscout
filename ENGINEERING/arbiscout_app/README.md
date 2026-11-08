# ArbiScout Deal Explorer — local Python app

A **working bounded crawler and self-contained HTML dashboard** for retailer sale listings. It runs on macOS with Python 3.9+ and BeautifulSoup. No LLM service, no JavaScript dependency for scraping, no eBay API, and no payments. Each run creates `arbiscout_output/index.html`: open it in any browser.

## Quick start on a Mac

Unzip the download, open Terminal in the extracted `arbiscout_full_app` folder, and run:

```bash
bash run.command
```

Enter a **full deals-page URL**, e.g. `https://www.example.com/sale`. It automatically creates its own Python virtual environment, installs `beautifulsoup4` (first run only), fetches the source URL when allowed, follows promising second/third-level deal-listing links, visits limited individual products with missing prices, and opens `arbiscout_output/index.html`.

Or use command line controls:

```bash
python3 -m pip install beautifulsoup4
python3 arbiscout.py 'https://www.example.com/sale' --depth 2 --max-listings 15 --max-products 10 --outdir arbiscout_output
open arbiscout_output/index.html
```

The initial URL is included; `--max-listings 15` means *up to 15 secondary/tertiary listing pages*, followed by *up to 10 individual product pages* where needed. Use `--depth 0 --max-products 0` to analyze only the landing page. Use `--save-html` to archive each fetched page in `arbiscout_output/raw_pages/` for analysis.

## Your saved Best Buy HTML

Because the website can limit automated retrieval, a **genuine offline mode** is included. This processes the real file you already saved without querying the website or needing lxml:

```bash
python3 arbiscout.py \
  --snapshot '/absolute/path/to/Best Buy Black Friday 2026 is Nov. 26–27.html' \
  --snapshot-url 'https://www.bestbuy.com/black-friday' \
  --offline --outdir arbiscout_output
open arbiscout_output/index.html
```

If you put that HTML file into the app folder, you can instead provide just its filename. Do **not** paste Markdown-format links (`[https://...](https://...)`) in Terminal; use a plain URL. You can also run `bash run_saved.command` and answer two questions.

**Verified offline result for the supplied Best Buy saved page:** 131 distinct products, 37 with current/previous retail prices, 94 without a complete price pair. The HTML dashboard was browser-tested for sorting, filtering and updating editable eBay queries. The user-uploaded HTML is **not bundled in the ZIP**.

## What the app does

- Fetches an input page using a bounded read-only HTTP client (or optional ordinary headless Chromium).
- Extracts product cards from current Best Buy `data-testid` markup, general retail product cards, and Schema.org `Product` JSON-LD when available.
- Reads sale/clearance category links **from the downloaded HTML**, ranks those links, and follows up to `--depth` 2 across one retailer domain.
- Merges repeated product URLs/IDs across pages, completing price records from other listings before fetching any individual product pages.
- Performs limited product-page fallbacks for products missing price pairs. `--enrich-models` optionally also visits priced product pages lacking explicit model identifiers.
- Calculates **retailer-advertised** savings: regular retailer price minus current retailer price, as both appeared in a single observation. Percentage = savings / regular price. No eBay math yet.
- Creates an offline `index.html`, plus `products.json`, `products.csv`, `crawl_log.json`, `next_pages.json`.
- The dashboard supports sortable discount %, dollar savings, current price, name; text search; hide incomplete rows; original retailer links; editable eBay sold-listings query links.

## eBay sold links: important limitation

The eBay URLs **do** apply Sold Items and Completed Items (`LH_Sold=1&LH_Complete=1`), sorted by ended recently (`_sop=13`). They do **not** restrict to the last 30 days: eBay's standard sold listing search typically reaches back ~90 days, and a reliable URL-only 30-day filter has not been demonstrated. Within eBay you can review the most recent 30 days, or later use an independently licensed dated sold-data API (CompsAPI/SoldComps) to perform true 30-day calculations. An eBay result may include nearby variants; the query field is editable and should be verified. Best Offer display prices may be misleading.

## Crawling and source restrictions

- Website terms and permissions still matter. The crawler identifies itself, fetches `robots.txt`, and refuses paths disallowed by it. It stops at HTTP blocks instead of solving CAPTCHA, disguising itself, rotating proxies or bypassing protections.
- **Best Buy's September 2026 website terms explicitly restrict unapproved agents and automated navigation.** Offline parsing of your own saved page is technically demonstrated; ongoing automated collection of Best Buy pages is **not** demonstrated or authorized by this package. A live run may be refused or blocked. Seek permitted access if needed.
- The current extraction rules fit the supplied Best Buy snapshot and certain common retail HTML/JSON-LD patterns. Other stores may need a custom adapter. A live blocked page, empty listing, or missing prices is reported in `crawl_log.json` rather than fabricated.
- Each vendor's local stock, membership prices, regional fees, delivery fees and checkout totals require independent verification before purchase.

## Browser-rendered pages (optional)

If an authorized retailer loads products only with client-side JavaScript, install Playwright inside the same Python environment:

```bash
.venv/bin/python -m pip install playwright
.venv/bin/python -m playwright install chromium
.venv/bin/python arbiscout.py 'https://www.example.com/sale' --mode browser --outdir arbiscout_output
```

Browser mode still respects `robots.txt` and does not attempt to bypass blocked pages. On older Macs, the Playwright Chromium build may be incompatible; use HTTP mode or an authorized alternative.

## Tests

```bash
python3 -m unittest discover -s tests -v
python3 arbiscout.py --snapshot sample/sample_deals.html --snapshot-url https://shop.example.com/sale --offline --outdir test_output
open test_output/index.html
```

The sample contains **fictional** prices. One test additionally validates the real uploaded Best Buy file when available adjacent to the package, but that file is deliberately not distributed.

## Next integration

The scanner does **not** yet automatically fetch historical eBay transactions or calculate retailer-vs-eBay price gaps. That requires an accepted reliable historical-sales provider and exact-item matching. All report savings are **within-retailer** advertised discounts only.

## November 7, 2026 addendum: 30-day eBay sold-evidence comparison

The `ebay_comparison.py` module and `run_compare.py` wrapper add a separate **purchase-price gap** view. It ranks the top 20 observed retailer discounts, parses dated eBay sold observations from supported saved HTML fixtures, excludes out-of-window and unresolved accepted-Best-Offer records, applies conservative model-token matching, calculates a 30-day median only after at least three usable observations, and generates `arbiscout_output/comparisons/index.html` with retailer and eBay links. Dates are filtered by this program; the eBay URL has no assumed 30-day filter.

```bash
python3 -m pip install -r requirements.txt
python3 run_compare.py 'https://www.bestbuy.com/black-friday' \
  --snapshot '/path/to/Best Buy Black Friday 2026 is Nov. 26–27.html' --offline
open arbiscout_output/comparisons/index.html
```

By default this produces an **honest unranked eBay comparison**, since it has no sale records. To parse legitimate saved eBay search HTML, put `01.html` through `20.html` in a directory corresponding to the top retailer candidates in rank order, then add `--ebay-fixtures /path/to/sold_html`. The `--ebay-live` flag opts into a robots-checked direct eBay HTTP request per candidate. It may refuse or fail because eBay requires login and/or restricts automation. There is no password, cookie, CAPTCHA solver, proxy rotation or bypass logic. For reliable automated operation, a permitted paid provider remains the strongest candidate; a provider adapter and empirical accepted-Best-Offer audit are not implemented in this version.

**Evidence limits:** The source-free tests prove date filtering and calculations for generated fixtures, not live actual paid-price fidelity or live retailer/eBay acquisition. Product-name token matching can yield false positives (variant conflicts), so an apparent gap is provisional and requires human verification unless UPC/MPN/variant and condition are independently established. Source rights remain separately gated.

```bash
python3 -m unittest discover -s tests -v
```


## Unified catalog and source filtering (Nov 7)

`build_catalog.py` merges `bestbuy_live`, `meh_live`, `woot_live`, and `kroger_live` into one `catalog/catalog.json` plus a filterable dashboard. `run_catalog.command` builds the catalog and serves the live selection UI at `127.0.0.1:8770`.

- Filter by **source** (Best Buy / Meh / Woot / Kroger; include or exclude any combination), by **category**, and by text.
- Sort by **highest % off**, **dollar savings**, **lowest/highest current price**, **name**, **source**, or **category**.
- Set **Top N** (default 20) and click **Build top N selection**. The selection is written to `catalog/selected/`.
- Capture eBay evidence for that selection with:
  ```bash
  ./watch_ebay.command ebay_saved --output catalog/selected --keep-selection
  ```
- A downloaded `selected.json` from the static dashboard can be processed with `./run_selected.command selected.json`.

Categories come from provider data where available (Woot categories, Kroger categories) and are inferred from the Best Buy source page/title otherwise. The catalog caps each source at 2,000 products by default (`--max-per-source`) so a large Woot feed remains manageable; the Woot adapter itself caps at 500. The selection is gross retailer discount only; eBay comparison and the below-eBay flags happen after the capture step.

## Complete executable 20-to-10 test operator (Nov 7)

See [TEST_VERSION.md](TEST_VERSION.md). Use `python3 run_test.py --demo --as-of 2026-11-07 --output demo_out --open` for an offline **fictional** 20-item demonstration that exercises the same actual extraction, 30-day date filtering, median, and top-ten ranking code. Or pass your saved Best Buy HTML with saved eBay sold pages or an explicitly authorized robots-checked live eBay request. Output is provisional displayed-price comparison, not proven actual paid historical prices. The earlier Nov 7 source bank is a permanent historical archive, not the current active version.
