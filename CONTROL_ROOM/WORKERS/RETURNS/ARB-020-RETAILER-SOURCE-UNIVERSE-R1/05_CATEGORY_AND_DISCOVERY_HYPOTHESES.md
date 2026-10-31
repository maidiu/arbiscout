# ARB-020 R1 — Category × source hypotheses, NOT observed gap yields
**2026-10-31.** This is an experimental ordering by exact identity feasibility, live offer-discovery plausibility and *hypothesized* eBay completed-sales comparison density. **ZERO live retailer observations and ZERO eBay price gaps** were tested in this reconnaissance. No actual ranking of retailers by realized purchase-price shortfall is possible.

## Why separate modelability from opportunity
A complete Best Buy API does not prove Best Buy has unusually cheap products compared with actual normal eBay sold prices; a 70% markdown from MSRP does not mean a 70% eBay gap. A sparse sealed LEGO set may have a high eBay price during a particular period, but its current sealed identity, age and actual historical sample count must be checked. Treat every candidate class below as a falsifiable trial with reasoned expected failure, not a purchase recommendation.

| Class | Suggested source candidates | Exact-identity proof | Why test | Critical negative cases | Test order |
|---|---|---|---|---|---|
| Branded electronics and audio | Best Buy;B&H;Adorama;Walmart | UPC+full model/revision;new-sealed | Likely eBay volume, stable identity | Heavy price competition may erase apparent eBay gap; refurbished versions | P0 |
| Computer SSD/RAM/peripherals | Newegg;Best Buy;Micro Center;Amazon direct | part number+capacity+revision+pack | Frequent catalog price/stock updates | Used/renewed, counterfeit, vendor model aliases | P0 |
| Video game consoles/controllers | GameStop;Walmart;Target;Nintendo Store | model variant/region/controller bundle | Recognizable model codes, frequent listings hypothesis | Used/refurbished vs new, collectors' bundles | P0 |
| LEGO sealed sets | LEGO Store;Target;Walmart;Barnes & Noble | set number+edition+new-sealed | Strong set number correspondence, seasonal markdowns | Retirement and release-date time-window distortion | P0 |
| Branded handheld power tools | Home Depot;Lowe's;Tractor Supply | manufacturer SKU+bare tool vs kit | Feed-friendly catalogs, seasonal tool promotions | Battery/charger bundles and store pickup | P0 |
| Smart-home devices | Home Depot;Best Buy;Costco | gen/model+regional voltage/kit | Brand exact matches and potential eBay comps | Package 2-packs, retailer exclusive models | P0 |
| Small branded appliances | Walmart;Target;Kohl's;Macy's | UPC/model/pack/voltage | Broad household promo catalog | Expensive shipping, loyalty promotions, returns | P1 |
| Kitchen electronics | Costco;Sam's Club;Best Buy | UPC/edition/region/quantity | Recognizable models and periodic discount | Warehouse bundles, member and oversized delivery | P1 |
| Power tool batteries | Home Depot;Lowe's;Amazon direct | OEM genuine model/Ah/quantity | Brand match and repeat sales plausible | Counterfeit/compatible battery, multi-packs | P1 |
| Printers and scanners | Staples;Office Depot;Best Buy | model+regional refill variant | Strong UPC and business catalog | Consumables subscriptions/rebates; shipping | P1 |
| Digital cameras and lenses | B&H;Adorama;Best Buy | exact model/lens mount/kit | Specific manufacturer SKUs | Lens bundles, grey-market warranty, refurbished | P1 |
| Headphones and wearables | Samsung;Best Buy;Costco | model/firmware/color/size | High contemporary eBay volume plausible | Open-box/used and new model revisions | P1 |
| Board games and hobby kits | Barnes & Noble;Michaels;Target | edition/language/UPC/quantity | Exact edition possible for sealed games | Small sale sample and box damage | P1 |
| Fitness devices | Dick's;REI;Academy | model/size/region | Branded devices and seasonality | Large-unit shipping; membership discounts | P2 |
| Outdoor electronics | Bass Pro;Cabela's;REI | model/region/frequency | Brand model may be matchable | Restricted products exclusions, shipping | P2 |
| Pet grooming tech | Chewy;Petco;PetSmart | manufacturer model/new condition | Brand UPC, electronic product | Autoship restrictions and small resale sample | P2 |
| Toys and collectibles | Disney;GameStop;Target;Walmart | limited edition/serial/set number | Clearance and limited release hypotheses | Sparse comps, subjective rarity and damaged packaging | P2 |
| Generic office supplies | Staples;Office Depot;Amazon marketplace | UPC/pack quantity | Bulk retailer inventory | Little absolute gap, size/quantity errors | P3 |
| Furniture and large home goods | Wayfair;Costco;Home Depot | GTIN/white-label alias/delivery cost | Large markdowns from advertised retail | Weak identical eBay sample and freight/pickup | P3 |
| Apparel/footwear | Macy's;Nordstrom Rack;Kohl's | style+size/color/year/condition | Seasonal clearance abundant | Identity matching and eBay comparables often too sparse | P3 |
| Private-label tools | Harbor Freight;Monoprice | brand exact model | Store-led clearance | No broad eBay comp density guarantee | P3 |
| Wholesale/import | Alibaba;AliExpress | genuine GTIN+MOQ+unit landed cost | Potential lower acquisition price only | Forgery, quantity, duty, shipping, lead time, different products | P3 |

## Funnel tests, not intuition
For each retailer×category cell in a legally sourced pilot, separately count `offer_records`, `distinct_GTIN_model_region_condition`, `checkout_verified`, `substantial_discount_vs_retailer_regular_price` (diagnostic only), `sufficient_90d_exact_eBay_sales`, `lower_ebay_quantile_above_total_purchase_price`, `final_qualified_gap`. Calculate precision and the error types and their confidence intervals by source/category. Never let a deep sticker discount rank a retailer until eBay-normal values exist.

### Category-specific adversarial examples
- **Kit mismatch:** bare DeWalt drill at retailer vs kit with two batteries on eBay (false gap); record explicit bundle contents.
- **Storage revision:** 2TB SSD revision with changed cache/DRAM or speed, wrong seller/model variant.
- **Console bundles:** stand-alone Xbox vs special game bundle or refurbishment.
- **LEGO retirement:** 90-day medians of retired product should not be mixed with active/current edition identity.
- **Warehouse two-pack:** Costco 2 pack vs single unit eBay, wrong per-unit arithmetic and membership.
- **Pickup-only:** $20 local clearance claimed nationally, no valid stock for actual purchase region.
- **Open box:** retailer unit-specific condition vs eBay factory-sealed price.
- **Marketplace:** third-party Seller on Walmart/Amazon vs Walmart/Amazon direct, different guarantees/fulfillment.
- **Coupon:** membership, loyalty cash, trade-in, personal invitation, rebate-in-future, account-specific stacking not general actual checkout.
- **Shipping:** furniture $100 nominal markdown offset by $125 delivery; shipping and duties must remain purchase-side cost, not future selling expense.
- **GTIN-absent exclusives:** advertised model is retailer-exclusive; unproven identical SKU eBay comparables despite familiar title.
- **Extreme scarcity:** 1 or 0 actual recent eBay sales; no statistically defensible ordinary reference, not an inflated single listing.
- **Older transaction:** evidence from >90d must be labeled and should not quietly replace 90-day price pattern.

## Separate hypotheses by discovery mechanism
- **ShopSavvy deals / Keepa `/deal`:** stronger initial unknown-offer enumeration with filters and recency but selection/ranking bias; validate against direct retailer.
- **Merchant bulk feed (Home Depot/Awin/CJ/Impact):** potential high completeness *within approved advertiser catalog*, but may omit actual clearance or store-only inventory, dynamic coupons and stock.
- **Best Buy category traversal:** genuine catalog enumeration plus price/stock API, but only one retailer; easy integration is not demonstrated highest opportunity yield.
- **DataForSEO/SerpApi:** primarily compare or verify already known products. Treat as follow-up enrichment, not proof of unknown retail bargain discovery.
- **Community deal sites:** curated by users/editors, may surface highly unusual opportunities, but biased, duplicative, often expired, and programmatic commercial reuse must be licensed.
- **Manufacturer/outlet:** potentially steep sale tags with individual configurations and open-box conditions; unknown GTIN equivalence and limited inventory.
- **Importers:** optional and high-exclusion lane; MOQ, actual landed cost and authenticity are required. Their low displayed prices alone say nothing about exact eBay comparability.

## How to rank *after* measurements exist
Show two separate scores:
1. **Source access/engineering feasibility**: source granted, documented fields, true enumerable/known query coverage, published cost, latency, fixed seller/locale data, cache/retention rights and usable quantity/condition.
2. **Observed evidence-qualified purchase-gap yield**: unique new checkout-verifiable offers with exact identity and sufficiently dense genuine completed-sale history per cost of acquisition; median and lower-quantile difference, not promotional MSRP.

No composite model should multiply an evidence grade by an arbitrarily guessed 'deal yield'. Publish raw denominators and uncertainty. A source that finds 5 genuinely qualifying nonduplicate purchases in 1,000 legally verified offers may outperform a source that offers 100,000 banner discounts with 0 exact historical matches. This is a **conditional comparison example**, not observed data.

## First-test sample allocation
Pilot 100 offers *only after permission*: 25 branded electronics/gaming, 20 power tools/smart-home, 20 LEGO/toys/collectibles, 20 small household/appliances, 15 adverse categories (open-box/membership/pickup/multi-pack/very sparse). Ensure >8 discovery modes/providers are included in comparative source-selection preflight; actual single-source first trial may test fewer and should not be presented as full ecosystem benchmark. All real-product slots **UNFILLED / NOT EXECUTED** until an authorized source yields actual observations.

**No prohibited goods, purchases, future transaction predictions or fee/ROI ranking.**
