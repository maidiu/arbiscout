# ARB-020 R1 — First producer pilot and independent 100-offer benchmark protocol
**As of 2026-10-31: NOT EXECUTED. ZERO real API offers, price checks, purchases, accounts, credentials, fees, or eBay actual-sale records.** This procedure does not authorize test execution; user selects provider/access/budget and source terms must permit it. First consumer is `ARB-031/033` evidence-grade retailer purchase offer → `ARB-030` exact matching → `ARB-040/051` eBay-normal reference → `ARB-050/060` gap → `ARB-071` source-linked index. A valid result may be 0.

## Preflight: eight distinct candidate discovery modes (comparative selection, not all compulsory subscriptions)
1. **ShopSavvy `GET /v1/deals`** — source-filtered current deal enumeration. Compare latest vs top vs clearance sort; inspect position bias.
2. **Keepa `/deal`** — Amazon price-change/deals, check first-party vs 3P seller and tokens.
3. **Home Depot accepted Impact daily catalog feed** — true manufacturer-coded bulk merchant catalog if permitted.
4. **Best Buy Categories/Products API** — enumerate category or `onSale` product attributes, then store/online stock.
5. **Awin advertiser-approved product feed** — prejoin vs joined feed access, update history and discount attribute.
6. **CJ GraphQL product feed summary/details** — paginated feed and joined publisher grant.
7. **DealNews RSS or authorized community deals** — editorial discovery, attribution and feed terms.
8. **DataForSEO Google Shopping query** — known UPC/keyword baseline; deliberately a *query-only negative comparator* for unknown deal recall.
Optional: Impact other approved advertiser, Walmart requested category Feed and Target current partner feed if permission granted; SerpApi and OpenWebNinja for alternate known-query comparison. No affiliate signup/access presumed.

**Choose exactly one accessible initial producer for ARB-029**, rather than demanding all eight. The eight source families belong in a later comparative benchmark if credentials and licences are acquired. Source-free contract/fixture work may proceed regardless.

## Legitimately authorized acquisition + provenance
Before each actual call: source API contract dated; credentials stored in secure nonpublic environment; permitted retailer/country/categories; quota/expiry/caching/redistribution; provider source provenance/approval; all requests and billable units logged; privacy minimization; no live seller/customer identities in public repo. Do not scrape merchant websites, bypass bots, use session cookies, automate browser-only checkout, register new accounts or accept trials without user approval. Capture written authorization or document HOLD. Query-specific direct retailer checkout verification must be human-permitted or authorized API; no actual purchase.

## Stratified 100-offer prospective sample
Only *after source approval*, build 100 actual dated offer rows, no manufactured IDs. Per-source unique provenance, SKU/GTIN, time and region; do not substitute the source's marketing screenshots.
- 25 electronics/gaming from branded models and variant challenges.
- 20 tools/DIY with bare-tool vs kit, store pickup and bundle variants.
- 20 LEGO/toys/collectibles with set/edition condition challenges.
- 20 small appliances/household with shipping and multi-pack issues.
- 15 purposely adversarial cases: membership, coupons, open-box, third-party seller, no GTIN, wrong location, shipping surcharge, stale, zero-stock or eBay-sparse.
Balance at least 5 product categories, 3+ merchants if the *actual chosen feed provides them*, and 10+ clearly negative controls; if it cannot meet a target say `SAMPLE_FRAME_INSUFFICIENT`, not paper over missing category rows.

## For each raw candidate, freeze and collect
Source/cost record: source family, endpoint/feed version, cursor/page, category/filter, date/time zone, geo, query `candidate_id`, source source URL/hash (respect retention), result position, vendor discount marker. Product record: GTIN/UPC/EAN, brand, manufacturer MPN/revision, product title, condition and pack size, retailer id vs marketplace merchant, source seller and fulfillment flags. Offer: price, currency, listed MSRP, displayed promo, price restrictions, coupons/membership, tax estimates, shipping, pickup region, stock confirmed timestamp, expiry. Direct authoritative price: official merchant URL or consented partner API matching exact GTIN/condition/region, observed checkout-reachable total; if missing → NOT_VERIFIED.

**Two independent audits:**
- **Discovery audit:** source-discovered item is a unique real currently purchasable offer under stated conditions.
- **Economic evidence audit:** its retailer total purchase price is below a statistically adequate same-product regular eBay *completed-sale* price reference from ARB-010. No eBay available → `EBAY_SOURCE_HOLD`, not a bargain.

## Predeclared measurements
For each source, and overall:
- `raw_observed`, `unique_products`, `unique_merchant_offers`, `duplicate_rate`, `added_unique_vs_existing_sources`, `missing_GTIN_rate`, `variant_mismatch_rate`, `wrong_condition_rate`, `third_party_seller_rate`, `out_of_stock_rate`, `out_of_region_pickup_rate`, `expired_offer_rate`, `coupon_ineligible_rate`, `shipping_unknown_rate`.
- `checkouts_verified`, `current_purchase_price_diff` vs aggregator price, `freshness_delay`, `median_latency`, `source_prices_observed` vs direct checkout, `API_billable_units_per_unique_checkout_verified`, `fee_USD`.
- `eBay_90d_valid_sale_count`, `same_condition_volume`, `paid_vs_asking_quality`, `robust_normal_reference`, `p25`, `median`, `conservative_gap`, `final_qualified_count`, `net_new_qualified_vs_other_sources`.
- `source_permission` includes exact contract, purpose and retention rights, no source 'licence YES' from mere access.

**Confidence:** Wilson interval for proportions with denominators (100 overall insufficient for sparse subclass generalization); price-error median/p90 and paired source comparisons, no claim of nationwide market coverage. Undocumented recall cannot be asserted by sampling one source only. Measure marginal yield from adding sources under overlapping real samples.

## Explicit negative test cases
1. Source indicates 70%-off MSRP but eBay-normal price is below retailer all-in offer → **NO_GAP**.
2. Source says $80 in-store but no shop within chosen region stocks item → **LOCAL_NOT_PURCHASABLE**.
3. Source says $40, but shipping $35 / tax unknown → **PRICE_CONDITIONS_INCOMPLETE** until comparable all-in cost.
4. Wrong model revision/region/condition or 2-pack vs 1-pack eBay references → **IDENTITY_REFUSAL**.
5. Third-party Walmart/Amazon seller mislabeled direct → **MERCHANT_IDENTITY_ERROR**.
6. Coupon requires targeted account, deferred rebate or future loyalty credit → **UNATTAINABLE_PRICE** for general offer.
7. ShopSavvy grade A+ without actual eBay completed sales → **NOT_PROOF_OF_GAP**.
8. Price-history merchant asking observation misread as eBay completed sales → **SOURCE_TYPE_ERROR**.
9. High ranked deal but competitor's exact item cheaper → **DEDUPE_CROSS_RETAILER**; retain trace.
10. Product stock or promotion changed between feed and verification → **STALE** with correct times.
11. Feed/retailer terms prohibit deriving index or bulk display → **AUTHORIZATION_HOLD**, even if real price.
12. No approved live eBay source or insufficient 90-day count → **REFERENCE_HOLD**, no invented regular historical price.
13. Data API reaches quota, cycles page cursor, returns sampled top-k only or fails job → **INCOMPLETE**, no inferred full catalog.

## Thresholds for *first limited producer*, NOT historical scientific acceptance
- At least 100 **real acquired** rows under a documented allowed source, or mark unable; exact query/page metadata and cost collected.
- >=95% of *claimed independently-verifiable* purchase prices within $0.01 of same-region merchant checkout **only if truly on same tax/shipping basis**, otherwise report magnitude rather than universal pass. This stringent proposed target is not an achieved result.
- >=95% exact GTIN/model+condition+quantity precision among rows accepted for same-item comparison; ambiguous identity rows excluded rather than guessed.
- Rejected/unknown availability, source-retailer mismatch, missing GST/US sales tax or shipping, expired coupons never silently pass.
- The provider must produce **incremental** discoverable, verified unknown deals, not only known UPC matches. Report 100 sources discovered and fewer valid without "fixing" counts.
- Before real ArbiScout eBay-conditioned pilot, >=1 independently accepted comparable real same-item historical reference and actual retailer price with positive conservative gap; later broad roll-out requires out-of-sample drift verification. This acceptance may be NONE if no qualified item exists; don't pad index.

## Execution gate sequence
G0 source document and permission qualification → G1 user approves account, host, trial/fees and privacy → G2 run limited paid/feed test → G3 independent separate source adjudicator checks samples → G4 strict ARB-031/033 adapter/identity/sourcefree replay → G5 ARB-010 actual eBay history approved → G6 independent historical price estimator and gap computation → G7 one real source-linked purchase-gap item or deliberate zero.

## Future artifacts and run commands (NOT run)
Manifest `offer_benchmark_100.json` with observation IDs and human validated retailer URLs, timestamps and rejection codes; programmatic `validate_offer_contract.py` schema checks; `compare_provider_checkout.py` paired rows (no secret fields) and static report. These scripts are proposed, **not created/executed in this documentary worker return**. Store only permissible, redacted evidence in public repo; confidential data and credentials outside.

**Final benchmark status: NOT EXECUTED 0/100.** This must be reported verbatim; no runtime approval or claimed source accuracy.
