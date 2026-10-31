# ArbiScout — Governing Product Constitution (revision 2026-10-31)

**Authority:** user-directed functional definition. Proposed on the ArbiScout control-room branch until reviewed and merged to canonical main. This supersedes earlier project descriptions wherever they define ArbiScout as an application *for a named person, seller, resale business, competing retailer, or dropshipping operation*.

## The product, exactly

> **ArbiScout broadly indexes bargains offered on the internet by major retailers, identifying opportunities to purchase those retailers' products under specified conditions informed by historical eBay price patterns.**

That is the system's constitutive function. It is not defined by the identity of a user, the legal form of an operator, an assumed onward sale, or a particular downstream use of a purchased item. Do not reintroduce an invented beneficiary in requirements, architecture or agent instructions.

## Operational capabilities

1. Discover deals, promotions, sale and clearance offers across multiple participating retail sources; optionally include import marketplaces when offer and freight conditions can be compared accurately.
2. Normalize product identity (brand, exact model, UPC/GTIN, variant, bundle quantity, condition) and merchant, price, availability, geography, timestamp, shipping, coupons and taxes where relevant.
3. Examine eBay historical price **patterns**, emphasizing genuinely comparable completed sales and frequency when available, separating these from active asking prices and missing data.
4. Define transparent purchase conditions: acquisition price versus historical eBay price distribution, evidence age, frequency, supply, full delivered cost, shipping time, availability, and uncertainty.
5. Rank and report up to ten sufficiently supported purchase candidates daily, retaining source references and explicit refusals. Zero qualifies when evidence is inadequate.
6. Measure whether the index remains accurate and useful against later price observations; optional user-provided purchase/outcome data may calibrate financial metrics but does not redefine the product as a resale service.

Financial modeling (fees, possible future selling price, margins, capital risk) is an **optional evaluative module**, useful for particular decisions but not the governing identity of the index.

## Negative definition

ArbiScout is not constituted as a service *for* a designated seller, retailer, beneficiary or resale platform. It need not run a storefront, buy goods, resell goods, create listings, reprice inventory, train on eBay material, or place orders. Future optional modules require separate decisions and source permission.

## Separate factual and legal assessments

This constitution specifies **what the software does**; it does not make a factual claim about who ultimately operates it or what they do with its recommendations. Any actual provider application, API request, agreement or approval must accurately describe the intended use and operator in that context. Rewording a project's constitution does **not** override third-party API agreements, transform affiliate advertising APIs into general shopping research feeds, or confer eBay sold-data rights.

Treat source access as a distinct research problem with outcomes ALLOWED_SCOPED / NOT_CLEARLY_AUTHORIZED / REQUIRES_PERMISSION / PROHIBITED / UNKNOWN, tied to exact clauses and use. Preserve the strongest reasonable interpretation for purchase-oriented use without pretending unanswered licensing questions are settled.

## Inheritance and migration

Earlier materials use retail arbitrage, resale-profit, seller, and human purchase/realized profit as the primary project's purpose. Preserve those as the **historical motivating request** and optional application/use cases, while correcting current terminal-function language to the neutral bargain index above.

The PROGRAMMA must register this revision as the effective user instruction, update its terminal map, checkpoint and worker/HQ grok, and distinguish unreconciled historical terms from current requirements. This is not an authorization to erase evidence, change a provider's terms, acquire credentials, subscribe to paid sources, or merge drafts.

**Terminal acceptance:** A reproducible, well-evidenced current-bargain index relating accurate retail purchase offers to usable eBay price-pattern evidence and clearly identified conditions for purchasing; daily 0–10 output and truthful unknowns. Actual purchases or resales are *not* prerequisites for constitutive product completion.
