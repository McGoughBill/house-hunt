"""Checker A: recompute figures for falmouth, welby, leeshall from raw sale rows and HPI files."""
import csv, json, glob, statistics, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = {"D": ("detached", "Detached"), "S": ("semi_detached", "SemiDetached"),
         "T": ("terraced", "Terraced"), "F": ("flat", "FlatMaisonette")}

uk = {r["month"]: r for r in csv.DictReader(open(f"{BASE}/data/hpi_sheffield_ukhpi.csv"))}
old = {}
for r in csv.DictReader(open(f"{BASE}/data/hpi_sheffield.csv")):
    old[(r["month"], r["type"])] = float(r["index"])

def idx(month, t):
    if month in uk:
        return float(uk[month][TYPES[t][0]])
    return old[(month, TYPES[t][1])]

def today(price, date, t, target="2026-09"):
    return price * idx(target, t) / idx(date[:7], t)

rows = []
for fn in glob.glob(f"{BASE}/data/sales/*.jsonl"):
    for l in open(fn):
        r = json.loads(l); r["_file"] = os.path.basename(fn); rows.append(r)

def q(xs):
    xs = sorted(xs)
    qs = statistics.quantiles(xs, n=4, method="inclusive")
    return qs[0], statistics.median(xs), qs[2]

print("== last sale in today's money")
for name, p, d, t in [("falmouth", 119950, "2012-01-27", "T"), ("welby", 242000, "2021-11-19", "D")]:
    print(name, round(today(p, d, t)))

print("== Lees Hall £/m2 (W2c rows, today's money)")
lh = [r for r in rows if r["_file"] == "W2c.jsonl" and r.get("for_house") == "leeshall"]
pp = [today(r["price"], r["date"], "S") / r["floor_area_m2"] for r in lh]
for r, v in zip(lh, pp):
    print(f"  {r['address']:35} {r['date']} {r['price']:>7} {r['floor_area_m2']:>4} {v:7.0f}")
lo, med, hi = q(pp)
print(f"n={len(pp)} q1={lo:.0f} med={med:.0f} q3={hi:.0f}; at 69 m2: {lo*69:.0f} {med*69:.0f} {hi*69:.0f}")
print(f"asking 290000/69 = {290000/69:.0f}; over median {(290000/69/med-1)*100:.1f}%")
# exclusive method too
qe = statistics.quantiles(pp, n=4)
print("exclusive quartiles", [round(x) for x in qe])

print("== W4C comparables today + range")
for h in ["falmouth", "welby", "leeshall"]:
    w = [r for r in rows if r["_file"] == "W4C.jsonl" and r.get("house") == h]
    vals = []
    for r in w:
        v = today(r["price"], r["date"], r["type"]); vals.append(v)
        print(f"  {h} {r['address']:30} {r['date']} {r['price']:>7} {r['type']} {r['tenure']} {r.get('floor_area_m2')} -> {v:.0f}")
    print(f"  {h} range {min(vals):.0f}-{max(vals):.0f}")

print("== street tops in held rows")
for h, key in [("falmouth", "Falmouth Road"), ("welby", "Welby Place"), ("leeshall", "Lees Hall Road")]:
    s = [r for r in rows if key.lower() in r["address"].lower()]
    top = max(s, key=lambda r: r["price"])
    print(h, top["address"], top["date"], top["price"], top["type"], top["tenure"], round(today(top["price"], top["date"], top["type"])))
bs = list(csv.DictReader(open(f"{BASE}/data/bungalow_sales.csv")))
wb = [r for r in bs if r["area"] == "welby_place"]
top = max(wb, key=lambda r: int(r["price"]))
print("welby top in bungalow_sales:", top["address"], top["date"], top["price"])
print("welby cash £/m2:", sorted(((round(int(r['price'])/int(r['m2'])), r['address'], r['group']) for r in wb), reverse=True)[:4])

print("== asking £/m2 and days")
from datetime import date
for h, p, a, d in [("falmouth", 210000, 94, "2026-08-27"), ("welby", 265000, 60, "2026-09-02"), ("leeshall", 290000, 69, "2026-09-08")]:
    print(h, round(p/a), (date(2026, 11, 19) - date.fromisoformat(d)).days)
print("falmouth cut %", round((215000-210000)/215000*100, 2), "1007 sqft m2", round(1007*0.092903, 1), "1163 sqft", round(1163*0.092903, 1), "1007 vs 1163", round((1-1007/1163)*100, 1))
print("kennedy", round(315000/81), round(870*0.092903, 1), round(315000/(870*0.092903)))
print("welby model vs asking", 265000-250699, 265000-245378)

print("== area tops in today's money")
for name, p, d, t, fact in [("falmouth 21 Endowood", 661000, "2022-04-20", "T", 768229),
                            ("welby 143 Meersbrook Park Rd", 650000, "2022-08-25", "D", 702220),
                            ("leeshall 220 Shirebrook Rd", 605000, "2025-08-27", "S", 618036),
                            ("welby street top 42 Welby", 292500, "2025-11-03", "T", 296181)]:
    v = today(p, d, t)
    print(name, round(v), "fact", fact, f"diff {(fact/v-1)*100:+.1f}%")
