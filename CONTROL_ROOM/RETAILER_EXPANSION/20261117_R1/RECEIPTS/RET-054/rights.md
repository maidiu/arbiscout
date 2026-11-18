# RET-054 Dell rights and capture receipt — 2026-11-17

- **Treatment status:** FIXTURE_VALIDATED (not LIVE_VALIDATED)
- **Access gate:** TERMS_REVIEW_NEEDED
- **Robots:** Dell robots.txt allowed the Top Deals path at the time of capture.
- **Capture:** One local read-only HTTP GET of https://www.dell.com/en-us/shop/deals/dc; no pagination, product-page crawl, sign-in or checkout.
- **Raw HTML:** local only; SHA-256 `282354b2a263f37db709cc76a0f9251c42799df04887be5f0c63d722e783bf4c`; 2,137,332 bytes.
- **Parsed offers:** 36 embedded products; 34 with a current and market reference; 2 current-only.
- **Blocker:** Dell terms, permitted purpose, retention and redistribution are unresolved. marketPrice is a vendor reference, not a paid price. Configuration/GTIN identity is not independently verified.
- **Next action:** obtain rights review and exact configuration/GTIN evidence before any LIVE_VALIDATED or production claim.
- **Review:** NOT_REVIEWED.
