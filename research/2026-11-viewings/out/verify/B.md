# Checker B: 6 Cawthorne Grove, 38 Underwood Road, 17 Helmton Drive, 51 Hollythorpe Road

Checked 20 Nov 2026. Recompute script: `out/B_calc.py` (raw rows in data/sales, HPI by type to 2026-09; quartiles use Python `statistics.quantiles(method="inclusive")`). No recomputed figure differs from the brief or facts.json by more than 2%.
LR = raw Land Registry price-paid CSV, opened in this check. Three street-wide LR queries (Cawthorne, Underwood, Hollythorpe) were refused by the fetch tool's permission check; the same rows were opened instead through postcode, date-window or min_price queries, listed per row. 41 fetches used.

## 1. 6 Cawthorne Grove, S8 0ND

| item | brief says | source says | verdict |
|---|---|---|---|
| Area | 80 m² | Rightmove 91503453: 863 sq ft (80 m²); HouseMetric lists No. 6 at 80 m² | confirmed |
| Asking £/m² | £3,750 (£4,062 at £325k) | 300,000/80 = 3,750; 325,000/80 = 4,062.5 | confirmed |
| Value as it stands | £270k / £292k / £306k; £3,377 / £3,644 / £3,821 per m², 8 semis with area | Recomputed: £3,377 / £3,644 / £3,821 → £270,191 / £291,515 / £305,669. All 8 areas match HouseMetric; all 8 LR rows match (S8 0ND and S8 0NB date-window queries). Note: the set includes No. 25 at £176,000 leasehold (£2,326/m², a likely outlier) and No. 45's 2025 sale with the area of its Nov 2023 sale | confirmed |
| Last sale | £253,000, Apr 2023 | LR: 6, S8 0ND, 2023-04-03, £253,000, S, F, cat A | confirmed |
| Last sale today | £277,475 | 253,000 × 104.3/95.1 = £277,475 | confirmed |
| Street top ever | £435,000, 27C, detached, 14 May 2025 | LR (min_price £320k): 27C, S8 0NB, 2025-05-14, £435,000, D, F, A | confirmed |
| Listed | 31 Jul 2026 at £300,000 | Rightmove: added 31/07/2026, guide £300,000 (text £300–325k), no reduction | confirmed |
| Days listed | 111 by 19 Nov, no cut | 31 Jul to 19 Nov = 111 days | confirmed |
| Tenure | freehold (LR) | LR 2023 sale: F; Rightmove: freehold (Saxton Mee's own page says "Unknown") | confirmed |
| Header: guide, agent, postcode | £300–325k, Saxton Mee Banner Cross, S8 0ND | Rightmove and Saxton Mee page; LR postcode S8 0ND | confirmed |
| Lever: 111 days, no cut | 111 days at £300k, no cut [L] | as above | confirmed |
| Lever: guide vs median | "Guide bottom £3,750/m² beats street median £3,644/m²" | Figures right. "Beats" reads as a bargain, but the guide is 3% **above** the median, not below it | overstated |
| Lever: own sale | £253k Apr 2023, £277k today; guide 8–17% more | 300/277.5 = +8.1%; 325/277.5 = +17.1% | confirmed |
| Lever: rivals | Periwood Dr guide £285–300k, Camping Lane £300k, both chain free | Zoopla 73170560: Periwood, Haus, guide £285k (text £285–300k), freehold, chain free. PrimeLocation 73376122: Camping Lane £300k, chain free (no agent named) | confirmed |
| W4C comp No. 26 | £270,000, 20 Jun 2025 → £285,030, 78 m², F | LR S8 0ND: 26, 2025-06-20, £270,000, S, F, A; calc £285,030; HouseMetric 78 m² | confirmed |
| W4C comp No. 22 | £248,000, 3 Jun 2025 → £261,806, 78 m², F | LR: 22, 2025-06-03, £248,000, S, F, A; calc £261,806; HouseMetric 78 m² | confirmed |
| W4C comp No. 8 | £320,000, 19 Dec 2025 → £322,162 | LR: 8, 2025-12-19, £320,000, S, F, A; calc £322,162 | confirmed |
| W4C comp No. 12 | £315,000, 22 Oct 2025 → £320,219 | LR: 12, 2025-10-22, £315,000, S, F, A; calc £320,219 | confirmed |
| W4C range | £261,806–£322,162 (n = 4) | recomputed same | confirmed |
| W4C street top | 27C £435,000 → £447,254 | detached index: 435,000 × 102.2/99.4 → £447,254 | confirmed |
| W4C area top (S8 0, semi) | 261 Abbey Lane, £710,000, 7 Aug 2025 → £725,299 | LR S8 semi ≥£450k: 261 Abbey Lane S8 0BT, 2025-08-07, £710,000, S, F, A; top in S8 0; calc £725,299 | confirmed |
| Sat doc: time, address, agent, price, phone | 12:45; S8 0ND; Saxton Mee Banner Cross; guide £300–325k; 0114 268 3241 | matches brief; phone on Saxton Mee page; branch address 949–951 Ecclesall Rd S11 8TN on Rightmove | confirmed |
| Sat doc: contact name | Abi Lenihan | no source in pack; Saxton Mee page names no staff | unsupported |
| Sat doc: No. 12 "same agent and same guide" | sold £315k | Rightmove PDF: 12 Cawthorne Grove, guide £300–325k, freehold, band B; **no agent named** | unsupported |
| Sat doc: verdict | "Neighbours back the guide" | a price judgement, not a fact | leak |

Counts: confirmed 20, overstated 1, unsupported 2, leak 1, wrong 0, unverifiable 0.

## 2. 38 Underwood Road, S8 8TH

| item | brief says | source says | verdict |
|---|---|---|---|
| Area | 85 m² | Zoopla 74619438: 915 sq ft (85.0 m²) | confirmed |
| Asking £/m² | £2,588 | 220,000/85 = 2,588 | confirmed |
| Comparables thin | 1 terrace sale since Nov 2023, 0 with area | LR S8 8TH, 19 Nov 2023 on: terraces No. 56 (cat A) and No. 18 (£87,500, cat B); the rest are semis. No areas found | confirmed |
| Last sale | £140,000, Dec 2020 | LR: 38, 2020-12-07, £140,000, T, L, cat A | confirmed |
| Last sale today | £180,345 | 140,000 × 104.6/81.2 = £180,345 | confirmed |
| Street top ever | £246,000, No. 36, semi, F, 16 Jun 2026 | LR S8 8TH ≥£200k: 36, 2026-06-16, £246,000, S, F, A; top terrace No. 56 £200k | confirmed |
| Listed | 28 Oct 2026 at £220,000, no cut | Zoopla: added 28/10/2026, OIRO £220,000, no price history | confirmed |
| Days listed | 22 by 19 Nov | 28 Oct to 19 Nov = 22 | confirmed |
| Tenure | leasehold (LR) | LR 2020: L. Zoopla tenure field "Ask agent"; description says leasehold | confirmed |
| Header: price, agent, postcode | OIRO £220k, Whitehornes, S8 8TH | Zoopla, Rightmove (Whitehornes Banner Cross); LR postcode | confirmed |
| Lever: over No. 56 | £13k over street's top terrace, No. 56, F, £207k today | LR: 56, 2025-07-17, £200,000, T, F, A; today £206,719; 220,000 − 206,719 = £13,281 | confirmed |
| Lever: over own sale | £40k over last sale in today's money | 220,000 − 180,345 = £39,655 | confirmed |
| Lever: leasehold | [S3] | LR L | confirmed |
| Lever: listing | needs renovation; EPC D | Zoopla: "In need of some renovations", EPC D | confirmed |
| Lever: rivals | three nearby 3-bed terraces also ask £220k | Woodseats Road link opens a search page: the Woodseats Road £220k terrace is Redbrik, guide £220–230k, 1,216 sq ft, **freehold** (facts: Whitehorn, 1,393 sq ft, leasehold). Holmhirst Drive link: **0 results**. Hackthorn Road: SK, guide £220–240k, end terrace, freehold. Other £220k terraces do appear nearby (Haughton Rd), but not the three cited | overstated |
| W4C comp No. 56 | £200,000, 17 Jul 2025 → £206,719, F | LR as above; calc £206,719 | confirmed |
| W4C comp No. 30 | £142,000, 17 Sep 2021 → £173,925, F | LR: 30, 2021-09-17, £142,000, T, F, A; calc £173,925 | confirmed |
| W4C comp No. 48 | £187,500, 27 Nov 2020 → £243,634, L | LR: 48, 2020-11-27, £187,500, T, L, A; calc £243,634. Note: No. 38 sold for £47,500 less 10 days later | confirmed |
| W4C range | £173,925–£243,634 (n = 3) | recomputed same | confirmed |
| W4C street top | No. 36 £246,000 → £246,236 | semi index; calc £246,236 | confirmed |
| W4C area top (S8 8, terraced) | 79 Norton Park View, £450,000, 13 Dec 2024 → £464,659 | LR S8 terraced ≥£270k: 79 Norton Park View S8 8GU, 2024-12-13, £450,000, **T, L**; top in S8 8; calc £464,659. But the same sale also appears in the semi query as **S, F**: type doubtful, as facts.json warns | confirmed |
| Sat doc: time, address, agent, price, phone | 13:30; S8 8TH; Whitehornes; OIRO £220k; 0114 268 8533 | matches brief; phone on Whitehornes site | confirmed |
| Sat doc: rivals | Woodseats Road (Whitehornes, 1,393 sq ft, leasehold); Holmhirst Drive (Whitehornes) | Woodseats Road £220k is Redbrik, 1,216 sq ft, freehold; Holmhirst Drive page has no listing | wrong |
| Brief Ask / Sat doc: Hunters listing | Hunters' Underwood Rd listing, OIRO £220k, added 30 Oct | Rightmove Norton Lees terraced page now shows only Whitehornes' Underwood Rd listing (added 28/10/2026); no Hunters listing | unsupported |

Counts: confirmed 21, overstated 1, wrong 1, unsupported 1, leak 0, unverifiable 0.

## 3. 17 Helmton Drive, S8 8QN

| item | brief says | source says | verdict |
|---|---|---|---|
| Area | 73 m² | Rightmove 89812113: 786 sq ft / 73 m²; HouseMetric lists No. 17 at 73 m² | confirmed |
| Asking £/m² | £3,630 | 265,000/73 = 3,630 | confirmed |
| Comparables thin | 1 semi sale since Nov 2023, 1 with area | LR street CSV: only semi since Nov 2023 is No. 1 (2025); HouseMetric 86 m² | confirmed |
| One-sale value | No. 1 at £3,382/m² → £246,886 at 73 m² | recomputed £3,382/m² → £246,907 (rounding) | confirmed |
| Last sale | £190,000, Dec 2018 | LR: 17, 2018-12-19, £190,000, S, F, cat A | confirmed |
| Last sale today | £264,933 | 190,000 × 104.3/74.8 = £264,933 | confirmed |
| Street top ever | £300,000, 1A, semi, L, 1 Jul 2022 | LR: 1A, 2022-07-01, £300,000, S, L, A (plus a £1,800 cat-B "other" row same day); highest in file | confirmed |
| Listed | 17 Jun 2026 at £300,000 | PrimeLocation 73476420: added 17/06/2026, OIRO £300,000; Zoopla card: listed 17 Jun 2026 | confirmed |
| Days and cuts | 155 days, 2 cuts, 11.7% in all | 17 Jun–19 Nov = 155; Rightmove £270k reduced 14/10/2026; now offers over £265k (Whitehornes, Zoopla "Reduced"); 35/300 = 11.7% | confirmed |
| Done-up value and buy-test margin | £247k–£265k; margin −£51,553 to −£29,560 | Ends of range = one comparable and the seller's own price indexed (both confirmed). Margin needs cost and target inputs not in the pack: cannot be checked | unsupported |
| Same | margin at asking (also Sat doc "Margin −£52k to −£30k") | a buy-test result is a verdict on price | leak |
| Tenure | freehold (ruled in wave 2) | LR 2018: F; Rightmove and Whitehornes: freehold | confirmed |
| Header: price, agent, postcode | offers over £265k, Whitehornes, S8 8QN | Whitehornes page; LR postcode S8 8QN | confirmed |
| Lever: days, cuts | 155 days, cut twice, 11.7% off £300k | as above | confirmed |
| Lever: one comparable | No. 1 (86 m²), £3,382/m²: £247k | confirmed figures. Omits that No. 1 is leasehold and 13 m² larger | confirmed |
| Lever: market | RICS price balance −36; Bank Rate up to 4% on 5 Nov | RICS Oct 2026: prices −36. BoE minutes: +0.25pp to 4%, meeting ended 4 Nov, published 5 Nov, vote 8–1. Both UK-wide, not Sheffield | confirmed |
| W4C comp No. 1 | £280,000, 15 May 2025 → £290,876, 86 m², L | LR: 1, 2025-05-15, £280,000, S, L, A; calc £290,876 | confirmed |
| W4C comp No. 3 | £195,000, 10 Feb 2023 → £208,814, 79 m², L | LR: 3, 2023-02-10, £195,000, S, L, A; calc £208,814; HouseMetric 79 m² | confirmed |
| W4C comp 1A | £300,000, 1 Jul 2022 → £334,295, L | LR as above; calc £334,295 | confirmed |
| W4C range | £208,814–£334,295 (n = 3) | recomputed same | confirmed |
| W4C street top | 1A £300,000 → £334,295; next No. 38 detached £290,000 (2020) | LR: 38, 2020-07-10, £290,000, D, L | confirmed |
| W4C area top (S8 8, semi) | 200 Norton Lane, £560,000, 21 Aug 2023 → £593,577 | LR S8 semi ≥£450k: 200 Norton Lane S8 8HB, 2023-08-21, £560,000, S, F, A; top in S8 8; calc £593,577 | confirmed |
| Sat doc: time, address, agent, price, phone | 14:00; S8 8QN; Whitehornes; offers over £265k; 0114 268 8533 | matches brief; phone on Whitehornes page | confirmed |
| Sat doc: Whitehornes address (agents table) | Unit 2 Acorn Business Park, Woodseats Close, S8 0TB | Whitehornes listing and Rightmove give the sales branch as 952 Ecclesall Road, S11 8TR | unsupported |
| Sat doc: verdict | "the asking price builds in nothing for any work they've done since" | a price judgement | leak |

Counts: confirmed 20, unsupported 2, leak 2, overstated 0, wrong 0, unverifiable 0.

## 4. 51 Hollythorpe Road, S8 9NF

| item | brief says | source says | verdict |
|---|---|---|---|
| Area | 68 m² | Zoopla card (70241795 resolves to a search page): Hollythorpe Rd, Whitehorn, 731 sq ft = 67.9 m² | confirmed |
| Asking £/m² | £4,118 | 280,000/68 = 4,118 (4,124 at 67.9 m²) | confirmed |
| Value as it stands | £249k / £276k / £286k; £3,664 / £4,061 / £4,199, 6 semis with area | recomputed £3,664 / £4,061 / £4,199 → £249,180 / £276,139 / £285,502. All 6 areas match HouseMetric; LR rows match | confirmed |
| Last sale | £136,500, Oct 2010 | LR S8 9NF: 51, 2010-10-01, £136,500, S, once L and once F, cat A | confirmed |
| Last sale today | £249,771 | 136,500 × 104.3/57.0 = £249,771 | confirmed |
| Street top ever | £330,000, No. 80, semi, F, 14 Mar 2025 | LR street ≥£300k: 80 (£330k, S, F), 49 (£315k), 15 (£310k) | confirmed |
| Listed | 23 Feb 2026 at £280,000, no cut | Zoopla card: listed 23 Feb 2026, OIRO £280k, no "Reduced" flag | confirmed |
| Days listed | 269 by 19 Nov | 23 Feb to 19 Nov = 269 | confirmed |
| Done-up value and buy-test margin | £276k–£286k; −£40,217 to −£26,021 | value range = the median and upper quartile (confirmed). Margin needs cost inputs not in the pack | unsupported |
| Same | margin at asking (also Sat doc "Margin −£40k to −£26k") | a buy-test result is a verdict on price | leak |
| Tenure | freehold, owner appears to hold both titles | LR two rows (L and F) same day and price; Whitehornes page: freehold. Title not seen | confirmed |
| Header: price, agent, postcode | OIRO £280k, Whitehornes, S8 9NF | Whitehornes page; LR postcode | confirmed |
| Lever: 269 days | unsold, never cut | as above | confirmed |
| Lever: margin | −£40k to −£26k at £280k | as above | unsupported |
| Lever: low comps | No. 30, 69 m² semi, £241k Mar 2025; No. 33 £235k | LR: 30, 2025-03-27, £241,000, S, L; 33, 2025-03-10, £235,000, S, L; HouseMetric 69 m². True, but picks the two cheapest: the same street's 2025 semis also sold at £295k (13), £315k (49, next door), £330k (80) | overstated |
| Lever: Hollythorpe Crescent | bigger semi (~75 m²) went STC at £240k | Zoopla 73286215: Redbrik, guide £240–250k, 807 sq ft (75 m²), semi, freehold, shown as "Just added"; **no STC** shown | overstated |
| W4C comp No. 30 | £241,000, 27 Mar 2025 → £243,098, 69 m², L | LR as above; calc £243,098 | confirmed |
| W4C comp No. 42 | £280,000, 1 Jul 2024 → £296,487, 70 m², F | LR: 42, S8 9NF, 2024-07-01, £280,000, S, F, A; calc; HouseMetric 70 m² | confirmed |
| W4C comp No. 14 | £285,000, 20 Sep 2024 → £294,312, 72 m², F | LR: 14, S8 9NE, 2024-09-20, £285,000, S, F, A; calc; HouseMetric 72 m² | confirmed |
| W4C comp No. 25 | £252,750, 1 Mar 2024 → £274,317, 68 m², L | LR: 25, 2024-03-01, £252,750, S, L, A; calc; HouseMetric 68 m² | confirmed |
| W4C range | £243,098–£296,487 (n = 4) | recomputed same | confirmed |
| W4C street top | No. 80 £330,000 → £332,872 | calc £332,872 | confirmed |
| W4C area top (S8 9, semi) | 220 Shirebrook Road, £605,000, 27 Aug 2025 → £618,036 | LR S8 semi ≥£450k: 220 Shirebrook Rd S8 9RG, 2025-08-27, £605,000, S, F, A; top in S8 9; calc £618,036 | confirmed |
| Sat doc: time, address, agent, price, phone | 14:45 (unconfirmed); S8 9NF; Whitehornes; OIRO £280k; 0114 268 8533 | matches brief ("No reply yet" vs "not yet confirmed"); phone on Whitehornes page | confirmed |
| Sat doc: neighbours today | No. 49 ≈ £333k, No. 80 ≈ £333k, No. 13 ≈ £300k | LR prices and dates match; calc £332,535 / £332,872 / £299,888 | confirmed |
| Sat doc: Hunters rival | Hollythorpe Rd semi £280k, Sold STC | Rightmove 89629326: S8 9NF, £280k, Hunters, added 12/06/2026, "SOLD STC" | confirmed |
| Sat doc: Hollythorpe Crescent | £240k (807 sq ft) went STC | no STC on the source page | overstated |
| Sat doc: verdict | "Nine months unsold is the strongest sign of a seller who needs to move" | a judgement, not a fact | leak |

Counts: confirmed 20, overstated 3, unsupported 2, leak 2, wrong 0, unverifiable 0.

## Totals

| house | confirmed | wrong | unsupported | overstated | unverifiable: blocked | leak |
|---|---|---|---|---|---|---|
| Cawthorne | 20 | 0 | 2 | 1 | 0 | 1 |
| Underwood | 21 | 1 | 1 | 1 | 0 | 0 |
| Helmton | 20 | 0 | 2 | 0 | 0 | 2 |
| Hollythorpe | 20 | 0 | 2 | 3 | 0 | 2 |
| **All** | **81** | **1** | **7** | **5** | **0** | **5** |

No figure for budget, deposit, mortgage, price ceiling, opening offer or walk-away was found in these four briefs or their Saturday-doc sections.
