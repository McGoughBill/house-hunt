# Comparables: 17 Helmton Drive, Woodseats, Sheffield

*From out/comps/summary.json and out/value.json (comps.py, value.py). Prices 'today' = Sep 2026, Sheffield UK HPI by type.*

```json
{
 "type": "S",
 "area_m2": 73,
 "area_m2_high": null,
 "asking": 265000,
 "asking_high": null,
 "asking_ppm2": 3630,
 "asking_ppm2_alt": null,
 "street_ceiling_ever": {
  "price": 300000,
  "note": "1A Helmton Drive (semi, leasehold), 1 Jul 2022; a £1,800 'other' sale of 1A same day. Highest since Nov 2024: £280,000, No.1 (semi, leasehold), 15 May 2025. Rows read through a page-summarising fetch tool, not raw CSV; re-check against the CSV.",
  "source": "https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HELMTON+DRIVE&town=SHEFFIELD"
 },
 "last_sale": {
  "date": "2018-12-19",
  "age": "6+ yrs",
  "price": 190000,
  "type": "S",
  "today": 264933,
  "source": "https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HELMTON+DRIVE&town=SHEFFIELD"
 },
 "first_listed": "2026-06-17",
 "days_on_market": 155,
 "first_price": 300000,
 "cuts": 2,
 "cut_pct": 11.7
}
```

value.json:
```json
{
 "area_m2": 73,
 "ring": null,
 "thin": true,
 "single": [
  {
   "address": "1 Helmton Drive, Sheffield",
   "ppm2": 3382,
   "value": 246886
  },
  {
   "address": "1 Helmton Drive, Sheffield",
   "ppm2": 3382,
   "value": 246886
  }
 ],
 "doneup": {
  "V": [
   246886,
   264933
  ],
  "W": [
   0,
   5000
  ],
  "why": "already done up per listing (modern and stylish), so W is cosmetic only; V low = 73 m² × £3,382/m², the one same-type comparable (1 Helmton Dr, 86 m², leasehold, thin); V high = the seller's 2018 £190k brought to today (£264,933)"
 },
 "margin": [
  -51553,
  -29560
 ],
 "most_to_offer": [
  213447,
  235440
 ]
}
```

## street: n=1, with area 1, thin=True, median £/m² 3382, spread [3382, 3382], top 3382

| Address | Date | Price | Today | Tenure | m² | £/m² today | Source |
|---|---|---|---|---|---|---|---|
| 1 Helmton Drive, Sheffield | 2025-05-15 | 280000 | 290876 | L | 86 | 3382 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&postcode=S8&min_date=1+November+2024&ptype%5B%5D=lrcommon%3Asemi-detached |

## postcode: n=1, with area 1, thin=True, median £/m² 3382, spread [3382, 3382], top 3382

| Address | Date | Price | Today | Tenure | m² | £/m² today | Source |
|---|---|---|---|---|---|---|---|
| 1 Helmton Drive, Sheffield | 2025-05-15 | 280000 | 290876 | L | 86 | 3382 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&postcode=S8&min_date=1+November+2024&ptype%5B%5D=lrcommon%3Asemi-detached |

numbers.yaml done-up inputs:
```yaml
V:
- 246886
- 264933
W:
- 0
- 5000
why: already done up per listing (modern and stylish), so W is cosmetic only; V low
  = 73 m² × £3,382/m², the one same-type comparable (1 Helmton Dr, 86 m², leasehold,
  thin); V high = the seller's 2018 £190k brought to today (£264,933)

```
