# Acceptance thresholds

| ID | Required positive demonstration | Required negative/adversarial demonstration | Initial status |
|---|---|---|---|
| A01 | Retail feed expressly permits needed usage and retention | Advertising-only or denied scopes rejected | OPEN |
| A02 | Current retail purchase price/stock/region/identity confirmed | Expired, local-only, different seller, out-of-stock | OPEN |
| A03 | Exact GTIN+variant+condition matching and source | Similar-but-different bundle and used/new refused | DRAFT PR #1 |
| A04 | Actual completed sales, comparable price/time/sample, allowed data rights | Active asking prices, no sales, missing offers refused | BLOCKED |
| A05 | Current purchase condition accounts for full retailer acquisition terms, historical comparison window and uncertainty; optional fee/ROI analysis is separately validated if enabled | False markdown, incomplete checkout price and unjustified ROI promise | DRAFT optional finance PR #1 |
| A06 | Optional import track reports real delivered price, MOQ and lead-time uncertainty when enabled | Freight, currency, quality and MOQ surprises concealed | OPTIONAL / OPEN |
| A07 | Report ranks **no more than** ten verifiable candidates | Zero valid candidates yields truthful empty report | DRAFT |
| A08 | Scheduled authorized run with timestamp, errors, retries and no duplicate spend | Provider failure, stale state, repeated results | OPEN |
| A09 | Real retailer offer → historical eBay price-pattern comparison → purchasing-condition judgment → indexed report | Actual false-match and stale-evidence adversarial review | BLOCKED |
| A10 | Index reliability evaluated against real later product prices, freshness and observed bargain availability; optional sale profitability calibrated only if used | Stale/inaccurate price signals and false-bargain alerts | OPEN |
| A11 | No public secrets, least-privileged credential and data-retention model | Secret/privacy/access regression | OPEN |
| A12 | Exact SHA + separate engineering/economic/permission verdicts | Synthetic green masquerading as live access rejected | OPEN |

Separate **ENGINEERING**, **ECONOMIC_EVIDENCE**, **AUTHORIZATION_PRIVACY** outcomes. All three must be acceptable for a claimed live production integration. A test-only adapter cannot grant access rights. An unmerged PR cannot be claimed as canonical.
