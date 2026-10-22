# ArbiScout

Evidence-first retail-arbitrage research. **Research support, not a buying or sales bot.**

## Status

`v0.1` is a **source-free, deterministic prototype**: it reads manually entered or synthetic retail offers and market observations, verifies minimum product identity and evidence rules, calculates estimated economics, and ranks eligible opportunities. It **does not** call eBay, retailers, or any AI provider; it **does not** scrape pages, infer actual sales from active listings, place orders, or make resale guarantees.

## Quickstart

Requires Python 3.11+; no third-party dependencies.

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m arbiscout.cli examples/synthetic_candidates.json --as-of 2026-10-21
```

All products, URLs, prices, and sales evidence in `examples/synthetic_candidates.json` are **fictional test fixtures**. They must not be interpreted as market data or investment recommendations.

## How a candidate becomes eligible

1. A retail offer has verifiable URL, captured price/timestamp, stock indication, and identifying brand/model or GTIN.
2. The market observation includes source type, reference, timestamp, *completed-sales* count over the preceding 30 days, recent sold-price estimate, active competing listings, and matching product identity/condition. **Current asking prices do not count as sold evidence**.
3. Exact known GTINs, models, brands, and conditions agree. If neither side shares a GTIN, both brand and model must agree. Uncertain variants are **not** silently matched.
4. Estimates account for acquisition tax/shipping, marketplace fee assumptions, packing and fulfillment, promotion, and returns reserve. Estimates are not exact eBay fee quotes.
5. Data must be sufficiently recent; product must be in stock; predicted profit, ROI, and 30-day sold count must clear configurable minimum thresholds.

Unknown or stale evidence produces **REVIEW**, not a high-confidence opportunity. A positive result is still **VERIFY BEFORE BUYING**, not a purchase instruction.

**Limitations:** Evidence references and `source_type` declarations are supplied by the operator, not independently authenticated by this code. It doesn't validate that an item was actually sold, or that a sold-price estimate represents a comparable sample. The heuristic score is *not* a predictive probability. Seller-specific fees and tax bases must be calibrated before using real capital.

## Inputs and data rights

Inputs are JSON with `assumptions` and `candidates` arrays. The example documents the shape. Human-entered Product Research findings, if used, must be entered only as allowed by the relevant terms. Do not upload eBay credentials, authentication cookies, screenshots containing sensitive information, or real buyers' personal data to this repository.

Before implementing live data adapters, determine which eBay and retailer APIs or data feeds explicitly permit the contemplated arbitrage use case. Access to the eBay website or Product Research UI alone is *not* proof of permission to programmatically extract its data. No restricted API or undocumented Seller Hub endpoint is used here.

## Next stages

- Audit candidate providers for licensed retail prices and recent completed sales (including fees and usage terms).
- Add authenticated provider adapters only after documenting permission and test fixtures for failures.
- Calibrate category-sensitive costs and demand estimates against actual resale outcomes.
- Add persistent history and scheduled reporting **only** when there is a compliant source with which to run it.

## Security

This repository is currently public. Never commit API keys or verification tokens. Use GitHub Actions secrets or a proper secret manager for future services. Human-verified market observations should exclude personal information and content for which retention is not permitted.
