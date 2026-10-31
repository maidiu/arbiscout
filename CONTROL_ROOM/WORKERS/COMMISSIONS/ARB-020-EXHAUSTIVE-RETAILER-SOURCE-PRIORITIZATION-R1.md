# LAUNCH — ARB-020 — EXHAUSTIVE RETAILER UNIVERSE, BARGAIN-DISCOVERY SOURCES AND PURCHASE-GAP PRIORITIZATION COURT

**COMMISSION STATUS: PREPARED_NOT_LAUNCHED.** Merely writing this file or issuing a GitHub ticket DOES NOT start another agent. The user must dispatch this whole commission in their explicitly selected Browser/Work or qualified local agent harness.

REPOSITORY: `maidiu/arbiscout` — public at last check.
ROLE: Independent **I3 / HIGH retailer-market, product-catalog, API/data-access, economic comparison and source-rights reconnaissance Rabochii**. NOT ArbiScout HQ, account operator, buyer, API approver, product developer, integrator, or own hostile reviewer.
SINGLE_AGENT_FULL_DELIVERABLE: YES — scope includes **the retailer universe and all genuinely plausible data routes**, not one convenient brand or three example retailers.
RECOMMENDED EDITOR/MODEL: Browser / GPT-6 High (user chooses and actually verifies editor, model and reasoning); NO autonomous editor/model/host switch. Token/cost and environment claims UNKNOWN until verified. Browser/Work S0–S1 public primary-source research and authorized GitHub reading/writing sufficient for the documentary court. S2 local scripts/tests ONLY if positively verified and safe. No S3 authenticated retailer/developer/affiliate accounts or billing without explicit user grant.
USER-SPECIFIED OBJECTIVE: ArbiScout is **solely** an internet retail **PURCHASE-RESEARCH** application indexing bargains whose actual obtainable retailer purchase prices are maximally below the **regular historical completed-sale price patterns on eBay for exactly corresponding products**. There is **no downstream sale, fee/ROI, inventory management or intended future transaction** in the application. Do not reinstate earlier historical resale vocabulary as its program.
HQ GOVERNANCE: consult `CONTROL_ROOM/PRODUCT_CONSTITUTION.md`, `CONTROL_ROOM/00_READ_ME_FIRST.md`, `CONTROL_ROOM/PROGRAMMA/00_PROGRAMMA_ARBISCOUT.md`, `DASHBOARD.md`, `01_WORK_REGISTRY.json`, `02_SOURCE_REGISTRY.json`, `QUESTIONS/03_RETAILERS_AND_SHOPPING.json`, `QUESTIONS/04_IMPORTS.json`, `QUESTIONS/05_IDENTITY_PRICE_GAP_AND_REPORT.json`, `CONTROL_ROOM/03_RABOCHII_AND_REVIEWS.md`, `04_SOURCE_PROVENANCE_AND_DECISION_LAW.md`, `06_EXECUTION_AND_GITHUB_LAW.md`, `STATUS/CURRENT_PROGRESS.json` before substantive conclusions.
EXACT FROZEN REFERENCE: `agent/arbiscout-programma-control-room-r1` at `64ae2a67bb13dca0a0711409651e41a55c8917cb` at initial commission. A snapshot, NOT a claim of current branch head when the worker executes. Verify current main, control branch, PRs and active ARB-010 worker/PR #4; do not disturb them. If GitHub writes explicitly authorized, create fresh task branch `agent/arb020-retailer-source-universe-r1` from verified control-room head and record merge-base and exact SHAs; independent draft PR only, no main merge. If not, return complete self-contained deliverables in session and mark UNCOMMITTED.

## Governing problem — WHAT TO DISCOVER

Find the **most fruitful actual online retailers and retailer-data discovery channels** from which ArbiScout can identify many **current, genuinely purchasable** offers on identical products for which eBay has reliable historical completed-sale comparables. Distinguish (A) potential magnitude/frequency of retailer-vs-eBay historical price gap, (B) exact identity matchability, (C) source acquisition and API cost, (D) geographic/stock/offer reliability, (E) documentation/permission for THIS purchase-indexing activity, (F) ability to **discover unknown sale/clearance bargains without previously knowing the UPC or search query**, (G) operational breadth/freshness, and (H) plausible scalability.

**Fundamental constraint:** This is an exploratory ranking, NOT a claim that any retailer has the highest verified real gap yield. Without real authorized eBay historical data from ARB-010, mark the index-yield estimates `HYPOTHESIS_ONLY` or `UNTESTED`. Do NOT fabricate sold-price datasets, currently buyable inventory, verified discounts or vendor permissions. Publish a proposed measurement design and separate confident *data-access feasibility* from unverified *observed opportunity yield*.

## Comprehensive search universe — expand rather than treat as limits

### 1. Major electronics, tools, toys, household, hobby, sports and general retail
Evaluate retail categories and named candidates as examples, not a predetermined league table: Best Buy, Walmart, Target, Home Depot, Lowe's, Amazon direct retail vs Amazon marketplace, Costco, Sam's Club, BJ's, B&H Photo, Newegg, Micro Center, GameStop, Staples, Office Depot, Kohl's, Macy's, Nordstrom Rack, REI, Dick's Sporting Goods, Academy Sports, Bass Pro/Cabela's, Tractor Supply, Harbor Freight, Michaels, Barnes & Noble, LEGO, Disney Store, Walgreens, CVS, Chewy, Petco, PetSmart, Wayfair, major manufacturer outlets and regional retailers. Discover additional better candidates without anchoring on any brand. Examine whether current 2026 retailer existence/coverage/status and open-box/clearance eligibility are real before labeling.

For each, ask: **Which product categories are likely to have highly matchable branded goods, deep verified markdowns, sustained eBay completed-sale observation counts, consistent available prices and usable acquisition data?** Do not equate arbitrary 70%-off MSRP with large gap below the *actual normal eBay sale price*. Distinguish physical store-only clearance, pickup-only, membership or coupon-only offers, outlet/refurbished/third-party merchant listings, seasonal markdowns, multipacks and condition mismatches.

### 2. First-party retail APIs and authorized data feeds
Find publicly documented direct product/search/catalog, offers, promotions, clearance, store availability, region, discounts, price history, and bulk feeds from actual retailers. Explore request rate, field quality, API-key/affiliate/store eligibility, cost and terms. **Best Buy**: Products/Categories/Stores/Buying Options/Open Box and discount fields; do not confuse invite-only Commerce ordering API with open product-data APIs. **Walmart**: clearly separate Affiliate Marketing API, request-only affiliate feed, partner/developer localized price/pickup API and Marketplace Seller APIs (not automatically consumer price feeds). **Target/Home Depot**: distinguish merchant/affiliate/supplier resources from an open consumer price API. **Amazon**: current Creators API versus historical Product Advertising API, Associates onboarding, offer fields/use restrictions, direct Amazon vs third-party seller. Test every vendor claim at its own original documentation rather than a comparative SEO blog.

### 3. Cross-retailer product feeds, catalog and partner networks
Assess Impact, Awin, CJ, Rakuten Advertising, Pepperjam/Ascend, Skimlinks/Sovrn Commerce and other networks only where verified applicable. Determine whether acceptance into an affiliate program or specific advertiser is required, which retailers expose actual products via API/CSV/FTP, product identifier fields, update cadence, allowed use, linking, caching, row/plan limits and data cost. Identify affiliate networks that do **not** actually provide an eligible feed. Never assume an affiliate feed can be used for arbitrary internal indexing; evaluate contract scope for the *actual* purchase-research index, not an invented business.

### 4. Cross-retailer SHOPPING and dedicated DEALS discovery
**Mandatory major research lane:** Compare direct browsing feeds that **enumerate unknown discounts** against search-based price aggregators that require supplied queries/products.

- Google Shopping via SerpApi, DataForSEO, SearchApi, Oxylabs, ScraperAPI, Bright Data, or other valid third-party search/Shopping results providers: exact product/offer/merchant fields, scope, geography, price freshness, query cost, and especially **whether arbitrary retailer sale inventory can be discovered without already specifying keywords/product IDs**. Google Merchant API is distinct and must not be called a general Google Shopping consumer catalog API.
- ShopSavvy **Data API** as a potential *one-provider many-retailer* source: `GET /v1/deals` filters and pagination, cross-retailer offers `/v1/products/offers`, history `/v1/products/offers/history`, exact barcode/model lookup, monitoring and price timestamps. Determine actual domain/retailer coverage, unseen sale-discovery yield, provenance, score selection bias, index-specific contract, category limits and pricing. Its published feed/documentation is more directly relevant to unknown deal discovery than a query-only Shopping search API. **Do not treat vendor's 'grade' as an eBay gap metric or treat its retail offer history as eBay completed-sale history**.
- Slickdeals and other community deal-discovery sites/feeds, DealNews, Rakuten/retail deal aggregators, BrickSeek or similar retail clearance services, price-comparison marketplaces, Keepa for Amazon, merchant email offers and authorized deal feeds. Examine only legitimately available APIs/feeds, category filters, retail source provenance, timestamps, paid plan and ToS. Distinguish unstructured community submissions from machine-verifiable checkout prices.

### 5. Importers and wholesale (differential scope)
Alibaba and AliExpress are optional retailer-acquisition sources, not substitutes for domestic daily clearance. Document API/affiliate/supplier data availability, shipping to US baseline, MOQ/price tiers, identity matching, delays, product authenticity and gap comparisons. Keep source strategy separate where identity cannot be verified.

### 6. Retailer discovery as a quantitative methodology
Develop a **two-dimensional ranking**:
- **Data integration feasibility:** proven fields, exact identifiers, catalog/deal discovery mode, price freshness, availability/geography, accessible onboarding, source permission, engineering complexity, cost at workload.
- **Potential historical eBay price-gap discovery yield:** frequency of legitimate clearance/markdowns, product matchability, reasonable eBay sample density and category health, low noisy third-party/outlet/condition false matches. **Hypotheses until actually measured**.

Do not give Best Buy or any retailer a high gap-yield score just because it has a rich API. Do not give Google Shopping high *discovery completeness* just because it compares known products well. Do not claim aggregator search results enumerate entire retailer catalog. Consider source **combinations** (licensed community deal discovery → direct retailer verification → eBay historical comparison) and marginal contribution/deduplication.

## Required claim/evidence and measurement discipline

For **EVERY** retailer and data provider considered, record:
`retailer_or_network_id; country/coverage; product category hypotheses; direct merchant vs marketplace sellers; actual discount/clearance inventory; source_kind (DIRECT_RETAIL_API, RETAIL_FEED, AFFILIATE_NETWORK, DEALS_FEED, SHOPPING_SEARCH, PUBLIC_MANUAL_ONLY, VENDOR_AGGREGATION, IMPORT_SOURCE); discovery_mode (ENUMERABLE_UNKNOWN_DEALS, CATALOG_PAGINATION, QUERY_ONLY, KNOWN_IDS_ONLY, CATEGORY_BROWSE, MANUAL_ONLY, UNKNOWN); precise API/feed URLs; source fields; UPC/GTIN/model/variant/condition; price, stock, region, fulfillment, shipping, coupon/expiry; last-checked timestamp; product count/coverage; access/signup/account/approval; published costs and quotas; exact terms and permitted-use confidence; license/retention provenance; documented failures; integration difficulty; conditional opportunity hypotheses; benchmark performed?; source refs and retrieval date; priority tier; next action; reviewer flags`.

**Primary sources first:** official retailer developer API/docs, network feed/API/terms and vendor technical manuals. External comparison articles and Reddit/commercial posts may surface candidates but are not authoritative on permissions, count/price or source rights. Cite primary date/URL; vendor marketing is source evidence of a **claim**, not independent confirmation.

No unapproved automated page extraction, private API calls, bypass of bot defenses, account cookies, hidden endpoints, or cost-incurring subscriptions. Do not expose secrets in this PUBLIC GitHub repo. If a lawful sample cannot be acquired, design the sample test and mark NOT_EXECUTED rather than filling in numbers.

## Critical research questions to settle (not a closed list)

- What is the **best source of previously unknown daily bargains**, rather than cheapest way to check a known UPC?
- Which retailers yield reliable near-real-time **actual purchase prices**, not MSRP/banner discounts, in a broad enumerated feed?
- What categories have plentiful exact matching and adequate eBay historical-sale observations?
- Is a ShopSavvy-like deal feed economically sufficient by itself to propose candidates, or does it miss store-only clearance and important source retailers?
- Which source types are search-first, browse-first, subscription-feed, batch vs individual lookup, and is crawling entire catalog impossible/uneconomical?
- Are Amazon direct retail and 3rd-party listing prices distinguishable, with membership/coupon/location conditions?
- How much of the same offer can be observed through multiple providers, and which is most reliable and timely?
- Can an initial single-source proof yield accurate, independently verified price-gap matches, and what **first pilot** should ARB-029 execute later, depending on ARB-010?
- What is the realistic price for continuously scanning 100 / 1,000 / 10,000 / 100,000 *offers or products per day*, taking **calls, pages, returned items, checks, duplicates and cache** into account?
- Which route provides a zero- or low-cost lawful, reproducible **first proof**, and which is best for large-scale indexing?

## Initial primary-source starting anchors (recheck Oct 2026)

- Best Buy official https://developer.bestbuy.com/apis and https://bestbuyapis.github.io/api-documentation/ — catalog/availability/API scopes, open-box and current pricing.
- Walmart https://walmart.io/termsandcondition ; https://walmart.io/docs/affiliates/introduction ; https://walmart.io/docs/dv-volt-api/v1/introduction/ — affiliate/partner differences, request-only feed, localized data.
- Walmart affiliate eligibility https://affiliates.walmart.com/page/faqs ; current terms https://affiliates.walmart.com/terms.
- Google Shopping vendor docs https://docs.dataforseo.com/v3/merchant-google-overview/ and https://serpapi.com/google-shopping-api — keyword/product constrained structured Shopping output.
- ShopSavvy `/v1/deals` https://shopsavvy.com/data/documentation/deals ; all API docs https://shopsavvy.com/data/documentation ; plans and **credit arithmetic** https://shopsavvy.com/pricing . As publicly documented in October 2026, monthly Starter $49/1,000 credits, Pro $199/10,000, Enterprise/Scale around $499/50,000; 1 credit/10 deals, 3 credits per all-retailer offer item, optional price history costs additional credits. **Verify, not assume** accuracy, current plan, broad discovery completeness or permitted indexing.
- Amazon Creators API onboarding https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding — Associates prerequisites; verify retailer purchase-index use.
- Third-party deal sites, affiliate networks, category aggregators and low-cost retailer feed sources must be independently discovered and checked against their *own* terms.

## REQUIRED INDEPENDENT PILOT DESIGN

Construct a stratified, **nonexecuted until authorized** comparison framework:
- At least 8 candidate discovery modes/providers (including at least one true deals feed and one direct retailer API).
- At least 5 retailer categories and products with GTIN/model evidence.
- Sample at least 100 actual dated offers **only if legitimately acquired**, including store-only and third-party merchant exclusions; request direct purchase-price verification on a balanced subset.
- For each source compute: offers found per request/dollar; genuinely new (not duplicate) current purchase offers; missing UPC/model rate; wrong variant/condition rate; confirmed availability; false markdown rate; coverage across categories; error/freshness; share with sufficient eBay completed-sale references **when ARB-010 supplies them**; and ultimately actual size/distribution of qualified retailer-to-eBay gaps.
- Observe explicit failure-mode samples: no stock, wrong location, coupon exclusion, marketplace seller, expired clearance, bundle inconsistency, missing GTIN, noncomparable eBay variant, category with sparse eBay history, and aggregator missing catalog-wide deals.
- Required `ARB-029` decision: **choose a first source that can be actually tested**, not a universal integration of Walmart, Best Buy and Google Shopping.

## REQUIRED COMPLETE RETURN (one worker, independent review later)

If GitHub writes authorized, use isolated branch and return under:
`CONTROL_ROOM/WORKERS/RETURNS/ARB-020-RETAILER-SOURCE-UNIVERSE-R1/`

1. `00_EXECUTIVE_AND_PRIORITY_VERDICT.md` — two different leaderboards: actual documented data feasibility and **hypothesized** purchase-gap yield, plus first proof and expansion flights. Label all unverified confidence explicitly.
2. `01_RETAILER_UNIVERSE.json` — minimum 25 sufficiently documented retailers/categories, more where justified, real negative findings, no invented fields.
3. `02_SOURCE_AND_NETWORK_MATRIX.json` — direct APIs, cross-retailer feed networks, deal discovery, Shopping aggregators, import providers, each with mandatory detailed provenance/access/right/cost/source-type/discovery-mode fields.
4. `03_PRIMARY_EVIDENCE_DOCKET.md` — exact official URLs, date, relevant field or short clause, claim, contradiction, limitations, why-not and confidence.
5. `04_COST_COVERAGE_AND_CAPACITY.md` — free-tier/startup/access/call/credit/rate costs and **100 / 1k / 10k / 100k daily products** modeling with stated assumptions.
6. `05_CATEGORY_AND_DISCOVERY_HYPOTHESES.md` — category×retailer reasons to test, exact-match availability, no invented observed profit or eBay comparisons.
7. `06_FIRST_PILOT_AND_BENCHMARK_PROTOCOL.md` — one-source-first ARB-029 method, source choices, thresholds, samples and negative tests without pretending to have executed.
8. `07_NORMALIZED_RETAIL_OFFER_CONTRACT.json` — propose fields/validation for ARB-031/033: retailer, merchant, item identity, variant/condition/quantity, observed purchase price, shipping/pickup costs, availability/region, date, link, restriction flags, provenance, nulls/refusals.
9. `08_RETAILER_ONBOARDING_AND_PERMISSION_QUESTIONS.md` — ready-to-send exact questions to top source vendors and retailer partner programs; **do not send**.
10. `09_RETURN_AND_PROGRAMMA_RECONCILIATION.md` — exact branch/commit, reviewed source IDs and scope, actual tool/test results, full why-not, current statuses of ARB-020 through ARB-029, Q031–Q052 (and Q053–059 where relevant), suggested nonoverlapping Rabochii follow-ups and no-loss handoff.

If GitHub writes unqualified, deliver complete contents as a single bounded session output and mark UNCOMMITTED. No payment, API account registration, unauthorized downloads, production integrations, new worker launches or modifications to unrelated ARB-010 branch. Do not automatically update canonical PROGRAMMA statuses based on your own unreviewed return or merge a branch.

## POST-RETURN HOSTILE REVIEW

A separate reviewer, appointed by HQ/user, must independently challenge the full *actual source* matrix, permission clause interpretations, affiliate vs non-affiliate field assumptions, currency/cost arithmetic, product identity and geographic false positives, benchmark honesty, false retailer-gain rankings, and source discovery completeness. Maintain separate **ENGINEERING/DATA ACCESS**, **PURCHASE-GAP-EVIDENCE**, and **AUTHORIZATION/PRIVACY** dispositions. Reviewer is not this Rabochii.

**STOP CONDITIONS:** requests for secrets or account access, paid trials/subscriptions, unexpected host/model switch, sources with prohibited automation, unverified scraper/undocumented endpoints, vendor price assumptions lacking primary source, other active branch conflicts. Continue other documentable lanes and return exact HOLDs.

**TERMINAL QUESTION:** What set of **retailers and data-discovery methods** gives ArbiScout the broadest and most economical chance of finding **real, exactly matchable, current retailer purchase prices far below ordinary eBay completed-sale patterns**, and what evidence/permissions/tests are still missing to establish which are actually best?
