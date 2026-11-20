"""Checker B: recompute figures for cawthorne, underwood, helmton, hollythorpe
straight from data/sales/*.jsonl and data/hpi_sheffield*.csv. Run with python3 -I."""
import csv, glob, json, os, statistics

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
TYPE = {"S": "SemiDetached", "T": "Terraced", "D": "Detached", "F": "FlatMaisonette"}

hpi = {}
for r in csv.DictReader(open(os.path.join(D, "hpi_sheffield.csv"))):
    hpi[(r["month"], r["type"])] = float(r["index"])
uk = {}
for r in csv.DictReader(open(os.path.join(D, "hpi_sheffield_ukhpi.csv"))):
    for col, t in [("detached", "Detached"), ("semi_detached", "SemiDetached"),
                   ("terraced", "Terraced"), ("flat", "FlatMaisonette")]:
        uk[(r["month"], t)] = float(r[col])

def today(price, date, typ, to="2026-09"):
    t = TYPE[typ]; m = date[:7]
    src = uk if (m, t) in uk else hpi
    return price * src[(to, t)] / src[(m, t)]

rows = {}
for f in glob.glob(os.path.join(D, "sales", "*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        k = (r["address"], r["date"], r["price"])
        old = rows.get(k)
        if old is None or (r.get("floor_area_m2") and not old.get("floor_area_m2")):
            rows[k] = r
rows = list(rows.values())

def street(name):
    return [r for r in rows if name.lower() in r["address"].lower()]

def quart(v, method):
    return statistics.quantiles(v, n=4, method=method)

def ppm(name, typ, since, area, exclude_cat_b=True):
    s = [r for r in street(name) if r["type"] == typ and r["date"] >= since and r.get("floor_area_m2")]
    v = sorted(today(r["price"], r["date"], typ) / r["floor_area_m2"] for r in s)
    print(f"  {name}: {len(v)} {typ} sales with area since {since}")
    for r in sorted(s, key=lambda r: r["date"]):
        print(f"    {r['address']:32} {r['date']} {r['price']:>7} {r['floor_area_m2']} m2 -> {today(r['price'], r['date'], typ)/r['floor_area_m2']:.0f}/m2")
    if len(v) >= 2:
        for m in ("inclusive", "exclusive"):
            q = quart(v, m)
            print(f"    quartiles ({m}): {q[0]:.0f} / {q[1]:.0f} / {q[2]:.0f} per m2 -> at {area} m2: "
                  f"{q[0]*area:.0f} / {q[1]*area:.0f} / {q[2]*area:.0f}")
    elif v:
        print(f"    single: {v[0]:.0f}/m2 -> {v[0]*area:.0f}")

def top(name):
    s = street(name)
    t = max(s, key=lambda r: r["price"])
    print(f"  street top in pack: {t['address']} {t['date']} {t['price']} {t['type']} {t['tenure']} today {today(t['price'], t['date'], t['type']):.0f}")

def comps(name, typ, picks):
    vals = []
    for r in street(name):
        if r["type"] == typ and r["address"].split()[0] in picks:
            v = today(r["price"], r["date"], typ); vals.append(v)
            print(f"    comp {r['address']:32} {r['date']} {r['price']} -> {v:.0f}")
    print(f"    range {min(vals):.0f} - {max(vals):.0f}")

print("CAWTHORNE (80 m2, semi)")
ppm("Cawthorne Grove", "S", "2023-11-19", 80)
print(f"  own last sale 253000 2023-04-03 S -> {today(253000, '2023-04-03', 'S'):.0f}")
comps("Cawthorne Grove", "S", {"26", "22", "8", "12"})
top("Cawthorne Grove")
print(f"  27C 435000 2025-05 D -> {today(435000, '2025-05-14', 'D'):.0f}")
print(f"  asking 300000/80={300000/80:.0f}, 325000/80={325000/80:.0f}")

print("\nUNDERWOOD (85 m2, terrace)")
ppm("Underwood Road", "T", "2023-11-19", 85)
print(f"  own last sale 140000 2020-12-07 T -> {today(140000, '2020-12-07', 'T'):.0f}")
comps("Underwood Road", "T", {"56", "30", "48"})
top("Underwood Road")
print(f"  asking 220000/85={220000/85:.0f}")

print("\nHELMTON (73 m2, semi)")
ppm("Helmton Drive", "S", "2023-11-19", 73)
print(f"  own last sale 190000 2018-12-19 S -> {today(190000, '2018-12-19', 'S'):.0f}")
comps("Helmton Drive", "S", {"1", "3", "1A"})
top("Helmton Drive")
print(f"  asking 265000/73={265000/73:.0f}; cut 300000->265000 = {(300000-265000)/300000*100:.1f}%")

print("\nHOLLYTHORPE (68 m2, semi)")
ppm("Hollythorpe Road", "S", "2023-11-19", 68)
print(f"  own last sale 136500 2010-10-01 S -> {today(136500, '2010-10-01', 'S'):.0f}")
comps("Hollythorpe Road", "S", {"30", "42", "14", "25"})
top("Hollythorpe Road")
print(f"  asking 280000/68={280000/68:.0f}, /67.9={280000/67.9:.0f}")
for no, p, d in [("49", 315000, "2025-06-30"), ("80", 330000, "2025-03-14"), ("13", 295000, "2025-10-28")]:
    print(f"  No. {no} {p} {d} -> {today(p, d, 'S'):.0f}")

print("\nAREA TOP PRICES (sector, same type), value today")
for a, p, d, t in [("261 Abbey Lane S8 0BT", 710000, "2025-08-07", "S"),
                   ("200 Norton Lane S8 8HB", 560000, "2023-08-21", "S"),
                   ("220 Shirebrook Road S8 9RG", 605000, "2025-08-27", "S"),
                   ("79 Norton Park View S8 8GU", 450000, "2024-12-13", "T")]:
    print(f"  {a} {p} {d} {t} -> {today(p, d, t):.0f}")
