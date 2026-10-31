# GitHub operation, branch fan-in and runtime

## Source of truth
`main` is canonical code/control plane only after an accepted merge. Isolated branches and draft PRs are proposals. The compact HQ CURRENT checkpoint is a **view**, while Programma's task/source registries and actual GitHub refs carry exact details. Never claim a status solely from a prior chat or stale memory.

## Changes and CAS discipline
1. Verify target branch, exact HEAD SHA and changed files at work start.
2. Use purpose-specific branch based on current actual canonical tip. Do not silently build on a draft unless that composition is deliberately commissioned.
3. Read before write; preserve unrelated modifications. Never use a stale SHA to overwrite another HQ/worker's changes.
4. Author atomic coherent changes with executable tests where possible.
5. Link worker/issue/original contract to PR; preserve exact test commands, output and expected result.
6. Independent review for high-stakes data/money/security claims.
7. Merge only under user-assigned rights, after current diff review, tests and no unexpected base changes.
8. Revisit Programma statuses, references, decision log, and checkpoint after accepted changes.
9. Mark `LIVE_CONSUMER_PROVED` only after actual end-to-end evidence at exact identity; do not conflate GitHub Actions green with data feed access.

## Test integrity
Adversarial tests should catch incorrect GTIN/variant, falsely sold listings, return/shipping costs, stale prices, missing fields, replays/duplicate offers, empty days, regional availability, API failures and provider rate limiting. Tests of mocked or synthetic data are valuable but only prove their local claims. No test can grant a vendor license.

## Access surfaces
- **S0:** browser or documentary read only.
- **S1:** connected GitHub/API/documentary write, without general local runtime.
- **S2:** verified local/CI runner, full source tree and safe tests.
- **S3:** live seller/retailer account execution with actual user grant, privacy, quota and merchant permission.

Do not assert local Mac or paid host access just because a tool is named; verify. No key in issue, code, PR diff or artifact. Use encrypted GitHub Actions secrets where supported and source-licensed.

## Worker flight
Maintain a small active-flight log, with exact statuses: `PREPARED`, `USER_DISPATCHED`, `RETURNED_UNREVIEWED`, `ACCEPTED_SCOPED`, `INTEGRATED`, `MERGED`. Avoid competing writers to same path. A queue of 40 issues is not evidence of 40 agents working.

## Anti-microfocus
Optimize for **one working evidence-to-report slice**, not 40 green YAML tests. A lack of legal access blocks only that live edge, not architecture or sourcefree ability. Do not build generic dashboards before a defensible real recommendation exists.
