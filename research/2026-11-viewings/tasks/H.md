You are one of several agents researching houses in Sheffield.
Task: H — Hazards: mining, ground, flood, knotweed, protected trees
Work in: /home/claude/house-hunt/research/2026-11-viewings (all paths below are relative to it).
Houses: read houses.yaml (ids: falmouth, welby, leeshall, cawthorne, underwood, helmton, hollythorpe)
Sources you may use: Mining Remediation Authority (Coal Authority) interactive map, BGS GeoIndex, Environment Agency flood maps (check-long-term-flood-risk.service.gov.uk), Environet knotweed map, Sheffield City Council TPO map
Fields to find, per house: coal_mining_risk, landslip, made_ground, shrink_swell, flood_rivers, flood_surface_water, knotweed_nearby, tree_preservation_order
Write: one line per fact to facts/H.jsonl, matching schema/fact.json.
  Easiest: python3 scripts/facts.py add facts/H.jsonl '<one JSON object>' (it validates).
Hollythorpe's postcode is unknown: find it from public records first, or record facts at street level and say so.
Check facts/seen_urls.txt before fetching; add every URL you fetch (append, one per line).
Rules: cite a URL for every fact; null plus reason if not found;
at most 15 fetches; no listing portals (Rightmove, Zoopla, OnTheMarket, agents' sites);
no contact with anyone; send no email; buy or order nothing (no title registers);
never use death notices or obituaries; do not run git.
Return: at most 80 words — done or partial, count of facts, gaps.
