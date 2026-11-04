# Judge one house

Judge this house for a buyer who will refurbish it and then live in it. Be sceptical, and mark any guess "est.". Work alone, and do not read other results.

## The house
- ID: {{id}} · Run: {{run}}
- Address: {{street}}, {{area}}, {{postcode}}
- Asking: {{price}} · Beds: {{beds}} · Floor area: {{m2}} · Tenure: {{tenure}}
- State: {{state}} · Agent: {{agent}}
- Listing: {{link}}
{{context}}
## Steps
1. Open the listing, photos and floorplan. If the page fails, find the house by street, agent and price on another portal or on the agent's site. If it has gone or is sold, set `"live": false`, fill in what you can, and stop. If you cannot open it or find it anywhere, set `"live": null` and every score to null, and still write the file.
2. Find V: the median of 3 done-up sales of the same type on the same street in the last 2 years. Use {{comps_sources}}. If there are fewer than 3, use the nearest similar street and say so in `v_basis`.
3. Price the works W from the floorplan and photos, aiming at the finished spec: {{finished_spec}} W excludes contingency.
4. Buying costs C: {{tax_note}} Add {{fees}} fees, and any auction reservation fee or buyer's premium.
5. Read `{{brief_path}}` and check every gate. A gate fails only on evidence that it fails. If the listing is silent, pass the gate and start its reason with "unconfirmed:". If any gate fails, still score everything, but set `"verdict": "REJECT"`.
6. Score each criterion in `"scores"` from 1 to 5, using the bands in the brief. The brief marks some criteria "computed"; leave those out.
7. Note the walk or transit time to each anchor in `anchors`: {{anchors}}.

Give a URL for every fact you found. Any fact without a URL is "est.".

## Output
Write one JSON object to `{{out_path}}` with the Write tool. Numbers are plain integers, in money or m² (no symbols, no commas, no "k"). Use null when unknown. Every score is an integer from 1 to 5, and `est` is true when the score rests on a guess.

```json
{"id": "{{id}}", "run": "{{run}}", "live": true, "listing_url": "", "asking": 0, "floor_area_m2": null,
 "house_type": "terrace|semi|detached|end-terrace",
 "gates": {{gates_json}},
 "V": 0, "v_basis": "3 sales: address, date, price", "W": 0, "w_basis": "main items and costs", "C": 0,
 "scores": [{"n": 1, "score": 3, "est": false, "evidence": "one line"}],
 "anchors": {"<anchor>": "minutes and mode"},
 "verdict": "PASS|REJECT", "biggest_risk": "one line", "sources": ["url"]}
```
Then reply with one line only: `OK {{id}} r{{run}} <live> <verdict>`.
