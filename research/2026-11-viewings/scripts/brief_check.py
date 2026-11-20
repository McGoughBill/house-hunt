#!/usr/bin/env python3
"""Check every £ figure, m² figure and date in each brief against the sources.

A figure passes if it matches a number or date in: facts.json (the house's lines and the market lines, values and notes),
the comps output (out/comps/summary.json, out/value.json, numbers.yaml, settled.yaml; for Welby also
out/welby/bungalow_ratio.md), or a line of the agent's own '### Working' that shows a sum or a source.
Rounding: '£251k' matches anything within £500; '£292.5k' within £50; '£3,644' within £1; '69 m²' within 0.5 m².
Dates: '19 Nov 2021' needs that day; 'Nov 2021' needs that month; ISO dates likewise.

Usage: brief_check.py [house ...]   -> prints unmatched figures per house; exit 1 if any.
"""
import json, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
BR = ROOT / "out/briefs"
MON = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
NUM = r"\d[\d,]*(?:\.\d+)?"


def to_f(s):
    return float(s.replace(",", ""))


def pool_numbers(text):
    """Every number in a source text, with k/m suffixes expanded and £/m² forms kept as plain numbers."""
    out = set()
    for m in re.finditer(rf"({NUM})\s?(k|m)?\b", text):
        try:
            x = to_f(m.group(1))
        except ValueError:
            continue
        out.add(x)
        if m.group(2) == "k":
            out.add(x * 1000)
        elif m.group(2) == "m" and x < 50:
            out.add(x * 1_000_000)
    return out


def pool_dates(text):
    """Set of (y, m, d) and (y, m, None) for every date in a source text."""
    out = set()
    for y, m, d in re.findall(r"\b(\d{4})-(\d{2})(?:-(\d{2}))?\b", text):
        out.add((int(y), int(m), int(d) if d else None)); out.add((int(y), int(m), None))
    for d, mo, y in re.findall(r"\b(?:(\d{1,2})\s+)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{4})\b", text, re.I):
        mm = MON[mo.lower()[:3]]
        out.add((int(y), mm, None))
        if d:
            out.add((int(y), mm, int(d)))
    return out


def sources_text(hid):
    facts = json.loads((ROOT / "facts.json").read_text())
    parts = [json.dumps(facts.get(hid, {}), ensure_ascii=False), json.dumps(facts.get("market", {}), ensure_ascii=False)]
    parts.append(json.dumps(json.loads((ROOT / "out/comps/summary.json").read_text()).get(hid, {}), ensure_ascii=False))
    parts.append(json.dumps(json.loads((ROOT / "out/value.json").read_text()).get(hid, {}), ensure_ascii=False))
    parts.append(json.dumps(yaml.safe_load((ROOT / "numbers.yaml").read_text())["houses"].get(hid, {}), default=str, ensure_ascii=False))
    parts.append("\n".join(json.dumps(r, ensure_ascii=False) for r in yaml.safe_load((ROOT / "settled.yaml").read_text())
                           if r["key"].split("/")[0].strip() in (hid, "market")))
    if hid == "welby":
        parts.append((ROOT / "out/welby/bungalow_ratio.md").read_text())
    return "\n".join(parts)


def working_text(hid):
    p = BR / f"{hid}.agent.md"
    if not p.exists():
        return "", []
    t = p.read_text()
    m = re.search(r"(?ms)^### Working\s*\n(.*?)(?=^### |\Z)", t)
    if not m:
        return "", []
    lines = [l for l in m.group(1).splitlines() if l.strip()]
    shown = [l for l in lines if re.search(r"[=×÷]|\best(imate)?\b|\[|source|from |per |http", l, re.I)]
    weak = [l for l in lines if l not in shown]
    return "\n".join(shown), weak


def brief_figures(text):
    """Yield (kind, value, tol, raw) for £, m² and dates in a brief."""
    text = text.replace("−", "-").replace("–", "-")
    # £ ranges like £245-250k or £213k-£235k: give the unit of the second to the first
    for m in re.finditer(rf"£({NUM})(k|m)?(-£?|\s-\s£)({NUM})(k|m)?(?![\d.,]*\s?(?:m²|%))", text):
        a, ua, b, ub = m.group(1), m.group(2), m.group(4), m.group(5)
        ua = ua or ub
        for v, u in ((a, ua), (b, ub)):
            yield ("£",) + money(v, u) + (m.group(0),)
    spans = [m.span() for m in re.finditer(rf"£({NUM})(k|m)?(-£?|\s-\s£)({NUM})(k|m)?(?![\d.,]*\s?(?:m²|%))", text)]
    for m in re.finditer(rf"£({NUM})(k|m)?", text):
        if any(s <= m.start() < e for s, e in spans):
            continue
        yield ("£",) + money(m.group(1), m.group(2)) + (m.group(0),)
    for m in re.finditer(rf"(?<![/£\d,.])({NUM})\s?m²", text):
        yield ("m²", to_f(m.group(1)), 0.5, m.group(0))
    for m in re.finditer(r"\b(?:(\d{1,2})\s+)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{4})\b", text):
        d, mo, y = m.groups()
        yield ("date", (int(y), MON[mo.lower()[:3]], int(d) if d else None), 0, m.group(0))
    for m in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", text):
        yield ("date", (int(m.group(1)), int(m.group(2)), int(m.group(3))), 0, m.group(0))


def money(v, u):
    x = to_f(v)
    if u == "k":
        return x * 1000, (50 if "." in v else 500)
    if u == "m":
        return x * 1_000_000, 5000
    return x, 1


def check(hid):
    brief = (BR / f"{hid}.md").read_text()
    src = sources_text(hid)
    work, weak = working_text(hid)
    # The rendered brief's own Numbers block is built from these same sources by brief.py, so it is checked too.
    nums_src, nums_work = pool_numbers(src), pool_numbers(work)
    dates_src, dates_work = pool_dates(src), pool_dates(work)
    bad, via_work = [], 0
    seen = set()
    for kind, val, tol, raw in brief_figures(brief):
        key = (kind, val, raw)
        if key in seen:
            continue
        seen.add(key)
        if kind == "date":
            ok_s = val in dates_src
            ok_w = val in dates_work
        else:
            ok_s = any(abs(abs(val) - a) <= tol for a in nums_src)
            ok_w = any(abs(abs(val) - a) <= tol for a in nums_work)
        if ok_s:
            continue
        if ok_w:
            via_work += 1
            continue
        bad.append(raw)
    return bad, via_work, weak


def main():
    ids = sys.argv[1:] or [p.stem for p in sorted(BR.glob("*.md")) if "." not in p.stem and p.stem != "all"]
    total = 0
    for hid in ids:
        bad, via_work, weak = check(hid)
        total += len(bad)
        words = len(re.sub(r"(?ms)^### Working.*", "", (BR / f"{hid}.md").read_text()).split())
        print(f"{hid}: {len(bad)} unmatched; {via_work} matched only by the agent's working; {words} words")
        for b in bad:
            print(f"   UNMATCHED  {b}")
        for w in weak:
            print(f"   working line with no sum or source: {w.strip()[:120]}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
