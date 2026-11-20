#!/usr/bin/env python3
"""Wave 4: build the two checker prompts from templates/verify.md -> tasks/verify_A.md, tasks/verify_B.md."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PACK = "/home/claude/w4-verify"
C = {"A": ("34 Falmouth Road (falmouth), 50 Welby Place (welby), 57 Lees Hall Road (leeshall)",
           "\nAlso check the market lines used in any brief (bank rate, five-year fixes, RICS balance and similar): "
           "find each in facts.json under \"market\", open its source and mark it as in step a."),
     "B": ("6 Cawthorne Grove (cawthorne), 38 Underwood Road (underwood), 17 Helmton Drive (helmton), 51 Hollythorpe Road (hollythorpe)", "")}
tpl = (ROOT / "templates/verify.md").read_text()
(ROOT / "tasks").mkdir(exist_ok=True)
for k, (houses, market) in C.items():
    t = tpl.format(briefs=f"{PACK}/saturday-briefs-2026-11-21.md and {PACK}/saturday-viewings-2026-11-21.md",
                   out=f"{PACK}/out/{k}.md", checker=k, pack=PACK, houses=houses, market=market)
    (ROOT / f"tasks/verify_{k}.md").write_text(t)
    print("wrote tasks/verify_%s.md" % k)
