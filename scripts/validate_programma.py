"""Validate the ArbiScout PROGRAMMA registry against its own stated evidence discipline.

Standard-library only; performs *structural checks*, not external factual or legal
verification. A PASS must never be represented as provider authorization.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "CONTROL_ROOM"
PATHS = {
    "work": BASE / "PROGRAMMA/01_WORK_REGISTRY.json",
    "sources": BASE / "PROGRAMMA/02_SOURCE_REGISTRY.json",
    "progress": BASE / "STATUS/CURRENT_PROGRESS.json",
}

SHA_LENGTH = 40


def check_registry() -> list[str]:
    errors: list[str] = []
    data = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in PATHS.items()}
    work, sources, progress = data["work"], data["sources"], data["progress"]

    tasks = work["tasks"]
    source_rows = sources["sources"]
    if not tasks or not source_rows:
        errors.append("program task and source registers must not be empty")
    tids = [r["id"] for r in tasks]
    sids = [r["id"] for r in source_rows]
    if len(set(tids)) != len(tids):
        errors.append("duplicate work item ID")
    if len(set(sids)) != len(sids):
        errors.append("duplicate source ID")
    ids, sid_set = set(tids), set(sids)
    statuses = set(work["status_vocabulary"])
    task_by_id = {t["id"]: t for t in tasks}
    for t in tasks:
        tid = t["id"]
        if t["status"] not in statuses:
            errors.append(f"{tid}: unknown status {t['status']}")
        if t["stage"] not in work["stages"] or t["level"] not in work["levels"]:
            errors.append(f"{tid}: invalid stage or level")
        for field in ("title", "required_capability", "first_consumer", "acceptance", "blocker", "next_action"):
            if not str(t.get(field, "")).strip():
                errors.append(f"{tid}: missing {field}")
        for dep in t["dependencies"]:
            if dep not in ids:
                errors.append(f"{tid}: unknown dependency {dep}")
            if dep == tid:
                errors.append(f"{tid}: self dependency")
        for sid in t["source_ids"]:
            if sid not in sid_set:
                errors.append(f"{tid}: unknown source id {sid}")
        for field in ("engineering_verdict", "economic_evidence_verdict", "authorization_verdict"):
            if field not in t:
                errors.append(f"{tid}: missing independent verdict {field}")
        if t["status"] in ("MERGED_MAIN", "LIVE_PROVED") and not t.get("implementation_ref"):
            errors.append(f"{tid}: cannot be merged/live without implementation ref")

    # Directed acyclic dependency graph, including all disconnected components.
    visited: set[str] = set()
    in_stack: set[str] = set()

    def visit(tid: str) -> None:
        if tid in in_stack:
            errors.append(f"cyclic dependency at {tid}")
            return
        if tid in visited:
            return
        in_stack.add(tid)
        for dep in task_by_id[tid]["dependencies"]:
            if dep in task_by_id:
                visit(dep)
        in_stack.remove(tid)
        visited.add(tid)

    for tid in tids:
        visit(tid)

    # Technical prerequisites, external live-evidence requirements, and alternative
    # provider choices are distinct. Do not turn ANY_OF into ALL_OF.
    for t in tasks:
        tid = t["id"]
        for dep in t.get("acceptance_dependencies", []):
            if dep not in ids or dep == tid:
                errors.append(f"{tid}: invalid live acceptance dependency {dep}")
        for dep in t.get("related_tasks", []):
            if dep not in ids or dep == tid:
                errors.append(f"{tid}: invalid nonblocking related task {dep}")
        for group in t.get("dependency_groups", []):
            if group.get("type") != "ANY_OF" or not group.get("task_ids"):
                errors.append(f"{tid}: invalid alternative-source group")
            for dep in group.get("task_ids", []):
                if dep not in ids or dep == tid:
                    errors.append(f"{tid}: invalid alternative source {dep}")
        if t.get("priority") not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"{tid}: invalid priority")
        active_text = t["title"] + " " + t["required_capability"]
        if re.search(r"\\b(?:roi|profit forecast|seller fees|resale profit|expected resale)\\b", active_text, re.I):
            errors.append(f"{tid}: old sale-focused requirement found in active work graph")

    questions = []
    for path in sorted((BASE / "PROGRAMMA/QUESTIONS").glob("*.json")):
        section = json.loads(path.read_text(encoding="utf-8"))
        questions.extend(section["items"])
    qids = [q["id"] for q in questions]
    expected_qids = {f"Q{i:03d}" for i in range(1, len(qids) + 1)}
    if set(qids) != expected_qids or len(qids) < 95:
        errors.append("PROGRAMMA questions must remain contiguous from Q001, unique, and retain the original 95")
    qmap = {q["id"]: q for q in questions}
    allowed_q_states = {"OPEN", "PARTIAL", "SETTLED", "SUPERSEDED", "DEFERRED", "DOCUMENTED"}
    for q in questions:
        qid = q["id"]
        if q["status"] not in allowed_q_states:
            errors.append(f"{qid}: invalid question status")
        if q["priority"] not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"{qid}: invalid question priority")
        if not q.get("question") or not q.get("acceptance"):
            errors.append(f"{qid}: missing question or proof standard")
        for dep in q["hard_dependencies"]:
            if dep not in qmap or dep == qid:
                errors.append(f"{qid}: invalid question prerequisite {dep}")
        for field in ("related_tasks", "proof_requires_tasks"):
            if field not in q:
                errors.append(f"{qid}: missing {field}")
            for dep in q.get(field, []):
                if dep not in ids:
                    errors.append(f"{qid}: unknown {field} task {dep}")
        for sid in q["source_ids"]:
            if sid not in sid_set:
                errors.append(f"{qid}: unknown reference {sid}")
    q_visited: set[str] = set()
    q_stack: set[str] = set()

    def visit_question(qid: str) -> None:
        if qid in q_stack:
            errors.append(f"question dependency cycle at {qid}")
            return
        if qid in q_visited:
            return
        q_stack.add(qid)
        for dep in qmap[qid]["hard_dependencies"]:
            if dep in qmap:
                visit_question(dep)
        q_stack.remove(qid)
        q_visited.add(qid)

    for qid in qids:
        visit_question(qid)

    if any(source in task_by_id["ARB-029"]["dependencies"] for source in
           ("ARB-022", "ARB-023", "ARB-024")):
        errors.append("ARB-029 must not hard-require all example retailers")
    if task_by_id["ARB-060"]["status"] == "PROTOTYPE_DRAFT":
        errors.append("old profit-ranked PR #1 cannot count as purchase-gap scoring")
    if "purchase" not in task_by_id["ARB-060"]["title"].lower() and "gap" not in task_by_id["ARB-060"]["title"].lower():
        errors.append("ARB-060 lost price-gap purchase-index mission")

    for s in source_rows:
        for field in ("title", "url", "claim", "rights_status", "source_status", "last_checked"):
            if not str(s.get(field, "")).strip():
                errors.append(f"{s['id']}: missing source field {field}")
        if not s.get("url", "").startswith("https://"):
            errors.append(f"{s['id']}: require an HTTPS locator")
        if s["source_status"] not in sources["status_vocab"]:
            errors.append(f"{s['id']}: invalid source status")
        if s["rights_status"] not in sources["rights_vocab"]:
            errors.append(f"{s['id']}: invalid rights status")
        if s["rights_status"] == "APPROVED_SCOPED" and not s.get("permission_evidence"):
            errors.append(f"{s['id']}: approved without exact permission receipt")

    if len(work["canonical_main_seed_sha"]) != SHA_LENGTH:
        errors.append("missing exact canonical main baseline SHA")
    if progress["main_seed_sha"] != work["canonical_main_seed_sha"]:
        errors.append("checkpoint/main baseline mismatch")
    if progress["control_room"]["branch"] != work["branch"]:
        errors.append("checkpoint/registry control branch mismatch")
    for flight in progress["flights"]:
        for tid in flight["task_ids"]:
            if tid not in ids:
                errors.append(f"flight {flight['id']}: unknown task {tid}")
        if flight["status"] == "USER_DISPATCHED" and not progress["active_workers"]:
            errors.append("flight dispatched but active worker roster empty")
    if progress["implementation"]["live_marketplace_integrations"] > 0 and all(
        t["status"] != "LIVE_PROVED" for t in tasks
    ):
        errors.append("claimed live integrations but no LIVE_PROVED task")
    return errors


def main() -> int:
    problems = check_registry()
    if problems:
        for problem in problems:
            print("FAIL", problem)
        return 1
    print("PASS: PROGRAMMA structural validation; NOT live data or legal approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
