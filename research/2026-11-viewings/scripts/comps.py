#!/usr/bin/env python3
"""Comparables, wave 2.
Reads data/sales/*.jsonl (schema/sale.json), data/bungalow_sales.csv (HouseMetric floor areas),
data/hpi_sheffield.csv (UK HPI, Sheffield, by type), numbers.yaml (each house's type, area, asking, price history)
and facts.json (own past sales, street's highest price ever).
For each house: asking £/m²; comparable £/m² (median, spread, top) for street and postcode, same type, last 3 years,
brought to today's values; street ceiling ever; last sale of the house in today's money; days on market; price cuts.
Flags 'thin' where fewer than 3 same-type sales in 3 years, or fewer than 3 of them with a floor area.
Writes out/comps/summary.json, out/comps/houses.md and out/comps/<sector>.csv."""
import csv, json, re, statistics as st, datetime as dt
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date(2026, 11, 19)
SINCE = dt.date(2023, 11, 19)          # 3-year window
TYPE = {"D": "Detached", "S": "SemiDetached", "T": "Terraced", "F": "FlatMaisonette"}

hpi = {}
for r in csv.DictReader((ROOT / "data/hpi_sheffield.csv").open()):
    hpi[(r["month"], r["type"])] = float(r["index"])
LATEST = max(m for m, _ in hpi)

def index(price, date, typ):
    """Price brought to the latest HPI month by Sheffield type index. None if the sale month is not in the series."""
    t = TYPE.get(typ); m = date[:7]
    if not t: return None
    if m > LATEST: return price                      # sold after the index ends: already today's money
    if (m, t) not in hpi: return None
    return round(price * hpi[(LATEST, t)] / hpi[(m, t)])

def key_addr(a):
    a = a.upper().split(",")[0]
    a = re.sub(r"\s+", " ", a.replace("SHEFFIELD", "")).strip()
    return a

def age_band(date):
    y = (TODAY - dt.date.fromisoformat(date)).days / 365.25
    return "6+ yrs" if y >= 6 else f"{int(y)}–{int(y)+1} yrs" if y >= 1 else "<1 yr"

# ---- load and merge sales ----
raw = []
for f in sorted((ROOT / "data/sales").glob("*.jsonl")):
    for l in f.read_text().splitlines():
        if l.strip():
            s = json.loads(l); s["_file"] = f.name; raw.append(s)
bc = ROOT / "data/bungalow_sales.csv"
if bc.exists():
    for r in csv.DictReader(bc.open()):
        raw.append({"address": r["address"], "postcode": r["postcode"], "date": r["date"], "price": int(r["price"]),
                    "type": r["lr_type"], "tenure": None, "new_build": False, "floor_area_m2": float(r["m2"]),
                    "area_source": r["source"], "source": r["source"], "_file": "bungalow_sales.csv",
                    "bungalow": r["group"] == "bungalow"})
merged = {}
for s in raw:
    k = (key_addr(s["address"]), s["date"], int(s["price"]))
    m = merged.setdefault(k, dict(s))
    for fld in ("floor_area_m2", "area_source", "tenure", "lr_category", "epc", "bungalow"):
        if m.get(fld) in (None, "") and s.get(fld) not in (None, ""): m[fld] = s[fld]
    if s.get("postcode") and len(s["postcode"]) > len(m.get("postcode") or ""): m["postcode"] = s["postcode"]
sales = list(merged.values())
for s in sales:
    s["age"] = age_band(s["date"])
    s["indexed"] = index(s["price"], s["date"], s["type"])
    a = s.get("floor_area_m2")
    s["ppm2"] = round((s["indexed"] or s["price"]) / a) if a else None
    s["standard"] = s.get("lr_category") != "B"

facts = json.loads((ROOT / "facts.json").read_text())
nums = yaml.safe_load((ROOT / "numbers.yaml").read_text())["houses"]
houses = yaml.safe_load((ROOT / "houses.yaml").read_text())["houses"]

def fval(h, field):
    for f in facts.get(h, {}).get(field, []):
        if f["value"] is not None: return f
    return None

def ring(rows):
    v = sorted(r["ppm2"] for r in rows if r["ppm2"])
    p = sorted(r["indexed"] or r["price"] for r in rows)
    top = max(rows, key=lambda r: r["indexed"] or r["price"], default=None)
    n, na = len(rows), len(v)
    return {"n": n, "n_with_area": na,
            "thin": n < 3 or na < 3,
            "median_ppm2": round(st.median(v)) if v else None, "spread_ppm2": [v[0], v[-1]] if v else None,
            "top_ppm2": v[-1] if v else None,
            "median_price_today": round(st.median(p)) if p else None,
            "top_price_today": top and (top["indexed"] or top["price"]), "top_address": top and top["address"],
            "sales": [{k: r.get(k) for k in ("address", "date", "age", "price", "indexed", "tenure", "floor_area_m2", "ppm2", "source")}
                      for r in sorted(rows, key=lambda r: r["date"], reverse=True)]}

summary = {}
for h in houses:
    hid = h["id"]; n = nums[hid]; typ = n["lr_type"]
    num = h["address"].split()[0]
    street = " ".join(h["address"].split(",")[0].split()[1:]).upper()
    own_key = f"{num} {street}"
    pool = [s for s in sales if s["type"] == typ and s["standard"] and dt.date.fromisoformat(s["date"]) >= SINCE
            and key_addr(s["address"]) != own_key]
    if hid == "welby":     # a bungalow: only bungalows are like for like; houses kept separately
        same_street = [s for s in pool if street in s["address"].upper()]
    else:
        same_street = [s for s in pool if street in s["address"].upper()]
    same_pc = [s for s in pool if (s.get("postcode") or "").upper() == h["postcode"].upper()]
    # own last sale
    own = fval(hid, "own_past_sales")
    last = None
    if own and own["value"]:
        o = max(own["value"], key=lambda x: x["date"])
        last = {"date": o["date"], "age": age_band(o["date"]), "price": o["price"], "type": o.get("type"),
                "today": index(o["price"], o["date"], o.get("type") or typ), "source": own["source"]}
    ceil = fval(hid, "street_highest_price")
    ceiling = ceil and {"price": ceil["value"], "note": ceil.get("note", ""), "source": ceil["source"]}
    # listing
    prices = n["prices"]; first = dt.date.fromisoformat(prices[0]["date"])
    cuts = [p for a, p in zip(prices, prices[1:]) if p["price"] < a["price"]]
    area, ask = n["area_m2"], n["asking"]
    summary[hid] = {
        "type": typ, "area_m2": area, "area_m2_high": n.get("area_m2_high"), "asking": ask, "asking_high": n.get("asking_high"),
        "asking_ppm2": round(ask / area),
        "asking_ppm2_alt": round(ask / n["area_m2_high"]) if n.get("area_m2_high") else
                           (round(n["asking_high"] / area) if n.get("asking_high") else None),
        "street": ring(same_street), "postcode": ring(same_pc),
        "street_ceiling_ever": ceiling, "last_sale": last,
        "first_listed": prices[0]["date"], "days_on_market": (TODAY - first).days,
        "first_price": prices[0]["price"], "cuts": len(cuts),
        "cut_pct": round(100 * (prices[0]["price"] - ask) / prices[0]["price"], 1) if cuts else 0.0,
    }

out = ROOT / "out/comps"; out.mkdir(parents=True, exist_ok=True)
(out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
by_sector = {}
for s in sales: by_sector.setdefault((s.get("postcode") or "")[:4].replace(" ", ""), []).append(s)
cols = ["address", "postcode", "date", "age", "price", "indexed", "type", "tenure", "lr_category", "new_build",
        "floor_area_m2", "ppm2", "area_source", "source"]
for sec, rows in by_sector.items():
    if not sec: continue
    with open(out / f"{sec}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader(); w.writerows(sorted(rows, key=lambda r: r["date"]))

def gbp(x): return f"£{x:,.0f}" if x is not None else "–"
def rng(r):
    if not r["median_ppm2"]: return f"no £/m² (n={r['n']}, {r['n_with_area']} with area)"
    return (f"{gbp(r['median_ppm2'])} ({gbp(r['spread_ppm2'][0])}–{gbp(r['spread_ppm2'][1])}); "
            f"n={r['n']}, {r['n_with_area']} with area" + (" **THIN**" if r["thin"] else ""))
L = [f"# Comparables by house\n\n*comps.py, run {TODAY}. Same Land Registry type, standard sales only, since {SINCE}, "
     f"brought to {LATEST} with the Sheffield UK HPI by type. Thin = fewer than 3 such sales, or fewer than 3 with a floor area.*\n",
     "| House | Asking £/m² | Street £/m², today | Postcode £/m², today | Street ceiling ever | Last sale → today | Days listed | Cuts |",
     "|---|---|---|---|---|---|---|---|"]
for hid, s in summary.items():
    ls = s["last_sale"]
    lst = f"{gbp(ls['price'])} ({ls['date'][:7]}) → {gbp(ls['today'])}" if ls else "none since 1995"
    ce = s["street_ceiling_ever"]
    L.append(f"| {hid} | {gbp(s['asking_ppm2'])}" + (f" / {gbp(s['asking_ppm2_alt'])}" if s["asking_ppm2_alt"] else "") +
             f" | {rng(s['street'])} | {rng(s['postcode'])} | {gbp(ce['price']) if ce else '–'} | {lst} | "
             f"{s['days_on_market']} | {s['cuts']} ({s['cut_pct']}%) |")
(out / "houses.md").write_text("\n".join(L) + "\n")
print(f"{len(sales)} sales after merge ({len(raw)} lines), HPI to {LATEST} -> out/comps/")
print("\n".join(L[3:]))
