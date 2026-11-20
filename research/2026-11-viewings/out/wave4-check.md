# Wave 4: checking (20 Nov 2026)

*One comparables agent (W4C), then two fresh checkers (A: Falmouth, Welby, Lees Hall and market lines; B: Cawthorne, Underwood, Helmton, Hollythorpe). The checkers saw only the two docs, facts.json, settled.yaml and raw data. Their tables: repo `research/2026-11-viewings/out/verify/A.md`, `B.md`; their own sums: `A_calc.py`, `B_calc.py`. Fixes are marked [W4] in both docs. `brief_check.py`: 0 unmatched figures in all seven briefs.*

**Pushed** to `McGoughBill/house-hunt`, branch `research-nov-viewings`, on 20 Nov.

## Verdicts per house

| House | Confirmed | Wrong | Unsupported | Overstated | Blocked | Leak |
|---|---|---|---|---|---|---|
| Falmouth | 15 | 0 | 4 | 0 | 5 | 2 |
| Welby | 21 | 2 | 0 | 1 | 0 | 3 |
| Lees Hall | 17 | 0 | 2 | 1 | 0 | 1 |
| Cawthorne | 20 | 0 | 2 | 1 | 0 | 1 |
| Underwood | 21 | 1 | 1 | 1 | 0 | 0 |
| Helmton | 20 | 0 | 2 | 0 | 0 | 2 |
| Hollythorpe | 20 | 0 | 2 | 3 | 0 | 2 |
| Market lines | 3 | 0 | 0 | 0 | 0 | 0 |
| **All** | **137** | **3** | **13** | **7** | **5** | **11** |

Both checkers recomputed every £/m² figure, range, last sale in today's money and top price from raw rows: **none is more than 2% off.** Every W4C comparable and top price matched its Land Registry record. "Leak" = a verdict or price view; all leaks sat in the Saturday doc, none in the briefs.

## Comparables and top prices

All from Land Registry, same street (step 1 was enough for every house). ≈ = today's money, Sheffield index by type to Sep 2026.

| House | Comparables (sale price → ≈ today) | Range today | Street top | Area top, same type (sector) |
|---|---|---|---|---|
| Falmouth (T) | No. 33 £240k Jul 2026 → £239k; No. 7 £290k Jun 2023 → £324k; No. 15 £200k Jun 2018 → £289k. No areas | £239k–£324k | £290k, No. 7, 2023 | S7 2: £661k, 21 Endowood Rd, Apr 2022 |
| Welby (D) | No. 45 £235k Apr 2021 → £286k (80 m²); No. 47 £195k Dec 2020 → £240k (70 m²); No. 52 £166.5k Mar 2017 → £250k (49 m²) | £240k–£286k | £292.5k, No. 42 (terrace), 2025 | S8 9: £650k, 143 Meersbrook Park Rd, Aug 2022 |
| Lees Hall (S) | No. 117 £268k Jul 2025 → £277k (69 m²); No. 26 £275k May 2025 → £286k (84 m²); No. 105 £255k Jan 2025 → £259k (71 m²); No. 58 £265k Feb 2024 → £287k (71 m²) | £259k–£287k | £551,551, No. 13, 2025 (outlier, 161 m²) | S8 9: £605k, 220 Shirebrook Rd, Aug 2025 |
| Cawthorne (S) | No. 8 £320k Dec 2025 → £322k; No. 12 £315k Oct 2025 → £320k; No. 26 £270k Jun 2025 → £285k (78 m²); No. 22 £248k Jun 2025 → £262k (78 m²) | £262k–£322k | £435k, No. 27C (detached), 2025 | S8 0: £710k, 261 Abbey Lane, Aug 2025 |
| Underwood (T) | No. 56 £200k Jul 2025 → £207k; No. 30 £142k Sep 2021 → £174k; No. 48 £187.5k Nov 2020 → £244k. No areas | £174k–£244k | £246k, No. 36 (semi), 2026 | S8 8: £450k, 79 Norton Park View, Dec 2024 (type doubtful) |
| Helmton (S) | No. 1 £280k May 2025 → £291k (86 m²); No. 3 £195k Feb 2023 → £209k (79 m²); No. 1A £300k Jul 2022 → £334k | £209k–£334k | £300k, No. 1A, 2022 | S8 8: £560k, 200 Norton Lane, Aug 2023 |
| Hollythorpe (S) | No. 30 £241k Mar 2025 → £243k (69 m²); No. 14 £285k Sep 2024 → £294k (72 m²); No. 42 £280k Jul 2024 → £296k (70 m²); No. 25 £252,750 Mar 2024 → £274k (68 m²) | £243k–£296k | £330k, No. 80, 2025 | S8 9: £605k, 220 Shirebrook Rd, Aug 2025 |

Area tops: Land Registry's sector query returns nothing, so these come from district-wide queries by type and price floor, kept to the sector. Medium confidence; "highest found", not proven highest ever.

## Changes made

**Briefs doc:** a Local prices block in each of the seven briefs, plus:
- Falmouth: 94 m² marked as Hunters' phone figure, unconfirmed; listing date and cut marked unconfirmed (source blocked); Abbeydale Rd rival marked unconfirmed, with a possible size clash (878 vs 1,283 sq ft); Tavistock Rd rival cut (listing not found).
- Welby: one-sale range corrected from £227k–£277k to **£207k–£304k**; model lever now says low confidence and that its range spans the asking; hall rule corrected (listing shows porch into hallway).
- Lees Hall: 69 m² marked unconfirmed; the "15% over median" lever now says it holds only if 69 m² is the whole house.
- Cawthorne: "guide beats median" corrected to "guide is 3% above the median".
- Underwood: rival terraces corrected (Woodseats Rd is Redbrik, £220–230k guide, 1,216 sq ft, freehold; Hackthorn Rd £220–240k guide; Holmhirst Dr not found); Hunters second-listing question updated (gone by 20 Nov).
- Helmton, Hollythorpe: buy-test margins cut (unsupported, and verdicts).
- Hollythorpe: low-comps lever now shows the high sales too (£295k–£330k); Hollythorpe Crescent "went STC" corrected to "£240–250k guide, no STC shown".

**Saturday doc:** a W4 note at the top, plus:
- Cut, as leaks: Falmouth's done-up estimate and margin; Welby's earlier fair value and the £220k break-even (twice); Lees Hall's £245–260k as-is band and "expect the agent to argue"; Helmton's judgement on the seller's works and margin; Hollythorpe's "strongest sign" line and margin.
- Reworded: Falmouth and Welby hall-rule verdicts; Cawthorne "neighbours back the guide" (and "same agent", unsupported).
- Same factual fixes as the briefs for Falmouth (phone figure, rivals, listing dates), Welby (range, hall), Lees Hall (69 m²), Underwood (rivals, Hunters listing), Hollythorpe (Crescent).
- Agents table: Abi Lenihan marked as from your emails; Whitehornes' address marked as per your notes, with the listings' 952 Ecclesall Road, S11 8TR alongside.

## Treat with care tomorrow

- **Measure Falmouth and Lees Hall.** Neither 94 m² nor 69 m² has a written source. Ask for the energy certificates.
- **Falmouth:** listing date, the £5k cut and the Abbeydale rival are unconfirmed. Comparables have no floor areas.
- **Welby:** all three comparables are 5+ years old; the model rests on 6 bungalow sales and its one-sale range spans the asking.
- **Underwood:** comparables have no floor areas and two are 5 years old. Whether Hunters also had it is open.
- **Helmton:** No. 1A's £300k (the street top) came with a same-day £1,800 non-market transfer; treat it as doubtful. All three comparables are leasehold; No. 17 is freehold.
- **Hollythorpe:** Whitehornes still hasn't confirmed 14:45. Comparables mix freehold and leasehold.
- **Not flagged, left as is:** "passes your hall rule" lines for Cawthorne and Helmton in the Saturday doc.
