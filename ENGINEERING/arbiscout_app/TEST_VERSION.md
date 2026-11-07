# ArbiScout — executable 20-to-10 test version

The existing dated eBay comparison module calculates the cutoff in Python. No eBay URL parameter for the last 30 days is necessary.

This new test operator does the complete chain:

1. Extract retailer products from your locally saved Best Buy page, or permitted live retailer pages.
2. Select up to 20 offers with complete observed current/regular retailer prices, ordered by retailer-advertised percentage discount.
3. Read a matching eBay sold-results HTML file for each candidate, or explicitly try the existing robots-checked direct eBay HTTP client where automation is allowed.
4. Parse sale dates and locally reject observations outside the preceding 30 days, missing dates, obvious mismatches, and unknown accepted Best Offer amounts.
5. Calculate a displayed-sold median and indicative retailer-to-eBay difference for sufficiently supported products.
6. Rank up to ten positive indicative price differences, linking sources. Display no results rather than fabricate missing history.

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

Place 01.html through 20.html in a local directory, matching the exact order of the 20 selected retailer offers in the comparison dashboard. These are the entire sold-results pages, not individual item pages. Then:

    python3 run_test.py \
      --snapshot '/path/to/your-saved-bestbuy.html' \
      --url 'https://www.bestbuy.com/black-friday' \
      --ebay-pages '/path/to/ebay-sold-pages' \
      --output bestbuy_test --open

The program computes the dates itself. Records with missing dates or price-type ambiguity are not counted. It never fills a 30-day median from older records.

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

## Application tests

    python3 -m unittest discover -s tests -v

The PR's GitHub Actions workflow now installs the app's BeautifulSoup requirement and runs application tests alongside the PROGRAMMA registry and archival integrity tests.
