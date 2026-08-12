"""
02_diet_optimization.py

Core constrained nonlinear optimization for the primary (5-ingredient)
model. For each dietary NDF floor in NDF_FLOOR_POINTS, solves for the
income-over-feed-cost (IOFC)-maximizing diet subject to the constraints
described in Materials and Methods ("Constrained Optimization Framework"):
CP bounds, forage-inclusion bounds, forage-NDF (physically effective fiber)
floor, ingredient inclusion ceilings, and single-forage diversification caps.

Produces output/Table2_diet_composition_frontier.csv and
data/processed/frontier_5ingredient.json (consumed by 07_make_figures.py
and by 03/04/05).
"""
import json
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from _paths import (DATA_RAW, DATA_PROCESSED, OUTPUT, NDF_FLOOR_POINTS,
                     CP_MIN, CP_MAX, FORAGE_MIN, FORAGE_MAX, FORAGE_NDF_MIN,
                     SINGLE_FORAGE_CAP, CORNGRAIN_CAP, SBM_CAP)
from _calc import diet_stats

# ---- Load the 5 primary ingredients ----
df = pd.read_csv(DATA_RAW / "ingredient_library.csv")
df = df[df["used_in_primary_model"]].reset_index(drop=True)
NAMES = df["ingredient"].tolist()
IDX = {n: i for i, n in enumerate(NAMES)}
NDF = df["ndf_pct_dm"].values / 100
ADF = df["adf_pct_dm"].values / 100
CP = df["cp_pct_dm"].values / 100
NEL = df["nel_mcal_kg_dm"].values
PRICE = (df["price_usd_per_ton_asfed"] / 907.185 / (df["dm_pct"] / 100)).values
FORAGE_MASK = df["is_forage"].values.astype(bool)

i_alfalfa = IDX["Alfalfa haylage"]
i_cornsil = IDX["Corn silage"]
i_grasshay = IDX["Grass hay"]
i_corngrain = IDX["Corn grain ground"]
i_sbm = IDX["Soybean meal 48pct CP"]


def neg_iofc(x):
    return -diet_stats(x, NDF, ADF, CP, NEL, PRICE, FORAGE_MASK)["iofc_d"]


def check_feasible(x, ndf_floor, tol=1e-4):
    forage_tot = x[i_alfalfa] + x[i_cornsil] + x[i_grasshay]
    return all([
        abs(np.sum(x) - 1.0) < 1e-4,
        (CP @ x) >= CP_MIN - tol, (CP @ x) <= CP_MAX + tol,
        forage_tot >= FORAGE_MIN - tol, forage_tot <= FORAGE_MAX + tol,
        (NDF @ x) >= ndf_floor - tol,
        float((NDF * FORAGE_MASK) @ x) >= FORAGE_NDF_MIN - tol,
        x[i_corngrain] <= CORNGRAIN_CAP + tol,
        x[i_sbm] <= SBM_CAP + tol,
        x[i_alfalfa] <= SINGLE_FORAGE_CAP + tol,
        x[i_cornsil] <= SINGLE_FORAGE_CAP + tol,
        x[i_grasshay] <= SINGLE_FORAGE_CAP + tol,
        np.all(x >= -tol),
    ])


def solve(ndf_floor):
    """Solve from 5 distinct starting points; return the best feasible solution."""
    n = len(NAMES)
    starts = [
        np.array([0.20, 0.20, 0.10, 0.35, 0.15]),
        np.array([0.10, 0.10, 0.30, 0.30, 0.20]),
        np.array([0.05, 0.05, 0.50, 0.25, 0.15]),
        np.array([0.00, 0.00, 0.55, 0.30, 0.15]),
        np.array([0.30, 0.10, 0.10, 0.30, 0.20]),
    ]
    cons = [
        {"type": "eq", "fun": lambda x: np.sum(x) - 1.0},
        {"type": "ineq", "fun": lambda x: (CP @ x) - CP_MIN},
        {"type": "ineq", "fun": lambda x: CP_MAX - (CP @ x)},
        {"type": "ineq", "fun": lambda x: (x[i_alfalfa] + x[i_cornsil] + x[i_grasshay]) - FORAGE_MIN},
        {"type": "ineq", "fun": lambda x: FORAGE_MAX - (x[i_alfalfa] + x[i_cornsil] + x[i_grasshay])},
        {"type": "ineq", "fun": lambda x: (NDF @ x) - ndf_floor},
        {"type": "ineq", "fun": lambda x: float((NDF * FORAGE_MASK) @ x) - FORAGE_NDF_MIN},
        {"type": "ineq", "fun": lambda x: CORNGRAIN_CAP - x[i_corngrain]},
        {"type": "ineq", "fun": lambda x: SBM_CAP - x[i_sbm]},
        {"type": "ineq", "fun": lambda x: SINGLE_FORAGE_CAP - x[i_alfalfa]},
        {"type": "ineq", "fun": lambda x: SINGLE_FORAGE_CAP - x[i_cornsil]},
        {"type": "ineq", "fun": lambda x: SINGLE_FORAGE_CAP - x[i_grasshay]},
    ]
    best = None
    for x0 in starts:
        r = minimize(neg_iofc, x0, method="SLSQP", bounds=[(0, 1)] * n, constraints=cons,
                      options={"maxiter": 1000, "ftol": 1e-12})
        if check_feasible(r.x, ndf_floor) and (best is None or diet_stats(r.x, NDF, ADF, CP, NEL, PRICE)["iofc_d"] > diet_stats(best, NDF, ADF, CP, NEL, PRICE)["iofc_d"]):
            best = r.x
    return best


if __name__ == "__main__":
    frontier = []
    for ndf_floor in NDF_FLOOR_POINTS:
        x = solve(ndf_floor)
        assert x is not None, f"No feasible solution found at NDF floor {ndf_floor}"
        s = diet_stats(x, NDF, ADF, CP, NEL, PRICE, FORAGE_MASK)
        row = dict(ndf_floor=ndf_floor, **s, **{f"share_{n}": round(float(v), 4) for n, v in zip(NAMES, x)})
        frontier.append(row)

    df_out = pd.DataFrame(frontier)
    df_out.to_csv(OUTPUT / "Table2_diet_composition_frontier.csv", index=False)
    with open(DATA_PROCESSED / "frontier_5ingredient.json", "w") as fh:
        json.dump(frontier, fh, indent=2, default=float)

    print("Table 2 -- Diet composition and outcomes across the dietary NDF floor sweep:")
    print(df_out[["ndf_floor", "ghg_intensity", "iofc_cwt", "dmi", "cp"] +
                  [f"share_{n}" for n in NAMES]].round(4).to_string(index=False))
    gap = frontier[0]["iofc_cwt"] - frontier[-1]["iofc_cwt"]
    ghg_pct = 100 * (frontier[-1]["ghg_intensity"] / frontier[0]["ghg_intensity"] - 1)
    print(f"\nHeadline finding: IOFC gap = ${gap:.2f}/cwt, GHG intensity increase = {ghg_pct:.1f}%")
    print(f"Wrote {OUTPUT / 'Table2_diet_composition_frontier.csv'}")
    print(f"Wrote {DATA_PROCESSED / 'frontier_5ingredient.json'}")
