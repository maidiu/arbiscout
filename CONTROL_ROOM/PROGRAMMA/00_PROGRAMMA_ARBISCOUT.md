# PROGRAMMA ARBISCOUT
## Whole purchase-research project: retailer purchase bargains indexed against regular eBay sale patterns

**Authority:** [Controlling Product Constitution](../PRODUCT_CONSTITUTION.md), user revision 2026-10-31. This is the proposed control-room branch of draft PR #2; it is not already merged into `main`.

### Sole terminal product

**Index current prices at which major retailers will sell goods and identify the largest reliable purchase-price gaps below regular historical eBay completed-sale patterns for the exact same product.** Discover sale and clearance stock broadly (not only a preselected retailer list); confirm identity/condition/quantity, current purchase price and availability; construct robust normal eBay sale-price baselines; evaluate the observed absolute and relative below-eBay gaps; and publish a daily **0–10** purchase-research list with original sources and uncertainties.

`absolute_gap = eBay_regular_historical_sale_price - current_retailer_total_purchase_price`

`relative_gap = absolute_gap / eBay_regular_historical_sale_price` where the historical reference is sufficiently evidenced and positive.

Historical eBay observations are comparison data, not forecasts or anticipated transactions. No later sale, seller fees, return-on-investment model, inventory operation, or specific user identity is necessary for this product. An optional Alibaba/AliExpress input is another *purchase-offer source* with quantity, freight and lead-time costs.

### R — Recognize, Recover, Reconcile

Track actual existing research, provider/API documentation, old draft PR #1, prior false assumptions, contradictions, source rights, alternative code and real consumers. Legacy draft financial scoring is **NOT** current application functionality; any neutral product-identity code must be independently evaluated before reuse. Preserve historical why-not decisions as history, not active product requirements.

### O — Organize, Adjudicate the whole

**Machine sources of truth:**
- [Work registry](01_WORK_REGISTRY.json): 39 capabilities, explicit ALL-OF technical prerequisites, optional ANY-OF alternative-source gates, nonblocking related work, P0–P3 priority, source and acceptance state.
- [Question registries](QUESTIONS/): 95 audited investigation/substantiation questions, divided into seven files, each carrying status, priority, question prerequisites, work-task dependencies for operational proof, findings and evidence refs.
- [Source registry](02_SOURCE_REGISTRY.json): provider documentary/evidential facts separated from API permissions, access, price coverage and cost.
- [Generated dashboard](DASHBOARD.md): status, high-leverage foundations, task and question tables; [CSV views](TASKS_TABLE.csv) / [questions CSV](QUESTIONS_TABLE.csv) when spreadsheet-style filtering is preferable.
- [Architecture and dependencies](03_ARCHITECTURE_AND_CRITICAL_PATH.md), [acceptance](04_ACCEPTANCE_MATRIX.md), [why-not](05_DECISION_AND_WHY_NOT_LOG.md), [current checkpoint](../STATUS/CURRENT_PROGRESS.json).

For any item answer: **question → prerequisite → evidence → interpretation → actual status → next action → terminal purchase-index consequence**. Distinguish source existence, lawful usage, synthetics-only code, runnable proof, real observation, independent acceptance, and merged/live consumer.

### I — Implement, Prove, Integrate, Learn

Select largest coherent useful index path: one real retailer offer source + eBay same-product historical observations → comparable regular price estimator → robust price-gap calculation → source-linked 0–10 report. An initial provider is sufficient; Best Buy, Walmart, Target, affiliate networks, Google Shopping aggregators and others are **examples to investigate, not universal mandatory prerequisites**. Run negative tests for wrong variants, stale location-based offers, missing completed sales, outliers, unsupported data, negative gaps and wrongly padded shortlists.

A source-free test supports only that local code claim. A permission ruling is distinct. A returned agent report is not an adopted current branch. No automatic external account access, paid subscription, worker dispatch or production merge.

### Priority logic

- `dependencies` means ALL must be met for the task's declared hard execution edge.
- `dependency_groups` `ANY_OF` means pick one qualified source; do NOT require every sample retailer.
- `related_tasks` means informative but **nonblocking**.
- `acceptance_dependencies` means live verification needs external permission/data even when source-free code can be developed.
- Question prerequisites are separate from associated work, and `proof_requires_tasks` means tasks needed for a conclusive operational test, not a ban on starting the research.
- Dependency reach is a **planning aid**, not an evidence of work completed or a replacement for the terminal-product critical path.

### One HQ question

What has actually advanced toward a **real evidence-backed retailer purchase-gap index**, what is merely researched/proposed/tested with fixtures, which provider and data quality edges remain externally unresolved, and which highest-leverage producer→consumer task should be executed next? Report DONE / REMAINING / BLOCKERS / TOP UPSTREAM PRIORITIES / NEXT PRODUCTIVE FLIGHT / DELTA.
