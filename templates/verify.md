# Check one listing is live

Your only job is to check whether this house is still for sale, and to find a listing page for it that opens. Work alone, and do not judge or score the house.

## The house
- ID: {{id}}
- Address: {{street}}, {{area}}, {{postcode}}
- Asking: {{price}} · Agent: {{agent}}
- Saved link: {{link}}
- Other links seen: {{other_links}}

## Steps
1. **Open the saved link** with WebFetch.
   - It counts only if it is this one house's own listing page.
   - A search-results page, an agent's home page, or a page listing many houses does not count.
2. **If it fails or doesn't count, look elsewhere.** Find the same house (street, agent, price) on:
   - the agent's own site;
   - then Rightmove, Zoopla, OnTheMarket or PrimeLocation.
   Start with WebSearch, then fetch the result URLs. WebFetch accepts URLs that appeared in a search result, but often refuses URLs you build yourself.
3. **Read the status on the page that opened.** Quote every status word you see, word for word, in `evidence`. Look for: Sold STC, SSTC, Sale agreed, Under offer, Sold, Reserved, "No longer on the market", "Property not found", "no records were found". A "Sold" board image (for example a file named `*Board_Sold*`) counts as a sold status.
   - Ignore status words that belong to other houses on the page, such as "similar properties" cards.
   - Ignore words in navigation links, such as "Sold house prices".
4. **Set `status`:**
   - `live`: the house's own page opened and shows no sold or under-offer label.
   - `sstc`: Sold STC, SSTC or Sale agreed.
   - `under_offer`: Under offer or Reserved.
   - `sold`: Sold.
   - `gone`: Not found, no longer on the market, or the link redirects to a search or home page and you can't find the house anywhere else.
   - `unknown`: you couldn't open any page for this house.

Do not guess. A page you couldn't open is `unknown`, never `live`.

## Output
Write one JSON object to `{{out_path}}` with the Write tool:

```json
{"id": "{{id}}", "status": "live|sstc|under_offer|sold|gone|unknown", "loads": true, "url": "the single-house listing page that opened, or null", "price_text": "as shown, or null", "evidence": "status words quoted from the page, or what failed", "checked_urls": ["every URL you tried"]}
```

Then reply with one line: `{{id}} <status>`.
