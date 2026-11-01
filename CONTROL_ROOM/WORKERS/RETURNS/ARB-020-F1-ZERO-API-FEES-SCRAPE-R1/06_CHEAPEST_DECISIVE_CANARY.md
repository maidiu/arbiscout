# ARB-020-F1 — Cheapest decisive 20–50 candidate canary
**Status 2026-10-31: PROTOCOL ONLY — NOT EXECUTED.** No retailer account key, user-selected Mac runner, merchant permission, checkout data, or qualified eBay API access was granted. This is deliberately designed to answer GO/NO-GO without a sprawling new task programme or subscription.

## Single experiment: two acquisition channels, ≤50 products, zero paid retailer data
**Channel A**: Best Buy official Products API if the developer use is accepted for actual *purchaser research*; otherwise one permitted official free merchant catalog API of comparable size. **Channel B**: approved no-fee Home Depot/Impact or Awin/CJ advertiser feed (with current catalog prices and matching IDs); if advertiser approval unavailable, one **named** consenting WooCommerce retailer with branded, on-sale products. These channels are *alternatives*; do not activate disallowed website scrapers for the sake of finishing 50.

### Gate G0 — before any external query
1. Confirm two actual sources with explicit applicable permission (or a terms clause granting the specific retrieval, retention and derived display), no account or billing fee, allowed rate and source/revision date; inspect relevant `robots.txt` for any permitted HTML mode. Use keys privately and user-authorized; no affiliate enrollment/keys requested by this worker.
2. For one retailer, identify actual unknown sale-product discovery mechanism: `onSale` and category pagination, an updated complete advertiser feed, or `on_sale=true` server filter; do not seed only known model names.
3. Specify bounds: maximum 100 source requests total across both, 25 candidate products each source maximum, rate below documented min, at most one store geography unless authorized to scan more; stop on 403/429/captcha, no retries designed to evade.
4. If not two qualified sources, run **one-source canary**, state dual-source criterion unmet, and hold broader discovery. Do not fabricate a second source.

### G1 — Collect 20–50 real dated sale candidates
Sample 10–25 from each approved source using a frozen deterministic selection (first qualifying after consistent category filters plus randomized page positions to avoid cherry-picked extreme discounts), total 20–50; require at least three standardized groups among branded electronics/game consoles, tools/smart home, LEGO/toys, small appliances. Store unique item/merchant URL, fetched timestamp, original page/record hash (if retention permitted), category, SKU/UPC/MPN/revision, condition, pack/kit, price/regular price, shipped or pickup stock, store/ZIP. All observed fields remain null when absent. Reject duplicate SKU/retailer/region/quantity.

No MSRP-based '70% discount' automatically qualifies as an eBay bargain. The **denominator is all source rows inspected**, not only retained likely winners. Record number of raw returned rows, source pages/bytes, removed duplicates and false sale flags.

### G2 — Verify direct price/stock for 10–20
Using explicit approved official API or manually permitted human checkout checks only (not bot checkout/unauthorized scraper), verify 10–20 distinct models from both channels. Verify actual current price available to generic purchaser, seller is retailer-direct/identified merchant, shipping and tax applicability, direct stock and ZIP, time and link. Exclude trade-in credits, future rebates, unavailable membership-only prices, bundles with mismatched components and hidden delivery surcharges. For a missing full total output `TOTAL_UNKNOWN`, not zero.

### G3 — Compare 5–10 exact eBay completed-sales historical references
Use eligible human official eBay Product Research through permitted human account (or independently validated licensed completed-sales API if separately authorized) to inspect exact UPC/MPN, condition, quantity and 90d window. Actual accepted Best Offer price matter; do not use ordinary displayed sold-listing asks as true transaction prices. For each model, record completed-sale count, median/p25, dates, normal reference uncertainty and separately the current retailer all-in purchaser cost; no later sale forecasts. If no sufficiently strong historical sample, exclude. ARB-010 is **HOLD** until eBay data rights/actual paid truth are qualified; a successful retailer test cannot close whole pipeline.

### G4 — Predeclared outcomes
| Criterion | GO threshold | NO-GO/HOLD behavior |
|---|---|---|
| Both retail sources | Written/documented scoped app permission; **$0 recurring retailer data-provider fee**, no workaround | If second absent: one-source PARTIAL only; no broad claims |
| Unknown products | At least 20 live dated offer candidates via unknown-product enumeration, not manually supplied known SKUs | If no true enumeration or 20 rows available, FAIL THIS SOURCE |
| Identity quality | Among accepted items, 100% have defensible exact SKU/brand/model/condition/quantity; may refuse any unknown | If all candidates lack usable GTIN/MPN or variants, STOP SKU comparison |
| Valid checkout | Of 10–20 direct-verified examples, >=80% source current price/availability reproducible (provisional experimental threshold), with source and time; **not an observed figure** | If <=50% match, NO-GO for this feed; intermediate require targeted repair and repeat |
| Data cost/effort | Source calls and human minutes measured, no recurring retail API/proxy/hosting fee | Unexpected mandatory payments/captcha/anti-bot = NO-GO at $0 |
| eBay independent truth | >=5 exact products with sufficient actual completed-price sample, including Best Offer probe where possible, and a defensible observed gap or honest zero | No legally credible eBay history: **RETAILER GO / COMPLETE $0 HOLD** |
| Overall decision | At least one reproducible source-linked live purchase offer with a defensible historical completed-sale comparison; zero candidates can be a truthful output if all verified offers lack positive gap | No independent evidence: do not call it a working price-gap index |

Thresholds are proposed source qualification tests, not empirical population-level statistics; 20–50 rows cannot establish future daily 100–1k throughput or cross-retailer market share. Output interval estimates, not unsupported extrapolation.

### G5 — Stop/scale
- If 20–50 live source offers cannot be obtained *without paid services or violating terms*, stop F1; choose a $0 legal narrower channel or explicitly relax cost constraint by user decision. No more speculative scraper campaign.
- If a signed approval exists and one source proves actual live offers, implement just that producer and deterministic consumer, then measure a week of daily fresh new offers with stock checks before capacity claim.
- If retailer acquisition succeeds but $0 eBay access cannot qualify, keep historical price gate **HOLD**; optional authorized manual eBay oracle pilot or tiny lawful paid-history test belongs to ARB-010 with explicit user approval, not hidden in F1.
- Do not install cron/launchd, send emails to merchants, create accounts or purchase services as part of this paper protocol.

**All stages G0–G5 have NOT BEEN EXECUTED on actual retailers, Mac or eBay.**
