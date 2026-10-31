# ARB-020 R1 — Executive and two-axis priority verdict
**Observation date:** 2026-10-31. **Disposition:** INDEPENDENT DOCUMENTARY RETURN, **UNADJUDICATED**. No retailer credentials, account signup, checkout, source-paid calls, authorized scrape, live stock observation, eBay sale benchmark, or user payment. Source claims and economic scenarios are prospective. Exact startup control-plane SHA: `79f15d00b23b79213e6c3a85a205ab0821ecdd2d`, replacing the original `64ae2a67...` frozen snapshot.

## Controlling product and critical distinction
ArbiScout is **only** a retailer *purchase-research index*: current *obtainable acquisition prices* for exactly identified, equivalent-condition products vs **regular observed completed-sale eBay prices**, with conservative absolute/relative gaps and 0–10 qualified source-linked daily candidates. Neither downstream resale, seller fees, expected ROI, profits nor inventory management is part of its application.

The retailer problem has **two non-interchangeable queries**:
- **Discovery/recall:** Which previously unknown, currently obtainable unusually discounted products exist across many merchants, including clearance? Search by known UPC or keyword does **not** enumerate all merchant inventory.
- **Verification/precision:** For a candidate exact identity, does the direct retailer actually offer that SKU/condition/bundle in the relevant location, today, for the quoted *all-in purchaser price*? A feed's reference MSRP and a discount badge do **not** prove an eBay-relative gap.

## Evidence-first priority: documented *data access and discovery mechanism* feasibility
These ranks describe public API/feed documentation **not approved account use, observed data quality or completed-sale gap yield**.

| Rank | Acquisition lane | Why it matters | Real blocker |
|---|---|---|---|
| **1A** | **ShopSavvy `GET /v1/deals`** | Real, documented, paginated, **unknown-deal enumerable feed** with retailer/category filters, clearance/price-drop/open-box/coupons; 1 credit/10 returned deals; 14-day Starter trial, $49/1k credits monthly. | Curated selection and unknown denominator, terms allow use in own application but third-party data upstream rights separate; retailer checkout verification remains. This is not eBay history. |
| **1B** | **Best Buy Product + Categories + Buying Options APIs** | Strong official 1m+ historical/current catalog with near-real-time prices, `salePrice`, `regularPrice`, `onSale`, barcode/model and stock, explicit open-box prices. 50k calls/day and 5/sec documented. | Application-purpose terms, 72-hour cache and external price-analysis restrictions; single retailer, **not** proven highest gap yield. |
| **1C** | **Awin / CJ / Impact approved merchant feeds** | Merchant-supplied bulk feed can enumerate **large numbers of catalog goods**, not just keyword top-k. Awin feeds include discounted price and update time; CJ has paginated full-feed subscriptions, Impact has CSV/FTP/API; Home Depot confirms an **official daily Impact feed**. | Affiliate network/advertiser membership, positive data-use licence for nonaffiliate purchase research, product feed availability, location-stock/discount accuracy, comparison purpose. |
| **2A** | **Keepa `/deal` Amazon feed** | 5 tokens/page up to 150 ASINs recently changed, paginated up to 10k per query; useful independent Amazon deal discovery. | Amazon-only, token plan/rights; price type and buy-box seller distinction essential. |
| **2B** | **DealNews RSS** | Official publicly documented category/most-recent/editorial deal RSS; can surface unknown products for selective human-approved validation. | Not comprehensive, editorial submission bias; source says links/referral codes may not be changed, public reuse needs attribution; systematic commercial indexing scope must be approved. |
| **2C** | **DataForSEO Google Shopping** | Cheap known-query/seller comparison (`$0.001` Standard per product/SERP) with region and product/merchant results, useful validation/enrichment. | **QUERY_ONLY**, may miss unknown clearance; $50 deposit; standard queue up to 45m, not freshness oracle. |
| **3** | SerpApi, SearchApi, OpenWebNinja, Oxylabs, Bright Data, Sovrn and Skimlinks | Alternative cross-retailer query or catalogs; supplier-failure substitutes and enrichment. | Search results not whole-catalog enumerations; rights and actual retailer buy-price still untested. |
| **HOLD** | Walmart affiliate/feed, Walmart localized DV-Volt, Amazon Creators, Target partner, Lowe's creator | Attractive categories and possible first-party data, with relevant access pathways. | Walmart API states advertising-only absent express written permission; feed requested by category. Amazon requires accepted Associates/qualifying sales. Target program revised in 2026, so old feed listings not enough. No generic app entitlement. |
| **NONPRODUCTION** | Arbitrary retail site HTML scraping, browser automation, an unapproved affiliate feed, store-only clearance rumors | Could reveal deals but cannot prove compliant, repeatable machine access. | Site terms, unstable parsing, no authentication and location/stock guarantees; do not run. |

## Separate purchase-gap opportunity hypotheses (NOT measured rankings)
Avoid a false league table. An apparent high markdown from MSRP has **zero epistemic force** for the eBay-completed-sale comparison until ARB-010 supplies real sale data. Our strongest *category×source experiments* are:
- **Branded electronics/computers/gaming** through Best Buy, B&H, Adorama, Newegg, GameStop, Amazon and manufacturer-direct: exact UPC/model usually plausible, deeper online competitive-price compression may make real cross-market gaps **smaller** than MSRP discounts imply.
- **Branded power tools/smart home** via Home Depot's daily feed, Lowe's, Best Buy and Walmart: exact manufacturer SKU with frequent seasonal/clearance periods; distinguish bare tool vs battery kit and regional pickup.
- **LEGO and branded toys** via Target, Walmart, Barnes & Noble, LEGO and GameStop: set/edition/pack identity strong, demand seasonality and retired-set time drift can distort 90-day comps.
- **Small household appliances, storage, selected pet-tech** across retailers: UPC often solid, heavy/oversize and package quantities produce false deals.
- **Outlet/open-box/refurb**: possible severe nominal discount but condition equivalence and actual availability must be proved for each unit; do not mingle new eBay comps with used retailer goods.
- **Fashion, furniture, store/private label, anonymous imports:** potentially impressive displayed markdowns but weak exact eBay comparables, white-label aliases, shipping or unsafe identity; later/narrowed lane.

Thus the two-axis result is: ShopSavvy/approved feeds have **better discovery shapes**, Best Buy has **better documented first-party exact price evidence**, and no retailer/category is demonstrated to have the largest eBay-relative gap yield.

## The first operational proof (ARB-029)
Choose one legally accessible source, **not all retailers simultaneously**. First human-permitted small sample: (1) enumerate licensed ShopSavvy deal candidates or Home Depot/Best Buy official catalog discounted products; (2) exact GTIN/MPN + brand/variant/quantity and filter locale/stock/checkout; (3) only where ARB-010 has lawful actual completed eBay sale observations calculate regular baseline, conservative p25, n, recency and uncertainty; (4) generate **one** source-linked qualified retailer purchase-gap record or honest zero. Record paid calls/credits and actual false positives; 100-offer independent pilot is designed, **NOT EXECUTED**.

**Recommended first trial pair:** licensed ShopSavvy `/deals` unknown-discovery and Best Buy first-party catalog/checkout corroboration **where actually overlapping**. If ShopSavvy's trial/terms aren't suitable, use a partner-approved Home Depot daily feed or authorized Best Buy category enumeration as first producer. Keepa is a separate Amazon-specific alternative. Use DataForSEO/SerpApi only for candidate enrichment, not a claim of exhaustive deal discovery.

## Architecture implications
Keep provenance-neutral `ARB-031` Offer record and `ARB-033` current-stock validation: discovery source and true merchant checkout are **two separate observations**, not one magic API. A supplier can generate candidates but may not be authoritative for final purchase price. Build:
`authorized feed/deals/category change → candidate dedup/GTIN → retailer origin verification + stock + shipping/discount conditions → ARB-030 identity → ARB-040/051 actual eBay sale baseline → ARB-050/060 gap + max ranking → ARB-071 0–10 daily index`.
Preserve failed/missing observations, never backfill from MSRP, Google Merchant merchant analytics, future-sale models or LLM guesses.

## Contracts/costs
- ShopSavvy October 2026 B2B terms **permit own apps, including user-facing display and storage**, but explicitly exclude raw feed resale/bulk redistribution and do not indemnify third-party data rights. Confirm exact ArbiScout use and seller/merchant upstream rights.
- Best Buy docs show API fields and quotas, but terms bind application to purpose and cache rules and can restrict third-party pricing analysis. The real activity is *purchaser research*, not resale; request a written determination instead of misrepresenting.
- Home Depot says affiliates need an operational website, approval, and its daily feed is via Impact; a no-fee affiliate signup **is not an unlimited independent indexing licence**.
- Awin and CJ advertiser feeds are **access-dependent**. A feed URL or publisher partnership alone does not grant display and retention outside partner promotion rules.
- No source fee should be incurred without user approval. Price models and 6× sensitivity are in `04_COST_COVERAGE_AND_CAPACITY.md`.

## Truth and review
This court provides **45 retailer records, 32 acquisition source/network records**, evidence docket, source cost model, risk-tiered category hypotheses, 100-offer prospective benchmark, typed source-neutral schema, unsent correspondence and full PROGRAMMA reconciliation. All records are public documentary or explicit UNKNOWN; neither ranks actual realized gap yield nor grants source authority. A separate hostile reviewer is required before HQ acceptance. **Engineering/data access: CONDITIONAL; purchase-gap evidence: HOLD; authorization/privacy: HOLD.**

## Highest-leverage next moves
1. Independent I3 cross-examine five source families: genuine unknown-deal enumeration vs ranked sample, feed completeness, legal access, actual all-in checkout, and $/verified unique gap.
2. Obtain scoped data-use response from ShopSavvy, Best Buy and one approved merchant feed; **do not** create accounts, approve recurring trials or pay without user consent.
3. Choose single ARB-029 source and execute 100 real offer checks only once granted. In parallel finish deterministic ARB-031/030/040/051/050/060/071 sourcefree consumer and negative tests.
4. Resolve ARB-010 eBay completed-sale history separately; this research does not cure that gate.
