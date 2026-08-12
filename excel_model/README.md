# Excel Model (Supplementary, Formula-Auditable Version)

## What This Is

`dairy_ghg_economics_model.xlsx` is a **formula-based spreadsheet
implementation** of the same diet-formulation, methane, and economic
calculations that the Python pipeline in `code/` implements
programmatically. It is provided as a supplementary, non-code-literate-
friendly artifact for readers, reviewers, and instructors who want to
inspect every intermediate calculation (feed cost, DMI, enteric methane,
GHG intensity, IOFC) cell-by-cell in a spreadsheet environment, without
needing to read Python.

**The Python pipeline in `code/` is the authoritative, primary source
for every table and figure reported in the manuscript** (see
`docs/REPRODUCIBILITY_CHECKLIST.md` for the full statistic-by-statistic
verification). The Excel workbook was used during model development and
for the initial exploratory 9-scenario comparison referenced in
Methods ("Study Design Overview") as superseded by the constrained-
optimization analysis; it does **not** independently run the
constrained SLSQP optimization itself (Excel has no native nonlinear
solver equivalent to SciPy's SLSQP used in `code/02_diet_optimization.py`
and `code/06_ingredient_library_robustness.py`), but its `Optimization`,
`Validation & Sensitivity`, and `Ingredient Library Robustness` sheets
reproduce the Python pipeline's *results* in formula-linked, auditable
form for cross-checking.

## Sheet-by-Sheet Guide

| Sheet | Contents | Corresponds to |
|---|---|---|
| `README` | Purpose, structure, color-coding key, assumptions to validate, and a summary of the ingredient-library robustness update | — |
| `Ingredients` | The 5 primary ingredients (feed composition, price, DM-basis conversion formulas) plus the 2 byproduct ingredients (DDGS, soybean hulls) used only in the robustness sheet | `data/raw/ingredient_library.csv`; Table 1 |
| `Diet Scenarios` | A fixed 9-scenario (3 forage sources \u00d7 3 forage:concentrate ratios) exploratory comparison used during model development, superseded by the constrained-optimization analysis (see Methods) | Not reported as a result (see manuscript, Methods, "Study Design Overview") |
| `Calculations` | Cell-by-cell ECM, FPCM, DMI, enteric methane, GHG intensity, feed cost, and IOFC formulas for each of the 9 fixed scenarios above | `code/_calc.py` (same equations, Python implementation) |
| `Results` | Summary trade-off table and marginal-cost curve for the 9 fixed scenarios | (superseded; see above) |
| `Optimization` | The primary 5-ingredient constrained-optimization frontier (headline finding) | Table 2; `code/02_diet_optimization.py` |
| `Validation & Sensitivity` | External validation against NASEM (2021) benchmarks; price-sensitivity tornado analysis; alfalfa-inclusion cost analysis | Tables 3-5; `code/03-05*.py` |
| `Ingredient Library Robustness` | The 7-ingredient (DDGS + soybean hulls) robustness check | Table 6; `code/06_ingredient_library_robustness.py` |

## Color Key (per in-sheet convention)

- **Blue text** = hardcoded input / editable assumption
- **Black text** = formula (recalculates automatically)
- **Yellow fill** = key assumption to review/update before submission

## Opening This File

This workbook was built and tested with LibreOffice Calc and Microsoft
Excel. All values are stored as live formulas (not hardcoded results),
so opening the file and pressing recalculate (F9 in Excel; Ctrl+Shift+F9
to force a full recalculation) will reproduce every value from the raw
inputs in the `Ingredients` sheet.
