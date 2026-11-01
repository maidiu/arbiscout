# ARBISCOUT HQ INTAKE R1 — ALL RESEARCH RETURNS, CROSS-COURT RECONCILIATION

**Date:** 2026-10-31 (Eastern); intake from authenticated GitHub primary project files and exact PR/branch heads. **Status: HQ INTAKE PROPOSAL / NOT SCIENTIFIC OR SOURCE PERMISSION ADOPTION.** No worker branch or canonical PROGRAMMA was merged or modified. This branch starts from control-room proposal SHA `92478568744bffcdd1061447f5d4027d4a0da735`; original `main` at `2c2f3d64ce49edc3073c7feb094bf803ee84d371`. Reverify live refs before use.

## Controlling product

ArbiScout is **only a retailer purchase-research index**: current actually obtainable retailer purchaser price, exact identical product/condition/quantity, reliable *historical actual completed* eBay price pattern, and maximally substantiated absolute/relative price gap. A future transaction, seller fees, predicted revenue, ROI, or a particular intended purchaser is not part of this software. The sociological research is about possible upstream signal density; a cause of the price gap is NOT required to display an accurately observed gap.

## Returned artifacts and exact evidence identities

| Work | PR and immutable head observed | Substantive files | Intake truth |
|---|---|---|---|
| ARB-010 I3 historical-price sources | [#4](https://github.com/maidiu/arbiscout/pull/4) `d27d18e4cae518ebca07e1b2f722ff4b8204047c` | 8 under `CONTROL_ROOM/WORKERS/RETURNS/ARB-010-EBAY-SOLD-HISTORY-R1/` | `RETURNED_UNADJUDICATED`: 29 route candidates and proposed adapter; no paid-price API benchmark, account grant or live seller history |
| ARB-020 I3 merchant/discovery sources | [#6](https://github.com/maidiu/arbiscout/pull/6) `ee2a82a71dbf20ab3f46255fab5a1989796c70bb` | 10 under `CONTROL_ROOM/WORKERS/RETURNS/ARB-020-RETAILER-SOURCE-UNIVERSE-R1/` | `RETURNED_UNADJUDICATED`: 45 retailer candidates, 32 acquisition source types, 22 category-source hypotheses, not a live retailer feed or pilot |
| ARB-035 I3 socio-market research | [#8](https://github.com/maidiu/arbiscout/pull/8) `af342308e26b886a838dbd474cb1442a0ad943ae` | 10 under `CONTROL_ROOM/WORKERS/RETURNS/ARB-035-CROSSMARKET-CULTURE-R1/` | `RETURNED_UNADJUDICATED`: 26 sector hypotheses, 38 generic not actual SKU candidate strata, 26 unmeasured crossmarket cells; no demonstrated sector winner |
| ARB-035 hostile review commission only | [#9](https://github.com/maidiu/arbiscout/pull/9) `e9c61f5c3f4cbf576abd43ae37eabe000255d1bb` | Commission `CONTROL_ROOM/WORKERS/COMMISSIONS/ARB-035-INDEPENDENT-HOSTILE-I3-REVIEW-R1.md` | PREPARED PROMPT, not separate scientific outcome |
| ARB-035 independent hostile review | [#10](https://github.com/maidiu/arbiscout/pull/10) `ca2194f79e0f535f059c35b74e34a890730a397b` | 7 under `CONTROL_ROOM/WORKERS/REVIEWS/ARB-035-HOSTILE-I3-R1/` | `REVIEW_RETURNED_UNADJUDICATED`: conditional documentary framework, **HOLD empirical/causal/sector adoption**, explicit P0 and P1 repairs |

All worker/review PRs are draft and base on the proposed control-room branch, not canonical `main`; each head frozen above may advance. The branch histories differ: ARB-010 forked from older control SHA `64ae2a67...`, ARB-020 from `79f15d00...`, ARB-035/review from `92478568...`. For documentary source-only fan-in, selectively reconcile exact return directories against the current receiving head, not a blanket merge of each older parent tree. Do not perform an across-worker fast-forward or treat a green workflow as scientific acceptance.

## Court A — ARB-010: actual paid eBay historical prices

**Well-documented producer typology:** eBay Seller Hub Product Research (formerly Terapeak), up to 3 years, actual accepted Best Offer historical amounts, is the best official **human-readable manual reference**; Team Access supports delegated human research. No general Product Research programmatic sold-history API or bulk export was substantiated. eBay Marketplace Insights is historically relevant for up-to-90-day sale records but restricted/new-developer access presently blocked in cited official matrix; Browse/Feed/Trading/Sell do not supply *market-wide competitors' actual historical transaction prices*, and Finding/Shopping are retired. The returned 29-route matrix is a documentary map, not independently validated rights.

**Trial candidates, not sources approved:** CompsAPI first for economical documented `/v1/sold`/licensed-derivative claims; CompSniper independently for its 90d/3y APIs; SoldComps optional accepted-offer enrichment; Trawl archived multi-year, Soldgraph a price-type negative control, eBay Sold Listings API an upstream authorization risk. PriceCharting's documented Prices API lacks historic sale-records and cannot replace eBay atomic data.

**Critical contradictions:**
- A completed/sold listing label does not show actual paid price if the seller accepted a different Best Offer; Soldgraph itself warns displayed sold value can be an asking-price upper bound. CompSniper's terms characterize some Best Offer values as upper bounds while later marketing suggests actual consideration. This is a P0 data truth gate, not a stylistic issue.
- CompsAPI vendor terms may permit derivatives but do not prove eBay-origin permissions. Source provider's own licence and true original data provenance are distinct.
- Seller Hub Reports CSV is not proof of Product Research export.
- Prior seed eBay agreement URL ending id=5414 resolves to **Indian** legal terms, not US; use current US agreement id=4259 and verify version.
- Three-year archives may have different sampling/field granularity than 90d rows. A historical mean based on listing aggregates or truncated pages cannot be treated as independent `ATOMIC_SALE` events.

**Real proof missing:** official human oracle baseline, a 30-item accepted-offer/identity/condition adverse sample, provider API credentials and rights, actual row-level paid provenance and completeness, per-true-comp cost. Benchmark **0/30**. Proposed `05_SOURCE_ADAPTER_CONTRACT.json` includes 10 invariants and typed `actual_paid` versus `ask`; needs engineering and independent rights review before adoption.

**Intake disposition:** **accept that a detailed 29-route documentary research return exists; HOLD all actual provider selection/accuracy/permission and ARB-010 as a solved producer.** Review ARB-010 independently before promoting Q013–Q030 or source/status records.

## Court B — ARB-020: retail offer discovery and correct acquisition price

**Key distinction:** *unknown-deal enumeration* ≠ *known-product search*. A cheap Google Shopping query cannot prove broad clearance coverage, just as an affiliate feed description cannot prove granted use or stock.

**Documented source-shaped candidates:** ShopSavvy `GET /v1/deals` is a discoverable, paginated curated discount feed; it is not a census of retailer stock. Best Buy Products/Categories/Buying Options gives a documented catalog/regular/sale/condition API shape with a 50k calls/day, 5/sec claim; actual key/purpose clearance is unresolved. Home Depot says eligible Impact partners get daily merchant feed; Awin/CJ/Impact product catalogs can enumerate items subject to advertiser/program grant. Keepa `/deal` can expose recent Amazon price changes; DealNews has editorial RSS. DataForSEO/SerpApi generally search known queries and are enrichment, not proven universe-wide clearance enumerators. Walmart affiliates, Target, Amazon Creators and partner networks have independent onboarding and use-specific permissions.

**Price/capacity caution, all values worker-published and UNBILLED:** ShopSavvy claims 1 credit/10 returned deals, $49/1k monthly, $199/10k, $499/50k; its all-retailer offers can cost 3 credits PER PRODUCT. Under lower-bound simplistic 30-day scenario, 10k deal rows/day = 30k feed credits ($499 plan fits published credits), but fetching all retailer offers for 100 identified items/day = 9k additional credits; never mistake deals-feed cost for fully verified eBay-qualified opportunities. DataForSEO known-query published `$0.001` Standard is an optimistic unit-cost illustration, not a complete retailer offer detection cost. No source invoice/call was obtained.

**Unresolved:** vendor rights/retention/upstream data, quote eligibility, actual promotion recall, SKU/GTIN quality, price/stock/ZIP, checkout; no 100-offer pilot, no real normalized producer; empirical price-gap yield unmeasured. Source neutral `07_NORMALIZED_RETAIL_OFFER_CONTRACT.json` exists as proposed JSON Schema with 12 invariants, not a running or independently reviewed adapter.

**Candidate-first producer architecture:** at least one permitted high-recall deal/merchant feed → deduplicate/normalize → original retailer check for actual price/stock/region/condition → exact SKU join → eBay true-paid history → robust reference → price-gap report. Run **one-source-first** before integrating all 45 retailers. A ShopSavvy ↔ first-party retailer overlap is a promising *experiment*, not a production winner.

**Intake disposition:** retain 45-retailer and 32-source candidate maps, 22 unmeasured category hypotheses, economic sensitivity arithmetic and one-source experiment design; **HOLD vendor selection/use claims and all source performance** pending independent hostile review and real source tests.

## Court C — ARB-035: sector/culture mismatch

**What research produced:** 26 sector profiles; 38 generic candidate item classes with null actual GTIN/MPN; 26 crossmarket sector×retailer source hypotheses with every real eBay price, retailer price, and attention-overlap field null. A clear 10-rival scientific framework describes possible SKU-specific market channel disjunction, urgency, geography, fitment, obfuscation, model obsolescence, highly informed enthusiasts, incorrect historic price reports, service/trust and fast price convergence. No category ranks or actual joint opportunities established. eBay FY2025 Focus Categories and 2026 recommerce survey describe broad markets and self-reported channel interests, **not** exact SKU demand, retailer markdown or individual shopping-channel overlap.

**Independent hostile review #10 (frozen original PR #8):** documentary frame CONDITIONALLY USEFUL, empirical/sector result HOLD. Three P0 defects:
1. The prospective 100 slots comprise 40 curated deals + 20 random catalog + 20 eBay reverse-selected + 20 deliberately deep-discount controls. This mixture is NOT a probability sample of an enumerated retailer-offer population and cannot support a pooled qualified-offers-per-1,000 or a sector-wide rate. Independent representative source frames and non-denominator diagnostic arms are necessary.
2. **38/38** claimed candidate SKU strata are merely generic product classes; no actual GTIN/MPN/item evidence. Count of strata does not satisfy exact item sample requirement. Either gather actual identities or properly relabel as class-only design.
3. **26/26** matrix `retail_evidence_status` values `SOURCE_CLAIMED_OR_THEORY_ONLY` violate the declared `source_statuses_allowed` vocabulary. Machine-level status contract rejects its own records.

Additional repairs: eBay US agreement jurisdiction, 2004 NBER working paper vs 2009 journal citation and E11/E14 mislabel, mutable LEGO/Adorama current-promo screenshots not proof of exact original historical timestamp, unverified forum/comment timestamps, **n90>=12 and >=6 active weeks** only a proposed heuristic not statistically validated p25 lower-confidence bound, uncorrected dependence/outlier or nonrandom missingness, source-frame and multiple-testing uncertainty.

**Most important logical criticism:** a current cheap retailer offer `R(t)` below a **trailing 90-day historical** eBay median `B90(t)` can exist even if every eBay buyer knows about the retailer sale, because the historical median lags mechanically. A descriptive purchase-price gap does not prove cultural ignorance, enduring contemporaneous price separation or any behavioral cause. Buyer attention requires independent direct, ethically collected evidence; public community posts refute *categorical unawareness* but cannot quantify share of eBay buyers who follow deals.

**Intake disposition:** 10 hypotheses, negative controls, conservative evidence rules and qualitative research questions may be retained as *unmeasured study design*. Do not adopt a sector winner, causal channel hypothesis as established, mixed-frame per-1000 denominator, incomplete SKU panel or invalid machine schema. Q096–Q112 stay empirically OPEN. The independent hostile review is itself a review return; no automatic user/HQ adoption or source-owner repair.

## Whole-program synthesis

Three independent producer/science workstreams now align on this exact chain:

```
retailer deal / catalog enumeration (ARB-020/029)
    → authorized feed + deduplicated candidate records
    → original merchant purchase offer / checkout and region (ARB-031/033)
    → exact identity + condition + bundle matching (ARB-030)
    → actual paid eBay past transactions + window/coverage (ARB-010/040)
    → robust regular historical sale baseline (ARB-051)
    → actual observed absolute / percentage / conservative gap (ARB-050)
    → qualified rank up to 10 or valid zero (ARB-060)
    → source-linked daily purchase-research index (ARB-071/090/091)
```

ARB-035 is **optional upstream prioritization and scientific explanation**, not a live P0 requirement to show a legitimate price gap. Proving channel attention divergence would require a separate direct sample/ethical study; no inference in the software depends on buyer ignorance.

**Two distinct statistical sampling frames:**
- Qualified bargain *rate for a provider's DEALS FEED*: predeclare deals-returned list, unique offer dedup and timeframe; measure within THAT CURATED FEED. Not national retailer offer rate.
- Qualified bargain *rate for all catalog retailer offers*: need a prospectively enumerated catalog population and randomized selection with coverage/inclusion probabilities; intentionally selected high-discount SKUs and eBay-chosen reverse control cannot be pooled. Make failures, unknowns, no eBay rows and stockouts visible denominators.

**Common data contract join:** `retailer_offer` (merchant, GTIN/MPN, bundle/condition, available total purchaser price/stock/region/source/rights/observed_at) joined to `historical_ebay_paid_sale` (exact same model/variant/condition/quantity, actual paid vs ask provenance, sold_at, shipping/currency/date, provider completeness/rights, source lineage). Reject unknown or false comparators. One robust `ARB-051` estimator from real transaction rows is a later task. Proposed ARB-010 and ARB-020 JSON contracts have not been implemented or cross-schema integration tested.

## What the research has NOT done

Zero retailer checkout-verifiable offers acquired with authorized production source; zero actual accepted-offer paid eBay transactions from a qualified new API; zero 30-item vendor benchmark; zero 100-offer retailer pilot; zero statistically measured sector rank/retailer-price-gap yield or buyer-channel overlap; zero run of the full index. No account signup, paid API call or original local S2 runtime; no source permission has been granted by these returns. None of the three research PRs or hostile PR #10 has been integrated into the canonical control branch or main.

## Proposed next flights and gating (not automatically dispatched)

| Order | Responsible independent role | Deliverable | Gate to adoption |
|---|---|---|---|
| P0 | Independent I3 ARB-010 hostile technical/data-rights reviewer | Test source matrix contradictions, paid-price semantics, eBay permission claims, cost at realistic pages and acceptance of proposed source schema | Document exact source cases and uphold or overturn candidates; no self-review |
| P0 | Independent I3 ARB-020 hostile source/vendor reviewer | Test ShopSavvy/B.Buy/feed claims, contracts, coverage inference, published costs, checkout and source-normalization, verify sample denominator/candidate IDs | Independent documented conditional verdict; source permissions still distinct |
| P0 | ARB-035 original-author bounded repair (or separate source-level engineer) | Repair 26 enum states, reclassify 38 generic strata, dated source/US agreement references; rewrite pilot separating true randomized source populations and diagnostic arms | Independent reviewer of exact repaired SHA; only then scoped documentary intake |
| P0 parallel | ARB-030/031/040/051/050/060/071 sourcefree engineering crew | Implement two producer schemas, actual-paid vs ask, identity gates, robust estimator, gap rank and report with synthetic tests and clear live holds | Separate engineering review with no claims of live source access |
| External gate | Source/provider access/rights owner, with user approval | Human official eBay Product Research sample, scoped vendor data-use responses/paid tests only if separately approved; one merchant discovery/checkout provider | Exact permission/cost and reproducible source observations; no passwords or secrets in public repo |
| P1 | Empirical ARB-029/035 study owner after rights cleared | Source-specific enumerated feed yield pilot, 30-item eBay test, reproducible SKU panel, clear sampling denominator and repeated offer observation | Actual positive and negative data with uncertainty, exact independent acceptance |
| P2 optional | Sociological attention investigator | Consented cross-channel buyer attention/direct matched cohort or event-time quasi-experiment | No population-level attention claim from aggregated community or historic price median |

**Decision:** DO NOT MERGE all four branches; do not mark any ARB-010/020/035 producer LIVE or sector winner PROVED. The correct immediate move is separate review of #4/#6, bounded #8 repair under #10's findings, and the first controlled actual-data + sourcefree producer-to-index implementation. This intake branch/document itself is a proposed court for user/HQ adoption, not an independent approval of the workers.
