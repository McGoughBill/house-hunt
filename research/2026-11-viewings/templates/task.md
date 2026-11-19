You are one of several agents researching houses in Sheffield.
Task: {task_id} — {scope}
Work in: {root} (all paths below are relative to it).
Houses: read houses.yaml (ids: {ids})
Sources you may use: {sources}
Fields to find, per house: {fields}
Write: one line per fact to facts/{task_id}.jsonl, matching schema/fact.json.
  Easiest: python3 scripts/facts.py add facts/{task_id}.jsonl '<one JSON object>' (it validates).
{extra}
Check facts/seen_urls.txt before fetching; add every URL you fetch (append, one per line).
Rules: cite a URL for every fact; null plus reason if not found;
at most {cap} fetches; no listing portals (Rightmove, Zoopla, OnTheMarket, agents' sites);
no contact with anyone; send no email; buy or order nothing (no title registers);
never use death notices or obituaries; do not run git.
Return: at most 80 words — done or partial, count of facts, gaps.
