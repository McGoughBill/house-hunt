#!/usr/bin/env python3
"""facts.py add FILE JSON | validate [FILE...] | merge
merge: all facts/*.jsonl -> facts.json (house -> field -> [facts]) and out/clashes.md."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ = ["house", "field", "value", "source", "retrieved", "confidence"]
HOUSES = {"market", "falmouth", "welby", "leeshall", "cawthorne", "underwood", "helmton", "hollythorpe"}

def check(f):
    errs = [f"missing {k}" for k in REQ if k not in f]
    if f.get("house") not in HOUSES: errs.append(f"unknown house {f.get('house')}")
    if f.get("confidence") not in ("high", "medium", "low"): errs.append("confidence must be high/medium/low")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(f.get("retrieved", ""))): errs.append("retrieved must be YYYY-MM-DD")
    if f.get("value") is None:
        if not f.get("note"): errs.append("null value needs a reason in note")
    elif not str(f.get("source") or "").startswith("http"): errs.append("non-null value needs a source URL")
    return errs

def lines(path):
    for i, ln in enumerate(Path(path).read_text().splitlines(), 1):
        if ln.strip():
            try: yield i, json.loads(ln)
            except json.JSONDecodeError as e: yield i, {"_bad": str(e)}

def validate(paths):
    bad = 0
    for p in paths:
        for i, f in lines(p):
            e = [f["_bad"]] if "_bad" in f else check(f)
            if e: bad += 1; print(f"{p}:{i}: {'; '.join(e)}")
    print("ok" if not bad else f"{bad} bad lines"); return bad

def norm(v):
    return json.dumps(v, sort_keys=True).lower() if not isinstance(v, str) else v.strip().lower()

# Fields that say the same thing under different names: canonical -> [(field, key inside a dict value or None)]
GROUPS = {
    "tenure": [("tenure_lr", None), ("tenure_listing", None), ("listing_facts", "tenure"), ("listing_history", "tenure")],
    "floor_area_m2": [("epc_floor_area_m2", None), ("floor_area_listing_m2", None), ("listing_facts", "area_m2")],
}

def canon(kind, v):
    if v is None: return None
    if kind == "tenure":
        s = str(v).strip().lower()
        return "L+F" if ("l" in s and "f" in s and "and" in s) else s[:1].upper() if s[:1] in "lf" else None
    try: return float(v)
    except (TypeError, ValueError): return None

def same(kind, a, b):
    return abs(a - b) <= 0.05 * max(a, b) if kind == "floor_area_m2" else a == b

def cross_clashes(out):
    """Clashes across differently named fields, and against the Saturday doc's claims in houses.yaml."""
    import yaml
    claims = {h["id"]: h.get("claims") or {} for h in yaml.safe_load((ROOT / "houses.yaml").read_text())["houses"]}
    res = []
    for h, fields in out.items():
        for kind, members in GROUPS.items():
            seen = []
            for field, key in members:
                for f in fields.get(field, []):
                    v = f["value"].get(key) if key and isinstance(f["value"], dict) else (None if key else f["value"])
                    c = canon(kind, v)
                    if c is not None: seen.append((c, f"{f['task']}/{field}", f["source"]))
            if h in claims and kind in claims[h]:
                seen.append((canon(kind, claims[h][kind]), "Saturday doc", "houses.yaml claims"))
            vals = [s[0] for s in seen]
            if any(not same(kind, a, b) for a in vals for b in vals if a is not None and b is not None):
                res.append(f"- **{h} / {kind}** (cross-field): " + "; ".join(f"{v} ({w}, {s})" for v, w, s in seen))
    return res

def merge():
    out, n, skipped = {}, 0, 0
    for p in sorted((ROOT / "facts").glob("*.jsonl")):
        for i, f in lines(p):
            if "_bad" in f or check(f): skipped += 1; continue
            f["task"] = p.stem
            out.setdefault(f["house"], {}).setdefault(f["field"], []).append(f); n += 1
    (ROOT / "facts.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    clashes = []
    for h, fields in out.items():
        for k, fs in fields.items():
            vals = {norm(f["value"]) for f in fs if f["value"] is not None}
            if len(vals) > 1:
                clashes.append(f"- **{h} / {k}**: " + "; ".join(
                    f"{json.dumps(f['value'], ensure_ascii=False)[:120]} ({f['task']}, {f['source']})" for f in fs if f["value"] is not None))
    clashes += cross_clashes(out)
    import yaml
    sp = ROOT / "settled.yaml"
    rules = {r["key"]: r for r in (yaml.safe_load(sp.read_text()) or [])} if sp.exists() else {}
    marked, open_ = [], 0
    for c in clashes:
        key = re.match(r"- \*\*(.+?)\*\*", c).group(1)
        r = rules.get(key)
        if r: marked.append(c + f"\n  - **SETTLED:** {r['winner']}. {r['why']}")
        else: marked.append(c + "\n  - **OPEN**"); open_ += 1
    found = {re.match(r"- \*\*(.+?)\*\*", c).group(1) for c in clashes}
    by_hand = [f"- **{k}** (found by hand)\n  - **SETTLED:** {r['winner']}. {r['why']}" if r["winner"] != "Unsettled"
               else f"- **{k}** (found by hand)\n  - **OPEN:** {r['why']}" for k, r in rules.items() if k not in found]
    (ROOT / "out/clashes.md").write_text("# Clashes\n\n" + ("\n".join(marked) or "None.") +
                                         ("\n\n## Other rulings\n\n" + "\n".join(by_hand) if by_hand else "") + "\n")
    print(f"merged {n} facts, skipped {skipped} bad, {len(clashes)} clashes ({open_} open) -> facts.json, out/clashes.md")

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["add"]:
        f = json.loads(a[2]); e = check(f)
        if e: sys.exit("rejected: " + "; ".join(e))
        with open(a[1], "a") as fh: fh.write(json.dumps(f, ensure_ascii=False) + "\n")
        print("added")
    elif a[:1] == ["validate"]:
        sys.exit(1 if validate(a[1:] or sorted((ROOT / "facts").glob("*.jsonl"))) else 0)
    elif a[:1] == ["merge"]:
        merge()
    else:
        sys.exit(__doc__)
