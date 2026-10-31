# RABOCHII LAUNCH — ARB-010 / ARB-011 / ARB-012 / ARB-013 — EXHAUSTIVE EBAY REGULAR COMPLETED-SALE HISTORY ACCESS COURT

**COMMISSION STATUS: PREPARED_NOT_LAUNCHED. A GitHub file/issue does not start an agent.** User must actually dispatch it in a selected Browser/Work or qualified local agent runtime. No agent is selected or running by this artifact.

REPOSITORY: `maidiu/arbiscout` (PUBLIC at seed).
ROLE: Independent **I3 / HIGH** documentary, API-ecosystem, data-science, and access-rights forensic reconnaissance Rabochii. **NOT** ArbiScout HQ, eBay-account operator, API permission authority, legal counsel, integrator, or own independent reviewer.
SINGLE_AGENT_FULL_DELIVERABLE: YES. Exhaust all plausible routes within the source/evidence standard instead of stopping at the first API, remembered product, or vendor sales claim.
EXECUTION: S0 public official/vendor/technical research; S1 authenticated GitHub reads and authorized *isolated branch documentation writes* if granted in the chosen session. No personal eBay account, developer login, purchased API keys, paid trials, automated external scraping, CAPTCHA bypass, or secret access. S2 code/test execution only if positively verified in assigned host. S3 live account execution prohibited unless separately explicitly delegated and source-permitted.
RECOMMENDED_EDITOR_MODEL_PAIR: Browser / GPT-6 High (or a user-chosen equally capable qualified research harness); **user selects editor/model/effort**, confirm actual capabilities; NO autonomous switches. HOST COST/QUOTA: UNKNOWN. Prefer use of already connected GitHub and primary public documentation rather than paid services. No billing.
BASELINE REFERENCE: `agent/arbiscout-programma-control-room-r1` at frozen pre-commission SHA `2d5e12b6abc9dda0bca2971b991d4257c05289f7`. This is an *evidence snapshot*, not a claim of latest HEAD at dispatch. Before working record current SHA, merge-base, branch/PR #2, PR #1 and whether constitution is on main. Use a new task branch `agent/arb010-ebay-history-exhaustive-r1` from a **verified current** control-room branch if user has authorized GitHub writes. Never reset or overwrite other work.
PRIMARY TASK: `ARB-010`. Related research `ARB-011` Product Research, `ARB-012` eBay developer/API capabilities, `ARB-013` third-party alternatives. Operational first consumer is `ARB-040` eBay historical-price record adapter → `ARB-051` robust ordinary eBay sale-price baseline → `ARB-050/060` index maximally reliable gap below the ordinary eBay completed-sale prices of the *same product*. **No future sale, seller fees, ROI, or business-operation modelling.**
GOVERNING CONSTITUTION: `CONTROL_ROOM/PRODUCT_CONSTITUTION.md`, `CONTROL_ROOM/PROGRAMMA/00_PROGRAMMA_ARBISCOUT.md`. Read `CONTROL_ROOM/00_READ_ME_FIRST.md`, all PROGRAMMA docs, `01_WORK_REGISTRY.json`, `QUESTIONS/` (especially Q011/Q013–Q030/Q062–Q066), `02_SOURCE_REGISTRY.json`, `DASHBOARD.md`, `03_RABOCHII_AND_REVIEWS.md`, `04_SOURCE_PROVENANCE_AND_DECISION_LAW.md`, `06_EXECUTION_AND_GITHUB_LAW.md`, `STATUS/CURRENT_PROGRESS.json` before starting analysis.

## The precise research objective

Discover **every genuinely plausible, technically usable avenue** for obtaining true historical eBay *completed-sale* price observations suitable for ARB-010. Determine by documentary and, where explicitly permitted, reproducible technical evidence: (1) what data is offered (actual final sale price vs asking price vs accepted Best Offer price, sold date, product GTIN/model/variant/condition/quantity, shipping, site/currency); (2) history depth and coverage, freshness and sampling completeness; (3) access eligibility and specific signup/approval/key/scopes steps; (4) actual license terms for using data in a **retailer purchase-research index**; (5) reliability, price/sample biases and verification methods; (6) initial and ongoing costs, quota, search count and operational scale; (7) legal/security/reputational risks; (8) implementation difficulty and first consumer; (9) recommended *sequenced* plan, backup paths, and unresolved approvals.

### Required search universe (don't assume exhaustive just because it is listed)

**Official first-party:**
1. eBay **Product Research** (formerly Terapeak): all Seller Hub / eligible app usage; up to three years, actual accepted offers, UPC/MPN/EAN/ePID search, sold count and average/range, supported export/download/manual sampling, Team Access, cost/eligibility, whether an authorized automated read/export is actually documented. Verify and explicitly label unverified any purported CSV or query-automation feature. Distinguish Sourcing Insights and its separate eligibility.
2. eBay ordinary sold/completed listings UI: 90-day scope, how displayed accepted-offer prices diverge from actual paid amounts, exact product matching and whether human use can act as benchmark; document public interactive route only. Don't propose automated scraping without permission.
3. eBay **Marketplace Insights** item_sales: limited release/new partner prospects, supported countries/categories, 90-day max, authorized application/partner onboarding process, realistic viability for a new app.
4. eBay **Browse** / other Buy REST + new GraphQL: prove precisely whether any endpoint returns **other sellers' historic sold transactions**, not just active listings. Explore Sell Analytics, Trading, Order APIs to exclude **own-sales-only** routes appropriately. Examine any approved Feed/Bulk/Marketing/Research/partner products; distinguish API marketing from actual completed-sales endpoint.
5. Retired **Finding API findCompletedItems / Shopping API**: verify 2025 decommission date from eBay primary documentation, kill stale GitHub architectures, and note any functional successors.
6. Directly negotiated eBay **business/developer partnership, enterprise data license, or commercial data sharing**, with published entrypoints if they exist. Draft precise, accurate request for permission and data/product availability. Do not send messages or create accounts without user authorization.

**Independent technical/data suppliers:**
7. CompsAPI; CompSniper; Soldgraph; SoldComps; Trawl; eBay Sold Listings API; any materially distinct functional provider discovered via reproducible search. Check each one's **own docs**, API spec, TOS, actual price schedule, output schema, country, count, pagination, latency, failure behavior, accepted-offer handling, sample window and provenance. Some vendors publish SEO comparisons of competitors: those are vendor marketing, not independent benchmark results.
8. Other historical-data aggregators (Terapeak competitors, research tools and inventory intelligence vendors) with legitimate API/CSV/enterprise feeds; identify e.g. ZIK Analytics, ShelfTrend, WorthPoint, 130point and category-specific price research only when a **real usable historical endpoint/export** is proven; separate visual subscription UI from machine-readable and multi-category sources.
9. Domain-restricted price-history APIs such as PriceCharting or other category-specific services: clearly label limitations and whether they return **individual historical eBay transactions** or only synthesized current price values. They cannot silently replace item-level regular eBay sale history.
10. Lawfully licensed historical data archives, public datasets, vendor exports or permissioned warehouses, if any; show age/bias/renewal and clear data grant; reject unverifiable datasets.
11. Off-the-shelf GitHub/OpenSource connectors claiming sold data: review source lines, license, exact call targets and whether actual data is from a retired endpoint, login cookies, browser stealth, dynamic scraping, mislabeled active listings or made-up statistics. Do not run stranger code with credentials; no stealth recommendation.
12. Feasible **hybrid** modes: human Product Research as oracle for quality and calibration with a licensed 90-day API for scale, narrow-category sanctioned price data, human-entered verified reference records, or staged manual pilot while live machine access remains unresolved. Explicitly distinguish one-off research, daily automation and possible account/retention restrictions.

### Initial verified leads (reverify currentness; do not copy vendor claims as findings)

- eBay Product Research https://www.ebay.com/help/selling/selling-tools/product-research?id=4853 and https://www.ebay.com/sellercenter/growth/ebay-research-tools — up to 3 years, actual accepted offer price, Seller Hub; separate Sourcing Insights.
- eBay Team Access https://www.ebay.com/help/account/team-access/team-access?id=5197 — research permission is delegable.
- eBay Marketplace Insights https://developer.ebay.com/api-docs/buy/marketplace-insights/static/overview.html and marketplace matrix https://developer.ebay.com/api-docs/buy/static/ref-marketplace-supported.html — restricted, new applicants currently not open; 90-day history, category-whitelisting.
- eBay Browse https://developer.ebay.com/develop/api/buy/browse_api — searchable active listings, not market-wide completed-sale data.
- eBay API deprecations https://www.developer.ebay.com/develop/get-started/api-deprecation-status — Finding and Shopping retired Feb 4 2025.
- eBay API terms https://developer.ebay.com/join/api-license-agreement and user agreement https://www.ebay.com/help/policies/member-behavior-policies/user-agreement?id=5414 — review specific clauses for price derivation, reuse, scraping, commercialization and actual operation.
- CompsAPI https://compsapi.com/pricing (advertises free 100 requests/mo, paid $9 5k and $29 25k, older history); CompSniper https://api.compsniper.com/docs and https://api.compsniper.com/pricing (advertises 100 free monthly and three-year research); Soldgraph https://soldgraph.com/docs/api/sold and https://soldgraph.com/docs/api/usage (admits Best Offer headline may NOT equal paid amount); SoldComps https://sold-comps.com/docs; Trawl https://www.trawl.dev/docs and https://trawl.dev/pricing; eBay Sold Listings API https://ebaysoldlistingsapi.com/docs; PriceCharting https://www.pricecharting.com/api-documentation (specifically says historic sales NOT supported in its Prices API). All are potential vendor *claims*, not independent proof.
- eBay general User Agreement restricts unauthorized automated extraction; a vendor's assertion of commercial-use rights under its own contract does not by itself show upstream authorization. Flag this as unresolved evidential/legal risk, neither automatic exoneration nor a categorical claim of illegality.
- Source vendor pricing and features may change in October 2026; snapshot each claim with retrieval date and quoted short clause/field. There may be substantial self-promotional SEO content masquerading as neutral comparison.

## Separate truth tests

DO NOT collapse these:
A. The vendor exists and its endpoint responds.
B. The endpoint returns *sold* rather than *completed-unsold* or *active* listings.
C. The visible price equals **actual transaction/accepted offer price**, not last listing ask.
D. The rows represent the **same item** (GTIN/model/condition/quantity).
E. The sampled rows and 90d/3y windows are sufficiently complete/recent for a statistically defensible normal price.
F. The provider has documented contractual rights for ArbiScout's actual internal purchase-research comparison and retention.
G. Technically affordable calls can sustain daily product-scale operation.
H. Independent cross-checks against eBay Product Research or another authoritative source succeed.
None of A–H establishes all others.

## Benchmark protocol (design mandatory; execution only on authorized credential/surface)

Create a 30-item stratified oracle sample: 10 common branded electronics/accessories, 10 toys/tools/appliances, 10 challenging variants/bundles/open-box/low-volume items. Use exact UPC/model+condition; document marketplace, date range and region. Query eBay Seller Hub Product Research **manually through delegated human interface** where permitted. For each third-party API compare up to 90d and if advertised up to 3y; sample size, unique listing IDs, raw sold prices, accepted-offer handling, median/p25/p75, timestamp and unmatched percent. Test: zero sales, one sale, 10+ sales, accepted-offer, different product revision, mixed lots, wrong condition, high shipping, region mismatch, API timeout, stale cache, removal, contradictory result. No anonymous website scrape benchmark without express permission; if live benchmark cannot run, provide executable benchmark plan, not false results.

Economic comparison: exact budget equation for 100 / 1,000 / 10,000 indexed product checks per day and cache policy; account for per-keyword request counts, pagination, 30 vs 90 days vs 3 years, batch, failed requests, quoted call limits and monthly quotas. Distinguish free *once* from recurring free monthly.

## Required ranked matrix and output

Provide a matrix for **every** avenue/candidate with:
`route_id, provider, primary URLs, currently supported historical price window, transaction-vs-asking evidence, actual accepted-best-offer treatment, product identity fields, shipping/condition/region fields, per-query max and pagination, observed or claimed refresh, coverage/selection bias, required signup/approval/API key, user/group eligibility, specific applicable clauses and status, storage/redistribution terms, free tier and paid price at observed date, usage scaling at 100/1k/10k per day, benchmark performed yes/no, evidence grade, principal failure mode, next verification, roadmap consumer, recommendation disposition`.

Classify source as `OFFICIAL_UI`, `OFFICIAL_RESTRICTED_API`, `OFFICIAL_ACTIVE_ONLY`, `RETIRED`, `THIRD_PARTY_VENDOR_CLAIM_UNTESTED`, `INDEPENDENTLY_VERIFIED`, `CATEGORY_SPECIFIC`, `MANUAL_ORACLE`, `INVALID_FOR_COMPLETED_SALES`, `UNRESOLVED`. Classify permissions independently: `EXPLICITLY_PERMITTED_SCOPED`, `TERMS_REVIEW_REQUIRED`, `UPSTREAM_PROVENANCE_UNVERIFIED`, `REQUIRES_VENDOR_APPROVAL`, `RESTRICTED`, `PROHIBITED_IN_CURRENT_FORM`.

Use ranked paths by **expected feasibility × evidence quality × data-rights confidence × operational cost × broad item coverage**, and separately by first usable manual canary vs daily scaled integration. Declare where the best route is a *conditional hypothesis* rather than a verified choice. Avoid false universal "no API exists": differentiate "no generally open first-party market-wide completed-sale API" from "no vendor or private partnership possible."

## Deliverables — a coherent single-worker return

Under a fresh authorized branch create:
1. `CONTROL_ROOM/WORKERS/RETURNS/ARB-010-EBAY-SOLD-HISTORY-R1/00_EXECUTIVE_VERDICT.md`: detailed provider-ranked verdict, path to first proof, why-not alternatives, honest unknowns.
2. `01_ROUTE_MATRIX.json`: schema-consistent machine-readable all-avenue matrix with dates, confidence and source refs.
3. `02_PRIMARY_EVIDENCE_DOCKET.md`: direct primary URLs, short quotation/field, exact support/limits, retrieved date, contradictions and if vendor marketing vs eBay authoritative.
4. `03_REQUIREMENTS_AND_COSTS.md`: each source's signup/eligibility, quota, plans, market/90d/3y support, data contracts and math at target daily volumes.
5. `04_INDEPENDENT_BENCHMARK_PROTOCOL.md`: stratified actual-price/condition matching, reproducibility and valid hold states; no fabricated test data.
6. `05_SOURCE_ADAPTER_CONTRACT.json`: proposed minimal per-sale fields (id, sold_at, actual_paid_price/ask_price and provenance separately, shipping, currency, GTIN/model/condition/lot, provider, query, fetch time, completeness) and rejection cases for `ARB-040`.
7. `06_ACCESS_AND_VENDOR_QUESTIONS.md`: specific written questions suitable for eBay developer support and leading vendors; DO NOT SEND.
8. `07_FULL_RETURN_AND_RECONCILIATION.md`: source changes, exact SHA/branch/test evidence, unresolved differences, impact on `ARB-010/011/012/013`, Q011/Q013–Q030, and recommended next flights. A source-backed return is not its own independent review.

DO NOT update canonical PROGRAMMA task states by inventing review acceptance, and do not merge. If authorized, open a separate draft PR to the verified control-room branch. If GitHub writes are unavailable, return all complete deliverables in the session and precise UNCOMMITTED status. Never output fabricated source proofs, screenshots or API calls.

## Independent review and stop

After worker returns, **ArbiScout HQ must commission independent hostile I3 examination** of the exact source refs, contradictory vendor claims, pricing math, eBay TOS/privacy assumptions and feasibility of a real first consumer. Worker cannot declare this review complete.
STOP on credentials requested, paid accounts/billing, vendor-only access, unverified runtime, prohibited automation, evidence claims relying only on marketing, contradictory upstream data authorization, or inability to access private content; document the missing gate precisely, continue other independent research branches.
Return `ENGINEERING`, `ECONOMIC_EVIDENCE` (here price-pattern/data-quality), and `AUTHORIZATION_PRIVACY` separate PASS/CONDITIONAL/HOLD/FAIL judgments with evidence limits.

**Launch compliance:** Present the full prompt as a single standalone launch, not merely an issue link. Merely committing this commission or opening an issue means PREPARED_NOT_LAUNCHED. User decides whether and where to start worker.
