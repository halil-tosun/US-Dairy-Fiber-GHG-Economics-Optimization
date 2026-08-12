"""
07_make_figures.py

Generates Figure 1 (efficient frontier: IOFC vs. GHG intensity) and
Figure 2 (cost-minimizing diet composition across the NDF floor sweep)
from data/processed/frontier_5ingredient.json (produced by
02_diet_optimization.py). Both figures are saved at 300 DPI.
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _paths import DATA_PROCESSED, FIGURES

with open(DATA_PROCESSED / "frontier_5ingredient.json") as fh:
    frontier = json.load(fh)

ghg = [f["ghg_intensity"] for f in frontier]
iofc = [f["iofc_cwt"] for f in frontier]
ndf = [f["ndf_floor"] * 100 for f in frontier]

BLUE = "#1b6ca8"
ORANGE = "#d9782d"

# ---- Figure 1: Efficient frontier ----
fig, ax = plt.subplots(figsize=(6.5, 5), dpi=300)
ax.plot(ghg, iofc, marker="o", color=BLUE, linewidth=1.6, markersize=6,
        markerfacecolor="white", markeredgewidth=1.6, markeredgecolor=BLUE, zorder=3)

ax.annotate("28.0% NDF\n(nutritional optimum)", xy=(ghg[0], iofc[0]),
            xytext=(ghg[0] + 0.0004, iofc[0] + 0.10), fontsize=8, color="#333333")
idx32 = ndf.index(32.2)
ax.annotate("32.2% NDF\n(intermediate reference)", xy=(ghg[idx32], iofc[idx32]),
            xytext=(ghg[idx32] - 0.006, iofc[idx32] + 0.14), fontsize=8, color="#333333")
ax.scatter([ghg[idx32]], [iofc[idx32]], color=ORANGE, s=55, zorder=5, edgecolor="white", linewidth=0.8)
ax.annotate("37.2% NDF\n(upper end of plausible\ncommercial range)", xy=(ghg[-1], iofc[-1]),
            xytext=(ghg[-1] - 0.011, iofc[-1] + 0.20), fontsize=8, color="#333333")
ax.scatter([ghg[-1]], [iofc[-1]], color=ORANGE, s=55, zorder=5, edgecolor="white", linewidth=0.8)

ax.set_xlabel("GHG emission intensity (kg CO2e / kg FPCM)", fontsize=10)
ax.set_ylabel("Income over feed cost ($/cwt)", fontsize=10)
ax.set_ylim(14.0, 14.85)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=9)
ax.grid(True, linewidth=0.4, alpha=0.4, color="#cccccc")
plt.tight_layout()
plt.savefig(FIGURES / "Figure1_frontier.png", dpi=300)
plt.close()
print(f"Wrote {FIGURES / 'Figure1_frontier.png'}")

# ---- Figure 2: Diet composition across the frontier ----
cornsil = [f["share_Corn silage"] * 100 for f in frontier]
grasshay = [f["share_Grass hay"] * 100 for f in frontier]
corngrain = [f["share_Corn grain ground"] * 100 for f in frontier]
sbm = [f["share_Soybean meal 48pct CP"] * 100 for f in frontier]

fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
colors = ["#1b6ca8", "#5fa8d3", "#d9782d", "#f2c288"]
ax.stackplot(ndf, cornsil, grasshay, corngrain, sbm,
             labels=["Corn silage", "Grass hay", "Corn grain", "Soybean meal"],
             colors=colors, edgecolor="white", linewidth=0.7)
ax.axvline(x=34.5, color="#333333", linestyle="--", linewidth=0.9)
ax.annotate("Corn silage share\nbegins to decline", xy=(34.5, 90), xytext=(35.1, 90),
            fontsize=8, color="#333333")
ax.set_xlabel("Dietary NDF floor (% DM)", fontsize=10)
ax.set_ylabel("Ingredient inclusion (% of diet DM)", fontsize=10)
ax.set_xlim(28, 37.2)
ax.set_ylim(0, 100)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=4, fontsize=8, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=9)
plt.tight_layout()
plt.savefig(FIGURES / "Figure2_composition.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"Wrote {FIGURES / 'Figure2_composition.png'}")
