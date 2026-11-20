You are one of seven agents, each writing the judgement part of one house's viewing brief. The buyer, Bill, views seven Sheffield houses on Saturday 21 Nov 2026 and reads these briefs on his phone at the door.
House: {id} — {address}, {postcode}. Viewing {viewing}. {price_text}, agent {agent}.
Work in: {root} (all paths below are relative to it).

Read these, and only these (do not browse the web; everything you need is here):
1. out/briefs/{id}.md — the rendered brief. Its Numbers part is fixed: don't repeat it, build on it.
2. out/briefs/{id}.facts.md — every fact line for the house, with source and confidence; the null lines say what's unknown; then the wave 2 rulings and the market lines.
3. out/briefs/{id}.comps.md — the comparables, sale by sale, and the value and margin working.
4. ref/saturday/{id}.md — this house's section of the Saturday viewing doc (older notes; where it and the fact lines disagree, the fact lines and rulings win).
5. ref/plan/{id}.md — this house's entry in the price-evidence plan §6. ref/price-evidence-plan-s2-s4-s6.md holds §2 (the viewing checks) and §4 (the pricing rules).
{extra}
The buyer: first-time buyer, no chain, agreement in principle. He buys cheap houses with sound bones and reworks them. Rules that end a house: the front door must open into a hall, lobby or porch, never straight into a room; freehold, or a lease of 150+ years with no live covenant dispute (profiles/sheffield-bill/brief.md; ask years left, ground rent, and any clause needing the freeholder's consent for alterations); serious structural movement. Areas in the briefs are from listings, not a tape: he measures on the day.

Write one file: out/briefs/{id}.agent.md, with exactly these headings, in this order:

### Levers
3–5 bullets, strongest first. Each is a true fact that argues the price down, with its source in brackets: the fact line's task id (e.g. [S3], [L], [W2c]) or [comps] or [value]. No bluffs, no guesses.

### Ask
At most 6 questions for the agent or seller, most valuable first, each one line. Include the tenure question if tenure is not settled at high confidence, and the wave 2 hazard questions that matter most here (flood, ground, knotweed, certificates; see the "At every house" list in ref/saturday/_common.md). Merge where you can.

### Check
5–8 things to look at in this house most likely to cut the price, from §2 and §6. One line each, with the sign to look for.

### Rule checks
One line each, only for: the hall rule, the lease rule, structure. Say what to look for on the day. No verdicts: Bill decides.

### Never say
One or two lines: the figures and preferences to keep from the agent at this house (e.g. his budget, what the seller paid, the days unsold, which house he prefers, that Staves/Whitehornes' other houses are on his list).

### Working
Not shown to Bill; the check script reads it. For every £ figure, m² figure and date you used above that is not printed verbatim in out/briefs/{id}.md, out/briefs/{id}.facts.md or out/briefs/{id}.comps.md, write one line showing where it came from or the sum that makes it, e.g. "£245k = £251,436 − 2.5%, rounded" or "£4,061 × 68 = £276,148". Mark estimates as estimates.

Rules:
- Every fact needs a source, or is marked as an estimate with its working.
- The seven parts above Working together: at most {words} words. Bill reads on a phone: about one and a half screens for the whole brief.
- Style: plain English, short words, active voice, no stock phrases, every word earning its place. Numbers, units and names checked. Use £ and m²; round prices to £1k (e.g. £245k).
- No web browsing, no contact with anyone, no email, buy nothing. Never use death notices or obituaries. Don't run git. Don't edit any file but out/briefs/{id}.agent.md.
- When done, run: python3 scripts/brief.py — and read out/briefs/{id}.md to see your parts in place. Fix anything that reads badly.
Return: at most 60 words — the strongest lever, and anything you could not support.
Never write a verdict, an opening offer or a walk-away figure: this is due diligence, not advice.
