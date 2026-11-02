# ARB-020 R1 — Cost, scope, credit and true coverage capacity
**As of 2026-10-31; USD public advertised tiers, NOT verified paid invoices or access permission.** The important denominator is **genuine new qualified retailer-purchase comparisons per $**, not # API requests or vendor-reported MSRP markdowns. No actual retailer queries, live costs, backend execution, account entitlements or payment made.

## Four required separate counting units
1. **Offers discovered:** raw candidate listing/deal rows; may duplicate the same UPC, be expired, use a marketplace seller, refer to wrong condition or require a local checkout.
2. **Distinct exact product/offer pairs:** deduplicated merchant+GTIN+variant+condition+pack+region+fulfillment+price.
3. **Validated buyable offers:** source / price / time / availability and all-in cost confirmed, not just old feed.
4. **eBay-normal price qualified opportunities:** sufficient genuine past sales of *identical* item; only these can enter final price-gap index.
Thus: `cost_per_qualified_candidate = (retailer_discovery_spend + retail_verification_spend + eBay_history_spend + required LLM/hardware spend) / N_qualified_eBay_reference_and_purchasable`. If zero qualified, metric is **undefined** and report zero, not infinity presented as a discovery rate.

## Scenario assumptions (not provider results)
N = distinct products OR deals attempted *daily*. D = 30 days/month. Counts: **100/day → 3,000/mo; 1k/day → 30,000/mo; 10k/day → 300,000/mo; 100k/day → 3,000,000/mo.** These are **not** equal to product feed pages or requests. Derive exact bill:
- `deals_credits = ceil(returned_deals / 10)` for ShopSavvy, ignoring any additional fetches and any pagination costs already included;
- `all_retailer_offer_credits = 3 × returned_products`; `single_retailer = 2 × returned_products`; `product_details = 1 × returned_products`; `keyword_search = 1 × results_returned`;
- `90d_offer_price_history = offer_credits + 90 credits PER REQUEST`, only where offers found; batch 100 identifiers/request reduces day-based overhead;
- Keepa `deals_tokens = 5 × number_of_pages`, maximum 150 recent Amazon deal records/page, query max 10k ASINs;
- DataForSEO known-query product/SERP request at `$0.001 Standard` or `$0.002 Priority`; do **not** equate 1 result/SERP to a complete retail item;
- SerpApi `one SERP / returned search` at tier quota;
- feed/affiliate catalogs priced by advertiser partnership, file frequency, permitted use rather than an inferred unit call price;
- eBay history (ARB-010) and final retailer checkout verification are **separate costs** not included in retailer-only tables.

## Monthly cost table A — ShopSavvy exclusively discover 100% of N via deals feed
A **lower-bound, illustrative** cost assuming N total returned deals per day across the feed; no repeats/retries and no extra validation. Real deal feed might not even contain that many unique current offers. Plan caps: Starter 1k credits $49; Pro 10k $199; Enterprise 50k $499; greater requires quote.

| Returned deals/day | 30-day deals | Credits (10 returned/credit) | Lowest listed monthly plan |
|---:|---:|---:|---|
| 100 | 3,000 | **300** | **$49** Starter |
| 1,000 | 30,000 | **3,000** | **$199** Professional |
| 10,000 | 300,000 | **30,000** | **$499** Enterprise |
| 100,000 | 3,000,000 | **300,000** | **CUSTOM**; not proven available |

**Caution:** deals may be ranked, deduped, or geographically selected; no right to extrapolate the 3m thought-experiment into 3m real current bargains. Deals max 100 rows/page; hourly call limit and pagination require testing.

## Monthly cost table B — retrieve ALL retailer offers for every discovered product (3 credits each)
| Unique products/day | Product checks/mo | Credits/mo | Plan |
|---:|---:|---:|---|
| 100 | 3,000 | **9,000** | **$199/mo** Professional |
| 1,000 | 30,000 | **90,000** | **CUSTOM** (>50k) |
| 10,000 | 300,000 | **900,000** | **CUSTOM** |
| 100,000 | 3m | **9,000,000** | **CUSTOM** |

If ALSO paying 1 credit per 10 discovered deals (same N), combined credits are 9,300, 93,000, 930,000, 9.3m. A $49/1k-credit trial does not fund 100 item×daily all-offer refresh for 30d; it is suitable to discover batches and selectively validate. Single-retailer offers reduce 3 to 2 credits/product but still require multi-source breadth elsewhere.

## Candidate-first funnel sensitivity
Illustrative **10,000 returned deals/day** (300k/month): ShopSavvy discovery = 30,000 credits/month. If **1%** (100/day) require an all-retailer follow-up, add 9,000 → **39k credits**; current Enterprise $499/50k fits *credits* (not proven throughput). If 5% (500/day) follow-up, add 45k → **75k credits** requiring a custom plan. All of this excludes the eBay lookup, retailer checkout, duplicate feed rows and unknown real per-deal usefulness. Never buy 50k credits until trial demonstrates returns.

ShopSavvy price-history sensitivity: one 90d historical merchant-price request for **one** item could cost 3 + 90 = 93 credits, but batch 10 items sharing 90d window costs 30 + 90 = 120 (not 930). However **retailer asking/offer history is not eBay completed-sales history**. Do not build the ARB-051 estimator from this data.

## Cost table C — known-product shopping checks (one result/SERP per item, NOT discovery census)
| Product-query searches/day | 30d queries | DataForSEO Standard $0.001 each | Priority $0.002 each | SerpApi cheapest documented tier |
|---:|---:|---:|---:|---|
| 100 | 3,000 | **$3** | **$6** | **$75/month (5k)** |
| 1,000 | 30,000 | **$30** | **$60** | **$275/month (30k)** |
| 10,000 | 300,000 | **$300** | **$600** | **ENTERPRISE QUOTE** |
| 100,000 | 3,000,000 | **$3,000** | **$6,000** | **ENTERPRISE QUOTE** |

**Interpretation:** These are optimistic unit costs **not output prices for checking all actual stock**, because Google Shopping results may require multiple queries, product detail calls, merchant result pages and additional checkout verification. DataForSEO Standard tasks may take up to 45 minutes; its cited $50 initial prepaid deposit is a cash commitment but balance is consumed rather than a separate $50 subscription. SearchAPI pricing unverified; don't counterfeit a comparison.

## Cost table D — Keepa Amazon-specific deal enumeration
| Deals/day attempted (if present) | Minimum 150-row pages/day | Token expenditure per 30d at 5/page |
|---:|---:|---:|
| 100 | 1 | **150** |
| 1,000 | 7 | **1,050** |
| 10,000 | 67 | **10,050** |
| 100,000 | 667 | **100,050** |

Keepa per-query cap 10k ASINs, priceType restriction and deals only recently updated (last ~12h) may require multiple categories/time slices; keepa paid subscription tokens and exact plan cost **not verified** here. This arithmetic does NOT imply 100k eligible deals/day exist or are obtainable. Token arithmetic is a nonfunctional budget model, not any benchmark.

## Official/free partner lanes: caution on economic claims
- **Best Buy Products API:** published limits 50k calls/day, 5/sec; no public per-call paid tier identified in cited developer docs, but account registration and **specific data-use entitlement not verified**. A single API call can return multiple product rows; never assume 50k calls implies exactly 50k products. Its 72h cache rule is not a license for permanent price-history accumulation.
- **Home Depot daily Impact feed:** free program *application*; actual feed only after approval, live site required; no established price-per-feed and no current access. Product feed may be large without more request charges, but does not automatically include store-level clearance/stock.
- **Awin/CJ/Impact networks:** network account and advertiser grant; some datasets allow full catalogs in CSV/FTP or GraphQL. Bulk feed ingestion can have low marginal per-row API cost **if** permitted, but direct eligibility, storage and merchant-specific rights unpriced.
- **Walmart affiliate/Feed:** no blanket right for this app; written exception may cost time/contract; restricted feed may require category approval.
- **DealNews RSS:** no paid API cost shown, but public RSS display restrictions and index purposes might require a separate grant; not complete.
- **Bright Data/Oxylabs:** prices depend on successful result/target/JavaScript and source rights, not free just because a trial/5k records exists. Scraping paid vendors require independent upstream rights assessment.

## Real-world coverage, delivery and failures drive unit cost
Always count: category feed exhaustion, overlapping retailer ads, deduped offers, GTIN missing, ambiguous or exclusive model numbers, third-party marketplace offer, pickup-only outside region, membership/coupon not actually eligible, promotion expired, delivery charge unknown, inventory stale, wrong bundle, nonexistent eBay actual paid comps. Include `records_discovered`, `unique_exact_ids`, `direct_verified_checkout`, `same_condition_matches`, `qualified_ebay_baseline`, `top10_positive_gaps` as distinct sequential counters. A cheap query-only API may score badly per *qualified bargain* if it finds nothing new.

## Data collection and scaling topology to minimize costs
(1) Licensed daily merchant bulk change feeds and deals as wide inexpensive *top-of-funnel*, rather than querying 100k known identifiers individually. (2) Deduplicate using UPC/MPN and digest before enrichment. (3) Recheck direct merchant price/stock only on ranked shortlist under source terms, not pay every hour for all merchant inventory. (4) Query external eBay price history only after exact identity and plausible retail discount, respecting authorised cache expiry. (5) LLM-assisted fuzzy text review at uncertain cases only; deterministic money, shipping, exclusion and reference statistics inside ArbiScout. (6) Track what **additional unique qualifying results** each new source provides after overlap, then keep or discard it.

## Multi-query/failure scenario
Let `q` product/variant queries per candidate, `p` pages, `r` retry fraction and `v` direct verification calls per possible deal. Nominal known-query billable requests = `N×30×q×p×(1+r) + N×30×v`. If q=2, p=3, r=0 and v=1, **7×** a naive one-lookup budget, *before* eBay. For example 1k products/day implies 210k monthly billable events if every event charged. Rate limiting, geographic store sampling, pricing updates and denied cache make any single '$10/mo' forecast unreliable without controlled trials.

**Bottom line:** The lowest-fee path to unknown bargain discovery is **not necessarily the cheapest SERP**. First-party/approved merchant bulk feeds, ShopSavvy deals and Keepa deal snapshots are structurally stronger; DataForSEO/SerpApi fill *known-item* verification. No estimated revenue, future sale or eventual resale operation enters this budget.
