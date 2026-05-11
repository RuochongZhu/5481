"""mbse_traceability_matrix - Requirements x Modules traceability.

A design-intent traceability matrix: each row is a CampusRide requirement
(some anchored on formative-survey findings F3/F4/F5), each column is a
delivered platform module. A filled cell means the module addresses that
requirement; the accent color marks the primary owner for that row.

Style follows scripts/_mbe_style_guide.md:
  - matplotlib imshow with categorical colors (no SQL, no file paths,
    no constants spelled out).
  - Navy fill for link cells, accent orange (#F39C12) for primary links,
    cool grey (#566573) for axis/text neutrals.
  - Title 14 bold pad=14, italic subtitle in #566573.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402
from render_mbe_figures import renderer  # noqa: E402


# Palette (per style guide)
NAVY = "#1A5276"
ACCENT = "#F39C12"
GREY = "#566573"
INK = "#1B2631"

# Columns: delivered platform modules (findings, not code).
MODULES = [
    "Carpool",
    "Marketplace",
    "Activities",
    "Groups",
    "Messages",
    "Points",
]

# Rows: requirements stated in plain English. Some carry a finding tag
# (F3 motivations, F4 willingness-to-pay, F5 driver rating-fairness)
# so the reader can trace the design back to the survey snapshot.
#
# Each row: (requirement_label, [primary_module], [secondary_modules])
REQS = [
    ("Cornell-only identity check before first session",
     ["Carpool"], ["Marketplace", "Activities", "Groups", "Messages", "Points"]),

    ("Verified-profile badge visible at booking",
     ["Carpool"], ["Marketplace", "Groups"]),

    ("Real-time trip matching for short campus hops  (F3)",
     ["Carpool"], ["Messages"]),

    ("Cost-sharing transparent to both sides  (F4)",
     ["Carpool"], ["Points"]),

    ("Driver supply incentives for long-distance routes  (F4)",
     ["Carpool"], ["Points"]),

    ("Bidirectional rating, deferred 2 hours after trip  (F5)",
     ["Carpool"], ["Messages"]),

    ("Rating remains revisable to soften driver-side asymmetry  (F5)",
     ["Carpool"], []),

    ("Trip-bound chat that expires shortly after arrival",
     ["Messages"], ["Carpool", "Groups"]),

    ("External outreach when supply is thin (WeChat post queue)",
     ["Messages"], ["Carpool"]),

    ("Cross-module points ledger as a soft reward layer",
     ["Points"], ["Carpool", "Marketplace", "Activities", "Groups"]),

    ("Campus-marketplace listings reusing the verified identity",
     ["Marketplace"], ["Messages", "Points"]),

    ("Activities sign-up with venue radius and check-in window",
     ["Activities"], ["Messages", "Points"]),

    ("Group spaces for recurring cohorts (clubs, dorms)",
     ["Groups"], ["Messages", "Points"]),
]


@renderer("mbse_traceability_matrix")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import ListedColormap, BoundaryNorm

    n_rows = len(REQS)
    n_cols = len(MODULES)

    # Encode the matrix: 0 = empty, 1 = secondary link, 2 = primary link.
    M = np.zeros((n_rows, n_cols), dtype=int)
    for i, (_, primaries, secondaries) in enumerate(REQS):
        for s in secondaries:
            M[i, MODULES.index(s)] = 1
        for p in primaries:
            M[i, MODULES.index(p)] = 2

    # Categorical colormap: white, navy, accent.
    cmap = ListedColormap(["#FFFFFF", NAVY, ACCENT])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

    fig, ax = plt.subplots(figsize=(13, 8.2))

    ax.imshow(
        M, cmap=cmap, norm=norm, aspect="auto",
        interpolation="nearest",
    )

    # Cell text and outlines.
    for i in range(n_rows):
        for j in range(n_cols):
            v = M[i, j]
            # Light grid outline on every cell
            ax.add_patch(plt.Rectangle(
                (j - 0.5, i - 0.5), 1, 1,
                fill=False, edgecolor="#D5DBDB", linewidth=0.6,
            ))
            if v == 2:
                ax.text(j, i, "primary",
                        ha="center", va="center",
                        fontsize=8.5, fontweight="bold",
                        color="white")
            elif v == 1:
                ax.text(j, i, "supports",
                        ha="center", va="center",
                        fontsize=8.5, color="white")

    # Axis labels in plain English.
    ax.set_xticks(range(n_cols))
    ax.set_xticklabels(MODULES, fontsize=10.5, color=INK,
                       rotation=30, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels([r[0] for r in REQS], fontsize=10, color=INK)

    # Soften the axis spines and ticks to grey.
    for spine in ax.spines.values():
        spine.set_color(GREY)
        spine.set_linewidth(0.8)
    ax.tick_params(colors=GREY, length=0)

    # Title + italic subtitle (design intent).
    fig.suptitle(
        "Requirements traceability across CampusRide modules",
        fontsize=14, fontweight="bold", color=INK, y=0.97,
    )
    fig.text(
        0.5, 0.925,
        "Each requirement is owned by one module (accent) and supported "
        "by neighbours; survey findings F3, F4, F5 anchor the design intent.",
        ha="center", va="center", fontsize=10, style="italic", color=GREY,
    )

    # Legend strip below the matrix.
    legend_ax = fig.add_axes([0.13, 0.02, 0.74, 0.05])
    legend_ax.set_xlim(0, 10)
    legend_ax.set_ylim(0, 1)
    legend_ax.axis("off")

    # primary swatch
    legend_ax.add_patch(plt.Rectangle((0.0, 0.2), 0.6, 0.6,
                                      facecolor=ACCENT, edgecolor="none"))
    legend_ax.text(0.75, 0.5, "primary owner",
                   ha="left", va="center", fontsize=10, color=INK)

    # supports swatch
    legend_ax.add_patch(plt.Rectangle((3.0, 0.2), 0.6, 0.6,
                                      facecolor=NAVY, edgecolor="none"))
    legend_ax.text(3.75, 0.5, "supports the requirement",
                   ha="left", va="center", fontsize=10, color=INK)

    # finding-tag note
    legend_ax.text(
        7.0, 0.5,
        "F3, F4, F5 = formative-survey findings",
        ha="left", va="center", fontsize=10, style="italic", color=GREY,
    )

    plt.subplots_adjust(left=0.34, right=0.97, top=0.88, bottom=0.13)

    pdf, png = save_mpl("mbse_traceability_matrix", dpi=300)
    register("mbse_traceability_matrix", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
