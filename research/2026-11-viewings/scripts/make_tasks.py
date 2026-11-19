#!/usr/bin/env python3
"""Build every agent prompt from templates/task.md. S1-S4 only if fetch_lr.py failed.
Usage: make_tasks.py  -> writes tasks/<id>.md and prints the ids."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tasks_def import TASKS

ROOT = Path(__file__).resolve().parent.parent
tpl = (ROOT / "templates/task.md").read_text()
lr = ROOT / "data/lr_status.json"
lr_ok = lr.exists() and json.loads(lr.read_text()).get("ok")
out = ROOT / "tasks"; out.mkdir(exist_ok=True)
made = []
for tid, t in TASKS.items():
    if t.get("comps") and lr_ok:
        continue
    text = tpl.format(task_id=tid, scope=t["scope"], root=ROOT, ids=", ".join(t["ids"]),
                      sources=t["sources"], fields=", ".join(t["fields"]), extra=t.get("extra", ""))
    (out / f"{tid}.md").write_text(text)
    made.append(tid)
print("Land Registry script:", "worked" if lr_ok else "failed or not run")
print("tasks:", " ".join(made))
