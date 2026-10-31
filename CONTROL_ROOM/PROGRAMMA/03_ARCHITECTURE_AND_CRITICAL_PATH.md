# Whole architecture and critical path

```text
DOMESTIC: Walmart/Target/BestBuy/deal feeds   IMPORT: AliExpress/Alibaba
              |                               |
              +---- documented acquisition offer ----+
                               |
             verify price, timestamp, seller, region, stock
                               |
             exact brand/GTIN/model/variant/bundle/condition
                               |
               usable historical eBay price patterns
                  (price distribution, 30d sales, supply)
                               |
             purchase conditions + optional finance/shipping
                optional lead-time/risk assessment
                               |
                0–10 qualified retailer bargains
                               |
            price-pattern/index quality validation
```

## True blocking edge
The hard live gate is not "creating an eBay app"; it is **a permissioned, sufficiently reliable source of comparable historical eBay price patterns**, with exact distinction between actual completed sales and current asking prices. eBay's ordinary active-listing search cannot replace this. The parallel retailer deal-feed legal/operational gate is separately unresolved. Contract/legal gates block only live use, not source-free architecture or a synthetic vertical demonstration.

## Product organs / producer-to-consumer contract
- **Source registry** → provider adapter: known output fields, permission, region, rate and retention.
- **Retail candidate** → offer verifier: immutable observed URL/seller/GTIN/condition/price/tax/stock/shipping/coupon/expiry.
- **Identity** → market comparison: exact match or type-specific refusal; no fuzzy optimistic substitution.
- **eBay demand evidence** → economics: documented completed-sales count, timeframe, sample, handling of accepted offers, market competitors and uncertainty.
- **Purchase-condition engine** → ranker: current acquisition terms against historical price patterns, freshness, available quantity and explicit thresholds. **Optional financial engine** can include future sale fees, reserves or import capital recovery.
- **Ranker** → human report: evidence references, expiry, confidence, 0-10 qualifying results; no automatic buying.
- **Index quality monitoring** → calibration: later observed retailer prices and price-pattern comparisons, invalid/stale offers and precision of bargain alerts. Optional downstream inventory/resale outcomes are not a terminal requirement.

## Stage ladder
G0 source-rights/price-pattern data feasibility; G1 provider-neutral bargain index schema & synthetic full pipeline; G2 first source-permitted retail offer + historical eBay signal; G3 qualified purchase-conditions report; G4 scheduled index-quality pilot; G5 coverage/freshness calibration; G6 optional financial/import modules and broader retailer expansion.

**Parallel productive lanes:** auditing candidate sources and using authorized structured shopping feeds; reviewing PR #1; import economics design; optional seller-specific fee research; tests of negative cases; human report design. G2 cannot claim PASS until both acquisition and sold-data provenance are genuine and permitted.

## Minimal realistic first consumer
One source-verifiable live discounted retail offer, matching historical eBay price-pattern evidence from a permitted route, a concrete comparison condition and linked human-facing index entry. Fee/revenue projections are optional. With data permissions unresolved, keep the producer tested using clearly labeled synthetic examples only.

## Fan-in
PR #1 and control-room branch start independently from main; review latest SHAs, accept scoped code and docs, integrate on an explicit merging branch, run tests together. No blind assertion that PR #1 is already on main.
