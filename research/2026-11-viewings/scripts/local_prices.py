#!/usr/bin/env python3
"""Wave 4: render a 'Local prices' block per house from the W4C fact lines in facts.json.
local_prices.py -> prints blocks; imported by apply_w4.py."""
import json, re
from pathlib import Path
from datetime import date
ROOT = Path(__file__).resolve().parent.parent
TYPE = {"T": "terrace", "S": "semi", "D": "detached"}
TEN = {"F": "freehold", "L": "leasehold"}
SECTOR = {"falmouth": "S7 2", "welby": "S8 9", "leeshall": "S8 9", "cawthorne": "S8 0", "underwood": "S8 8", "helmton": "S8 8", "hollythorpe": "S8 9"}
TYPEW = {"falmouth": "terraces", "welby": "detached", "leeshall": "semis", "cawthorne": "semis", "underwood": "terraces", "helmton": "semis", "hollythorpe": "semis"}


def mon(d):
    y, m, _ = map(int, d.split("-")); return date(y, m, 1).strftime("%b %Y")


def k(x):
    return f"£{round(x / 1000):,}k"


def short(addr):
    a = re.sub(r",\s*Sheffield.*", "", addr)
    a = re.sub(r"^(\d+[A-Z]?) ", r"No. \1, ", a)
    return a.replace(" Road", " Rd").replace(" Place", " Pl").replace(" Grove", " Gr").replace(" Drive", " Dr")


def age(a):
    a = a.replace(" yrs", "").replace(" yr", "").replace("-", "–")
    return "<1 yr" if a == "<1" else a + " yrs"


def diff(c):
    d = re.sub(r",?\s*(free|lease)hold,?", "", c["differs"]).strip(" ,;")
    d = re.sub(r"(size unknown|same size)", "", d).strip(" ,;")
    return d or "–"


def block(hid, facts):
    h = [f for v in facts[hid].values() for f in v if f.get("task") == "W4C"] or \
        [f for v in facts[hid].values() for f in v if f.get("field") in ("comparable", "street_top_price_ever", "area_top_price_same_type")]
    comps = [f["value"] for f in h if f["field"] == "comparable"]
    st = next(f["value"] for f in h if f["field"] == "street_top_price_ever")
    at = next(f for f in h if f["field"] == "area_top_price_same_type")
    out = ["**Local prices [W4]** (Land Registry; ≈ = in today's money, Sheffield index by type to Sep 2026; all same-street sales, step 1)"]
    for c in sorted(comps, key=lambda c: c["date"], reverse=True):
        dist = "same postcode" if not c.get("distance_m") else f"{c['distance_m']} m"
        area = f"{c['floor_area_m2']:g} m²" if c.get("floor_area_m2") else "area unknown"
        out.append(f"- {short(c['address'])} · {mon(c['date'])} · £{c['price']:,} (≈ {k(c['value_today'])}) · {age(c['age_band'])} · "
                   f"{TYPE.get(c['type'], c['type'])}, {TEN.get(c['tenure'], c['tenure'])} · {area} · {dist} · {diff(c)}")
    out.append(f"- Street top: £{st['price']:,}, {short(st['address'])} ({TYPE.get(st['type'])}, {TEN.get(st['tenure'])}), {mon(st['date'])} (≈ {k(st['value_today'])})")
    v = at["value"]
    doubt = "; type doubtful, also filed as a semi" if hid == "underwood" else ""
    out.append(f"- Area top, {SECTOR[hid]} {TYPEW[hid]}: £{v['price']:,}, {short(v['address'])}, "
               f"{mon(v['date'])} (≈ {k(v['value_today'])}; medium{doubt})")
    return "\n".join(out)


if __name__ == "__main__":
    f = json.loads((ROOT / "facts.json").read_text())
    for hid in SECTOR:
        print(block(hid, f), "\n")
