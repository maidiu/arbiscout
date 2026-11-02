# ARB-020 R1 — Retailer/API/affiliate access and permission correspondence (ALL DRAFTS — NOT SENT)
**2026-10-31.** No messages, tickets, account registrations, trial activations, purchases or API calls performed. User approval required to contact any party or submit credentials, billing or account application. The actual application is a **retailer purchase-research index** of current *buyable* prices versus **regular actual eBay historical completed-sale** references for precisely equivalent goods; it does not model future resale, seller fees, business margin, ROI or purchasing on anyone's behalf.

## A. ShopSavvy Data API — proposed request
Subject: Data API clearance discovery and retailer purchase-index authorization/coverage

We are evaluating your `GET /v1/deals` as a source of **previously unknown** discounted retailer products, followed by `/v1/products/offers` for direct merchant links and price/availability. Our application independently checks actual purchase prices and compares exact items with completed-sale history from a separately licensed source; we will not resell your underlying feed.

1. Your B2B terms permit display/store inside our own apps and derivative analytics but prohibit bulk standalone redistribution. Does our source-linked user-facing daily **0–10 qualified bargain index**, with sourced price/stock/history confidence, specifically fall within permitted app use? What retention/expiry/retraction duties apply to raw offers and historical aggregate analyses?
2. Does your upstream retailer/data acquisition carry required permissions for collecting, making available and allowing us to reuse price/deals/retailer history for this purpose? What rights can you substantiate, and which remain customer's responsibility?
3. For `GET /v1/deals`, enumerate the participating merchants/categories, geographic resolution, daily unique new deals, latest observed timestamps, site selection bias, total counts/offset truncation, clearance vs online vs local-store, third-party seller distinction and eligibility of membership coupons. Is it comprehensive within any defined scope or solely curated/ranked editorial records?
4. Does `is_clearance` mean verified actual checkout, or a source promo marker? Can we filter no membership, no coupons, new/sealed and direct retailer seller only? How are UPC, MPN, revision, bundle components and pack quantity associated with deals?
5. For `/products/offers`, is `availability` verified per destination zip/store and when? When does the source fetch/refresh a retailer price? Can our later merchant checkout validation find stale/incorrect prices and request corrections?
6. Please reconcile current pricing credit docs' **schedule refreshes free** with other marketing claims of charges per update; distinguish once-per-schedule vs ongoing price monitoring. Do errors, no-match queries, history per-day overhead and 100-identifier batches cost credits? Rate limit for 100k candidates/day?
7. Confirm $49/1k, $199/10k, $499/50k monthly plans, nonrollover credits, 14-day trial cancellation and custom 75k/500k/month pricing. Can we publish unfavorable independent benchmark findings?
8. Please authorize **one scoped 100-offer independent test** with raw source ID, timestamps, retailer link, matched GTIN and payment credit ledger. We will not ask for private credentials, customers or retailer session cookies.

**Status: NOT SENT.**

## B. Best Buy developer and data-rights
Subject: Proposed documented retailer purchase-price research using Best Buy public API

Our application compares **documented current Best Buy purchaser prices** with independent historical completed eBay sale prices for the exact same manufacturer SKU. We would link users to Best Buy purchase offers; there is no competing retailer operator or downstream sale service. Can you confirm in writing:
1. Whether this app fits the licence's purposes tied to offers/sales of Best Buy products, and whether your third-party pricing-analysis clause or other price-derived restrictions apply to an independent purchaser-reference application, not a retailer repricer? Specific controlling sections and any exception required.
2. May we enumerate `onSale`, price/clearance and exact UPC/MPN across Products/Categories and Buying Options, and cache only briefly (not beyond documented 72h) for display? Can we preserve **derived daily gap statistics and noncontent audit identifiers** beyond 72h, or does cache provision prohibit even derivatives?
3. Exactly which fields distinguish `salePrice`, `regularPrice`, promotion, web availability, store-level stock/zip, open-box condition, shipping and current purchase checkout? Which do not provide a sufficient total purchaser price?
4. Are direct Buy links and attribution sufficient; is a Developer API key free for the use described; do 50k/day/5/sec quotas apply to our key? Are category queries supporting true full-catalog pagination and sale filters?
5. Is Buyer Options open-box stock updated reliably, and how long do unit-specific prices persist? May consumers view location-specific prices with source timestamps?
6. Can we conduct a 25-product bounded manual and permitted API check and report price mismatch, exclusions and eBay median comparison without publishing private customer data?

**Status: NOT SENT.**

## C. Home Depot / Impact merchant-feed partnership
Subject: Approved daily Home Depot catalog feed for retail purchase-research index

Your affiliate FAQ describes daily product data feeds through Impact for approved affiliate websites. We ask:
1. Would a site displaying links to Home Depot purchase offers alongside eBay historical completed-sale reference prices qualify for the program? Does the permitted purpose cover independent product-price comparison and retention of source-derived price differences, even if no affiliate commissions are part of the software's function?
2. Is the daily full catalog feed available to newly accepted partners and what fields provide manufacturer GTIN/UPC/MPN, sale/regular price, discount, store stock/zip, ship-to-home, direct Home Depot vs marketplace third party, shipping, coupons, open box and update timestamp?
3. What percentage of web discounts or local clearance are represented? Is the feed a full eligible inventory census or restricted to the products you select? What file size, download schedule, stale data SLA, feed API/FTP and specific cache/redistribution terms?
4. Does affiliate acceptance require a live website, promotional links and minimum conversion? Are non-affiliate product research uses permitted through a different direct licence? What written approval is needed?
5. May we audit 20 tool/smart-home UPCs and report the precision of direct merchant checkout match and source feed timestamp?

**Status: NOT SENT.**

## D. Awin / CJ / Impact / Rakuten / Skimlinks / Sovrn
To each network and (where required) the **specific retailer advertiser**, send tailored version of:
- Are full product feeds or per-product APIs available to a new publisher before or only after acceptance by each merchant? Can we list **feed existence and last update** for nonjoined brands without downloading their contents?
- Does the actual allowed use encompass a retailer purchase-research comparison to historical eBay sale prices in a daily consumer index, with links to the merchant? Which provisions govern feed storage, full catalog indexing, derived stats, product descriptions/images, affiliate link attribution, caching and expiration?
- Is there per-merchant count, catalog-completeness flag, delta-feed feature, stock/zip, sale vs regular price, coupon and timing fields? Which product identity codes are true GTIN/MPN vs seller-provided title?
- Where are **merchant-specific authorization**, API/CSV/FTP credentials, minimum sales, quotas, fees and feed-latency SLA documented? Can category-wide clearance be enumerated, and how are out-of-stock or excluded products removed?
- Confirm access to specific required merchants; an account at CJ/Awin/Impact is not itself proof of a usable Best Buy, Target, Walmart or Home Depot feed.
Specific caution: Target 2026 affiliate/creator program changed; ask **current** Target managers, do not rely on historical Target Partner FAQ alone. Skimlinks product-key API is distinct from managed-only merchant reporting API.
**Status: NOT SENT.**

## E. Walmart I/O / Affiliate / DV-Volt — special written exception request
Your current I/O terms restrict affiliate API to **advertising Walmart products**, absent express permission for other uses, and restrict competitor pricing analyses. Our app is **not a competing retailer's pricing tool**, but it does produce an independent consumer purchase research index. Would that purpose receive affirmative permission? If yes specify scope, feed/category/zip access, raw and derivative retention, direct Walmart merchant filtering, site attribution, active discount/clearance enumeration, 5k/day quotas, partner costs and category feed approval. If no, please state exact restriction and any alternative commercial licensed product.

**Status: NOT SENT; no Walmart keys or affiliate enrollment.**

## F. Amazon Creators and Keepa
Amazon: Given the requirement for an accepted Associates account and qualifying referrals, is a purchase-research index with real Amazon purchase links and eBay historical price comparison allowed? Can a newly launched app without 10 qualified sales in 30 days be granted access? Distinguish Amazon retail direct offers from marketplace sellers, coupons and seller delivery charges; what TTL/attribution obligations apply?

Keepa: How is `/deal` recall determined across ASINs? Are only changed last-12h items searchable? Can we separately query Amazon direct only, available inventory, exact variant, 1-/2-pack, price type and regional delivery? Show licensed feed/redistribution/retention terms, paid token plans for 150/1,050/10,050/100,050 monthly deal-request tokens plus product details. Does any offline stored history meet publication requirements? Can 100 current offers be validated independently?

**Status: NOT SENT.**

## G. DataForSEO / SerpApi / SearchApi / OpenWebNinja / Oxylabs / Bright Data
Provide written clarification of:
- Whether supported data is merely query-ranked top-k Google Shopping vs **full unknown-merchant/catalog deal enumeration**; what actual retailer domains, marketplaces and regions and time freshness are covered?
- Whether given keyword/UPC returns every offer, only sponsored/relevant ranked offers or limited pages, and whether selected merchants can be filtered.
- Which fields verify *actual purchaser price and purchasability* (coupon, membership, tax, shipping, stock and localized pickup) vs displayed ad/asking price.
- Exact billed unit (search page vs successful result vs offer row), batch/parallel limits, partial failures/retries and price for **3k/30k/300k/3m queries monthly**, including refundable/nonrefundable deposits and data delivery delays.
- Upstream source rights: is automated extraction expressly authorized where site terms restrict it? Does the vendor contract grant our application the ability to publish source-linked derived historical comparisons and retain price records? Must user obtain separate site permission?
- Is an independently publishable 100-offer benchmark permitted? No API key, eBay account, cookie or buyer data is requested by this letter.
**Status: NOT SENT.**

## H. Editorial/community deals and physical/local clearance
DealNews: We have read your official RSS conditions (attribution, link preservation, no public browser extension). Does ingesting feed items as *candidate pointers* into a product research application, verifying them independently and publishing a URL to the original merchant or DealNews with attribution qualify? Must we preserve your referral code or can we only preserve the original DealNews link? What automated refresh/request limits apply? We will not rewrite links until grant confirmed.
Slickdeals / BrickSeek: Is there a current licensed and documented JSON/feed/API arrangement for newly posted deals, category filters, merchant IDs, UPC and local stock/coupon conditions, plus rate/retention/publication rules? If absent, no automated integration is proposed.
**Status: NOT SENT.**

## I. Alibaba / AliExpress (optional)
Does a developer or affiliate API permit actual consumer purchaser price retrieval (rather than supplier MOQ negotiation), shipping/taxes/duties to US, verified manufacturer GTIN, manufacturer brand authenticity, pack minimum, stock and delivery date? Is purchase-price indexing and retention permitted? If not, do not count imports as interchangeable domestic branded inventory.
**Status: NOT SENT.**

## Handling responses
Record date, exact operative clause, document version, vendor representative/contract authority and redacted proof securely. No public credentials, personal customer data, unpublished contract exhibits or confidential samples. Vendor promotional statements and fee schedules **are not independent proof** of full coverage/price accuracy or upstream rights. All requests above remain unsubmitted.
