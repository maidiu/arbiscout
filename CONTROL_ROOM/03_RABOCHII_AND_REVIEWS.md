# Rabochii — scoped commissions, evidence returns, review and integration

## Dispatch law
Write one **complete standalone copy-paste prompt per worker**, both in a GitHub commission artifact and user-visible reply (no issue-only launch). The user selects the actual editor/model/host; no automatic account switches. Before launch name **AGENT_TYPE**, **INTELLIGENCE_LEVEL** (I0 mechanical, I1 bounded, I2 contested engineering/evidence, I3 conceptual/architectural), **S0** source-only, **S1** connected limited execution, **S2** verified local Git runner, or **S3** external live account (never presumed). Include **REPOSITORY, BRANCH, EXACT_STARTUP_SHA, model/editor/effort/availability, scope, exclusions, finished artifact and first consumer, tests, return schema, review owner, stop conditions, budget and safety**. A GitHub issue/prompt is only **PREPARED**, never automatically LAUNCHED.

Route economically: Browser with actual connector read/commit capabilities if sufficient → local worker with verified editor/model and max effort for full task if necessary → high-cost execution only on a demonstrated need. User remains model chooser. Avoid interrupting existing workers; reuse warm qualified environments, prefer one coherent outcome/owner loop.

## Worker types
- **Reconnaissance:** source documentation, product-market candidate research, TOS/access evaluation, competitor code audit; no credentials.
- **Engineer:** source-free code, tests, sanctioned live adapters on isolated branch; cannot grant source permissions.
- **Hostile reviewer:** adversarial inspection of exact independent SHA/claim; cannot review own changes.
- **Integrator:** combine already returned/accepted code on authorized branch, preserving provenance and no silent merge.

## Return schema
Use `WORKERS/RETURN_SCHEMA.json` as a minimal field vocabulary. Include original question, exact branch/startup/final SHA, relevant files, evidence direct links/quotes and observation date, actual command and CI URL where executed, positive and adversarial tests, independent limits, changed assumptions and consumer check, unresolved/blocked paths, evidence-rights distinction, recommendation and why-not, and separately typed engineering/economic/authorization dispositions. **No generated confidence number substitutes for missing proof.**

## Return intake / fan-in
`DISPATCHED` → `RETURNED_UNADJUDICATED` → `REVIEW_PENDING` → `ACCEPTED_SCOPED` or `REJECTED/HOLD` → `INTEGRATED_BRANCH` → `MERGED_MAIN` → `LIVE_CONSUMER_PROVED`. Preserve exact SHAs and distinct source/implementation/consumer states; do not overclaim live status from green fixtures.

If two rounds yield no useful delta, diagnose missing data permission, bad test oracle, absent runtime, mistaken architecture or wrong scope. Do not multiply identical workers. An independent review should cover a coherent deliverable and return all material defects together.

## Commission file naming
`WORKERS/COMMISSIONS/ARB-<task-id>-<purpose>-R1.md`; completed returns `WORKERS/RETURNS/ARB-.../00_RETURN.md` with evidence. **No commissions have been launched by creating this constitution.**

## Three-court acceptance
Each return is graded separately: **ENGINEERING**, **ECONOMIC_EVIDENCE**, **AUTHORIZATION_PRIVACY**. An authorization HOLD is never converted into an engineer's code PASS. Work behind an unresolved legal gate may be implemented using synthetic fixtures only, not live keys.
