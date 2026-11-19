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
    (ROOT / "out/clashes.md").write_text("# Clashes\n\n" + ("\n".join(clashes) or "None.") + "\n")
    print(f"merged {n} facts, skipped {skipped} bad, {len(clashes)} clashes -> facts.json, out/clashes.md")

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
