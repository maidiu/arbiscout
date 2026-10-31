# ARB-010 — first-pass public evidence seed (2026-10-31)

**Status: RECONNAISSANCE_ONLY / NOT INDEPENDENTLY ACCEPTED / NO PAID OR AUTHENTICATED API TEST.** This is material for the separately prepared I3 Rabochii, not a canonical vendor choice. Reverify dates/pricing/URLs and each distinct eBay marketplace. It must not be treated as proof of live production access or historical-price validity.

## First-party facts established at documentary grain

1. eBay [Product Research](https://www.ebay.com/help/selling/selling-tools/product-research?id=4853): documented Seller Hub tool for eligible sellers, **up to three years** of actual completed sales, including accepted Best Offer transaction price; filters include UPC/MPN/EPID/EAN/ISBN, condition/date, price, site/location and category. This is the strongest **official human-accessible reference** for spot-checking. **No documented public developer API or bulk CSV export confirmed by this pass**; must not infer the Seller Hub Reports CSV/exports are Product Research exports. Investigate supported manual exports and data-use permissions.
2. [Team Access](https://www.ebay.com/help/account/team-access/team-access?id=5197): eBay explicitly lists permission to **research products using Product Research**, without sharing passwords. This supports authorized *human* baseline checks; delegated permission does not itself grant API extraction.
3. [Marketplace Insights](https://developer.ebay.com/api-docs/buy/marketplace-insights/static/overview.html) + [marketplace availability](https://www.developer.ebay.com/api-docs/buy/static/ref-marketplace-supported.html): historically `item_sales` searches up to **90 days**; Limited Release, categories require whitelisting; marketplace doc says **not open to new users**. Eligibility for a new application is therefore a primary negative constraint.
4. [Browse API](https://developer.ebay.com/develop/api/buy/browse_api): item availability/current asking prices and catalog matching; not a full completed-sale API.
5. [Deprecation status](https://www.developer.ebay.com/develop/get-started/api-deprecation-status): Finding API and Shopping API decommissioned **2025-02-04**, making `findCompletedItems` not a viable new integration.
6. [eBay User Agreement](https://www.ebay.com/help/policies/member-behavior-policies/user-agreement?id=5414): prohibits automated scraping/data-extraction means absent eBay prior express permission; [eBay developer license](https://developer.ebay.com/join/api-license-agreement) has separate restrictions around content, derived statistics, price modeling and certain activities. Exact operation-specific contract review required; neutral purchase research ≠ the imagined earlier seller-scoring app.

## Third-party vendors with specific documented endpoints — claims UNTESTED

| Supplier | What vendor claims | Advertised minimum/starting cost (at observed date) | Central evidential problem | First source |
|---|---|---|---|---|
| CompsAPI | Search page up to 240 historical sold listings; free 1yr, Growth 3yr; accepts Best Offer actual price | Free: 100 monthly calls; $9: 5k/mo, 1yr; $29: 25k/mo, 3yr | Supplier marketing; real paid-price provenance and sampling completeness not established | https://compsapi.com/pricing |
| CompSniper | `/v1/scrape` recent, `/v1/research/sold` 3yr, up to 240 entries, accepted Best Offer | Free 100/mo; $9: 2k/mo; $29: 10k/mo | Supplier claims actual paid accepted-offer price, upstream provenance and 3yr completeness untested | https://api.compsniper.com/docs and https://api.compsniper.com/pricing |
| Soldgraph | `/v1/ebay/sold`, multi-marketplace sold-result page, summaries, 15-minute cache | 100 free **once**; $9: 2k/mo | **Explicitly notes accepted Best Offer display may be seller's asking price**; must not treat as paid transaction | https://soldgraph.com/docs/api/sold and https://soldgraph.com/docs/api/usage |
| SoldComps | `/v1/scrape` page of sold records, batch capability, accepted offer hydration optional | Pricing requires separate primary-plan review | Paid-price hydration and batch extra request cost, provenance, coverage | https://sold-comps.com/docs |
| Trawl | `/ebay/v1/sold` stored multi-year US/UK sold archive, up to 100/page | $20/mo: 3k credits; $50: 15k; custom volume | Archive coverage/completeness, latency and actual accepted-offer price not verified; category/item specifics vary | https://www.trawl.dev/docs and https://trawl.dev/pricing |
| eBay Sold Listings API | `/scrape` up to 240 results, CSV/batch, multiple marketplaces, accepted offer opt-in | Free **50** requests; priced tiers need independent official review | Distinct provider identity, listing quality, provenance, completeness and costs untested | https://ebaysoldlistingsapi.com/docs |
| PriceCharting (category-specific comparator) | Historical pricing context for video games/collectibles; paid JSON/CSV catalog | Paid subscription, 1 request/sec; commercial sharing separately licensed | Its **Prices API explicitly says historical sale records are NOT supported**. Historical eBay transaction replacement is NOT established | https://www.pricecharting.com/api-documentation |

**Potential additional providers/research tools to investigate, without inferred accessible machine-readable historical outputs:** ZIK Analytics, WorthPoint, ShelfTrend, 130point, CompSniper-hosted MCP, other licensed pricing aggregators, data warehouse archives and direct eBay partner agreements. No provider is proven merely because their website markets a product.

## Why a provider's median may be wrong

- User-chosen query matches different model generations, conditions, lots, accessories or multipacks.
- Accepted Best Offer may display LAST ASK rather than PRICE PAID (Soldgraph acknowledges this), overstating the ordinary reference.
- Search results page may be a **top-k subset** rather than a complete 90-day window, biasing a median.
- Shipping may be excluded for some rows and included for others; multi-quantity sales counted inconsistently.
- Product Research's more complete, up-to-three-year view may disagree with a third-party latest-90-day endpoint for a legitimate reason.
- Country/currency, item location, outliers and seller removals may distort a reference.

Each vendor result should therefore have a separate quality test against an authorized official Product Research *manual* oracle; don't use the vendor's own benchmark as independent validation.

## Preliminary recommendation — **NOT FINAL**

(1) Treat eBay Product Research as first-party validation oracle and optional human pilot, not as a proven automated input. (2) Commission direct primary documentation/rights/cost evaluation of at least six sold-data API suppliers in parallel. (3) Seek clear written confirmation of actual underlying data provenance, rights/retention and accepted-offer paid-price basis. (4) Design an independent 30-item source-by-source accuracy benchmark but don't run unapproved paid or automated authenticated calls. (5) Implement source-neutral ARB-040 observation schema only with explicit provenance/missing-price flags while ARB-010 remains unresolved.

## Commission and review

Full [ARB-010 I3 exhaustive commission](../WORKERS/COMMISSIONS/ARB-010-EXHAUSTIVE-EBAY-SOLD-HISTORY-RECON-R1.md) and [prepared issue #3](https://github.com/maidiu/arbiscout/issues/3). A prepared issue is **NOT a running agent**. Independent primary-source and domain-specific adverse review is required before vendor status changes to ACCEPTED.
