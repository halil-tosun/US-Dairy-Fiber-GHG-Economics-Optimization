# Replication Guide

This guide walks through reproducing every table and figure in the
accompanying manuscript, step by step.

## 1. Set Up the Environment

**Option A -- Conda (recommended)**

```bash
conda env create -f environment.yml
conda activate dairy-fiber-ghg-econ-repro
```

**Option B -- pip**

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Run the Full Pipeline

```bash
cd code
python run_all.py
```

You should see console output for seven steps, each printing the table
(or figures) it produces, followed by a total runtime (approximately
15-20 seconds on a standard laptop).

## 3. Verify the Outputs

After running, check that the following files exist:

```
output/Table1_ingredient_library.csv
output/Table2_diet_composition_frontier.csv
output/Table3_external_validation.csv
output/Table4_price_sensitivity.csv
output/Table5_alfalfa_cost.csv
output/Table6_ingredient_library_robustness.csv
figures/Figure1_frontier.png
figures/Figure2_composition.png
data/processed/frontier_5ingredient.json
data/processed/frontier_7ingredient.json
```

## 4. Regenerate a Single Table or Figure

Each numbered script can be run independently, for example:

```bash
cd code
python 06_ingredient_library_robustness.py
```

This is useful if you only want to re-verify one specific result (e.g.,
the byproduct-feed robustness check) without rerunning the full
pipeline. Note that scripts `03`, `04`, and `05` depend on
`data/raw/ingredient_library.csv` directly (not on script `02`'s
output), so any script can, in principle, be run standalone once the
environment is set up; only `07_make_figures.py` requires that
`02_diet_optimization.py` has been run first, since it reads
`data/processed/frontier_5ingredient.json`.

## 5. Understanding the Model

Before reusing or extending this package, read `docs/CODEBOOK.md` in
full, particularly the section "Why Does Script 06 Sweep a Ceiling
Instead of a Floor?" This package's two frontiers (primary 5-ingredient
model and the 7-ingredient robustness check) sweep the dietary NDF
constraint in **opposite directions**, for a substantive economic
reason documented there; conflating the two, or assuming both use the
same constraint direction, will produce nonsensical results.

Also read `docs/DATA_DESCRIPTION.md` for the provenance of every price
and composition figure, and note explicitly that **all prices are
national averages**, not region- or farm-specific -- see the
Limitations discussion in the accompanying manuscript before using any
dollar-denominated result for an operation-specific decision.

## 6. Adapting This Package to a Different Ingredient Set, Price Environment, or Animal

This package was designed to be extended:

- **Different prices**: edit `data/raw/ingredient_library.csv` directly;
  no code changes are required.
- **Different animal (BW, milk yield, composition)**: edit the constants
  at the top of `code/_paths.py` (`BW`, `MILK`, `FAT`, `PROT_MILK`).
  Note that `MILK` is also hardcoded in `04_sensitivity_analysis.py`
  (for the milk-price-perturbation revenue calculation); update both
  locations together if you change milk yield.
- **Additional ingredients**: add a row to
  `data/raw/ingredient_library.csv` with `used_in_primary_model = FALSE`
  (to include it only in a robustness-style check analogous to script
  `06`) or `TRUE` (to include it in the primary model directly -- in
  which case you will likely also need to reconsider the diversification
  and inclusion-cap constraints in `code/_paths.py`, which were
  calibrated for the specific 5- and 7-ingredient libraries used in this
  study).

## 7. Troubleshooting

- **`ModuleNotFoundError`**: confirm the environment from Step 1 is
  activated before running `run_all.py`.
- **Optimization appears to hang or take unusually long**: SLSQP with 5-7
  restarts per NDF point normally completes each script in 1-5 seconds;
  if a script runs for more than ~30 seconds, check that SciPy is a
  recent version (>=1.11) per `requirements.txt`.
- **Figures look different from the manuscript**: confirm your
  matplotlib version matches `requirements.txt`; minor rendering
  differences across matplotlib versions do not affect the underlying
  data, only cosmetic details (marker size, font rendering).
