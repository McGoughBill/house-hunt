You are one of several agents researching houses in Sheffield.
Task: W2a — Market gaps: how far below asking houses sell now; S8 days on market and share of listings cut
Work in: /home/claude/house-hunt/research/2026-11-viewings (all paths below are relative to it).
Houses: read houses.yaml (ids: market)
Sources you may use: Zoopla House Price Index reports (business.zoopla.co.uk / zoopla.co.uk/discover), Rightmove House Price Index press releases (plc.rightmove.co.uk, rightmove.co.uk/news), Sheffield estate agents' published market reports, Jitty or other published local market statistics pages, ONS/Land Registry sales counts. Research and press pages only: never open a property listing.
Fields to find, per house: sale_vs_asking_gap_pct, s8_median_days_on_market, s8_share_listings_price_cut, s8_listings_for_sale, s8_months_of_stock, sheffield_days_to_sell, sheffield_share_listings_cut
Write: one line per fact to facts/W2a.jsonl, matching schema/fact.json.
  Easiest: python3 scripts/facts.py add facts/W2a.jsonl '<one JSON object>' (it validates).
Latest month available (Oct or Nov 2026 ideally); say in note the area (UK, Yorkshire, Sheffield, S8) and the month each figure covers. If no S8 figure exists, give the nearest wider area (Sheffield, then Yorkshire and the Humber) under the sheffield_* field, and keep the s8_* field null with the reason. Months of stock = listings / sales per month (S8 sales run about 45 a month, Mar-May 2026, per facts/M2.jsonl); show the sum.
Known blocked, do not try: map.bgs.ac.uk and BGS GeoIndex; the Coal Authority/Mining Remediation Authority interactive map; check-long-term-flood-risk.service.gov.uk (captcha) and Environment Agency ArcGIS map services; planningapps.sheffield.gov.uk; find-energy-certificate.service.gov.uk; Environet's knotweed map; Sheffield's TPO map; Home.co.uk; PropertyData. The shell cannot reach the web at all: use WebSearch and WebFetch only.
Check facts/seen_urls.txt before fetching; add every URL you fetch (append, one per line).
Rules: cite a URL for every fact; null plus reason if not found;
at most 15 fetches; no listing portals (Rightmove, Zoopla, OnTheMarket, agents' sites);
no contact with anyone; send no email; buy or order nothing (no title registers);
never use death notices or obituaries; do not run git.
Return: at most 80 words — done or partial, count of facts, gaps.
