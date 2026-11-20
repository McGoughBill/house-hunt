# Wave 2 status: numbers for the Saturday houses

*20 Nov 2026. Wave 2 only; wave 3 (briefs) not started. Repo `McGoughBill/house-hunt`, branch `research-nov-viewings`, folder `research/2026-11-viewings/`. Every figure comes from a script (`comps.py`, `value.py`, `mortgage.py`) or has a source line in `facts.json`.*

## Weaknesses first

- **Four of seven houses have too few comparables for a £/m² value.** Falmouth, Welby, Underwood and Helmton each have fewer than 3 same-type sales with a floor area in 3 years. I haven't widened the net to fill them. HouseMetric's robots rule blocked Falmouth Road and Underwood Road, and the energy-certificate register still blocks fetching.
- **Every area is from a listing or HouseMetric, not a tape measure.** At £3,600/m², each 5 m² error moves the value by about £18k.
- **Sale prices give no condition.** A done-up house and a wreck at the same £/m² look alike. So the quartiles show spread, not condition.
- **Flood checks used postcode centres, not houses.** Surface-water risk is still unknown for all seven.
- **Coal and landslip are known only for the area as a whole.** Most of Sheffield sits on coal measures.

## Numbers per house

All prices are brought to Sep 2026 (the latest month) with the official Sheffield house price index for that house type. Comparables: same Land Registry type, standard sales, sold since 19 Nov 2023, the house itself left out. Value as it stands = area × comparable £/m² (lower quartile / median / upper quartile). "Thin" = fewer than 3 such sales with a floor area.

| House | Area | Asking £/m² | Comparable £/m² today, median (lowest–highest): street; postcode | Street's highest price ever | Last sale → today | Value as it stands | Done-up margin | Days listed, cuts | Flood risk (rivers) |
|---|---|---|---|---|---|---|---|---|---|
| Falmouth (T) | 94 m² (108 by listing) | £2,234 (£1,944 at 108) | **Thin:** 1 terrace (No. 33, £240k, Jul 2026), no area; same for postcode | £290k (No. 7, Jun 2023; ≈ £324k today) | £119,950 (Jan 2012) → **£227,709** | **No £/m² value.** Anchors: No. 33 at £240k, last sale today £228k | Old shortlist: −£113k (its note says −£55k; not redone) | 84 days; 1 cut (£215k → £210k, −2.3%) | Postcode outside zones 2 and 3; a small Zone 2 patch 150–200 m south |
| Welby (D, bungalow) | 60 m² | £4,417 | **Thin:** no detached sale on the street since Nov 2021 | £292.5k (No. 42, terrace, Nov 2025); top detached £242k (No. 50, 2021) | £242,000 (Nov 2021) → **£279,147** | Bungalow model (wave 1): **£245–250k**; £227–277k on Welby Place alone | Not redone: plan says extending loses money above about a £220k purchase | 78 days; no cut | Outside zones 2 and 3 |
| Lees Hall (S) | 69 m² (may leave out the extension) | £4,203 | Street: **£3,644** (£3,042–£4,762), 13 of 16 with area; postcode: £3,566 (£3,401–£4,042), 3 of 4 | £551,551 (No. 13, 161 m² semi, Jan 2025) | No sale since 1995 | **£236k / £251k / £277k** | No works figure yet (after viewing) | 72 days; no cut | Outside zones 2 and 3 |
| Cawthorne (S) | 80 m² | £3,750 (£4,062 at £325k) | Street: **£3,644** (£2,326–£3,942), 8 of 11; postcode: £3,644 (£3,356–£3,942), 6 of 8 | £435k (No. 27C, detached, May 2025); top semi £350k (No. 27B, Apr 2025) | £253,000 (Apr 2023) → **£277,475** | **£270k / £292k / £306k** | No works figure yet; "recent improvements" per listing | 111 days; no cut | Outside zones 2 and 3 (checked first) |
| Underwood (T) | 85 m² | £2,588 | **Thin:** 1 terrace (No. 56, £200k Jul 2025 ≈ £207k), no area | £246k (No. 36, semi, Jun 2026); top terrace £200k | £140,000 (Dec 2020) → **£180,345** | **No £/m² value.** Anchors: top terrace £207k today, last sale today £180k | No works figure yet; listing says "in need of some renovation" | 22 days; no cut | Outside zones 2 and 3 |
| Helmton (S) | 73 m² | £3,630 | **Thin:** 1 semi (No. 1, 86 m², leasehold, £3,382/m²) | £300k (No. 1A, semi, Jul 2022) | £190,000 (Dec 2018) → **£264,933** | One sale gives £246,886 (thin). Last sale today £264,933 | **−£52k to −£30k** (was −£28k) | 155 days; 2 cuts (£300k → £265k, −11.7%) | Outside zones 2 and 3 |
| Hollythorpe (S) | 68 m² | £4,118 | Street: **£4,061** (£3,523–£4,250), 6 of 10; postcode: thin (2 of 4) | £330k (No. 80, Mar 2025; medium: the street extract may be cut off) | £136,500 (Oct 2010) → **£249,771** | **£249k / £276k / £286k** | **−£40k to −£26k** (was −£95k) | 269 days; no cut | Outside zones 2 and 3 |

**Working for the two redone margins.** The house-hunt buy test: margin = 0.9 × done-up value − 1.15 × works − £3,000 fees − asking. Both listings say the house is already done up, so works are £0–5k of cosmetics.

- **Helmton:** done-up value £246,886 (73 m² × £3,382, the one comparable) to £264,933 (the seller's 2018 price today). Margin = 0.9 × £246,886 − 1.15 × £5,000 − £3,000 − £265,000 = −£51,553, up to 0.9 × £264,933 − £0 − £3,000 − £265,000 = −£29,560. Most to offer by the same test: **£213k–£235k**.
- **Hollythorpe:** done-up value £276,148 (68 m² × median £4,061) to £285,532 (× upper quartile £4,199). Margin = 0.9 × £276,148 − £5,750 − £3,000 − £280,000 = −£40,217, up to 0.9 × £285,532 − £283,000 = −£26,021. Most to offer: **£240k–£254k**.

The 0.9 builds in a 10% safety cut, so a negative margin here doesn't mean the house is overpriced. It means it fails your buy-cheap test. Read against the comparables alone, Hollythorpe's asking price is fair (£4,118/m² against a street median of £4,061), and Helmton's is a little high on one thin comparable.

**Market.**
- How far below asking houses sell: no figure for the size of the gap exists in any open source. 81% of Propertymark's member agents reported sales below asking in Sep 2026 (UK-wide).
- Days to sell: UK median 44 days to sale agreed (Zoopla, Sep data). No Sheffield or S8 figure.
- S8 stock and price cuts: no S8 listing count, so no months of stock. S8 sells about 45–52 houses a month.
- Mortgage, £1,200 a month over 30 years: borrows £211,346 at 5.5%, £200,150 at 6.0% and £189,853 at 6.5%. Each half-point rise in rates cuts such a buyer's budget by £10–11k.

## What moved since the Saturday doc

| House | Figure | Was | Now |
|---|---|---|---|
| Helmton | Done-up value | £280k (old shortlist, 109 m²) | £247–265k (73 m²; one comparable, thin) |
| Helmton | Margin | −£28k | −£52k to −£30k |
| Helmton | Condition | Unknown; "the fault list carries the offer" | Already done up (listing: "modern and stylish throughout") |
| Hollythorpe | Done-up value | £241k (borrowed street) | £276–286k (6 street semis with areas) |
| Hollythorpe | Margin | −£95k | −£40k to −£26k |
| Hollythorpe | Condition | Unknown | Already done up ("immaculately presented, no expense spared") |
| Lees Hall | Street £/m² | £3,273–3,884 (4 sales, not indexed) | Median £3,644, quartiles £3,426–4,019 (13 sales, indexed) |
| Lees Hall | Value as it stands | £245–260k | £236k / £251k / £277k (quartiles). The median agrees; the range is wider |
| Cawthorne | Value as it stands | None | £270k / £292k / £306k. The guide's lower end (£300k) sits above the median |
| Falmouth | Last sale today | "Too old for the index" | £227,709 (index now reaches back to 2010) |
| Hollythorpe | Last sale today | "Too old for the index" | £249,771 |
| Falmouth | Conservation area | Unresolved | Probably just outside Nether Edge (medium), so Article 4 probably doesn't apply |
| Underwood, Helmton | Conservation area | Unresolved | Not in one (medium) |
| Underwood | Ground rent, band, EPC | Unknown | £0 ground rent, council tax A, EPC D, "needs some renovation" |
| All | River flood zone | Unknown | Outside zones 2 and 3 at every postcode; Falmouth has a Zone 2 patch about 150–200 m south |

## Gaps still open

Each becomes a Saturday question. The conveyancer's searches will cover the hazards after an offer: environmental (flood, ground), coal mining (CON29M) and local authority (planning, building control, conservation, Article 4).

- **Surface-water flood risk, all seven.** The only source is the government checker, which needs a captcha.
- **Coal mining and landslip, all seven.** Known only for the area as a whole: Sheffield's coal measures, and no recorded landslip in these suburbs (BGS, 2005 and 2008).
- **Knotweed and tree preservation orders, all seven.** The maps need JavaScript.
- **Planning history and building-control sign-off, all seven.** Sheffield's planning portal blocks fetching.
- **Energy certificates, all seven.** The register blocks fetching. This also leaves Falmouth's 94 vs 108 m² open, and whether Lees Hall's 69 m² includes the extension.
- **FENSA and Gas Safe.** You approved both, but FENSA's checker blocks fetching, and Gas Safe gives copies only to an owner who pays. Buying is ruled out.
- **Comparables:** Falmouth, Welby, Underwood and Helmton are thin (see table).
- **Market:** no figure for how far below asking houses sell, no S8 days on market, no share of listings cut, no months of stock.
- **Underwood:** a Hunters listing on the same street at the same price may be this house with a second agent.

## How each clash was settled

Full rulings are in `settled.yaml`; `facts.py merge` now marks each clash in `out/clashes.md` as settled or open.

| Clash | Winner | Why |
|---|---|---|
| Helmton tenure (Saturday doc said leasehold) | Freehold | Land Registry (2018) and both listings agree; the lease belonged to No. 25 |
| Helmton area (109 vs 73 m²) | 73 m² | 109 m² was No. 25's; 73 m² is No. 17's own 3-bed listing |
| Which Helmton listing | The 3-bed semi at offers over £265k | The viewing link opens it; the 2-bed, 1,026 sq ft listing is another house |
| Hollythorpe tenure (Land Registry leasehold and freehold) | Freehold, both titles held | The 2010 sale was filed under both titles at one price; both listings say freehold |
| Lees Hall tenure | Leasehold (medium) | The only source on No. 57 itself (Zoopla card), backed by 8 of 9 street semis |
| Welby: to let or for sale | For sale only | No advert to let anywhere; "for-rent" is just the web address |
| Falmouth area (108 vs 94 m²) | Work on 94 m²; show 108 | No third source; the method takes the smallest supportable figure |
| Falmouth Article 4 | Probably doesn't apply | The postcode tests outside the conservation area; the earlier line was conditional |
| Cawthorne flood (two agents) | Outside zones 2 and 3 | The flood-zone query, with a working control; the other agent's "not found" agrees |
| Underwood listing facts (two sources) | The Zoopla listing itself | Read directly; the other line cited a search page for another street |
| UK price trend (Nationwide, Halifax, ONS) | No winner; use the Sheffield index by type | All three say flat; the local index by type is what values the houses |
| Underwood second listing | **Open** | Can't settle without contacting agents: ask Saturday |

*Facts and arithmetic, not advice. Measure every house on Saturday: the areas carry the values.*
