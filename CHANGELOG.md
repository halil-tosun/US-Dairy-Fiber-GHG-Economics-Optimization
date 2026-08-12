# CHANGELOG

All notable changes to this reproducibility package will be documented in
this file.

The format is inspired by *Keep a Changelog* and follows semantic
versioning where appropriate.

---

## Version 1.0.0 (Initial Public Release)

### Added
- Complete Python source code for the constrained nonlinear optimization
  pipeline: diet formulation (`02_diet_optimization.py`), external
  validation against published benchmarks (`03`), price-sensitivity
  ("tornado") analysis (`04`), the minimum-alfalfa-inclusion cost
  analysis (`05`), the seven-ingredient byproduct-feed robustness check
  (`06`), and Figures 1-2 (`07`).
- Supplementary, formula-auditable Excel workbook
  (`excel_model/dairy_ghg_economics_model.xlsx`) implementing the same
  calculations for cell-by-cell inspection, with its own README.
- Ingredient composition and price library (`data/raw/ingredient_library.csv`)
  and external validation benchmark data (`data/raw/external_benchmarks.csv`).
- All six result tables (`output/Table1-6*.csv`) and both figures
  (`figures/Figure1-2*.png`, 300 DPI).
- README.md with repository overview and usage instructions.
- CODEBOOK.md describing the analytical workflow, the methane and
  economic equations, and the script-to-output correspondence.
- DATA_DESCRIPTION.md documenting data sources, provenance, and
  variable-level definitions.
- REPRODUCIBILITY_CHECKLIST.md.
- Replication_Guide.md with complete, step-by-step replication
  instructions.
- CITATION.cff and .zenodo.json for software citation and Zenodo
  metadata.
- LICENSE, requirements.txt, environment.yml, .gitignore.

### Reproducibility
- One-command Python workflow via `run_all.py` (7 scripts, well under
  one minute).
- All figures rendered at 300 DPI.
- Every statistic reported in the accompanying manuscript's Tables 1-5
  and Figures 1-2 was independently regenerated from this package and
  confirmed to match exactly (or within documented floating-point/solver
  tolerance) prior to release; see `docs/REPRODUCIBILITY_CHECKLIST.md`,
  "Internal Consistency Checks".
- Repository organized to remain valid regardless of eventual journal,
  manuscript title, or submission outcome.
- A single, minor ($0.01/cwt) numerical difference between this
  package's Table 6 and the manuscript's Table 6, attributable to
  SLSQP solver reinitialization order across a refactor rather than to
  any methods discrepancy, was identified during package preparation
  and is documented transparently in
  `docs/REPRODUCIBILITY_CHECKLIST.md`.
- Cross-checking this package against the manuscript also caught two
  display-only rounding slips in the manuscript's hand-transcribed
  Table 1 (soybean meal and soybean hull price per kg DM); the
  manuscript has been corrected to match this package's
  programmatically computed values. See
  `docs/REPRODUCIBILITY_CHECKLIST.md`, "A Corrected Manuscript Error,
  Caught by This Package."

### Notes
The Zenodo DOI: https://doi.org/10.5281/zenodo.21900057

The manuscript's own DOI (once published) will be added to this file and to
the citation metadata files at that time.
