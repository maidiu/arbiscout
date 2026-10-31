# Worker commission and return space

Worker artifacts are prepared scopes, not autonomous tasks. A worker is **launched only when the user actually dispatches it** in the selected editor/model/host.

- [Commission template](COMMISSION_TEMPLATE.md).
- [Structured return schema](RETURN_SCHEMA.json).
- [HQ review and fan-in law](../03_RABOCHII_AND_REVIEWS.md).

Naming: `COMMISSIONS/ARB-<task-id>-<scope>-R1.md`, `RETURNS/ARB-<task-id>-<scope>-R1/00_RETURN.md`. Link exact branch and startup SHA, first consumer and proof thresholds. One complete copy-paste launch per worker, never a mere pointer.
