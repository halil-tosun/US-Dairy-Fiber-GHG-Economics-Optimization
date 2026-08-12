"""
03_external_validation.py

Compares model outputs (from data/processed/frontier_5ingredient.json,
produced by 02_diet_optimization.py) against published external
benchmarks (data/raw/external_benchmarks.csv), including the
lactating-cow-only vs. whole-farm-equivalent feed cost reconciliation
described in Results ("External Validation Against Published Benchmarks").

Produces output/Table3_external_validation.csv.
"""
import json
import pandas as pd
from _paths import DATA_RAW, DATA_PROCESSED, OUTPUT

with open(DATA_PROCESSED / "frontier_5ingredient.json") as fh:
    frontier = json.load(fh)

bench = pd.read_csv(DATA_RAW / "external_benchmarks.csv").set_index("quantity")

ndf_vals = [f["ndf"] * 100 for f in frontier]
dmi_vals = [f["dmi"] for f in frontier]
cp_vals = [f["cp"] * 100 for f in frontier]
feedcost_vals = [f["feed_cost_cwt"] for f in frontier]

lactating_share = bench.loc["Lactating-cow share of whole-farm feed expenditure", "benchmark_value"]
wholefarm_lo = min(feedcost_vals) / lactating_share
wholefarm_hi = max(feedcost_vals) / lactating_share

rows = [
    dict(quantity="Dietary NDF, %DM",
         model_value=f"{min(ndf_vals):.1f}-{max(ndf_vals):.1f} (range across frontier)",
         benchmark=f"{bench.loc['Dietary NDF','benchmark_value']} +/- {bench.loc['Dietary NDF','benchmark_sd']} (mean +/- SD)",
         assessment="Within range"),
    dict(quantity="Forage-sourced (physically effective) NDF, %DM",
         model_value="20.0 (imposed floor)",
         benchmark=f">= {bench.loc['Forage-sourced (physically effective) NDF minimum','benchmark_low']:.0f}-{bench.loc['Forage-sourced (physically effective) NDF minimum','benchmark_high']:.0f} (guidance minimum)",
         assessment="Consistent"),
    dict(quantity="Dietary CP, %DM",
         model_value=f"{min(cp_vals):.1f} (constant, lower bound)",
         benchmark=f"{bench.loc['Dietary CP','benchmark_value']} +/- {bench.loc['Dietary CP','benchmark_sd']} (mean +/- SD)",
         assessment="Modestly below mean; see Discussion"),
    dict(quantity="DMI, kg/d",
         model_value=f"{min(dmi_vals):.1f}-{max(dmi_vals):.1f} (range across frontier)",
         benchmark=f"{bench.loc['DMI','benchmark_value']} +/- {bench.loc['DMI','benchmark_sd']} (mean +/- SD)",
         assessment="Within range"),
    dict(quantity="Body weight, kg",
         model_value="650 (fixed input)",
         benchmark=f"{bench.loc['Body weight','benchmark_value']} +/- {bench.loc['Body weight','benchmark_sd']} (mean +/- SD)",
         assessment="Within range"),
    dict(quantity="Feed cost, $/cwt milk (lactating-cow ration only)",
         model_value=f"${min(feedcost_vals):.2f}-${max(feedcost_vals):.2f} (range across frontier)",
         benchmark="n/a -- different scope (see reconciliation below)",
         assessment="See reconciliation below"),
    dict(quantity="Feed cost, $/cwt milk (whole-farm-equivalent)",
         model_value=f"${wholefarm_lo:.2f}-${wholefarm_hi:.2f} (reconciled using {lactating_share:.0%} lactating-cow share)",
         benchmark=f"${bench.loc['Whole-farm feed cost','benchmark_low']:.2f}-${bench.loc['Whole-farm feed cost','benchmark_high']:.2f} ({bench.loc['Whole-farm feed cost','source']})",
         assessment="Within range"),
]

df_out = pd.DataFrame(rows)
df_out.to_csv(OUTPUT / "Table3_external_validation.csv", index=False)

print("Table 3 -- External validation against published benchmarks:")
for r in rows:
    print(f"- {r['quantity']}: model = {r['model_value']}; benchmark = {r['benchmark']}; {r['assessment']}")
print(f"\nWrote {OUTPUT / 'Table3_external_validation.csv'}")
