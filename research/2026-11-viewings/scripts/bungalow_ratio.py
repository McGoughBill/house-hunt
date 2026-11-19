#!/usr/bin/env python3
"""Bungalow vs house price per m², and what it implies for 50 Welby Place.
Reads data/bungalow_sales.csv and data/hpi_sheffield_ukhpi.csv (UK HPI, Sheffield, by type).
Model, fitted by least squares on sales indexed to the latest HPI month:
    ln(price_today) = area_effect + b * ln(m²) + c * bungalow
exp(c) is the size-adjusted bungalow premium; b < 1 means small homes cost more per m².
50 Welby itself is left out of the fit, then predicted. Writes out/welby/bungalow_ratio.md."""
import csv, math, datetime as dt
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date(2026, 11, 19)
COL = {"D": "detached", "S": "semi_detached", "T": "terraced", "F": "flat"}
hpi = list(csv.DictReader(open(ROOT / "data/hpi_sheffield_ukhpi.csv")))
H = {r["month"]: r for r in hpi}
LATEST = hpi[-1]["month"]

def age_band(d):
    y = (TODAY - d).days / 365.25
    return "6+ yrs" if y >= 6 else f"{int(y)}–{int(y)+1} yrs" if y >= 1 else "<1 yr"

def index(price, d, t):
    c = COL[t]
    return price * float(H[LATEST][c]) / float(H[d.strftime("%Y-%m")][c])

rows = []
for r in csv.DictReader(open(ROOT / "data/bungalow_sales.csv")):
    d = dt.date.fromisoformat(r["date"])
    r["d"], r["price"], r["m2"] = d, int(r["price"]), float(r["m2"])
    r["idx"] = index(r["price"], d, r["lr_type"])
    r["ppm2"], r["ppm2_idx"], r["age"] = r["price"] / r["m2"], r["idx"] / r["m2"], age_band(d)
    rows.append(r)

areas = sorted({r["area"] for r in rows})
def fit(data):
    global areas
    areas = sorted({r["area"] for r in data})
    X = [[1.0 if r["area"] == a else 0.0 for a in areas] + [math.log(r["m2"]), 1.0 if r["group"] == "bungalow" else 0.0] for r in data]
    X, y = np.array(X), np.array([math.log(r["idx"]) for r in data])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (len(y) - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    return beta, cov, math.sqrt(s2)

def predict(beta, cov, s, area, m2, bung):
    x = np.array([1.0 if a == area else 0.0 for a in areas] + [math.log(m2), 1.0 if bung else 0.0])
    mu, se_mean = x @ beta, math.sqrt(x @ cov @ x)
    se_pred = math.sqrt(se_mean**2 + s**2)
    return math.exp(mu), math.exp(mu - 1.96 * se_mean), math.exp(mu + 1.96 * se_mean), math.exp(mu - 1.96 * se_pred), math.exp(mu + 1.96 * se_pred)

def report(data, label):
    beta, cov, s = fit(data)
    b, c = beta[-2], beta[-1]
    se_c = math.sqrt(cov[-1, -1])
    p = predict(beta, cov, s, "welby_place", 60, True)
    return dict(label=label, n=len(data), nb=sum(r["group"] == "bungalow" for r in data), b=b, prem=math.exp(c),
                prem_lo=math.exp(c - 1.96 * se_c), prem_hi=math.exp(c + 1.96 * se_c), s=s, pred=p)

train = [r for r in rows if r["address"] != "50 Welby Place"]
runs = [report(train, "All sales 2016–26, 50 Welby left out"),
        report([r for r in train if (TODAY - r["d"]).days < 5 * 365.25], "Sales under 5 years old"),
        report([r for r in train if r["area"] == "welby_place"], "Welby Place only")]

# Raw ratio by area, recent only, no size control
raw = []
for a in sorted({r["area"] for r in rows}):
    for lab, cut in [("all", 99), ("<5 yrs", 5)]:
        g = lambda grp: [r["ppm2_idx"] for r in train if r["area"] == a and r["group"] == grp and (TODAY - r["d"]).days < cut * 365.25]
        bu, ho = g("bungalow"), g("house")
        if bu and ho:
            raw.append((a, lab, len(bu), np.median(bu), len(ho), np.median(ho), np.median(bu) / np.median(ho),
                        np.mean([r["m2"] for r in train if r["area"] == a and r["group"] == "bungalow"]),
                        np.mean([r["m2"] for r in train if r["area"] == a and r["group"] == "house"])))

own = next(r for r in rows if r["address"] == "50 Welby Place")
L = [f"# 50 Welby Place: bungalow-to-house pricing\n",
     f"*Built {TODAY:%d %b %Y} by `scripts/bungalow_ratio.py`. Prices brought to {LATEST} with the official UK House Price Index for Sheffield, by house type (Land Registry). Floor areas from energy certificates via HouseMetric.*\n",
     "## Size-adjusted model\n",
     "ln(price today) = street effect + b·ln(m²) + bungalow premium. 50 Welby is left out of the fit, then priced at 60 m².\n",
     "| Sample | Sales (bungalows) | b (size) | Bungalow premium, 95% range | Welby at 60 m²: central | Likely range (95%, mean) | Range for one sale (95%) |",
     "|---|---|---|---|---|---|---|"]
for r in runs:
    c, lo, hi, plo, phi = r["pred"]
    L.append(f"| {r['label']} | {r['n']} ({r['nb']}) | {r['b']:.2f} | ×{r['prem']:.2f} (×{r['prem_lo']:.2f}–×{r['prem_hi']:.2f}) | £{c:,.0f} | £{lo:,.0f}–£{hi:,.0f} | £{plo:,.0f}–£{phi:,.0f} |")
L += ["\n## Raw £/m² ratio (no size control, in today's money)\n",
      "| Street | Sales used | Bungalows: n, median £/m² | Houses: n, median £/m² | Ratio | Mean size: bungalow vs house |", "|---|---|---|---|---|---|"]
for a, lab, nb, mb, nh, mh, ratio, sb, sh in raw:
    L.append(f"| {a.replace('_',' ')} | {lab} | {nb}, £{mb:,.0f} | {nh}, £{mh:,.0f} | ×{ratio:.2f} | {sb:.0f} vs {sh:.0f} m² |")
L += ["\n## 50 Welby's own sale\n",
      f"Bought {own['d']:%d %b %Y} for £{own['price']:,}: £{own['ppm2']:,.0f}/m². Indexed by the Sheffield detached series to {LATEST}: **£{own['idx']:,.0f}** (£{own['ppm2_idx']:,.0f}/m²). Age: {own['age']}.\n",
      "## Every sale used, with its age\n",
      "| Street | Address | Sold | Age | Price | m² | £/m² paid | £/m² today | Group | Note |", "|---|---|---|---|---|---|---|---|---|---|"]
for r in sorted(rows, key=lambda r: (r["area"], r["d"]), reverse=True):
    L.append(f"| {r['area'].replace('_',' ')} | [{r['address']}]({r['source']}) | {r['d']:%b %Y} | {r['age']} | £{r['price']:,} | {r['m2']:.0f} | £{r['ppm2']:,.0f} | £{r['ppm2_idx']:,.0f} | {r['group']} | {r['bungalow_evidence']} |")
(ROOT / "out/welby/bungalow_ratio.md").write_text("\n".join(L) + "\n")
print("\n".join(L[:12])); print("\n".join(L[12:20])); print(L[20:23])
