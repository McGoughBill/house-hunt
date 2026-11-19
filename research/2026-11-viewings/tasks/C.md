You are one of several agents researching houses in Sheffield.
Task: C — Certificates: energy certificates, FENSA, Gas Safe
Work in: /home/claude/house-hunt/research/2026-11-viewings (all paths below are relative to it).
Houses: read houses.yaml (ids: falmouth, welby, leeshall, cawthorne, underwood, helmton, hollythorpe)
Sources you may use: find-energy-certificate.service.gov.uk (energy-certificate register), FENSA certificate check, Gas Safe Register
Fields to find, per house: epc_certificates, epc_floor_area_m2, epc_current_band, epc_property_type, epc_improvements, fensa_record, gas_safe_record
Write: one line per fact to facts/C.jsonl, matching schema/fact.json.
  Easiest: python3 scripts/facts.py add facts/C.jsonl '<one JSON object>' (it validates).
epc_certificates: every certificate, as a list of {date, band, floor_area_m2, url}. epc_improvements: the list with cost ranges, quoted from the latest certificate. The shell cannot reach the register (fetch_epc.py failed), so use the web tools.
Check facts/seen_urls.txt before fetching; add every URL you fetch (append, one per line).
Rules: cite a URL for every fact; null plus reason if not found;
at most 15 fetches; no listing portals (Rightmove, Zoopla, OnTheMarket, agents' sites);
no contact with anyone; send no email; buy or order nothing (no title registers);
never use death notices or obituaries; do not run git.
Return: at most 80 words — done or partial, count of facts, gaps.
