#!/usr/bin/env python3
"""Join sales to floor areas, index to today with Sheffield HPI by type, work out £/m².
Reads data/sales/*.jsonl (schema/sale.json) and data/hpi_sheffield.csv.
Writes out/comps/<sector>.csv and out/comps/summary.json (per house: street and postcode median, spread, top; ceiling; indexed last sale)."""
import csv, json, statistics as st
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
TYPE = {"D": "Detached", "S": "SemiDetached", "T": "Terraced", "F": "FlatMaisonette"}
hpi = {}
p = ROOT / "data/hpi_sheffield.csv"
if p.exists():
    for r in csv.DictReader(p.open()): hpi[(r["month"], r["type"])] = float(r["index"])
latest = {t: max((m for m, tt in hpi if tt == t), default=None) for t in TYPE.values()}

def index(price, date, typ):
    t = TYPE.get(typ); m = date[:7]
    if not t or (m, t) not in hpi or not latest[t]: return None
    return round(price * hpi[(latest[t], t)] / hpi[(m, t)])

sales = []
for f in sorted((ROOT / "data/sales").glob("*.jsonl")):
    sales += [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
seen = set(); uniq = []
for s in sales:
    k = (s["address"].upper(), s["date"], s["price"])
    if k not in seen: seen.add(k); uniq.append(s)
for s in uniq:
    s["indexed"] = index(s["price"], s["date"], s["type"])
    a = s.get("floor_area_m2")
    s["ppm2"] = round((s["indexed"] or s["price"]) / a) if a else None

def summ(rows):
    v = sorted(r["ppm2"] for r in rows if r["ppm2"])
    top = max(rows, key=lambda r: r["price"], default=None)
    return {"n": len(rows), "n_with_area": len(v), "median_ppm2": st.median(v) if v else None,
            "spread_ppm2": [v[0], v[-1]] if v else None, "top_price": top and top["price"], "top_address": top and top["address"]}

out = ROOT / "out/comps"; out.mkdir(parents=True, exist_ok=True)
summary = {}
for h in yaml.safe_load((ROOT / "houses.yaml").read_text())["houses"]:
    street = " ".join(h["address"].split(",")[0].split()[1:]).upper()
    on_street = [s for s in uniq if street in s["address"].upper()]
    in_pc = [s for s in uniq if h["postcode"] and s["postcode"].upper() == h["postcode"].upper()]
    in_sector = [s for s in uniq if s["postcode"].upper().startswith(h["sector"].upper())]
    own = [s for s in on_street if s["address"].upper().startswith(h["address"].split()[0] + " ")]
    last = max(own, key=lambda s: s["date"], default=None)
    summary[h["id"]] = {"street": summ(on_street), "postcode": summ(in_pc), "sector": summ(in_sector),
                        "street_ceiling": max((s["price"] for s in on_street), default=None),
                        "last_sale": last and {k: last[k] for k in ("date", "price", "indexed", "source")}}
by_sector = {}
for s in uniq: by_sector.setdefault(s["postcode"][:4].replace(" ", ""), []).append(s)
cols = ["address", "postcode", "date", "price", "indexed", "type", "tenure", "new_build", "floor_area_m2", "ppm2", "source"]
for sec, rows in by_sector.items():
    with open(out / f"{sec}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader(); w.writerows(sorted(rows, key=lambda r: r["date"]))
(out / "summary.json").write_text(json.dumps(summary, indent=1))
print(f"{len(uniq)} sales, HPI {'loaded' if hpi else 'MISSING: prices not indexed'} -> out/comps/")
