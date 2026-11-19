#!/usr/bin/env python3
"""Value as it stands = floor area × comparable £/m² (same type, street ring, else postcode ring), today's money.
Central = median £/m²; range = lower to upper quartile. Thin rings are reported, not stretched.
Done-up margin (house-hunt buy test) = 0.9V − 1.15W − C − asking, C = £3,000 fees (+ stamp duty above £300k).
Reads out/comps/summary.json and numbers.yaml (optional 'doneup' block). Writes out/value.md and out/value.json."""
import json, statistics as st
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "out/comps/summary.json").read_text())
N = yaml.safe_load((ROOT / "numbers.yaml").read_text())["houses"]
gbp = lambda x: f"£{x:,.0f}"

def sdlt_ftb(p):   # first-time buyer: nil to £300k, 5% to £500k
    return 0.05 * max(0, min(p, 500000) - 300000)

def quart(rows):
    v = sorted(r["ppm2"] for r in rows if r["ppm2"])
    if len(v) < 3: return None
    q1, q2, q3 = st.quantiles(v, n=4, method="inclusive")
    return round(q1), round(q2), round(q3), len(v)

res, md = {}, ["# Value as it stands, and done-up margins\n",
               "*value.py. Area × comparable £/m² (same type, sold since 19 Nov 2023, brought to Sep 2026). "
               "Central = median; range = lower–upper quartile. Thin = fewer than 3 sales with a floor area: not stretched.*\n"]
for hid, s in S.items():
    a = s["area_m2"]; r = {"area_m2": a}
    ring = None
    for name in ("street", "postcode"):
        q = quart(s[name]["sales"])
        if q: ring = (name, q); break
    if ring:
        name, (q1, q2, q3, n) = ring
        r.update(ring=name, n=n, ppm2=[q1, q2, q3], value=[a * q1, a * q2, a * q3])
        md.append(f"## {hid}\n- {a} m² × {name} £/m² {gbp(q1)} / **{gbp(q2)}** / {gbp(q3)} (quartiles of {n} sales) "
                  f"= {gbp(a*q1)} / **{gbp(a*q2)}** / {gbp(a*q3)}.")
        if s.get("area_m2_high"):
            b = s["area_m2_high"]; r["value_high_area"] = [b * q1, b * q2, b * q3]
            md.append(f"- At the listing's {b} m²: {gbp(b*q1)} / {gbp(b*q2)} / {gbp(b*q3)}.")
    else:
        one = [x for x in s["street"]["sales"] + s["postcode"]["sales"] if x["ppm2"]]
        r.update(ring=None, thin=True, single=[{"address": x["address"], "ppm2": x["ppm2"], "value": a * x["ppm2"]} for x in one])
        md.append(f"## {hid}\n- **Too thin for a £/m² value** ({s['street']['n']} same-type street sales, "
                  f"{s['street']['n_with_area']} with area)." +
                  ("".join(f" Single sale: {x['address']} at {gbp(x['ppm2'])}/m² → {a} m² × {gbp(x['ppm2'])} = {gbp(a*x['ppm2'])}."
                           for x in {y['address']: y for y in one}.values())))
    d = N[hid].get("doneup")
    if d:
        ask = N[hid]["asking"]; C = 3000 + sdlt_ftb(ask)
        lo = 0.9 * d["V"][0] - 1.15 * d["W"][1] - C - ask
        hi = 0.9 * d["V"][1] - 1.15 * d["W"][0] - C - ask
        mx = [0.9 * d["V"][0] - 1.15 * d["W"][1] - C, 0.9 * d["V"][1] - 1.15 * d["W"][0] - C]
        r.update(doneup=d, margin=[round(lo), round(hi)], most_to_offer=[round(mx[0]), round(mx[1])])
        md.append(f"- Done-up V {gbp(d['V'][0])}–{gbp(d['V'][1])}, works W {gbp(d['W'][0])}–{gbp(d['W'][1])} ({d['why']}). "
                  f"Margin = 0.9V − 1.15W − {gbp(C)} − {gbp(ask)} = **{gbp(lo)} to {gbp(hi)}**. "
                  f"Most to offer (0.9V − 1.15W − C) = {gbp(mx[0])}–{gbp(mx[1])}.")
    res[hid] = r
(ROOT / "out/value.json").write_text(json.dumps(res, indent=1))
(ROOT / "out/value.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
