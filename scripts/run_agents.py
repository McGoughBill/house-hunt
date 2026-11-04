#!/usr/bin/env python3
"""Run agent jobs through the claude CLI: at most --max at once, exit codes polled, each failure retried once.

Usage: python3 scripts/run_agents.py [options] JOB [JOB ...]
       python3 scripts/hh.py jobs P D | python3 scripts/run_agents.py [options] -

JOB is a prompt file, as "path", "agent=path" or "agent<TAB>path" (the form hh.py jobs prints).
With no agent named, prompts under prompts/search/ go to house-search and the rest to house-judge.
Each job runs: claude -p --agent A --model M --effort E "Read <path> and do exactly what it says."
with the model, effort and tools taken from agents/A.md.

A job succeeds when the CLI exits 0, reports no error, and, for a prompt at .../prompts/<kind>/<stem>.md,
leaves readable JSON at .../results/<kind>/<stem>.json. Jobs whose result already exists are skipped, so
rerunning the same command resumes a run that was cut off.

A failure is retried once. A failure that looks like a rate limit (429, "rate limit", "overloaded") does not
use up that retry: it pauses new launches for --cooldown seconds, halves the number running (not below 4),
and requeues the job, at most 3 times. After 10 successes in a row the cap climbs back by 2 towards --max.

Logs: one JSON line per attempt in <run dir>/agent-runs.jsonl; CLI output per attempt in <run dir>/logs/.
Stdout: a start line, one line per job that finally fails, and a summary line.
Exit: 0 all ok · 3 some failed · 4 the claude CLI is missing or cannot sign in.
"""
import argparse, json, os, re, shutil, signal, subprocess, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CFG = json.loads((REPO / "house-hunt.json").read_text()).get("runner", {}) if (REPO / "house-hunt.json").exists() else {}
RATE = re.compile(r"\b429\b|rate.?limit|overloaded|too many requests", re.I)
AUTH = re.compile(r"not logged in|invalid api key|authentication|please run /login|unauthori[sz]ed|\b401\b", re.I)

def agent_def(name):
    f = REPO / "agents" / f"{name}.md"
    meta = {}
    if f.exists():
        m = re.match(r"---\n(.*?)\n---", f.read_text(), re.S)
        for line in (m.group(1).splitlines() if m else []):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return {"model": meta.get("model", "haiku"), "effort": meta.get("effort", "xhigh"),
            "tools": [t.strip() for t in meta.get("tools", "Read, Write, WebSearch, WebFetch").split(",") if t.strip()]}

def parse_job(s):
    s = s.strip()
    if not s or s.startswith("#"):
        return None
    agent, path = None, s
    if "\t" in s:
        agent, path = s.split("\t", 1)
    elif "=" in s and not s.startswith("/") and s.split("=", 1)[0].replace("-", "").isalnum():
        agent, path = s.split("=", 1)
    p = Path(path.strip())
    p = p if p.is_absolute() else (Path.cwd() / p)
    if not agent:
        agent = "house-search" if "/prompts/search/" in str(p) else "house-judge"
    return {"agent": agent.strip(), "prompt": p.resolve()}

def expected(prompt):
    parts = prompt.parts
    if "prompts" not in parts:
        return None
    i = len(parts) - 1 - parts[::-1].index("prompts")
    return Path(*parts[:i], "results", *parts[i + 1:-1], prompt.stem + ".json")

def readable(p):
    try:
        txt = p.read_text()
        m = re.search(r"[\[{].*[\]}]", txt, re.S)
        json.loads(m.group(0))
        return True
    except Exception:
        return False

def run_dir(prompt):
    parts = prompt.parts
    if "prompts" in parts:
        return Path(*parts[:len(parts) - 1 - parts[::-1].index("prompts")])
    return prompt.parent

def key(job):
    return f"{job['prompt'].parent.name}/{job['prompt'].stem}"

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("jobs", nargs="*")
    ap.add_argument("--max", type=int, default=CFG.get("max", 20))
    ap.add_argument("--retries", type=int, default=CFG.get("retries", 1))
    ap.add_argument("--timeout", type=float, default=CFG.get("timeout_min", 30), help="minutes per attempt")
    ap.add_argument("--cooldown", type=int, default=CFG.get("cooldown_s", 300), help="seconds to pause after a rate limit")
    ap.add_argument("--poll", type=float, default=2.0)
    ap.add_argument("--force", action="store_true", help="run jobs even if their result exists")
    a = ap.parse_args()

    raw = []
    for s in a.jobs:
        raw += sys.stdin.read().splitlines() if s == "-" else [s]
    jobs, seen = [], set()
    for s in raw:
        j = parse_job(s)
        if j and j["prompt"] not in seen:
            seen.add(j["prompt"]); jobs.append(j)
    cli = shutil.which(CFG.get("cli", "claude"))
    if not cli:
        print("run_agents: claude CLI not found; launch with the Agent tool instead"); sys.exit(4)
    todo, skipped = [], 0
    for j in jobs:
        if not j["prompt"].exists():
            print(f"run_agents: no prompt file {j['prompt']}"); continue
        out = expected(j["prompt"])
        if out and out.exists() and readable(out) and not a.force:
            skipped += 1; continue
        j.update(out=out, attempt=0, fails=0, rate_tries=0)
        todo.append(j)
    print(f"run_agents: {len(todo)} to run, {skipped} already done, up to {a.max} at once")
    if not todo:
        sys.exit(0)

    running, ok, failed = {}, [], []
    cap, streak, pause_until, retried, rated, cost, t0 = a.max, 0, 0.0, 0, 0, 0.0, time.time()

    def stop_all(*_):
        for p, _j, _f in running.values():
            p.kill()
        print(f"run_agents: stopped; {len(running)} killed, rerun the same command to resume")
        sys.exit(130)
    signal.signal(signal.SIGTERM, stop_all)
    signal.signal(signal.SIGINT, stop_all)

    def launch(j):
        d = agent_def(j["agent"])
        rd = run_dir(j["prompt"]); logs = rd / "logs"; logs.mkdir(parents=True, exist_ok=True)
        j["attempt"] += 1
        stem = f"{key(j).replace('/', '-')}.{j['attempt']}"
        fo, fe = open(logs / f"{stem}.json", "w"), open(logs / f"{stem}.err", "w")
        cmd = [cli, "-p", "--agent", j["agent"], "--model", d["model"], "--effort", d["effort"],
               "--permission-mode", "dontAsk", "--allowedTools", *d["tools"], "--output-format", "json",
               f"Read {j['prompt']} and do exactly what it says."]
        p = subprocess.Popen(cmd, cwd=REPO, stdin=subprocess.DEVNULL, stdout=fo, stderr=fe,
                             env={**os.environ, "CLAUDE_CODE_ENTRYPOINT": "house-hunt-runner"})
        j["start"], j["stem"], j["logs"] = time.time(), stem, logs
        running[p.pid] = (p, j, (fo, fe))

    def record(j, code, okk, reason, c):
        with open(run_dir(j["prompt"]) / "agent-runs.jsonl", "a") as fh:
            fh.write(json.dumps({"job": key(j), "agent": j["agent"], "try": j["attempt"], "exit": code, "ok": okk,
                                 "reason": reason, "secs": round(time.time() - j["start"]), "cost": c}) + "\n")

    queue = list(todo)
    while queue or running:
        now = time.time()
        while queue and len(running) < cap and now >= pause_until:
            launch(queue.pop(0))
        time.sleep(a.poll)
        for pid, (p, j, files) in list(running.items()):
            code = p.poll()
            late = time.time() - j["start"] > a.timeout * 60
            if code is None and not late:
                continue
            if code is None:
                p.kill(); p.wait(); code = -9
            for f in files:
                f.close()
            del running[pid]
            out_txt = (j["logs"] / f"{j['stem']}.json").read_text(errors="replace")
            err_txt = (j["logs"] / f"{j['stem']}.err").read_text(errors="replace")
            res, c = {}, None
            try:
                res = json.loads(out_txt); c = res.get("total_cost_usd")
            except ValueError:
                pass
            cost += c or 0
            text = " ".join([str(res.get("result", "")), err_txt[-2000:]])
            if late:
                reason = "timeout"
            elif code != 0 or res.get("is_error"):
                reason = "rate limit" if RATE.search(text) else ("auth" if AUTH.search(text) else f"exit {code}")
            elif j["out"] and not (j["out"].exists() and readable(j["out"])):
                reason = "no readable result file"
            else:
                reason = None
            record(j, code, reason is None, reason, c)
            if reason is None:
                ok.append(j); streak += 1
                if streak >= 10 and cap < a.max:
                    cap, streak = min(a.max, cap + 2), 0
                continue
            streak = 0
            if reason == "auth":
                for q, _j, _f in running.values():
                    q.kill()
                print("run_agents: the claude CLI cannot sign in; launch with the Agent tool instead"); sys.exit(4)
            if reason == "rate limit" and j["rate_tries"] < 3:
                j["rate_tries"] += 1; rated += 1
                pause_until = time.time() + a.cooldown; cap = max(4, cap // 2)
                queue.append(j); continue
            j["fails"] += 1
            if j["fails"] <= a.retries:
                retried += 1; queue.append(j); continue
            failed.append(j)
            print(f"FAILED {key(j)} after {j['attempt']} tries: {reason}")
    mins = (time.time() - t0) / 60
    print(f"run_agents: ok {len(ok)}, failed {len(failed)}, retried {retried}, rate-limited {rated}, "
          f"cap now {cap}, ${cost:.2f}, {mins:.0f} min")
    sys.exit(3 if failed else 0)

if __name__ == "__main__":
    main()
