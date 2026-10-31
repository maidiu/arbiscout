# ARB-010 R1 — Draft eBay/provider questions (NOT SENT)
**Date:** 2026-10-31. **Draft only.** No emails, portal tickets, account creations, API requests, authentication or paid subscriptions were initiated. Submit only after user explicitly chooses channel and authorizes the inquiry. All questions describe **ArbiScout as a retailer purchase-research index comparing documented current retailer purchase prices with past actual eBay completed-sale prices for identical products**; no downstream sales forecast, fee, ROI or resale service is part of the requested use.

## A. eBay developer and business/data licensing inquiry — send only if authorized
Subject: Request for authorized historical eBay completed-sales data for third-party retailer purchase-price research

We are evaluating an application that compares current prices offered by major internet retailers for exact GTIN/model/condition/quantity with historically observed *real completed eBay sale prices* for the same goods. The application produces a source-linked purchase-research index; it does not list goods, recommend prices for eBay sellers, project future sales, model fees or trade on behalf of other parties. We want to use a documented and expressly permitted eBay data interface, not scrape Seller Hub or other eBay pages.

1. Is there a current eBay program, sanctioned API, batch export, partner data licence or third-party data redistribution channel that exposes **other sellers' item-level completed-sale observations** market-wide? Please distinguish private/seller-owned orders, active item feeds, aggregated research statistics and individual historical paid prices.
2. Product Research documents up to three years and actual accepted Best Offer price: is there a **supported machine-readable API or authorized export** specifically for these observations? If no, please explicitly confirm. Are any manually recorded aggregates/derived statistics from a permitted Product Research user allowed in an independently operated retailer purchase-research index, with reproducible internal evidence retention? Can third-party operators be delegated Team Access without automating its interface?
3. Marketplace Insights `item_sales`: official matrix says **not open to new users**. Is there any current partner/enterprise exception or successor that is admitting applicants? Which categories/sites/90d lookback, request quotas and allowed data fields apply? Are actual accepted Best Offer amounts available, or only displayed listing prices?
4. Does the Buy/Feed/GraphQL family or new 2026 product expose individual historical transactions otherwise not described by Marketplace Insights? Please supply **current, public or partner-specific documentation** and the exact current product name, not a generic developer API suggestion.
5. What is the source-level definition of one sale, amount (buyer-paid item price vs last ask), quantity, sold timestamp, shipping and currency? Can we obtain stable listing/sale IDs, model/GTIN, condition, and completeness/coverage metadata by category/marketplace over 90d/1y/3y?
6. Is the proposed **retailer purchase-price historical comparison** permitted by the API License Agreement, restrictions on pricing-derived analytics, competitive use and eBay Marketplace data redistribution? Please identify precise controlling provisions/required special grant. Is internal retention of raw records and publication of aggregated median/quantile comparison allowed, and for how long? Does a public user-facing reference price differ from internal use?
7. What application review, OAuth scopes, whitelisting, commercial minimums, SLA, data protection, user data deletion/expiry and quota/billing obligations would apply? Who can provide a signed data access/licensing determination?
8. Can approved use include independent audit against eBay Product Research of 30 selected real product identities, without automated page extraction? Are source-level data removal notices/updates available?

**Requested answer form:** named endpoint or product, current document version, admissible applicant class, verified use-case permission, covered markets/categories/fields/windows, price schedule and the office/contract capable of authorizing it. No login or nonpublic credential is requested in correspondence.

## B. Common questionnaire for every specialized API supplier
**Scope statement:** We want your API as a machine-readable historical *completed-sale observation* source, only for comparisons of the same product with **current retailer purchase offers**; no onward transaction model. Please answer under the terms actually governing this use case, in writing and with example **redacted** JSON, not customer authentication secrets.

1. **Truth:** Does field X equal amount actually paid by the buyer (excluding seller-listed ask), including accepted Best Offers? Which source/method substantiates the true price for each sale? Does a `soldPrice`, `sale_price` or `best_offer` flag sometimes mean a listed upper bound, proxy, last ask, or listing-wide average? Are sales of multiple quantities separated into dated transactions?
2. **Identity:** Are UPC/EAN/GTIN, ePID/MPN, manufacturer model/revision, color, storage capacity, pack quantity, bundle contents, item condition and refurbishment status returned or filterable? How do you resolve multiple unrelated title matches or listing variants?
3. **History and completeness:** Is your 90d/365d/1095d query a comprehensive timestamp-bounded archive or ranked/capped page of live publicly surfaced listings? Supply per-query total, unique sale/listing IDs, cursor limits, date distribution, deduplication, archival migration gaps, deleted sales handling and missingness. Is your result count transactions, listings or quantities?
4. **Price basis:** Sale item only vs buyer's item+shipping, taxes, discounts, conversion currency/date, Best Offer time lag and refund/reversal treatment? How do you represent null/unknown/upper-bound? May we see an example showing Best Offer with *two different* ask and actual paid amounts and its source-level corroboration?
5. **Provenance and upstream rights:** Is the eBay sale data sourced through an **eBay approved feed/partner grant**, your permitted licensed archive, or automated retrieval from eBay pages/authenticated sessions? Please provide the legal basis of acquisition and whether eBay expressly permits it, with authorized written acknowledgement or agreement provisions where discloseable. A vendor-side customer API licence alone is **not** a complete response.
6. **Permitted application use:** Are internal retailer purchase-price benchmarking, retention of source observations and source-derived public historical median/p25/p75 figures expressly allowed? Are verbatim rows, example links, screenshot citations, public caching, sublicense, redistribution and user-visible historic references restricted? What expiry, deletion, attribution and data correction duties apply? May developer/public GitHub contain synthetic fixtures only?
7. **API and cost:** exact current API docs/JSON schema; sandbox/live approval; per-request vs per-page vs per-item billable unit, batch discount, `hydrateBoa` extra charges, 429 handling, paid retries, rate and concurrency limits, free tier monthly vs one-time, 30/90/365/1095d plan gates, pricing/quotes for **3k / 30k / 300k successful pages monthly** and **6× sensitivity**; data freshness, caching expiry, refunds, SLA and vendor support.
8. **Benchmark:** Will you authorize a 30-item stratified independent comparison with official eBay Product Research, including six accepted-offer cases, negative/sparse examples and 90d/3y comparisons? Can we publish aggregate accuracy/error and missingness findings even if unfavorable? Can you provide the same dates and marketplaces as the official oracle?
9. **Privacy/security:** Are eBay session cookies, eBay seller login credentials, buyer information or rotating residential IPs needed behind your service? Whose account authorization, if any, covers it? Can we use only a vendor key and no access to our eBay account? Your customer credentials must never be shared in a public repo.

**Responses that are not evidence:** 'works for many customers', 'we are compliant', 'public data', 'we only supply an API', a successful request screenshot, an SEO competitor comparison or a website footer saying 'not affiliated with eBay'. Ask for terms and field semantics.

## C. Provider-targeted contradiction probes
### CompsAPI
- Your [terms](https://compsapi.com/terms) say no representation about third-party underlying rights, while allowing our derived statistics and indefinite retention of retrieved data. What is the **affirmative eBay data acquisition permission** for this service? Would public purchase-index price estimates be allowed without releasing raw listings?
- Describe exactly how `best_offer=1` and `verify` distinguish actual accepted price from listing ask and non-verifiable conditions; how many rows have verified actual paid vs missing by category and 90d/3y window?
- What does `days=1095` return at Growth tier if sold listing search is capped? Are prices per sold unit or per listing, and how are repetitions, revisions and bundles handled?
- Are $9 5k / $29 25k / $79 100k tiers monthly and is 300k+/mo commercial plan actually available? Can each product be searched by GTIN, exact filters, date and market?

### CompSniper
- On https://compsniper.com/terms (Aug 26 2026) Best Offer displayed prices are called **upper bounds**, but https://api.compsniper.com/pricing claims actual accepted offers. Which document describes the current API correctly? Show first-party validation of the exact field, changed acquisition method, rollout date and percentage of records where actual amount remains unknown.
- Does 3-year `/v1/research/sold` produce atomic sale events or listing aggregation? Your docs show `soldPrice=null`, `soldDate=null`, `averageSoldPrice` and `condition=null` for some records. Can any historical endpoint return actual per-sale timestamp, paid item price and condition at scale? If not, state limitation.
- Confirm recent `/v1/scrape` vs archival request charge, rate and country features separately.

### Soldgraph
- Please confirm `best_offer_accepted` and `displayed_price` are **not** accepted paid amount and `completeness=provider_page_only` cannot prove full population. Is there any licensed alternate data feed with actual offer prices?
- Is free 100 for a **new** account one-time? Does a paid cache hit count as a request? Can per-product 90d window paginate exhaustively and report total number of sale transactions?

### SoldComps
- Exactly when does `hydrateBoa=true` return actual `boaAcceptedPrice` rather than ask? Is unresolved value null with `best_offer` flag? Which currency? Are additional units charged per successful hydrated listing or per page/job?
- Can you certify the provenance of each hydrated offer and offer inclusion rate by category, plus rights for internal purchase-price benchmarking and public aggregates?

### Trawl
- Of your multi-year US/UK archive, what fraction has source-true accepted Best Offer prices? Your docs call `sale_price` the original asking price for offers, with category-specific collectible details. Are exact sale timestamp, quantity and condition available outside collectibles?
- What exact daily 10k product/300k monthly page plan and 2-credit detailed-item multiplier applies? How is archive completeness established?

### eBay Sold Listings API
- Your site describes **signed-in retrieval and parsing**. Is this an eBay-approved collection arrangement, and whose login is used? Provide express eBay grant or partner framework for sale-price collection and redistribution; no user credentials or cookies will be supplied.
- In `bestOfferPrice=true` mode what proportion have `found`, `pending`, `not_available`? Can historical `acceptedOfferPrice` independently match eBay Product Research and be priced in source currency rather than USD conversion? Can 300k/mo run on $299 'unlimited' without fair-use throttling?

## D. Specialist/vendor archive follow-up (only if general providers fail)
To WorthPoint, ZIK Analytics, ShelfTrend, 130point and possible licensed archive curators: Do you offer documented **item-level eBay completed-sale price observations**, with paid amount and accepted offer, original currency/condition/quantity and dates across major product categories? Is there a sanctioned API or redistributable machine export and specific grant for a public retailer purchase-research index? If not, your research UI or synthesized guide prices will not meet ARB-010. To PriceCharting: documentation says historical sales unsupported by Prices API; is there a **different separately licensed historical raw-sales product**? Do not infer that it exists.

## Return and correspondence controls
All inquiries remain **NOT SENT**. Preserve vendor-written responses and any licence/contract in a permission-controlled location, not public GitHub. Record sender, date, exact quoted operative clauses and document revision; adjudicate independently of promotional claims. Accounts, spending, and vendor data-processing terms require user approval before use.
