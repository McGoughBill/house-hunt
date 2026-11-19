You are one of several agents researching houses in Sheffield.
Task: W2c — Floor areas for comparable sales, and sales back to Nov 2023, so more sales get a £/m²
Work in: /home/claude/house-hunt/research/2026-11-viewings (all paths below are relative to it).
Houses: read houses.yaml (ids: falmouth, welby, leeshall, cawthorne, underwood, helmton, hollythorpe)
Sources you may use: HouseMetric (housemetric.co.uk street pages: Land Registry prices joined to energy-certificate floor areas), Land Registry price-paid search (landregistry.data.gov.uk/app/ppd, street or postcode CSV), other sold-price pages that show a floor area and cite Land Registry or the energy-certificate register (e.g. Chimnie, Bricks&Logic sold-price pages, never a for-sale listing).
Fields to find, per house: comps_floor_areas_added
Write: one line per fact to facts/W2c.jsonl, matching schema/fact.json.
  Easiest: python3 scripts/facts.py add facts/W2c.jsonl '<one JSON object>' (it validates).
Goal: for each house's street and full postcode, every sale since 19 Nov 2023 of the same Land Registry type as the house (falmouth T; welby D; leeshall S; cawthorne S; underwood T; helmton S; hollythorpe S), each with floor_area_m2 where any source gives it. Existing sales are in data/sales/S1-S4.jsonl (Nov 2024 on, no floor areas). Write every sale you find or confirm, old or new, to data/sales/W2c.jsonl, one per line, matching schema/sale.json, with floor_area_m2 (m², 1 sq ft = 0.0929 m²) and its source URL in a field area_source. Keep source = the Land Registry or sold-price URL for the price. Same address+date+price as an existing line is fine: comps.py merges them. Best route: one HouseMetric street page per street (e.g. https://housemetric.co.uk/house-prices/Welby-Place/S8-9D), which lists price, date and m² together. Streets: Falmouth Road S7 2; Welby Place S8 9; Lees Hall Road S8 9; Cawthorne Grove S8 0; Underwood Road S8 8; Helmton Drive S8 8; Hollythorpe Road S8 9. Then, per house, one fact line field comps_floor_areas_added: value = count of same-type sales since Nov 2023 with a floor area, note = gaps. Do not open the seven houses' own for-sale listings.
Known blocked, do not try: map.bgs.ac.uk and BGS GeoIndex; the Coal Authority/Mining Remediation Authority interactive map; check-long-term-flood-risk.service.gov.uk (captcha) and Environment Agency ArcGIS map services; planningapps.sheffield.gov.uk; find-energy-certificate.service.gov.uk; Environet's knotweed map; Sheffield's TPO map; Home.co.uk; PropertyData. The shell cannot reach the web at all: use WebSearch and WebFetch only.
Check facts/seen_urls.txt before fetching; add every URL you fetch (append, one per line).
Rules: cite a URL for every fact; null plus reason if not found;
at most 20 fetches; no listing portals (Rightmove, Zoopla, OnTheMarket, agents' sites);
no contact with anyone; send no email; buy or order nothing (no title registers);
never use death notices or obituaries; do not run git.
Return: at most 80 words — done or partial, count of facts, gaps.
