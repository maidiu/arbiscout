# ArbiScout — state of project at control-room seed (2026-10-31)

## Governing product identity and historical motivation
**Current governing constitution (user revision, 2026-10-31):** broadly index internet retailer bargains under purchasing conditions informed by historical eBay price patterns. There is no defined beneficiary or necessary subsequent resale. Read [PRODUCT_CONSTITUTION](PRODUCT_CONSTITUTION.md). **Historical motivation:** an earlier request concerned Walmart/Target/Best Buy retail arbitrage and potential Alibaba/AliExpress sourcing; downstream resale-profit analysis is now optional, not terminal-purpose law.

## Evidence-backed repo state at seed
- Repository: `maidiu/arbiscout`, **public**; `main` at `2c2f3d64ce49edc3073c7feb094bf803ee84d371` when seeding, with initial README.
- Separate existing **draft PR #1**: `agent/arbiscout-sourcefree-foundation-r1`, code and unit tests for deterministic source-free candidate matching/economics. At previously verified head `799747af35bf154fcf23c994604230c945fe0161`, CI passed. **NOT MERGED**. Must recheck current PR and test identity before adoption.
- This control room: `agent/arbiscout-programma-control-room-r1` as **separate** proposed branch; does not import PR #1's code.
- No verified live retailer API, no authorized eBay historical price-pattern feed, no deployed daily bargain index, no live validated purchase-condition report. A resale-profit backtest is an optional extension, not a terminal criterion.
- An eBay account and developer-program membership have been discussed. No confirmed production application or API entitlement is inferred, and no passwords/keys stored.

## Major live unknowns
- Useful historical eBay price-pattern evidence in permitted programmatic form; official Marketplace Insights access constraints and API terms require use-specific interpretation, not assumptions about a resale business.
- Whether individual/private analytical uses under retailer API licenses are authorized; no blanket small-seller exception established.
- Google Merchant API ≠ consumer Google Shopping search API; third-party Shopping result providers need terms/cost/freshness vetting.
- Best Buy, Walmart, Target, Home Depot/Impact, AliExpress, Alibaba: supplier-specific permission and data contract unresolved.
- Purchase/shipping/stock/region conditions and safe product categories. Resale fee/returns variables belong to optional economic analysis, not a presumed seller.
- Repo privacy choice before any private business data is uploaded.

## Current strategic selection
Proceed source-free and evaluate data access in parallel. Keep explicit permission gates on live integrations. Critical path: retailer-price and eBay-history access → verified current offer and same-product history → purchase-condition comparison → daily index (0–10) → index accuracy evaluation. Optional financial and import modules do not block this spine.

## Immediate planned coherent efforts (none launched)
1. **ARB-SRC-01** cross-retailer source/legal feasibility with explicit scope and priced proof.
2. **ARB-MKT-01** completed-sales rights and possible independent licensed data providers, plus human Product Research boundary.
3. **ARB-CORE-01** review PR #1 and selectively retain exact matching, with downstream resale finance remaining optional.
4. **ARB-DISC-01** Google Shopping discovery proof with authorized provider and no bills before user approval.

Read `STATUS/CURRENT_PROGRESS.json` for the record; do not claim this dated snapshot remains live without revalidation.
