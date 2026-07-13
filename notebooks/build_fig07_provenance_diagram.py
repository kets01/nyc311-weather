"""Builds figures/fig_07_provenance_chain.png.

Not a numbered analysis notebook (00-05) because it documents the pipeline rather than
being an output of it (see docs/FAIR_and_provenance.md). Kept as a committed script,
unlike the one-off _build_NN_*.py scripts used to scaffold the notebooks themselves,
because this figure has no other code in the repo that reproduces it.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(14.2, 3.4))
ax.set_xlim(0, 14.2)
ax.set_ylim(0, 3.4)
ax.axis("off")

boxes = [
    ("NYC Open Data portal\n(erm2-nwe9)\n+\nNOAA NCEI portal\n(USW00094728)",
     "entity", 0.3, "Source portals\n(external, public)"),
    ("Raw CSVs\ndata/raw/*.csv\n\nvia 00_download.ipynb",
     "activity", 3.0, "Download\n(Socrata + NCEI APIs)"),
    ("Clean CSVs\n311_clean.csv\nweather_clean.csv\n\nvia 04_integrate.ipynb",
     "activity", 6.0, "Clean\n(parse, dedupe, map categories)"),
    ("Joined table\nanalysis_daily.csv\n\nvia 04_integrate.ipynb",
     "entity", 9.0, "Aggregate + join\n(day x category grain)"),
    ("figures/\nfig_01_requests_vs_tmax.png\n\nvia 05_analysis.ipynb",
     "entity", 11.7, "Plot\n(H1 figure)"),
]

box_w, box_h = 2.0, 1.7
y0 = 1.5

for i, (label, kind, x, caption) in enumerate(boxes):
    color = "#cfe8ff" if kind == "entity" else "#ffe9b3"
    rect = mpatches.FancyBboxPatch(
        (x, y0 - box_h / 2), box_w, box_h,
        boxstyle="round,pad=0.05,rounding_size=0.08",
        linewidth=1.2, edgecolor="#333333", facecolor=color,
    )
    ax.add_patch(rect)
    ax.text(x + box_w / 2, y0, label, ha="center", va="center", fontsize=7.6)
    ax.text(x + box_w / 2, y0 + box_h / 2 + 0.35, caption, ha="center", va="center",
            fontsize=7.6, style="italic", color="#444444")
    if i < len(boxes) - 1:
        next_x = boxes[i + 1][2]
        ax.annotate("", xy=(next_x - 0.05, y0), xytext=(x + box_w + 0.05, y0),
                    arrowprops=dict(arrowstyle="->", lw=1.4, color="#333333"))

entity_patch = mpatches.Patch(color="#cfe8ff", label="entity (W3C PROV)")
activity_patch = mpatches.Patch(color="#ffe9b3", label="activity (W3C PROV)")
ax.legend(handles=[entity_patch, activity_patch], loc="lower center",
          bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=False, fontsize=8)

ax.set_title(
    "Provenance chain for fig_01_requests_vs_tmax.png "
    "(agent throughout: kemki)",
    fontsize=9.5, pad=14,
)

plt.tight_layout()
plt.savefig("../figures/fig_07_provenance_chain.png", dpi=300, bbox_inches="tight")
print("saved figures/fig_07_provenance_chain.png")
