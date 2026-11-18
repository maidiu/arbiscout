# ARBISCOUT — MAXIMUM RETAILER ACQUISITION MECHANISM DOSSIER
**OpenCode implementation handoff · 2026-11-17 · 54 retailer/source cases · read-only research, no repository writes.**

> **Controlling interpretation:** The research question is *HOW* a merchant supplies current discounted purchasable products, not whether its HTML is similar to Best Buy. Build retailer-specific adapters. The existing ArbiScout **eBay Sold/Completed opening → user-saved HTML watcher → 30-day calculations → Results UI** remains operational and must not be replaced or reframed as missing. This document is retailer-source research, not a mandate to engineer eBay acquisition anew.

## 1. Evidence, currentness and limits

- **Exact implementation basis:** `maidiu/arbiscout`, branch `work/arbiscout-local-build`, observed commit `65529f5c5d23820d679f8d003157a1dd25d4f994` (verify HEAD again immediately before modifications). The current test ZIP artifact is not production acceptance.
- **Coverage:** 45 original ARB-020 retailer/source cases, 8 later specialist/operating additions, and a separate Dell new-product deal page, totaling **54**. Amazon sold-by-Amazon and Amazon third-party are separate for price provenance. Dell Outlet and new Dell deals also stay separate.
- **Evidence strengths:** `VERIFIED_*` means source-visible URL/product fields or official documentation. `PUBLIC_*` means a public page/docs show the sale surface but no parser fixture. `PRIOR_*` means the older Oct 2026 GitHub investigation, not an independently verified current network trace. `OFFICIAL_API*` means a documented feed endpoint; purpose-specific access and permissions may still be unresolved.
- **Hard limit:** This research did *not* acquire raw HTML/DevTools HAR for all 54 sites, nor simulate user-sign-in/checkout, nor execute the Best Buy crawler against 54 live hosts. **CSS selectors, private XHR endpoints, internal state object paths, and page-completeness are unknown for sites without a real capture**. Never fabricate these. Exact public URL pagination is supplied when corroborated. Browser research results are not a substitute for a reproducible local saved-HTML extraction test.
- **Rights gate:** Site robots/terms and feed licenses are separate from technical possibility. For merchants with documented anti-extraction restrictions (notably Walmart, Target, Newegg, B&H, GameStop and sometimes others), OpenCode may write an offline parser and a permissioned feed adapter, but must not turn this dossier into an unapproved automated crawler or bypass protections.

## 2. Existing ArbiScout code: exact extension seams

**File examined:** `ENGINEERING/arbiscout_app/arbiscout.py` at exact base; current repo app copy also in the GitHub artifact `ArbiScout-Complete-Test-Version`.

| Current function / class | Actual behavior | Generalize / preserve |
|---|---|---|
| `Fetcher.get` | Playwright Chrome/Edge/Chromium or bounded HTTP; checks robots.txt; waits for DOMContentLoaded/load; scrolls; counts Best Buy price selectors | Shared permitted browser session and capture pipeline; per-retailer readiness; preserve refusal on blocked/unauthorized URLs |
| `get_links` / `score_link` | Follows same-host links with sale/clearance/deals keywords; visits a bounded listing queue | Adapter-defined discovery graph; explicit `Next`, `page`, `start` or cursor; dedupe canonical category URLs; do not hard-code one host for merchant subdomains without permission |
| `extract_bestbuy_cards` / `extract_bestbuy_offers` | Best Buy-specific `data-testid` and `.wf-offer` | Keep intact as Best Buy adapter, not global parser |
| `extract_generic_cards` | Picks the first generic candidate selector with hits; text-derived first-dollar parsing can confuse price role | Scan all supported card families, rank by semantic fields/containers and dedupe; reject unlabeled ambiguous amounts |
| `extract_schema` | JSON-LD `Product` / `Offer` carries name, url, price, model/MPN/SKU | Useful fallback after capture; do not assume listing pages expose all products or old price |
| `Store.add` / `.records` | Dedupe by URL/SKU and flag variant or price conflicts; normalized current/regular fields | Preserve output contract, add exact offer identity, source price evidence, condition, stock/region/eligibility and completeness receipts |
| `build_catalog.py` and `providers.py` | Unified retailers (Best Buy, Woot, Meh, Kroger) | Add adapter outputs in same `retailer/products.json` format, then catalog/filter/top-N unchanged |
| `ebay_watcher.py`, `ebay_comparison.py` | User opens/saves eBay Sold/Completed page; watcher ingests saved HTML, extracts dated observations; Results reports distribution | **Do not replace**. Only attach retailer offer provenance/variant metadata and keep matched product identity rules |

**Current bug classes to avoid across every store:** a price-range minimum treated as buyable; two unrelated dollar amounts conflated; a header promotional percentage mistaken for product markdown; one family card with many variants treated as one exact model; quantity/pack mismatch; missing `Next`; stopped scroll too early; stale promotions; regional prices treated as nationwide; coupon/trade-in/reward conflated with unconditional price; membership price published without eligibility; no stock; fetch success with zero product records; and markup changed without negative diagnostics.

## 3. Site-specific mechanism dossiers — all 54

**Legend:** “Observed” below refers only to publicly visible page text/URL or official endpoint documentation, not a Chrome HAR examination. Any HTML/XHR parsing step must first be grounded in a saved capture; URLs are starting discovery surfaces, not automatically authorized crawl targets.

### RET-001 — Best Buy

**Acquisition family:** `HYDRATED_LISTING_WITH_BESTBUY_SELECTORS`. **Evidence status:** `IMPLEMENTED_SOURCE_AND_BANKED_LOCAL_RUN`. **Access gate:** `PURPOSE/TERMS_HOLD`.

- **Where to begin:** https://www.bestbuy.com/black-friday
- **How discovery/traversal actually works or should be investigated:** Start Black Friday and Top 100 category pages; follow ranked sale links at bounded depth; scroll for lazy cards, wait until customer-price elements settle. Existing runner uses 12 secondary pages; no product pages by default.
- **How to read records:** Current code reads [data-testid="product-card"], .wf-offer, generic grid cards, JSON-LD and optional product-page details; archive settled rendered HTML and dedupe by product URL/SKU.
- **What disqualifies or qualifies a real comparable purchase price:** Current/regular price must come from one product observation; inspect open-box, membership, pickup and sold-out separately.
- **OpenCode-specific treatment:** Reuse current browser + extractor; add configurable readiness criteria and correct pagination; do not throw away working Best Buy branch.
- **First-party/documentation evidence:** https://github.com/maidiu/arbiscout/blob/65529f5c5d23820d679f8d003157a1dd25d4f994/ENGINEERING/arbiscout_app/arbiscout.py
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-002 — Walmart

**Acquisition family:** `MARKETPLACE_CLEARANCE_GRID`. **Evidence status:** `PUBLIC_LISTING_TEXT_VERIFIED`. **Access gate:** `EXPLICIT_SITE_RESTRICTION`.

- **Where to begin:** https://www.walmart.com/
- **How discovery/traversal actually works or should be investigated:** Public clearance surface /shop/deals/clearance. Inspect filter and next-page links / network events; exact paging query not proven.
- **How to read records:** Items can show “Options from $X–$Y” and “Was $Z”; a family price range is not a purchasable single SKU price. Extract each offer seller and variant only after selecting exact option.
- **What disqualifies or qualifies a real comparable purchase price:** Distinguish Walmart as seller from marketplace sellers; ZIP pickup/shipping and member prices; do not collapse third-party offers.
- **OpenCode-specific treatment:** Source document and optional manual saved-page parser; no automated website adapter without permitted access. Investigate qualified category feed separately.
- **First-party/documentation evidence:** https://www.walmart.com/shop/deals/clearance
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-003 — Target

**Acquisition family:** `CATEGORY_CLEARANCE_FACETS`. **Evidence status:** `PUBLIC_ENTRY_AND_REPO_TERMS`. **Access gate:** `EXPLICIT_SITE_RESTRICTION`.

- **Where to begin:** https://www.target.com/c/clearance/-/N-5q0ga
- **How discovery/traversal actually works or should be investigated:** Clearance lives at /c/clearance/-/N-5q0ga; inspect filters and page controls in rendered browser; URLs for continuation not established.
- **How to read records:** Collect product cards with DPCI/TCIN and price badges, select variant/condition and Pickup/Ship context. Do not use marketing tile as product.
- **What disqualifies or qualifies a real comparable purchase price:** Target Circle account offers, regional availability and color/size differences.
- **OpenCode-specific treatment:** Site-policy-gated collector; use permitted partner data route or offline saved HTML for parser experiments.
- **First-party/documentation evidence:** https://www.target.com/c/clearance/-/N-5q0ga
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-004 — Home Depot

**Acquisition family:** `PROMOTION_PAGE_PLUS_OFFICIAL_FEED`. **Evidence status:** `OFFICIAL_FEED_DOC_AND_PROMO`. **Access gate:** `APPROVED_FEED_NEEDED`.

- **Where to begin:** https://www.homedepot.com/daily-deals
- **How discovery/traversal actually works or should be investigated:** Daily Deals/Special Buys campaign pages; track actual category landing product links and any pagination; official daily merchant product feed via Impact for approved partners.
- **How to read records:** Manufacturer MPN/model, SKU, store/online availability, promotion ends, specific current offer and original price where actually given; do not infer kit contents from headline.
- **What disqualifies or qualifies a real comparable purchase price:** Free battery/tool bundles, online-only vs store, in-cart promotions, local delivery/freight.
- **OpenCode-specific treatment:** Build Impact importer as first-class route; optional authorized HTML capture for campaign tiles and merchant verification.
- **First-party/documentation evidence:** https://www.homedepot.com/c/SF_MS_Affiliate_Program_FAQs
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-005 — Lowe's

**Acquisition family:** `SAVINGS_LANDING_TO_LOCALIZED_LISTINGS`. **Evidence status:** `PUBLIC_SAVINGS_PAGE`. **Access gate:** `TERMS_REVIEW_RESTRICTION`.

- **Where to begin:** https://www.lowes.com/
- **How discovery/traversal actually works or should be investigated:** Deal discovery entry /l/savings groups daily deals, special events and clearance; discover actual product grids by following category promotions, not the header or banner.
- **How to read records:** Preserve Lowes item number + manufacturer model, store/ZIP selected, sale/was labels and availability; inspect page hydration and real next-page behavior.
- **What disqualifies or qualifies a real comparable purchase price:** Clearance can be local, contractor/membership discounts, project kits and pickup-only.
- **OpenCode-specific treatment:** Manual saved-page proof until source-rights review; approved feed preferred at scale.
- **First-party/documentation evidence:** https://www.lowes.com/l/savings
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-006 — Amazon (sold by Amazon)

**Acquisition family:** `ASIN_OFFER_AND_KEEPA_DEALS`. **Evidence status:** `OFFICIAL_API_DOC`. **Access gate:** `API/TERMS_HOLD`.

- **Where to begin:** https://www.amazon.com/
- **How discovery/traversal actually works or should be investigated:** Use Keepa /deal for enumerable Amazon price-change/deal candidates; Amazon Creators/approved data path for ASIN offer confirmation where permitted. Generic site crawl is not an equivalent.
- **How to read records:** ASIN, offer merchant Amazon.com, Buy Box, condition, shipping/Prime, coupon vs sale; Keepa price-history state and current state separated.
- **What disqualifies or qualifies a real comparable purchase price:** A generic ASIN represents multiple sellers and conditions; avoid claiming price is sold by Amazon without offer verification.
- **OpenCode-specific treatment:** Dedicated Keepa adapter and seller-of-record filter, no Amazon web scraper as default.
- **First-party/documentation evidence:** https://keepa.com/api-docs/deals.html
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-007 — Amazon (third-party marketplace)

**Acquisition family:** `ASIN_SELLER_OFFER_AND_KEEPA`. **Evidence status:** `OFFICIAL_API_DOC`. **Access gate:** `API/TERMS_HOLD`.

- **Where to begin:** https://www.amazon.com/
- **How discovery/traversal actually works or should be investigated:** Same Keepa ASIN discovery, but seller offers must be separately enumerated/qualified; no inference from a single Amazon Buy Box card.
- **How to read records:** Keep seller ID/name, offer ID, fulfillment/shipping and condition; no cross-seller dedupe into one retailer offer.
- **What disqualifies or qualifies a real comparable purchase price:** FBA, FBM, seller shipping, coupons, different price-to-checkout terms.
- **OpenCode-specific treatment:** Separate third-party marketplace purchase-offer schema and source permissions; do not treat as Amazon-direct.
- **First-party/documentation evidence:** https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/resources/offersV2
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-008 — Costco

**Acquisition family:** `MEMBERSHIP_CAMPAIGN_PAGE`. **Evidence status:** `PUBLIC_CAMPAIGN_TERMS`. **Access gate:** `TERMS_HOLD`.

- **Where to begin:** https://www.costco.com/o/-/warehouse-savings
- **How discovery/traversal actually works or should be investigated:** Warehouse Savings /o/-/warehouse-savings lists campaign offers by period, online-only and warehouse-only. Product pages may be member gated; no universal SKU pagination established.
- **How to read records:** Classify savings tiles versus purchasable product pages; capture validity period, online/warehouse scope, pack sizes and member entitlement.
- **What disqualifies or qualifies a real comparable purchase price:** Member-only pricing, warehouse location, bundle/club packaging, shipping, Costco Direct conditions.
- **OpenCode-specific treatment:** Campaign parser only on permissioned/saved pages; do not equate public flyer saving with actual current acquisition price.
- **First-party/documentation evidence:** https://www.costco.com/o/-/warehouse-savings
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-009 — Sam's Club

**Acquisition family:** `MEMBERSHIP_INSTANT_SAVINGS`. **Evidence status:** `OFFICIAL_PROGRAM_TERMS`. **Access gate:** `TERMS_HOLD`.

- **Where to begin:** https://www.samsclub.com/
- **How discovery/traversal actually works or should be investigated:** Instant Savings Program, member-linked online/club inventory; map promotional list to product offers after entitlement and club context selected.
- **How to read records:** Member item ID, club ZIP, offer validity, member actual payable price and pack quantity. Record inaccessible price as unknown.
- **What disqualifies or qualifies a real comparable purchase price:** Membership prerequisite, instant savings can be redeemed once, local club vs online inventory.
- **OpenCode-specific treatment:** No anonymous crawl-as-universal-price; optional authorized member-context proof/partner feed.
- **First-party/documentation evidence:** https://help.samsclub.com/app/answers/detail/a_id/520/~/what-is-sams-club-instant-savings-program
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-010 — BJ's Wholesale

**Acquisition family:** `MEMBERSHIP_CLEARANCE_CATEGORY`. **Evidence status:** `PUBLIC_CLEARANCE_PAGE`. **Access gate:** `TERMS_HOLD`.

- **Where to begin:** https://www.bjs.com/
- **How discovery/traversal actually works or should be investigated:** Public /category/clearance/ category hierarchy lists furniture and electronics and supports brand/price/special-offer filters; actual paging needs DOM/HAR.
- **How to read records:** Keep club item, pack count, membership price, store and fulfillment channel; distinguish coupon benefit from price.
- **What disqualifies or qualifies a real comparable purchase price:** Membership, location, split club/online offers, coupon price.
- **OpenCode-specific treatment:** Capture fixture and discover pagination with approved session; do not assume site is nonenumerable.
- **First-party/documentation evidence:** https://www.bjs.com/category/clearance/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-011 — B&H Photo

**Acquisition family:** `DEALZONE_EDITORIAL_LIST`. **Evidence status:** `PUBLIC_DEALZONE_PAGE_AND_REPO_TERMS`. **Access gate:** `EXPLICIT_SITE_RESTRICTION`.

- **Where to begin:** https://www.bhphotovideo.com/find/dealZone.jsp
- **How discovery/traversal actually works or should be investigated:** Deal Zone shows current limited-time camera/computer/audio promotions; record timed section/category links, page continuation unknown.
- **How to read records:** Manufacturer model, B&H SKU, current/regular price when present, rebate and bundle/kit variation; do not interpret promotion countdown as stock.
- **What disqualifies or qualifies a real comparable purchase price:** Instant/mail-in rebates, multi-item kits, ship/tax eligibility.
- **OpenCode-specific treatment:** No unauthorized automated retrieval; saved-page parser or approved price source only.
- **First-party/documentation evidence:** https://www.bhphotovideo.com/find/dealZone.jsp
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-012 — Newegg

**Acquisition family:** `EVENT_SALE_AND_MARKETPLACE_GRID`. **Evidence status:** `PUBLIC_EVENT_PAGE_AND_REPO_TERMS`. **Access gate:** `REPO_RESTRICTED_TERMS_RECHECK`.

- **Where to begin:** https://www.newegg.com/
- **How discovery/traversal actually works or should be investigated:** Shell Shocker /Shell-Shocker/EventSaleStore/ID-10381 is time-boxed event inventory; inspect “Shop all deals” secondary category links, paging, and event expiry.
- **How to read records:** Extract brand/MPN, current/regular price, seller name, availability, promo code and combo restrictions.
- **What disqualifies or qualifies a real comparable purchase price:** Third-party marketplace vs Newegg seller, code/limit, new vs refurbished vs open box, event expiration.
- **OpenCode-specific treatment:** Do not deploy unapproved crawler; partner/supplied feed or source-rights exception. Technical parser can be tested on saved snapshots.
- **First-party/documentation evidence:** https://www.newegg.com/Shell-Shocker/EventSaleStore/ID-10381
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-013 — Micro Center

**Acquisition family:** `STORE_SCOPED_CLEARANCE_AND_OPEN_BOX`. **Evidence status:** `PUBLIC_STORE_SPECIFIC_URL`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.microcenter.com/site/content/clearance-outlet.aspx
- **How discovery/traversal actually works or should be investigated:** Clearance/Overstock page plus Open Box and closeout listing surfaces; links support ?storeid=### on site; enumerate *within a chosen store*, not nationwide.
- **How to read records:** Product SKU, model, retail vs open-box, grade, local in-store quantity and SKU-specific price. One-off open-box items separate.
- **What disqualifies or qualifies a real comparable purchase price:** Store-required price visibility (“just sign in” sometimes), pickup-only, grade variation and expired one-off items.
- **OpenCode-specific treatment:** Store-context adapter with refusal if ZIP/selected store unresolved.
- **First-party/documentation evidence:** https://www.microcenter.com/site/content/clearance-outlet.aspx?storeid=101
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-014 — GameStop

**Acquisition family:** `CLEARANCE_FILTERED_COMMERCE_GRID`. **Evidence status:** `PUBLIC_FILTERED_PAGE_AND_REPO_TERMS`. **Access gate:** `EXPLICIT_SITE_RESTRICTION`.

- **Where to begin:** https://www.gamestop.com/deals/electronics/new%2Bpre-owned%2Brefurbished?prefn1=lifecycleStatus&prefv1=Shop+Clearance&sv=new
- **How discovery/traversal actually works or should be investigated:** Deals page /deals and /all-clearance; filter parameters prefn1=lifecycleStatus&prefv1=Shop+Clearance; product condition facets New / Pre-Owned / Refurbished; pagination needs direct anchor inspection.
- **How to read records:** System/platform, edition/region, physical vs digital, GameStop SKU, lifecycle condition, list/Pro price and quantity.
- **What disqualifies or qualifies a real comparable purchase price:** Pro-only price and condition must never compare to new eBay data; excluded gift cards/digital goods.
- **OpenCode-specific treatment:** Tech exists but site terms gate automation; store-furnished feed or manual evidence intake.
- **First-party/documentation evidence:** https://www.gamestop.com/all-clearance
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-015 — Staples

**Acquisition family:** `DEAL_CATEGORY_WITH_PRODUCT_ROWS`. **Evidence status:** `PUBLIC_PRODUCT_PAGE`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.staples.com/deals/Electronics-Deals/BI1278390
- **How discovery/traversal actually works or should be investigated:** Landing /deals/Electronics-Deals/BI1278390 and nested product categories; discover page/sort behavior from actual links/HAR; no reliable query pagination observed.
- **How to read records:** Exact model often appears in Staples item title; capture product page canonical URL, regular/sale price, item number and store availability.
- **What disqualifies or qualifies a real comparable purchase price:** Business/member pricing, coupon thresholds, multipacks and larger printer supply bundles.
- **OpenCode-specific treatment:** Saved HTML card parser candidate; restrict crawler until terms reviewed.
- **First-party/documentation evidence:** https://www.staples.com/deals/Electronics-Deals/BI1278390
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-016 — Office Depot

**Acquisition family:** `TOP_DEALS_LANDING_AND_LOGIN_PRICES`. **Evidence status:** `PUBLIC_DEAL_LANDING`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.officedepot.com/deals
- **How discovery/traversal actually works or should be investigated:** Top Deals /l/deal-center/top-deals and /deals; navigate to clearance product categories; log-in-to-see-price rows cannot be scored anonymously.
- **How to read records:** Office Depot item ID, pack count, business price context and coupon; price visibility state separate from price value.
- **What disqualifies or qualifies a real comparable purchase price:** Business/account prices, buy-online-pickup discounts, tax/shipping coupon terms.
- **OpenCode-specific treatment:** Default to unknown where price hidden; saved-page/parser adaptation only with authorized access.
- **First-party/documentation evidence:** https://www.officedepot.com/l/deal-center/top-deals
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-017 — Kohl's

**Acquisition family:** `EVENT_PROMOTION_TO_PRODUCT_GRID`. **Evidence status:** `PUBLIC_PROMO_TERMS`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.kohls.com/sale-event/todays-deals.jsp
- **How discovery/traversal actually works or should be investigated:** Today’s Deals /sale-event/todays-deals.jsp is promotion-heavy; follow campaign/category result links, not only top page cards.
- **How to read records:** Regular/Original vs Sale labels, promo eligibility and product SKU/size/color; independently capture offer price and coupon condition.
- **What disqualifies or qualifies a real comparable purchase price:** Kohl’s Cash and future reward credits do NOT reduce purchase price; cardholder-only codes and exclusions.
- **OpenCode-specific treatment:** Two-stage campaign discovery → product listing parser; eligibility must be part of offer record.
- **First-party/documentation evidence:** https://www.kohls.com/sale-event/todays-deals.jsp
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-018 — Macy's

**Acquisition family:** `CLEARANCE_VARIANT_GRID`. **Evidence status:** `PUBLIC_SALE_GRID`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.macys.com/shop/sale/clearance-closeout?id=54698
- **How discovery/traversal actually works or should be investigated:** Clearance Closeout /shop/sale/clearance-closeout?id=54698 has department facets and product grid; pagination mechanism not established.
- **How to read records:** Current/Orig. price by product; “now from” or price range is a family, not a purchasable exact variant; resolve style/color/size after selection.
- **What disqualifies or qualifies a real comparable purchase price:** Promo code, final sale, region, size-based price variation.
- **OpenCode-specific treatment:** Extract card family and explicit range; only create exact offer after variant price proven.
- **First-party/documentation evidence:** https://www.macys.com/shop/sale/clearance-closeout?id=54698
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-019 — Nordstrom Rack

**Acquisition family:** `OFFPRICE_CLEARANCE_VARIANT_GRID`. **Evidence status:** `PUBLIC_LISTING_PRICE_RANGE`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.nordstromrack.com/
- **How discovery/traversal actually works or should be investigated:** Clearance section /clearance/shoes has category/facet inventory; paging unknown until actual browser trace.
- **How to read records:** Current Price $X–$Y ranges are common; product style, color, size and stock must bind to exact offer.
- **What disqualifies or qualifies a real comparable purchase price:** Some rows say Add to Bag/Wish List to see price; one-of-a-kind size stock, noncompareable condition.
- **OpenCode-specific treatment:** Saved HTML + variant-resolution path; reject hidden prices and range-as-price.
- **First-party/documentation evidence:** https://www.nordstromrack.com/clearance/shoes
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-020 — REI

**Acquisition family:** `EXPLICIT_PAGE_30_GRID`. **Evidence status:** `VERIFIED_PAGE_COUNT_AND_PRICE_SEMANTICS`. **Access gate:** `BRAND_APPROVAL_NEEDED_FOR_FEED`.

- **Where to begin:** https://www.rei.com/f/scd-deals
- **How discovery/traversal actually works or should be investigated:** Confirmed /f/scd-deals?page=N, “Showing 30 results per page”, current page 2 displayed 31–60 of 9,387 products; subcategories preserve /c/.../f/scd-deals?page=N.
- **How to read records:** Public page displays price or price range, Save percent, “compared to” reference, Outlet badge, Sale Ends and individual product links.
- **What disqualifies or qualifies a real comparable purchase price:** Size/color range must remain unresolved; price “compared to” is REI reference, not historical eBay; Outlet new/used classification explicit.
- **OpenCode-specific treatment:** HTML document-pagination first, optional browser hydration; count visible 30 products/page and stop on final page or repeat; verify product variant.
- **First-party/documentation evidence:** https://www.rei.com/f/scd-deals?page=2
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-021 — DICK'S Sporting Goods

**Acquisition family:** `FILTERABLE_SALE_GRID`. **Evidence status:** `PUBLIC_LISTING_REPO_PUBLISHED`. **Access gate:** `CJ_BRAND_APPROVAL_NEEDED`.

- **Where to begin:** https://www.dickssportinggoods.com/f/sale?selectedSort=0
- **How discovery/traversal actually works or should be investigated:** Sale category /f/sale?selectedSort=0; discover actual page/cursor mechanism from controls and browser network rather than guessing.
- **How to read records:** Card product title, current and previous pricing and pickup/ship status; “See Price in Cart” and min–max range get special unresolved status.
- **What disqualifies or qualifies a real comparable purchase price:** Variant/size/colour, clearance versus regular sales, local stock and cart-only discounts.
- **OpenCode-specific treatment:** Target first-card saved-page parser; build range and cart-price refusal tests.
- **First-party/documentation evidence:** https://www.dickssportinggoods.com/f/sale?selectedSort=0
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-022 — Academy Sports + Outdoors

**Acquisition family:** `NESTED_CLEARANCE_CATEGORY`. **Evidence status:** `PUBLIC_CATEGORY_ENTRY`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.academy.com/c/academy-clearance/clothing-shoes-clearance/shoes-clearance
- **How discovery/traversal actually works or should be investigated:** Clearance is organized as nested /c/academy-clearance/... category paths; crawl category-to-subcategory then bounded pagination (URL shape unknown).
- **How to read records:** Product-card price, old/current tags, style SKU, ship/pickup state and exact size/color.
- **What disqualifies or qualifies a real comparable purchase price:** Store-local pricing, exclusives, condition and footwear size.
- **OpenCode-specific treatment:** Special category graph discovery; avoid treating parent banner and child cards as duplicates.
- **First-party/documentation evidence:** https://www.academy.com/c/academy-clearance/clothing-shoes-clearance/shoes-clearance
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-023 — Bass Pro Shops

**Acquisition family:** `FIRSTRESULT_AND_PAGE_GRID`. **Evidence status:** `VERIFIED_PAGING_URL`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.basspro.com/l/bargain-cave-fishing-sale-and-clearance
- **How discovery/traversal actually works or should be investigated:** Bargain Cave category /l/bargain-cave-fishing-sale-and-clearance; observed firstResult=32&page=2 and firstResult=72&page=3; follow actual next link not fixed arithmetic.
- **How to read records:** Collect title/price/retail compared values, item/UPC, size and quantity from card/product; category-specific units.
- **What disqualifies or qualifies a real comparable purchase price:** In-store and membership-only, bundle, fishing line length and pack, variant options.
- **OpenCode-specific treatment:** Extract visible next link; preserve both firstResult and page exactly, refuse duplicate page loops.
- **First-party/documentation evidence:** https://www.basspro.com/l/bargain-cave-fishing-sale-and-clearance?firstResult=32&page=2
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-024 — Cabela's

**Acquisition family:** `FIRSTRESULT_AND_PAGE_GRID`. **Evidence status:** `VERIFIED_PAGING_URL`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.cabelas.com/l/fishing-boating-hot-deals
- **How discovery/traversal actually works or should be investigated:** Fishing/Boating Hot Deals /l/fishing-boating-hot-deals shows firstResult=36&page=2 and firstResult=72&page=3. Different offsets from Bass Pro mean do not share hard-coded page size.
- **How to read records:** Product/variant and current listed offer price with optional original; item/seller stock per site.
- **What disqualifies or qualifies a real comparable purchase price:** Price/stock are location-specific, quantity/rod configuration, overlap with Bass Pro.
- **OpenCode-specific treatment:** Shared generic cursor-follower code with site-specific link selectors, not one arithmetic template.
- **First-party/documentation evidence:** https://www.cabelas.com/l/fishing-boating-hot-deals?firstResult=36&page=2
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-025 — Tractor Supply

**Acquisition family:** `STORE_CONTEXT_CLEARANCE_CATEGORIES`. **Evidence status:** `PUBLIC_TABBED_DEAL_CARDS_NOW_WAS`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.tractorsupply.com/
- **How discovery/traversal actually works or should be investigated:** Homepage exposes Shop Items On Sale tabbed product list (Top Deals, Outdoor Power Equipment, Pet, Poultry, Livestock, Truck & Automotive, Tools etc); separate Digital Flyer at /tsc/cms/digital-flyer. Precise pagination still requires saved HTML.
- **How to read records:** Public Top Deals renders item-level Now/Was/Save labels (e.g. $299.99 Was $399.99), Add to Cart, and some See Price at Checkout cards; capture store, item ID, model, stock, pack and category.
- **What disqualifies or qualifies a real comparable purchase price:** Store-selected promotions, oversized equipment and freight, farm package quantities.
- **OpenCode-specific treatment:** First extract tabbed Shop Items On Sale cards and linked Digital Flyer promotions; resolve checkout-hidden items and store-scoped status; record any pagination discovered from actual HTML.
- **First-party/documentation evidence:** https://www.tractorsupply.com/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-026 — Harbor Freight

**Acquisition family:** `COUPON_AND_CLUB_CAMPAIGN`. **Evidence status:** `VERIFIED_51_CLEARANCE_ROWS_AND_FULFILLMENT`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.harborfreight.com/collections/inside-track-club-deals.html
- **How discovery/traversal actually works or should be investigated:** Direct public /merchandising-promotions/clearance.html lists 51 clearance items at checked snapshot; each card can be In-Store Only, Online Exclusive, Add to Cart or Choose Options. Separate Inside Track Club campaigns.
- **How to read records:** Sale grid lists individual tool/accessory names, prices and stock/fulfillment flags. Options/Sizes cards may show Starting at rather than an exact variant. Coupon and ITC deal pages are a separate feed of conditional offers.
- **What disqualifies or qualifies a real comparable purchase price:** Club membership and coupon redemption can gate price; private-label items may have few exact eBay comps.
- **OpenCode-specific treatment:** Build direct clearance list adapter first with in-store-only vs online capture, then a separate Inside Track Club coupon/campaign adapter; both need exact HF item number and region.
- **First-party/documentation evidence:** https://www.harborfreight.com/merchandising-promotions/clearance.html
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-027 — Michaels

**Acquisition family:** `CLEARANCE_PLUS_MARKETPLACE_VARIANTS`. **Evidence status:** `OFFICIAL_VARIANT_RULES`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.michaels.com/clearance
- **How discovery/traversal actually works or should be investigated:** Clearance /clearance groups categories and product cards; also MakerPlace third-party seller products, which need separate seller/offer identities.
- **How to read records:** Original versus marked price and exact craft size/color/pack; makerplace rules explicitly describe variant-specific sale price only after selection.
- **What disqualifies or qualifies a real comparable purchase price:** Michaels store versus MakerPlace seller, percent-off coupon conditions and reward credits.
- **OpenCode-specific treatment:** Split native retailer vs MakerPlace offers; resolve variant and seller before comparison.
- **First-party/documentation evidence:** https://www.michaels.com/makerplace/seller-support-center/marketing/set-up-a-sale
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-028 — Barnes & Noble

**Acquisition family:** `EDITORIAL_COUPON_TO_FORMAT_SPECIFIC_PRODUCTS`. **Evidence status:** `PUBLIC_OFFICIAL_PROMO_PAGE`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.barnesandnoble.com/shop/clearance
- **How discovery/traversal actually works or should be investigated:** Coupons/deals landing /pages/coupons-deals groups category promotions; explore a separate clearance/campaign listing if present; pagination unknown.
- **How to read records:** ISBN-13, hardcover/paperback/vinyl format, signed edition, cover variant, price/promo and membership rules.
- **What disqualifies or qualifies a real comparable purchase price:** A title alone is never enough: ISBN and media format mandatory.
- **OpenCode-specific treatment:** Treat editorial campaign as discovery, then extract ISBN-formatted item offers with eBay exact-edition match.
- **First-party/documentation evidence:** https://www.barnesandnoble.com/pages/coupons-deals
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-029 — LEGO Store

**Acquisition family:** `PAGE_NUMBERED_SET_CATALOG`. **Evidence status:** `VERIFIED_PAGE_NUMBER_URL`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.lego.com/en-us/categories/sales-and-deals
- **How discovery/traversal actually works or should be investigated:** Sale /en-us/categories/sales-and-deals?page=N; indexed page 2 confirmed. Inspect real next/last page and avoid unrelated promotional pages with huge page counts.
- **How to read records:** Set number (four/five digits), set/edition, current/regular price, availability; separate GWP from price discount.
- **What disqualifies or qualifies a real comparable purchase price:** Insiders point multipliers and gifts-with-purchase do not decrease purchase price.
- **OpenCode-specific treatment:** Exact LEGO set number as model key; only physical sets with verified offer.
- **First-party/documentation evidence:** https://www.lego.com/en-us/categories/sales-and-deals?page=2
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-030 — Disney Store

**Acquisition family:** `BRANDED_SALE_GRID`. **Evidence status:** `PUBLIC_SALE_PAGE`. **Access gate:** `CJ_BRAND_APPROVAL_NEEDED`.

- **Where to begin:** https://www.disneystore.com/
- **How discovery/traversal actually works or should be investigated:** Official /sale/ page displays sale category and filters; page/cursor evidence not yet identified.
- **How to read records:** Disney Store merchandise ID and licensed character/collection, edition, size/color/pack and actual item price.
- **What disqualifies or qualifies a real comparable purchase price:** Collectible edition differences and conditional promotional offers.
- **OpenCode-specific treatment:** Source-linked page parser after snapshot; prioritize uniquely SKU-coded toys over clothing.
- **First-party/documentation evidence:** https://www.disneystore.com/sale/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-031 — Walgreens

**Acquisition family:** `WEEKLY_AD_AND_COUPON_CATALOG`. **Evidence status:** `OFFICIAL_CLIPPED_COUPONS_PROGRAM`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.walgreens.com/shop
- **How discovery/traversal actually works or should be investigated:** Official Weekly Ad / shop sale route; coupons are clipped to myWalgreens/card and applied at checkout. Extract weekly flyer item links as one acquisition source, and category sale listings as another, with store context.
- **How to read records:** Price before coupon vs account-targeted savings, coupons clip state and pack quantity.
- **What disqualifies or qualifies a real comparable purchase price:** Cash rewards not immediate price reduction; drug/regulated products out of scope.
- **OpenCode-specific treatment:** Opt into physical general merchandise only; require observed purchasable price and loyalty entitlement.
- **First-party/documentation evidence:** https://www.walgreens.com/topic/help/shophelp/coupons_help.jsp
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-032 — CVS

**Acquisition family:** `EXTRACARE_PROMO_AND_WEEKLY_AD`. **Evidence status:** `OFFICIAL_MEMBERSHIP_RULES`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.cvs.com/shop/weekly-ad
- **How discovery/traversal actually works or should be investigated:** Extra Big Deals and online weekly ad are distinct deal surface; discover linked item pages not flyer images only.
- **How to read records:** SKU, member price when ExtraCare linked, regular price, promotion conditions and exact pack/size.
- **What disqualifies or qualifies a real comparable purchase price:** ExtraBucks are deferred rewards; ExtraCare card can be required for sale price.
- **OpenCode-specific treatment:** Offer value has entitlement qualifiers and cashback distinct from current price.
- **First-party/documentation evidence:** https://www.cvs.com/extracare/overview
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-033 — Chewy

**Acquisition family:** `DUAL_PRICE_AUTOSHIP_AND_STANDARD`. **Evidence status:** `PUBLIC_DUAL_PRICE_LABELS`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.chewy.com/deals/todays-deals-2723
- **How discovery/traversal actually works or should be investigated:** Today’s Deals /deals/todays-deals-2723; category and promo navigation; paging unknown.
- **How to read records:** “Chewy Price” and “Autoship Price” must be separately labeled, with product size/pack and recurring subscription condition.
- **What disqualifies or qualifies a real comparable purchase price:** First-order Autoship discount cannot be treated as a generally available single-purchase price; gifts and account credits separate.
- **OpenCode-specific treatment:** Primary regular single-purchase price channel; optional subscription-only offer with eligibility recorded.
- **First-party/documentation evidence:** https://www.chewy.com/deals/todays-deals-2723
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-034 — Petco

**Acquisition family:** `PAGE_48_AND_SORT_GRID`. **Evidence status:** `VERIFIED_48_PAGINATION_SORT`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.petco.com/category/top-deals/clearance
- **How discovery/traversal actually works or should be investigated:** Clearance /category/top-deals/clearance shows 1–48 of 527 results; page=2 works; supported sortby=offerprice&sortorder=ascending in URL.
- **How to read records:** Cards visibly state e.g. $75.00 was $149.99; some require choices (“More Choices Available”), pickup/same-day state.
- **What disqualifies or qualifies a real comparable purchase price:** Regional pickup-only, package quantity, conditional rewards and product option range.
- **OpenCode-specific treatment:** Exact product+variant checker, enumerate observed page links until results exhausted; separate online shippable from store pickup.
- **First-party/documentation evidence:** https://www.petco.com/category/top-deals/clearance?page=2&sortby=offerprice&sortorder=ascending
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-035 — PetSmart

**Acquisition family:** `CLEARANCE_GRID_PLUS_STRIKETHROUGH_DEFINITION`. **Evidence status:** `OFFICIAL_REFERENCE_PRICE_DEFINITION`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.petsmart.com/
- **How discovery/traversal actually works or should be investigated:** Official /sale/clearance/ category page. Discover pagination controls from snapshot and product list, rather than assuming.
- **How to read records:** Current price plus strike-through reference, SKU/size/pack; promotional terms specify crossed-out reference may be MSRP, median paid or non-member retail.
- **What disqualifies or qualifies a real comparable purchase price:** Treat strikethrough as retailer reference with unknown basis; loyalty and store pickup prices distinct.
- **OpenCode-specific treatment:** Do not use crossed-out value as evidence of real previously obtainable price or eBay reference.
- **First-party/documentation evidence:** https://www.petsmart.com/help/promotional-terms
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-036 — Wayfair

**Acquisition family:** `FLASH_SALE_FACETED_FURNITURE_GRID`. **Evidence status:** `VERIFIED_CLOSEOUT_WAS_PRICE`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.wayfair.com/daily-sales/clearance
- **How discovery/traversal actually works or should be investigated:** Public /daily-sales/clearance and /daily-sales/closeout show finite promotional lists, explicit was/current prices and countdown-style clearance offers. Document hidden continuation or filter state from browser capture.
- **How to read records:** Brand/manufacturer model if available, SKU, dimensions/color/finish, current price by configuration, delivery cost.
- **What disqualifies or qualifies a real comparable purchase price:** Retailer renaming of identical generic OEM models, bulky shipping and product option ranges may preclude exact match. Some page prices are per item in multipacks; preserve quantity.
- **OpenCode-specific treatment:** Capture first; strict identity gating, no family-level eBay comparison.
- **First-party/documentation evidence:** https://www.wayfair.com/daily-sales/closeout
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-037 — Adorama

**Acquisition family:** `PROMO_LISTING_WITH_RIGHTS_CONFLICT`. **Evidence status:** `F2_PRIMARY_TERMS_CONFLICT`. **Access gate:** `PUBLISHED_AFFILIATE_CONFLICT`.

- **Where to begin:** https://www.adorama.com/g/adorama-affiliate-program
- **How discovery/traversal actually works or should be investigated:** Retail sale/Deal page category inventory can be inspected as snapshot; separate published affiliate product-feed promise.
- **How to read records:** Manufacturer model vs Adorama bundle SKU, current/regular price, rebates and kit inclusions.
- **What disqualifies or qualifies a real comparable purchase price:** Adorama affiliate agreement reviewed in F2 restricts price publication and caching under cited terms; version conflict with Impact/Partnerize program copy.
- **OpenCode-specific treatment:** No production ingest under conflicting terms until current binding authorization for price display/cache obtained.
- **First-party/documentation evidence:** https://www.adorama.com/api/getContent?contentName=Affiliate_Agreement&output=desktop
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-038 — Monoprice

**Acquisition family:** `CLEARANCE_PRODUCT_LIST_CURRENT_PRICE`. **Evidence status:** `PUBLIC_PRODUCTS_AND_CURRENT_PRICES`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.monoprice.com/pages/products_clearance
- **How discovery/traversal actually works or should be investigated:** Clearance /pages/products_clearance lists individual products and subcategory clearances, e.g. /pages/clearance_cs; pagination/load-more unknown.
- **How to read records:** Text-visible product title, link and current price; regular price may be absent. Exact Monoprice product ID from URL/product page if recorded.
- **What disqualifies or qualifies a real comparable purchase price:** Current-only retailer source remains eligible for eBay comparison; do not synthesize “was” price.
- **OpenCode-specific treatment:** Enable `include_current_only`, verify manufacturer SKU/pack, stop if no eBay exact match.
- **First-party/documentation evidence:** https://www.monoprice.com/pages/products_clearance
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-039 — Samsung US

**Acquisition family:** `TRADEIN_HEAVY_CAMPAIGN`. **Evidence status:** `PUBLIC_TRADEIN_OFFER_TERMS`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.samsung.com/us/offer/
- **How discovery/traversal actually works or should be investigated:** Featured offers /us/shop/featured-offers/ groups device/promo tiles; actual item listings through product URL, not banner copy.
- **How to read records:** Exact Samsung model code, capacity/carrier/unlocked, outright list/purchase price versus trade-in net price, program eligibility.
- **What disqualifies or qualifies a real comparable purchase price:** “Up to” trade-in credit or Samsung credit is not unconditional purchase-price markdown.
- **OpenCode-specific treatment:** Extract only outright price; explicit trade-in and finance branches with none as base comparator.
- **First-party/documentation evidence:** https://www.samsung.com/us/shop/featured-offers/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-040 — Dell Outlet

**Acquisition family:** `UNIQUE_OUTLET_CONFIGURATION`. **Evidence status:** `PUBLIC_OUTLET_PAGE`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.dell.com/en-us/shop/lp/outlet
- **How discovery/traversal actually works or should be investigated:** Separate Outlet/Refurb landing /en-us/shop/lp/outlet; inspect list pagination/configure flows with explicit current stock per unique machine.
- **How to read records:** Service/configuration ID, processor/RAM/SSD/OS, refurb grade and warranty; sample may be unique stock.
- **What disqualifies or qualifies a real comparable purchase price:** An Outlet machine is not a new Dell retail SKU; exact-condition sold comp often sparse.
- **OpenCode-specific treatment:** Keep separate source from Dell new deals; strong condition and configuration gate.
- **First-party/documentation evidence:** https://www.dell.com/en-us/shop/lp/outlet
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-041 — Lenovo US

**Acquisition family:** `CONFIGURED_PARTNUMBER_DEAL_GRID`. **Evidence status:** `PUBLIC_DEAL_CATEGORY`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.lenovo.com/us/en/d/deals/laptops/
- **How discovery/traversal actually works or should be investigated:** Deals category /us/en/d/deals/laptops/ is part of Lenovo deal taxonomy; determine continuation from filters and product grids.
- **How to read records:** Machine Type Model (MTM)/part number, fixed versus customized specs, coupon codes and ship date.
- **What disqualifies or qualifies a real comparable purchase price:** Family name not exact configured item; student/account discounts conditional.
- **OpenCode-specific treatment:** Extract manufacturer part and immutable configuration; query eBay by part not ThinkPad family.
- **First-party/documentation evidence:** https://www.lenovo.com/us/en/d/deals/laptops/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-042 — HP US

**Acquisition family:** `WEEKLY_CONFIGURABLE_PRODUCTS`. **Evidence status:** `PUBLIC_CONFIG_TEXT`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.hp.com/us-en/shop/slp/weekly-deals
- **How discovery/traversal actually works or should be investigated:** Weekly deals /us-en/shop/slp/weekly-deals shows category tabs and product cards including explicit laptop configuration titles; inspect all tabs and paging.
- **How to read records:** Full HP product SKU, CPU/RAM/SSD/screen/warranty, now/regular and add-to-cart status; fixed SKU versus customizable builder.
- **What disqualifies or qualifies a real comparable purchase price:** Customized base price changes with options; Instant Savings not identical to rebate.
- **OpenCode-specific treatment:** Treat preconfigured SKU as atomic; quote configurations only if fully frozen.
- **First-party/documentation evidence:** https://www.hp.com/us-en/shop/slp/weekly-deals
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-043 — Nintendo Store

**Acquisition family:** `DIGITAL_HEAVY_SALE_CATALOG`. **Evidence status:** `PUBLIC_STORE_SALE`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.nintendo.com/us/store/sales-and-deals/
- **How discovery/traversal actually works or should be investigated:** Nintendo sales/deals page /us/store/sales-and-deals/ lists digital game markdowns; explicit category filter required for physical products.
- **How to read records:** Platform generation, edition, downloadable vs physical cartridge, region, regular/current price.
- **What disqualifies or qualifies a real comparable purchase price:** Digital licence cannot be compared with physical used cartridge eBay sales; bundle/edition matters.
- **OpenCode-specific treatment:** Default exclude digital, software licence and gift cards; physical-only collector if present.
- **First-party/documentation evidence:** https://www.nintendo.com/us/store/sales-and-deals/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-044 — AliExpress

**Acquisition family:** `CROSS_BORDER_VARIATION_MARKETPLACE`. **Evidence status:** `PRIOR_REPO_MARKETPLACE_CANDIDATE`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.aliexpress.com/
- **How discovery/traversal actually works or should be investigated:** Seller product catalog and promotional flash sales; official sanctioned affiliate data path rather than generalized website auto-navigation.
- **How to read records:** Seller, product offer ID, selected variant/spec, shipping to destination, VAT/tax, quantity, delivery date.
- **What disqualifies or qualifies a real comparable purchase price:** Base tile price often cheapest option; shipping or variation changes paid amount; long delivery and import duties.
- **OpenCode-specific treatment:** Dedicated import offer contract with total delivered cost and seller identity, not Best Buy object assumptions.
- **First-party/documentation evidence:** https://www.aliexpress.com/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-045 — Alibaba

**Acquisition family:** `B2B_TIERED_QUOTATION`. **Evidence status:** `PRIOR_REPO_B2B_CANDIDATE`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.alibaba.com/
- **How discovery/traversal actually works or should be investigated:** Supplier catalog and RFQ; product tiles often show per-piece price range at MOQ, not single consumer transaction.
- **How to read records:** Factory/supplier, specification, quantity break, MOQ, shipping term, freight, import/tariff duties and lead time.
- **What disqualifies or qualifies a real comparable purchase price:** Cannot compare 100-unit FOB quote to one delivered eBay unit; no amount due until quote qualified.
- **OpenCode-specific treatment:** Separate import workflow; exclude from direct retail gap ranking unless delivered one-unit comparable contract exists.
- **First-party/documentation evidence:** https://www.alibaba.com/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-046 — Woot

**Acquisition family:** `OFFICIAL_CATEGORY_FEED_AND_BATCH_DETAILS`. **Evidence status:** `OFFICIAL_API_AND_EXISTING_ADAPTER`. **Access gate:** `API_USE_RIGHTS_REVIEW`.

- **Where to begin:** https://developer.woot.com/
- **How discovery/traversal actually works or should be investigated:** Existing keyed GET /feed/{feedname}, categories All/Clearance/Computers/Electronics/Tools; POST /getoffers expands offer details in batches (local adapter batches 25).
- **How to read records:** OfferId, SalePrice/ListPrice, IsSoldOut, Condition, variant details and actual offer URL; preserve collection family/variant structure.
- **What disqualifies or qualifies a real comparable purchase price:** Min/Max price ranges and multiple conditions must remain separate purchasable variants; merchant/stock/shipping conditions.
- **OpenCode-specific treatment:** Retain operating direct adapter, improve variant atomicity rather than browser scrape.
- **First-party/documentation evidence:** https://developer.woot.com/
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-047 — Meh

**Acquisition family:** `SINGLE_DAILY_DEAL_FEED`. **Evidence status:** `OFFICIAL_FEED_AND_EXISTING_ADAPTER`. **Access gate:** `USE_RIGHTS_REVIEW`.

- **Where to begin:** https://meh.com/feed.json
- **How discovery/traversal actually works or should be investigated:** Existing keyed /api/1/current.json plus documented public https://meh.com/feed.json and RSS; one daily headline deal, not a merchant-wide paginated sale catalog.
- **How to read records:** Deal/items, variants, price, MSRP, soldOutAt, item ID, item-specific product link.
- **What disqualifies or qualifies a real comparable purchase price:** Bundles and variant prices may differ; one deal/day throughput ceiling.
- **OpenCode-specific treatment:** Keep existing API, public feed fallback only if usage terms allow.
- **First-party/documentation evidence:** https://meh.com/support
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-048 — Kroger

**Acquisition family:** `LOCATION_SCOPED_OAUTH_PRODUCT_SEARCH`. **Evidence status:** `OFFICIAL_API_AND_EXISTING_ADAPTER`. **Access gate:** `API_USE_RIGHTS_REVIEW`.

- **Where to begin:** https://api.kroger.com/v1/products
- **How discovery/traversal actually works or should be investigated:** Existing client-credential OAuth, choose store by location ZIP, query GET /v1/products with filter.term, filter.locationId, filter.limit. No documented enumerate-all-sale filter.
- **How to read records:** Product UPC/productId, item regular and promo, productPageURI, category and store ID.
- **What disqualifies or qualifies a real comparable purchase price:** Price promotion is for selected location, no global deal coverage, nonfood inventory sparse.
- **OpenCode-specific treatment:** Keep API; expand search terms/category strategy only as discovery hypothesis, not exhaustive census.
- **First-party/documentation evidence:** https://www.postman.com/kroger/the-kroger-co-s-public-workspace/documentation/ki6utqb/kroger-public-apis
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-049 — Backcountry

**Acquisition family:** `DEEP_PAGE_NUMBER_CLEARANCE_GRID`. **Evidence status:** `VERIFIED_DEEP_PAGING_AND_TOTAL`. **Access gate:** `PARTNER_APPROVAL_NEEDED_FOR_FEED`.

- **Where to begin:** https://www.backcountry.com/rc/clearance
- **How discovery/traversal actually works or should be investigated:** Confirmed /rc/clearance?page=N; indexed page 95 exists and page 5 reports 4,061 results. Category facets and price/discount facet links. This is a deep paginated enumerable clearance surface.
- **How to read records:** Products show color counts; resolve the actual size/color current offer, not cheapest among family and not wrong model year.
- **What disqualifies or qualifies a real comparable purchase price:** Category broad, lot of apparel variants; Outlet/clearance need stock and individual option.
- **OpenCode-specific treatment:** Bounded page-to-page adapter plus robust variant/identity extraction; source official partner feed available upon approval.
- **First-party/documentation evidence:** https://www.backcountry.com/rc/clearance?page=5
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-050 — Acme Tools

**Acquisition family:** `OFFSET_SIZE_SKU_PRICE_PAIR`. **Evidence status:** `VERIFIED_FIELD_AND_PAGINATION`. **Access gate:** `ACTIVE_FEED_UNVERIFIED`.

- **Where to begin:** https://www.acmetools.com/price-drop/
- **How discovery/traversal actually works or should be investigated:** Price Drop /price-drop/?start=24&sz=24 (and /new/price-drop/). Indexed first and offset pages show SKU#, in-stock/available-to-order, shipping class, current, Was and Save percent.
- **How to read records:** Each listing includes real MPN/SKU in text; e.g. bare tool vs combo kit and refurbished/reconditioned are explicitly labeled.
- **What disqualifies or qualifies a real comparable purchase price:** Freight shipping vs ground, reconditioned item condition, free battery with purchase and “available to order” not necessarily stock.
- **OpenCode-specific treatment:** Use published `start`/`sz` params, literal SKU, and annotated current/was/stock; one of the most tractable purpose-specific adapters.
- **First-party/documentation evidence:** https://www.acmetools.com/price-drop/?start=24&sz=24
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-051 — Advance Auto Parts

**Acquisition family:** `LOCATION_VEHICLE_FITMENT_AND_IMPACT_CATALOG`. **Evidence status:** `PUBLIC_PROMO_PAGE_PLUS_OFFICIAL_FEED`. **Access gate:** `PARTNER_APPROVAL_NEEDED_FOR_FEED`.

- **Where to begin:** https://shop.advanceautoparts.com/
- **How discovery/traversal actually works or should be investigated:** Official /o/advance-auto-parts-coupons-and-deals is a real promotion landing with links advertising up to 80% clearance; Impact product catalog is a separate official partner channel. Follow the promo category links and resolve local store/vehicle fitment.
- **How to read records:** Manufacturer part + brand, OEM cross-ref, exact fitment, checkout store, core charge and shipping.
- **What disqualifies or qualifies a real comparable purchase price:** SKU might be compatible rather than physically identical; core charges and store-specific promotions.
- **OpenCode-specific treatment:** Investigate real clearance page from the promotion landing and implement a partner-feed importer in parallel; retain OEM/MPN and fitment/core-charge gates. Official purchase terms say ordinary promotional codes may exclude sale/clearance items.
- **First-party/documentation evidence:** https://shop.advanceautoparts.com/o/advance-auto-parts-coupons-and-deals
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-052 — Fanatics

**Acquisition family:** `IMPACT_LICENSED_MERCH_CATALOG`. **Evidence status:** `OFFICIAL_FEED_DOC`. **Access gate:** `PARTNER_APPROVAL_NEEDED_FOR_FEED`.

- **Where to begin:** https://www.fanatics.com/affiliates/x-51
- **How discovery/traversal actually works or should be investigated:** Official /affiliates/x-51 announces Impact product feeds; storefront sale page routing remains to be inspected from actual listing.
- **How to read records:** Licensed team/player/edition/style, color, size, personalization, merch ID and current/regular amount.
- **What disqualifies or qualifies a real comparable purchase price:** Custom/personalized and sizes not fungible; seasonal inventory and franchise rights.
- **OpenCode-specific treatment:** Prefer feed for sale enumeration; unique product/edition/color/size row once data available.
- **First-party/documentation evidence:** https://www.fanatics.com/affiliates/x-51
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-053 — PUMA US

**Acquisition family:** `SALE_AND_FINAL_SALE_VARIANT_GRID`. **Evidence status:** `PUBLIC_SALE_PAGE_AND_PROMO_TERMS`. **Access gate:** `CJ_BRAND_APPROVAL_NEEDED`.

- **Where to begin:** https://us.puma.com/us/en/sale/all-sale
- **How discovery/traversal actually works or should be investigated:** Shop All Sale /us/en/sale/all-sale and /sale/final-sale; promotion category pages contain variant color thumbnails and price display.
- **How to read records:** PUMA style code, size, color, retail/regular price and final-sale indicator; identify SKU revision.
- **What disqualifies or qualifies a real comparable purchase price:** General sale codes may explicitly exclude clearance; promo availability cannot be applied to all items.
- **OpenCode-specific treatment:** Single family card, defer actual matching until specific size/color SKU resolved; approved CJ daily feed backup.
- **First-party/documentation evidence:** https://us.puma.com/us/en/sale/all-sale
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

### RET-054 — Dell new-product deals

**Acquisition family:** `EMBEDDED_STRUCTURED_OFFER_OBJECT`. **Evidence status:** `VERIFIED_EMBEDDED_OFFER_FIELDS`. **Access gate:** `TERMS_REVIEW_NEEDED`.

- **Where to begin:** https://www.dell.com/en-us/shop/deals/dc
- **How discovery/traversal actually works or should be investigated:** Top Deals /en-us/shop/deals/dc with laptop/desktop category slugs. Public search results expose embedded JSON objects with offerid, productData.shopUrl, marketPrice, dellPrice, metrics.productid, stockstatus, position.
- **How to read records:** Parse actual captured embedded offer JSON if present; preserve offerid+configuration ID, stockstatus, dellPrice, marketPrice, canonical shopUrl. Check configurable variants against cart item selection.
- **What disqualifies or qualifies a real comparable purchase price:** marketPrice is reference/marketing price, not historical paid price; configurable base SKU not always final configuration; price changes can occur across observations.
- **OpenCode-specific treatment:** Build structured-data-first Dell deals adapter; no brittle first-dollar heuristic. Prefer parsed scripts over visible banners.
- **First-party/documentation evidence:** https://www.dell.com/en-us/shop/deals/dc
- **Capture-dependent unknown:** Exact current production HTML card selector, in-page JSON paths and any background request/cursor are **unverified** unless the family cites a documented API/Best Buy existing source. Instrument actual page before creating selectors or private endpoint calls.

## 4. OpenCode adapter architecture — methods, not one-size-fits-all selectors

### 4.1 Discovery/source types
1. **Document-pagination sources:** Follow real `rel=next`, pagination anchors or visibly sourced query parameters. Verified examples: REI `?page=N`; Backcountry `?page=N`; LEGO `?page=N`; Petco `?page=N`; Acme `?start=N&sz=24`; Bass Pro/Cabela’s `?firstResult=N&page=M`. Query values shown above are public examples, **not a guarantee the endpoint will remain static**.
2. **Hydrated/product-grid sources:** Render page in normal Chrome when authorized, wait for product count/price coverage to stabilize, detect lazy-loaded cards, and capture HTML. Use explicit per-store readiness and coverage tests, not Best Buy price selectors everywhere.
3. **Structured-data sources:** Prefer public embedded JSON/JSON-LD when it identifies an exact product offer, e.g. Dell `offerid/productData` objects. Confirm byte-level source fixture and JSON paths before adapter implementation. Audit raw display price against structured fields.
4. **Campaign/weekly ad sources:** Traverse from promotional tiles to real item listings; no generalized %‑off marketing text becomes a product record. Examples: Kohl’s, CVS, Walgreens, Costco, Samsung.
5. **Store-/account-conditional sources:** Preserve selected location, membership and entitled price or emit `PRICE_UNAVAILABLE`. Examples: Micro Center, Sam’s, Costco, Kroger, BJ’s, Office Depot, Tractor Supply, Target.
6. **Approved bulk feed / public API sources:** Import merchant rows from Impact, CJ, Awin, Woot, Meh, Kroger, Best Buy API, eligible Amazon/Keepa and consented WooCommerce. Merchant approval, field shape, comparison/display/storage rights and freshness are independent of technical documentation.
7. **Marketplaces/import quotations:** Separate seller-specific offers from aggregate product titles; preserve variation, shipping, MOQ and quantity. Do not map Alibaba tier quotes into a one-unit current-price field.

### 4.2 Capture protocol for every merchant
For the authorized first sample: record a canonical URL, local date/time/timezone, locale/currency, selected ZIP/store, membership/session status (without credentials), robots/terms assessment, screenshot when useful, raw initial page HTML, **fully settled rendered HTML**, scroll-end product count, visible title/price text, `Next`/page-link hrefs and a second page, product-level detail for 3 difficult examples, and—only if allowed—a sanitized network HAR with response URL, method, content-type, status, pagination parameter and a short schema illustration. Never store authentication headers, cookies, API keys, or customer data in the repo.

**How to discover a site’s real data transport:** Compare initial HTML vs rendered HTML card counts; inspect `<script type="application/ld+json">`; inspect `<script>` tags for serialized product/offer records; inspect `fetch`/XHR response names only in a permitted ordinary browser session and verify whether a documented/authorized endpoint exists; inspect visible `Next` links and URL changes on user navigation; if all fail, write an offline HTML adapter using user-provided page snapshots. Never guess a private API endpoint or defeat anti-bot controls.

### 4.3 Explicit intermediate data contracts
Each discovered `retailer_offer` must carry: `source_id`, `merchant_id`, `merchant_name`, `seller_of_record`, `source_url`, `canonical_product_url`, `capture_timestamp_utc`, `currency`, `region/ZIP/store`, `availability_status`, `shipping_scope/cost`, `membership/eligibility`, `coupon/rebate/gift/credit rules`, `variant_group_id`, `variant_id`, `brand`, `gtin/upc/ean`, `mpn/model`, `merchant_sku`, `condition`, `quantity/pack_size`, `list_price`, `current_price`, `current_price_type` (exact/range/minimum/in-cart/with-trade-in/subscription/member/etc), `price_evidence_excerpt_and_locator`, `raw_evidence_sha256`, `parse_version`, `catalog_category`, `discovery_cursor`, `source_permission_gate`, `warnings`, `rejection_reason`.

**Rule:** `current_price_type=range|min_only|in_cart|trade_in_conditional|unresolved_variant|unknown` cannot generate a concrete purchase-gap observation until exact price/variant/eligibility is established. Display it as a discoverable product-family candidate, not a verified offer. `regular_price` is retailer-provided reference data, *never* eBay historical regular price. Source-provided MSRP is not an actual past transaction.

### 4.4 Traversal completeness court
For each listing source and page: `source_page`, `source_type`, `loaded_count`, `distinct_cards`, `cards_with_current_price`, `cards_with_old_price`, `cards_with_exact_identifier`, `cards_with_variant_range`, `cards_with_stock`, `extracted_count`, `rejected_count_by_reason`, `linked_pages_discovered`, `last_cursor`, `pages_visited`, `visited_hashes`, `next_link_evidence`, `not_fetched_reason`, `stop_reason`. Stop on repeated content/cursor, explicit final page or authorized bounds; never call a 12-page sample an exhaustive 300-page catalog.

### 4.5 Source-selection and preserving eBay
In the Control Room, new sources should be discoverable independent producers. In Deals, source filters, category, date, price, saved-only and selected Top-N should work for all sources. In Results, **the existing human-browser-open → HTML-save → watcher** flow remains; per-source product identifiers and exact variants are passed to that flow. CompsAPI may be a separate optional audit channel for Best Offer actual amount claims, not a prerequisite for retailer expansion.

## 5. Concrete external producer adapters (outside HTML)

| Provider / system | Official access path and real data shape | OpenCode action | Rights/quality gate |
|---|---|---|---|
| **Woot** | [Developer guide](https://developer.woot.com/) `GET /feed/{feedname}`, `POST /getoffers`; categories and offer variants | Keep/extend existing API adapter, test Offer ID/condition/price range | Developer key, purpose/storage terms |
| **Meh** | [Support/feed](https://meh.com/support), public `feed.json`/RSS and keyed daily-deal API | Preserve one-deal/day adapter | Product, bundle, public-feed reuse |
| **Kroger** | [Products API](https://www.postman.com/kroger/the-kroger-co-s-public-workspace/documentation/ki6utqb/kroger-public-apis), OAuth and location-specific `filter.term/filter.locationId` | Keep store-specific adapter; no universal on-sale feed claimed | Region/stock, rights, non-food availability |
| **Impact** | [Partner catalog downloads](https://help.impact.com/partner/what-would-you-like-to-learn-about/platform-features/marketing-content/product-marketplace-and-catalogs/download-product-catalogs-as-a-partner), platform/FTP/API after brand acceptance | Common CSV/feed importer, incremental dates, advertiser-specific contract fields | Need explicit participating brand relationship and comparison/display/storage right |
| **CJ** | [ProductFeed GraphQL](https://docs.cj.com/docs/productfeed-api-search) publisher feed summaries and details with pagination | GraphQL importer + normalized variant rows | Account + advertiser permission |
| **Awin** | [Publisher feed guide](https://help.awin.com/developers/docs/product-feed-publisher-guide-intro) feed list/updated timestamps | Approved merchant download/reconciliation | Publisher/advertiser approval and output rights |
| **WooCommerce** | [Store Products API](https://developer.woocommerce.com/docs/apis/store-api/resources-endpoints/products/) `?on_sale=true&page=N&per_page=100` when site permits | Reusable consented merchant adapter; note default variation exclusion | Do not scan unknown independent stores without applicable authorization; variation lookup essential |
| **Keepa / Amazon** | [Deals endpoint](https://keepa.com/api-docs/deals.html), token-metered ASIN discovery | Separate Amazon seller/offer verification channel | Tokens, seller of record and offer licences |
| **Best Buy Products API** | [Official API](https://developer.bestbuy.com/apis) | Explore official sale/stock producer parallel to browser | Purpose/retention/third-party comparison terms |
| **CompsAPI** | [Vendor](https://compsapi.com/) eBay sold/completed sales only | Optional eBay accepted-Best-Offer audit, **not retailer discoverer** | Claimed paid price unverified against independent eBay Product Research; upstream rights unresolved |

**Specialty named feeds already investigated in repo:** REI, Backcountry, DICK’S, Acme Tools, Advance Auto Parts, Fanatics, Disney Store, PUMA; Home Depot official daily Impact feed. F2’s documented Adorama terms conflict makes it a HOLD; eBay first consumer and retailer expansion are separate workstreams. All written applications/permission requests remain user-approved, not autonomous.

## 6. Acceptance and negative tests for OpenCode

**Unit/fixture:** Each source must include at least two independently saved pages where pagination exists and three difficult products (exact price, price range, gated/coupon or ambiguous). Expected product count, URLs, exact current/regular price, SKU, price type, offer state and rejection diagnostics are asserted. Parse a price range without selecting a variant → `PRICE_UNRESOLVED`; trade-in price not applied to outright purchase; “Was” reference bound to same card; no mixing unrelated card prices.

**Technical live canary only when authorized:** Two consecutive real pages for each selected merchant, compare 10 sampled extracted card records to browser-visible items; measure 100% direct source-link validity and semantic price role, `n_missing` instead of inventing; show new source in Deals and route a saved product into existing Results/eBay flow. Store new code on isolated branch based on latest HEAD, preserve source-fixture provenance; run tests and source/rights review; no merge claimed by implementer alone.

**Cross-store tests:** duplicate products across retailer sources retain distinct offer/seller/region; identical brand but different variant not collapsed; family product card cannot be used as exact eBay match; no arbitrary SKU match based only on product title; page 2 not mistaken for page 1 because card contents repeated; total advertised results and collected pages mismatch marked incomplete; permission fail stops network but allows local fixture parsing; source refresh errors preserve prior dated evidence without presenting it as current.

**Output requirement:** For every merchant produce `SOURCE_RECEIPT.json`, `PAGING_RECEIPT.json`, `PRICE_EXTRACTION_RECEIPT.json`, `RIGHTS_RECEIPT.json` (documentary state), 3+ provenance-safe fixtures where available, `retailer/products.json` and a candid `GO/HOLD/NO-PROOF` verdict. Source-free parser PASS does not imply live authorized data integration.

## 7. Handoff instructions — exact next operation

1. Fetch and verify the current `work/arbiscout-local-build` branch HEAD; treat `65529f5...` as research anchor, not guaranteed present future HEAD. Do not restart architecture or replace current eBay Results.
2. Import `MECHANISM_SPECIFICATIONS.json` as source profiles. Map each source to one or more adapter families in §4, not to one generic CSS reader. Preserve original code and tests; create common interface then individual modules.
3. Acquire first authorized/local saved product listing and—when pagination exists—the actual page 2. Inspect DOM, JSON-LD, embedded state and permitted network traces to replace `NOT_OBSERVED_IN_CURRENT_HTML` with proven element pointers. Never claim evidence before capture.
4. Implement verification parser, explicit price role/variant identities, page loop and receipts. Feed normalized products into the **existing** catalog/Deals; route saved selection into **existing** eBay capture and Results.
5. Keep source-rights, usage, account credentials, quotas and future prod runs separately gated. Record negative and empty outcomes.
6. Compare source yield by *valid new exact purchasable offers*, not gross number of found cards; reconcile before moving to next source.

The objective is **implementation of differentiated source acquisition for every viable merchant**, without giving up on technically challenging sites merely because their HTML differs. An unresolved mechanism becomes a concrete browser-inspection task, never a guessed `fetch` endpoint.

## 8. Primary evidence/index URLs for audit

- **REI page 2 has 30 rows and 9,387 total:** https://www.rei.com/f/scd-deals?page=2 · `PUBLIC_HTML_TEXT` · 2026-11-17; supports Pagination and exact price/compared-to/range.
- **Backcountry clearance 4,061 results and page=5:** https://www.backcountry.com/rc/clearance?page=5 · `PUBLIC_HTML_TEXT` · 2026-11-17; supports Deep pages, category facets and color counts.
- **Acme Tools offset 24 size 24:** https://www.acmetools.com/price-drop/?start=24&sz=24 · `PUBLIC_HTML_TEXT` · 2026-11-17; supports SKU#, current, Was, stock, shipping, clearance status.
- **Bass Pro firstResult and page:** https://www.basspro.com/l/bargain-cave-fishing-sale-and-clearance?firstResult=32&page=2 · `INDEXED_REAL_URL` · 2026-11-17; supports Query shape, do not infer page-size constant.
- **Cabela firstResult and page:** https://www.cabelas.com/l/fishing-boating-hot-deals?firstResult=36&page=2 · `INDEXED_REAL_URL` · 2026-11-17; supports Query shape differs from Bass Pro.
- **Petco 48-page plus sort:** https://www.petco.com/category/top-deals/clearance?page=2&sortby=offerprice&sortorder=ascending · `PUBLIC_HTML_TEXT` · 2026-11-17; supports 1-48 of 527, was-price markers and choices.
- **LEGO page 2:** https://www.lego.com/en-us/categories/sales-and-deals?page=2 · `INDEXED_REAL_URL` · 2026-11-17; supports Pagination URL.
- **Dell deal offer JSON:** https://www.dell.com/en-us/shop/deals/dc · `PUBLIC_INDEXED_CONTENT` · 2026-11-17; supports Embedded offerid/productData and stockstatus objects.
- **Chewy today’s deals dual-price:** https://www.chewy.com/deals/todays-deals-2723 · `PUBLIC_HTML_TEXT` · 2026-11-17; supports Chewy Price vs Autoship Price.
- **PetSmart strikethrough definitions:** https://www.petsmart.com/help/promotional-terms · `OFFICIAL_TERMS` · 2026-11-17; supports Strikethrough may not be prior actual price.
- **Costco warehouse savings:** https://www.costco.com/o/-/warehouse-savings · `PUBLIC_HTML_TEXT` · 2026-11-17; supports Member/online/warehouse location campaign terms.
- **Sams Instant Savings requirements:** https://help.samsclub.com/app/answers/detail/a_id/520/~/what-is-sams-club-instant-savings-program · `OFFICIAL_TERMS` · 2026-11-17; supports Active membership needed.
- **CVS ExtraCare price entitlement:** https://www.cvs.com/extracare/overview · `OFFICIAL_TERMS` · 2026-11-17; supports Price account-linked.
- **Awin feed download and update information:** https://help.awin.com/developers/docs/product-feed-publisher-guide-intro · `OFFICIAL_API_DOC` · 2026-11-17; supports Feed list and last-updated.
- **CJ GraphQL Product Feed Search:** https://docs.cj.com/docs/productfeed-api-search · `OFFICIAL_API_DOC` · 2026-11-17; supports Publisher productFeeds/product query.
- **Impact product catalog download:** https://help.impact.com/partner/what-would-you-like-to-learn-about/platform-features/marketing-content/product-marketplace-and-catalogs/download-product-catalogs-as-a-partner · `OFFICIAL_API_DOC` · 2026-11-17; supports Catalog download via website/FTP/API.
- **WooCommerce Store products on_sale:** https://developer.woocommerce.com/docs/apis/store-api/resources-endpoints/products/ · `OFFICIAL_API_DOC` · 2026-11-17; supports on_sale=true; page/per_page; variation exclusion.
- **Keepa deal browse:** https://keepa.com/api-docs/deals.html · `OFFICIAL_API_DOC` · 2026-11-17; supports Tokenized deal query, ASIN data.
- **Woot official developer:** https://developer.woot.com/ · `OFFICIAL_API_DOC` · 2026-11-17; supports Category feed + offer batch expansion.
- **Best Buy API:** https://developer.bestbuy.com/apis · `OFFICIAL_API_DOC` · 2026-11-17; supports Catalog, pricing, SKU.
- **Tractor Supply tabbed Shop Items On Sale and Now/Was:** https://www.tractorsupply.com/ · `PUBLIC_HTML_TEXT` · 2026-11-17; supports Tabbed category list, product prices, See Price at Checkout.
- **Harbor Freight public clearance 51 listings:** https://www.harborfreight.com/merchandising-promotions/clearance.html · `PUBLIC_HTML_TEXT` · 2026-11-17; supports Online Exclusive/In-Store Only/Choose Options per product.
- **Wayfair Closeout current/was:** https://www.wayfair.com/daily-sales/closeout · `PUBLIC_HTML_TEXT` · 2026-11-17; supports Closeout card prices and discount countdown.
- **Advance Auto coupons/clearance landing:** https://shop.advanceautoparts.com/o/advance-auto-parts-coupons-and-deals · `PUBLIC_HTML_TEXT` · 2026-11-17; supports Clearance campaign and exclusions.
- **Walgreens official coupon mechanics:** https://www.walgreens.com/topic/help/shophelp/coupons_help.jsp · `OFFICIAL_TERMS` · 2026-11-17; supports myWalgreens clipped coupons and weekly ad.
- **CompsAPI price information not retailer feed:** https://compsapi.com/ · `PROVIDER_CLAIM` · 2026-11-17; supports eBay actual paid-price claim; not retailer feed.
- **Current ArbiScout implementation:** https://github.com/maidiu/arbiscout/tree/work/arbiscout-local-build/ENGINEERING/arbiscout_app · `REPOSITORY_SOURCE` · 2026-11-17; supports Crawler/categorizer/eBay watcher.
- **ARB-020 F1 restrictions and candidate matrix:** https://github.com/maidiu/arbiscout/tree/agent/arb020-f1-zero-api-fees-scraping-feasibility-r1/CONTROL_ROOM/WORKERS/RETURNS · `REPOSITORY_SOURCE` · 2026-11-17; supports Technical, terms and feasibility, October research.
- **ARB-020 F2 evidence ten:** https://github.com/maidiu/arbiscout/blob/1abba9ad24a846d73d06efa9943f550f475b5fa1/CONTROL_ROOM/WORKERS/RETURNS/ARB-020-F2-SPECIALIST-FEED-COVERAGE-R1/06_EXPANDED_TEN_SOURCE_SHORTLIST_AND_TERMS_CORRECTION_R2.md · `REPOSITORY_SOURCE` · 2026-11-17; supports Ten documented leads, zero granted use rights.

**Research custody:** Original ARB-020 survey and the F1/F2 worker returns are documentary evidence and retain their own exact branch SHAs. Neither those returns nor this dossier constitutes independently accepted code or authorizes scraping/licensed data usage.
