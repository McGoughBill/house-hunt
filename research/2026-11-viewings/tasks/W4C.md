You are one of several agents researching houses in Sheffield.
Task: W4C — Comparables and top prices for all seven houses: at least 2 comparable sales each, widening step by step
Work in: /home/claude/house-hunt/research/2026-11-viewings (all paths below are relative to it).
Houses: read houses.yaml (ids: falmouth, welby, leeshall, cawthorne, underwood, helmton, hollythorpe)
Sources you may use: Land Registry price-paid search via WebFetch (landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=...&town=SHEFFIELD, or &postcode=S8+9DB, or &postcode=S8+9 for a sector, with min_date/max_date and property_type=detached|semi-detached|terraced); postcodes.io for coordinates (https://api.postcodes.io/postcodes/<postcode>) to measure distance; HouseMetric street pages and other sold-price pages that cite Land Registry or the energy-certificate register, for floor areas only. Never a for-sale listing.
Fields to find, per house: comparable, street_top_price_ever, area_top_price_same_type, comps_summary
Write: one line per fact to facts/W4C.jsonl, matching schema/fact.json.
  Easiest: python3 scripts/facts.py add facts/W4C.jsonl '<one JSON object>' (it validates).
Already known (read first, do not refetch): data/sales/S1-S4.jsonl and W2c.jsonl (sales and floor areas), out/comps/summary.json
(street and postcode summaries, street_ceiling_ever, last sale), facts.json. Land Registry types: falmouth T (mid-terrace); welby D (detached
bungalow, 60 m², built about 1990); leeshall S; cawthorne S; underwood T; helmton S; hollythorpe S. Falmouth, Welby, Underwood and Helmton
have fewer than 2 usable comparables now; Lees Hall, Cawthorne and Hollythorpe have enough, so for those three pick the 2-4 best
existing ones (same street, same type, nearest size, most recent) and add only the two top prices.

For each house, widen step by step and STOP at the first step that gives at least 2 comparables:
  1. Same street, same type, any age.
  2. Same type within 500 m of the house, last 5 years (since Nov 2021).
  3. Similar type within 1 km (e.g. a semi for a terrace, any detached house for a bungalow), last 5 years.
  4. Older sales of the step-2 or step-3 kind.
A sale counts only once a Land Registry record (or a sold-price page that quotes one) gives its address, date and price. Exclude new builds,
category-B (non-market) sales, and the house's own past sales.

Write ONE fact line per comparable, field "comparable", value an object:
 {"address","postcode","date","price","value_today","age_band","type","tenure","floor_area_m2","distance_m","differs","step","lr_record"}
 - value_today: price x index(2026-09, type) / index(sale month, type), Sheffield UK HPI. Use data/hpi_sheffield_ukhpi.csv
   (2016-01 on; columns detached, semi_detached, terraced). For 2010-10 to 2015-12 use data/hpi_sheffield.csv (same UK HPI series,
   long form) and say so in note. Before 2010-10: null, with the reason. Do the sums in a short python script, not by hand.
 - age_band, counted back from 19 Nov 2026: <1, 1-2, 2-3, 3-4, 4-5, 5-6 or 6+ yrs.
 - distance_m: straight line from the house's postcode centre to the sale's postcode centre (postcodes.io), rounded to 10 m;
   0 for same postcode. Say "postcode centres" in note.
 - differs: a few words, e.g. "end terrace, 12 m² larger, freehold".
 - step: 1-4. lr_record: the Land Registry URL that shows this sale (also put it in source).
Also append each comparable as a sale row to data/sales/W4C.jsonl (schema/sale.json, plus "house" and "step" keys) so the checkers can
recompute from raw rows.

Per house, also:
 - street_top_price_ever: value {address, date, price, type, tenure, value_today}: the highest price ever paid on the house's street,
   any type, from a Land Registry street query with no date limit. Check out/comps/summary.json street_ceiling_ever and confirm or correct it.
 - area_top_price_same_type: value {address, date, price, value_today, area}: the highest price paid for the house's type in its
   postcode sector (S7 2, S8 0, S8 8 or S8 9; name the sector in area). Query the sector with the type filter; if the query only
   works over a date window, give the window in note and say "highest found in <window>", not "ever".
 - comps_summary: value {n, steps_used, range_today_low, range_today_high}, note = gaps or doubts.
Known blocked, do not try: map.bgs.ac.uk and BGS GeoIndex; the Coal Authority/Mining Remediation Authority interactive map; check-long-term-flood-risk.service.gov.uk (captcha) and Environment Agency ArcGIS map services; planningapps.sheffield.gov.uk; find-energy-certificate.service.gov.uk; Environet's knotweed map; Sheffield's TPO map; Home.co.uk; PropertyData. The shell cannot reach the web at all: use WebSearch and WebFetch only.
Check facts/seen_urls.txt before fetching; add every URL you fetch (append, one per line).
Rules: cite a URL for every fact; null plus reason if not found;
at most 35 fetches; no listing portals (Rightmove, Zoopla, OnTheMarket, agents' sites);
no contact with anyone; send no email; buy or order nothing (no title registers);
never use death notices or obituaries; do not run git.
Return: at most 80 words — done or partial, count of facts, gaps.
