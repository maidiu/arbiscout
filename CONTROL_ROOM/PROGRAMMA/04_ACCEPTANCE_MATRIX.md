# Acceptance thresholds

| ID | Required positive demonstration | Required negative/adversarial demonstration | Initial status |
|---|---|---|---|
| A01 | Retail feed expressly permits needed usage and retention | Advertising-only or denied scopes rejected | OPEN |
| A02 | Current retail purchase price/stock/region/identity confirmed | Expired, local-only, different seller, out-of-stock | OPEN |
| A03 | Exact GTIN+variant+condition matching and source | Similar-but-different bundle and used/new refused | DRAFT PR #1 |
| A04 | Actual completed sales, comparable price/time/sample, allowed data rights | Active asking prices, no sales, missing offers refused | BLOCKED |
| A05 | Fees, shipping, taxes, reserve and ROI independently checked | High asking-price spread but negative real margin | DRAFT PR #1 |
| A06 | Import landed unit cost and lead-time uncertainty | MOQ/duties/quality/safety kill false import deals | OPEN |
| A07 | Report ranks **no more than** ten verifiable candidates | Zero valid candidates yields truthful empty report | DRAFT |
| A08 | Scheduled authorized run with timestamp, errors, retries and no duplicate spend | Provider failure, stale state, repeated results | OPEN |
| A09 | Real provider→evidence→profit→human report and review | Actual false-match test by separate reviewer | BLOCKED |
| A10 | Realized purchase/sale receipts validate profit/time forecast | Returns, unsold stock, loss-making items | OPEN |
| A11 | No public secrets, least-privileged credential and data-retention model | Secret/privacy/access regression | OPEN |
| A12 | Exact SHA + separate engineering/economic/permission verdicts | Synthetic green masquerading as live access rejected | OPEN |

Separate **ENGINEERING**, **ECONOMIC_EVIDENCE**, **AUTHORIZATION_PRIVACY** outcomes. All three must be acceptable for a claimed live production integration. A test-only adapter cannot grant access rights. An unmerged PR cannot be claimed as canonical.
