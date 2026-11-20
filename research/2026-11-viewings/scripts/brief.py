#!/usr/bin/env python3
"""Render each house's phone brief -> out/briefs/<id>.md, plus the agent's inputs.

Rendered by script (never by an agent):
  - Numbers: wave 2's figures from out/comps/summary.json, out/value.json, numbers.yaml (done-up margins),
    out/welby/bungalow_ratio.md (Welby), and the rulings in settled.yaml.
  - out/briefs/<id>.facts.md: every fact line for the house, non-null first, with source.
  - out/briefs/<id>.comps.md: the house's comparables, sale by sale.
Written by the wave 3 agent: out/briefs/<id>.agent.md, with the headings in AGENT_PARTS plus '### Working'.
  If it exists, its parts are merged into the brief; if not, the brief shows placeholders.
Usage: brief.py            render all seven
       brief.py --combine  also write out/briefs/all.md, in viewing order
"""
import json, re, sys
from datetime import date
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out/briefs"
OUT.mkdir(parents=True, exist_ok=True)
TPL = (ROOT / "templates/brief.md").read_text()
FACTS = json.loads((ROOT / "facts.json").read_text())
COMPS = json.loads((ROOT / "out/comps/summary.json").read_text())
VALUE = json.loads((ROOT / "out/value.json").read_text())
NUMS = yaml.safe_load((ROOT / "numbers.yaml").read_text())["houses"]
RULINGS = yaml.safe_load((ROOT / "settled.yaml").read_text())
HOUSES = yaml.safe_load((ROOT / "houses.yaml").read_text())["houses"]
TYPE = {"D": "detached", "S": "semi", "T": "terrace"}
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
AGENT_PARTS = {"Levers": "levers", "Ask": "questions",
               "Check": "checks", "Red flags": "red_flags", "Never say": "never_say"}


def k(x):
    """£ to the nearest £1k, as £251k."""
    return f"£{round(x / 1000):,}k"


def gbp(x):
    return f"£{x:,}" if x >= 0 else f"−£{-x:,}"


def mon(d):
    y, m = d[:7].split("-")
    return f"{MON[int(m) - 1]} {y}"


def no(addr):
    """'33 Falmouth Road, Sheffield' -> 'No. 33'."""
    m = re.match(r"(\d+[A-Za-z]?)\s", addr or "")
    return f"No. {m.group(1)}" if m else addr


def first_sentence(s):
    return re.split(r"(?<=[.;])\s|\s-\s|\s—\s", s.strip())[0].rstrip(".;")


def welby_model():
    md = (ROOT / "out/welby/bungalow_ratio.md").read_text()
    row = lambda start: [c.strip() for c in next(l for l in md.splitlines() if l.startswith(start)).split("|")[1:-1]]
    allr, wp = row("| All sales 2016"), row("| Welby Place only")
    num = lambda x: int(re.sub(r"[^\d]", "", x))
    lo, hi = [num(x) for x in wp[5].split("–")]
    return (f"- Bungalow model: **{k(num(allr[4]))}–{k(num(wp[4]))}** as it stands; "
            f"likely range {k(lo)}–{k(hi)} on Welby Place sales alone (out/welby/bungalow_ratio.md)")


def numbers(h):
    hid = h["id"]
    c, v, n = COMPS[hid], VALUE[hid], NUMS[hid]
    t = TYPE[c["type"]]
    lines = []
    area = f"- Area: **{c['area_m2']} m²**"
    if c.get("area_m2_high"):
        area += f" (listing says {c['area_m2_high']} m²; work on the smaller)"
    area += f" · asking {gbp(c['asking_ppm2'])}/m²"
    if c.get("asking_high"):
        area += f" ({gbp(round(c['asking_high'] / c['area_m2']))}/m² at {k(c['asking_high'])})"
    lines.append(area)
    s = c["street"]
    if v.get("ring"):
        lo, mid, hi = v["value"]
        lines.append(f"- Value as it stands: **{k(lo)} / {k(mid)} / {k(hi)}** "
                     f"({v['n']} street {t} sales with area; {gbp(v['ppm2'][0])} / {gbp(v['ppm2'][1])} / {gbp(v['ppm2'][2])} per m²)")
    elif hid == "welby":
        lines.append(f"- Comparables **thin**: no detached sale on the street since Nov 2021")
        lines.append(welby_model())
    else:
        lines.append(f"- Comparables **thin**: {s['n']} {t} sale{'s' if s['n'] != 1 else ''} on the street since Nov 2023, {s['n_with_area']} with area. No £/m² value")
        if v.get("single"):
            one = v["single"][0]
            lines.append(f"- One sale only: {no(one['address'])} at {gbp(one['ppm2'])}/m² → {gbp(one['value'])} at {c['area_m2']} m²")
    if c.get("last_sale"):
        ls = c["last_sale"]
        lines.append(f"- Last sold {gbp(ls['price'])} ({mon(ls['date'])}) → **{gbp(ls['today'])} today**")
    else:
        lines.append("- Last sold: none on Land Registry since 1995")
    ce = c["street_ceiling_ever"]
    note = re.sub(r"\s*\(S\d+ \d\w\w\)", "", first_sentence(ce["note"])).replace(" (", ", ").replace(")", "")
    if "outlier" in ce["note"]:
        note += "; an outlier"
    lines.append(f"- Street's top price ever: {gbp(ce['price'])} ({note})")
    cut = f"{c['cuts']} cut{'s' if c['cuts'] > 1 else ''} ({c['cut_pct']}% in all)" if c["cuts"] else "no cut"
    lines.append(f"- Listed {date.fromisoformat(c['first_listed']).strftime('%-d %b %Y')} at {gbp(c['first_price'])}: "
                 f"{c['days_on_market']} days by 19 Nov, {cut}")
    if v.get("doneup"):
        V, m, mo = v["doneup"]["V"], v["margin"], v["most_to_offer"]
        lines.append(f"- Done-up value {k(V[0])}–{k(V[1])}; buy-test margin at asking {gbp(m[0])} to {gbp(m[1])}")
    tr = [r for r in RULINGS if r["key"].replace(" ", "") == f"{hid}/tenure"]
    if tr:
        w = first_sentence(tr[0]["winner"]).lower()
        m = re.match(r"(.*?)\s*\((.*)\)$", w)
        lines.append(f"- Tenure: {m[1]} (ruled in wave 2; {m[2]})" if m else f"- Tenure: {w} (ruled in wave 2)")
    else:
        ten = [f for f in FACTS[hid].get("tenure_lr", []) if f["value"]]
        if ten:
            tv = {"F": "freehold", "L": "leasehold"}.get(ten[0]["value"], ten[0]["value"])
            lines.append(f"- Tenure: {tv} (Land Registry)")
    return "\n".join(lines)


def fmt(v):
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s.replace("|", "/").replace("\n", " ")


def facts_md(h):
    hid = h["id"]
    rows = [f"# Fact lines: {h['address']}", "", "| Field | Value | Task | Conf. | Source |", "|---|---|---|---|---|"]
    nulls = []
    for field, fs in sorted(FACTS.get(hid, {}).items()):
        for f in fs:
            if f["value"] is None:
                nulls.append(f"- {field} ({f['task']}): {fmt(f.get('note', ''))[:200]}")
            else:
                note = f" — {fmt(f['note'])}" if f.get("note") else ""
                rows.append(f"| {field} | {fmt(f['value'])}{note} | {f['task']} | {f['confidence']} | {f['source']} |")
    rows += ["", "## Not found (null lines)", *nulls]
    rows += ["", "## Wave 2 rulings on clashes (settled.yaml)"]
    for r in RULINGS:
        if r["key"].split("/")[0].strip() in (hid, "market"):
            rows.append(f"- **{r['key']}**: {r['winner']}. Why: {r['why']}")
    rows += ["", "## Market (shared by all houses)", "", "| Field | Value | Source |", "|---|---|---|"]
    for field, fs in sorted(FACTS.get("market", {}).items()):
        for f in fs:
            if f["value"] is not None:
                note = f" — {fmt(f['note'])}" if f.get("note") else ""
                rows.append(f"| {field} | {fmt(f['value'])}{note} | {f['source']} |")
    return "\n".join(rows) + "\n"


def comps_md(h):
    hid = h["id"]
    c, v = COMPS[hid], VALUE[hid]
    out = [f"# Comparables: {h['address']}", "",
           "*From out/comps/summary.json and out/value.json (comps.py, value.py). Prices 'today' = Sep 2026, Sheffield UK HPI by type.*", "",
           "```json", json.dumps({k_: x for k_, x in c.items() if k_ not in ("street", "postcode")}, indent=1, ensure_ascii=False), "```",
           "", "value.json:", "```json", json.dumps(v, indent=1, ensure_ascii=False), "```"]
    for ring in ("street", "postcode"):
        r = c[ring]
        out += ["", f"## {ring}: n={r['n']}, with area {r['n_with_area']}, thin={r['thin']}, "
                    f"median £/m² {r['median_ppm2']}, spread {r['spread_ppm2']}, top {r['top_ppm2']}",
                "", "| Address | Date | Price | Today | Tenure | m² | £/m² today | Source |", "|---|---|---|---|---|---|---|---|"]
        for x in r["sales"]:
            out.append(f"| {x['address']} | {x['date']} | {x['price']} | {x['indexed']} | {x['tenure']} | "
                       f"{x['floor_area_m2']} | {x['ppm2']} | {x['source']} |")
    if hid in NUMS and NUMS[hid].get("doneup"):
        out += ["", "numbers.yaml done-up inputs:", "```yaml", yaml.safe_dump(NUMS[hid]["doneup"], allow_unicode=True), "```"]
    return "\n".join(out) + "\n"


def agent_parts(hid):
    p = OUT / f"{hid}.agent.md"
    parts = {v: "*(wave 3 agent: not written)*" for v in AGENT_PARTS.values()}
    if not p.exists():
        return parts, False
    cur = None
    buf = {}
    for ln in p.read_text().splitlines():
        m = re.match(r"^###\s+(.+?)\s*$", ln)
        if m:
            cur = m.group(1)
            buf[cur] = []
        elif cur:
            buf[cur].append(ln)
    for head, key in AGENT_PARTS.items():
        if head in buf:
            parts[key] = "\n".join(buf[head]).strip()
    return parts, True


def render():
    order = sorted(HOUSES, key=lambda h: h["viewing"])
    briefs = []
    for i, h in enumerate(order, 1):
        hid = h["id"]
        (OUT / f"{hid}.facts.md").write_text(facts_md(h))
        (OUT / f"{hid}.comps.md").write_text(comps_md(h))
        parts, done = agent_parts(hid)
        when = h["viewing"][11:]
        text = TPL.format(n=i, address=h["address"].replace(", Sheffield", ""), time=when,
                          price_text=h["price_text"], agent=h["agent"], postcode=h["postcode"],
                          numbers=numbers(h), **parts)
        (OUT / f"{hid}.md").write_text(text)
        briefs.append(text)
        print(f"wrote {hid}.md ({len(text.split())} words){'' if done else ' — agent parts missing'}")
    if "--combine" in sys.argv:
        head = ("# Saturday briefs: 21 Nov 2026\n\n"
                "*Wave 3, written 20 Nov 2026. One brief per house, in viewing order. Numbers: wave 2 scripts "
                "(repo `McGoughBill/house-hunt`, branch `research-nov-viewings`, `research/2026-11-viewings/`). "
                "Due diligence only: facts, levers, questions and checks; no verdicts or offer figures. Keep every figure here from the agent.*\n")
        (OUT / "all.md").write_text(head + "\n---\n\n" + "\n---\n\n".join(briefs))
        print("wrote all.md")


if __name__ == "__main__":
    render()
