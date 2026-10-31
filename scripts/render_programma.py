"""Render ArbiScout's purchase-gap PROGRAMMA from canonical JSON records.

Usage:
  python scripts/render_programma.py --write  # regenerate committed Markdown + CSV
  python scripts/render_programma.py --check  # fail if any generated view is stale
  python scripts/render_programma.py          # print dashboard to standard output

No network calls, accounts, purchases or provider scraping.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "CONTROL_ROOM" / "PROGRAMMA"
QUESTION_DIR = BASE / "QUESTIONS"
DONE = {"SETTLED", "SUPERSEDED"}


def load():
    work = json.loads((BASE / "01_WORK_REGISTRY.json").read_text(encoding="utf-8"))
    sources = json.loads((BASE / "02_SOURCE_REGISTRY.json").read_text(encoding="utf-8"))
    sections = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(QUESTION_DIR.glob("*.json"))]
    questions = [q for section in sections for q in section["items"]]
    return work, sources, sections, questions


def reach(rows, edges):
    """Number of distinct downstream nodes, not a probability or work-time forecast."""
    children = {r["id"]: set() for r in rows}
    for row in rows:
        for parent in edges(row):
            if parent in children:
                children[parent].add(row["id"])
    out = {}
    for key in children:
        seen = set()
        stack = list(children[key])
        while stack:
            item = stack.pop()
            if item == key or item in seen:
                continue
            seen.add(item)
            stack.extend(children[item] - seen)
        out[key] = len(seen)
    return out


def flat(value):
    return ", ".join(value) if value else "—"


def md(value):
    return str(value).replace("|", r"\|").replace("\n", " ").strip()


def table(headers, rows):
    return "\n".join([
        "| " + " | ".join(md(x) for x in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *["| " + " | ".join(md(x) for x in row) + " |" for row in rows],
        "",
    ])


def provider_gate(t):
    out = []
    for group in t.get("dependency_groups", []):
        out.append(group["type"] + "(" + ", ".join(group["task_ids"]) + ")")
    return "; ".join(out) if out else "—"


def source_link(ids, source_map):
    return ", ".join(
        "[" + sid + "](" + source_map[sid]["url"] + ")" if sid in source_map else sid
        for sid in ids
    ) or "—"


def csv_doc(headers, rows):
    f = io.StringIO(newline="")
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return f.getvalue()


def build():
    work, sources, sections, questions = load()
    tasks = work["tasks"]
    source_map = {s["id"]: s for s in sources["sources"]}
    task_map = {t["id"]: t for t in tasks}
    qmap = {q["id"]: q for q in questions}
    tr = reach(tasks, lambda x: (
        x["dependencies"]
        + x.get("acceptance_dependencies", [])
        + [v for g in x.get("dependency_groups", []) for v in g["task_ids"]]
    ))
    qr = reach(questions, lambda x: x["hard_dependencies"])
    task_headers = ["Task", "Priority", "State", "Actual capability", "Hard prerequisites (ALL)", "Alternative source (ANY)", "Live evidence gates", "Related, nonblocking", "Downstream reach", "Finding / blocker", "References"]
    task_rows = []
    for t in tasks:
        task_rows.append([
            t["id"], t["priority"], t["status"], t["title"],
            flat(t["dependencies"]), provider_gate(t), flat(t.get("acceptance_dependencies", [])),
            flat(t.get("related_tasks", [])), tr[t["id"]],
            t.get("finding") or t.get("blocker") or "Not recorded",
            source_link(t.get("source_ids", []), source_map),
        ])
    question_headers = ["Question", "Priority", "State", "Research / substantiation question", "Hard question prerequisites", "Work needed for operational proof", "Associated tasks (not blockers)", "Downstream questions", "Finding", "References"]
    question_rows = []
    for q in questions:
        question_rows.append([
            q["id"], q["priority"], q["status"], q["question"], flat(q["hard_dependencies"]),
            flat(q.get("proof_requires_tasks", [])), flat(q["related_tasks"]),
            qr[q["id"]], q.get("findings") or "Not recorded",
            source_link(q["source_ids"], source_map),
        ])
    source_headers = ["ID", "Provider / source", "Documented source", "Use/access state", "Recorded claim / limit", "Next verification"]
    source_rows = [[s["id"], s["title"], s["source_status"], s["rights_status"], s["claim"], s["next_probe"]] for s in sources["sources"]]

    task_title = "# PROGRAMMA — task dependencies and status\n\n**GENERATED** from `01_WORK_REGISTRY.json`. Do not edit this table directly. `ALL` means every hard prerequisite. `ANY` means one qualifying provider, not every named retailer. Live gates concern real-source acceptance, not whether source-free engineering can start. Related work is never a prerequisite.\n\n"
    question_title = f"# PROGRAMMA — {len(questions)} substantiation questions\n\n**GENERATED** from the seven `QUESTIONS/*.json` records. Hard question prerequisites govern what must be established to conclude a finding. `Work needed for operational proof` is not a requirement to delay documentary reconnaissance. Associated tasks are pointers, not dependencies.\n\n"
    task_md = task_title + table(task_headers, task_rows)
    q_md = question_title
    for section in sections:
        q_md += "## " + section["section"] + ". " + section["title"] + "\n\n"
        ids = {x["id"] for x in section["items"]}
        q_md += table(question_headers, [r for r in question_rows if r[0] in ids])
        q_md += "\n"

    task_counts = Counter(t["status"] for t in tasks)
    q_counts = Counter(q["status"] for q in questions)
    task_counts_str = ", ".join(f"{k}: {v}" for k, v in sorted(task_counts.items()))
    q_counts_str = ", ".join(f"{k}: {v}" for k, v in sorted(q_counts.items()))
    roots = [t for t in tasks if not t["dependencies"] and t["priority"] == "P0"]
    roots.sort(key=lambda t: (-tr[t["id"]], t["id"]))
    ready_questions = [
        q for q in questions if q["status"] not in DONE and q["priority"] == "P0"
        and all(qmap[x]["status"] in DONE for x in q["hard_dependencies"])
    ]
    ready_questions.sort(key=lambda q: (-qr[q["id"]], q["id"]))
    top_t = [[t["id"], t["title"], t["status"], tr[t["id"]],
              flat(t.get("acceptance_dependencies", [])), provider_gate(t)]
             for t in roots[:15]]
    top_q = [[q["id"], q["question"], q["status"], qr[q["id"]], flat(q["related_tasks"])]
             for q in ready_questions[:15]]
    dashboard = """# ArbiScout PROGRAMMA — operating dashboard

**Generated from canonical JSON.** This is an overview of research and implementation **states**, not a declaration of proven live commercial access. Governing scope: **purchase research only** — find retailer prices maximally below regular eBay completed-sale patterns for the identical product. No future selling model.

**Read:** [Constitution](../PRODUCT_CONSTITUTION.md) · [Full PROGRAMMA](00_PROGRAMMA_ARBISCOUT.md) · [Tasks table](TASKS_TABLE.md) · [question table](QUESTIONS_TABLE.md) · [Work JSON](01_WORK_REGISTRY.json) · [Question records](QUESTIONS/) · [Source JSON](02_SOURCE_REGISTRY.json) · [Current HQ](../STATUS/CURRENT_PROGRESS.md).

## Scope and counts

"""
    dashboard += f"- **{len(tasks)}** tracked capability tasks: {task_counts_str}.\n"
    dashboard += f"- **{len(questions)}** research/substantiation questions: {q_counts_str}.\n"
    dashboard += "- **Question dependency** = another conclusion needed first; **task hard prerequisite** = ALL; **source choice** = ANY ONE permitted source; **live evidence gate** = needed for real-world acceptance, not synthetic development.\n"
    dashboard += "- **Downstream reach** counts graph descendants and signals leverage, **not estimated effort, importance by itself, or proof of completion**. All `P0` items require judgment, not automatic worker dispatch.\n\n"
    dashboard += "## High-leverage independent P0 work tasks\n\n"
    dashboard += table(["Task", "What it establishes", "State", "Potential downstream", "Live evidence gates", "Alternative source gate"], top_t)
    dashboard += "\n## P0 research questions ready for independent investigation\n\n"
    dashboard += table(["Question", "Question to settle", "State", "Downstream questions", "Associated work"], top_q)
    dashboard += "\n## First terminal proof\n\n"
    dashboard += "**One actual purchase offer → exact product match → adequate eBay regular completed-sale baseline → conservative absolute and percentage gap → source-linked purchase-research index entry.** A zero-item day is valid when data are insufficient. No transaction, fees or other future operations are needed.\n\n"
    dashboard += "## Source-reference inventory\n\n"
    dashboard += table(source_headers, source_rows)
    dashboard += "\n## Maintenance\n\n"
    dashboard += "Edit JSON task/question/source records and log dated evidence; regenerate with `python scripts/render_programma.py --write` and validate with `python scripts/validate_programma.py`. CI checks the generated files. Status codes do not measure progress percentages.\n"
    return {
        "DASHBOARD.md": dashboard,
        "TASKS_TABLE.md": task_md,
        "QUESTIONS_TABLE.md": q_md,
        "TASKS_TABLE.csv": csv_doc(task_headers, task_rows),
        "QUESTIONS_TABLE.csv": csv_doc(question_headers, question_rows),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    args = p.parse_args()
    docs = build()
    if args.write:
        for name, content in docs.items():
            (BASE / name).write_text(content, encoding="utf-8")
            print("WROTE", name)
        return 0
    if args.check:
        bad = []
        for name, content in docs.items():
            path = BASE / name
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                bad.append(name)
        if bad:
            print("STALE generated PROGRAMMA views: " + ", ".join(bad))
            return 1
        print("PASS: generated PROGRAMMA views are current")
        return 0
    sys.stdout.write(docs["DASHBOARD.md"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
