#!/usr/bin/env python3
"""Render each house's brief from facts.json, out/comps/summary.json and templates/brief.md -> out/briefs/<id>.md.
Never overwrites the agent-written parts: run before wave 3 only, or pass --force."""
import json, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
tpl = (ROOT / "templates/brief.md").read_text()
facts = json.loads((ROOT / "facts.json").read_text())
cp = ROOT / "out/comps/summary.json"
comps = json.loads(cp.read_text()) if cp.exists() else {}

def cell(v):
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s.replace("|", "/").replace("\n", " ")[:160]

for h in yaml.safe_load((ROOT / "houses.yaml").read_text())["houses"]:
    path = ROOT / f"out/briefs/{h['id']}.md"
    if path.exists() and "--force" not in sys.argv:
        print("skip", path.name); continue
    rows = ["| Field | Value | Source |", "|---|---|---|"]
    for field, fs in sorted(facts.get(h["id"], {}).items()):
        for f in fs:
            v = cell(f["value"]) if f["value"] is not None else f"*null: {cell(f.get('note', ''))}*"
            rows.append(f"| {field} | {v} | [{f['task']}]({f['source']}) |" if f["source"] else f"| {field} | {v} | {f['task']} |")
    c = comps.get(h["id"])
    ctext = "```json\n" + json.dumps(c, indent=1) + "\n```" if c else "*Not yet run.*"
    path.write_text(tpl.format(**{k: h.get(k) for k in ("address", "postcode", "price_text", "agent", "viewing")},
                               facts_table="\n".join(rows), comps=ctext))
    print("wrote", path.name)
