# ArbiScout PROGRAMMA — operating dashboard

**Generated from canonical JSON.** This is an overview of research and implementation **states**, not a declaration of proven live commercial access. Governing scope: **purchase research only** — find retailer prices maximally below regular eBay completed-sale patterns for the identical product. No future selling model.

**Read:** [Constitution](../PRODUCT_CONSTITUTION.md) · [Full PROGRAMMA](00_PROGRAMMA_ARBISCOUT.md) · [Tasks table](TASKS_TABLE.md) · [question table](QUESTIONS_TABLE.md) · [Work JSON](01_WORK_REGISTRY.json) · [Question records](QUESTIONS/) · [Source JSON](02_SOURCE_REGISTRY.json) · [Current HQ](../STATUS/CURRENT_PROGRESS.md).

## Scope and counts

- **48** tracked capability tasks: BLOCKED_EXTERNAL: 1, IN_PROGRESS: 3, NOT_STARTED: 19, PROPOSED: 3, PROTOTYPE_DRAFT: 16, REVIEW_PENDING: 1, SCOPED: 1, SOURCE_DOCUMENTED: 4.
- **112** research/substantiation questions: OPEN: 74, PARTIAL: 32, SETTLED: 4, SUPERSEDED: 2.
- **Question dependency** = another conclusion needed first; **task hard prerequisite** = ALL; **source choice** = ANY ONE permitted source; **live evidence gate** = needed for real-world acceptance, not synthetic development.
- **Downstream reach** counts graph descendants and signals leverage, **not estimated effort, importance by itself, or proof of completion**. All `P0` items require judgment, not automatic worker dispatch.

## High-leverage independent P0 work tasks

| Task | What it establishes | State | Potential downstream | Live evidence gates | Alternative source gate |
| --- | --- | --- | --- | --- | --- |
| ARB-030 | Exact product identity and variant engine | PROTOTYPE_DRAFT | 17 | — | — |
| ARB-010 | eBay completed-sale historical price access | IN_PROGRESS | 16 | — | — |
| ARB-031 | Purchase-offer schema and provenance | PROTOTYPE_DRAFT | 16 | — | — |
| ARB-022 | Google Shopping search aggregators | SOURCE_DOCUMENTED | 6 | — | — |
| ARB-023 | Best Buy purchase-offer API and price fields | SOURCE_DOCUMENTED | 6 | — | — |
| ARB-024 | Walmart purchase-offer sources | SOURCE_DOCUMENTED | 6 | — | — |
| ARB-020 | Retailer bargain-source landscape | PROTOTYPE_DRAFT | 0 | — | — |
| ARB-035 | Cross-market buyer culture, turnover, ticket size and discount-attention asymmetry | PROPOSED | 0 | ARB-010, ARB-029 | — |

## P0 research questions ready for independent investigation

| Question | Question to settle | State | Downstream questions | Associated work |
| --- | --- | --- | --- | --- |
| Q025 | Which eBay API responses are active asking prices and which are actual completed-sale prices? | PARTIAL | 16 | ARB-010, ARB-040 |
| Q060 | Which exact product identifiers and quantity/condition fields are necessary for defensible retailer-to-eBay price comparisons? | PARTIAL | 8 | ARB-030 |
| Q045 | Which actual price, seller, shipping, product identity and location fields do third-party Google Shopping APIs return? | PARTIAL | 7 | ARB-022 |
| Q086 | Can a fresh Browser agent reconstruct the entire current purchase-research mission, code, sources and status without relying on chat history? | PARTIAL | 6 | ARB-083, ARB-084 |
| Q034 | Which Best Buy API product fields expose actual sale prices, discounts, stock, identity, and freshness? | PARTIAL | 4 | ARB-023 |
| Q005 | Does Best Buy's affirmative permitted-use language include purchase-oriented bargain indexing that links to Best Buy purchase offers? | PARTIAL | 3 | ARB-023 |
| Q008 | Does Walmart's affiliate API affirmatively permit a broad purchase-oriented bargain index, or require another license? | PARTIAL | 3 | ARB-024 |
| Q015 | What exact historical windows, regular completed-sale price summaries, accepted offers and count/dispersion metrics does Product Research expose? | PARTIAL | 3 | ARB-011, ARB-051 |
| Q037 | Which Walmart API/feed families can surface actual consumer purchase prices, rather than only affiliate, seller or advertisement data? | PARTIAL | 3 | ARB-024 |
| Q099 | Which sector×retailer pairs exhibit recurrent genuine price dips, and how long do discounted purchase offers remain available? | OPEN | 3 | ARB-035, ARB-020, ARB-032 |
| Q011 | Which eBay API/data-use agreement clauses govern accessing historical price patterns for purchases at other retailers? | PARTIAL | 2 | ARB-010 |
| Q088 | Are source documentation, access permission, implementation, actual execution, independent review and genuine index outputs treated as separate truth states? | PARTIAL | 2 | ARB-083, ARB-084 |
| Q027 | Do licensed independent suppliers expose dependable eBay historical completed-sale prices, samples, windows and costs? | OPEN | 1 | ARB-013, ARB-040 |
| Q042 | Can a compliant catalog/affiliate network yield offers from several retailers with stable identities, rather than separate retailer adapters? | OPEN | 1 | ARB-020, ARB-026 |
| Q096 | Which sector/subsector hypotheses combine unusually high regular eBay buyer demand with genuine discount-producing retailer sources? | OPEN | 1 | ARB-035, ARB-020 |

## First terminal proof

**One actual purchase offer → exact product match → adequate eBay regular completed-sale baseline → conservative absolute and percentage gap → source-linked purchase-research index entry.** A zero-item day is valid when data are insufficient. No transaction, fees or other future operations are needed.

## Source-reference inventory

| ID | Provider / source | Documented source | Use/access state | Recorded claim / limit | Next verification |
| --- | --- | --- | --- | --- | --- |
| E-EBAY-LICENSE | eBay developer API License Agreement | VERIFIED_PUBLIC_DOC | PERMISSION_UNRESOLVED | eBay API restricted activities distinguish modeling prices for items listed on eBay from historical price comparisons that inform RETAILER purchases. Actual bargain-index operations must be evaluated clause-by-clause. Seller arbitrage examples should not be presumed to define this project, nor can revised terminology override a provision that actually applies. | Record qualified permitted-use determination and a bounded product/price sample |
| E-EBAY-INSIGHTS | eBay Marketplace Insights API | VERIFIED_PUBLIC_DOC | NO_ACCESS_VERIFIED | Completed sales data historically limited release; current new-user entitlement unresolved. | Record qualified permitted-use determination and a bounded product/price sample |
| E-EBAY-RESEARCH | eBay Seller Hub Product Research | VERIFIED_PUBLIC_TOOL | ACCOUNT_NOT_CHECKED | Seller interface permits manual demand research with historical sold data; UI access does not confer automated extraction API. | Record qualified permitted-use determination and a bounded product/price sample |
| E-BESTBUY-API | Best Buy Products and Buying Options API | VERIFIED_PUBLIC_DOC | NO_KEY_OR_USE_GRANT_VERIFIED | Official product catalog, price, promotional signals and availability may directly support retailer bargain indexing and linking to Best Buy purchase offers; access subject to application-specific terms. | Record qualified permitted-use determination and a bounded product/price sample |
| E-BESTBUY-TERMS | Best Buy Developer API Terms | VERIFIED_PUBLIC_DOC | PERMISSION_UNRESOLVED | API is licensed in connection with offers/sales of Best Buy products. A bargain-index app linking to Best Buy purchase offers may fit that positive purpose. Separately, use for pricing analysis on behalf of a third party has a distinct restriction: applicability depends on actual operations and operator, not presumed resale. Terms also set display/attribution and cache limits. | Evaluate Best Buy official product API against actual retailer-purchase bargain index use, clause-by-clause (license purpose, third-party pricing-benefit restriction, display/link and 72-hour cache), without assigning a fictitious beneficiary. |
| E-WALMART-IO | Walmart affiliate I/O API terms | VERIFIED_PUBLIC_DOC | OTHER_USE_REQUIRES_PERMISSION | Affiliate I/O API terms are primarily advertising-oriented; consumer bargain indexing to aid purchases may need distinct permission. Ordinary retail purchases and affiliate/API qualifying-link purchases are separate activities; no presumption that the latter is used. | Record qualified permitted-use determination and a bounded product/price sample |
| E-WALMART-AFF | Walmart affiliate Operating Agreement 2026 | VERIFIED_PUBLIC_DOC | OTHER_USE_REQUIRES_PERMISSION | Affiliate link purchasing for resale is separately restricted; ArbiScout is a retailer bargain purchase index, not an affiliate-link resale purchasing bot. Access to affiliate data for general indexing still needs a compatible positive license. | Record qualified permitted-use determination and a bounded product/price sample |
| E-GOOGLE-MERCHANT | Google Merchant API market reports | VERIFIED_PUBLIC_DOC | ELIGIBILITY_UNCHECKED | Merchant Center account eligibility; not consumer Google Shopping general results feed. | Record qualified permitted-use determination and a bounded product/price sample |
| E-SERPAPI | SerpApi Google Shopping API | VERIFIED_VENDOR_DOC | PURCHASE_NOT_AUTHORIZED | Third-party structured Shopping search results; exact commercial contract, quality and unit cost need review. | Check permitted general-purpose price comparison/index use, retailer and eBay history coverage, freshness/region, retention and actual cost. No subscription without approval. |
| E-DATAFORSEO | DataForSEO Google Shopping API | VERIFIED_VENDOR_DOC | PURCHASE_NOT_AUTHORIZED | Third-party Google Shopping product/seller/price observations; documented pay-per-use, provider claims commercial applications. | Check permitted general-purpose price comparison/index use, retailer and eBay history coverage, freshness/region, retention and actual cost. No subscription without approval. |
| E-DATAFORSEO-PRICE | DataForSEO Google Shopping prices | VERIFIED_VENDOR_DOC | PRICING_NOT_ACCEPTED | Prices vary by response quantity, latency and tier; reverify before budgeting. | Record qualified permitted-use determination and a bounded product/price sample |
| E-TARGET | Target retail products | PUBLIC_RETAIL_SITE_ONLY | UNVERIFIED_API | Target clearance candidate, no generally open product-price API established by this registry. | Record qualified permitted-use determination and a bounded product/price sample |
| E-HOMEDEPOT | Home Depot retail products | PUBLIC_RETAIL_SITE_ONLY | UNVERIFIED_PERMISSION | Affiliate feed/Impact possibility from prior reconnaissance, needs independently qualified program documentation. | Record qualified permitted-use determination and a bounded product/price sample |
| E-ALIEXPRESS | AliExpress sourcing | PUBLIC_RETAIL_SITE_ONLY | UNVERIFIED_API | Third-party sellers, imported shipping/currency/warranty/stock variability; API rights and data unverified. | Record qualified permitted-use determination and a bounded product/price sample |
| E-ALIBABA | Alibaba sourcing | PUBLIC_RETAIL_SITE_ONLY | UNVERIFIED_API | Wholesale MOQ, supplier-specific data and landed costs; API/contract status unverified. | Record qualified permitted-use determination and a bounded product/price sample |
| E-PR1 | ArbiScout source-free PR #1 | REPOSITORY_ARTIFACT | REVIEW_PENDING | Matching, profit and ranking engine on draft branch. CI previously observed passing at a specific SHA, not merged or real-data tested. | Review exact diff and CI at current head |
| E-EBAY-2025-10K | eBay 2025 Form 10-K (SEC official) | VERIFIED_PUBLIC_DOC | NOT_APPLICABLE_PUBLIC_RESEARCH | Official focus-category growth in motor P&A, collectibles, luxury, refurbished, apparel/sneakers, and demand-side community needs. Aggregate growth does not establish specific SKU regular completed-sales counts, retail markdown frequency or cross-platform customer attention. | Separate category GMV and eBay platform strategy evidence from specific regular SKU sales and retailer-sale overlap |
| E-EBAY-RECOMMERCE-2026 | eBay 2026 Recommerce Report (company-commissioned survey) | VERIFIED_PUBLIC_DOC | NOT_APPLICABLE_PUBLIC_RESEARCH | 2026 secondhand buyer and seller surveys report broad category interests, purchase cadence, channel patterns and consumer motivations; useful for market-culture hypotheses, not proof an eBay buyer does not monitor retail deals. | Inspect survey methods, country splits and cohort biases before using any attention/channel proxy |
| E-MEH-API | Meh API current deal | VERIFIED_PUBLIC_DOC | REVIEW_PENDING | Official current-deal JSON endpoint; user-supplied API key used locally; one request per minute guidance; deal, item and price fields parsed. | Record provider terms and permitted-use review; verify reference-price availability. |
| E-WOOT-API | Woot Developer API | VERIFIED_PUBLIC_DOC | REVIEW_PENDING | Official x-api-key feed and offer endpoints; user-supplied key used locally; rate limits 1 request per second and 1000 per day; list and sale prices observed. | Record provider terms, feed coverage and permitted-use review. |
| E-KROGER-API | Kroger Products and Locations API | VERIFIED_PUBLIC_DOC | REVIEW_PENDING | Official OAuth2 client-credentials products and locations API; user-supplied credentials used locally; price requires locationId; regular and promo prices observed. | Record provider terms, location coverage and permitted-use review. |
| E-EBAY-SAVED-SOLD | User-saved eBay sold-search HTML | PUBLIC_RETAIL_SITE_ONLY | OTHER_USE_REQUIRES_PERMISSION | Manual user-saved sold-search HTML parsed locally; no automated eBay retrieval; eBay robots.txt disallows /sch/ for automated agents. | Use a licensed completed-sales provider or eBay API entitlement before claiming live automated evidence. |

## Maintenance

Edit JSON task/question/source records and log dated evidence; regenerate with `python scripts/render_programma.py --write` and validate with `python scripts/validate_programma.py`. CI checks the generated files. Status codes do not measure progress percentages.
