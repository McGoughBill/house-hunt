#!/usr/bin/env python3
"""house-hunt helper: every deterministic step of the search -> longlist -> judge -> shortlist pipeline.

Usage: python3 hh.py <command> <profile> [date] [options]
  install                     copy agents/*.md to ~/.claude/agents
  brief P                     render profiles/P/brief.md from profile.json
  scout P D                   write area + source scout prompts (new profiles)
  scout-apply P D [--fit 4]   merge scout results into profile.json
  search P D                  write known.txt and one search prompt per source
  ingest P D                  merge search results into the registry; write the incremental longlist
  judge P D                   write first-run judge prompts for new houses
  reprice P D                 write one re-judge prompt per house whose price change moves its score
  next P D N                  print the next N prompts to launch as "agent<TAB>path" and mark them launched
  orphans P D [--reset]       launched prompts with no result (e.g. agents killed); --reset relaunches them
  collect P D                 fold judge results into the registry; requeue unreadable runs once
  topup P D                   add runs for houses ranked inside top N with too few runs
  rank P                      write state/ranking.md and ranking.csv
  shortlist P D               update the shortlist; prints NEW lines and exits 10 if a new house entered
  status P D                  one-line counts
  new P [--like Q]            start profiles/P/profile.json from Q's (default sheffield-bill), place-specific fields cleared
  preset P improve|ready      apply a weight preset from templates/presets.json
  set P key.path=value ...    set profile fields; values parsed as JSON when they can be (lists, numbers)
"""
import csv, json, re, shutil, statistics as st, sys
from datetime import date as _date
from pathlib import Path

REPO = Path(__file__).resolve().parent
T = REPO / "templates"

# ---------- small helpers ----------
def jload(p, default=None):
    p = Path(p)
    if not p.exists():
        return default
    txt = p.read_text()
    m = re.search(r"[\[{].*[\]}]", txt, re.S)          # tolerate fences or stray prose
    return json.loads(m.group(0)) if m else default

def jsave(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")

def num(x):
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        return x
    if isinstance(x, str):
        s = re.sub(r"[£$€,\s]", "", x).lower()
        m = re.search(r"(\d+(?:\.\d+)?)(k|m)?", s)
        if m:
            v = float(m.group(1)) * {"k": 1e3, "m": 1e6}.get(m.group(2), 1)
            return v
    return None

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")[:28]

def canon(url):
    u = (url or "").lower().strip()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^(www\.|app\.|m\.)", "", u)
    u = u.split("#")[0].split("?")[0].rstrip("/")
    return u

def street_key(s):
    s = re.sub(r"^\d+[a-z]?\s+", "", (s or "").lower())       # drop house number
    return re.sub(r"[^a-z]", "", s)

def fill(text, d):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(d.get(m.group(1), m.group(0))), text)

def money(cur, x):
    return f"{cur}{x:,.0f}" if isinstance(x, (int, float)) else "–"

def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None

# ---------- profile, paths, state ----------
class Ctx:
    def __init__(self, prof, day=None):
        self.name = prof
        self.dir = REPO / "profiles" / prof
        self.p = jload(self.dir / "profile.json")
        if self.p is None:
            sys.exit(f"no profile at {self.dir}/profile.json")
        self.state = self.dir / "state"
        self.day = day or _date.today().isoformat()
        self.work = REPO / "work" / prof / self.day
        self.reg_path = self.state / "registry.json"
        self.reg = jload(self.reg_path, {"next_id": 1, "houses": {}})
        self.cur = self.p.get("currency", "£")

    def save(self):
        jsave(self.reg_path, self.reg)

    def wd(self, *parts):
        d = self.work.joinpath(*parts)
        d.mkdir(parents=True, exist_ok=True)
        return d

    def new_id(self, district, street):
        n = self.reg["next_id"]
        self.reg["next_id"] = n + 1
        return f"H{n:04d}-{slug(district)}-{slug(street)}"

def fees_tax(p, price):
    bt = p["buy_test"]
    tax, lo = 0.0, 0
    for upto, rate in bt.get("tax_bands", []):
        if price > lo:
            tax += (min(price, upto) - lo) * rate
        lo = upto
    return bt.get("fees", 0) + tax

# ---------- brief ----------
def render_brief(c):
    p, s = c.p, c.p["search"]
    fmt = {"price_max": money(c.cur, s["price_max"]), "allin_max": money(c.cur, s["allin_max"])}
    L = [f"# Scoring brief: {p['name']}", "", p.get("intent", ""), "",
         f"**Vibe:** {p['vibe']['summary']}", "",
         f"**Finished spec:** {p['finished_spec']}", "",
         "V = finished value: median of 3 done-up same-street, same-type sales in the last 2 years. "
         "W = works before contingency. C = buying costs.", "",
         "## Gates (pass/fail; any fail = REJECT)", ""]
    L += [f"- **{g['key']}**: {g['text'].format(**fmt)}" for g in p["gates"]]
    L += ["", "## Scores (1-5 each). Total = Σ(weight × score) ÷ 5", "",
          "| # | Criterion | Wt | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|---|---|"]
    for k in p["criteria"]:
        name = k["name"] + (" *(computed by the ranker — do not score)*" if k.get("computed") else "")
        L.append(f"| {k['n']} | {name} | {k['w']} | " + " | ".join(k["bands"]) + " |")
    bt = p["buy_test"]
    L += ["", f"Weights total {sum(k['w'] for k in p['criteria'])}.", "",
          f"**Buy test:** most to offer = {bt['headroom']}V − {bt['contingency']}W − C. {bt.get('tax_note', '')}", ""]
    (c.dir / "brief.md").write_text("\n".join(L))
    return c.dir / "brief.md"

# ---------- scout (new profiles) ----------
def cmd_scout(c):
    p = c.p
    d = c.wd("prompts", "scout"); r = c.wd("results", "scout")
    base = {"date": c.day, "city": p["city"], "country": p["country"], "currency": c.cur,
            "vibe": p["vibe"]["summary"], "model_areas": ", ".join(p["vibe"].get("model_areas", [])) or "none",
            "anchors": "; ".join(a["name"] for a in p.get("anchors", [])) or "none",
            "price_max": f"{p['search']['price_max']:,}", "beds_min": p["search"]["beds_min"],
            "areas": "; ".join(a["district"] + " " + ", ".join(a["neighbourhoods"]) for a in p.get("areas", [])) or p["city"]}
    (d / "areas.md").write_text(fill((T / "scout-areas.md").read_text(), {**base, "out_path": r / "areas.json"}))
    (d / "sources.md").write_text(fill((T / "scout-sources.md").read_text(),
                                       {**base, "out_path": r / "sources.json", "comps_path": r / "comps.txt"}))
    print(f"wrote 2 scout prompts in {d}")

def cmd_scout_apply(c, fit=4):
    r = c.work / "results" / "scout"
    areas = jload(r / "areas.json", []) or []
    srcs = jload(r / "sources.json", []) or []
    keep = [a for a in areas if (a.get("fit") or 0) >= fit and a.get("budget_fit") != "over"]
    by = {}
    for a in keep:
        by.setdefault((a.get("district") or "?").upper(), []).append(a["name"])
    if keep:
        c.p["areas"] = [{"district": k, "neighbourhoods": v, "only_these": True} for k, v in by.items()]
    if srcs:
        c.p["sources"] = [{"name": s["name"], "desc": s["desc"]} for s in srcs if s.get("name")]
    comps = r / "comps.txt"
    if comps.exists():
        c.p["buy_test"]["comps_sources"] = comps.read_text().strip()
    jsave(c.dir / "profile.json", c.p)
    print(f"areas {len(keep)}/{len(areas)} kept (fit>={fit}), sources {len(srcs)}")
    for a in keep:
        print(f"  {a['name']} {a.get('district')} fit {a.get('fit')} {a.get('budget_fit')}: {a.get('why', '')[:80]}")

# ---------- search ----------
def cmd_search(c):
    p, s = c.p, c.p["search"]
    d = c.wd("prompts", "search"); r = c.wd("results", "search")
    known = c.work / "known.txt"
    lines = [f"{h['url']} | {h['street']} | {h['district']} | {h.get('price') or ''}"
             for h in c.reg["houses"].values() if h.get("url")]
    known.write_text("\n".join(sorted(lines)) + "\n")
    areas = "\n".join(f"   - {a['district']}" + (" but only " if a.get("only_these") else " (") +
                      ", ".join(a["neighbourhoods"]) + ("" if a.get("only_these") else ")") for a in p["areas"])
    so = s.get("small_ok", {})
    base = {"date": c.day, "city": p["city"], "types": ", ".join(s["types"]), "exclude": ", ".join(s["exclude"]),
            "price_band": f"{money(c.cur, s['price_min'])}–{money(c.cur, s['price_max'])}", "areas": areas,
            "beds_min": s["beds_min"], "beds_less": so.get("beds", s["beds_min"] - 1),
            "two_bed_ok_if": f"it is in {', '.join(so.get('districts', [])) or 'none'}, or shows at least {so.get('or_min_m2', 'n/a')} m² inside",
            "size_min_m2": s["size_min_m2"], "record": "; ".join(s["record"]),
            "keywords": ", ".join(f'"{k}"' for k in s["keywords"]), "known_path": known}
    for src in p["sources"]:
        f = d / f"{slug(src['name'])}.md"
        f.write_text(fill((T / "search.md").read_text(), {**base, "source_name": src["name"], "source_desc": src["desc"],
                                                         "out_path": r / f"{slug(src['name'])}.json"}))
    print(f"wrote {len(p['sources'])} search prompts; {len(lines)} known houses")

def area_ok(p, district, area):
    for a in p["areas"]:
        if a["district"].upper() == (district or "").upper():
            if not a.get("only_these"):
                return True
            txt = (area or "").lower()
            return any(n.lower() in txt for n in a["neighbourhoods"]) or not txt
    return False

def brief_fail(p, h):
    s = p["search"]
    st_ = (h.get("status") or "").lower()
    if any(w in st_ for w in ("sold", "under offer", "stc", "agreed", "let ")):
        return "status: " + st_
    if any(w in (h.get("property_type") or "").lower() for w in ("flat", "maisonette", "apartment", "park home", "retirement")):
        return "type"
    if not area_ok(p, h.get("district"), h.get("area")):
        return "area"
    pr = h.get("price")
    if pr is not None and not (s["price_min"] * 0.95 <= pr <= s["price_max"]):
        return "price"
    beds, m2, so = num(h.get("beds")), num(h.get("m2")), s.get("small_ok", {})
    if beds is not None and beds < s["beds_min"]:
        ok = beds >= so.get("beds", 99) and ((h.get("district") or "").upper() in so.get("districts", [])
                                            or (m2 or 0) >= so.get("or_min_m2", 1e9))
        if not ok:
            return "beds"
    if m2 is not None and m2 < s["size_min_m2"] and not (beds is not None and beds < s["beds_min"]):
        return "size"
    return None

def match(c, h):
    cu = canon(h.get("url"))
    for k, x in c.reg["houses"].items():
        if cu and cu in [canon(u) for u in x.get("urls", [])]:
            return k
    sk, dist = street_key(h.get("street")), (h.get("district") or "").upper()
    for k, x in c.reg["houses"].items():
        if sk and street_key(x["street"]) == sk and x["district"].upper() == dist and \
           (num(x.get("beds")) == num(h.get("beds")) or h.get("beds") is None):
            a, b = x.get("price"), h.get("price")
            if a and b and abs(a - b) / a <= 0.05:
                return k
            if a and b and x.get("agent") and (x["agent"].split()[0].lower() in (h.get("agent") or "").lower()) and abs(a - b) / a <= 0.15:
                return k
    return None

def cmd_ingest(c):
    p = c.p
    files = sorted((c.work / "results" / "search").glob("*.json"))
    new, upd, out, seen = [], [], 0, 0
    for f in files:
        for raw in (jload(f, []) or []):
            if not isinstance(raw, dict):
                continue
            seen += 1
            h = {"street": raw.get("street") or "", "area": raw.get("area") or "",
                 "district": (raw.get("postcode_district") or "").upper().split(" ")[0],
                 "price": num(raw.get("price_gbp")) or num(raw.get("price_text")), "price_text": raw.get("price_text"),
                 "property_type": raw.get("property_type"), "beds": raw.get("beds"), "m2": num(raw.get("floor_area_m2")),
                 "tenure": raw.get("tenure"), "condition": raw.get("condition"), "flags": raw.get("flags") or [],
                 "agent": raw.get("agent"), "url": raw.get("url"), "status": raw.get("status"),
                 "verified": raw.get("verified"), "source": raw.get("source") or f.stem, "notes": raw.get("notes")}
            k = match(c, h)
            if k:                                    # known house: price change, extra source
                x = c.reg["houses"][k]
                x["last_seen"] = c.day
                if x["status"] == "unconfirmed" and not brief_fail(p, {**x, "status": h.get("status")}):
                    x["status"] = "new"; new.append(k)     # seen live again: judge it
                if h["url"] and canon(h["url"]) not in map(canon, x["urls"]):
                    x["urls"].append(h["url"])
                if h["source"] not in x["sources"]:
                    x["sources"].append(h["source"])
                if h["price"] and x.get("price") and abs(h["price"] - x["price"]) / x["price"] >= p["run"]["reprice_min_change"]:
                    x["price_history"].append([c.day, h["price"]])
                    x["reprice_from"], x["price"] = x["price"], h["price"]
                    upd.append(k)
                continue
            if raw.get("known"):
                continue                             # price-change report we could not match
            why = brief_fail(p, h)
            hid = c.new_id(h["district"] or "x", h["street"])
            rec = {**h, "id": hid, "urls": [h["url"]] if h["url"] else [], "sources": [h["source"]],
                   "first_seen": c.day, "last_seen": c.day, "price_history": [[c.day, h["price"]]],
                   "status": "out" if why else "new", "out_reason": why, "runs": [], "retries": {}}
            c.reg["houses"][hid] = rec
            if why:
                out += 1
            else:
                new.append(hid)
    c.save()
    write_longlist(c, new, upd)
    shutil.copytree(c.work / "results" / "search", c.state / "raw" / c.day / "search", dirs_exist_ok=True)
    print(f"search rows {seen} from {len(files)} sources: new {len(new)}, price changes {len(upd)}, outside brief {out}")

def write_longlist(c, new, upd):
    H = c.reg["houses"]
    def row(h):
        return (f"| {h['id']} | {h['district']} | {h['street']} | {h['area']} | {money(c.cur, h.get('price'))} | "
                f"{h.get('beds') or ''} | {h.get('m2') or ''} | {h.get('condition') or ''} | {h.get('tenure') or ''} | "
                f"{h.get('agent') or ''} | [link]({h['url']}) |" if h.get("url") else "| – |")
    hdr = ["| ID | PC | Street | Area | Price | Beds | m² | State | Tenure | Agent | Link |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    L = [f"# Longlist additions {c.day} ({c.name})", "", f"New houses: {len(new)}. Price changes on known houses: {len(upd)}.", ""]
    L += hdr + [row(H[k]) for k in new]
    if upd:
        L += ["", "## Price changes", ""] + [f"- {H[k]['id']} {H[k]['street']}: {money(c.cur, H[k]['reprice_from'])} → {money(c.cur, H[k]['price'])}" for k in upd]
    (c.state / "history").mkdir(parents=True, exist_ok=True)
    (c.state / "history" / f"longlist-{c.day}.md").write_text("\n".join(L) + "\n")
    allh = sorted(H.values(), key=lambda h: (h["status"] == "out", h["district"], h["street"]))
    A = [f"# Longlist, all runs ({c.name})", "", f"{sum(h['status'] != 'out' for h in allh)} in brief, "
         f"{sum(h['status'] == 'out' for h in allh)} outside it. Updated {c.day}.", "",
         "| ID | Status | PC | Street | Area | Price | Beds | m² | First seen | Link |", "|---|---|---|---|---|---|---|---|---|---|"]
    A += [f"| {h['id']} | {h['status']}{' (' + h['out_reason'] + ')' if h.get('out_reason') else ''} | {h['district']} | {h['street']} | {h['area']} | "
          f"{money(c.cur, h.get('price'))} | {h.get('beds') or ''} | {h.get('m2') or ''} | {h['first_seen']} | "
          f"{'[link](' + h['url'] + ')' if h.get('url') else ''} |" for h in allh]
    (c.state / "longlist.md").write_text("\n".join(A) + "\n")

# ---------- judging ----------
def judge_prompt(c, h, run, context=""):
    p = c.p
    d = c.wd("prompts", "judge"); r = c.wd("results", "judge")
    stem = f"{h['id']}_r{run}"
    gates = {g["key"]: {"pass": True, "reason": ""} for g in p["gates"]}
    vals = {"id": h["id"], "run": run, "street": h["street"], "area": h["area"], "postcode": h["district"],
            "price": money(c.cur, h.get("price")) if h.get("price") else (h.get("price_text") or "on request"),
            "beds": h.get("beds") or "?", "m2": f"{h['m2']:.0f} m²" if h.get("m2") else "not given",
            "tenure": h.get("tenure") or "not given", "state": h.get("condition") or "unknown",
            "agent": h.get("agent") or "?", "link": h.get("url") or "none (find it by street, agent and price)",
            "context": context, "comps_sources": p["buy_test"]["comps_sources"], "finished_spec": p["finished_spec"],
            "tax_note": p["buy_test"].get("tax_note", ""), "fees": money(c.cur, p["buy_test"].get("fees", 0)),
            "brief_path": c.dir / "brief.md", "anchors": "; ".join(a["name"] for a in p.get("anchors", [])) or "none",
            "gates_json": json.dumps(gates), "out_path": r / f"{stem}.json"}
    (d / f"{stem}.md").write_text(fill((T / "judge.md").read_text(), vals))
    return stem

def cmd_judge(c):
    render_brief(c)
    n = 0
    for h in c.reg["houses"].values():
        if h["status"] == "new" and not h["runs"]:
            for i in range(1, c.p["run"]["first_runs"] + 1):
                judge_prompt(c, h, i); n += 1
    print(f"wrote {n} judge prompts")

def cmd_reprice(c):
    render_brief(c)
    n = skip = 0
    for h in c.reg["houses"].values():
        if h.get("reprice_from") is None or not h["runs"]:
            continue
        old = score_house(c, h, asking=h["reprice_from"]); new = score_house(c, h)
        if old["status"] != new["status"] or abs((old["total"] or 0) - (new["total"] or 0)) >= 0.5:
            last = h["runs"][-1]
            ctx = (f"\n**Re-check after a price change.** Judged on {last['date']} at {money(c.cur, h['reprice_from'])}: "
                   f"V {money(c.cur, last.get('V'))} ({last.get('v_basis', '')[:200]}); W {money(c.cur, last.get('W'))}; "
                   f"floor {last.get('m2') or '?'} m²; risk: {last.get('risk', '')[:200]}. The asking price is now "
                   f"{money(c.cur, h['price'])}. Confirm the listing is live at the new price, reuse the earlier evidence "
                   f"where it still holds, and re-score everything the price touches.\n")
            judge_prompt(c, h, f"p{len(h['price_history'])}", ctx); n += 1
        else:
            skip += 1
        h["reprice_from"] = None
    c.save()
    print(f"wrote {n} reprice prompts; {skip} price changes did not move the score")

def cmd_topup(c):
    rows = rank_rows(c)
    n = 0
    top = [r for r in rows if r["status"] in ("PASS", "REJECT")][: c.p["run"]["topup_n"]]
    for r in top:
        h = c.reg["houses"][r["id"]]
        have = {str(x["run"]) for x in h["runs"] if x.get("live") is True and x["scores"]}
        need = c.p["run"]["topup_runs"] - len(have)
        for i in range(1, 10):
            if need <= 0:
                break
            if str(i) not in have and not (c.work / "prompts" / "judge" / f"{h['id']}_r{i}.md").exists():
                judge_prompt(c, h, i); n += 1; need -= 1
    print(f"wrote {n} top-up prompts for the top {len(top)}")

def compact(raw, day):
    sc = {}
    for s in raw.get("scores") or []:
        if isinstance(s, dict) and str(s.get("score", "")).strip().isdigit():
            sc[str(int(s["n"]))] = min(max(int(s["score"]), 1), 5)
    est = sum(bool(s.get("est")) for s in raw.get("scores") or [] if isinstance(s, dict))
    gates = raw.get("gates") or {}
    return {"run": str(raw.get("run")), "date": day, "live": raw.get("live"), "asking": num(raw.get("asking")),
            "V": num(raw.get("V")), "W": num(raw.get("W")), "C": num(raw.get("C")), "m2": num(raw.get("floor_area_m2")),
            "type": raw.get("house_type"), "fails": [g for g, v in gates.items() if isinstance(v, dict) and v.get("pass") is False],
            "fail_reasons": {g: (v.get("reason") or "")[:160] for g, v in gates.items() if isinstance(v, dict) and v.get("pass") is False},
            "unconf": sum(1 for v in gates.values() if isinstance(v, dict) and str(v.get("reason", "")).startswith("unconfirmed")),
            "scores": sc, "est": est, "verdict": raw.get("verdict"), "risk": (raw.get("biggest_risk") or "")[:240],
            "v_basis": (raw.get("v_basis") or "")[:300], "url": raw.get("listing_url"), "anchors": raw.get("anchors")}

def cmd_collect(c):
    rdir = c.work / "results" / "judge"
    launched = c.work / "launched.txt"
    done = retry = 0
    for f in sorted(rdir.glob("*.json")):
        raw = jload(f)
        hid, run = f.stem.rsplit("_r", 1)
        h = c.reg["houses"].get(hid)
        if h is None or raw is None:
            continue
        rec = compact(raw, c.day)
        blank = rec["live"] is None and not rec["scores"]
        if blank and h["retries"].get(f.stem, 0) < 1:      # requeue once
            h["retries"][f.stem] = 1
            dest = c.state / "raw" / c.day / "failed"; dest.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), dest / f.name)
            if launched.exists():
                launched.write_text("\n".join(x for x in launched.read_text().split() if x != f"judge/{f.stem}") + "\n")
            retry += 1
            continue
        h["runs"] = [x for x in h["runs"] if x["run"] != rec["run"] or x["date"] != c.day] + [rec]
        if h["status"] == "new":
            h["status"] = "judged"
        done += 1
    c.save()
    if rdir.exists():
        shutil.copytree(rdir, c.state / "raw" / c.day / "judge", dirs_exist_ok=True)
    print(f"collected {done} runs; requeued {retry} blank runs (launch them with next)")

# ---------- scoring ----------
def band(x, cuts):
    return None if x is None else 1 + sum(x > k for k in cuts)

def score_house(c, h, asking=None):
    p = c.p
    bt, s = p["buy_test"], p["search"]
    asking = asking if asking is not None else h.get("price")
    runs = h["runs"]
    if not runs:
        return {"status": "NEW", "total": None}
    latest = max(runs, key=lambda r: (r["date"], r["run"]))
    gone = latest.get("live") is False or sum(r.get("live") is False for r in runs) > len(runs) / 2
    sc = [r for r in runs if r.get("live") is True and r["scores"]]
    if not sc:
        return {"status": "GONE" if gone else "UNREADABLE", "total": None, "runs": len(runs)}
    per, margins, uplifts, fails = {}, [], [], {}
    for r in sc:
        a = asking or r.get("asking")
        V, W = r.get("V"), r.get("W")
        C = r.get("C") or (fees_tax(p, a) if a else None)
        m = bt["headroom"] * V - bt["contingency"] * W - C - a if None not in (V, W, C, a) else None
        u = V / a if V and a else None
        margins.append(m); uplifts.append(u)
        over = (a and a > s["price_max"]) or (None not in (a, W, C) and a + bt["contingency"] * W + C > s["allin_max"])
        for g in set(r["fails"]) | ({"budget"} if over else set()):
            if g != "budget" or over:
                fails[g] = fails.get(g, 0) + 1
        for k in p["criteria"]:
            n = str(k["n"])
            if k.get("computed") == "margin":
                v = band(m, k["cuts"])
            elif k.get("computed") == "uplift":
                v = band(u, k["cuts"])
            else:
                v = r["scores"].get(n)
            per.setdefault(n, []).append(v)
    medv = {n: med(v) for n, v in per.items()}
    missing = [n for n, v in medv.items() if v is None]
    for n in missing:
        medv[n] = 3                                           # neutral fill, flagged
    total = round(sum(k["w"] * medv[str(k["n"])] for k in p["criteria"]) / 5, 1)
    failed = [g for g, n in fails.items() if n > len(sc) / 2]
    totals = []
    for r in sc:
        t = 0
        for k in p["criteria"]:
            vals = per[str(k["n"])]
            v = vals[sc.index(r)] if sc.index(r) < len(vals) else None
            t += k["w"] * (v if v is not None else medv[str(k["n"])])
        totals.append(round(t / 5, 1))
    split = [k["name"][:24] for k in p["criteria"]
             if len([v for v in per[str(k["n"])] if v is not None]) > 1
             and max(v for v in per[str(k["n"])] if v is not None) - min(v for v in per[str(k["n"])] if v is not None) >= 2]
    return {"status": "GONE" if gone else ("REJECT" if failed else "PASS"), "total": total, "runs": len(sc),
            "run_totals": totals, "failed": failed, "margin": med(margins), "uplift": med(uplifts),
            "V": med([r.get("V") for r in sc]), "W": med([r.get("W") for r in sc]), "m2": med([r.get("m2") for r in sc]),
            "est": round(sum(r["est"] for r in sc) / (len(sc) * len(p["criteria"])), 2), "neutral": missing,
            "disagree": split, "risk": latest.get("risk", ""), "medv": medv}

def rank_rows(c):
    order = {"PASS": 0, "REJECT": 1, "NEW": 2, "UNREADABLE": 3, "GONE": 4}
    rows = []
    for h in c.reg["houses"].values():
        if h["status"] == "out":
            continue
        s = score_house(c, h)
        rows.append({"id": h["id"], **s, "street": h["street"], "area": h["area"], "district": h["district"],
                     "asking": h.get("price"), "url": h.get("url"), "first_seen": h["first_seen"]})
    rows.sort(key=lambda r: (order[r["status"]], -(r.get("total") or 0)))
    return rows

def cmd_rank(c):
    rows = rank_rows(c)
    cur = c.cur
    k = lambda x: f"{cur}{x/1000:.0f}k" if isinstance(x, (int, float)) else ""
    L = [f"# Ranking ({c.name}, {c.day})", "", "| # | Status | Total | Runs | House | Asking | V | W | Margin | Uplift | m² | Failed | Risk |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        up = f"{r['uplift']:.2f}" if r.get("uplift") else ""
        L.append(f"| {i} | {r['status']} | {r.get('total') or ''} | {' / '.join(map(str, r.get('run_totals', [])))} | "
                 f"[{r['street']}, {r['area']} {r['district']}]({r['url']}) | {k(r['asking'])} | {k(r.get('V'))} | "
                 f"{k(r.get('W'))} | {k(r.get('margin'))} | {up} | {r.get('m2') or ''} | {', '.join(r.get('failed', []))} | "
                 f"{(r.get('risk') or '')[:120]} |")
    (c.state / "ranking.md").write_text("\n".join(L) + "\n")
    cols = ["id", "status", "total", "runs", "street", "area", "district", "asking", "V", "W", "margin", "uplift", "m2", "est", "failed", "disagree", "neutral", "risk", "url", "first_seen"]
    with (c.state / "ranking.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for r in rows:
            w.writerow({**r, "failed": ", ".join(r.get("failed", [])), "disagree": ", ".join(r.get("disagree", [])),
                        "neutral": ", ".join(r.get("neutral", []))})
    from collections import Counter
    print(dict(Counter(r["status"] for r in rows)))
    return rows

def cmd_shortlist(c):
    rows = cmd_rank(c)
    n = c.p["run"]["shortlist_n"]
    top = [r for r in rows if r["status"] == "PASS"][:n]
    prev = jload(c.state / "shortlist.json", {"ids": []})
    new = [r for r in top if r["id"] not in prev["ids"]]
    gone = [i for i in prev["ids"] if i not in {r["id"] for r in top}]
    k = lambda x: f"{c.cur}{x/1000:.0f}k" if isinstance(x, (int, float)) else "–"
    L = [f"# Shortlist ({c.name}), top {n}", "", f"Updated {c.day}. New this run: {len(new)}. Dropped: {len(gone)}.", "",
         "| # | Total | House | Asking | V | Margin | Uplift | m² | Risk |", "|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(top, 1):
        flag = " **NEW**" if r in new else ""
        up = f"{r['uplift']:.2f}" if r.get("uplift") else "–"
        L.append(f"| {i} | {r['total']} | [{r['street']}, {r['area']} {r['district']}]({r['url']}){flag} | {k(r['asking'])} | "
                 f"{k(r.get('V'))} | {k(r.get('margin'))} | {up} | {r.get('m2') or '–'} | {(r.get('risk') or '')[:140]} |")
    if new or gone or not prev["ids"]:
        (c.state / "shortlist.md").write_text("\n".join(L) + "\n")
        (c.state / "history" / f"shortlist-{c.day}.md").write_text("\n".join(L) + "\n")
        jsave(c.state / "shortlist.json", {"date": c.day, "ids": [r["id"] for r in top]})
    for r in new:
        rank = top.index(r) + 1
        print(f"NEW #{rank} {r['street']}, {r['area']} {k(r['asking'])} score {r['total']}")
    for i in gone:
        print(f"DROPPED {i}")
    sys.exit(10 if new and prev["ids"] else 0)

# ---------- queue ----------
def cmd_next(c, n):
    launched = c.work / "launched.txt"
    done = set(launched.read_text().split()) if launched.exists() else set()
    out = []
    for kind, agent in (("scout", "house-judge"), ("search", "house-search"), ("judge", "house-judge")):
        for f in sorted((c.work / "prompts" / kind).glob("*.md")) if (c.work / "prompts" / kind).exists() else []:
            key = f"{kind}/{f.stem}"
            if key not in done and len(out) < n and not (c.work / "results" / kind / f"{f.stem}.json").exists():
                out.append((key, agent, f))
    with launched.open("a") as fh:
        for key, _, _ in out:
            fh.write(key + "\n")
    for _, agent, f in out:
        print(f"{agent}\t{f}")
    left = sum(1 for kind in ("scout", "search", "judge") for f in (c.work / "prompts" / kind).glob("*.md")
               if (c.work / "prompts" / kind).exists()) - len(done) - len(out)
    print(f"# {left} left", file=sys.stderr)

def cmd_orphans(c, reset=False):
    launched = c.work / "launched.txt"
    keys = launched.read_text().split() if launched.exists() else []
    orph = [k for k in keys if "/" in k and not (c.work / "results" / k.split("/")[0] / f"{k.split('/')[1]}.json").exists()]
    for k in orph:
        print(k)
    if reset and orph:
        launched.write_text("\n".join(k for k in keys if k not in orph) + "\n")
        print(f"# reset {len(orph)}; launch them again with next", file=sys.stderr)

def cmd_status(c):
    from collections import Counter
    print(c.name, c.day, dict(Counter(h["status"] for h in c.reg["houses"].values())),
          "runs", sum(len(h["runs"]) for h in c.reg["houses"].values()))

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    cmd = a[0]
    if cmd == "install":
        dst = Path.home() / ".claude" / "agents"; dst.mkdir(parents=True, exist_ok=True)
        for f in (REPO / "agents").glob("*.md"):
            shutil.copy(f, dst / f.name)
        print(f"installed agents to {dst}"); return
    if cmd == "new":
        like = a[a.index("--like") + 1] if "--like" in a else "sheffield-bill"
        p = jload(REPO / "profiles" / like / "profile.json")
        p.update({"name": a[1], "created": _date.today().isoformat(), "owner": "", "intent": "", "city": "", "areas": [],
                  "sources": [], "anchors": [], "vibe": {"summary": "", "model_areas": [], "likes": [], "avoid": []}})
        jsave(REPO / "profiles" / a[1] / "profile.json", p)
        print(f"wrote profiles/{a[1]}/profile.json (criteria, gates and run settings copied from {like})"); return
    if cmd == "preset":
        f = REPO / "profiles" / a[1] / "profile.json"; p = jload(f)
        w = jload(T / "presets.json")[a[2]]
        for k, x in zip(p["criteria"], w):
            k["w"] = x
        jsave(f, p); print(f"weights set to {a[2]} (total {sum(w)})"); return
    if cmd == "set":
        f = REPO / "profiles" / a[1] / "profile.json"; p = jload(f)
        for kv in a[2:]:
            k, v = kv.split("=", 1)
            try:
                v = json.loads(v)
            except ValueError:
                pass
            node, keys = p, k.split(".")
            for x in keys[:-1]:
                node = node[int(x)] if isinstance(node, list) else node.setdefault(x, {})
            node[int(keys[-1]) if isinstance(node, list) else keys[-1]] = v
        jsave(f, p); print(f"set {len(a) - 2} fields"); return
    c = Ctx(a[1], a[2] if len(a) > 2 and re.match(r"\d{4}-\d\d-\d\d", a[2]) else None)
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    {"brief": lambda: print(render_brief(c)), "scout": lambda: cmd_scout(c),
     "scout-apply": lambda: cmd_scout_apply(c, int(opt("--fit", 4))), "search": lambda: cmd_search(c),
     "ingest": lambda: cmd_ingest(c), "judge": lambda: cmd_judge(c), "reprice": lambda: cmd_reprice(c),
     "next": lambda: cmd_next(c, int(a[3] if len(a) > 3 else 1)), "orphans": lambda: cmd_orphans(c, "--reset" in a),
     "collect": lambda: cmd_collect(c), "topup": lambda: cmd_topup(c), "rank": lambda: cmd_rank(c),
     "shortlist": lambda: cmd_shortlist(c), "status": lambda: cmd_status(c)}[cmd]()

if __name__ == "__main__":
    main()
