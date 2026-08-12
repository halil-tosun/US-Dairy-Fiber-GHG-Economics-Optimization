"""
05_alfalfa_constraint.py

Because alfalfa haylage does not enter the unconstrained cost-minimizing
solution at any tested price level (04_sensitivity_analysis.py), this
script re-solves the optimization at the nutritionally optimal NDF floor
(28.0% DM) with a minimum alfalfa-inclusion constraint imposed at levels
consistent with common industry practice, quantifying the IOFC cost
(Results, "Economic Cost of Alfalfa Inclusion").

Produces output/Table5_alfalfa_cost.csv.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from _paths import DATA_RAW, OUTPUT, CP_MIN, CP_MAX, FORAGE_MIN, FORAGE_MAX, \
    FORAGE_NDF_MIN, SINGLE_FORAGE_CAP, CORNGRAIN_CAP, SBM_CAP
from _calc import diet_stats

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
i_alfalfa, i_cornsil, i_grasshay = IDX["Alfalfa haylage"], IDX["Corn silage"], IDX["Grass hay"]
i_corngrain, i_sbm = IDX["Corn grain ground"], IDX["Soybean meal 48pct CP"]

NDF_FLOOR = 0.28


def neg_iofc(x):
    return -diet_stats(x, NDF, ADF, CP, NEL, PRICE, FORAGE_MASK)["iofc_d"]


def solve(min_alfalfa):
    cons = [
        {"type": "eq", "fun": lambda x: np.sum(x) - 1.0},
        {"type": "ineq", "fun": lambda x: (CP @ x) - CP_MIN},
        {"type": "ineq", "fun": lambda x: CP_MAX - (CP @ x)},
        {"type": "ineq", "fun": lambda x: (x[i_alfalfa] + x[i_cornsil] + x[i_grasshay]) - FORAGE_MIN},
        {"type": "ineq", "fun": lambda x: FORAGE_MAX - (x[i_alfalfa] + x[i_cornsil] + x[i_grasshay])},
        {"type": "ineq", "fun": lambda x: (NDF @ x) - NDF_FLOOR},
        {"type": "ineq", "fun": lambda x: float((NDF * FORAGE_MASK) @ x) - FORAGE_NDF_MIN},
        {"type": "ineq", "fun": lambda x: CORNGRAIN_CAP - x[i_corngrain]},
        {"type": "ineq", "fun": lambda x: SBM_CAP - x[i_sbm]},
        {"type": "ineq", "fun": lambda x: SINGLE_FORAGE_CAP - x[i_cornsil]},
        {"type": "ineq", "fun": lambda x: SINGLE_FORAGE_CAP - x[i_grasshay]},
        {"type": "ineq", "fun": lambda x: x[i_alfalfa] - min_alfalfa},
    ]
    x0 = np.array([max(min_alfalfa, 0.1), 0.2, 0.1, 0.35, 0.15])
    x0 = x0 / x0.sum()
    r = minimize(neg_iofc, x0, method="SLSQP", bounds=[(0, 1)] * 5, constraints=cons,
                 options={"maxiter": 1000, "ftol": 1e-12})
    return diet_stats(r.x, NDF, ADF, CP, NEL, PRICE, FORAGE_MASK)


if __name__ == "__main__":
    rows = []
    base = solve(0.0)
    for min_alfalfa, label in [(0.0, "0% (unconstrained economic optimum)"), (0.10, "10%"),
                                (0.15, "15% (typical industry minimum)"), (0.20, "20%")]:
        s = solve(min_alfalfa)
        cost = base["iofc_cwt"] - s["iofc_cwt"]
        rows.append(dict(min_alfalfa_share=label, resulting_iofc_cwt=round(s["iofc_cwt"], 2),
                          cost_vs_unconstrained_cwt=round(cost, 2)))
        print(f"min alfalfa={label:35s}: IOFC=${s['iofc_cwt']:.2f}/cwt, cost=${cost:.2f}/cwt")

    df_out = pd.DataFrame(rows)
    df_out.to_csv(OUTPUT / "Table5_alfalfa_cost.csv", index=False)
    print(f"\nWrote {OUTPUT / 'Table5_alfalfa_cost.csv'}")
