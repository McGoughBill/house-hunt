#!/usr/bin/env python3
"""Show which fields are filled for each house and list the gaps. Reads facts.json; writes out/status.md."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tasks_def import TASKS, HOUSE_IDS

ROOT = Path(__file__).resolve().parent.parent
facts = json.loads((ROOT / "facts.json").read_text()) if (ROOT / "facts.json").exists() else {}
want = {}
for tid, t in TASKS.items():
    for h in t["ids"]:
        want.setdefault(h, []).extend((tid, f) for f in t["fields"])

rows, gaps = ["| House | Filled | Null | Missing |", "|---|---|---|---|"], []
for h in ["market"] + HOUSE_IDS:
    filled = null = 0
    for tid, f in want.get(h, []):
        fs = facts.get(h, {}).get(f, [])
        if any(x["value"] is not None for x in fs): filled += 1
        elif fs: null += 1; gaps.append(f"- {h} / {f} ({tid}): null — {fs[0].get('note','')[:100]}")
        else: gaps.append(f"- {h} / {f} ({tid}): not reported")
    extra = len(set(facts.get(h, {})) - {f for _, f in want.get(h, [])})
    rows.append(f"| {h} | {filled}/{len(want.get(h, []))} (+{extra} other) | {null} | {len(want.get(h, [])) - filled - null} |")

text = "# Status\n\n" + "\n".join(rows) + "\n\n## Gaps\n\n" + ("\n".join(gaps) or "None.") + "\n"
(ROOT / "out/status.md").write_text(text)
print("\n".join(rows)); print(f"{len(gaps)} gaps -> out/status.md")
