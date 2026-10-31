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
               lawfully accessible eBay SOLD evidence
                  (price distribution, 30d sales, supply)
                               |
             full landed cost + selling fees + shipping
                return/quality/lead-time & capital risk
                               |
                0–10 evidenced human-reviewed picks
                               |
            actual buy → sell → net return → calibration
```

## True blocking edge
The hard live gate is not "creating an eBay app"; it is **a permissioned, complete, affordable, high-quality source of actual comparable completed-sale evidence**. eBay's ordinary active-listing search cannot replace this. The parallel retailer deal-feed legal/operational gate is separately unresolved. Contract/legal gates block only live use, not source-free architecture or a synthetic vertical demonstration.

## Product organs / producer-to-consumer contract
- **Source registry** → provider adapter: known output fields, permission, region, rate and retention.
- **Retail candidate** → offer verifier: immutable observed URL/seller/GTIN/condition/price/tax/stock/shipping/coupon/expiry.
- **Identity** → market comparison: exact match or type-specific refusal; no fuzzy optimistic substitution.
- **eBay demand evidence** → economics: documented completed-sales count, timeframe, sample, handling of accepted offers, market competitors and uncertainty.
- **Finance** → ranker: realistic final acquisition and selling economics, category fees, returns reserve; distinguish domestic vs import time-to-capital recovery.
- **Ranker** → human report: evidence references, expiry, confidence, 0-10 qualifying results; no automatic buying.
- **Outcome ledger** → calibration: actual realized sale, unsold inventory, returns, cost, time, model error and data-source yield.

## Stage ladder
G0 source-rights/price/sold-data feasibility; G1 provider-neutral schema & synthetic full pipeline; G2 first source-permitted retail and comparable sales pair; G3 fully priced human-facing report; G4 scheduled 30-day pilot; G5 realized-profit learning; G6 multi-retailer/import expansion and observed yield optimization.

**Parallel productive lanes:** auditing candidate sources and using authorized structured shopping feeds; reviewing PR #1; import economics design; seller-specific fee research; tests of negative cases; human report design. G2 cannot claim PASS until both acquisition and sold-data provenance are genuine and permitted.

## Minimal realistic first consumer
One source-verifiable live discounted item, exact matched completed-sales evidence from a permitted route, category-specific fee and shipping inputs, a human report and item-level audit trail. With data permissions unresolved, keep the producer tested using clearly labeled synthetic examples only.

## Fan-in
PR #1 and control-room branch start independently from main; review latest SHAs, accept scoped code and docs, integrate on an explicit merging branch, run tests together. No blind assertion that PR #1 is already on main.
