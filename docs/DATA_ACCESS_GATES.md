# Data access and architecture gates (2026-10-21)

**Status:** No live data source is approved for ArbiScout. These are technical/legal risk findings, not legal advice. Confirm contract permissions before using any API or storing real platform data.

## Non-negotiable distinction

A source can be:
1. **Technically reachable** without login;
2. **Accessible to a human account** through a browser UI;
3. **Programmable with a developer key**;
4. **Permitted for our particular arbitrage analysis, caching, comparison, reporting and AI use**.

Passing one does not establish the others. Do not infer source rights from an API returning HTTP 200.

## eBay

Official agreement: https://developer.ebay.com/join/api-license-agreement

- Section 9 expressly restricts using eBay content to suggest/model prices for eBay items and using eBay services to engage in seller arbitrage (with examples of repricing and after-sale ordering). It also restricts using eBay content to train ML/AI, and restricts third-party comparison displays.
- Product Research is available in Seller Hub for eligible sellers as a human tool and covers three years of historical sales, but no general-purpose Product Research API is established by that fact: https://www.ebay.com/help/selling/selling-tools/terapeak?id=4853
- Marketplace Insights has sold-history capabilities but is a limited-release API requiring approval: https://developer.ebay.com/api-docs/buy/marketplace-insights/static/overview.html
- **Gate: no eBay integration until we have a documented permissible use / appropriate access rights.** Do not use anti-bot browsers, undocumented endpoints, stolen session cookies, or legacy Finding API endpoints as substitutes.

## Best Buy

Official catalog APIs: https://developers.bestbuy.com/apis

- Products API advertises product price and inventory availability and a developer key is available.
- Terms: https://developers.bestbuy.com/legal
- The February 2021 terms limit license scope and say the service/content may not be used on behalf of or for the benefit of third parties (including other retailers) to analyze Best Buy prices, products or services; caching is limited to 72 hours. An individual resale-research workflow **may** be outside the permitted scope; this requires an explicit approval determination, not an assumption.
- **Gate: do not install a live Best Buy ingestion job before resolving authorized use and retention restrictions.**

## Retail alternatives

Target, Walmart, Home Depot and other retailer interfaces should be investigated one at a time for:
- Documented API or licensed feed;
- Explicit permission for individual reseller sourcing and price comparisons;
- Allowed caching window, rate limits, geographical pricing, inventory and SKU identification;
- Price provenance, taxes, discount qualification, and seller-independent availability.

Do not treat public website visibility as a blanket scraping license.

## Interim plan without any credentials

1. Keep deterministic fee-aware and identity-aware adjudication independent of live data.
2. Add strict data schemas and provenance with synthetic data only.
3. Obtain a small set of **human-reviewed** candidate examples where lawful and record only permitted fields.
4. Evaluate a properly licensed sold-market data supplier or permission from eBay for this particular use case.
5. Calibrate seller-specific category fees and supply real shipping measurements.
6. Only after access is resolved, build staged provider adapters with error controls and independent tests.

## Account security

A longstanding eBay account should **not** be shared by sending passwords or copying browser cookies. If another person needs access to Seller Hub features, determine whether eBay's official Team Access supports the relevant research privileges and use scoped delegation. Seller Hub Product Research help documents Team Access as an available feature.

## Product integrity

Any system that lacks completed-sale evidence must label suggestions `UNVERIFIED`. Never convert asking-price spreads into fictional sell-through probabilities. Scoring models must distinguish predicted from realized profit, and preserve their fee assumptions.
