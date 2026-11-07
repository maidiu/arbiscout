# ArbiScout HQ — 20-to-10 executable test receipt, 2026-11-07

**Status: SOURCEFREE_DEMONSTRATED / DRAFT PR #16 / LIVE EVIDENCE HOLD / NOT INDEPENDENTLY RECEIVED.** This is an additive engineering receipt, subordinate to PRODUCT_CONSTITUTION.md and PROGRAMMA ARBISCOUT. The exact full terminal product remains the current retailer purchase-price index below regular historical **actual completed eBay paid sale** patterns.

## Code and product consumer

- ENGINEERING/arbiscout_app/run_test.py is the complete CLI for up to twenty retailer discount candidates, 30-day sold-record parsing/comparison and a provisional top-ten display. It reuses the existing retailer crawler (arbiscout.py) and historical comparator (ebay_comparison.py), rather than replacing either.
- ENGINEERING/arbiscout_app/TEST_VERSION.md gives full replay and source modes. Four additional tests are in tests/test_run_test.py.
- Output: index.html, top10.json, top10.csv, retailer/index.html, comparisons/index.html, retailer/products.json, comparisons/sold_observations.json, run_receipt.json.
- Existing immutable historical code bank (ENGINEERING/SOURCE_BANK_20261107_R1, bank commit f98f11e220d038650f36be52cdfe49e49aa05111) is retained byte-for-byte. The active app is allowed to evolve and remains on a draft branch.

## Execution evidence

At prior verified run [GitHub Actions #42412720168](https://github.com/maidiu/arbiscout/actions/runs/42412720168), head 7c486130958a69d213f3098106f790ce93435b7d:

- All workflows succeeded, including PROGRAMMA graph/views verification, active-application test suite, full synthetic demo generation, demo artifact upload, and root archive/control unit tests.
- Active application suite: **20 tests executed, 19 passed and 1 skipped**. The skipped test requires the historical user-supplied Best Buy HTML file intentionally excluded from GitHub. This is not evidence that a test failed.
- Structural/archive tests: 4 executed / 4 passed.
- Actual synthetic end-to-end demonstration: **20 fictional retailer offers selected, 20 provisional positive displayed-price comparisons, 10 ranked in the dashboard, ZERO verified actual-paid comparisons**. Historical dates are filtered inside Python; 45-day-old sales and unknown accepted Best Offers are excluded.
- Uploaded demonstration: artifact **arbiscout-demo-20-to-10**, artifact ID 13590102124, accessible from that workflow run.

All numbers above are from SYNTHETIC data and internal software behavior. The old real user-saved Best Buy snapshot was previously parsed (131 unique, 37 complete price pairs) but was not in the GitHub Action and is not falsely asserted as retested here.

## Remaining empirical/rights gate

A displayed eBay Sold Items amount may not equal an accepted Best Offer's actual paid amount. The current parser only supports provisional displayed-sold comparisons and model-token matching. It is not a trusted actual-paid source. No permissions for automated retailer collection, eBay site scraping, seller account use, source retention or license grants are inferred; the opt-in eBay client obeys robots.txt but that is not a full contractual authorization.

The user-requested **test version is runnable**, but the real purchase-research index remains blocked until a permitted live retailer offer and corresponding reliably actual-paid, precisely matched historical eBay transactions can be demonstrated, with total purchase costs and availability.

## Next consumer

Qualified review of exact PR head, then one user-authorized bounded source-pair canary with real paid-price provenance. Separate ENGINEERING / ECONOMIC_EVIDENCE / AUTHORIZATION_PRIVACY decisions; do not merge or self-certify from green fixture tests alone.

No separate worker was launched, no subscription or API charge incurred, and no main merge performed by this receipt.
