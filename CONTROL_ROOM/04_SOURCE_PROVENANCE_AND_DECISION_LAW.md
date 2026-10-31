# Evidence, contracts, identity, and temporal law

## Facts vs interpretations
A claim requires `source_id`, source URL or protected document locator, observation/capture date, verbatim relevant passage or exact parameter names, product/operation scope, claimant, and confidence level. Record a source's *published* vs *last checked* date separately. Do not cite generic developer landing pages as proof of personal approval. Unverified source clauses receive `NEEDS_VERIFICATION`.

**Source presence ≠ credential ownership ≠ account eligibility ≠ permission for this use ≠ completeness ≠ operational reliability**. Similarly, candidate price ≠ verified checkout price ≠ GTIN match ≠ sold demand ≠ realized profit.

## Contract analysis
Always separate:
1. Normal individual purchases for one's own resale inventory.
2. Browsing publicly displayed pages and individual research.
3. API contract for scripted commercial analysis, reuse/retention, combined market comparisons.
4. Site automation and extraction rights.
5. Selling-policy compliance after inventory is owned.

Scale can change enforcement/rate-limit risk but does not create a license exemption. Interpret actual clause rather than labeling all resale "illegal". Where ambiguous, say `NOT_CLEARLY_AUTHORIZED`, list competing readings, and seek written clarification instead of inventing counsel.

## Data quality
For retail offer: brand/model, GTIN/MPN, variant, bundle quantity, condition, seller, offer region/ZIP, time seen, checkout price, stock, shipping, coupons and tax. Third-party marketplace offers are not necessarily retailer-owned listings.
For eBay evidence: exact match, sold/completed—not merely listed—count/window, actual net sold-price distribution where lawful, accepted offers, shipping inclusion, market competition, timestamp, sampling coverage and exclusions. Unknown sold-price evidence cannot be silently substituted by active asking prices.
For imports: MOQ, total landed cost, freight mode, duty/fees, currency, lead-time distribution, supplier/quality/counterfeit risk, returns, regulatory compliance, capital lock-up.
For financial model: category-dependent fee base, promoted listing, tax (jurisdiction/user basis), returns, damaged/unsellable risk, shipping size/weight, storage and throughput. Distinguish assumptions and observations, use Decimal.
For ranking: permit zero qualified results; never label a heuristic as statistically calibrated demand probability.

## Status and references
Each program task references source IDs and exact artifact SHAs, plus claim status. An old positive result does not prevail automatically over newer live evidence; a newer document does not automatically supersede a validated older one. When material result changes, update SOURCE_REGISTRY, task node, decision log and current checkpoint together **on one reviewable branch**.

## Source rights ceiling
A commercial price-data vendor may advertise white-label use; still verify contract, sublicensing, retention and whether underlying source terms constrain intended use. Never solve permission problems by stealth automation, CAPTCHA avoidance, rate-limit evasion or hidden cookies.

## Privacy and public repo
This repo is PUBLIC. Source registry should contain only publicly safe URLs and excerpts. Keep credentials, permissions grants, private account details, customer data, provider contract correspondence, and research datasets with use restrictions OUTSIDE Git until private authorized storage exists.
