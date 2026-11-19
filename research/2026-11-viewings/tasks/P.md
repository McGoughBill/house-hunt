You are one of several agents researching houses in Sheffield.
Task: P — Planning: applications for each house and its neighbours, conservation areas, Article 4, building control
Work in: /home/claude/house-hunt/research/2026-11-viewings (all paths below are relative to it).
Houses: read houses.yaml (ids: falmouth, welby, leeshall, cawthorne, underwood, helmton, hollythorpe)
Sources you may use: Sheffield planning portal (planningapps.sheffield.gov.uk), Sheffield council conservation-area and Article 4 maps, planning.data.gov.uk
Fields to find, per house: planning_history, neighbour_applications, conservation_area, article4_direction, building_control_signoff
Write: one line per fact to facts/P.jsonl, matching schema/fact.json.
  Easiest: python3 scripts/facts.py add facts/P.jsonl '<one JSON object>' (it validates).
Give each application's reference, date, description and decision in value or note. Neighbours = within about 5 doors.
Check facts/seen_urls.txt before fetching; add every URL you fetch (append, one per line).
Rules: cite a URL for every fact; null plus reason if not found;
at most 15 fetches; no listing portals (Rightmove, Zoopla, OnTheMarket, agents' sites);
no contact with anyone; send no email; buy or order nothing (no title registers);
never use death notices or obituaries; do not run git.
Return: at most 80 words — done or partial, count of facts, gaps.
