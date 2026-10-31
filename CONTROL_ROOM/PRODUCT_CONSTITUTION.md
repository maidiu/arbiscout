# ARBISCOUT — CONTROLLING PRODUCT CONSTITUTION
**User directive: 2026-10-31. Proposed control-room PR #2, not yet canonical main.**

## Exactly what the software does

**ArbiScout is a purchase-research application.** It broadly indexes bargains from major internet retailers and identifies **current purchase prices maximally below the regular historical sale-price patterns for the identical product on eBay**.

No external individual, retailer, sale operation, or presumed later use defines the application. A comparative eBay historical sale is an **observed reference price**, not a forecast, promise or intended transaction. The positive purchase opportunity is the **documented price gap**.

## In-scope producer-to-consumer chain

1. Discover current offers, sales and clearance across major retailers; retailer discovery must not depend on a fixed initial shortlist.
2. Validate exact product identity, condition, variant, size, bundle and quantity for the retailer offer and historical eBay comparable.
3. Record true retailer **total purchaser price** (item plus applicable acquisition-side shipping/discounts/tax where reliably known), stock, location, seller, date and link.
4. Construct a defensible **regular eBay historical completed-sale price baseline** for the identical product (distribution, observation count, time window, outliers and confidence); never confuse asking prices with actual completed-sale patterns.
5. Compute and rank price gaps: `absolute_gap = historical_reference_price - actual_retail_purchase_price`; `relative_gap = absolute_gap / historical_reference_price` (only with positive, adequately evidenced reference). A conservative historical quantile and source uncertainty should check false bargains. Ranking favors **large substantiated below-eBay purchase gaps**, not an imagined future sale or financial return.
6. Report zero to ten qualified purchasable bargains daily, with original retailer links, eBay historical evidence, last-checked timestamps, gap magnitude, uncertainty, exclusions and reasons. Return zero rather than invent.
7. Verify later price/availability observations and improve the **accuracy of the index**, independent of whether anyone purchases an item.
8. Optional import-source coverage may add wholesale quantity, delivered purchase cost, duties, currency and shipping-time conditions. These remain purely purchase-side comparisons.

## Out of scope

No future-sale simulation, eventual resale assumptions, seller marketplace fees, expected profit, ROI, inventory liquidation, automated purchasing, listing, dropshipping or account-specific selling behavior forms any part of the purchase-research application. Legacy code for these concerns in draft PR #1 is **not an approved component**; only neutral exact-product utilities can be considered for separate reuse.

Historical conversations that motivated an earlier design may remain in a clearly marked history/why-not record, but must not generate active requirements, tests, scoring criteria or downstream consumers.

## Data-access law

The project's **actual operations** determine which third-party API restrictions are applicable. Do not interpret terms against an invented resale service or third-party retailer. Conversely, neither a new description nor this document itself grants permission to access a restricted provider. Evaluate each source's terms honestly against bargain indexing and eBay historical price comparison, including operator/recipient facts where genuinely requested by a contract.

## Acceptance

A real current retailer purchase offer, matched to reliable regular historical eBay completed-sale prices for the same item, with an accurately calculated and substantial gap, reproducible purchase conditions and a truthful user-facing index entry. A daily 0–10 pipeline with reliable source update behavior is the terminal product. No subsequent economic transaction or realized income is necessary.
