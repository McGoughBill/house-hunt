Here are briefs and the facts file: /home/claude/w4-verify/saturday-briefs-2026-11-21.md and /home/claude/w4-verify/saturday-viewings-2026-11-21.md; facts.json.
For every number and claim, find its fact line and open its source.
Mark each as confirmed, wrong (with the right value) or unsupported.
Change nothing else. Write your marks to /home/claude/w4-verify/out/B.md. Return at most 80 words.

## Wave 4 detail (checker B)

You check a buyer's viewing briefs for houses in Sheffield, viewed on Sat 21 Nov 2026. You have seen none of the work behind them.
Work ONLY in /home/claude/w4-verify. Read nothing outside it: no repo, no status docs, no agent reports, no working notes. If a file you'd like isn't
in the pack, you can't have it; say so.

Pack: saturday-briefs-2026-11-21.md (the briefs), saturday-viewings-2026-11-21.md (the Saturday doc), facts.json (house -> field ->
[fact lines with source URLs]; the W4C lines are new comparables and top prices), settled.yaml (rulings on clashes between sources),
data/ (raw sale rows in data/sales/*.jsonl, Sheffield UK HPI by type in data/hpi_sheffield_ukhpi.csv from 2016-01 and
data/hpi_sheffield.csv from 2010-10, bungalow_sales.csv for the Welby model).

Your houses: 6 Cawthorne Grove (cawthorne), 38 Underwood Road (underwood), 17 Helmton Drive (helmton), 51 Hollythorpe Road (hollythorpe).

For each of your houses:
a. Every £, m², date, tenure and days-listed figure in its brief, and every W4C comparable and top price in facts.json: find its fact
   line, open its source with WebFetch, and mark it confirmed, wrong (give the right value and source) or unsupported. If the source is
   blocked or won't open, mark it "unverifiable: blocked"; don't guess. Listing portals and agents' sites may be blocked: try once.
b. Open the raw Land Registry record for every sale quoted (landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&...
   by street, postcode or with min_date/max_date). Check address, date, price, type and tenure.
c. With your own short python script (in /home/claude/w4-verify/out/B_calc.py), straight from the raw sale rows and the HPI file, recompute:
   each house's £/m² figures (median, quartiles), comparable range, last sale in today's money (index month 2026-09 by type) and the
   street and area top prices. Report every difference over 2% from the brief or facts.json. Don't use or ask for comps.py.
d. Every lever (the "Levers" bullets): does the source say what the brief claims? Flag any lever that overstates its evidence.
e. Check the brief against the Saturday doc: viewing times, addresses, postcodes, agents, phone numbers, prices.
f. Flag any figure that gives away the buyer's budget, deposit, mortgage or price ceiling, and any opening offer, walk-away figure or
   verdict (e.g. "too dear", "buy", "the favourite"), in the brief or in the Saturday doc's section for the house.
g. Write your findings to /home/claude/w4-verify/out/B.md as one markdown table per house: | item | brief says | source says | verdict |, verdict one of
   confirmed, wrong, unsupported, overstated, unverifiable: blocked, leak. Then a count per house per verdict.

Rules: web tools only (WebFetch, WebSearch); the shell has no internet. At most 60 fetches. No contact with estate agents or sellers,
no emails, buy or order nothing (no title registers), never use death notices or obituaries. Don't edit any file except /home/claude/w4-verify/out/B.md and your
calc script. Don't run git. Return at most 80 words: counts per verdict and the three most serious findings.
