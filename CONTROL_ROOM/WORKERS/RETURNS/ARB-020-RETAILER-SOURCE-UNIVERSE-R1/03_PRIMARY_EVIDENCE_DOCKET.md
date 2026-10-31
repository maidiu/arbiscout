# ARB-020 R1 — Primary-source documentary docket
**Observed 2026-10-31.** Cite URLs as documentary evidence of current published claims/access terms, **not a live feed, price observation or verified purchase-gap yield**. Research covers first-party direct merchant API pages, vendor's own docs and network's own help/terms; retailer homepages in Universe JSON are discovery/context only. Recheck source timestamps/contract versions prior to signing or implementation.

## Direct retailer and governance sources
**E01 Best Buy official APIs:** https://developers.bestbuy.com/apis — Products API describes 1m+ current/historic products, near-real-time pricing; Categories/Stores; Buying Options contains Open Box inventory/condition/prices; Commerce API invite-only (not required for a purchase-link index). See https://bestbuyapis.github.io/api-documentation/ for `salePrice`, `regularPrice`, `onSale`, UPC, condition, availability and store queries. **Limit:** availability online/site/region and checkout price must be tested, no live observations here.

**E02 Best Buy developer terms:** https://developer.bestbuy.com/legal — developer account/key required; 50,000 calls/day and 5 calls/sec; content cache at most 72h and only temporary response-display purpose; licence specifically for own apps in connection with offers/sales of Best Buy goods; restriction on analysis of pricing for a third party (e.g. competing retailers); attributed source/link requirements. Actual ArbiScout application is **retailer purchase-research**, not presumed retailer competitor or resale operation, yet contract applicability remains **HOLD** until written approval. Terms carry old 2021 last-updated header; present service policy must be checked.

**E03 Walmart I/O terms:** https://walmart.io/termsandcondition — API for affiliate partners **solely advertising Walmart.com products**, no other purposes absent express written permission; competitor pricing analysis separately prohibited; 5,000 requests/day default; requested-only category Feed API via `affilops@wal-mart.com`. **Negative:** free affiliate enrollment or API availability is not permission for independent price indexing without relevant positive grant.

**E04 Walmart localized program:** https://walmart.io/docs/dv-volt-api/v1/introduction/ — distinct affiliate marketing catalog, subscription-based online pickup/delivery zip-code price and availability and separate additional-approval commerce/checkout. **Limit:** not a universally open consumer price feed; partner qualifications and price unknown.

**E05 Home Depot:** https://www.homedepot.com/c/SF_MS_Affiliate_Program_FAQs — official homepage explicitly says **daily product data feed** to accepted affiliate websites, partner platform Impact, program free, live website prerequisite; >500k home-shippable products claimed. **Limit:** affiliate-purpose use, feed availability only after acceptance; SKU counts and inventory not verified; local-store clearance unknown.

**E06 Target legacy partner route:** https://partners.target.com/faqs says Impact partners apply, free to join; https://corporate.target.com/news-features/article/2026/05/club-target shows 2026 creator/ambassador changes. **Contradiction/chronology:** prior Target partner FAQs may not establish current 2026 bulk feed eligibility or approval. Ask Target current program specifically; do not count as verified API.

**E07 Lowe's:** https://www.lowes.com/l/creator/joinlowescreator — current creator program to refer sales via links with approved US-based creators. **Limit:** a creator page does not provide published general licensed catalog feed or checkout API.

**E08 Amazon Creators:** https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding/register-for-creators-api — full approved Associates account required, qualifying sales to obtain API. https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction — SearchItems/GetItems/GetVariations/GetBrowseNodes, 10 qualifying sales in past 30d prerequisite published. **Limit:** not an unrestricted Amazon.com price feed; terms and direct-seller vs marketplace merchant basis essential.

## First-party source-network/feed docs
**E09 Awin:** https://help.awin.com/developers/docs/product-feed-publisher-guide-intro — product feed lists product names, price, discounts/shipping, product URLs and attributes, targeted expressly at price comparison/deal publishers; https://help.awin.com/developers/docs/product-feed-list-download — list of accessible feeds includes last update, joined status and download URL; scriptable lists. **Limit:** join status and advertiser provided data, no automatic all-network feed access or permission for arbitrary independent retention.

**E10 CJ:** https://docs.cj.com/docs/productfeed-api-search — GraphQL Feed Summary with `productCount` and `lastUpdated`; product search, 1,000 default/10k max page, pagination/full feed subscription, publisher personal access token and companyId; some feed summaries can include nonjoined advertisers. **Limit:** summary visibility != content entitlement; publisher/advertiser approval and exact use terms separate.

**E11 Impact:** https://help.impact.com/partner/what-would-you-like-to-learn-about/platform-features/marketing-content/product-marketplace-and-catalogs/download-product-catalogs-as-a-partner — approved brands may upload CSV/FTP/API catalogs; brand partnership needed. **Limit:** no assumption that all retail partner programs include complete catalog or zero-delay price changes.

**E12 Rakuten Advertising:** https://rakutenadvertising.com/product-feed-specification/ and https://developers.rakutenadvertising.com/documentation/en/affiliate_apis — product-feed file specification / affiliate APIs; public publisher entitlement to full merchant feed **not proven**.

**E13 Skimlinks:** https://support.skimlinks.com/hc/en-us/articles/39795251710621-Product-Key-API-vs-Data-Feed-Which-Should-I-Use — Product Key API on-demand UPC/ASIN/URL, publisher bulk feed with more fields, merchant refresh around 24h claimed; separately https://support.skimlinks.com/hc/en-us/articles/360024600634-What-is-the-Merchant-API says **Merchant API** limited to Managed tier and is **performance/reporting**, not the same as merchandise/product key API. **Don't conflate product feed, merchant report and merchant approval.**

**E14 Sovrn Commerce:** https://knowledge.sovrn.com/kb/api-onboarding-guide-for-commerce — Merchandise API returns URL-based brand/SKU/UPC/price where available, Approved Merchants API and transactions; https://knowledge.sovrn.com/kb/api-implementation-with-commerce requires Network Quality review. **Limit:** known URL enrichment rather than a proven broad clearance feed.

## True deals and retail comparison — vendor self-documentation
**E15 ShopSavvy deals:** https://shopsavvy.com/data/documentation/deals — `GET /v1/deals` with pagination/sort/category/retailer filters and flags `is_clearance,is_price_drop,is_open_box,requires_membership,has_coupon_code`; 1 credit/10 returned deals. **Crucial:** vendor's grade is *not* eBay-normal price gap. A deal feed is curated; no census of US retailer clearance, and feed source timestamps must be checked.

**E16 ShopSavvy offer/price:** https://shopsavvy.com/data/documentation — cross-retailer `/v1/products/offers` by barcode/ASIN/URL/MPN; price/availability/condition/last seen, plus historical *retailer offers* (not eBay completed sales); doc claims tens of thousands of retailers; unknown actual coverage in user's target categories.

**E17 ShopSavvy quota/price:** https://shopsavvy.com/data/documentation/pricing-credits ; https://shopsavvy.com/pricing — 1 credit per 10 deals; 3 per product all retailer offers, 2 per product single retailer; product search charges 1 per returned result; $49/1000, $199/10000, $499/50000 credits monthly, 14-day trial, **no ongoing free API tier**; 100 identifier/request, 366-day history, 1000 requests/rolling hour. **Documentation contradiction:** some marketing pages describe per-refresh monitoring charges while current pricing-credit documentation says scheduled refreshes free after schedule; query contract before forecasting.

**E18 ShopSavvy B2B terms:** https://shopsavvy.com/terms/api — vendor allows display, storage and use of returned product/offer/history data in own apps/end-user products; prohibits resale/sublicense/redistribution as bulk standalone dataset; third-party-origin data not covered by provider software patent/copyright warranty. **Not** independent confirmation of eBay rights or full source retailer permissions.

**E19 Keepa:** https://keepa.com/api-docs/deals.html — Amazon recent changed-product `/deal` at 5 tokens/150 results, max 10k ASINs per query, data updated last 12h; https://keepa.com/api-docs/ has product and history endpoints (Amazon offer history, not eBay sold history). **Limit:** Amazon-only and deal selection/priceType bias; subscription token prices need approved account/updated quotation.

**E20 DealNews official RSS:** https://www.dealnews.com/pages/rss.html — most recent, most popular, editor's choice and categorical RSS. Terms require attribution on public display and preserving feed content/links/referral codes; browser extension use prohibited. **Not** blanket permission to populate a separate commercial machine index or change links.

**E21 DataForSEO:** https://dataforseo.com/pricing/merchant/google-shopping-api — `$0.001` Standard product/seller/SERP vs `$0.002` Priority; queue delays up to 45m vs 1m. https://dataforseo.com/terms-of-service — DataForSEO disclaims errors from user-side redundant tasks; client license/source terms need review. **Limit:** known-keyword Shopping search is not a complete merchant clearance feed; `$50` prepaid deposit reported separately and must be confirmed before account activation.

**E22 SerpApi:** https://serpapi.com/pricing — free 250 searches/mo; $25/1k, $75/5k, $150/15k, $275/30k, $725/100k; query-based Google Shopping API, no all-retailer completeness guarantee.

**E23 Oxylabs:** https://oxylabs.io/products/web-api/scrape/ecommerce — source-target scraping API, Web API Starter $30/mo with target-specific charge; other page lists up to 2000 results free trial. **Limit:** vendor selling extraction technology is not a source-site data-rights grant or actual checkout validation. Price by target, not assumed one flat fee for all platforms.

**E24 Bright Data:** https://brightdata.com/products/web-scraper/ecommerce — advertised 5k records monthly free, $1.5/1k successful records pay-as-you-go, $499/384k tier. **Limit:** capture-specific parsing, source-site rights, retention, region, SKU/stock semantics must be audited; 'record' is not a verified distinct purchasable deal.

**E25 OpenWebNinja combined:** https://www.openwebninja.com/api/real-time-e-commerce-data — combined search across a selection of large platforms, per-request advertised $25/10k etc; **query-first, not a catalogue-wide or all-clearance feed**. Vendor's own comparison blogs are not independent benchmark proofs.

**E26 Google Merchant:** https://developers.google.com/merchant/api/guides/reports/explore-competitive-landscape — Merchant Center eligibility, merchant account's reports/visibility, **not** open consumer Google Shopping data. Categorically reject as generic retailer discovery feed.

## Evidence gaps, leading contradictions
1. **Unknown-deal discovery vs known-UPC comparison**: ShopSavvy `/deals`, Keepa deals and merchant full feeds are structurally better; Google Shopping SERPs rank answers to supplied queries, not unknown entire US retail stock.
2. **Base price vs purchaser price**: discount percent vs MSRP is never the eBay reference. All sale badges, historic offer charts, product-feed `price` and purchase coupon terms require direct merchant checkout verification and a separately licensed actual eBay history.
3. **Affiliate program**: free signup/website link code is not a guaranteed usable full product feed for the research index; source-side retention and linking terms vary by merchant.
4. **Source economics**: ShopSavvy 1k credits is not 1k products/day; a typical all-retailer offer fetch costs 3 credits each *returned product*, plus discovery/identity, and successful stock checks.
5. **Site scraping**: do not run unapproved bots, session cookies, proxies, hidden APIs or credentialed extraction. An extraction vendor's contract cannot override upstream restrictions.
6. **Retailer universe**: 45 candidate records include many retailer sites with no generally open API established. They are hypotheses, not claims of licensed automated data.
7. **Price evidence**: no live products, feed dates, merchant prices, GTIN matches, stock levels, clearance yields or eBay comparative baselines observed by this worker; pilot **NOT EXECUTED**.
