# ARB-020-F1 — One-page $0 retailer acquisition GO/NO-GO
**Observed:** 2026-10-31, US source jurisdiction. **Scope:** existing Mac, $0 recurring retailer data-provider fees, $0 paid scraping/proxy/hosting. **Source proof:** primary published terms/API docs, directly read selected robots.txt, **NOT LIVE retailer/API calls**. Synthetic parser test **8/8 PASS in verified container Python 3.13.5**, not on user's Mac.

## Direct verdict
**RETAILER SIDE: CONDITIONAL GO for a narrow, approved two-source prototype. BROAD automatic clearance census of major US retailers at $0: NOT PROVED, presently NO-GO for claiming reliable universal coverage. END-TO-END $0: HOLD** because ARB-010 has not qualified a free, permissioned, market-wide actual-paid eBay completed-sale API. A free retailer producer does not resolve eBay. No strong empirical daily qualified-offer yield is known.

Best $0-recurring-fee **candidate lanes, not three approved live feeds**:
1. **Best Buy public developer Products/Categories/Buying Options API** — best large direct merchant SKU/price/availability and potential `onSale` catalog enumeration. Published **50k calls/day and 5/sec**, apparently no published per-call subscription. **Gate:** register key voluntarily, confirm application licence (offers/sales related), no use for certain third-party pricing analysis and max 72-hour display cache. Neither key nor permitted indexing is confirmed. Best Buy HTML scraper is unnecessary and has distinct robots restrictions.
2. **Merchant-supplied feeds** — Home Depot publicly offers a **daily** Impact data feed to *approved* affiliates with an existing live website; Awin and CJ document publisher product feeds containing prices and update times; Impact downloads require joining a brand with a catalog. **Gate:** accept into right advertiser, explicit purchase-index use/retention, data fields and merchant web sale coverage. Program application nominally free does not prove approved $0 feed rights. Full bulk catalog is stronger for unknown products than targeted SKU search.
3. **Written-permission WooCommerce Store API from a suitable independent retailer** — documented unauthenticated `/wp-json/wc/store/v1/products?on_sale=true&page=N&per_page=100` with price, currency, availability, SKU and paginated total headers. **Gate:** identify 1–2 *actual* sizeable branded-merchant catalogs and obtain consent or equivalent applicable authorization; framework openness does **not** authorize scanning arbitrary WooCommerce merchants. Its branded, high-ticket, eBay-comparable sale density is untested.

**Kroger** merits a limited *fourth* test: a public self-service OAuth Products API yields UPC/product and store-specific price with `filter.locationId`. It may return broad products but has **no documented `on_sale` filter**, price/stock requires selected location, grocery categories generally less attractive for eBay; site scraping is separately prohibited by Kroger's Sept 2026 terms. Registered free API access vs reuse in this purchase index needs review.

## Firmly rejected as automatic HTML defaults
**Walmart and Target** explicitly prohibit unapproved site scraping/automated product extraction. **Newegg** separately prohibits website automation and says scrapers may cause IP bans; **B&H** prohibits page-scrape/robots without written consent; **GameStop** prohibits systematic commercial product extraction. These restrictions apply despite a Mac, Selenium/Playwright, robots paths or public visible prices. Shopify API terms explicitly restrict systematic product indexing; `products.json` is **not** a general automatic licence.

## Volume
| Unknown discounted **unique buyable** candidates/day | S0/S1 evidence verdict | Actual test |
|---|---|---|
| **100** | Plausible if a broad Best Buy query or approved large merchant daily feed returns enough sale/stock matches | NOT EXECUTED |
| **500** | Possible only with verified catalog breadth and good sale rate; zero documented feed gives a guaranteed 500 | NOT EXECUTED |
| **1,000** | No reliable consented and accurate multi-merchant route presently proved; high source maintenance or bulk catalog access needed | NOT EXECUTED |

Raw downloaded catalog records **are not** unique current discounted offers. Brand/GTIN, current actual obtainable price, condition, stock/ZIP, shipping, duplicates, region and permissions must survive filtering. A feed with 10k products can produce zero qualifying offers.

## Least-expensive decisive experiment
Do **not** start by building dozens of scrapers. Get a written/in-scope **no-charge** Best Buy key grant (or accepted no-fee feed), then an independent second no-charge channel (approved Home Depot/merchant feed or consented Woo store). Retrieve **20–50 real dated sale candidates total across two approved sources**, dedupe exact models, verify 10–20 current retailer purchase prices/availability through authorized merchant channels/human checks. Manually reference official eBay Product Research for a subset of 5–10 exact items if lawfully accessible; use a scoped/qualified sold API only if separately authorized and affordable. Instrument records/source, true paid basis, calls and human minutes. If **zero** valid identity/product matches or no attainable price/stock on 20–50 despite permitted source, stop that route; if no legal eBay sales truth, record **retailer GO / complete index HOLD** rather than saying successful.

### Explicit judgments (worker self-report, not acceptance)
- **Engineering:** CONDITIONAL, sourcefree parser **8/8 PASS** but zero live retailer producer and no Mac execution.
- **Purchase-gap/data quality:** HOLD, no 20–50 live offers or qualified eBay reference.
- **Permission/privacy:** HOLD, no actual retailer developer keys, brand grants, or permitted source data retention; blocked HTML targets rejected.

**Next action required:** ONE small authorized dual-source canary, not another expansive research program. Preserve separate hostile reviewer on exact Git SHA. No production source, 100/day yield, or eBay actual-paid source accepted.
