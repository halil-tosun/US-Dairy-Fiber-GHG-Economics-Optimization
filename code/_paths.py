"""
_paths.py -- Shared path configuration and constants for this repository.

Not run directly. Imported by every numbered script in code/.
"""
from pathlib import Path

# ---- Repository-relative paths ----
ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "output"
FIGURES = ROOT / "figures"

for p in (DATA_PROCESSED, OUTPUT, FIGURES):
    p.mkdir(parents=True, exist_ok=True)

# ---- Fixed animal / production assumptions (held constant across all diet scenarios) ----
BW = 650.0                 # body weight, kg
MILK = 38.0                 # milk yield, kg/d
FAT = 3.8                   # milk fat, %
PROT_MILK = 3.1              # milk true protein, %
NEM_COEF = 0.080             # NEmaintenance coefficient, Mcal/kg BW^0.75
NEL_PER_KG_MILK = 0.74       # NEl per kg milk, Mcal/kg
MILK_PRICE_CWT = 21.00       # USD/cwt, USDA NASS all-milk price (May 2026: $21.30/cwt)
PREMIX_USD_PER_COW_DAY = 0.55

# ---- Methane / GWP constants ----
MJ_PER_KG_CH4 = 55.65        # gross energy value of methane (Brouwer, 1965)
GWP100_CH4 = 27.9            # 100-yr GWP, kg CO2e/kg CH4 (IPCC AR6, 2021)

# ---- Optimization bounds (Methods, "Constrained Optimization Framework") ----
CP_MIN, CP_MAX = 0.160, 0.185
FORAGE_MIN, FORAGE_MAX = 0.35, 0.65
FORAGE_NDF_MIN = 0.20          # physically effective fiber floor, primary 5-ingredient model
FORAGE_NDF_MIN_7ING = 0.15     # relaxed for the 7-ingredient robustness check (Table 6)
SINGLE_FORAGE_CAP = 0.45
CORNGRAIN_CAP = 0.40
SBM_CAP = 0.20
DDGS_CAP = 0.20
SOYHULLS_CAP = 0.20

# ---- NDF sweep points ----
# Primary 5-ingredient model: NDF FLOOR swept from the rumen-safe minimum (28.0% DM)
# to the upper end of the plausible commercial range (37.2% DM; ~2/3 SD above the
# NASEM 2021 published mean of 34.1 +/- 4.6% DM).
NDF_FLOOR_POINTS = [0.28, 0.30, 0.32, 0.322, 0.34, 0.35, 0.36, 0.37, 0.372]

# 7-ingredient robustness check: NDF CEILING swept (direction reverses -- see
# docs/CODEBOOK.md -- because soybean hulls shift the unconstrained economic
# optimum to a much higher crude-NDF composition than the 5-ingredient model).
# Note: 40.0% is intentionally omitted -- it produces an identical solution to
# 41.7% (both hit the DDGS/soybean-hulls inclusion ceilings), so the manuscript's
# Table 6 reports only the six distinct points below.
NDF_CEILING_POINTS_7ING = [0.30, 0.32, 0.34, 0.36, 0.38, 0.417]

# ---- Reproducibility ----
SEED = 42  # not used for randomness in this deterministic-optimization study;
           # retained for consistency with SciPy solver initialization ordering.
