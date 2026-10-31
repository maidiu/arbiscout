# CURRENT — ArbiScout HQ checkpoint

**2026-10-31 · proposed control-room draft PR #2. Verify current GitHub refs before reusing this snapshot.**

## Exact sole function

Broadly index genuine retailer bargains with offered purchase prices **maximally below regular historical eBay completed-sale prices of the identical goods**, with statistically defensible reference price, gap magnitude, purchase conditions, stock/region and observation dates. Publish 0–10 evidence-backed candidates. No future sale transaction or seller financial modeling.

## Programma operational records

- **40 task nodes:** [generated task table](../PROGRAMMA/TASKS_TABLE.md) · [canonical work JSON](../PROGRAMMA/01_WORK_REGISTRY.json).
- **112 question/substantiation nodes:** [generated question table](../PROGRAMMA/QUESTIONS_TABLE.md) · [seven canonical JSON files](../PROGRAMMA/QUESTIONS/).
- **16 source evidence records:** [source registry](../PROGRAMMA/02_SOURCE_REGISTRY.json).
- [Compact dependency-priority dashboard](../PROGRAMMA/DASHBOARD.md), [task CSV](../PROGRAMMA/TASKS_TABLE.csv), [question CSV](../PROGRAMMA/QUESTIONS_TABLE.csv).
- All generated views are derived from the JSON records, not manually authoritative tables.

## DONE

Governing purpose clarified; entire research-question inventory captured with dependencies, priority, status and proof-task links; task graph distinguishes ALL-OF hard prerequisites, ANY-OF retailer sources, related work and live evidence gates; Markdown/CSV dashboards and structural validation implemented on proposal branch.

## NOT DONE

No current real eBay history feed, no independently verified live retailer offer+historical-eBay pair, no working price-gap calculator/ranker, no daily real purchase-research index. Earlier [PR #1](https://github.com/maidiu/arbiscout/pull/1) is a separate historical source-free draft: **its former scoring is nonconforming and not adopted**. Only neutral exact identity utilities merit review.

## BLOCKERS / ROOTS

`ARB-010` historic eBay actual completed-sale price access and samples; `ARB-020` retailer bargain-feed landscape, with **any one suitable retailer sufficient** for a pilot; `ARB-030` exact identity; `ARB-031` total retailer purchase offer schema; `ARB-040/051` actual-sales historical reference and robust normal-price estimator; `ARB-050/060` observed price-gap computation/rank; `ARB-071` source-linked report.

## LARGEST PRODUCTIVE MOVE

Parallel evidence reconnaissance for historical eBay prices and one retailer offer feed, plus source-free exact-item/robust-reference/gap-calculator and report development. Never block independent research on a parent task merely because an umbrella workstream is incomplete.

## FLIGHTS (all prepared, **none dispatched**)

FLIGHT-001 eBay historical-price research; FLIGHT-002 first retailer source and broad discovery; FLIGHT-003 producer→gap→report implementation.

## DELTA

112-question research/substantiation graph covers 40 development tasks, including ARB-035's cultural-market hypotheses. No live authorization, real price comparison or merge has been claimed. Generated PROGRAMMA checks run in GitHub Actions and must be rechecked at exact current SHA.
