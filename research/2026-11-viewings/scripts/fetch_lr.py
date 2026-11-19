#!/usr/bin/env python3
"""Land Registry price-paid (by street, postcode and sector, with tenure) and UK HPI for Sheffield.
Writes data/lr_<key>.csv, data/hpi_sheffield.csv and data/lr_status.json ({"ok": bool, "error": ...})."""
import csv, datetime as dt, io, json, sys
from pathlib import Path
import requests, yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; DATA.mkdir(exist_ok=True)
PPD = "https://landregistry.data.gov.uk/app/ppd/ppd_data.csv"
HPI = "https://landregistry.data.gov.uk/data/ukhpi/region/sheffield/month/{}.json"
since = (dt.date.today() - dt.timedelta(days=730)).strftime("%d %B %Y")

def status(ok, err=None):
    (DATA / "lr_status.json").write_text(json.dumps({"ok": ok, "error": err, "at": dt.datetime.now().isoformat(timespec="seconds")}))

def ppd(key, **q):
    r = requests.get(PPD, params={"header": "true", "limit": "all", **q}, timeout=60); r.raise_for_status()
    (DATA / f"lr_{key}.csv").write_text(r.text)
    return sum(1 for _ in csv.reader(io.StringIO(r.text))) - 1

try:
    houses = yaml.safe_load((ROOT / "houses.yaml").read_text())["houses"]
    for h in houses:
        street = " ".join(h["address"].split(",")[0].split()[1:]).upper()
        print(h["id"], "street", ppd(f"street_{h['id']}", street=street, town="SHEFFIELD"))       # all years: own history + ceiling
        if h["postcode"]:
            print(h["id"], "postcode", ppd(f"pc_{h['id']}", postcode=h["postcode"], min_date=since))
    for s in sorted({h["sector"] for h in houses}):
        print(s, "sector", ppd("sector_" + s.replace(" ", ""), postcode=s, min_date=since))
    rows, d = [], dt.date.today().replace(day=1)
    for i in range(36):
        m = (d - dt.timedelta(days=31 * i)).strftime("%Y-%m")
        r = requests.get(HPI.format(m), timeout=30)
        if r.status_code != 200: continue
        t = r.json()["result"]["primaryTopic"]
        for typ in ("Detached", "SemiDetached", "Terraced", "FlatMaisonette"):
            v = t.get(f"housePriceIndex{typ}")
            if v: rows.append([m, typ, v, HPI.format(m)])
    with open(DATA / "hpi_sheffield.csv", "w", newline="") as fh:
        csv.writer(fh).writerows([["month", "type", "index", "source"], *sorted(rows)])
    status(True); print("ok")
except Exception as e:
    status(False, f"{type(e).__name__}: {e}"[:300]); sys.exit(f"fetch_lr failed: {e}")
