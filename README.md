# Quantifying the Economic Cost of Reducing Dietary Fiber to Mitigate Greenhouse Gas Emissions in U.S. Dairy Cattle

## Reproducibility Package

This repository contains the complete reproducibility package accompanying
a manuscript that uses constrained nonlinear optimization to jointly
quantify the enteric-methane and farm-profitability consequences of
dietary fiber (neutral detergent fiber, NDF) composition in U.S.
lactating dairy cow diets. Realistic, rumen-health-constrained diets are
formulated de novo across the commercial range of dietary NDF, and the
income-over-feed-cost (IOFC)-maximizing diet is solved for at each fiber
level, using the published enteric methane equation of Niu et al.
(2018).

This package is intentionally organized around the *study* rather than
any single journal submission. If the manuscript title, framing, or
target journal changes during peer review, this repository and its
contents remain valid without modification.

---

## Key Finding

Greenhouse gas (GHG) emission intensity rises approximately **linearly**
with dietary NDF, but farm profitability (income over feed cost, IOFC)
does not decline in step: the economic cost is small at low fiber levels
and steepens sharply once the least expensive low-fiber forage option is
exhausted (Figure 1). Under the primary five-ingredient model, this
produces a $0.53/cwt IOFC gap across the commercial NDF range. A
robustness check adding two common byproduct feeds (distillers dried
grains with solubles and soybean hulls) to the ingredient library
reduces this economic gap roughly ten-fold, to $0.05/cwt, while leaving
the underlying biological relationship between fiber and methane
unchanged -- demonstrating that the *economic*, but not the
*environmental*, stakes of dietary fiber management depend materially on
which feeds are available to the formulator.

---

## Repository Overview

This repository follows open science and computational reproducibility
principles and includes:

- Complete Python source code for the full constrained-optimization
  pipeline: diet formulation, external validation, price-sensitivity
  analysis, an alfalfa-inclusion cost analysis, and a seven-ingredient
  byproduct-feed robustness check
- A supplementary, formula-auditable Excel workbook implementing the
  same calculations for cell-by-cell inspection (`excel_model/`)
- The ingredient composition/price library and external validation
  benchmark data used as model inputs
- All six result tables and two figures reported in the manuscript
- Comprehensive documentation of the model equations, constraints, and
  data provenance
- Software environment specifications

---

## Repository Structure

```text
US-Dairy-Fiber-GHG-Economics-Optimization/
├── code/
│   ├── _paths.py                              # shared path config + fixed model constants
│   ├── _calc.py                                # shared calculation functions (methane, milk, DMI, economics)
│   ├── 01_ingredient_library.py                 # Table 1
│   ├── 02_diet_optimization.py                  # Table 2 (primary 5-ingredient frontier) -- CORE ANALYSIS
│   ├── 03_external_validation.py                # Table 3
│   ├── 04_sensitivity_analysis.py                # Table 4 (price tornado)
│   ├── 05_alfalfa_constraint.py                  # Table 5
│   ├── 06_ingredient_library_robustness.py       # Table 6 (7-ingredient byproduct-feed check)
│   ├── 07_make_figures.py                        # Figures 1-2
│   └── run_all.py
├── excel_model/
│   ├── dairy_ghg_economics_model.xlsx     # formula-auditable spreadsheet version (see excel_model/README.md)
│   └── README.md
├── data/
│   ├── raw/
│   │   ├── ingredient_library.csv                # 5 primary + 2 byproduct ingredients
│   │   └── external_benchmarks.csv               # published validation benchmarks
│   └── processed/
│       ├── frontier_5ingredient.json
│       └── frontier_7ingredient.json
├── output/                                       # generated tables (.csv)
├── figures/                                       # generated Figures 1-2 (.png, 300 DPI)
├── docs/
│   ├── CODEBOOK.md
│   ├── DATA_DESCRIPTION.md
│   ├── REPRODUCIBILITY_CHECKLIST.md
│   └── Replication_Guide.md
├── README.md
├── CHANGELOG.md
├── CITATION.cff
├── .zenodo.json
├── LICENSE
├── requirements.txt
├── environment.yml
└── .gitignore
```

## Documentation

- **docs/CODEBOOK.md** -- analytical workflow, core equations, and why
  the primary and robustness-check frontiers sweep the NDF constraint in
  opposite directions (important -- read before extending this package)
- **docs/DATA_DESCRIPTION.md** -- data sources, provenance, and
  variable definitions
- **docs/REPRODUCIBILITY_CHECKLIST.md** -- reproducibility checklist and
  full internal consistency verification against the manuscript
- **docs/Replication_Guide.md** -- complete, step-by-step replication
  guide, including how to adapt this package to a different ingredient
  set, price environment, or animal

## Installation

```bash
conda env create -f environment.yml
conda activate dairy-fiber-ghg-econ-repro
```

or

```bash
pip install -r requirements.txt
```

## Run

```bash
cd code
python run_all.py
```

This reproduces the complete analytical workflow: the ingredient
library (Table 1), the core constrained-optimization frontier across the
primary five-ingredient model (Table 2), external validation against
published benchmarks (Table 3), price-sensitivity analysis (Table 4),
the minimum-alfalfa-inclusion cost analysis (Table 5), the
seven-ingredient byproduct-feed robustness check (Table 6), and Figures
1-2.

Expected runtime: approximately 15-20 seconds on a standard laptop. This
is a **deterministic optimization study** -- there is no random sampling
anywhere in this package, so every run produces identical output (see
`docs/CODEBOOK.md`, "Determinism").

## Script-to-Output Correspondence

| Script | Produces |
|---|---|
| `01_ingredient_library.py` | Table 1 (ingredient composition and price) |
| `02_diet_optimization.py` | Table 2 (primary 5-ingredient diet composition and outcomes frontier) -- **core analysis** |
| `03_external_validation.py` | Table 3 (validation against published NASEM and USDA ARMS/FBFM benchmarks) |
| `04_sensitivity_analysis.py` | Table 4 (\u00b120% ingredient price / \u00b110% milk price sensitivity) |
| `05_alfalfa_constraint.py` | Table 5 (economic cost of minimum alfalfa inclusion) |
| `06_ingredient_library_robustness.py` | Table 6 (7-ingredient byproduct-feed robustness check) |
| `07_make_figures.py` | Figure 1 (efficient frontier); Figure 2 (diet composition across the frontier) |

## A Note on the Two Optimization Frontiers

This package solves **two distinct constrained-optimization frontiers**,
which sweep the dietary NDF constraint in **opposite directions** for a
substantive economic reason (not an inconsistency): the primary
5-ingredient model sweeps an NDF **floor** (because the unconstrained
optimum sits at the lowest feasible NDF), while the 7-ingredient
robustness check sweeps an NDF **ceiling** (because adding soybean hulls
shifts the unconstrained optimum to a much higher NDF than the primary
model's entire range). This is explained in full, with the underlying
economics, in `docs/CODEBOOK.md`, "Why Does Script 06 Sweep a Ceiling
Instead of a Floor?" -- **read this before extending or reusing the
optimization code.**

## Citation

Please cite both the published article (once available) and this
archived repository. Citation metadata are provided in `CITATION.cff`
and `.zenodo.json`.

## License

MIT License (code and derived/processed data in this repository). The
underlying ingredient-price and external-validation benchmark data
originate from publicly available third-party sources; see
`docs/DATA_DESCRIPTION.md` for provenance, access details, and their own
terms of use.

## Contact

**Halil Tosun**

Department of Animal Science, School of Agricultural and Food Sciences,

ADA University, Baku, Azerbaijan

ORCID: https://orcid.org/0000-0001-5117-0390

Email: halilibrahimtosun@gmail.com

**Victor E. Cabrera**

Department of Animal and Dairy Sciences, 

University of Wisconsin-Madison,
Madison, WI, USA

ORCID: https://orcid.org/0000-0003-1739-7457

Email: vcabrera@wisc.edu

**Zenodo DOI:** https://doi.org/10.5281/zenodo.21900057

**Version:** 1.0.0
