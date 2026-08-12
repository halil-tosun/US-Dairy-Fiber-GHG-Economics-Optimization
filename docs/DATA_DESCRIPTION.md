# DATA_DESCRIPTION

## Overview

This study does not analyze a pre-existing observational dataset. It
formulates diets computationally, using two small, fully transparent
input files as model parameters. Every number in every output table is
derived from these two files plus the fixed model equations and
constants documented in `docs/CODEBOOK.md`.

---

## `data/raw/ingredient_library.csv`

The composition and price of every feed ingredient available to the
optimizer. Seven ingredients are listed; five (`used_in_primary_model =
TRUE`) constitute the primary model's ingredient library (Table 1,
Tables 2-5); all seven are used only in the ingredient-library-breadth
robustness check (Table 6; script `06_ingredient_library_robustness.py`).

| Column | Description |
|---|---|
| `ingredient` | Ingredient name |
| `dm_pct` | Dry matter, % as-fed |
| `ndf_pct_dm` | Neutral detergent fiber, % of DM |
| `adf_pct_dm` | Acid detergent fiber, % of DM (hemicellulose = NDF \u2212 ADF; Van Soest et al., 1991) |
| `cp_pct_dm` | Crude protein, % of DM |
| `nel_mcal_kg_dm` | Net energy for lactation, Mcal/kg DM |
| `price_usd_per_ton_asfed` | Price, USD per short ton (907.185 kg), as-fed basis |
| `is_forage` | TRUE for alfalfa haylage, corn silage, and grass hay (used to compute the forage-inclusion-total and forage-sourced-NDF/physically-effective-fiber constraints); FALSE for all concentrates and byproducts |
| `used_in_primary_model` | TRUE for the 5 ingredients used in Tables 1-5; FALSE for DDGS and soybean hulls, used only in Table 6 |
| `price_source` | Citation/provenance for the price figure |
| `composition_source` | Citation/provenance for the composition figures |

### Composition and price provenance

- **Alfalfa haylage, corn silage, grass hay, corn grain, soybean meal**:
  composition from representative published NASEM (2021) feed library
  values. Prices from current (2026) USDA NASS Agricultural Prices, USDA
  WASDE, and the University of Missouri Extension 2026 Corn Silage
  Planning Budget (Publication G664) -- the last selected specifically
  because it reports the **full economic cost** of home-grown forage
  (operating plus ownership costs, including land opportunity cost),
  matching the USDA Agricultural Resource Management Survey (ARMS)
  "full economic cost of feed" costing philosophy (Dubman, 2000) rather
  than a spot or standing-crop market price.
- **DDGS**: composition from standard corn DDGS reference values; price
  from a late-2025/early-2026 futures-linked price projection.
- **Soybean hulls**: composition from Blasi et al. (2000, Kansas State
  University Extension MF-2438); price is an illustrative 2026 byproduct
  estimate (~90% of the corn grain price per ton), since no single
  current national quote for soybean hulls was independently confirmed
  during manuscript preparation -- **users extending this package for
  operation-specific decisions should replace this price with a local
  quote.**

All prices are **national averages** as of mid-2026, not region- or
farm-specific. The manuscript's Discussion and this package's
`REPRODUCIBILITY_CHECKLIST.md` both flag this explicitly: the
sensitivity analysis (Table 4) shows the economic magnitude of the
central finding to be highly sensitive to forage price assumptions in
particular, and dollar-denominated results should be treated as
illustrative of a real, directionally robust phenomenon rather than as
precise, farm-specific estimates.

---

## `data/raw/external_benchmarks.csv`

Published third-party benchmark values used for the external validation
check (Table 3; script `03_external_validation.py`).

| Column | Description |
|---|---|
| `quantity` | The model quantity being validated |
| `benchmark_value` | Published mean (where reported as mean \u00b1 SD) |
| `benchmark_sd` | Published standard deviation |
| `benchmark_low` / `benchmark_high` | Published range (where reported as a range rather than mean \u00b1 SD) |
| `unit` | Unit of measurement |
| `source` | Full citation/provenance |

Sources: NASEM (2021) *Nutrient Requirements of Dairy Cattle*, 8th
revised edition (a large, published multi-study dataset, for dietary
NDF, CP, DMI, and body weight); USDA ERS/Dairy Margin Coverage Program
and University of Illinois Farm Business Farm Management Association
(for the whole-farm feed cost benchmark); Farm and Dairy and Hubbard
Feeds extension benchmarks (for the lactating-cow share of whole-farm
feed expenditure used in the feed-cost accounting-scope reconciliation).
Full bibliographic details are provided in the accompanying manuscript's
Literature Cited section.

---

## Why This Package Does Not Contain a "Raw Observational Dataset"

Readers familiar with observational-study reproducibility packages may
expect a large primary dataset. This study is instead a **constrained
optimization** exercise: the two small CSV files above are the *entire*
empirical input; every table and figure is *computed*, not looked up,
from them via the equations documented in `docs/CODEBOOK.md`. This
design choice was made deliberately, to maximize computational
transparency and auditability -- every intermediate number, from a
single ingredient's price-per-kg-DM to the final IOFC gap, can be traced
to a specific line of code and a specific cited source.

---

## Data Access and Terms of Use

- USDA NASS, USDA WASDE, USDA ERS, and University of Missouri/Illinois
  Extension data are publicly available at no cost and require no
  special access permissions.
- NASEM (2021) benchmark figures are drawn from a copyrighted book;
  only the specific summary statistics (means, standard deviations)
  used for validation are reproduced here, consistent with fair use for
  research and educational purposes. Readers wishing to consult the full
  underlying dataset should obtain the original publication.
