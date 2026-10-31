# ARB-035 / 04 — Retail markdown timing, value and what the pages actually prove
**Research date:** 2026-10-31. **Caution:** A current retailer promotional page or a discount *from the retailer's own list/reference price* is neither a measured repeat cadence nor a verified difference from normal eBay paid-sale history.

## Dated, first-party documentary offer surfaces (NOT eBay gap records)
| Source & observation | Observed public page claim | Mechanism supported | Critical missing proof |
|---|---|---|---|
| LEGO US sale page [E05], viewed 2026-10-31 | Set **10345 Flower Arrangement** publicly displayed at **$65.99 vs $109.99** (40% badge); page includes retiring-soon flagged goods and other set numbers. | Exact set-number offer discovery, publicly offered markdown and structured identity. | Checkout and geographic stock, timeline of *previous* discounts, actual paid eBay new/sealed comparable distribution. An expensive MSRP/set does not mean an eBay gap. |
| Adorama US camera clearance [E06], viewed 2026-10-31 | Sony a7 IV camera+28–70 mm lens special bundle, listing **$2,217.95 vs $2,717.95**, tagged $500 limited-time saving; manufacturer part shown and included-value extras. | High-dollar nominal promotion exists in specialist photography; available catalog includes $1000+ ticket bands. | Manufacturer base vs bundled kit identity, each included accessory, condition, direct checkout, true eBay historical paid-price for exactly matching contents. No repeated-frequency observation. |
| Home Depot Daily Deals [E07], viewed 2026-10-31 | Official page describes **daily** special buys, select tool/appliance categories, and explicitly says online only, while supplies last; current deals reset at specified time. | **Promotional event schedule** at a retailer, not frequency at a product SKU. | Number of eligible deep discounts per SKU over time, approval/licensed feed, eBay historical transaction correlation, actual final all-in price. |
| Harbor Freight Ways to Save [E08], 2026-10-31 | First-party page identifies several annual parking-lot sale occasions, instant savings, in-store/online clearance, highly localized open-box, and bundle promotions. | Mechanism for high/low ticket irregular clearance, pickup-only geography, kit identity hazards. | Any particular item recurrence or paid eBay market. Store-private labels may have little regular eBay history. |
| Harbor Freight coupon [E09], dated Oct 30–Nov 1, 2026 | 15% off one eligible item, one use per person/day, with exclusions and store/online conditions. | Verified **short promotional window and quantity constraint**; example of observable customer purchase conditions. | Not a claim a particular qualified SKU sold at that total price; not a repeated SKU discount; only if coupon conditions apply. |
| Best Buy Products API [E10] | Documents `regularPrice`, `salePrice`, `onSale`, `priceUpdateDate`, online/store availability. | First-party **data shape** supports longitudinal merchant price monitoring, if rights and actual access granted. | No API call in this work; no sampled current prices, permissions or sold eBay matched samples. |
| ShopSavvy deals API [E11] | Vendor describes paginated curated feed, clearance and price-drop filters, 1 credit per 10 deals, editorial/community grade. | Enumerable *discovery* in contrast to known-product lookups. | No authorized API call, no proof of entire retailer census, independent retailer checkout truth or official eBay sale price; its grade is irrelevant to gap truth. |

**Documentary snapshot rule:** Retail pages are mutable. This return records the content accessible at research time, not an archived checkout receipt, price-history time series or guarantee that the page remains unchanged. Figures above are **retailer-page advertised prices, not validated final purchase totals**; no gap dollars are inferred. The coupon item is a promotion mechanism, not a specific SKU bargain. Do not transfer these values to `02` as if they were matched completed-sale comparisons.

## What *cadence* actually means
Distinguish (a) a store's sale-event schedule (Home Depot daily, LEGO episodic, HF seasonal) from (b) repeated price dips on *the same exact identity* with stable package/condition. A daily-deals page can rotate different products every day without offering a single product twice. Estimate for each SKU/merchant from authorized longitudinal observations: 
- Local time of first active regular/base price, `price_dip_start`, `price_dip_end`; a dip is counted only if product was independently observable between promotions and own ordinary merchant price is separately documented.
- Decline from eBay same-SKU ordinary historical median and conservative p25 **at the sale timestamp**; calculate `purchase_gap`, not `(MSRP-sale)/MSRP`. Count negative and zero gaps in denominator.
- Fraction of weekly checks with bona fide stock and valid purchase, distinct events per 90 days, markdown magnitude distribution, duration survival curve, repeated events per year/season. Do not count 10 returned sponsored listings as 10 distinct merchant offers.
- Separate member-only, rebate-after-purchase, store-only, open-box, final-sale, return-policy and one-per-customer promotions. Exclude unknown freight/tax or mark geographically conditional, never invent all-in checkout.

## Falsification and decay
At promotion publication (t_0), observe retailer stock/total-price `R(t)`, eBay recent completed-sale `B(t)` from rolling windows, and (if allowable) eBay active asking changes. Historical paid sales naturally lag; do not interpret an immediate unchanged 90-day median as proof information has not diffused. Compare `t_0+6h,24h,72h,7d` for merchant offer survival; observe subsequent actual-sale distribution by the **same product**, compare matched unpromoted SKU time-series, control for model releases and seasonal sale events.

**Alternative drivers**: a gap may disappear because clearance stock runs out (not because eBay buyers saw it); eBay historical baseline may fall because product demand weakens; a promotion may lower its national effective price while final checkout is not accessible regionally. Attribute mechanisms only after comparison.

## Priority source families (NOT ranked gap yields)
**Better discovery:** authorized ShopSavvy deal feed and approved merchant catalogs (see ARB-020); **better first-party price and identity:** Best Buy Products API; **better explicit sale-event evidence:** Home Depot daily deals, LEGO first-party sale, Adorama clearance; **harder localized potential:** HF store clearance. Nothing here proves that the highest percentage-off supplier delivers the largest evidence-qualified eBay-relative dollar gaps.

### Source URLs
E05 https://www.lego.com/en-us/categories/sales-and-deals
E06 https://www.adorama.com/clearance/l/Photography/Cameras
E07 https://www.homedepot.com/daily-deals
E08 https://www.harborfreight.com/ways-to-save
E09 https://go.harborfreight.com/coupons/2026/10/e184905-001-2/
E10 https://bestbuyapis.github.io/api-documentation/
E11 https://shopsavvy.com/data/documentation/deals
ARB-020 documentary return: https://github.com/maidiu/arbiscout/tree/agent/arb020-retailer-source-universe-r1/CONTROL_ROOM/WORKERS/RETURNS/ARB-020-RETAILER-SOURCE-UNIVERSE-R1

## Pending numeric observations
`eligible_distinct_offer_count=UNKNOWN; weekly_repeated_SKU_markdowns=UNKNOWN; offer_duration_distribution=UNKNOWN; median_absolute_eBay_gap=UNKNOWN; eBay_p25_purchase_gap=UNKNOWN; verified_qualifying_per_1000=UNKNOWN`. No paid API/retailer checkout test, longitudinal tracking, historical matching or real bargain acceptance executed.
