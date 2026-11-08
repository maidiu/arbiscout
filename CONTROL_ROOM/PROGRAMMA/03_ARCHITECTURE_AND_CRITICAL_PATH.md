# ArbiScout: purchase-research architecture and exact dependency spine

```text
UNIFIED CATALOG (source and category filters, top-N selection)
  Best Buy / Meh / Woot / Kroger normalized products
                                                      +
RETAILER OFFER DISCOVERY (source-neutral)
  Browser-mode listing pages (Best Buy and others) / Meh / Woot / Kroger APIs
  Walmart / Target / other feeds / price aggregators / import offers
    -> current purchaser's all-in price, stock, geography, timestamp, quantity
    -> exact product identity / condition / brand / model / bundle
                                                      +
EBAY REGULAR COMPLETED-SALE PRICE HISTORY
    -> user-saved sold-search HTML only; no automated eBay /sch/ retrieval
    -> same-product actual sales in meaningful window
    -> robust ordinary-price baseline + sample size, recency and uncertainty
    -> displayed sold low/high/mean/median and middle-50% range
                                                      |
                                                      v
                 PRICE-GAP COMPARATOR (no anticipated transaction)
    absolute = provisional eBay historical sale baseline - retailer purchase price
    relative = absolute / ordinary historical eBay price (positive denominator)
    optional conservative lower historical price quantile
    current output is GROSS only: fees, shipping, tax and returns excluded
                                                      |
                                                      v
           QUALIFY actual bargain / refuse unsupported comparisons
                    rank 0–10 maximal reliable purchase gaps
                                                      |
                                                      v
                 DAILY SOURCE-LINKED PURCHASE RESEARCH INDEX
                           -> later price/stock verification
```

## Hard prerequisites versus alternative sources

- Retailer offer schema `ARB-031` and exact match `ARB-030` can be developed source-free.
- Regular historical eBay price observations `ARB-040` → robust reference `ARB-051` → gap calculator `ARB-050` → ranking `ARB-060` → daily report `ARB-071`.
- Retail price / real stock checks `ARB-033` qualify the live offer, while source rights and quality gates affect whether real observations are admissible.
- Unified catalog `ARB-106` merges scraped and API outputs, filters by source/category and writes the top-N selection. Saved list `ARB-107` persists a hand-picked subset and sends exactly that subset to the eBay run. Provider adapters `ARB-100` (Meh/Woot/Kroger) and browser-mode listing discovery `ARB-101` feed the same purchase-offer schema. User-saved eBay intake `ARB-102` and distribution flags `ARB-103` feed the provisional comparator. Credentials are local-only `ARB-104`; non-food category coverage is probed under `ARB-105`.
- Automated eBay sold-search retrieval is **not** part of the architecture. eBay's robots.txt disallows `/sch/` for automated agents; the watcher reads only files the user saves manually.
- **One** suitable retailer source is enough for first live proof `ARB-090` and first yield pilot `ARB-029`. Best Buy `ARB-023`, Walmart `ARB-024`, Google Shopping `ARB-022`, Target `ARB-025`, Home Depot `ARB-026` are exploratory **alternatives**, not mandatory ALL-OF tasks. Further sources may be added.
- Current eBay historical-price source suitability `ARB-010` is an **external live evidence acceptance dependency**, not a reason to stop writing source-neutral code.
- Product category exploration and import-source acquisition conditions can progress independently. No anticipated onward transaction is part of this architecture.

## Priority foundation

Immediate upstream tasks to address in parallel:
1. `ARB-010` access to comparable completed eBay sale-price history, including negative provider answers.
2. `ARB-020` broad retailer discount discovery, without fixing a retailer trio in advance; one candidate route can be tested.
3. `ARB-030` exact product/condition matching, reviewing neutral utilities from old draft.
4. `ARB-031` source-neutral retailer offered purchase-price schema.
5. `ARB-040` historical price observation schema plus `ARB-051` ordinary-price baseline.
6. `ARB-050` gap computation and `ARB-060` maximum *substantiated* gap ranking.
7. `ARB-071` legible report as first actual consumer.

The [generated dependency dashboard](DASHBOARD.md) and [full tasks table](TASKS_TABLE.md) list all tasks, live gates, optional sources, and downstream reach; the [95-question register](QUESTIONS_TABLE.md) tracks research unknowns.

## Actual first acceptance

One verified purchasable retailer item whose price is materially below a regular eBay actual completed-sale price baseline for the identical product, with precise source URLs, date/region/condition, quantified absolute/relative shortfall and sample support. Then reproducible daily 0–10 index. No future sale, seller economics, margin projection or purchase execution required.

Source-free fixture proof and live licensed source observation are different tests. Legacy PR #1's nonconforming calculations are not adopted.
