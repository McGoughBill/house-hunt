# Comparables: 6 Cawthorne Grove, Millhouses, Sheffield

*From out/comps/summary.json and out/value.json (comps.py, value.py). Prices 'today' = Sep 2026, Sheffield UK HPI by type.*

```json
{
 "type": "S",
 "area_m2": 80,
 "area_m2_high": null,
 "asking": 300000,
 "asking_high": 325000,
 "asking_ppm2": 3750,
 "asking_ppm2_alt": 4062,
 "street_ceiling_ever": {
  "price": 435000,
  "note": "27C Cawthorne Grove (S8 0NB), detached, 14 May 2025. Highest semi: 27B, £350,000, 29 Apr 2025. Highest on S8 0ND: No. 8, semi, £320,000, 19 Dec 2025; No. 12, £315,000, 22 Oct 2025. Rows read from the Land Registry CSV through a summarising fetch tool; spot-check before relying on them.",
  "source": "https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD"
 },
 "last_sale": {
  "date": "2023-04-03",
  "age": "3–4 yrs",
  "price": 253000,
  "type": "S",
  "today": 277475,
  "source": "https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD"
 },
 "first_listed": "2026-07-31",
 "days_on_market": 111,
 "first_price": 300000,
 "cuts": 0,
 "cut_pct": 0.0
}
```

value.json:
```json
{
 "area_m2": 80,
 "ring": "street",
 "n": 8,
 "ppm2": [
  3377,
  3644,
  3821
 ],
 "value": [
  270160,
  291520,
  305680
 ]
}
```

## street: n=11, with area 8, thin=False, median £/m² 3644, spread [2326, 3942], top 3942

| Address | Date | Price | Today | Tenure | m² | £/m² today | Source |
|---|---|---|---|---|---|---|---|
| 8 Cawthorne Grove, Sheffield | 2025-12-19 | 320000 | 322162 | F | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 12 Cawthorne Grove, Sheffield | 2025-10-22 | 315000 | 320219 | F | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 45 Cawthorne Grove, Sheffield | 2025-06-30 | 295000 | 311422 | L | 79 | 3942 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 26 Cawthorne Grove, Sheffield | 2025-06-20 | 270000 | 285030 | F | 78 | 3654 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 22 Cawthorne Grove, Sheffield | 2025-06-03 | 248000 | 261806 | F | 78 | 3356 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 27B Cawthorne Grove, Sheffield | 2025-04-29 | 350000 | 361078 | F | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 21 Cawthorne Grove, Sheffield | 2024-11-04 | 284000 | 292411 | F | 76 | 3848 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 25 Cawthorne Grove, Sheffield | 2024-10-10 | 176000 | 181391 | L | 78 | 2326 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 55 Cawthorne Grove, Sheffield | 2024-10-04 | 275000 | 283424 | F | 78 | 3634 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 51 Cawthorne Grove, Sheffield | 2024-07-19 | 270000 | 285898 | F | 75 | 3812 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 2 Cawthorne Grove, Sheffield | 2024-03-28 | 290000 | 314745 | F | 93 | 3384 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |

## postcode: n=8, with area 6, thin=False, median £/m² 3644, spread [3356, 3942], top 3942

| Address | Date | Price | Today | Tenure | m² | £/m² today | Source |
|---|---|---|---|---|---|---|---|
| 8 Cawthorne Grove, Sheffield | 2025-12-19 | 320000 | 322162 | F | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 12 Cawthorne Grove, Sheffield | 2025-10-22 | 315000 | 320219 | F | None | None | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 45 Cawthorne Grove, Sheffield | 2025-06-30 | 295000 | 311422 | L | 79 | 3942 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 26 Cawthorne Grove, Sheffield | 2025-06-20 | 270000 | 285030 | F | 78 | 3654 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 22 Cawthorne Grove, Sheffield | 2025-06-03 | 248000 | 261806 | F | 78 | 3356 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD |
| 55 Cawthorne Grove, Sheffield | 2024-10-04 | 275000 | 283424 | F | 78 | 3634 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 51 Cawthorne Grove, Sheffield | 2024-07-19 | 270000 | 285898 | F | 75 | 3812 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
| 2 Cawthorne Grove, Sheffield | 2024-03-28 | 290000 | 314745 | F | 93 | 3384 | https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=CAWTHORNE+GROVE&town=SHEFFIELD&min_date=19+November+2023&max_date=18+November+2024 |
