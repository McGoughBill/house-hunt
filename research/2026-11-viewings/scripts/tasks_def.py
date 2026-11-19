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
