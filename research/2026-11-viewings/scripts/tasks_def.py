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
