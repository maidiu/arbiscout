# ARB-035 / 06 — Exact-SKU demand × retailer-gap × attention Pareto court
**Status:** Proposed measurement and comparison methodology, NO observed price-gap data. No winner ranking or estimated profit. Reference date 2026-10-31.

## Observation unit and admissibility
Each **time-stamped US-region (retailer, merchant-of-record, exact SKU, variant/quantity/condition, price/stock, eBay market, historical window)** is an observation. A product observed from two feeds is not two opportunities; deduplicate at retailer listing/GTIN/region/time key and preserve observation provenance.

The purchase-side number is **total actually purchasable retailer price** = listed item price + mandatory purchase-time shipping, location-correct tax if known, mandatory acquisition charges - only universally redeemable and currently verified immediate discounts. If a membership, one-use coupon, store pickup, delivery date or local tax applies, identify applicable cohort and mark incomparable without it. No future sales, seller fees, hypothetical returns or profit.

Comparable eBay paid-sales require identical product/contents and condition (or separately justified exact condition strata), known accepted-offer consideration or proven paid-price source; shipping must be normalized to a declared basis. Record location/currency, tax treatment and historical date; use robust median `B50`, lower quartile `B25`, upper quartile `B75`, sample `n`, `IQR`, weeks-with-sale, last-sale age. No robust baseline from one exceptional sale.

Let `R` be validated total retailer purchase price, `B50` historical same-condition eBay actual paid sale reference, `B25` lower comparable percentile:
- **Observed absolute gap:** `G50 = B50 - R` USD.
- **Observed conservative gap:** `G25 = B25 - R` USD.
- **Relative gap:** `g50 = G50 / B50` if `B50 > 0`.
- **Conservative relative gap:** `g25 = G25 / B25` if `B25 > 0`; never compare unlike price bases.
- **Historical demand:** `n90`, `active_weeks13 = count(weeks with >= 1 qualified completed sale)`, `last_sale_age_days`, median intersale gap, effective sales frequency. Do not call a ratio of n sold to active listings *true consumer probability*.
- **Retail markdown cadence:** `price_dips_per_sku_90d`, fraction of weekly source checks with same SKU on accessible promotion, duration distribution, median price level *outside* promotions, optional repeat over 365d. Store event calendar is distinct from per-SKU cadence.
- **Detection yield:** `1000 * count(unique verified admissible G25>0 with minimum historical regularity) / count(unique retail candidate offers scanned)`; report per merchant/sector and separately per source credits/time, with nonqualifying denominator retained.
- **Duration:** observed `promotion_end - promotion_start`, right censor when still live and interval censor when missed between polls; do not assign invented 24h windows.
- **Attention overlap:** direct linked consented panel conditional probability and CI; no numeric scalar based on Reddit/Google Trends aggregate.
- **Practical comparability:** reason-coded exclusion for units that cannot be acquired in the specified region, mismatch, tax/shipping unknown, stock unverified, ambiguous true paid eBay price, warranty/serial/restricted product.

## Three competing objectives — never fabricate a universal weighted scalar
1. **Max substantiated absolute-dollar below-eBay gap** while meeting comparison and demand quality gates.
2. **Recurrence and throughput**: number of eligible exact-SKU sales and offer events, plus *qualified unique gaps per 1000 scanned offers*.
3. **Coverage and evidence confidence**: how often a source has valid identifiers, source rights, allowable snapshots, actual checkout, actual eBay paid prices and nonstale stock.

Adopt an **admissible Pareto frontier**: candidate A dominates B only when A is no worse on the prespecified comparable axes `(G25, n90, active_weeks, valid_markdown_event_rate, yield_per_1000, evidence_completeness)` and strictly better on one, with intervals sufficiently separated. Attention separation is an independent explanatory axis **not** a presumed bonus. Do not compare dollar gap across differently sized bundles without exact identity and product-line note. Show uncertainty interval and observed duration rather than hiding gaps behind a score.

## Uncertainty and bias
- **eBay price:** if row-level paid data allowed, bootstrap resample sales *by week or listing cohort* for 95% percentile interval of `B25` and `B50` rather than treating many offers from one seller as independent; report weeks and count. Block bootstrap does not solve provider missingness.
- **Positive gap:** require conservatively **lower uncertainty bound of `B25-R` >0** and preregistered *material dollar threshold* calibrated on purchase research effort, not future resale revenue. If no reliable variance estimate or sample sparse: HOLD, not extrapolate.
- **Yield:** denominator is all prospectively sampled offers, including false GTIN, no eBay history and stockouts; Wilson interval for eligible proportion (stratified design-weighted or bootstrap with correct frame). Curated deal feeds vs random full-catalog feeds are separate sampling frames, never share a naïve denominator.
- **Multiple testing:** report exploratory multiplicity and holdout replication. Use a second month or independent stores/retailer window, not just the best 3 deals among thousands.
- **Reference trend:** estimate rolling 30d/90d medians and 365d context; high price drift or release/retirement invalidates pooled windows; time-match sale event to *preceding* reference where possible to avoid look-ahead.
- **Best Offer provenance:** upper-bound prices bias eBay baseline upward; run sensitivity under accepted-offer missingness; if never resolved mark NO_COMPARABLE_DATA.
- **Selection/representation:** collector forums and ShopSavvy curated deals are selected; one row per real SKU, region, offer time, and draw weights by listing frame. A single local stock unit may be observable but does not establish national reproducibility.

## Seven mandatory separate ranking lanes (all currently **NO EMPIRICAL RANK**)
| Axis | Metric needed | Research-priority strata to test first (NOT measured best) |
|---|---|---|
| 1. eBay actual sales regularity | n90, active weeks, 365d trend | OEM auto; tools; consoles control; LEGO; branded components |
| 2. Ticket size | empirical median normal paid price by exact SKU | cameras/optics; pro IT; instruments; industrial; tool bundles |
| 3. Deep repeat markdowns | repeat SKU dips and duration/90d | Home Depot tools; Best Buy electronic closeouts; LEGO; Adorama clearance |
| 4. Largest proven eBay-relative gap | G25 with statistical band and real stock | **NO RESEARCH WINNER POSSIBLE FROM CURRENT SOURCES**; prioritize intersection experiments |
| 5. Cross-channel attention separation | linked buyer/promotion monitoring and lag study | regional store clearance; obsolete OEM/industrial, with TCG/LEGO fast-alert controls |
| 6. Source/identity observability | valid GTIN/condition+price+stock+rights fraction | Best Buy electronics; LEGO set number; OEM MPN; approved catalogs |
| 7. Balanced Pareto | nondominated evidence-qualified gap yield across source dollar/scan | auto OEM × approved distributor; tools × HD; camera × Adorama; networking × Newegg; LEGO × retailer feeds |

These rows are **test ordering**, NOT claims about how many goods sell, available gap, or real overlap.

## Multi-scenario sensitivity (no fake point estimates)
Show outputs separately at study regimes:
- **Access conservative:** only authorized product history; no vendor inferred Best Offer paid values; checkout required; sparse markets excluded.
- **Discovery broad:** approved full merchant feed and one curated deal feed; weight by separate sampling frames and dedupe.
- **Regional strict:** price qualifies only if home-region purchase and shipping are possible, no assumed remote-pickup access.
- **Price conservatism:** `B25` vs `B50` and lower CI; negative, marginal and positive bands rather than an artificial sure thing.
- **Attention null:** no attention assumption; compare results with attention not measured, and only study it once direct panel data are legitimately available.
- **Cadence stress:** promotion window 1-day vs 7-day/90-day only **as simulation parameters** for methodological test, not fitted claims, and provide sensitivity not predictions.

## Implementation-facing typed output
`{sku_key, retailer_id, retail_offer_id, locale, observed_at, price_basis, total_purchase_price, stock_evidence, seller_type, license_status, exact_identity_status, ebay_source, actual_paid_provenance, sold_count_7_30_90_365, weeks_with_sales, last_sale, B25, B50, B75, B25_CI, G25, G50, gap_uncertainty, currency, observed_promotion_events, observed_offer_lifetime, scan_frame, scanned_offers_denominator, attention_measure_type, refusal_reason[]}`. Never silently replace `null` with 0. Route into ARB-030 identity, ARB-031 offer, ARB-040 paid observations, ARB-051 baseline, ARB-050/060 comparator and ARB-071 daily 0–10 index.
