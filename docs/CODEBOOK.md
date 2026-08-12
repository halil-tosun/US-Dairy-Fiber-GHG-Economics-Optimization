# CODEBOOK

## Analytical Workflow

Unlike a purely observational study, this package does not analyze a
single pre-collected dataset; it **formulates diets de novo** through
constrained nonlinear optimization, using a five-ingredient library
(`data/raw/ingredient_library.csv`) as model input. Every result table
and figure is produced by solving an optimization problem, not by
computing a summary statistic on fixed data.

| Script | Description | Produces |
|---|---|---|
| `_paths.py` | Shared path configuration and fixed model constants (animal assumptions, methane/GWP constants, optimization bounds, NDF sweep points); not run directly | — |
| `_calc.py` | Shared calculation module: ECM, FPCM, DMI (dilution-of-maintenance), the Niu et al. (2018) methane equation, GHG intensity, feed cost, and IOFC; not run directly | — |
| `01_ingredient_library.py` | Loads and validates the raw ingredient library; converts as-fed prices to a DM basis | Table 1 |
| `02_diet_optimization.py` | **Core analysis.** For each dietary NDF floor (28.0-37.2% DM), solves the constrained nonlinear optimization (SLSQP, 5 restarts) for the IOFC-maximizing diet among the 5 primary ingredients | Table 2; `data/processed/frontier_5ingredient.json` |
| `03_external_validation.py` | Compares model DMI, body weight, dietary NDF, and CP against a published multi-study benchmark (NASEM, 2021); reconciles the model's lactating-cow-only feed cost against published whole-farm feed cost benchmarks using a 65% lactating-cow expenditure share | Table 3 |
| `04_sensitivity_analysis.py` | Perturbs each ingredient price (\u00b120%) and the milk price (\u00b110%) independently, re-solving the optimization at both NDF-floor endpoints (28.0%, 37.2%) under each perturbation | Table 4 |
| `05_alfalfa_constraint.py` | Re-solves the optimization at the 28.0% NDF floor with a minimum alfalfa-inclusion constraint (0%, 10%, 15%, 20%), quantifying the IOFC cost of forcing alfalfa into the diet | Table 5 |
| `06_ingredient_library_robustness.py` | **Robustness check.** Adds DDGS and soybean hulls to the ingredient library (7 ingredients total) and re-solves the optimization, sweeping an NDF **ceiling** (not floor -- see below) | Table 6; `data/processed/frontier_7ingredient.json` |
| `07_make_figures.py` | Generates Figure 1 (efficient frontier) and Figure 2 (diet composition across the frontier) at 300 DPI, from `frontier_5ingredient.json` | Figure 1; Figure 2 |
| `run_all.py` | Runs scripts 01-07 in order | All tables and figures |

## Why Does Script 06 Sweep a Ceiling Instead of a Floor?

This is the single most important methodological detail to understand
before extending this package, and is worth stating plainly.

Scripts 02, 04, and 05 sweep a dietary NDF **floor** (minimum) because,
among the 5 primary ingredients, the unconstrained economic optimum sits
at the *lowest* feasible NDF (28.0% DM, the rumen-safety floor) -- cheap
ingredients in that library happen to have naturally low NDF profiles.
Raising the floor therefore forces the optimizer toward *higher*-NDF,
*more expensive* diets, producing the primary frontier reported in Table
2.

Once DDGS and (especially) soybean hulls are added to the library
(script 06), this relationship **reverses**. Soybean hulls combine a low
price with very high crude NDF (67% DM) and high digestible energy,
which makes the unconstrained economic optimum shift to a *much higher*
NDF composition (41.7% DM) than the primary model's entire tested range.
A floor constraint would therefore never bind across the primary
model's 28.0-37.2% range -- the same, unconstrained solution would
satisfy every floor value, producing a flat, uninformative frontier.

Script 06 instead sweeps an NDF **ceiling** (maximum) from 30.0% up to
the unconstrained optimum (41.7% DM), directly answering the practically
relevant question once byproducts are available: *what does it cost to
keep dietary NDF below various levels, given that a cheap, high-fiber
byproduct exists?* This produces a genuine, non-degenerate frontier
(Table 6) and is the basis for the manuscript's central robustness
finding: the *direction* of the fiber-GHG relationship is unchanged, but
its *economic magnitude* falls roughly ten-fold once byproduct feeds are
available to the optimizer.

## Core Equations (implemented in `_calc.py`)

| Quantity | Equation | Source |
|---|---|---|
| Energy-corrected milk (ECM) | ECM = 0.327\u00d7Milk + 12.95\u00d7Fat(kg/d) + 7.2\u00d7Protein(kg/d) | Tyrrell and Reid, 1965 |
| Fat- and protein-corrected milk (FPCM) | FPCM = Milk\u00d7(0.337 + 0.116\u00d7Fat% + 0.06\u00d7Protein%) | Sjaunja et al., 1990; reconsidered by Hall, 2023 |
| Net energy for maintenance | NE_m (Mcal/d) = 0.080\u00d7BW^0.75 | NASEM, 2021 |
| Net energy for lactation | NE_l (Mcal/d) = Milk\u00d70.74 | NASEM, 2021 |
| Dry matter intake (dilution of maintenance) | DMI = (NE_m + NE_l) / Diet NEL density | Bauman and Currie, 1980 |
| Enteric methane | CH4 (MJ/d) = 13.3 + 0.118\u00d7NDF \u2212 0.130\u00d7ECM + 2.20\u00d7MF \u2212 1.71\u00d7CP + 0.00521\u00d7BW | Niu et al., 2018 |
| Methane mass | CH4 (kg/d) = CH4(MJ/d) / 55.65 | Brouwer, 1965 (gross energy value of methane) |
| GHG intensity | kg CO2e/kg FPCM = CH4(kg/d)\u00d727.9 / FPCM | IPCC AR6 (2021), GWP100 |
| Feed cost | $/d = DMI\u00d7\u03a3(x_i\u00d7Price_i) + Premix | This study |
| Income over feed cost | IOFC = Milk revenue \u2212 Feed cost | This study |

Full bibliographic details for every reference above, including DOIs
where independently confirmed, are provided in the accompanying
manuscript's Literature Cited section.

## Optimization Method

All optimization problems are solved with SciPy's SLSQP (Sequential
Least-Squares Quadratic Programming; Kraft, 1988) implementation
(`scipy.optimize.minimize`, `method="SLSQP"`). Because SLSQP can
converge to a local rather than global optimum, every optimization in
this package is solved from **5 (primary model) or 7 (robustness check)
distinct starting points** spanning the feasible region, and the
feasible solution with the highest IOFC is retained. Feasibility of the
retained solution is independently re-verified against every constraint
(tolerance 1\u00d710\u207b\u2074) rather than relying on the solver's internal
convergence flag -- a deliberate design choice after an early version of
this analysis (during manuscript preparation, not present in this
package) was found to silently return an infeasible-but-flagged-feasible
solution at two frontier points.

## Determinism

This is a **deterministic optimization study**, not a stochastic
simulation: there is no random sampling, bootstrap resampling, or Monte
Carlo component anywhere in this package, and `SEED` in `_paths.py` is
retained only for documentation completeness (it is not consumed by any
random-number generator). Given the same ingredient library, price
inputs, and SciPy version, every script in this package will produce
bit-for-bit identical output on every run and on every machine.

The one caveat is **solver reinitialization order**: because SLSQP is
solved from multiple starting points and the *best feasible* result is
retained, changing the order or composition of the starting-point list
can, in rare cases, cause the solver to settle in a very slightly
different corner of a flat or near-flat region of the objective (this
occurs at at most one decimal place, in one table, in this package; see
`REPRODUCIBILITY_CHECKLIST.md`).
