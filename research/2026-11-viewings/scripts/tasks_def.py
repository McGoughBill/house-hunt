"""Task definitions shared by make_tasks.py and status.py. One task = one source, all houses."""
HOUSE_IDS = ["falmouth", "welby", "leeshall", "cawthorne", "underwood", "helmton", "hollythorpe"]

TASKS = {
    "M1": dict(
        scope="Market: national and Sheffield trends, gap below asking, RICS, rates",
        ids=["market"],
        sources="Nationwide, Halifax, ONS UK HPI, Zoopla house price reports, RICS Residential Market Survey, Moneyfacts, Bank of England",
        fields=["uk_hpi_nationwide_annual_pct", "uk_hpi_halifax_annual_pct", "ons_ukhpi_annual_pct",
                "sheffield_hpi_detached", "sheffield_hpi_semi", "sheffield_hpi_terraced", "sheffield_hpi_flat",
                "sale_vs_asking_gap_pct", "rics_new_buyer_enquiries_balance", "rics_new_instructions_balance",
                "bank_rate", "next_bank_rate_decision_date", "avg_2yr_fixed_rate", "avg_5yr_fixed_rate"],
        extra="For each sheffield_hpi_* fact give the latest month's index and price, and the 1, 3 and 12-month % changes in note.\n"
              "Also, if you can, write Sheffield HPI by type for the last 36 months to data/hpi_sheffield.csv (month,type,index,source)."),
    "M2": dict(
        scope="Stock: months of stock, days on market and share of price cuts in S8",
        ids=["market"],
        sources="Home.co.uk asking price index, PropertyData free pages, ONS/Land Registry sales counts",
        fields=["s8_listings_for_sale", "s8_sales_per_month", "s8_months_of_stock",
                "s8_median_days_on_market", "s8_share_listings_price_cut"],
        extra="Say in note which area and month each figure covers. Months of stock = listings / sales per month; show the sum."),
    "H": dict(
        scope="Hazards: mining, ground, flood, knotweed, protected trees",
        ids=HOUSE_IDS,
        sources="Mining Remediation Authority (Coal Authority) interactive map, BGS GeoIndex, Environment Agency flood maps (check-long-term-flood-risk.service.gov.uk), Environet knotweed map, Sheffield City Council TPO map",
        fields=["coal_mining_risk", "landslip", "made_ground", "shrink_swell",
                "flood_rivers", "flood_surface_water", "knotweed_nearby", "tree_preservation_order"],
        extra="Hollythorpe's postcode is unknown: find it from public records first, or record facts at street level and say so."),
    "P": dict(
        scope="Planning: applications for each house and its neighbours, conservation areas, Article 4, building control",
        ids=HOUSE_IDS,
        sources="Sheffield planning portal (planningapps.sheffield.gov.uk), Sheffield council conservation-area and Article 4 maps, planning.data.gov.uk",
        fields=["planning_history", "neighbour_applications", "conservation_area",
                "article4_direction", "building_control_signoff"],
        extra="Give each application's reference, date, description and decision in value or note. Neighbours = within about 5 doors."),
    "C": dict(
        scope="Certificates: energy certificates, FENSA, Gas Safe",
        ids=HOUSE_IDS,
        sources="find-energy-certificate.service.gov.uk (energy-certificate register), FENSA certificate check, Gas Safe Register",
        fields=["epc_certificates", "epc_floor_area_m2", "epc_current_band", "epc_property_type",
                "epc_improvements", "fensa_record", "gas_safe_record"],
        extra="epc_certificates: every certificate, as a list of {date, band, floor_area_m2, url}. "
              "epc_improvements: the list with cost ranges, quoted from the latest certificate. "
              "The shell cannot reach the register (fetch_epc.py failed), so use the web tools."),
}

SECTORS = {"S1": ("S7 2", ["falmouth"]), "S2": ("S8 0", ["cawthorne"]),
           "S3": ("S8 8", ["underwood", "helmton"]), "S4": ("S8 9", ["welby", "leeshall", "hollythorpe"])}
for tid, (sector, ids) in SECTORS.items():
    TASKS[tid] = dict(
        scope=f"Comparables for sector {sector}: Land Registry sales and floor areas",
        ids=ids, comps=True,
        sources="Land Registry price-paid search (landregistry.data.gov.uk/app/ppd), energy-certificate register for floor areas; sold-price sites only if they cite Land Registry",
        fields=["own_past_sales", "last_sale_price", "last_sale_date", "tenure_lr",
                "street_highest_price", "street_sales_24m", "postcode_sales_24m"],
        extra=f"Also write every sale since Nov 2024 of the same house type on each house's street, its full postcode and sector {sector} "
              f"to data/sales/{tid}.jsonl, one per line, matching schema/sale.json. Add floor_area_m2 from the energy-certificate register where you can.")

COMPS_AVAILABLE_IF_LR = ["own_past_sales", "last_sale_price", "last_sale_date", "tenure_lr"]

# ---- Wave 2: gap-fill, web tools only. Skip what wave 1 showed is blocked. ----
BLOCKED = ("Known blocked, do not try: map.bgs.ac.uk and BGS GeoIndex; the Coal Authority/Mining Remediation Authority interactive map; "
           "check-long-term-flood-risk.service.gov.uk (captcha) and Environment Agency ArcGIS map services; planningapps.sheffield.gov.uk; "
           "find-energy-certificate.service.gov.uk; Environet's knotweed map; Sheffield's TPO map; Home.co.uk; PropertyData. "
           "The shell cannot reach the web at all: use WebSearch and WebFetch only.")
TASKS["W2a"] = dict(
    wave=2, cap=15,
    scope="Market gaps: how far below asking houses sell now; S8 days on market and share of listings cut",
    ids=["market"],
    sources="Zoopla House Price Index reports (business.zoopla.co.uk / zoopla.co.uk/discover), Rightmove House Price Index press releases "
            "(plc.rightmove.co.uk, rightmove.co.uk/news), Sheffield estate agents' published market reports, Jitty or other published "
            "local market statistics pages, ONS/Land Registry sales counts. Research and press pages only: never open a property listing.",
    fields=["sale_vs_asking_gap_pct", "s8_median_days_on_market", "s8_share_listings_price_cut",
            "s8_listings_for_sale", "s8_months_of_stock", "sheffield_days_to_sell", "sheffield_share_listings_cut"],
    extra="Latest month available (Oct or Nov 2026 ideally); say in note the area (UK, Yorkshire, Sheffield, S8) and the month each figure covers. "
          "If no S8 figure exists, give the nearest wider area (Sheffield, then Yorkshire and the Humber) under the sheffield_* field, and "
          "keep the s8_* field null with the reason. Months of stock = listings / sales per month (S8 sales run about 45 a month, Mar-May 2026, "
          "per facts/M2.jsonl); show the sum.\n" + BLOCKED)
TASKS["W2b"] = dict(
    wave=2, cap=22,
    scope="Council documents and hazards: conservation areas, Article 4, flood risk and history, mining and landslip",
    ids=HOUSE_IDS,
    sources="Sheffield City Council conservation-area appraisals and boundary maps (PDFs on sheffield.gov.uk), planning.data.gov.uk "
            "(conservation-area and article-4 datasets, by API or entity pages), Sheffield Strategic Flood Risk Assessment (SFRA) and its maps, "
            "Sheffield Local Flood Risk Management Strategy and Section 19 flood investigation reports, Environment Agency documents "
            "(e.g. Don catchment / River Sheaf reports), insurers' or other postcode flood-risk pages that open without a captcha, "
            "news reports of past floods by street (2007, 2019, 2023), BGS or council geology and mining documents (e.g. the Sheffield "
            "Plan's coal-mining development referral area, Coal Authority referral-area data on planning.data.gov.uk).",
    fields=["conservation_area", "article4_direction", "flood_rivers", "flood_surface_water", "flood_history",
            "coal_mining_risk", "landslip"],
    extra="Order of work: (1) conservation_area and article4_direction for falmouth (Nether Edge CA, Article 4 of 2005), underwood and helmton "
          "(Norton CA nearby) only; for these three, decide in or out against a boundary map or geometry, and give the house's coordinates "
          "and how you placed it. Write nothing new for those fields on the other four (wave 1 covered them). "
          "(2) Flood, all seven houses, cawthorne first (6 Cawthorne Grove, S8 0ND, Millhouses, beside the River Sheaf, which flooded in 2007). "
          "flood_rivers and flood_surface_water: the zone or risk band and the source map or table; flood_history: any recorded flooding of the "
          "street or postcode, with date. (3) coal_mining_risk and landslip from any document you can open (e.g. whether the postcode lies in "
          "the Coal Authority's development high-risk area or coalfield). If only area-level evidence exists, give it with confidence low and say so. "
          "Postcodes are in houses.yaml. Get coordinates for each postcode from postcodes.io via WebFetch "
          "(https://api.postcodes.io/postcodes/<postcode>).\n" + BLOCKED)
TASKS["W2c"] = dict(
    wave=2, cap=20,
    scope="Floor areas for comparable sales, and sales back to Nov 2023, so more sales get a £/m²",
    ids=HOUSE_IDS,
    sources="HouseMetric (housemetric.co.uk street pages: Land Registry prices joined to energy-certificate floor areas), "
            "Land Registry price-paid search (landregistry.data.gov.uk/app/ppd, street or postcode CSV), other sold-price pages that show "
            "a floor area and cite Land Registry or the energy-certificate register (e.g. Chimnie, Bricks&Logic "
            "sold-price pages, never a for-sale listing).",
    fields=["comps_floor_areas_added"],
    extra="Goal: for each house's street and full postcode, every sale since 19 Nov 2023 of the same Land Registry type as the house "
          "(falmouth T; welby D; leeshall S; cawthorne S; underwood T; helmton S; hollythorpe S), each with floor_area_m2 where any source gives it. "
          "Existing sales are in data/sales/S1-S4.jsonl (Nov 2024 on, no floor areas). Write every sale you find or confirm, old or new, to "
          "data/sales/W2c.jsonl, one per line, matching schema/sale.json, with floor_area_m2 (m², 1 sq ft = 0.0929 m²) and its source URL "
          "in a field area_source. Keep source = the Land Registry or sold-price URL for the price. Same address+date+price as an existing line "
          "is fine: comps.py merges them. Best route: one HouseMetric street page per street (e.g. https://housemetric.co.uk/house-prices/"
          "Welby-Place/S8-9D), which lists price, date and m² together. Streets: Falmouth Road S7 2; Welby Place S8 9; Lees Hall Road S8 9; "
          "Cawthorne Grove S8 0; Underwood Road S8 8; Helmton Drive S8 8; Hollythorpe Road S8 9. Then, per house, one fact line "
          "field comps_floor_areas_added: value = count of same-type sales since Nov 2023 with a floor area, note = gaps. Do not open the "
          "seven houses' own for-sale listings.\n" + BLOCKED)

# ---- Wave 4: usable local prices. Every brief needs 2+ comparables and a top price, even if old or few. ----
TASKS["W4C"] = dict(
    wave=4, cap=35,
    scope="Comparables and top prices for all seven houses: at least 2 comparable sales each, widening step by step",
    ids=HOUSE_IDS,
    sources="Land Registry price-paid search via WebFetch (landregistry.data.gov.uk/app/ppd/ppd_data.csv?header=true&limit=all&street=...&town=SHEFFIELD, "
            "or &postcode=S8+9DB, or &postcode=S8+9 for a sector, with min_date/max_date and property_type=detached|semi-detached|terraced); "
            "postcodes.io for coordinates (https://api.postcodes.io/postcodes/<postcode>) to measure distance; HouseMetric street pages and "
            "other sold-price pages that cite Land Registry or the energy-certificate register, for floor areas only. Never a for-sale listing.",
    fields=["comparable", "street_top_price_ever", "area_top_price_same_type", "comps_summary"],
    extra="""Already known (read first, do not refetch): data/sales/S1-S4.jsonl and W2c.jsonl (sales and floor areas), out/comps/summary.json
(street and postcode summaries, street_ceiling_ever, last sale), facts.json. Land Registry types: falmouth T (mid-terrace); welby D (detached
bungalow, 60 m², built about 1990); leeshall S; cawthorne S; underwood T; helmton S; hollythorpe S. Falmouth, Welby, Underwood and Helmton
have fewer than 2 usable comparables now; Lees Hall, Cawthorne and Hollythorpe have enough, so for those three pick the 2-4 best
existing ones (same street, same type, nearest size, most recent) and add only the two top prices.

For each house, widen step by step and STOP at the first step that gives at least 2 comparables:
  1. Same street, same type, any age.
  2. Same type within 500 m of the house, last 5 years (since Nov 2021).
  3. Similar type within 1 km (e.g. a semi for a terrace, any detached house for a bungalow), last 5 years.
  4. Older sales of the step-2 or step-3 kind.
A sale counts only once a Land Registry record (or a sold-price page that quotes one) gives its address, date and price. Exclude new builds,
category-B (non-market) sales, and the house's own past sales.

Write ONE fact line per comparable, field "comparable", value an object:
 {"address","postcode","date","price","value_today","age_band","type","tenure","floor_area_m2","distance_m","differs","step","lr_record"}
 - value_today: price x index(2026-09, type) / index(sale month, type), Sheffield UK HPI. Use data/hpi_sheffield_ukhpi.csv
   (2016-01 on; columns detached, semi_detached, terraced). For 2010-10 to 2015-12 use data/hpi_sheffield.csv (same UK HPI series,
   long form) and say so in note. Before 2010-10: null, with the reason. Do the sums in a short python script, not by hand.
 - age_band, counted back from 19 Nov 2026: <1, 1-2, 2-3, 3-4, 4-5, 5-6 or 6+ yrs.
 - distance_m: straight line from the house's postcode centre to the sale's postcode centre (postcodes.io), rounded to 10 m;
   0 for same postcode. Say "postcode centres" in note.
 - differs: a few words, e.g. "end terrace, 12 m² larger, freehold".
 - step: 1-4. lr_record: the Land Registry URL that shows this sale (also put it in source).
Also append each comparable as a sale row to data/sales/W4C.jsonl (schema/sale.json, plus "house" and "step" keys) so the checkers can
recompute from raw rows.

Per house, also:
 - street_top_price_ever: value {address, date, price, type, tenure, value_today}: the highest price ever paid on the house's street,
   any type, from a Land Registry street query with no date limit. Check out/comps/summary.json street_ceiling_ever and confirm or correct it.
 - area_top_price_same_type: value {address, date, price, value_today, area}: the highest price paid for the house's type in its
   postcode sector (S7 2, S8 0, S8 8 or S8 9; name the sector in area). Query the sector with the type filter; if the query only
   works over a date window, give the window in note and say "highest found in <window>", not "ever".
 - comps_summary: value {n, steps_used, range_today_low, range_today_high}, note = gaps or doubts.
""" + BLOCKED)
