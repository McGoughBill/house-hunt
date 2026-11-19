# Clashes

- **falmouth / article4_direction**: "Nether Edge Article 4 direction (made 2005) applies IF the house is inside Nether Edge CA; many external alterations th (P, https://www.sheffield.gov.uk/planning-development/nether-edge-conservation-area); "Nether Edge 2005 direction probably does not apply (house outside the CA it covers)" (W2b, https://www.planning.data.gov.uk/entity.json?dataset=conservation-area&geometry=POINT(-1.487909%2053.35284)&geometry_relation=intersects&limit=10)
  - **SETTLED:** Probably outside Nether Edge conservation area, so the 2005 Article 4 direction probably does not apply (W2b). W2b tested the postcode centre against the conservation-area boundary on planning.data.gov.uk, with a control point that does hit Nether Edge. P's line was conditional ('applies IF inside'), not a contrary finding. Medium only: the boundary is within about 400 m and No. 34's place on the street is unknown. Ask on Saturday.
- **cawthorne / flood_rivers**: "flood zone not found; street not named in the two EA River Sheaf flood warning areas nearby" (W2b, https://riverlevels.uk/flood-warning-river-sheaf-from-west-view-lane-abbeydale-to-archer-road-norton-hammer-including-beauchief-hotel); "outside Flood Zones 2 and 3 (river flood zone 1, low)" (W2main, https://www.planning.data.gov.uk/entity.json?dataset=flood-risk-zone&geometry=POLYGON((-1.4890%2053.3450,-1.4840%2053.3450,-1.4840%2053.3475,-1.4890%2053.3475,-1.4890%2053.3450))&geometry_relation=intersects&limit=20)
  - **SETTLED:** Outside river Flood Zones 2 and 3 (W2main). Environment Agency flood zones on planning.data.gov.uk, with a control box over the Sheaf that does return Zone 2. W2b's line says 'not found', which agrees. Surface water is still unknown.
- **underwood / listing_facts**: {"type": "mid-terrace", "beds": 3, "receptions": 1, "area_sqft": 915, "area_m2": 85.0, "tenure": "L"} (L, https://www.primelocation.com/for-sale/houses/sheffield/hackthorn-road/); {"type": "mid-terrace", "beds": 3, "receptions": 1, "baths": 1, "area_sqft": 915, "area_m2": 85.0, "tenure": "L", "groun (L2, https://www.zoopla.co.uk/for-sale/details/74619438/)
  - **SETTLED:** L2 (Zoopla 74619438, opened directly). L2 read the listing itself; L's line cites a PrimeLocation search page for Hackthorn Road. The shared fields agree; L2 adds band A, EPC D, £0 ground rent and 'needs renovation'.
- **helmton / listing_facts**: {"type": "semi-detached", "beds": 3, "area_m2": 73, "area_sqft": 786, "tenure": "F", "council_tax": "B", "epc": "C", "ha (L, https://www.rightmove.co.uk/properties/89812113); {"type": "semi-detached", "beds": 3, "receptions": 1, "baths": 1, "tenure": "F", "council_tax": "B", "epc": "C", "price" (L2, https://whitehornes.co.uk/property-for-sale/helmton-drive-woodseats-s8-2/)
  - **SETTLED:** Both: same listing. L2 is the viewing listing (whitehornes s8-2: 3-bed semi, offers over £265k, freehold, B, C); L's Rightmove 89812113 is the same 3-bed listing and supplies the 786 sq ft (73 m²). No field disagrees.
- **hollythorpe / tenure** (cross-field): L+F (S4/tenure_lr, https://landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=HOLLYTHORPE+ROAD&town=SHEFFIELD); F (L2/listing_facts, https://whitehornes.co.uk/property-for-sale/hollythorpe-road-norton-lees-s8/); F (L/listing_history, https://www.zoopla.co.uk/for-sale/details/70241795)
  - **SETTLED:** Freehold (owner appears to hold both titles). Land Registry filed the 2010 sale twice at one price, once leasehold and once freehold, so the buyer took the house and its freehold together; both listings say freehold. Ask that the freehold title is in the sale; the conveyancer confirms the titles.

## Other rulings

- **helmton / tenure** (found by hand)
  - **SETTLED:** Freehold. Land Registry (2018 sale of No. 17, estate F) and both listings agree. The Saturday doc's leasehold claim came from No. 25, a different house.
- **helmton / floor_area_m2** (found by hand)
  - **SETTLED:** 73 m². From the 3-bed listing for No. 17. The 109 m² belonged to No. 25. Measure on Saturday.
- **leeshall / tenure** (found by hand)
  - **SETTLED:** Leasehold (medium). The only source on No. 57 itself is Zoopla's card for the Staves listing (leasehold). Land Registry is silent (no sale since 1995). 8 of 9 recent street semis were leasehold. Ask years left, ground rent and consent clauses.
- **welby / for_sale_or_let** (found by hand)
  - **SETTLED:** For sale only. Every portal shows it for sale; no advert to let was found; the 'for-rent' web address is Staves' page slug. The SpareRoom bungalow is a different house (garage and drive).
- **market / uk_trend** (found by hand)
  - **SETTLED:** No winner on direction; use the Sheffield UK HPI by type. Nationwide +0.5%, Halifax −1.2%, ONS +1.2%: all flat. Valuations index with the official Sheffield series by house type, which is local and by type.
- **falmouth / floor_area_m2** (found by hand)
  - **SETTLED:** Working figure 94 m², with 108 m² shown as the upper case. No third source: the energy-certificate register blocks fetching and HouseMetric refused the street. The method (price-evidence-plan §1c) takes the smallest supportable area. Measure on Saturday and ask for the EPC.
- **helmton / which_listing** (found by hand)
  - **SETTLED:** The 3-bed semi at offers over £265k (whitehornes s8-2). The viewing link in the Saturday doc opens the 3-bed listing; the 2-bed 1,026 sq ft Helmton Drive listing is another house.
- **underwood / second_listing** (found by hand)
  - **OPEN:** A Hunters listing on Underwood Road at the same price (30 Oct) may be this house with a second agent. Agents' pages can't settle it without contact: ask on Saturday.
