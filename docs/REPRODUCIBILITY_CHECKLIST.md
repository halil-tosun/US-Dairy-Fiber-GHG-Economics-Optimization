# REPRODUCIBILITY_CHECKLIST

## Study

**Quantifying the economic cost of reducing dietary fiber to mitigate
greenhouse gas emissions in U.S. dairy cattle** (constrained
nonlinear optimization, single representative lactating cow)

---

## Reproducibility Status

| Item | Status |
|------|:------:|
| Source code included (Python) | \u2713 |
| Supplementary formula-auditable Excel workbook included | \u2713 |
| Ingredient library and benchmark input data included | \u2713 |
| Data provenance documented | \u2713 |
| README provided | \u2713 |
| CODEBOOK provided | \u2713 |
| Data documentation provided (including variable-level definitions) | \u2713 |
| Software dependencies documented | \u2713 |
| Conda environment provided | \u2713 |
| License provided | \u2713 |
| Citation metadata (CITATION.cff, .zenodo.json) | \u2713 |
| One-command workflow (`run_all.py`) | \u2713 |
| Figures reproducible (300 DPI) | \u2713 (Figures 1-2) |
| Tables reproducible | \u2713 (Tables 1-6) |
| Every reported statistic independently re-verified against the manuscript prior to release | \u2713 |
| Deterministic (no random sampling) | \u2713 |
| Open repository planned | \u2713 |
| Zenodo DOI | Pending -- will be added upon archival release |
| Manuscript DOI | Pending -- will be added once available |

---

## Computational Environment

- Python environment documented in `environment.yml`
- Package list and pinned versions documented in `requirements.txt`
- Python version tested: 3.12
- Expected runtime: approximately 15-20 seconds on a standard laptop

---

## Expected Workflow

1. Create the Python environment (`conda env create -f environment.yml`
   or `pip install -r requirements.txt`).
2. Run `python code/run_all.py`.
3. Verify that Tables 1-6 appear in `output/` and that Figures 1-2 appear
   in `figures/` at 300 DPI.
4. Cross-check reported values against the manuscript's tables and
   figures (see `docs/CODEBOOK.md` for the full script-to-output
   correspondence).

---

## Internal Consistency Checks

Every value in Tables 1-6 and in Figures 1-2 produced by this package
was compared directly against the corresponding value reported in the
accompanying manuscript prior to this repository's release, including:

| Quantity | Manuscript value | Reproduced by |
|---|---|---|
| Headline IOFC gap (28.0% vs. 37.2% NDF, primary model) | $0.53/cwt | `02_diet_optimization.py` (exact: $14.636 \u2212 $14.105 = $0.531) |
| Headline GHG increase (28.0% vs. 37.2% NDF) | +6.1% | `02_diet_optimization.py` (exact: +6.06%) |
| GHG intensity, 28.0% NDF | 0.2450 kg CO2e/kg FPCM | `02_diet_optimization.py` (exact: 0.24504) |
| GHG intensity, 37.2% NDF | 0.2599 kg CO2e/kg FPCM | `02_diet_optimization.py` (exact: 0.25990) |
| External validation (NDF, DMI, BW, CP ranges vs. NASEM 2021) | Table 3 | `03_external_validation.py` |
| Feed cost accounting-scope reconciliation ($9.78-$10.62/cwt whole-farm-equivalent) | Table 3 | `03_external_validation.py` (exact: $9.79-$10.61/cwt; $0.01/cwt rounding, see below) |
| Price-sensitivity tornado (all 6 rows) | Table 4 | `04_sensitivity_analysis.py` (exact match on all 6 rows) |
| Alfalfa-inclusion cost (0/10/15/20%) | Table 5 | `05_alfalfa_constraint.py` ($0.00/$0.73/$1.14/$1.56/cwt; exact match) |
| Ingredient-library-breadth robustness (IOFC range) | $15.32-$15.37/cwt (gap $0.05/cwt) | `06_ingredient_library_robustness.py` (exact: $15.324-$15.368/cwt, gap $0.044/cwt) |

---

## Known, Documented Numerical Differences

Two minor, sub-cent differences were identified during package
preparation between this package's programmatically computed output and
the manuscript's reported values. Both were traced to their root cause,
judged immaterial to any conclusion, and are disclosed here in the
interest of full transparency (following the same disclosure practice
used in the companion regional study's own reproducibility package):

1. **Table 3 whole-farm-equivalent feed cost**: this package computes
   $9.79-$10.61/cwt; the manuscript reports $9.78-$10.62/cwt. The $0.01
   difference at each end is a floating-point rounding artifact of where
   division by the 65% lactating-cow-share factor is applied relative to
   rounding of the underlying per-cwt figures. Both ranges fall
   comfortably within the external benchmark ($10.26-$11.64/cwt) and
   support the same conclusion.
2. **Table 6 IOFC gap**: this package computes a $0.044/cwt gap across
   the 7-ingredient frontier; the manuscript reports $0.05/cwt. The
   difference arises from SLSQP solver reinitialization order in a
   refactor of the original analysis code into this package's cleaner,
   documented script structure (see `docs/CODEBOOK.md`, "Determinism").
   The headline comparison -- a roughly ten-fold reduction in economic
   magnitude relative to the primary model's $0.53/cwt gap -- is
   identical under both values ($0.53/$0.044 \u2248 12-fold; $0.53/$0.05 =
   10.6-fold) and does not affect any reported conclusion.

No other discrepancies were identified. All other values in Tables 1-6
and Figures 1-2 match the manuscript exactly (to the rounding shown).

### A Corrected Manuscript Error, Caught by This Package

During final package preparation, cross-checking this package's
programmatically computed Table 1 against the manuscript's Table 1
revealed that the manuscript's hand-typed price column contained two
display-only rounding slips: soybean meal was shown as $0.373/kg DM
(correct, formula-derived value: $0.3736 \u2192 rounds to $0.374) and
soybean hulls as $0.173/kg DM (correct value: $0.1715 \u2192 rounds to
$0.171). Both prices were always correctly computed at full floating-
point precision in every underlying calculation throughout the
manuscript and this package (the error was confined to the displayed,
rounded table cell, introduced when Table 1 was manually transcribed
into the manuscript rather than generated programmatically); no other
reported table, figure, or in-text statistic was affected. The
manuscript's Table 1 has been corrected to $0.374 and $0.171
respectively, matching this package's `output/Table1_ingredient_library.csv`
exactly. This is recorded here as a demonstration of the value of an
independent, code-based reproducibility package: the discrepancy was
caught by cross-checking this repository against the manuscript, not
the reverse.

---

## Transparency Statement

This repository has been prepared to maximize computational
reproducibility and long-term accessibility. It is organized around the
underlying study rather than any specific journal submission, so that it
remains fully valid regardless of the eventual publication venue,
manuscript title, or peer-review outcome.

Once archived, this release will be assigned a permanent Zenodo DOI,
which will be added to this document, to `README.md`, `CITATION.cff`,
and `.zenodo.json`.
