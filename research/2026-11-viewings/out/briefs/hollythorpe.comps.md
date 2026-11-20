# Comparables: 51 Hollythorpe Road, Norton Lees, Sheffield

*From out/comps/summary.json and out/value.json (comps.py, value.py). Prices 'today' = Sep 2026, Sheffield UK HPI by type.*

```json
{
 "type": "S",
 "area_m2": 68,
 "area_m2_high": null,
 "asking": 280000,
 "asking_high": null,
 "asking_ppm2": 4118,
 "asking_ppm2_alt": null,
 "street_ceiling_ever": {
  "price": 330000,
  "note": "80 Hollythorpe Road (S8 9NF), semi, freehold, 14 Mar 2025. Medium: full-street extract may have been cut off at No. 85.",
  "source": "https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD"
 },
 "last_sale": {
  "date": "2010-10-01",
  "age": "6+ yrs",
  "price": 136500,
  "type": "S",
  "today": 249771,
  "source": "https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD"
 },
 "first_listed": "2026-02-23",
 "days_on_market": 269,
 "first_price": 280000,
 "cuts": 0,
 "cut_pct": 0.0
}
```

value.json:
```json
{
 "area_m2": 68,
 "ring": "street",
 "n": 6,
 "ppm2": [
  3664,
  4061,
  4199
 ],
 "value": [
  249152,
  276148,
  285532
 ],
 "doneup": {
  "V": [
   276148,
   285532
  ],
  "W": [
   0,
   5000
  ],
  "why": "already done up per listing (immaculate, no expense spared), so W is cosmetic only and V sits in the top half of the street range: 68 m² × median £4,061 to upper quartile £4,199/m², 6 semis with floor areas"
 },
 "margin": [
  -40217,
  -26021
 ],
 "most_to_offer": [
  239783,
  253979
 ]
}
```

## street: n=10, with area 6, thin=False, median £/m² 4061, spread [3523, 4250], top 4250

| Address | Date | Price | Today | Tenure | m² | £/m² today | Source |
|---|---|---|---|---|---|---|---|
| 13 Hollythorpe Road, Sheffield | 2025-10-28 | 295000 | 299888 | F | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=1+November+2024 |
| 49 Hollythorpe Road, Sheffield | 2025-06-30 | 315000 | 332535 | L | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=1+November+2024 |
| 30 Hollythorpe Road, Sheffield | 2025-03-27 | 241000 | 243098 | L | 69 | 3523 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=1+November+2024 |
| 80 Hollythorpe Road, Sheffield | 2025-03-14 | 330000 | 332872 | F | 94 | 3541 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=1+November+2024 |
| 33 Hollythorpe Road, Sheffield | 2025-03-10 | 235000 | 237045 | L | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=1+November+2024 |
| 72 Hollythorpe Road, Sheffield | 2024-10-04 | 287500 | 296307 | L | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 14 Hollythorpe Road, Sheffield | 2024-09-20 | 285000 | 294312 | F | 72 | 4088 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 42 Hollythorpe Road, Sheffield | 2024-07-01 | 280000 | 296487 | F | 70 | 4236 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 25 Hollythorpe Road, Sheffield | 2024-03-01 | 252750 | 274317 | L | 68 | 4034 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 15 Hollythorpe Road, Sheffield | 2024-02-09 | 310000 | 335753 | L | 79 | 4250 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |

## postcode: n=4, with area 2, thin=True, median £/m² 3888, spread [3541, 4236], top 4236

| Address | Date | Price | Today | Tenure | m² | £/m² today | Source |
|---|---|---|---|---|---|---|---|
| 49 Hollythorpe Road, Sheffield | 2025-06-30 | 315000 | 332535 | L | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=1+November+2024 |
| 80 Hollythorpe Road, Sheffield | 2025-03-14 | 330000 | 332872 | F | 94 | 3541 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=1+November+2024 |
| 72 Hollythorpe Road, Sheffield | 2024-10-04 | 287500 | 296307 | L | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 42 Hollythorpe Road, Sheffield | 2024-07-01 | 280000 | 296487 | F | 70 | 4236 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |

numbers.yaml done-up inputs:
```yaml
V:
- 276148
- 285532
W:
- 0
- 5000
why: 'already done up per listing (immaculate, no expense spared), so W is cosmetic
  only and V sits in the top half of the street range: 68 m² × median £4,061 to upper
  quartile £4,199/m², 6 semis with floor areas'

```
