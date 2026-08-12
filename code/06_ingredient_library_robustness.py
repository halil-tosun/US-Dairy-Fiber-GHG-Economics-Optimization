"""
06_ingredient_library_robustness.py

Robustness check addressing the critique that a 5-ingredient library does
not reflect commercial U.S. byproduct feeding practice. Adds distillers
dried grains with solubles (DDGS) and soybean hulls to the ingredient
library (7 ingredients total) and re-solves the optimization.

Because the unconstrained economic optimum under this expanded library
exceeds the primary model's NDF range entirely (soybean hulls' cheap,
high-NDF, highly digestible fiber shifts the cost-minimizing diet to a
much higher crude-NDF composition), this script sweeps an NDF CEILING
(maximum) rather than a floor (minimum) -- see docs/CODEBOOK.md,
"Why Does Script 06 Sweep a Ceiling Instead of a Floor?".

Produces output/Table6_ingredient_library_robustness.csv.
"""
import json
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from _paths import (DATA_RAW, DATA_PROCESSED, OUTPUT, NDF_CEILING_POINTS_7ING,
                     CP_MIN, CP_MAX, FORAGE_MIN, FORAGE_MAX, FORAGE_NDF_MIN_7ING,
                     SINGLE_FORAGE_CAP, CORNGRAIN_CAP, SBM_CAP, DDGS_CAP, SOYHULLS_CAP)
from _calc import diet_stats

df = pd.read_csv(DATA_RAW / "ingredient_library.csv")  # all 7 ingredients
NAMES = df["ingredient"].tolist()
IDX = {n: i for i, n in enumerate(NAMES)}
NDF = df["ndf_pct_dm"].values / 100
ADF = df["adf_pct_dm"].values / 100
CP = df["cp_pct_dm"].values / 100
NEL = df["nel_mcal_kg_dm"].values
PRICE = (df["price_usd_per_ton_asfed"] / 907.185 / (df["dm_pct"] / 100)).values
FORAGE_MASK = df["is_forage"].values.astype(bool)

i_alfalfa, i_cornsil, i_grasshay = IDX["Alfalfa haylage"], IDX["Corn silage"], IDX["Grass hay"]
i_corngrain, i_sbm = IDX["Corn grain ground"], IDX["Soybean meal 48pct CP"]
i_ddgs, i_soyhulls = IDX["DDGS"], IDX["Soybean hulls"]
N = len(NAMES)


def neg_iofc(x):
    return -diet_stats(x, NDF, ADF, CP, NEL, PRICE, FORAGE_MASK)["iofc_d"]


def check_feasible(x, ndf_ceiling, tol=1e-4):
    forage_tot = x[i_alfalfa] + x[i_cornsil] + x[i_grasshay]
    return all([
        abs(np.sum(x) - 1.0) < 1e-4,
        (CP @ x) >= CP_MIN - tol, (CP @ x) <= CP_MAX + tol,
        forage_tot >= FORAGE_MIN - tol, forage_tot <= FORAGE_MAX + tol,
        (NDF @ x) <= ndf_ceiling + tol,
        (NDF @ x) >= 0.25 - tol,
        float((NDF * FORAGE_MASK) @ x) >= FORAGE_NDF_MIN_7ING - tol,
        x[i_corngrain] <= CORNGRAIN_CAP + tol, x[i_sbm] <= SBM_CAP + tol,
        x[i_ddgs] <= DDGS_CAP + tol, x[i_soyhulls] <= SOYHULLS_CAP + tol,
        x[i_alfalfa] <= SINGLE_FORAGE_CAP + tol, x[i_cornsil] <= SINGLE_FORAGE_CAP + tol,
        x[i_grasshay] <= SINGLE_FORAGE_CAP + tol, np.all(x >= -tol),
    ])


def solve(ndf_ceiling):
    starts = [np.array(v) for v in (
        [0.20, 0.20, 0.10, 0.25, 0.10, 0.10, 0.05], [0.10, 0.10, 0.30, 0.20, 0.10, 0.10, 0.10],
        [0.05, 0.05, 0.45, 0.15, 0.10, 0.10, 0.10], [0.00, 0.00, 0.55, 0.15, 0.10, 0.10, 0.10],
        [0.30, 0.10, 0.10, 0.15, 0.10, 0.15, 0.10], [0.00, 0.30, 0.20, 0.10, 0.10, 0.20, 0.10],
        [0.10, 0.00, 0.35, 0.10, 0.05, 0.20, 0.20])]
    starts = [s / s.sum() for s in starts]
    cons = [
        {"type": "eq", "fun": lambda x: np.sum(x) - 1.0},
        {"type": "ineq", "fun": lambda x: (CP @ x) - CP_MIN},
        {"type": "ineq", "fun": lambda x: CP_MAX - (CP @ x)},
        {"type": "ineq", "fun": lambda x: (x[i_alfalfa] + x[i_cornsil] + x[i_grasshay]) - FORAGE_MIN},
        {"type": "ineq", "fun": lambda x: FORAGE_MAX - (x[i_alfalfa] + x[i_cornsil] + x[i_grasshay])},
        {"type": "ineq", "fun": lambda x: ndf_ceiling - (NDF @ x)},
        {"type": "ineq", "fun": lambda x: (NDF @ x) - 0.25},
        {"type": "ineq", "fun": lambda x: float((NDF * FORAGE_MASK) @ x) - FORAGE_NDF_MIN_7ING},
        {"type": "ineq", "fun": lambda x: CORNGRAIN_CAP - x[i_corngrain]},
        {"type": "ineq", "fun": lambda x: SBM_CAP - x[i_sbm]},
        {"type": "ineq", "fun": lambda x: DDGS_CAP - x[i_ddgs]},
        {"type": "ineq", "fun": lambda x: SOYHULLS_CAP - x[i_soyhulls]},
        {"type": "ineq", "fun": lambda x: SINGLE_FORAGE_CAP - x[i_alfalfa]},
        {"type": "ineq", "fun": lambda x: SINGLE_FORAGE_CAP - x[i_cornsil]},
        {"type": "ineq", "fun": lambda x: SINGLE_FORAGE_CAP - x[i_grasshay]},
    ]
    best, best_iofc = None, -np.inf
    for x0 in starts:
        r = minimize(neg_iofc, x0, method="SLSQP", bounds=[(0, 1)] * N, constraints=cons,
                      options={"maxiter": 1000, "ftol": 1e-12})
        if check_feasible(r.x, ndf_ceiling):
            s = diet_stats(r.x, NDF, ADF, CP, NEL, PRICE, FORAGE_MASK)
            if s["iofc_cwt"] > best_iofc:
                best, best_iofc = r.x, s["iofc_cwt"]
    return best


if __name__ == "__main__":
    frontier = []
    for ndf_ceiling in NDF_CEILING_POINTS_7ING:
        x = solve(ndf_ceiling)
        assert x is not None, f"No feasible solution at NDF ceiling {ndf_ceiling}"
        s = diet_stats(x, NDF, ADF, CP, NEL, PRICE, FORAGE_MASK)
        row = dict(ndf_ceiling=ndf_ceiling, **s, **{f"share_{n}": round(float(v), 4) for n, v in zip(NAMES, x)})
        frontier.append(row)
        print(f"NDF ceiling={ndf_ceiling*100:.1f}%  realized NDF={s['ndf']*100:.1f}%  "
              f"GHG={s['ghg_intensity']:.4f}  IOFC=${s['iofc_cwt']:.2f}/cwt")

    df_out = pd.DataFrame(frontier)
    df_out.to_csv(OUTPUT / "Table6_ingredient_library_robustness.csv", index=False)
    with open(DATA_PROCESSED / "frontier_7ingredient.json", "w") as fh:
        json.dump(frontier, fh, indent=2, default=float)

    gap_7ing = frontier[0]["iofc_cwt"] - frontier[-1]["iofc_cwt"]
    print(f"\n7-ingredient IOFC range: ${min(f['iofc_cwt'] for f in frontier):.2f}-"
          f"${max(f['iofc_cwt'] for f in frontier):.2f}/cwt (gap ${abs(gap_7ing):.2f}/cwt)")
    print("Primary 5-ingredient model comparable-range gap: $0.53/cwt")
    print(f"\nWrote {OUTPUT / 'Table6_ingredient_library_robustness.csv'}")
    print(f"Wrote {DATA_PROCESSED / 'frontier_7ingredient.json'}")
