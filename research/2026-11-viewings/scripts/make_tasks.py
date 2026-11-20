#!/usr/bin/env python3
"""Build agent prompts.
Wave 1/2: make_tasks.py [ID ...]  -> tasks/<id>.md from templates/task.md and tasks_def.py (S1-S4 only if fetch_lr.py failed).
Wave 3:   make_tasks.py --briefs [house ...] -> tasks/brief_<house>.md from templates/brief_task.md, and the per-house
          context files ref/saturday/<house>.md and ref/plan/<house>.md, cut from the Saturday doc and the plan's §6."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tasks_def import TASKS

ROOT = Path(__file__).resolve().parent.parent
out = ROOT / "tasks"; out.mkdir(exist_ok=True)

# Per-house extras for wave 3. Thin = fewer than 3 same-type sales with a floor area (wave 2).
THIN = {"falmouth", "welby", "underwood", "helmton"}
BRIEF_EXTRA = {
    "falmouth": "Special: the listing says the front door opens into the living room (hall rule). Area 94 vs 108 m² is unsettled: work on 94.",
    "welby": "Special: read out/welby/bungalow_ratio.md too (bungalow model; 50 Welby's own 2021 sale). His extension plan loses money above about a £220k purchase (Saturday doc); the old notes said open £225k, walk away £235k: test those against the evidence, don't copy them.",
    "leeshall": "Special: the 69 m² (EPC) may leave out the dining-room extension; say how the price moves if it does (each 10 m² ≈ street median × 10). Tenure is leasehold at medium confidence only.",
    "cawthorne": "Special: guide £300–325k; the seller bought in Apr 2023. Don't anchor on the guide.",
    "underwood": "Special: listed 28 Oct, so the time-on-market lever is weak. A Hunters listing on the same street at the same price may be this house with a second agent (open ruling).",
    "helmton": "Special: the seller shows the house: questions should be open and aimed at motive and timing. Already done up per listing, so faults may be few.",
    "hollythorpe": "Special: viewing time not yet confirmed by Whitehornes. Already done up per listing. 269 days unsold with no cut.",
}


def cut_sections():
    sat = (ROOT / "out/saturday-viewings-2026-11-21.md").read_text()
    plan = (ROOT / "ref/price-evidence-plan-s2-s4-s6.md").read_text()
    (ROOT / "ref/saturday").mkdir(parents=True, exist_ok=True)
    (ROOT / "ref/plan").mkdir(parents=True, exist_ok=True)
    common = re.search(r"^## At every house\n.*?(?=^---|^## 1\.)", sat, re.S | re.M).group(0)
    (ROOT / "ref/saturday/_common.md").write_text(common)
    secs = re.split(r"(?m)^(?=## \d\. )", sat)
    for hid, word in [("falmouth", "Falmouth"), ("welby", "Welby"), ("leeshall", "Lees Hall"), ("cawthorne", "Cawthorne"),
                      ("underwood", "Underwood"), ("helmton", "Helmton"), ("hollythorpe", "Hollythorpe")]:
        s = next(x for x in secs if x.startswith("## ") and word in x.splitlines()[0])
        s = re.split(r"(?m)^---\s*$|^## Not on Saturday", s)[0]
        (ROOT / f"ref/saturday/{hid}.md").write_text(s.strip() + "\n")
        p = re.search(rf"(?ms)^### {hid} —.*?(?=^### |^\*\*Agents:\*\*)", plan).group(0)
        tail = re.search(r"(?ms)^\*\*Agents:\*\*.*", plan).group(0)
        (ROOT / f"ref/plan/{hid}.md").write_text(p.strip() + "\n\n" + tail.strip() + "\n")


def briefs(only):
    import yaml
    tpl = (ROOT / "templates/brief_task.md").read_text()
    cut_sections()
    made = []
    for h in yaml.safe_load((ROOT / "houses.yaml").read_text())["houses"]:
        if only and h["id"] not in only:
            continue
        extra = BRIEF_EXTRA.get(h["id"], "")
        text = tpl.format(id=h["id"], address=h["address"], postcode=h["postcode"], viewing=h["viewing"],
                          price_text=h["price_text"], agent=h["agent"], root=ROOT,
                          thin="they are, for this house" if h["id"] in THIN else "not the case here, but the rule stands",
                          extra=("6. " + extra + "\n") if extra else "", words=260)
        (out / f"brief_{h['id']}.md").write_text(text)
        made.append(h["id"])
    print("brief tasks:", " ".join(made))


def wave12(only):
    tpl = (ROOT / "templates/task.md").read_text()
    lr = ROOT / "data/lr_status.json"
    lr_ok = lr.exists() and json.loads(lr.read_text()).get("ok")
    made = []
    for tid, t in TASKS.items():
        if only and tid not in only:
            continue
        if not only and (t.get("wave", 1) != 1 or (t.get("comps") and lr_ok)):
            continue
        text = tpl.format(task_id=tid, scope=t["scope"], root=ROOT, ids=", ".join(t["ids"]),
                          sources=t["sources"], fields=", ".join(t["fields"]), extra=t.get("extra", ""), cap=t.get("cap", 15))
        (out / f"{tid}.md").write_text(text)
        made.append(tid)
    print("Land Registry script:", "worked" if lr_ok else "failed or not run")
    print("tasks:", " ".join(made))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--briefs":
        briefs(set(args[1:]))
    else:
        wave12(set(args))
