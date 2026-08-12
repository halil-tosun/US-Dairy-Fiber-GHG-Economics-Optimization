# REPRODUCIBILITY_CHECKLIST

## Study

**Quantifying the economic cost of reducing dietary fiber to mitigate
greenhouse gas emissions in U.S. dairy cattle** (constrained
nonlinear optimization, single representative lactating cow)

---

## Reproducibility Status

| Item | Status |
|------|:------:|
| Source code included (Python) | Ok |
| Supplementary formula-auditable Excel workbook included | Ok |
| Ingredient library and benchmark input data included | Ok |
| Data provenance documented | Ok |
| README provided | Ok |
| CODEBOOK provided | Ok |
| Data documentation provided (including variable-level definitions) | Ok |
| Software dependencies documented | Ok |
| Conda environment provided | Ok |
| License provided | Ok |
| Citation metadata (CITATION.cff, .zenodo.json) | Ok |
| One-command workflow (`run_all.py`) | Ok |
| Figures reproducible (300 DPI) | (Figures 1-2) |
| Tables reproducible | (Tables 1-6) |
| Every reported statistic independently re-verified against the manuscript prior to release | Ok |
| Deterministic (no random sampling) | Ok |
| Open repository planned | Ok |
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
| Headline IOFC gap (28.0% vs. 37.2% NDF, primary model) | $0.53/cwt | `02_diet_optimization.py` |
| Headline GHG increase (28.0% vs. 37.2% NDF) | +6.1% | `02_diet_optimization.py` |
| GHG intensity, 28.0% NDF | 0.2450 kg CO2e/kg FPCM | `02_diet_optimization.py` |
| GHG intensity, 37.2% NDF | 0.2599 kg CO2e/kg FPCM | `02_diet_optimization.py` |
| External validation (NDF, DMI, BW, CP ranges vs. NASEM 2021) | Table 3 | `03_external_validation.py` |
| Feed cost accounting-scope reconciliation ($9.78-$10.62/cwt whole-farm-equivalent) | Table 3 | `03_external_validation.py` |
| Price-sensitivity tornado (all 6 rows) | Table 4 | `04_sensitivity_analysis.py` |
| Alfalfa-inclusion cost (0/10/15/20%) | Table 5 | `05_alfalfa_constraint.py` |
| Ingredient-library-breadth robustness (IOFC range) | $15.32-$15.37/cwt (gap $0.05/cwt) | `06_ingredient_library_robustness.py` |

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
