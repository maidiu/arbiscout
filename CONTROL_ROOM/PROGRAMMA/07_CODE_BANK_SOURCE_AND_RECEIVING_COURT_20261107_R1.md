# ArbiScout — code-bank source, custody and receiving court (2026-11-07)

**CANDIDATE ONLY.** This document is an additive currentness/engineering receipt for `PROGRAMMA ARBISCOUT`, subordinate to [the purchase-research constitution](../PRODUCT_CONSTITUTION.md). It is **not** an independent review, merger, third-party data grant, live eBay data proof or declaration of production readiness.

## Exact GitHub source cut

- Parent control room: `agent/arbiscout-programma-control-room-r1@92478568744bffcdd1061447f5d4027d4a0da735`, PR #2 **DRAFT / UNMERGED** at this inspection.
- User-directed banking branch: `agent/programma-arbiscout-codebank-ebay30d-20261107-r1`, initial bank commit `f98f11e220d038650f36be52cdfe49e49aa05111`.
- Current executable tree: [`ENGINEERING/arbiscout_app/`](../../ENGINEERING/arbiscout_app/) (relative paths resolve from repo root; use GitHub tree if rendered paths differ).
- Full no-drop local historical source tree: `ENGINEERING/SOURCE_BANK_20261107_R1/`: **22 files** (current 10 files + legacy/pilot material and source-bank README), with current code *also* mounted as separate active runnable tree (32 tree entries total).
- No original retailer HTML, login data, personal saved pages, developer keys, provider accounts or non-user-owned pages were banked.

## Scope of work genuinely performed

1. Deterministic bounded retail acquisition application: optional URL fetch, listing/department link priority, HTML/JSON-LD product extraction, source/product identity dedupe, missing-price product fallback, local HTML dashboard, retailer links and eBay sold-search links.
2. Actual saved Best Buy HTML **locally inspected** by earlier code: 152 cards / 131 unique products / 37 complete current+prior price pairs / 94 missing-price records. This is a historical snapshot, NOT a live price/feed assertion; the user's saved HTML was *not committed*.
3. Dated eBay 30-day evidence module: selects 20 supported retailer discounts, parses saved sold-search HTML fixture records, filters by sale date, requires sufficiently matching model tokens, excludes unproven accepted Best Offers, computes an exploratory median and price gap, and renders a secondary HTML report.
4. Local full application tests: `python3 -m unittest discover -s tests -v` from `ENGINEERING/arbiscout_app/` returned **16/16 PASS** on 2026-11-07. These include a synthetic full consumer pass and negative cases. A PASS is not market-data accuracy, independent acceptance or legal source-use approval.
5. The source-free legacy experiments remain retained for regression/forensic use, *not adopted concurrently as independent production implementations*.

## Precise evidence and operation ceilings

| Gate | Supported now | Not supported |
|---|---|---|
| S0 provenance | Exact Git blobs, immutable banking commit, declared operating scope | Production acceptance or protected main merge |
| S1 local engineering | 16 synthetic/offline tests; parsed user-provided historical Best Buy HTML | Live retailer crawl continuity or complete stock/checkout pricing |
| S2 external retailer | User reports personal Woot/Meh/Kroger access; independent scopes not accessed by this worker | Authorized live adapter, logged evidence of fresh price and purchasability |
| S2 external eBay | Saved HTML parser, opt-in robots-checked HTTP pathway subject to refusal, 30-day local date filter | Successful automated live eBay access, complete 30-day coverage, actual accepted-offer paid data |
| S3 independent receiving | A reviewable draft candidate | Independently confirmed code/rights/economic grades, protected CAS main integration |

**Important distinction:** eBay HTML `DISPLAYED_SOLD` is *not* an authoritative actual paid record; accepted Best Offer prices may differ. No UI listing sample is automatically promoted to the historical normal-sale truth needed by the constitution. The current `model_match` is a heuristic; real exact GTIN/MPN/condition/quantity evidence is still required.

## Existing task lineage (no separate fourth program)

The source code advances **candidate source-free evidence** relevant to `ARB-030/031/040/050/051/060/071/081`, but does not certify any of them as complete, especially `ARB-060` (existing validator forbids treating legacy profit-ranking as this task's fulfilment). `ARB-010` eBay historical provider research and `ARB-020/F1/F2` retailer-source research remain separate unmerged PR returns, not silently reincorporated. The dated status overlay in `CONTROL_ROOM/STATUS/CURRENT_PROGRESS.*` is current for this branch; the existing 2026-10-31 generated task table remains a frozen planning view until qualified task-registry receiving/regeneration.

## First real consumer and stop conditions

The productive gate is one **current, truly obtainable retailer purchase offer** + same-item **historical actual eBay sales**, with amount/date/condition/quantity provenance + a conservative observed difference + an attributable index entry. Lack of enough reliable matches means *NO RANK*, not padding. Do not pay a provider, create retailer accounts, initiate unauthorized crawling, or deploy a production scanner as a side effect of this source bank.

**Next: independent sourcefree review at exact PR head; narrow authorized real-data canary; permitted and benchmarked sold-data provider; then independently reviewed first consumer, rights and final merge by the user/authorized integrator.**
