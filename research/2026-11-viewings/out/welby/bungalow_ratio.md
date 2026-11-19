# 50 Welby Place: bungalow-to-house pricing

*Built 19 Nov 2026 by `scripts/bungalow_ratio.py`. Prices brought to 2026-09 with the official UK House Price Index for Sheffield, by house type (Land Registry). Floor areas from energy certificates via HouseMetric.*

## Size-adjusted model

ln(price today) = street effect + b·ln(m²) + bungalow premium. 50 Welby is left out of the fit, then priced at 60 m².

| Sample | Sales (bungalows) | b (size) | Bungalow premium, 95% range | Welby at 60 m²: central | Likely range (95%, mean) | Range for one sale (95%) |
|---|---|---|---|---|---|---|
| All sales 2016–26, 50 Welby left out | 31 (6) | 0.74 | ×1.33 (×1.09–×1.61) | £245,378 | £199,388–£301,977 | £153,766–£391,573 |
| Sales under 5 years old | 15 (1) | 0.51 | ×1.43 (×0.90–×2.29) | £290,271 | £153,522–£548,826 | £136,647–£616,605 |
| Welby Place only | 16 (3) | 0.36 | ×1.17 (×1.02–×1.33) | £250,699 | £227,154–£276,686 | £206,522–£304,327 |

## Raw £/m² ratio (no size control, in today's money)

| Street | Sales used | Bungalows: n, median £/m² | Houses: n, median £/m² | Ratio | Mean size: bungalow vs house |
|---|---|---|---|---|---|
| derbyshire lane | all | 3, £4,462 | 12, £3,116 | ×1.43 | 87 vs 82 m² |
| derbyshire lane | <5 yrs | 1, £3,245 | 6, £2,627 | ×1.24 | 87 vs 82 m² |
| welby place | all | 3, £3,570 | 13, £2,698 | ×1.32 | 66 vs 89 m² |

## 50 Welby's own sale

Bought 19 Nov 2021 for £242,000: £4,033/m². Indexed by the Sheffield detached series to 2026-09: **£279,147** (£4,652/m²). Age: 4–5 yrs.

## Every sale used, with its age

| Street | Address | Sold | Age | Price | m² | £/m² paid | £/m² today | Group | Note |
|---|---|---|---|---|---|---|---|---|---|
| welby place | [42 Welby Place](https://housemetric.co.uk/31274801/S8-9DB/42+Welby+Place) | Nov 2025 | 1–2 yrs | £292,500 | 114 | £2,566 | £2,598 | house |  |
| welby place | [21 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Feb 2025 | 1–2 yrs | £232,500 | 78 | £2,981 | £3,042 | house |  |
| welby place | [16 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Jan 2025 | 1–2 yrs | £240,000 | 78 | £3,077 | £3,128 | house |  |
| welby place | [4 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Dec 2024 | 1–2 yrs | £243,000 | 93 | £2,613 | £2,698 | house |  |
| welby place | [6 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Aug 2023 | 3–4 yrs | £230,000 | 100 | £2,300 | £2,445 | house |  |
| welby place | [14 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Mar 2023 | 3–4 yrs | £216,000 | 90 | £2,400 | £2,640 | house |  |
| welby place | [3 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Apr 2022 | 4–5 yrs | £242,000 | 83 | £2,916 | £3,389 | house |  |
| welby place | [44 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Dec 2021 | 4–5 yrs | £180,000 | 97 | £1,856 | £2,234 | house |  |
| welby place | [50 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Nov 2021 | 4–5 yrs | £242,000 | 60 | £4,033 | £4,652 | bungalow | confirmed: listing (Staves) 2-bed detached bungalow |
| welby place | [45 Welby Place](https://housemetric.co.uk/26530351/S8-9DA/45+Welby+Place) | Apr 2021 | 5–6 yrs | £235,000 | 80 | £2,938 | £3,570 | bungalow | confirmed: EPC 'Detached Bungalow' built 1983-90 |
| welby place | [47 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Dec 2020 | 5–6 yrs | £195,000 | 70 | £2,786 | £3,434 | bungalow | probable: detached in same 1980s cluster; EPC type not seen |
| welby place | [23 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Oct 2019 | 6+ yrs | £175,000 | 83 | £2,108 | £2,882 | house |  |
| welby place | [36 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Nov 2018 | 6+ yrs | £203,000 | 110 | £1,845 | £2,641 | house |  |
| welby place | [27 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Sep 2017 | 6+ yrs | £149,000 | 71 | £2,099 | £3,057 | house |  |
| welby place | [52 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Mar 2017 | 6+ yrs | £166,500 | 49 | £3,398 | £5,099 | bungalow | probable: detached 49 m² next to No. 50; EPC type not seen |
| welby place | [42 Welby Place (2017)](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Jan 2017 | 6+ yrs | £145,000 | 84 | £1,726 | £2,687 | house | area at that sale per housemetric; later EPC 114 m² |
| welby place | [38 Welby Place](https://housemetric.co.uk/house-prices/Welby-Place/S8-9D) | Nov 2016 | 6+ yrs | £145,250 | 72 | £2,017 | £3,178 | house |  |
| derbyshire lane | [210 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SE) | Feb 2026 | <1 yr | £193,000 | 89 | £2,169 | £2,154 | house |  |
| derbyshire lane | [317 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SG) | Mar 2025 | 1–2 yrs | £330,000 | 102 | £3,235 | £3,245 | bungalow | probable: detached 2-bed in the S8 8SG row of 1930s bungalows (No. 307 confirmed bungalow by agent brochure) |
| derbyshire lane | [250 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8S) | Aug 2024 | 2–3 yrs | £115,000 | 70 | £1,643 | £1,698 | house | low price; likely poor condition |
| derbyshire lane | [201 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SA) | Dec 2023 | 2–3 yrs | £295,000 | 109 | £2,706 | £2,895 | house |  |
| derbyshire lane | [273a Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8S) | Sep 2022 | 4–5 yrs | £187,500 | 85 | £2,206 | £2,359 | house |  |
| derbyshire lane | [278 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8S) | Jul 2022 | 4–5 yrs | £178,000 | 61 | £2,918 | £3,254 | house |  |
| derbyshire lane | [158 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8S) | Apr 2022 | 4–5 yrs | £195,000 | 60 | £3,250 | £3,777 | house |  |
| derbyshire lane | [163 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8S) | Sep 2021 | 5–6 yrs | £375,000 | 115 | £3,261 | £3,978 | house |  |
| derbyshire lane | [314 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SF) | Jun 2021 | 5–6 yrs | £230,000 | 95 | £2,421 | £2,978 | house |  |
| derbyshire lane | [309 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SG) | Jun 2021 | 5–6 yrs | £320,000 | 85 | £3,765 | £4,553 | bungalow | probable: as above |
| derbyshire lane | [274 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SF) | Feb 2021 | 5–6 yrs | £130,000 | 61 | £2,131 | £2,626 | house |  |
| derbyshire lane | [306 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SF) | Sep 2020 | 6+ yrs | £252,000 | 79 | £3,190 | £4,206 | house |  |
| derbyshire lane | [215a Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SB/?imperial=T) | Jun 2018 | 6+ yrs | £228,000 | 81 | £2,815 | £4,011 | house |  |
| derbyshire lane | [169 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SA) | May 2018 | 6+ yrs | £230,000 | 77 | £2,987 | £4,285 | house |  |
| derbyshire lane | [301 Derbyshire Lane](https://housemetric.co.uk/house-prices/Derbyshire-Lane/S8-8SG) | May 2017 | 6+ yrs | £220,000 | 74 | £2,973 | £4,462 | bungalow | probable: as above |
