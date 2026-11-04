# Map the vibe onto neighbourhoods

Today is {{date}}. A buyer wants a home in or near {{city}}, {{country}}.

**Their vibe:** {{vibe}}
**Model areas they already like:** {{model_areas}}
**Anchors (places to be near):** {{anchors}}
**Budget:** asking up to {{price_max}} {{currency}} for {{beds_min}}+ bedrooms.

Find every neighbourhood within reach that matches the vibe, where houses of that size can be bought within budget. Model areas count only if they still fit the budget. For each neighbourhood, use web search to check typical prices for that size, the housing stock and its character (period, inter-war, new-build), parks, high street, schools, transport, and any reasons to avoid it (student lets, main roads, flood risk, crime).

Write a JSON array to `{{out_path}}`. Each item has: `name, district (postal district/zip), fit (1-5 for the vibe), budget_fit ("comfortable"|"stretch"|"over"), typical_price, stock, why (one line), watch_out (one line), sources (urls)`. Sort the array by fit, best first.

Then reply with one line only: `OK areas <count>`.
