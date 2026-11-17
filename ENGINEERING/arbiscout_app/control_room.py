#!/usr/bin/env python3
"""ArbiScout control room: one local browser UI for every source and report.

Runs on 127.0.0.1 only. It starts the existing scripts as subprocesses, streams
their output to status cards, and launches the catalog/capture consoles.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import webbrowser
from urllib.parse import parse_qs, urlparse

APP_DIR = Path(__file__).resolve().parent
ENV_PATH = APP_DIR / ".env"
LOG_DIR = APP_DIR / "control_room_logs"
PY = sys.executable

JOBS = {
    "bestbuy": {"label": "Best Buy", "status": "idle", "started": None, "finished": None, "log": []},
    "meh": {"label": "Meh", "status": "idle", "started": None, "finished": None, "log": []},
    "woot": {"label": "Woot", "status": "idle", "started": None, "finished": None, "log": []},
    "kroger": {"label": "Kroger", "status": "idle", "started": None, "finished": None, "log": []},
    "catalog": {"label": "Build catalog", "status": "idle", "started": None, "finished": None, "log": []},
    "everything": {"label": "Update everything", "status": "idle", "started": None, "finished": None, "log": []},
}
LOCK = threading.RLock()
ACTIVE_JOB = None
CATALOG_PROC = None
WATCHER_PROC = None


def read_env(path=ENV_PATH):
    values = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[7:].strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


def load_env():
    for key, value in read_env().items():
        os.environ.setdefault(key, value)


def write_env(updates, clears=(), path=ENV_PATH):
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    seen = set()
    out = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            out.append(line)
            continue
        key = line.split("=", 1)[0].strip()
        if key.startswith("export "):
            key = key[7:].strip()
        if key in clears:
            continue
        if key in updates:
            out.append(f"{key}={updates[key]}")
            seen.add(key)
        else:
            out.append(line)
    for key, value in updates.items():
        if key not in seen and key not in clears:
            out.append(f"{key}={value}")
    path.write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    for key, value in updates.items():
        if key in clears:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def append_log(job_id, line):
    line = line.rstrip("\n")
    with LOCK:
        job = JOBS[job_id]
        job["log"].append(line)
        job["log"] = job["log"][-500:]
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with (LOG_DIR / f"{job_id}.log").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def set_status(job_id, status):
    with LOCK:
        JOBS[job_id]["status"] = status
        if status == "running":
            JOBS[job_id]["started"] = now()
            JOBS[job_id]["finished"] = None
        elif status in ("success", "failed", "skipped"):
            JOBS[job_id]["finished"] = now()


def command_for(job):
    env = read_env()
    if job == "bestbuy":
        return [PY, "run_test.py", "--url", env.get("BESTBUY_URL") or "https://www.bestbuy.com/black-friday",
                "--mode", "browser", "--browser-visible", "--timeout", "60", "--delay", "2",
                "--output", "bestbuy_live"]
    if job == "meh":
        return [PY, "providers.py", "--source", "meh", "--output", "meh_live"]
    if job == "woot":
        return [PY, "providers.py", "--source", "woot", "--feed", env.get("WOOT_FEED") or "All",
                "--max-products", env.get("WOOT_MAX") or "500", "--output", "woot_live"]
    if job == "kroger":
        command = [PY, "providers.py", "--source", "kroger",
                   "--terms", env.get("KROGER_TERMS") or "milk,eggs,bread",
                   "--limit", "50", "--max-products", "500", "--output", "kroger_live"]
        if env.get("KROGER_LOCATION_ID"):
            command += ["--location-id", env["KROGER_LOCATION_ID"]]
        elif env.get("KROGER_ZIP"):
            command += ["--zip", env["KROGER_ZIP"]]
        return command
    if job == "catalog":
        return [PY, "build_catalog.py", "--output", "catalog"]
    return None


def run_process(job_id, command, prefix=""):
    proc = subprocess.Popen(command, cwd=APP_DIR, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in proc.stdout or []:
        append_log(job_id, (prefix + line).rstrip())
    return proc.wait()


def run_single(job_id):
    try:
        command = command_for(job_id)
        if not command:
            append_log(job_id, "No command for this job.")
            set_status(job_id, "failed")
            return
        append_log(job_id, "$ " + " ".join(command))
        code = run_process(job_id, command)
        set_status(job_id, "success" if code == 0 else "failed")
        append_log(job_id, f"Finished with exit code {code}.")
    except Exception as exc:
        append_log(job_id, f"ERROR: {exc}")
        set_status(job_id, "failed")


def run_everything():
    try:
        env = read_env()
        steps = [("bestbuy", "Best Buy")]
        if env.get("MEH_API_KEY"):
            steps.append(("meh", "Meh"))
        else:
            append_log("everything", "Skipping Meh: MEH_API_KEY is not set.")
        if env.get("WOOT_API_KEY"):
            steps.append(("woot", "Woot"))
        else:
            append_log("everything", "Skipping Woot: WOOT_API_KEY is not set.")
        if env.get("KROGER_CLIENT_ID") and env.get("KROGER_CLIENT_SECRET") and (env.get("KROGER_ZIP") or env.get("KROGER_LOCATION_ID")):
            steps.append(("kroger", "Kroger"))
        else:
            append_log("everything", "Skipping Kroger: client credentials or ZIP/location are not set.")
        failed = False
        for job_id, label in steps:
            append_log("everything", f"=== {label} ===")
            command = command_for(job_id)
            if not command:
                continue
            append_log("everything", "$ " + " ".join(command))
            code = run_process("everything", command, prefix=f"[{label}] ")
            if code != 0:
                failed = True
                append_log("everything", f"{label} failed with exit code {code}; continuing.")
        append_log("everything", "=== Catalog ===")
        code = run_process("everything", command_for("catalog"), prefix="[Catalog] ")
        if code != 0:
            failed = True
        set_status("everything", "failed" if failed else "success")
    except Exception as exc:
        append_log("everything", f"ERROR: {exc}")
        set_status("everything", "failed")


def start_job(job_id):
    global ACTIVE_JOB
    with LOCK:
        if ACTIVE_JOB:
            return False, f"{ACTIVE_JOB} is already running."
        ACTIVE_JOB = job_id
        JOBS[job_id]["log"] = []
        set_status(job_id, "running")
    target = run_everything if job_id == "everything" else (lambda: run_single(job_id))
    def worker():
        try:
            target()
        finally:
            global ACTIVE_JOB
            with LOCK:
                ACTIVE_JOB = None
    threading.Thread(target=worker, daemon=True).start()
    return True, "Started."


def start_server(args, log_name, pattern, timeout=10):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / log_name
    log_path.write_text("", encoding="utf-8")
    proc = subprocess.Popen([PY] + args, cwd=APP_DIR, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
    def reader():
        with log_path.open("a", encoding="utf-8") as handle:
            for line in proc.stdout or []:
                handle.write(line)
                handle.flush()
    threading.Thread(target=reader, daemon=True).start()
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        text = log_path.read_text(encoding="utf-8", errors="replace")
        match = re.search(pattern, text)
        if match:
            return proc, match.group(0)
        if proc.poll() is not None:
            break
        time.sleep(0.2)
    proc.terminate()
    return None, log_path.read_text(encoding="utf-8", errors="replace")[-800:]


def ensure_catalog():
    global CATALOG_PROC
    if CATALOG_PROC and CATALOG_PROC.poll() is None:
        return None, "http://127.0.0.1:8770/"
    if not (APP_DIR / "catalog" / "catalog.json").is_file():
        return None, "No catalog yet. Run Build catalog or Update everything first."
    proc, result = start_server(
        ["catalog_server.py", "--catalog", "catalog", "--output", "catalog",
         "--port", "8770", "--no-open"],
        "catalog_server.log", r"http://127\.0\.0\.1:\d+/")
    if not proc:
        return None, "Catalog server failed to start:\n" + result
    CATALOG_PROC = proc
    return proc, result


def ensure_watcher():
    global WATCHER_PROC
    if WATCHER_PROC and WATCHER_PROC.poll() is None:
        return None, "http://127.0.0.1:8765/"
    selected = APP_DIR / "catalog" / "selected" / "retailer" / "products.json"
    output = None
    keep = False
    if selected.is_file():
        output = "catalog/selected"
        keep = True
    else:
        for candidate in ("bestbuy_live", "woot_live", "meh_live", "kroger_live"):
            if (APP_DIR / candidate / "retailer" / "products.json").is_file():
                output = candidate
                break
    if not output:
        return None, "No retailer products yet. Run a source first."
    args = ["ebay_watcher.py", "--folder", "ebay_saved", "--output", output,
            "--port", "8765", "--no-open"]
    if keep:
        args.append("--keep-selection")
    proc, result = start_server(args, "ebay_watcher.log", r"http://127\.0\.0\.1:\d+/")
    if not proc:
        return None, "Capture console failed to start:\n" + result
    WATCHER_PROC = proc
    return proc, result


HOME = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ArbiScout control room</title><style>
:root{color-scheme:light;font:14px system-ui,-apple-system,Segoe UI,sans-serif;color:#172333;background:#f3f5f8}
*{box-sizing:border-box}body{margin:0}header{background:#0c2544;color:#fff;padding:24px max(20px,calc((100vw - 1200px)/2))}
header h1{margin:0;font-size:27px}header p{color:#c1d5ea;margin:6px 0 0;font-size:13px}
.wrap{max-width:1200px;padding:20px;margin:auto}.top{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 16px}
button,.btn{display:inline-block;padding:10px 15px;border-radius:9px;border:0;background:#1261bd;color:#fff;font-weight:650;text-decoration:none;cursor:pointer;font-size:13px}
.btn.alt{background:#fff;color:#17508d;border:1px solid #b9cce2}.btn.big{font-size:16px;padding:14px 22px;background:#0b7a53}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:15px}
.card h3{margin:0 0 8px;font-size:16px;display:flex;justify-content:space-between;gap:8px;align-items:center}
.badge{font-size:11px;padding:3px 8px;border-radius:999px;background:#eaf0f8;color:#31506f;font-weight:700;text-transform:uppercase}
.badge.running{background:#fff4df;color:#9a630e}.badge.success{background:#e6f5ee;color:#0b7a53}.badge.failed{background:#fdecec;color:#a33}
.badge.skipped{background:#eef2f6;color:#64748b}
.card p{color:#536071;font-size:12px;line-height:1.4;margin:6px 0}
pre{white-space:pre-wrap;background:#f6f8fa;border-radius:7px;padding:9px;max-height:150px;overflow:auto;font-size:11px;margin:8px 0 0}
.note{background:#fff9e6;border:1px solid #f1d38d;border-radius:9px;padding:11px 14px;color:#644a1a;font-size:13px;margin:14px 0}
.footer{color:#738197;font-size:12px;margin-top:20px}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
</style></head><body>
<header><h1>ArbiScout <span style="font-weight:400;color:#97bce7">/ control room</span></h1>
<p>Everything runs locally. No terminal needed after launch.</p></header>
<main class="wrap">
<div class="top">
  <button class="btn big" data-job="everything">Update everything</button>
  <a class="btn alt" href="/catalog" target="_blank">Open catalog</a>
  <a class="btn alt" href="/capture" target="_blank">Capture eBay</a>
  <a class="btn alt" href="/reports/top10" target="_blank">Top 10 report</a>
  <a class="btn alt" href="/reports/comparisons" target="_blank">All comparisons</a>
  <a class="btn alt" href="/settings">Settings</a>
</div>
<div class="note">eBay sold pages are still saved by you in the browser; the capture console watches your Downloads and ebay_saved folders. Gaps are gross; fees, shipping and net margin are not included.</div>
<div class="grid" id="cards"></div>
<div class="footer">Local only · 127.0.0.1 · no keys are shown in this page.</div>
</main>
<script>
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
let active=null;
async function poll(){
  try{const r=await fetch('/api/status',{cache:'no-store'});const s=await r.json();active=s.active;render(s.jobs);}catch(e){}
}
function render(jobs){
  $('cards').innerHTML=Object.entries(jobs).map(([id,j])=>`<div class="card"><h3>${esc(j.label)} <span class="badge ${esc(j.status)}">${esc(j.status)}</span></h3>
    <p>${j.started?'Started '+esc(j.started):'Not run yet.'}${j.finished?' · finished '+esc(j.finished):''}</p>
    <button class="btn alt" data-job="${esc(id)}" ${active?'disabled':''}>Run ${esc(j.label)}</button>
    <pre>${esc((j.log||[]).slice(-12).join('\n')||'No output yet.')}</pre></div>`).join('');
  document.querySelectorAll('[data-job]').forEach(b=>b.onclick=()=>run(b.dataset.job));
}
async function run(job){
  const r=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({job})});
  const j=await r.json();if(j.error)alert(j.error);poll();
}
document.querySelectorAll('[data-job]').forEach(b=>b.onclick=()=>run(b.dataset.job));
poll();setInterval(poll,2000);
</script></body></html>"""


SETTINGS = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ArbiScout settings</title><style>
:root{color-scheme:light;font:14px system-ui,-apple-system,Segoe UI,sans-serif;color:#172333;background:#f3f5f8}
body{margin:0}header{background:#0c2544;color:#fff;padding:22px max(20px,calc((100vw - 900px)/2))}header h1{margin:0;font-size:25px}
.wrap{max-width:900px;padding:20px;margin:auto}.card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px;margin-bottom:14px}
h2{font-size:17px;margin:0 0 10px}label{display:block;font-size:12px;color:#50617a;margin:10px 0 4px}
input{width:100%;padding:9px;border:1px solid #cfd9e4;border-radius:8px;font-size:13px}
.hint{font-size:11px;color:#738197;margin-top:3px}.status{font-size:12px;color:#0b7a53;font-weight:700}
button,.btn{display:inline-block;padding:10px 15px;border-radius:9px;border:0;background:#1261bd;color:#fff;font-weight:650;text-decoration:none;cursor:pointer;font-size:13px}
.btn.alt{background:#fff;color:#17508d;border:1px solid #b9cce2}.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.note{background:#fff9e6;border:1px solid #f1d38d;border-radius:9px;padding:11px 14px;color:#644a1a;font-size:13px;margin:12px 0}
@media(max-width:600px){.row{grid-template-columns:1fr}}
</style></head><body>
<header><h1>ArbiScout / settings</h1></header><main class="wrap">
<p><a class="btn alt" href="/">Back to control room</a></p>
__SAVED__
<div class="note">Keys are stored only in this folder's <b>.env</b> and are never displayed again. Leave a key blank to keep the current value; tick Clear to remove it.</div>
<form method="post" action="/api/settings">
<div class="card"><h2>Best Buy</h2>
<label>Deals page URL</label><input name="BESTBUY_URL" value="__BESTBUY_URL__" placeholder="https://www.bestbuy.com/black-friday">
</div>
<div class="card"><h2>Woot</h2>
<div class="row"><div><label>Feed</label><input name="WOOT_FEED" value="__WOOT_FEED__" placeholder="All"></div>
<div><label>Maximum products</label><input name="WOOT_MAX" value="__WOOT_MAX__" placeholder="500"></div></div>
<label>Woot API key <span class="status">__WOOT_KEY_STATUS__</span></label><input name="WOOT_API_KEY" type="password" placeholder="leave blank to keep current">
<label><input type="checkbox" name="clear_WOOT_API_KEY" style="width:auto"> Clear saved Woot key</label>
</div>
<div class="card"><h2>Meh</h2>
<label>Meh API key <span class="status">__MEH_KEY_STATUS__</span></label><input name="MEH_API_KEY" type="password" placeholder="leave blank to keep current">
<label><input type="checkbox" name="clear_MEH_API_KEY" style="width:auto"> Clear saved Meh key</label>
</div>
<div class="card"><h2>Kroger</h2>
<div class="row"><div><label>Client ID <span class="status">__KROGER_ID_STATUS__</span></label><input name="KROGER_CLIENT_ID" type="password" placeholder="leave blank to keep current"></div>
<div><label>Client secret <span class="status">__KROGER_SECRET_STATUS__</span></label><input name="KROGER_CLIENT_SECRET" type="password" placeholder="leave blank to keep current"></div></div>
<label>Search terms (comma-separated)</label><input name="KROGER_TERMS" value="__KROGER_TERMS__" placeholder="milk,eggs,bread">
<div class="row"><div><label>ZIP code</label><input name="KROGER_ZIP" value="__KROGER_ZIP__" placeholder="29072"></div>
<div><label>Location ID (optional)</label><input name="KROGER_LOCATION_ID" value="__KROGER_LOCATION_ID__" placeholder=""></div></div>
<label><input type="checkbox" name="clear_KROGER_CLIENT_ID" style="width:auto"> Clear Kroger client ID</label>
<label><input type="checkbox" name="clear_KROGER_CLIENT_SECRET" style="width:auto"> Clear Kroger client secret</label>
</div>
<button type="submit">Save settings</button>
</form>
</main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _file(self, path):
        target = Path(path)
        if not target.is_file():
            return self._send(404, "Not generated yet.")
        self._send(200, target.read_bytes())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            return self._send(200, HOME)
        if parsed.path == "/settings":
            env = read_env()
            saved = "<p class='status'>Settings saved.</p>" if parsed.query == "saved=1" else ""
            html = SETTINGS
            replacements = {
                "__SAVED__": saved,
                "__BESTBUY_URL__": env.get("BESTBUY_URL", "https://www.bestbuy.com/black-friday"),
                "__WOOT_FEED__": env.get("WOOT_FEED", "All"),
                "__WOOT_MAX__": env.get("WOOT_MAX", "500"),
                "__KROGER_TERMS__": env.get("KROGER_TERMS", "milk,eggs,bread"),
                "__KROGER_ZIP__": env.get("KROGER_ZIP", ""),
                "__KROGER_LOCATION_ID__": env.get("KROGER_LOCATION_ID", ""),
                "__WOOT_KEY_STATUS__": "set" if env.get("WOOT_API_KEY") else "not set",
                "__MEH_KEY_STATUS__": "set" if env.get("MEH_API_KEY") else "not set",
                "__KROGER_ID_STATUS__": "set" if env.get("KROGER_CLIENT_ID") else "not set",
                "__KROGER_SECRET_STATUS__": "set" if env.get("KROGER_CLIENT_SECRET") else "not set",
            }
            for key, value in replacements.items():
                html = html.replace(key, str(value))
            return self._send(200, html)
        if parsed.path == "/api/status":
            with LOCK:
                jobs = {key: {**value, "log": value["log"][-80:]} for key, value in JOBS.items()}
                body = json.dumps({"active": ACTIVE_JOB, "jobs": jobs}, ensure_ascii=False)
            return self._send(200, body, "application/json; charset=utf-8")
        if parsed.path == "/catalog":
            _, result = ensure_catalog()
            if result.startswith("http"):
                self.send_response(302)
                self.send_header("Location", result)
                self.end_headers()
                return
            return self._send(400, result)
        if parsed.path == "/capture":
            _, result = ensure_watcher()
            if result.startswith("http"):
                self.send_response(302)
                self.send_header("Location", result)
                self.end_headers()
                return
            return self._send(400, result)
        if parsed.path == "/reports/top10":
            for candidate in ("catalog/selected/index.html", "bestbuy_live/index.html"):
                if (APP_DIR / candidate).is_file():
                    return self._file(APP_DIR / candidate)
            return self._send(404, "No top-10 report yet.")
        if parsed.path == "/reports/comparisons":
            for candidate in ("catalog/selected/comparisons/index.html", "bestbuy_live/comparisons/index.html"):
                if (APP_DIR / candidate).is_file():
                    return self._file(APP_DIR / candidate)
            return self._send(404, "No comparison report yet.")
        if parsed.path == "/reports/retailer":
            for candidate in ("catalog/selected/retailer/index.html", "bestbuy_live/retailer/index.html"):
                if (APP_DIR / candidate).is_file():
                    return self._file(APP_DIR / candidate)
            return self._send(404, "No retailer dashboard yet.")
        return self._send(404, "Not found.")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/run":
            try:
                length = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(length) or b"{}")
                job = body.get("job")
                if job not in JOBS:
                    return self._send(400, json.dumps({"error": "Unknown job."}),
                                      "application/json; charset=utf-8")
                ok, message = start_job(job)
                return self._send(200 if ok else 409,
                                  json.dumps({"ok": ok, "message": message}, ensure_ascii=False),
                                  "application/json; charset=utf-8")
            except Exception as exc:
                return self._send(500, json.dumps({"error": str(exc)[:200]}),
                                  "application/json; charset=utf-8")
        if parsed.path == "/api/settings":
            try:
                length = int(self.headers.get("Content-Length") or 0)
                form = parse_qs(self.rfile.read(length).decode("utf-8", errors="replace"))
                updates = {}
                clears = []
                for key in ("BESTBUY_URL", "WOOT_FEED", "WOOT_MAX", "KROGER_TERMS",
                            "KROGER_ZIP", "KROGER_LOCATION_ID"):
                    if key in form:
                        updates[key] = form[key][0].strip()
                for key in ("MEH_API_KEY", "WOOT_API_KEY", "KROGER_CLIENT_ID",
                            "KROGER_CLIENT_SECRET"):
                    if form.get(f"clear_{key}"):
                        clears.append(key)
                    elif key in form and form[key][0].strip():
                        updates[key] = form[key][0].strip()
                write_env(updates, clears)
                self.send_response(302)
                self.send_header("Location", "/settings?saved=1")
                self.end_headers()
                return
            except Exception as exc:
                return self._send(500, f"Settings error: {exc}")
        return self._send(404, "Not found.")

    def log_message(self, *_args):
        pass


def main(argv=None):
    parser = argparse.ArgumentParser(description="ArbiScout local control room")
    parser.add_argument("--port", type=int, default=8800)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args(argv)
    load_env()
    port = args.port
    server = None
    for candidate in range(args.port, args.port + 15):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate), Handler)
            port = candidate
            break
        except OSError:
            continue
    if server is None:
        raise SystemExit("Could not find a free local port.")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/"
    print("ArbiScout control room:", url)
    print("Press Ctrl+C to stop.")
    if not args.no_open:
        webbrowser.open(url)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.shutdown()
        for proc in (CATALOG_PROC, WATCHER_PROC):
            if proc and proc.poll() is None:
                proc.terminate()


if __name__ == "__main__":
    main()
