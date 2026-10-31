# ARB-035 / 03 — eBay demand, completed-sale turnover and evidential limits
**2026-10-31. Actual matched SKU-level historical eBay completed-sale records obtained in this task: ZERO.** This is NOT a claim of zero market sales. No seller account or licensed paid-price historical API was used.

## Two separate courts: platform category activity ≠ per-SKU regular sales
| Evidence | Grounded observation | What it cannot establish |
|---|---|---|
| eBay FY2025 Form 10-K [E01] | In 2025, eBay reports almost $80B GMV across all marketplaces and 135M buyers worldwide; 2025 Focus Category growth exceeded rest of platform and includes collectibles, Motors P&A, luxury, refurbished, apparel/sneakers. Filing says GMV includes returns and cancellations. | SKU counts, ticket/median per subcategory, new-condition comparable sales, eBay/retailer gap, high historical dollar reference |
| eBay Seller Hub Product Research [E02] | Official seller-facing research documents up to **three years** sales, filters UPC/MPN/EPID/condition/location/format, actual sold price including accepted Best Offers, average sale price/range, seller counts; ordinary completed listing search limited to previous **90 days** [E02 FAQ]. | Access in this session, bulk machine-readable access rights, exact historical sale rows or time-series derived values |
| Seller Center Sourcing Insights [E04] | Category-level demand/supply research for sellers with qualifying Basic+ Store subscription; trend and item-specific analysis potential. | Individual price-paid truth, merchant discounts, cross-channel attention |
| eBay 2026 Recommerce study [E03] | Surveyed categories and consumer motivations; trust/quality prominent. | Actual marketplace census, any exact SKU completed-sale count, separation from retailer deal monitors |
| ARB-010 PR #4 [R01] | Unadjudicated 29-route documentary source reconnaissance; credible human eBay oracle, conditional third-party vendor candidates, paid-price rights and accepted-offer warnings. | Granted license, independent price accuracy, live API, usable sold sample |

## Required observations, currently unavailable
At an exact identity key `(brand, canonical MPN/GTIN, variant, pack/bundle, condition, location, marketplace)`, request dated completed transactions for **7, 30, 90 and 365 days** (when allowed); optional last 36 months only if official Product Research/historical provider supports it. Avoid assuming 7-day slice availability from vendors supporting only 90-day aggregated counts. Carry:
- `sale_record_id` (stable pseudonymous provider record identifier only), `sold_at`, `actual_paid_item_price`, `paid_price_provenance`, `seller_shipment_charged` or `shipping_unknown`, currency, site, true condition and exact contents; do NOT collect buyer identity.
- `n_7,n_30,n_90,n_365`, weeks with >=1 paid sale, longest intersale gap, last-sale age, robust median, p25/p75, IQR/MAD, serial/week stability and outlier sensitivity. If provider only returns aggregates, record precisely which fields **cannot** be reconstructed.
- `supply_active_listing_count` separate from sales count, with point-in-time exposure (not sold/available ratio naïvely equated to demand).
- Sparse-price and trend flags, Best Offer actual-paid provenance, refunded/canceled inclusion uncertainty, used vs new stratification, new model generation and item location shipping treatment.

### Explicit missing-data matrix
| Sector grouping | n7 | n30 | n90 | n365 | median | lower quartile | weeks-with-sales | source status |
|---|---|---|---|---|---|---|---|---|
| OEM vehicle components | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO ROW ACCESS |
| Professional tools / genuine batteries | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO ROW ACCESS |
| Cameras / optics / pro audio | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO ROW ACCESS |
| Networking / computer parts / industrial | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO ROW ACCESS |
| LEGO / sealed hobby / TCG | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO ROW ACCESS |
| Small appliances / printer OEM | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO ROW ACCESS |
| Watches / sport / luxury | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO ROW ACCESS |
| Mainstream consoles / negative controls | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO ROW ACCESS |

## False market-depth mechanisms to prohibit
1. **eBay categories promoted by management** are not same-item recurring sales, and focus investments select outcomes; corporate GMV and 135M buyer totals cannot rank SKU demand.
2. **Current listings** are supply/asking prices; `sold` indicator without verified actual consideration can conceal accepted Best Offer paid amount lower than displayed headline.
3. **Condition mixture**: used/refurb eBay observations vs retailer new or new-open-box SKU can inflate or reverse difference. No routine multi-condition median.
4. **Bundle and compatibility drift**: lens kit vs camera body, tool kit vs bare unit, model-year module change, refurbished network device lacking licenses, LEGO limited edition vs retail box. No shared population if contents differ.
5. **Survival and selection**: most expensive surviving active listings are unsold; selective highlight sales overstate recurrence. A 90-day spike from new release or retirement is not normal 365-day demand.
6. **Price nonstationarity**: tariffs/currency, major model change, production stoppage and seasonality; a stale 3y reference can be irrelevant even if historically actual.
7. **Return/cancellation**: aggregated GMV includes them as eBay notes; where row provider cannot establish net consideration/cancellations, state the limitation, don't overclaim completed net sales.
8. **Seller cohort concentration**: a few batch transactions are not weekly independently recurring demand; consumer identities not needed to check concentration by allowed pseudonymous listing/seller cohorts.

## Decision rules for later pilot
An observation is *historically adequate* only under preregistered minimum sample/window and uncertainty constraints in 07: **illustrative study gate n90 >= 12 paid exact-condition comparable sales, >= 6 distinct weeks with sale across 13 rolling weeks, last sale <= 21 days, price-shift inspection**; these are conservative study heuristics, **not validated market laws**. Report raw rows even when fewer; label exploratory/sparse, not an index-qualified regular baseline. 365-day auxiliary sample cannot fix a nonstationary 90-day market without declared exception, sensitivity and review. For stratified science, include low-volume cells deliberately rather than excluding them before measuring the denominator.

## Source and permission
[E01] https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm
[E02] https://www.ebay.com/help/selling/selling-tools/research?id=4853
[E03] https://www.ebayinc.com/recommerce-report/
[E04] https://www.ebay.com/sellercenter/growth/ebay-research-tools
[R01] https://github.com/maidiu/arbiscout/pull/4
**Actual human Seller Hub Product Research interaction, manually sampled output, third-party API keys, rows, REST requests and independent comparison:** NOT EXECUTED. ARB-010 source claims remain review-pending; vendor access is not proven permissible because documentation exists.
