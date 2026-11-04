# List where these houses are sold

Today is {{date}}. A buyer wants a house in these areas of {{city}}, {{country}}: {{areas}}.

Use web search to find every high-value place where houses for sale in those areas get listed. Cover:
- the national property portals for {{country}}, and any portal that shows floor area or condition;
- the local estate agents or brokers that actually sell in those areas, with their branch;
- auctions and auction aggregators;
- any probate, off-market or price-drop sources.

For each source, write one paragraph an agent could follow: the site, which branch covers which area, what its listing URLs look like, and any known trick. For example, if the portal blocks automated fetches, say where else the same stock shows.

Write a JSON array to `{{out_path}}`, each item `{"name": "...", "desc": "..."}`. List 12–25 sources, most useful first. Also write `{{comps_path}}` as one line naming where sold prices and floor areas can be found in {{country}}.

Then reply with one line only: `OK sources <count>`.
