"""
04_sensitivity_analysis.py

Perturbs each ingredient price by +/-20% and the assumed milk price by
+/-10%, re-solving the optimization at both endpoints of the primary
NDF-floor sweep (28.0% and 37.2% DM) under each perturbation, to test the
robustness of the headline IOFC gap to input price uncertainty (Results,
"Sensitivity of the Headline Finding to Input Price Assumptions").

Produces output/Table4_price_sensitivity.csv.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from _paths import DATA_RAW, OUTPUT, CP_MIN, CP_MAX, FORAGE_MIN, FORAGE_MAX, \
    FORAGE_NDF_MIN, SINGLE_FORAGE_CAP, CORNGRAIN_CAP, SBM_CAP, MILK_PRICE_CWT
from _calc import diet_stats
import _calc

df = pd.read_csv(DATA_RAW / "ingredient_library.csv")
df = df[df["used_in_primary_model"]].reset_index(drop=True)
NAMES = df["ingredient"].tolist()
IDX = {n: i for i, n in enumerate(NAMES)}
NDF = df["ndf_pct_dm"].values / 100
ADF = df["adf_pct_dm"].values / 100
CP = df["cp_pct_dm"].values / 100
NEL = df["nel_mcal_kg_dm"].values
BASE_PRICE_TON = df["price_usd_per_ton_asfed"].values.copy()
DM = df["dm_pct"].values / 100
FORAGE_MASK = df["is_forage"].values.astype(bool)
i_alfalfa, i_cornsil, i_grasshay = IDX["Alfalfa haylage"], IDX["Corn silage"], IDX["Grass hay"]
i_corngrain, i_sbm = IDX["Corn grain ground"], IDX["Soybean meal 48pct CP"]


def price_per_kg_dm(price_ton):
    return price_ton / 907.185 / DM


def solve(ndf_floor, price_ton, milk_price):
    price = price_per_kg_dm(price_ton)
    old_mp = _calc.MILK_REVENUE_USD_PER_DAY
    _calc.MILK_REVENUE_USD_PER_DAY = (38.0 / 45.359237) * milk_price

    def neg_iofc(x):
        return -diet_stats(x, NDF, ADF, CP, NEL, price, FORAGE_MASK)["iofc_d"]

    def feasible(x, tol=1e-4):
        forage_tot = x[i_alfalfa] + x[i_cornsil] + x[i_grasshay]
        return all([
            abs(np.sum(x) - 1.0) < 1e-3,
            (CP @ x) >= CP_MIN - tol, (CP @ x) <= CP_MAX + tol,
            forage_tot >= FORAGE_MIN - tol, forage_tot <= FORAGE_MAX + tol,
            (NDF @ x) >= ndf_floor - tol,
            float((NDF * FORAGE_MASK) @ x) >= FORAGE_NDF_MIN - tol,
            x[i_corngrain] <= CORNGRAIN_CAP + tol, x[i_sbm] <= SBM_CAP + tol,
            x[i_alfalfa] <= SINGLE_FORAGE_CAP + tol, x[i_cornsil] <= SINGLE_FORAGE_CAP + tol,
            x[i_grasshay] <= SINGLE_FORAGE_CAP + tol, np.all(x >= -tol),
        ])

    starts = [np.array(v) for v in (
        [0.20, 0.20, 0.10, 0.35, 0.15], [0.10, 0.10, 0.30, 0.30, 0.20],
        [0.05, 0.05, 0.50, 0.25, 0.15], [0.00, 0.00, 0.55, 0.30, 0.15],
        [0.30, 0.10, 0.10, 0.30, 0.20])]
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
    best_iofc = -np.inf
    for x0 in starts:
        r = minimize(neg_iofc, x0, method="SLSQP", bounds=[(0, 1)] * 5, constraints=cons,
                      options={"maxiter": 1000, "ftol": 1e-12})
        if feasible(r.x):
            s = diet_stats(r.x, NDF, ADF, CP, NEL, price, FORAGE_MASK)
            if s["iofc_cwt"] > best_iofc:
                best_iofc = s["iofc_cwt"]
    _calc.MILK_REVENUE_USD_PER_DAY = old_mp
    return best_iofc


def gap(price_ton, milk_price):
    lo = solve(0.28, price_ton, milk_price)
    hi = solve(0.372, price_ton, milk_price)
    return lo - hi


if __name__ == "__main__":
    baseline_gap = gap(BASE_PRICE_TON, MILK_PRICE_CWT)
    print(f"Baseline IOFC gap (28.0% vs 37.2% NDF): ${baseline_gap:.2f}/cwt\n")

    rows = []
    for i, name in enumerate(NAMES):
        prices_lo, prices_hi = BASE_PRICE_TON.copy(), BASE_PRICE_TON.copy()
        prices_lo[i] *= 0.8
        prices_hi[i] *= 1.2
        g_lo = gap(prices_lo, MILK_PRICE_CWT)
        g_hi = gap(prices_hi, MILK_PRICE_CWT)
        rows.append(dict(input_perturbed=f"{name} price (+/-20%)", gap_minus20pct=round(g_lo, 2), gap_plus20pct=round(g_hi, 2)))
        print(f"{name:25s} price -20%: gap=${g_lo:.2f}   +20%: gap=${g_hi:.2f}")

    g_lo = gap(BASE_PRICE_TON, MILK_PRICE_CWT * 0.9)
    g_hi = gap(BASE_PRICE_TON, MILK_PRICE_CWT * 1.1)
    rows.append(dict(input_perturbed="Milk price (+/-10%)", gap_minus20pct=round(g_lo, 2), gap_plus20pct=round(g_hi, 2)))
    print(f"{'Milk price':25s}      -10%: gap=${g_lo:.2f}   +10%: gap=${g_hi:.2f}")

    df_out = pd.DataFrame(rows)
    df_out.to_csv(OUTPUT / "Table4_price_sensitivity.csv", index=False)
    print(f"\nWrote {OUTPUT / 'Table4_price_sensitivity.csv'}")
