# ArbiScout — state of project at control-room seed (2026-10-31)

## Business demand (user-supplied)
A personal research scout for **retail arbitrage + import sourcing**, scanning Walmart/Target/Best Buy and possibly others for daily marked-down items, finding exact same items selling **consistently** for a higher *completed-sale* price on eBay, producing **up to ten actionable candidates per day**. Alibaba/AliExpress add supplier landed costs, minimum quantities, shipping price/time and uncertainty. Human makes purchase decision.

## Evidence-backed repo state at seed
- Repository: `maidiu/arbiscout`, **public**; `main` at `2c2f3d64ce49edc3073c7feb094bf803ee84d371` when seeding, with initial README.
- Separate existing **draft PR #1**: `agent/arbiscout-sourcefree-foundation-r1`, code and unit tests for deterministic source-free candidate matching/economics. At previously verified head `799747af35bf154fcf23c994604230c945fe0161`, CI passed. **NOT MERGED**. Must recheck current PR and test identity before adoption.
- This control room: `agent/arbiscout-programma-control-room-r1` as **separate** proposed branch; does not import PR #1's code.
- No verified live retailer API, no authorized eBay completed-sales API, no deployed daily pipeline, no actual market backtest, no validated real report.
- An eBay account and developer-program membership have been discussed. No confirmed production application or API entitlement is inferred, and no passwords/keys stored.

## Major live unknowns
- Usable sold-market evidence in a permitted programmatic form; official eBay Marketplace Insights limited access and eBay API arbitrage restrictions.
- Whether individual/private analytical uses under retailer API licenses are authorized; no blanket small-seller exception established.
- Google Merchant API ≠ consumer Google Shopping search API; third-party Shopping result providers need terms/cost/freshness vetting.
- Best Buy, Walmart, Target, Home Depot/Impact, AliExpress, Alibaba: supplier-specific permission and data contract unresolved.
- Purchase, shipping and tax basis for the actual seller; allowable categories, returns and regulated goods.
- Repo privacy choice before any private business data is uploaded.

## Current strategic selection
Proceed source-free and evaluate data-access economics in parallel. Keep explicit authorization gates on live integrations. Do not mistake a finished charter for a finished data pipeline. Critical path: source agreement → verified price and sold evidence → exact matching → economics → daily shortlist → human validation → historical calibration.

## Immediate planned coherent efforts (none launched)
1. **ARB-SRC-01** cross-retailer source/legal feasibility with explicit scope and priced proof.
2. **ARB-MKT-01** completed-sales rights and possible independent licensed data providers, plus human Product Research boundary.
3. **ARB-CORE-01** review and adopt PR #1 only after independent engineering/evidence assessment.
4. **ARB-DISC-01** Google Shopping discovery proof with authorized provider and no bills before user approval.

Read `STATUS/CURRENT_PROGRESS.json` for the record; do not claim this dated snapshot remains live without revalidation.
