# ARB-010 R1 — Independent 30-product adversarial benchmark (NOT EXECUTED)
**Research date:** 2026-10-31. **Execution:** **NOT EXECUTED**. No permitted eBay Product Research account session, third-party vendor key, eBay data license or authorized API test was available. This is a protocol for later user-approved human and provider operations; **not** a claim of live precision, coverage, median agreement or prices.

## Adversarial oracle construction (30 exact identities, not 30 loose keywords)
Select actual purchased-at-retailer product identifiers from real storefronts only after validating their UPC/GTIN/MPN/model, revision, condition, quantity and marketplace. Record purchase-side detail only to define exact-product comparison; no future-sale model. **Do not fabricate SKU/UPC or result counts.** Stratify precisely:

| Slots | Sampling strata / targeted challenge | Acceptance trace |
|---|---|---|
| E01–E02 | Common branded chargers/cables with genuine model/connector/revision differences | Exact UPC/MPN and unit count; reject visually similar counterfeit/multipacks |
| E03–E04 | Branded headphones/earbuds with old/new revisions and retailer region differences | Model suffix, sealed/new vs refurbished, color if value-sensitive |
| E05–E06 | Branded SSD/storage with capacity, hardware generation and packaging differences | Capacity, revision, region/warranty; bundle exclusion |
| E07–E08 | Computer accessories/input peripherals with firmware/revision or layout variants | GTIN/model, language/region, genuine condition |
| E09–E10 | Small consumer electronics with high sales volume | 10+ true transactions and stable identity; include accepted-offer candidate |
| M11–M12 | Branded power tools with 'tool only' vs kit batteries/charger | Tool/kit exact bill-of-materials and quantity |
| M13–M14 | Appliance/household models with pack-size or color mismatch | Same model and quantity, shipping/pickup distinctions |
| M15–M16 | Toys/building sets with sealed vs opened, complete vs incomplete | Exact edition, piece/set number, sealed condition |
| M17–M18 | Personal-care devices/household consumables with 1-, 2- or 4-packs | GTIN, size and no per-pack price coercion |
| M19–M20 | Replacement parts / home goods with model revision and compatibility | Manufacturer part number, condition, compatible vs OEM |
| H21–H22 | Sparse/zero recent sales but some older sales | Explicit zero/singleton behavior; same item 90d vs 3y |
| H23–H24 | Mixed open-box/used/refurbished within a keyword | Condition-conditioned oracle; exclusion of wrong conditions |
| H25–H26 | Bundles, accessories, lots, or multiunit listings | Quantity and identical bundle verification; mark nontransaction averages |
| H27–H28 | Accepted Best Offer with displayed ask distinct from actual paid | Product Research vs vendor paid-price/upper-bound disagreement |
| H29–H30 | Contradictory outliers, stale cached page, cross-marketplace/currency | Capture historical date and region, currency at sale, high shipping and duplicate ID |

This is a **selection recipe**; it contains 30 distinct test slots, **not** 30 sampled products. Human investigator must fill canonical exact-model, UPC, URL, observed condition/quantity, site and selection timestamp. Balance 10 common electronics, 10 toys/tools/appliances, 10 adverse cases; include at least six confirmed accepted-offer cases if realistically findable. Record empty strata transparently instead of cherry-picking alternatives.

## Oracle procedure
1. Under human-permitted eBay Seller Hub Product Research (or authorized Team Access), fix marketplace and timezone, 90d window and, separately, comparable 365/1095d when available; use exact GTIN/MPN or model query plus condition and category. Log precise query, filters, UTC date endpoints, actual UI field labels and tool version. Do not harvest hidden interfaces or use scraping plugins.
2. For each slot record official sold count, price range, median where provided (calculate median from manually permitted individual rows only where licensed), average, interquartile range, accepted-offer paid amount where visible, shipping, and matching/exclusion notes. Mark official `count_method` (transactions vs listings vs quantities) rather than assuming; record if oracle shows aggregates only and cannot support listing-level reconciliation. Save permitted redacted references locally rather than buyer/seller personal data in public GitHub.
3. Independently request each eligible provider's documented endpoint with the **same product identifiers and markets/date boundaries**, after written authorization. Preserve JSON response hash, request parameters, code, page/cursor chain, status, latency, quota, cache age, query endpoint version and field semantics. Pay no fee or run any call before explicit separate user approval.
4. Gather all pages to a vendor's published termination, or record `CENSORED_MAX_PAGE`, `PARTIAL`, timeout and unsupported date window. Deduplicate by provider item/transaction ID plus event time/quantity; do not collapse repeated genuine multiunit transactions. Test 90d independently of 3y; 90d count/median agreement is a narrower claim than 3y completeness.
5. Freeze matching decisions blinded to vendor-price outcome. Two human adjudicators independently review ambiguous product/condition/quantity matches; reconcile disagreements. Capture rejected rows and reasons.

## Price-truth taxonomy
- `ACTUAL_PAID_VERIFIED`: realized buyer-paid item amount corroborated by official Product Research or independently validated first-party method for that sale.
- `PAID_VENDOR_CLAIM_UNVERIFIED`: vendor labels amount paid, but oracle corroboration missing. **Not yet usable** for production baseline.
- `DISPLAYED_ASK` / `BEST_OFFER_UPPER_BOUND`: shown listing price may exceed accepted amount. **Never converted to transaction price.**
- `LISTING_AVERAGE`: per listing aggregate of multiple sales. **Not a single sale.**
- `UNKNOWN`/null: no proven actual-paid price. **Do not fill with asking, average, reserve, or historical guide prices.**

Use shipping as a separate dimension. An accepted-offer item paid 25 USD with 15 USD shipping is not directly comparable to a 30 USD free-shipping identical product without item+shipping policy. Keep free shipping, paid shipping, pickup, unknown and calculated location-shipping distinct. Currency conversion needs recorded dated FX rate/source and confidence, not an implicit universal USD.

## Mandatory cross-source comparison measures
- **Coverage:** official count (definition!) vs vendor matched count, fraction with known actual-paid amounts, accepted-offer missingness, deduplication, invalid identity percentage, condition/quantity mismatches, percent archived outside common 90d window, page truncation. Never infer true market-wide recall from an incomplete oracle.
- **Pricing:** where row-level links truly align, exact amount equality/mismatch after identical shipping basis; median absolute error and median percentage error, p25/p75 difference, spread/outlier and robust p20 baseline differences, accepted-offer signed inflation and high shipping effect.
- **Timeliness:** last sold at, query at, provider indexed at, API cache age and 90d/365d/3y gaps.
- **Availability:** success/error on 30 IDs, 429/backoff/retry, max pages, 404/zero-sales, duplicate IDs, variant search OR/AND semantics, batch partial failures, unexpected markets, currency.
- **Authorization:** permission grant identifier/scope/expiry, allowed retention/public derivative, customer user fields (none needed), source provenance claim and eBay written license where appropriate. **Rights test is separate; cannot be 'passed' by data equality.**

## Prespecified acceptance / refusal gates
**Evidence gate:** 30 slots sampled and logged; at least 20 non-sparse products and at least 6 accepted-offer challenge slots if obtainable, with conspicuous unmet quotas recorded. For fully comparable *row-level* matched paid cases, target **>=95%** price equality within smallest currency unit (or explain taxes/FX/shipping distinction) and **>=95%** correct model/condition/quantity. For windows having >=10 exact transactions, target provider median absolute percentage deviation from official within **5%** and high coverage, with uncertainty/distribution displayed. **These are proposed engineering criteria, NOT achieved statistics or a proof of representativeness**. Reject any undocumented conversion of known offer upper bounds into actual paid values, any paid price fabricated from listing averages, or inability to state sample completeness. Nonrepresentative missingness invalidates median acceptance even if sampled price accuracy is high.

**Statistical gate:** Use bootstrap or binomial intervals, not naked 30-item point estimate. Thirty products with correlated listings and uneven category demand are **insufficient to assert market-wide provider completeness**. Require a second blinded out-of-sample audit (and rolling drift canary) before broad promotion. Report product-level vs row-level denominators separately.

**Authorization gate:** provider contract expressly allows actual retailer purchase-research indexing and derived historical reference publication/retention, plus eBay underlying acquisition right sufficiently established; otherwise **HOLD** even if test prices are perfect. Payment, OAuth/app entitlement and technical accessibility are separate tests.

**Scale gate:** measure charged pages per exact product, max response and sustained rate at 100/day, 1k/day, 10k/day. Reject estimate if only a one-page marketing example supports it. A simulated sourcefree client can validate pagination logic but is not an actual provider benchmark.

## Test suite: expected negative behaviors
- ZERO_SALES: zero observations → unavailable, never a price zero.
- SINGLETON: count 1 → insufficient regular reference unless future justified rule; emit NO_BASELINE.
- MULTIPACK / WRONG_VARIANT / WRONG_CONDITION / REFURB: reject even if title similarity high.
- BEST_OFFER_UNRESOLVED: paid field null, ask remains explicit upper bound; no median inclusion as paid.
- MULTIUNIT_LISTING: per-listing average blocked from atomic sale records.
- SHIPPING_UNKNOWN / HIGH_SHIPPING / CROSS_SITE / CROSS_CURRENCY: retain types, refuse false arithmetic.
- ARCHIVE_ONLY: 3y result must not count as 90d record; no fabricated sold time.
- DUPLICATE / CURSOR_CYCLE / TOP_K_CENSOR: deduplicate where justified; flag incomplete.
- TIMEOUT / RATE_LIMIT / STALE_CACHE / DELETE_RETRACTION: status and freshness, never silent last-good as current.
- NEGATIVE_COMPARISON: if historical reference inadequate or lower than current retailer price, do not invent a bargain.

## Reproducible artifact layout for **future** authorized execution
Store versioned manifest for each slot: `slot_id`, `gtin`, `brand`, `model_revision`, `quantity`, `condition`, `marketplace`, `currency`, `time_window`, `oracle_method`, `oracle_summary`, `provider_query_refs`, `provider_row_hashes`, `exclusion_codes`, `rights_grant_ref`, `analyst`, `reviewer`, `observed_at`. Confidential samples/keys only in permitted private secure location; public repo gets redacted numbers, hashes and nonconfidential evidence.

**Actual benchmark outcome this return: NOT EXECUTED (0 / 30).** No scores, accepted-offer match rate, provider price series, real calls or authentic item IDs are claimed.
