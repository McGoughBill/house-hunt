"""One-off: seed a profile registry from the 3 Nov 2026 house-judge run.
python3 scripts/import_house_judge.py <profile> <house-judge dir>"""
import re, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hh

prof, src = sys.argv[1], Path(sys.argv[2])
DAY = "2026-11-03"
c = hh.Ctx(prof, DAY)
c.reg = {"next_id": 91, "houses": {}}
judged = {(h["link"], h["street"]): h for h in json.loads((src / "houses.json").read_text())}

def add(h, hid, status, why=None):
    c.reg["houses"][hid] = {**h, "id": hid, "urls": [h["url"]] if h.get("url") else [], "sources": ["2026-11-03 search"],
        "first_seen": DAY, "last_seen": DAY, "price_history": [[DAY, h.get("price")]], "status": status,
        "out_reason": why, "runs": [], "retries": {}}

# 1. every row of the 3 Nov table
for line in (src / "shortlist-table.md").read_text().splitlines():
    cells = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(cells) != 12 or cells[0] in ("PC", "---") or set(cells[0]) <= {"-"}:
        continue
    pc, street, area, price, beds, m2, _, state, tenure, agent, conf, link = cells
    url = (re.search(r"\((http[^)]+)\)", link) or [None, None])[1]
    h = {"street": street, "area": area, "district": pc.upper(), "price": hh.num(price) if "£" in price else None,
         "price_text": price, "beds": beds or None, "m2": hh.num(m2), "tenure": tenure or None, "condition": state,
         "agent": agent or None, "url": url, "flags": []}
    if (url, street) in judged:
        add(h, judged[(url, street)]["id"], "judged")
    else:
        add(h, c.new_id(pc, street), "unconfirmed")

# 2. the 19 left out
for line in ((src / "shortlist-table.md").read_text().split("## Left out") + [""])[1].splitlines()[1:]:
    m = re.match(r"- (.+?)(?: \((£[\d,]+)\))?: (.+)", line.strip())
    if m:
        add({"street": m[1], "area": "", "district": "", "price": hh.num(m[2]) if m[2] else None, "price_text": m[2],
             "beds": None, "m2": None, "tenure": None, "condition": None, "agent": None, "url": None, "flags": []},
            c.new_id("x", m[1]), "out", m[3])

# 3. the 270 judge runs
n = 0
for f in sorted((src / "results").glob("*.json")):
    hid, run = f.stem.rsplit("_r", 1)
    if hid in c.reg["houses"]:
        raw = hh.jload(f)
        if raw:
            rec = hh.compact(raw, DAY); rec["run"] = run
            if hid.split("-")[0] in {"H001", "H002", "H003", "H004", "H005", "H006", "H007"}:
                rec["prompt"] = "v1"
            c.reg["houses"][hid]["runs"].append(rec); n += 1
c.save()
from collections import Counter
print(n, "runs;", Counter(h["status"] for h in c.reg["houses"].values()))
