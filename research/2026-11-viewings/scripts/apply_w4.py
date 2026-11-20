#!/usr/bin/env python3
"""Wave 4: apply checker fixes and Local prices blocks to out/briefs/<id>.md, rebuild out/briefs/all.md,
and fix out/saturday-viewings-2026-11-21.md. Every replacement must match exactly once."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from local_prices import block
ROOT = Path(__file__).resolve().parent.parent
BR = ROOT / "out/briefs"
facts = json.loads((ROOT / "facts.json").read_text())

B = {
"falmouth": [
 ("- Area: **94 m²** (listing says 108 m²; work on the smaller)", "- Area: **94 m²** (Hunters by phone; no written source, unconfirmed [W4]; listing says 108 m²; work on the smaller)"),
 ("1 cut (2.3% in all)", "1 cut (2.3% in all); source blocked, unconfirmed [W4]"),
 ("- Hunters' phone figure, 1,007 sq ft (94 m²), is 13% under the listing [W2 ruling].", "- Hunters' phone figure, 1,007 sq ft (94 m²), is 13% under the listing; not in writing yet, so ask for it [W4]."),
 ("- 84 days unsold; cut £215k to £210k on 9 Oct [L].", "- 84 days unsold; cut £215k to £210k on 9 Oct [L]; unconfirmed, source blocked [W4]."),
 ("- Rivals: Abbeydale Rd, 1,283 sq ft, £210k; Tavistock Rd £200k [L].", "- Rival: Abbeydale Rd £210k [L]; unconfirmed, source blocked; another Abbeydale Rd terrace at £210k shows 878 sq ft, so 1,283 sq ft may be wrong. Tavistock Rd cut: listing not found [W4]."),
],
"welby": [
 ("- Bungalow model: **£245k–£251k** as it stands; likely range £227k–£277k on Welby Place sales alone", "- Bungalow model (low confidence: 6 bungalow sales): **£245k–£251k** as it stands; one sale could land anywhere in £207k–£304k on Welby Place data [W4]"),
 ("- Model: £245k–£251k, £14–20k under asking [value].", "- Model: £245k–£251k, £14–20k under asking [value]; low confidence, and its one-sale range (£207k–£304k) spans the asking [W4]."),
 ("- Hall: you enter straight into a room. Notes say porch into hall; see.", "- Hall: listing shows an entrance porch into a hallway [W4]; check on entry."),
],
"leeshall": [
 ("- Area: **69 m²** · asking", "- Area: **69 m²** (EPC figure from your notes, not re-found: unconfirmed [W4]; may leave out the extension) · asking"),
 ("- Asking £4,203/m², 15% over street median [value].", "- Asking £4,203/m², 15% over street median, if 69 m² is the whole house; the rear extension may be extra [value] [W4]."),
],
"cawthorne": [
 ("- Guide bottom £3,750/m² beats street median £3,644/m² [value].", "- Guide bottom £3,750/m² is 3% above the street median £3,644/m²; the top is 11% above [value] [W4]."),
],
"underwood": [
 ("- Three nearby 3-bed terraces also ask £220k [L].", "- Nearby 3-bed terraces ask about the same: Woodseats Rd guide £220k–£230k (1,216 sq ft, freehold); Hackthorn Rd guide £220k–£240k (end terrace, freehold) [W4]."),
 ("- Is Hunters' Underwood Road listing (30 Oct) this house?", "- Is it also with Hunters? (Rightmove showed a Hunters Underwood Road terrace, added 30 Oct; gone by 20 Nov.) [W4]"),
],
"helmton": [
 ("- Done-up value £247k–£265k; buy-test margin at asking −£51,553 to −£29,560", "- Done-up value £247k–£265k (the one comparable, up to the seller's 2018 price today); buy-test margin cut [W4]"),
],
"hollythorpe": [
 ("- Done-up value £276k–£286k; buy-test margin at asking −£40,217 to −£26,021", "- Done-up value £276k–£286k (street median to upper quartile); buy-test margin cut [W4]"),
 ("- Done up: margin −£40k to −£26k at £280k [value].\n", ""),
 ("- No. 30, 69 m² semi, sold £241k in Mar 2025; No. 33 £235k [comps].", "- Cheapest 2025 street semis: No. 30 (69 m²) £241k and No. 33 £235k, both leasehold; but Nos 13, 49 and 80 sold £295k–£330k [comps] [W4]."),
 ("- Bigger Hollythorpe Crescent semi (about 75 m²) went STC at £240k [L].", "- Bigger Hollythorpe Crescent semi (about 75 m²) asks a £240k–£250k guide, freehold; not shown as sold STC on 20 Nov [W4]."),
],
}

def sub1(t, old, new, where):
    n = t.count(old)
    if n != 1: sys.exit(f"{where}: {n} matches for: {old[:70]}")
    return t.replace(old, new)

for hid, reps in B.items():
    p = BR / f"{hid}.md"; t = p.read_text()
    if "**Local prices [W4]**" in t: sys.exit(f"{hid}: already applied")
    for o, n in reps: t = sub1(t, o, n, hid)
    lp = block(hid, facts).replace('same-day £1,800 cat-B "other" transfer of 1A', "same day, a £1,800 non-market transfer of 1A: treat with care")
    t = sub1(t, "\n**Levers**", "\n" + lp + "\n\n**Levers**", hid)
    p.write_text(t)

# rebuild all.md: keep its header, then the seven briefs in viewing order
allp = BR / "all.md"; a = allp.read_text()
head = a[:a.index("## 1. ")]
head = sub1(head, "Keep every figure here from the agent.*", "Keep every figure here from the agent.*\n\n*[W4] 20 Nov: checked line by line by two fresh agents against Land Registry and the facts file (results: `wave4-check.md`). Each brief now has a Local prices block; every fix is marked [W4]; items whose source was blocked say \"unconfirmed\".*", "all")
order = ["falmouth", "welby", "leeshall", "cawthorne", "underwood", "helmton", "hollythorpe"]
allp.write_text(head + "\n\n---\n\n".join((BR / f"{h}.md").read_text().strip() for h in order) + "\n")

S = [
 ("*Wave 2 (20 Nov): every figure that moved, and every hazard question added, is marked **[W2]**. Working and sources: `wave2-status.md`.*",
  "*Wave 2 (20 Nov): every figure that moved, and every hazard question added, is marked **[W2]**. Working and sources: `wave2-status.md`.*\n\n*Wave 4 (20 Nov): two fresh agents checked every figure; fixes and cuts are marked **[W4]**. Three or four same-street comparables per house are in each brief's Local prices block. Results: `wave4-check.md`.*"),
 ("| Saxton Mee, Banner Cross (949–951 Ecclesall Road, S11 8TN) | Abi Lenihan |", "| Saxton Mee, Banner Cross (949–951 Ecclesall Road, S11 8TN) | Abi Lenihan (from your emails; not on their site **[W4]**) |"),
 ("| Whitehornes (Unit 2 Acorn Business Park, Woodseats Close, S8 0TB) |", "| Whitehornes (Unit 2 Acorn Business Park, Woodseats Close, S8 0TB, per your notes; listings give 952 Ecclesall Road, S11 8TR **[W4]**) |"),
 ("Hunters quoted 1,007 sq ft on the phone.", "Hunters quoted 1,007 sq ft on the phone (not in writing yet **[W4]**)."),
 ("- Rival terraces within 1 km, asking now: Tavistock Rd £200k; Abbeydale Rd £210k (back on the market);", "- Rival terraces within 1 km, asking now: Abbeydale Rd £210k (back on the market; unconfirmed, page blocked **[W4]**);"),
 ("with a lobby only to the stairs. That breaks your hall rule.", "with a lobby only to the stairs. Check it against your hall rule **[W4]**."),
 ("My rough estimate of its value once done up is £290,000. The street's best sale is now worth about £324k, so that ceiling is less tight than I first said. The margin after works still looks thin or negative.",
  "The street's best sale is now worth about £324k. **[W4]** Done-up estimate and margin cut; three same-street sales are in the brief's Local prices block."),
 ("- Side porch into a large L-shaped hall, which passes your hall rule.", "- Side porch into a large L-shaped hall (listing: entrance porch, hallway) **[W4]**."),
 ("versus the £265k asking. Your earlier fair value of £215–235k sits below the model's middle, though inside its range. Your extension plan loses money above about a £220k purchase. Expect",
  "versus the £265k asking. **[W4]** Earlier price views cut. Expect"),
 ("tops out at about £325–360k, and loses money above about a £220k purchase.", "tops out at about £325–360k. **[W4]** Break-even purchase figure cut."),
 ("- About 69 m² by the EPC, which may not include the extension.", "- About 69 m² by the EPC (figure from your notes, not re-found **[W4]**), which may not include the extension."),
 ("- As-is value about £245–260k. Today's-money comps (£255–286k for 69–84 m²) sit at or a little above the top of that range.", "- **[W4]** Earlier as-is band cut. Today's-money comps: £255–286k for 69–84 m²."),
 ("At 69 m²: **£236k / £251k / £277k**. The median backs £245–260k; expect the agent to argue up to the upper quartile. Asking", "At 69 m²: **£236k / £251k / £277k**. Asking"),
 ("- Neighbours back the guide: No. 12, same agent and same guide, sold", "- Neighbours sold near the guide **[W4]**: No. 12, same guide, sold"),
 ("- Rival 3-bed terraces near Woodseats at about £220k, asking now: Woodseats Road (Whitehornes, 1,393 sq ft, leasehold), Holmhirst Drive (Whitehornes), Hackthorn Road (freehold).",
  "- **[W4]** Rival 3-bed terraces near Woodseats, asking now: Woodseats Road (Redbrik, guide £220–230k, 1,216 sq ft, freehold); Hackthorn Road (guide £220–240k, end terrace, freehold). Holmhirst Drive: no listing found."),
 ("- Rightmove also shows an Underwood Road terrace at offers around £220k, listed by Hunters on 30 Oct. Is that this house with a second agent?",
  "- Rightmove showed an Underwood Road terrace at offers around £220k, listed by Hunters on 30 Oct; gone by 20 Nov **[W4]**. Was that this house with a second agent?"),
 ("brought up to date. So the asking price builds in nothing for any work they've done since.", "brought up to date. **[W4]** Judgement on their works cut."),
 ("**Margin −£52k to −£30k** (was −£28k).", "**[W4]** Margin cut."),
 ("- Nine months unsold is the strongest sign of a seller who needs to move.", "- Nine months unsold **[W4]**."),
 ("**Margin −£40k to −£26k** (was −£95k). ", "**[W4]** Margin cut. "),
 ("Hollythorpe Crescent £240k (807 sq ft) went STC.", "Hollythorpe Crescent guide £240–250k (807 sq ft, freehold), not shown as STC on 20 Nov **[W4]**."),
]
sp = ROOT / "out/saturday-viewings-2026-11-21.md"; s = sp.read_text()
for o, n in S: s = sub1(s, o, n, "saturday")
sp.write_text(s)
print("applied")
