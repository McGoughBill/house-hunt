You are one of seven agents, each writing the judgement part of one house's viewing brief. The buyer, Bill, views seven Sheffield houses on Saturday 21 Nov 2026 and reads these briefs on his phone at the door.
House: hollythorpe — 51 Hollythorpe Road, Norton Lees, Sheffield, S8 9NF. Viewing 2026-11-21 14:45 (not yet confirmed by agent). Offers around £280,000, agent Whitehornes.
Work in: /home/claude/house-hunt/research/2026-11-viewings (all paths below are relative to it).

Read these, and only these (do not browse the web; everything you need is here):
1. out/briefs/hollythorpe.md — the rendered brief. Its Numbers part is fixed: don't repeat it, build on it.
2. out/briefs/hollythorpe.facts.md — every fact line for the house, with source and confidence; the null lines say what's unknown; then the wave 2 rulings and the market lines.
3. out/briefs/hollythorpe.comps.md — the comparables, sale by sale, and the value and margin working.
4. ref/saturday/hollythorpe.md — this house's section of the Saturday viewing doc (older notes; where it and the fact lines disagree, the fact lines and rulings win).
5. ref/plan/hollythorpe.md — this house's entry in the price-evidence plan §6. ref/price-evidence-plan-s2-s4-s6.md holds §2 (the viewing checks) and §4 (the pricing rules).
6. Special: viewing time not yet confirmed by Whitehornes. Already done up per listing. 269 days unsold with no cut.

The buyer: first-time buyer, no chain, agreement in principle. He buys cheap houses with sound bones and reworks them. Rules that end a house: the front door must open into a hall, lobby or porch, never straight into a room; freehold, or a lease of 150+ years with no live covenant dispute (profiles/sheffield-bill/brief.md; ask years left, ground rent, and any clause needing the freeholder's consent for alterations); serious structural movement. Areas in the briefs are from listings, not a tape: he measures on the day.

Write one file: out/briefs/hollythorpe.agent.md, with exactly these headings, in this order:

### Verdict
One line: "Pursue", "Pursue only at a deep cut" or "Drop", then why, in under 25 words.

### Price
Two bullets: **Open £X** and **Walk away £Y**, each with its working in one short clause (e.g. "street median £3,644/m² × 69 m² = £251k, less 3%"). Both are before any faults: Saturday's faults come off these. Where the comparables are thin (not the case here, but the rule stands), say "Comparables thin" and anchor on the street's top price, the last sale in today's money and the days on the market. Never stretch the comparables: don't borrow other streets or types to fake a £/m² value. Follow §4: open below the value, leave room to rise in shrinking steps. Where wave 2 gives a buy-test "most to offer", the walk-away must not exceed it.

### Levers
3–5 bullets, strongest first. Each is a true fact that argues the price down, with its source in brackets: the fact line's task id (e.g. [S3], [L], [W2c]) or [comps] or [value]. No bluffs, no guesses.

### Ask
At most 6 questions for the agent or seller, most valuable first, each one line. Include the tenure question if tenure is not settled at high confidence, and the wave 2 hazard questions that matter most here (flood, ground, knotweed, certificates; see the "At every house" list in ref/saturday/_common.md). Merge where you can.

### Check
5–8 things to look at in this house most likely to cut the price, from §2 and §6. One line each, with the sign to look for.

### Red flags
Walk away if… One line each, only for: the hall rule, the lease rule, structure. Say how to tell on the day.

### Never say
One or two lines: the figures and preferences to keep from the agent at this house (e.g. the walk-away, what the seller paid, the days unsold, which house he prefers, that Staves/Whitehornes' other houses are on his list).

### Working
Not shown to Bill; the check script reads it. For every £ figure, m² figure and date you used above that is not printed verbatim in out/briefs/hollythorpe.md, out/briefs/hollythorpe.facts.md or out/briefs/hollythorpe.comps.md, write one line showing where it came from or the sum that makes it, e.g. "£245k = £251,436 − 2.5%, rounded" or "£4,061 × 68 = £276,148". Mark estimates as estimates.

Rules:
- Every fact needs a source, or is marked as an estimate with its working.
- The seven parts above Working together: at most 260 words. Bill reads on a phone: about one and a half screens for the whole brief.
- Style: plain English, short words, active voice, no stock phrases, every word earning its place. Numbers, units and names checked. Use £ and m²; round prices to £1k (e.g. £245k).
- No web browsing, no contact with anyone, no email, buy nothing. Never use death notices or obituaries. Don't run git. Don't edit any file but out/briefs/hollythorpe.agent.md.
- When done, run: python3 scripts/brief.py — and read out/briefs/hollythorpe.md to see your parts in place. Fix anything that reads badly.
Return: at most 60 words — the verdict, open and walk-away figures, and anything you could not support.
