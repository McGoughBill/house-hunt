# Wave 1 status: Saturday houses

*19–20 Nov 2026. Waves 0 and 1 only; wave 2 not started. Repo: `McGoughBill/house-hunt`, branch `research-nov-viewings`, folder `research/2026-11-viewings/`. Every figure below has a source line in `facts.json`.*

## Did the Land Registry script work?

**No.** The shell's proxy refuses Land Registry, the price index and the energy-certificate register (403, policy block), so `fetch_lr.py` and `fetch_epc.py` were not run. The energy-certificate API also needs a free key. Agents S1–S4 did the comparables instead. They could reach Land Registry's street and postcode search through the web tools, but not whole-sector searches or the price index. So sale prices aren't adjusted to today's market yet, and no floor areas came from certificates.

Agents read the sale rows through a tool that summarises pages, so check any figure against the raw Land Registry record before it goes into an offer.

## Facts found per house

241 lines in all. A "null" line means the agent looked and couldn't get the data. It always gives the reason.

| House | Filled | Null | Main finds |
|---|---|---|---|
| Market | 14 | 5 | Bank Rate raised to 4% on 5 Nov; next decision 17 Dec. RICS new buyer enquiries −24, new listings −8 (Oct). Average 2- and 5-year fixes about 6.0%. Sheffield semi average £239k (Sep, +1.8% over the year). |
| Falmouth | 11 | 19 | Listed 27 Aug at £215k, cut to £210k on 9 Oct. Last sold £119,950 (Jan 2012), leasehold. Street's highest sale £290k (No. 7, 2023). Only recent sale: No. 33, £240k (Jul 2026). |
| Welby | 14 | 18 | Listed 2 Sep at £265k, no cut. Bought £242k on 19 Nov 2021, freehold. No detached sale on the street in two years. Highest sale on the street: £292.5k (No. 42, a terrace, Nov 2025). |
| Lees Hall | 13 | 21 | Listed 8 Sep at £290k, no cut. Zoopla lists it as leasehold. No sale of No. 57 on record since 1995. |
| Cawthorne | 13 | 18 | 3-bed semi, 80 m², freehold, hall. Listed 31 Jul. No. 6 bought for £253k in Apr 2023. No. 12 had the same agent and the same guide, and sold for £315k (Oct 2025). No. 8 sold for £320k (Dec 2025). |
| Underwood | 10 | 19 | Leasehold terrace, last sold £140k (Dec 2020). Highest terrace sale on the street: £200k (No. 56, Jul 2025). Listing history not found. |
| Helmton | 13 | 19 | 3-bed semi, 73 m², freehold. Listed 17 Jun at offers in the region of £300k, then £270k (14 Oct), now offers over £265k. Last sold £190k (Dec 2018), freehold. |
| Hollythorpe | 15 | 18 | Postcode S8 9NF. Listed 23 Feb 2026 at offers in the region of £280k, 731 sq ft (68 m²), freehold. Last sold £136.5k (2010). |

## Gaps

- **Hazards (all houses): nothing found.** The proxy blocks the Coal Authority, BGS and Environment Agency maps. The flood checker needs a captcha. The knotweed and protected-tree maps need JavaScript. Check Cawthorne's flood risk (River Sheaf) yourself before Saturday: [check-long-term-flood-risk.service.gov.uk](https://check-long-term-flood-risk.service.gov.uk).
- **Energy certificates, FENSA and Gas Safe (all houses): nothing found.** The certificate register blocks automated fetching. The FENSA and Gas Safe checks needed your approval, which never came. So no floor areas came from certificates: Falmouth's 108 m² vs 94 m² is still open.
- **Planning history and building-control sign-off (all houses): nothing found.** Sheffield's planning portal blocks automated fetching.
- **Conservation areas.** Probably none at Welby, Lees Hall, Hollythorpe or Cawthorne (medium confidence). Falmouth is unresolved: if it's inside the Nether Edge conservation area, the area's Article 4 direction (2005) applies. Underwood and Helmton are unresolved too, with the Norton conservation area nearby.
- **Market.** No current figure for how far below asking houses sell. No count of S8 houses for sale, so no months of stock. S8 sales run about 45 a month (Mar–May 2026). No days-on-market or price-cut share for S8: Home.co.uk and PropertyData wouldn't load.
- **Underwood's listing history.** Zoopla 74619438 wasn't opened, because that page needed your approval.

## Clashes between sources

The merge script found no clashes, because sources gave the same thing under different field names. These clashes I found by hand:

1. **Helmton's size and tenure.** The Saturday doc says about 109 m² and "one source says a 136-year lease". Both figures match **No. 25** Helmton Drive: a 1,171 sq ft end terrace on a 137-year lease, now Sold STC. For **No. 17**, Land Registry says freehold semi (2018 sale). The Whitehorn listing at £265k says 786 sq ft (73 m²), 3-bed, freehold. Whitehorn also lists a 2-bed semi on the same road at £265k (1,026 sq ft, freehold), so confirm which house is No. 17.
2. **Lees Hall's tenure.** Zoopla's card for the Staves £290k listing says leasehold. Land Registry has no sale since 1995 to show it. 8 of the 9 semis sold on the street recently were leasehold.
3. **Hollythorpe's tenure.** The 2010 sale was filed twice at the same price, once leasehold and once freehold, which suggests the freehold was bought along with the house. The listing says freehold.
4. **Welby, to let or for sale.** The Staves web address reads "for-rent", but every portal shows it for sale. I found no advert to let it. A SpareRoom advert for a 2-bed detached bungalow near Meersbrook Park lists a garage and drive. Welby has a workshop and one-car parking, so it's a different house.
5. **The national trend.** Nationwide says +0.5% over the year (Oct), Halifax/Lloyds −1.2% (Oct), ONS +1.2% (Sep). They agree prices are flat. They don't agree on which way they're moving.

## What changes Saturday

- **Helmton (14:00) is a different house from the one in the notes.** It's about 73 m², not 109, so the asking price is about £3,630/m², not £2,431. That makes it far less cheap. It's freehold, so it passes your lease rule. The −£28k margin rested on the wrong size, so work it out again. Lever: five months on the market and two cuts, from offers in the region of £300k down to offers over £265k (−12%). The seller paid £190k in 2018.
- **Hollythorpe (14:45) has been for sale since 23 February:** nine months unsold, at £4,123/m² for 68 m². That's the strongest sign of a seller who has to move, and it lines up with your plan to cut deep. Ask why it hasn't sold.
- **Lees Hall (12:00) is probably leasehold.** Ask about the ground rent and the lease length. No. 57 hasn't changed hands since before 1995, so it may be a long-held or estate sale. Ask the agent; never use obituaries. The asking price is £4,203/m² on the energy certificate's 69 m². Recent street sales ran £3,273–£3,884/m², and No. 26 sold for £5k less in 2025 than in 2024. A rival on the same road at offers in the region of £250k (Yopa, leasehold) has sat unsold since March after a cut.
- **The Cawthorne (12:45) guide is backed by its neighbours.** Nos. 8 and 12 sold for £315–320k in late 2025. Your lever is the £253k the seller paid in April 2023: the guide is 19–28% above that. Also, 111 days on the market. It has a hall, so it passes the front-door rule.
- **Underwood's (13:30) asking price is above anything a terrace on the street has fetched.** £220k against a top terrace sale of £200k (No. 56, Jul 2025). It's leasehold, and it last sold for £140k in Dec 2020.
- **Falmouth (10:15) has already been cut once** (£215k to £210k). Every sale on the street is leasehold.
- **Welby (11:30): no change.** Unsold for 11 weeks with no cut, and no sign it's also advertised to let.
- **Market line for every agent:** Bank Rate went up on 5 Nov. Fixed rates are about 6%. RICS buyer enquiries are falling. The next rate decision is 17 Dec. All of these back an offer before Christmas.

*Facts, not advice. The sizes for Helmton, Hollythorpe and Cawthorne come from listings; measure them on Saturday.*

## Follow-ups (19 Nov, 23:40)

- **Land Registry spot-check:** raw rows match the agents' figures for all seven houses and the comparables quoted. Helmton confirmed: No. 17 is a freehold semi (£190,000, Dec 2018), and No. 25 is a leasehold terrace.
- **Underwood:** listed 28 Oct at offers around £220k, 85 m², leasehold. A Hunters listing on the same street at the same price (30 Oct) may be the same house with a second agent: a question for Saturday.
- **Welby rivals:** no 2-bed detached bungalow for sale within 1 km. The nearest is on Kennedy Road, Woodseats, at about £3,900/m².
- **Cawthorne rivals:** five 3-bed semis within 1 km at £250–325k, listed in the Saturday doc.
- **Hollythorpe:** neighbours sold at £295–330k in 2025, which cuts against the £241k done-up estimate.
- **`facts.py merge`** now checks clashes across field names, and against the Saturday doc's own figures (`claims` in `houses.yaml`). It now flags Helmton's tenure and size by itself.
- **Everything I couldn't check online** (hazards, energy certificates, planning, FENSA and Gas Safe) is now in the Saturday doc as questions for each agent.
