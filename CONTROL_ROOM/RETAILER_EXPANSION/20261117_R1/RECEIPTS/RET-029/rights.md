# RET-029 LEGO rights and capture receipt — 2026-11-17

- **Treatment status:** FIXTURE_VALIDATED (not LIVE_VALIDATED)
- **Access gate:** TERMS_REVIEW_NEEDED
- **Robots:** LEGO robots.txt allowed the sales-and-deals path at capture time.
- **Capture:** One local read-only HTTP GET of https://www.lego.com/en-us/categories/sales-and-deals; no pagination, product-page crawl, sign-in or checkout.
- **Raw HTML:** local only; SHA-256 `9c1726178de633da4453a47c244f615e672aef469b6f3078f8ce2e2ad15c174b`; 1,174,608 bytes.
- **Parsed sets:** 18 sale sets; 18 with current and list reference.
- **Blocker:** LEGO terms, permitted purpose, retention and redistribution are unresolved. listPrice is a vendor reference, not a paid price. Set identity is strong; GTIN is not captured.
- **Next action:** obtain rights review and confirm pagination/set completeness before any LIVE_VALIDATED or production claim.
- **Review:** NOT_REVIEWED.
