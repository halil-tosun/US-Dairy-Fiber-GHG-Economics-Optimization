"""
01_ingredient_library.py

Loads data/raw/ingredient_library.csv, validates it, and writes
output/Table1_ingredient_library.csv (DM-basis price in $/kg DM, matching
the manuscript's Table 1) for the five ingredients used in the primary
model, plus the two byproduct ingredients used only in the ingredient-
library-breadth robustness check (Table 6; see 06_ingredient_library_robustness.py).
"""
import pandas as pd
from _paths import DATA_RAW, OUTPUT

df = pd.read_csv(DATA_RAW / "ingredient_library.csv")

# Convert as-fed $/ton price to DM-basis $/kg DM (1 short ton = 907.185 kg)
df["price_usd_per_kg_dm"] = df["price_usd_per_ton_asfed"] / 907.185 / (df["dm_pct"] / 100)

# Sanity checks
assert (df["dm_pct"] > 0).all() and (df["dm_pct"] <= 100).all(), "DM%% out of range"
assert (df["ndf_pct_dm"] >= df["adf_pct_dm"]).all(), "NDF must be >= ADF for all ingredients (hemicellulose = NDF - ADF)"
assert df["used_in_primary_model"].sum() == 5, "Primary model must use exactly 5 ingredients"
assert len(df) == 7, "Full library (primary + byproduct) must contain 7 ingredients"

out_cols = ["ingredient", "dm_pct", "ndf_pct_dm", "adf_pct_dm", "cp_pct_dm",
            "nel_mcal_kg_dm", "price_usd_per_kg_dm", "used_in_primary_model"]
df[out_cols].round(4).to_csv(OUTPUT / "Table1_ingredient_library.csv", index=False)

print("Table 1 -- Ingredient library (DM basis):")
print(df[["ingredient", "dm_pct", "ndf_pct_dm", "adf_pct_dm", "cp_pct_dm",
          "nel_mcal_kg_dm", "price_usd_per_kg_dm"]].round(3).to_string(index=False))
print(f"\nWrote {OUTPUT / 'Table1_ingredient_library.csv'}")
