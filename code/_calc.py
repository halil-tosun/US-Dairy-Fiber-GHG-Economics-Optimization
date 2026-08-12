"""
_calc.py -- Shared calculation functions (methane, milk, DMI, economics).

Implements the exact formulas reported in Materials and Methods of the
accompanying manuscript. Not run directly; imported by every numbered
script that needs to compute diet-level outcomes.
"""
import numpy as np
from _paths import (BW, MILK, FAT, PROT_MILK, NEM_COEF, NEL_PER_KG_MILK,
                     MILK_PRICE_CWT, MJ_PER_KG_CH4, GWP100_CH4, PREMIX_USD_PER_COW_DAY)

# ---- Fixed, diet-independent animal quantities (computed once) ----
# Energy-corrected milk (Tyrrell and Reid, 1965)
ECM = 0.327 * MILK + 12.95 * (MILK * FAT / 100) + 7.2 * (MILK * PROT_MILK / 100)

# Fat- and protein-corrected milk (Sjaunja et al., 1990; as reconsidered by Hall, 2023)
FPCM = MILK * (0.337 + 0.116 * FAT + 0.06 * PROT_MILK)

# Net energy for maintenance (NASEM, 2021)
NE_MAINTENANCE = NEM_COEF * BW ** 0.75

# Net energy for milk production (NASEM, 2021)
NE_LACTATION = MILK * NEL_PER_KG_MILK

# Milk revenue is fixed across all scenarios because milk yield/composition/price
# are held constant (see Methods, "Animal and Production Assumptions").
MILK_REVENUE_USD_PER_DAY = (MILK / 45.359237) * MILK_PRICE_CWT


def diet_stats(x, NDF, ADF, CP, NEL, PRICE, forage_mask=None):
    """
    Given a vector of DM-basis ingredient inclusion shares `x` (must sum to 1)
    and parallel ingredient-attribute arrays, return a dict of diet-level
    outcomes: composition, DMI, enteric methane, GHG intensity, feed cost, IOFC.

    Implements:
      - DMI = (NEmaintenance + NElactation) / Diet NEL density   [dilution of maintenance;
        Bauman and Currie, 1980]
      - CH4 (MJ/d) = 13.3 + 0.118*NDF - 0.130*ECM + 2.20*MF - 1.71*CP + 0.00521*BW
        [Niu et al., 2018]
      - GHG intensity (kg CO2e/kg FPCM) = CH4(kg/d) * GWP100 / FPCM
      - Feed cost ($/d) = DMI * weighted ingredient price + premix
      - IOFC = Milk revenue - Feed cost
    """
    x = np.asarray(x, dtype=float)
    ndf = float(NDF @ x)
    adf = float(ADF @ x)
    cp = float(CP @ x)
    nel = float(NEL @ x)
    price = float(PRICE @ x)

    dmi = (NE_MAINTENANCE + NE_LACTATION) / nel
    feed_cost_d = dmi * price + PREMIX_USD_PER_COW_DAY

    ch4_mj = 13.3 + 0.118 * (ndf * 100) - 0.130 * ECM + 2.20 * FAT - 1.71 * PROT_MILK + 0.00521 * BW
    ch4_kg = ch4_mj / MJ_PER_KG_CH4
    ch4_co2e_kg = ch4_kg * GWP100_CH4
    ghg_intensity = ch4_co2e_kg / FPCM

    iofc_d = MILK_REVENUE_USD_PER_DAY - feed_cost_d
    milk_cwt = MILK / 45.359237

    out = dict(
        ndf=ndf, adf=adf, hemicellulose=ndf - adf, cp=cp, nel=nel, dmi=dmi,
        ch4_mj_d=ch4_mj, ch4_kg_d=ch4_kg, ch4_co2e_kg_d=ch4_co2e_kg,
        ghg_intensity=ghg_intensity,
        feed_cost_d=feed_cost_d, feed_cost_cwt=feed_cost_d / milk_cwt,
        iofc_d=iofc_d, iofc_cwt=iofc_d / milk_cwt,
        milk_revenue_d=MILK_REVENUE_USD_PER_DAY,
    )
    if forage_mask is not None:
        out["forage_ndf"] = float((NDF * forage_mask) @ x)
    return out
