# Checker A: Falmouth, Welby, Lees Hall (20 Nov 2026)

Method: each figure traced to its facts.json line, source opened with WebFetch (23 fetches). Land Registry (LR) checked from raw price-paid CSVs (Falmouth by postcode S7 2DG: the street query was refused by the fetch tool; Welby by street; Lees Hall by street since 19 Nov 2023, by min_price £340k, and by paon=57). Recomputed in `out/A_calc.py` from data/sales/*.jsonl and the HPI files (index 2026-09 by type; hpi_sheffield.csv for months before 2016). No recomputed figure differs from the brief or facts.json by more than 2%.

## 34 Falmouth Road (falmouth)

| item | brief says | source says | verdict |
|---|---|---|---|
| Price, agent, postcode, time | £210,000 · Hunters, Hunters Bar · S7 2DG · 10:15 | Hunters listing: £210,000; Saturday doc matches all four | confirmed |
| Working area | 94 m² (Hunters' phone figure 1,007 sq ft) | No fact line and no source; only the settled.yaml ruling. Phone call not recorded anywhere in the pack | unsupported |
| Listing area | 108 m² | Hunters: "Total Size: 1163 SQ FT" = 108.0 m² | confirmed |
| Asking £/m² | £2,234/m² | 210,000/94 = 2,234 (sum right, area unsupported) | unsupported |
| Comparables thin | 1 terrace sale since Nov 2023, 0 with area | LR: only No. 33 (£240k, 31 Jul 2026) since Nov 2023; no area found | confirmed |
| Last sale | £119,950, Jan 2012 | LR: £119,950, 27 Jan 2012, T, L, cat A | confirmed |
| Last sale today | £227,709 | Recomputed £227,709 (terraced 55.1 -> 104.6) | confirmed |
| Street top ever | £290,000, No. 7, T, L, 13 Jun 2023 | LR: exactly so; today £323,735 (recomputed) | confirmed |
| Listed / cut | 27 Aug 2026 at £215k; cut to £210k 9 Oct | nethouseprices page failed to open; Hunters page gives no date or cut | unverifiable: blocked |
| Days listed | 84 by 19 Nov | Sum right from 27 Aug; start date unverifiable | unverifiable: blocked |
| Cut size | 1 cut, 2.3% | 5,000/215,000 = 2.33%; prices unverifiable | unverifiable: blocked |
| Tenure | leasehold (LR) | LR: L on 2012 sale; every S7 2DG sale since 1995 is L. Hunters: leasehold, 672 years left | confirmed |
| W4C comp: 33 Falmouth | £240,000, 31 Jul 2026, T, L -> £239,314 | LR row matches; recomputed £239,314 | confirmed |
| W4C comp: 7 Falmouth | £290,000, 13 Jun 2023 -> £323,735 | LR matches; recomputed £323,735 | confirmed |
| W4C comp: 15 Falmouth | £200,000, 22 Jun 2018 -> £288,552 | LR matches; recomputed £288,552 | confirmed |
| W4C comp range | £239,314–£323,735 | Recomputed same | confirmed |
| W4C exclusion | 38 Falmouth £50,000 Mar 2022 left out | LR: £50,000, 4 Mar 2022, cat A | confirmed |
| W4C area top (terraced, S7 2) | 21 Endowood Rd, £661,000, 20 Apr 2022, L -> £768,229; next 47 Endowood £625k Feb 2024 | LR S7 terraced ≥£380k: both rows match; recomputed £768,229 | confirmed |
| Lever: phone figure | 1,007 sq ft is 13% under the listing [W2 ruling] | 1,007/1,163 = 13.4% under, but the phone figure itself has no source | unsupported |
| Lever: door into living room | [listing] | Hunters: "As you enter, you are greeted by a spacious bay-windowed living room" | confirmed |
| Lever: 84 days, cut 9 Oct | [L] | Source page won't open | unverifiable: blocked |
| Lever: Abbeydale Rd 1,283 sq ft, £210k | [L] | PrimeLocation 73109342 won't open. Note: Zoopla shows an Abbeydale Rd 3-bed mid-terrace at £210k, 878 sq ft, freehold (Redbrik, 10 Nov); if the same house, 1,283 sq ft is wrong | unverifiable: blocked |
| Lever: Tavistock Rd £200k | [L] | Zoopla 72912926 opens to a results page with no Tavistock Rd listing | unsupported |
| Saturday doc: done-up value and margin | "rough estimate ... once done up is £290,000 ... margin after works still looks thin or negative" | Verdict on the house | leak |
| Saturday doc: hall | "That breaks your hall rule" | Verdict | leak |

Count: confirmed 15 · wrong 0 · unsupported 4 · overstated 0 · unverifiable: blocked 5 · leak 2

## 50 Welby Place (welby)

| item | brief says | source says | verdict |
|---|---|---|---|
| Price, agent, postcode, time | £265,000 · Staves, Woodseats · S8 9DB · 11:30 | Zoopla card: £265,000, Staves; LR postcode S8 9DB; Saturday doc matches | confirmed |
| Area | 60 m² | HouseMetric: No. 50, 60 m², £4,033/m²; OnTheMarket "645" (no unit; 645 sq ft = 59.9 m²) | confirmed |
| Asking £/m² | £4,417/m² | 265,000/60 = 4,417 | confirmed |
| Comparables thin | no detached sale since Nov 2021 | LR: last D sales Nos 50 (Nov 2021), 45 (Apr 2021), 47 (Dec 2020) | confirmed |
| Bungalow model | £245k–£251k | Fact line: £245,378 (all data), £250,699 (Welby only). Model not re-run (not asked); fact confidence low | confirmed |
| Model likely range | £227k–£277k on Welby Place alone | Fact line: £206,522–£304,327; Saturday doc: "about £205–305k" | wrong (should be about £207k–£304k) |
| Last sale | £242,000, Nov 2021 | LR: £242,000, 19 Nov 2021, D, F, cat A | confirmed |
| Last sale today | £279,147 | Recomputed £279,147 (detached 88.6 -> 102.2) | confirmed |
| Street top ever | £292,500, No. 42, T, F, 3 Nov 2025 | LR: exactly so; today £296,181 (recomputed) | confirmed |
| Listed | 2 Sep 2026 at £265,000, no cut | Zoopla: "Listed on 2nd Sep 2026", £265,000, no Reduced tag, Freehold | confirmed |
| Days listed | 78 by 19 Nov | Sum right | confirmed |
| Tenure | freehold (LR) | LR: F on 2021 sale | confirmed |
| W4C comp: 45 Welby | £235,000, 30 Apr 2021, D, F, 80 m² -> £285,577 | LR and HouseMetric (80 m²) match; recomputed £285,577 | confirmed |
| W4C comp: 47 Welby | £195,000, 11 Dec 2020, D, F, 70 m² -> £240,398 | LR and HouseMetric (70 m²) match; recomputed £240,398 | confirmed |
| W4C comp: 52 Welby | £166,500, 2 Mar 2017, D, F, 49 m² -> £249,872 | LR and HouseMetric (49 m²) match; recomputed £249,872 | confirmed |
| W4C comp range | £240,398–£285,577 | Recomputed same | confirmed |
| W4C area top (detached, S8 9) | 143 Meersbrook Park Rd £650,000, 25 Aug 2022, F -> £702,220; next 207 Shirebrook Rd £591,500 Dec 2021 | LR S8 detached ≥£550k: both match; recomputed £702,220 | confirmed |
| Lever: 78 days, no cut | [L] | Zoopla as above | confirmed |
| Lever: model £14–20k under asking | [value] | 265,000 − 250,699 = £14.3k; − 245,378 = £19.6k. But the fact line rates the model low confidence (6 bungalow sales, 1 under 4 years) and its own single-sale range (£207k–£304k) spans the asking price | overstated |
| Lever: Kennedy Road £3,889/m² | bigger detached bungalow [L] | street.co.uk: guide £315–325k, "approximately 870 square feet" (80.8 m²) = £3,897/m²; also leasehold and 1.5–4 km away, which the brief omits | confirmed |
| Lever: 2021 highest cash £/m² for a bungalow | [value] | HouseMetric: No. 50 £4,033/m², highest on the street page; next bungalow No. 52 £3,397 | confirmed |
| Lever / market: five-year fixes 6.00% | [market] | mpamag (4 Nov 2026): five-year average 6.00% in Nov 2026 (5.01% a year before). Article doesn't name Moneyfacts for this figure; predates the 5 Nov rise | confirmed |
| Rule check: hall | "you enter straight into a room. Notes say porch into hall" | OnTheMarket: "Entrance porch ... Hallway"; Saturday doc: "Side porch into a large L-shaped hall, which passes your hall rule". The brief's claim has no source | wrong |
| Saturday doc: earlier fair value | "Your earlier fair value of £215–235k" | Buyer's own price view | leak |
| Saturday doc: extension break-even | "Your extension plan loses money above about a £220k purchase" (twice) | Works as a walk-away figure | leak |
| Saturday doc: hall | "passes your hall rule" | Verdict | leak |

Count: confirmed 21 · wrong 2 · unsupported 0 · overstated 1 · unverifiable: blocked 0 · leak 3

## 57 Lees Hall Road (leeshall)

| item | brief says | source says | verdict |
|---|---|---|---|
| Price, agent, postcode, time | £290,000 · Staves, Woodseats · S8 9JJ · 12:00 | Staves page: "57 Lees Hall Road ... £290,000"; Zoopla card £290,000 Staves; Saturday doc matches | confirmed |
| Area | 69 m² (Saturday doc: "by the EPC") | facts.json epc_floor_area_m2 is null (register blocked); HouseMetric doesn't list No. 57; Staves page gives no area | unsupported |
| Asking £/m² | £4,203/m² | 290,000/69 = 4,203 (sum right, area unsupported) | unsupported |
| Value as it stands | £236k / £251k / £277k; £3,426 / £3,644 / £4,019 per m² | Recomputed from 13 W2c rows: £3,426 / £3,644 / £4,019; at 69 m² £236,391 / £251,433 / £277,306. Set includes No. 13 (£551,551, 161 m², flagged outlier) and No. 26 twice | confirmed |
| Sales with area | 13 street semi sales | LR: 16 semi sales since 19 Nov 2023; HouseMetric areas match all 13 used | confirmed |
| Last sold | none on LR since 1995 | LR query paon=57: no rows | confirmed |
| Street top ever | £551,551, No. 13, semi, F, 24 Jan 2025 | LR: exactly so (S8 9JH); next No. 12 £425k (Feb 2021); today £559,599 (recomputed) | confirmed |
| Listed | 8 Sep 2026 at £290,000, no cut | Zoopla: "Listed on 8th Sep 2026", £290,000, no Reduced tag | confirmed |
| Days listed | 72 by 19 Nov | Sum right | confirmed |
| Tenure | leasehold (wave 2 ruling; medium) | Zoopla card: Leasehold. Staves page silent; LR has no sale | confirmed |
| W4C comp: 117 LHR | £268,000, 15 Jul 2025, S, L, 69 m² -> £277,306 | LR and HouseMetric match; recomputed £277,306 | confirmed |
| W4C comp: 105 LHR | £255,000, 20 Jan 2025, 71 m² -> £258,721 | LR and HouseMetric match; recomputed £258,721 | confirmed |
| W4C comp: 26 LHR | £275,000, 7 May 2025, 84 m² -> £285,682 | LR and HouseMetric match; recomputed £285,682 | confirmed |
| W4C comp: 58 LHR | £265,000, 9 Feb 2024, 71 m² -> £287,015 | LR and HouseMetric match; recomputed £287,015 | confirmed |
| W4C comp range | £258,721–£287,015 | Recomputed same | confirmed |
| W4C area top (semi, S8 9) | 220 Shirebrook Rd £605,000, 27 Aug 2025, F -> £618,036; next 77 Brook Rd £590,000 Feb 2025 | LR S8 semi ≥£450k: both match (77 Brook Rd is leasehold); recomputed £618,036 | confirmed |
| Lever: £4,203/m², 15% over median | [value] | 4,203/3,644 = +15.3%, but it rests on the unsourced 69 m², which may leave out the rear extension (Staves: "extended to the rear") | overstated |
| Lever: two leasehold semis ~£250k; Yopa unsold since 20 Mar despite a cut | [L] | Zoopla: Yopa £250k OIRO, leasehold, listed 20 Mar 2026, "Reduced"; Blundells £250k OIRO, leasehold, 3-bed semi, "Just added". Yopa's house type not shown | confirmed |
| Lever: 72 days listed | [L] | As above | confirmed |
| Lever: No. 26 £275k May 2025, £5k below Jan 2024 | [L] | LR: £275,000 7 May 2025; £280,000 26 Jan 2024. Rightmove agrees | confirmed |
| Saturday doc: value band | "As-is value about £245–260k ... expect the agent to argue up to the upper quartile" | Reads as the buyer's offer band | leak |

Count: confirmed 17 · wrong 0 · unsupported 2 · overstated 1 · unverifiable: blocked 0 · leak 1

## Market lines used in any brief

| item | brief says | source says | verdict |
|---|---|---|---|
| Bank rate (Helmton) | up to 4% on 5 Nov | BoE Nov 2026 summary: raised 0.25 pp to 4%, 8–1, summary dated 5 Nov | confirmed |
| RICS price balance (Helmton) | −36 | RICS Oct 2026 survey: house prices −36 | confirmed |
| Five-year fixes (Welby) | 6.00% | mpamag 4 Nov 2026: 6.00% | confirmed |

Count: confirmed 3

## Not in the pack / notes
- No source for Hunters' 1,007 sq ft phone figure, nor any EPC floor area for Falmouth, Welby or Lees Hall.
- Brief vs Saturday doc (step e): times, addresses, postcodes, agents and prices agree for all three. The brief gives no phone numbers. Clashes: Welby's model range and hall (above).
- Brief header says "no verdicts or offer figures"; the briefs themselves hold no budget, deposit, mortgage or offer figure for these three houses. The leaks above sit in the Saturday doc's house sections.
