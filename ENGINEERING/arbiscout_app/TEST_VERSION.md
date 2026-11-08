# ArbiScout — executable 20-to-10 test version

The existing dated eBay comparison module calculates the cutoff in Python. No eBay URL parameter for the last 30 days is necessary.

This new test operator does the complete chain:

1. Extract retailer products from your locally saved Best Buy page, or permitted live retailer pages.
2. Select up to 20 offers with complete observed current/regular retailer prices, ordered by retailer-advertised percentage discount.
3. Read a matching eBay sold-results HTML file for each candidate, or explicitly try the existing robots-checked direct eBay HTTP client where automation is allowed.
4. Parse sale dates and locally reject observations outside the preceding 30 days, missing dates, obvious mismatches, and unknown accepted Best Offer amounts.
5. Calculate displayed-sold low, high, mean, median, and the typical middle-50% range, plus an indicative retailer-to-eBay difference for sufficiently supported products.
6. Rank up to ten positive indicative price differences, linking sources, and flag whether the Best Buy price is below the eBay sold low or median. Display no results rather than fabricate missing history.

## Fully executable, source-free test: 20 -> 20 -> 10

From ENGINEERING/arbiscout_app:

    python3 -m pip install -r requirements.txt
    python3 run_test.py --demo --as-of 2026-11-07 --output demo_out --open

This creates 20 FICTIONAL retail products and 20 sets of FICTIONAL eBay sold-result pages. Each sold-results fixture includes three recent dated prices, an old excluded result, and a Best Offer whose paid amount is unknown. It runs the same extraction, filtering, comparison and HTML report code as the other modes. The output marks every number fictional.

## Saved Best Buy page, without network

    python3 run_test.py \
      --snapshot '/path/to/Best Buy Black Friday 2026 is Nov. 26–27.html' \
      --url 'https://www.bestbuy.com/black-friday' \
      --output bestbuy_test --open

The saved page is not in this public repository. The previous HQ measured 131 distinct products and 37 complete retailer price pairs from the uploaded snapshot. With no eBay sold HTML supplied, the output truthfully shows zero indicative comparisons.

## Supply the corresponding eBay sold-results pages

Place 01.html through 20.html in a local directory. The comparisons dashboard labels each product with the filename to use. These are the entire sold-results pages, not individual item pages. Then:

    python3 run_test.py \
      --snapshot '/path/to/your-saved-bestbuy.html' \
      --url 'https://www.bestbuy.com/black-friday' \
      --ebay-pages '/path/to/ebay-sold-pages' \
      --output bestbuy_test --open

To reuse an existing retailer scrape instead of crawling again (keeps the same candidate/fixture order):

    python3 run_test.py \
      --ebay-pages '/path/to/ebay-sold-pages' \
      --reuse-retailer --output bestbuy_test --open

The program computes the dates itself. Records with missing dates or price-type ambiguity are not counted. It never fills a 30-day median from older records. The report shows sold low, high, mean, median, the typical middle-50% range, and whether Best Buy is below the eBay sold low or median. Live automated eBay sold-search collection remains disabled because eBay's robots.txt disallows `/sch/` for automated agents.

## Live capture console (click, save, result)

After one Best Buy scrape:

    ./watch_ebay.command

This opens a local console. Click **Open next waiting eBay page**, save the completed-listing page into `ebay_saved/` with the filename shown in its row, and the row updates automatically with sold low/high/mean/median, the typical middle-50% range, and the Best Buy-vs-eBay flag. Each saved file is parsed and the top-10 and comparison reports are regenerated. The console only reads files you save; it never fetches eBay itself. On exit it can delete the saved HTML files.

## Explicit opt-in network test

Where automated collection is actually authorized, the existing HTTP mode can attempt to retrieve dated eBay result pages:

    python3 run_test.py \
      --snapshot '/path/to/your-saved-bestbuy.html' \
      --ebay-live --output bestbuy_test --open

This reads robots.txt and stops on refusal, login challenges and access errors. It does not evade blocks, automate login, use undocumented APIs or claim that robots permission alone settles contractual rights. Some or all twenty requests may fail.

## Outputs

The output directory contains:
- index.html: top ten positive INDICATIVE differences only, clearly labeled provisional
- top10.json / top10.csv: source-linked machine-readable ranking
- comparisons/index.html: all selected offers and excluded/failed eBay comparisons
- comparisons/comparisons.json / sold_observations.json: complete parsed evidence and calculations
- retailer/index.html / products.json: raw retailer candidate dashboard and product extraction
- run_receipt.json: time window, source mode, number of selected offers and source failure counts

Source limitation is binding: eBay's ordinary Sold Items results may display an accepted Best Offer's original asking price rather than its actual paid price. Even unflagged displayed sold prices and approximate model matches need independent verification. The report therefore says ZERO actual-paid verified comparisons; its displayed gaps are diagnostic only. True checkout price, SKU, condition and source permissions remain open.

The immutable historical Nov 7 source bank remains under ENGINEERING/SOURCE_BANK_20261107_R1. The new test runner is an additive, active development component, not a replacement for or silent mutation of those archived bytes. No merge into main, payments, live marketplace claim or independent reviewer approval is implied.

## Unified multi-source catalog

After running `./run_live.command` and any of `./run_api.command meh|woot|kroger`:

    ./run_catalog.command

This merges the available source folders into `catalog/catalog.json` and opens a local catalog at `127.0.0.1:8770`. Filter by source and category, sort by % off / savings / price / name, set Top N, and click **Build top N selection**. The selection is written to `catalog/selected/`; capture eBay pages with:

    ./watch_ebay.command ebay_saved --output catalog/selected --keep-selection

The static dashboard's **Build** button downloads `selected.json`; process it with `./run_selected.command selected.json`. Categories are provider-provided where possible and inferred from Best Buy source pages/titles otherwise. Woot results are capped per source (default 2,000 in the catalog, 500 in the adapter) so source filtering stays responsive. Selection is gross retailer discount only; eBay sold comparison follows the capture step.

## Application tests

    python3 -m unittest discover -s tests -v

The PR's GitHub Actions workflow now installs the app's BeautifulSoup requirement and runs application tests alongside the PROGRAMMA registry and archival integrity tests.
