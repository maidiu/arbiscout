# ARB-010 R1 — Executive verdict and decision court
**Observed:** 2026-10-31. **Status:** RETURNED_UNADJUDICATED; documentary source research only. No authenticated provider access, paid test, official Product Research benchmark, production adapter, or independent review.
**Repository:** https://github.com/maidiu/arbiscout ; inherited control-plane head `64ae2a67bb13dca0a0711409651e41a55c8917cb`. This work belongs to an isolated branch, not the unmerged PR #2 or main.

## Terminal determination
**There is no established all-green, open-access, market-wide, transaction-true, permitted and economical automated eBay historical sales feed for a new ArbiScout application.** The most authoritative historical reference is **eBay Seller Hub Product Research**: up to three years, including eBay's actual accepted Best Offer values, searchable with UPC/MPN and other identifiers. Its documented entitlement is human Seller Hub research; neither a generally available machine-readable Product Research API nor a qualified bulk-export right was substantiated.

For the *first machine-readable experiment*, trial **CompsAPI** first (transparent tier economics, 1y/3y claims, an identifiable `/v1/sold` endpoint and explicit vendor-side right to retain and derive statistics) and **CompSniper** independently as a high-priority adversarial comparator (separate 90d `/v1/scrape` and 3y listing-level `/v1/research/sold`). **Do not endorse either as production** until actual paid-price fidelity, query coverage and underlying authorization are confirmed. CompsAPI's terms explicitly decline assurances about third-party rights; CompSniper's own August 2026 terms call Best Offer values upper bounds even though October 2026 marketing calls them actual paid amounts.

If these fail, test **SoldComps** (optional offer-price hydration), **eBay Sold Listings API** (distinct accepted-price status; claimed logged-in retrieval increases authorization risk), and **Trawl** (multi-year stored archive but Best Offer values are often asking-price upper bounds). **Soldgraph** is useful as a transparency/negative control because it documents that accepted-offer headline values are NOT actual paid prices; raw all-sale medians from it cannot qualify without excluding or separately resolving those rows.

## Four distinct winners
1. **Official reference / oracle:** eBay Product Research via permitted seller human interface or properly delegated Team Access. Manual pilot is feasible at tens of exact products, not a 10,000-product daily feed. Document actual account entitlement, UI date/marketplace selectors and manually captured aggregate evidence; seek specific retention/derivative-use permission where necessary.
2. **Machine-readable candidate:** CompsAPI, **conditional, not an acceptance**. Evidence: documented endpoint, dated vendor terms/pricing, multi-year option and vendor-side right to derived internal use. Missing: independent row truth, source-level eBay permission, completeness and exact-model fidelity.
3. **Lowest-cost multi-provider evaluation:** free or low-cost authorized key tests only *after* terms, data rights and user-approved signups; current no-key reference case is manual Product Research. CompsAPI free 100 monthly, CompSniper free 100 monthly, SoldComps free 100 monthly, Trawl free 250 monthly, eBay Sold Listings API free 50 monthly, Soldgraph free 100 **one-time** for new accounts. Free trials do not authorize hidden scraping, account delegation or benchmark claims.
4. **Long-term:** source-neutral, typed, refusal-capable `ARB-040` sale-observation adapter + `ARB-051` robust historical reference; contractually approved official eBay partnership preferred if available, otherwise independently benchmarked and permitted vendor feed, a second validated vendor as fallback, and manual Product Research audit/calibration. Enforce actual-paid-price provenance rather than silently treating offer upper bounds as realized prices.

## Route ordering for a **new** application
| Priority | Route | True sale evidence | Entry/use burden | Daily 100 / 1k / 10k sustainability | Decision |
|---|---|---|---|---|---|
| 1 manual | eBay Product Research | Official actual accepted offers, 3y | Seller Hub eligibility; manual, no demonstrated API | Manual 100 possible with labor; 1k/10k impractical | **AUTHORITATIVE MANUAL ORACLE** |
| 1 machine test | CompsAPI | Vendor's 1y/3y paid-price claims untested | Key + source provenance/contract clarification | Pricing models cover 100, 1k; 10k needs quote | **CONDITIONAL EVALUATE** |
| 2 independent test | CompSniper | Recent/archival split; terms contradict offer claims | Key + resolve August terms/October claim | Published plans span all three, multi-page scaling uncertain | **CONDITIONAL EVALUATE** |
| 3 | SoldComps | Optional hydration, not guaranteed | Key + hydration coverage/cost permission | Tiers published, per-page & hydration multiplication | **CONDITIONAL EVALUATE** |
| 4 | eBay Sold Listings API | Claimed accepted price status; soldPrice is ask on offers | Key, signed-in extraction provenance permission | $299 claimed fair-use unlimited, actual throttle unknown | **HOLD DATA RIGHTS** |
| 5 | Trawl | Archive but many accepted offers are asking bounds | Key, category/coverage check | Published through 200k credits; 300k+ quote | **CONDITIONAL SPECIALIST** |
| 6 | Soldgraph | Explicitly admits wrong offer headline price | Key, page-only completeness | Published tiers span volume | **NEGATIVE CONTROL / SUBSET ONLY** |
| Strategic | eBay Marketplace Insights | Official 90d sold data | Limited Release, whitelist; **not open to new users** | Pricing/access unknown | **HOLD NEW ENTITLEMENT** |
| Strategic | eBay negotiated rights/feed | Potential first-party complete data; **not established** | Written bespoke business/data agreement | Unknown | **INQUIRE, DON'T ASSUME** |
| Reject | Browse/Feed/Marketing/Trading/Sell/Finding/Shopping | Active, aggregate, own-sale only, or retired | Irrelevant | Not legitimate historical producer | **NOT ARB-010 SOLUTION** |
| Hold | WorthPoint, ZIK, ShelfTrend, 130point, PriceCharting, scraping actors | Specialist UI, no proven broad row API; PriceCharting explicitly excludes historic sales | Commercial/automation rights absent | Not established | **NO GENERIC HISTORY INTEGRATION** |

## What changes the verdict?
The vendor must supply **individual, exact-product, completed-sale observations with unambiguous actual paid price (or honest price type), sold time, sufficient quantity/condition/shipping/site details and defensible window coverage**. Two independent needs remain:
- **Epistemic:** 30-item official-oracle audit across accepted offers, variants, bundles, 90d/3y, sparse or stale queries; row-level IDs, record-count and median/p25/p75 comparison. Do not mistake a successful HTTP response or marketing screenshot for truth.
- **Authorization:** written provider permission for ArbiScout's actual retailer *purchase-research index*, retention and derived-price publication, with verifiable eBay upstream entitlement or a satisfactory authorized provenance explanation. Vendor's licence for its own output cannot cure absent upstream authorization.

## Specific next flight, without accounts/payments now
(A) Confirm official Product Research access and authorized 30 manual oracle cases (Team Access if needed; no password or private account in public repo); (B) send **drafted, not sent** written questions to eBay data partnership and CompsAPI/CompSniper/SoldComps; (C) engineer source-neutral adapter with synthetic typed prices and explicit rejection; (D) seek user authorization for a bounded, separately paid/live trial only once scope/right/price are known; (E) run independent third-party comparison and hostile review of evidence/contract, then choose producer and deploy a first real `ARB-040 → ARB-051 → purchase-gap report` consumer.

Do not resurrect deprecated `findCompletedItems` (Finding and Shopping APIs decommissioned 2025-02-04); do not use Browse/Feed active offers as sale prices; do not automate Product Research UI without express permission; do not model later selling operations. A **zero-candidate** index day is correct if reference evidence is missing.

## Three independent return judgments (not independent acceptance)
- **ENGINEERING: CONDITIONAL** — workable source-neutral contract specified, but no adapter implemented or integrated and no production calls.
- **ECONOMIC_EVIDENCE: HOLD** — tier arithmetic can be done; real actual-paid accuracy, coverage, all-in per-product calls and adequacy of ordinary price estimator remain untested.
- **AUTHORIZATION_PRIVACY: HOLD** — no eBay or vendor-specific verified use grant, no upstream license, no credential disclosure. Public documentary reading does not authorize production data acquisition.

**First consumer:** ARB-040 individual observations → ARB-051 normal historical price baseline → ARB-050/060 purchase-gap indexing. No anticipated later sale, fee, ROI or profit.
