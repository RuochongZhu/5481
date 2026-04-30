"""mbe_a2 — Module x Primitive Engagement Matrix.

Visualizes Table 2 of the CampusRide draft (tab:primitives) augmented with
WTP-uplift means from the formative survey (F3, F4, F5).

Rows (modules):    Carpool, Marketplace, Activities, Groups, Messages, Points
Columns (prim.):   Identity, Safety, Rating Fairness, Rewards
Cell symbol:       intensive (filled diamond x2), present (filled diamond),
                   not applicable (open ring). Drawn as patches so the figure
                   does not depend on Unicode glyph coverage in Helvetica.
Column band:       Sequential blue intensity from F3/F4 means.
Rating Fairness:   Hatched header band (not in F3); annotated F5 driver subset.
Points:            Greyed full-row band labelled "(cross-module meta-layer)".
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


@renderer("mbe_a2_module_primitive_matrix")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.colors import Normalize
    from matplotlib.cm import get_cmap

    # --- Data -------------------------------------------------------------
    modules = ["Carpool", "Marketplace", "Activities",
               "Groups", "Messages", "Points"]
    primitives = ["Identity", "Safety", "Rating\nFairness", "Rewards"]

    # 2 = intensive, 1 = present, 0 = not applicable, -1 = meta-layer cell
    # Carpool:     Identity present, Safety intensive, Rating intensive,
    #              Rewards present.
    engagement = [
        [1, 2, 2, 1],   # Carpool
        [1, 0, 1, 1],   # Marketplace (Safety deferred to future work)
        [1, 0, 0, 1],   # Activities
        [1, 0, 0, 0],   # Groups
        [1, 0, 0, 0],   # Messages
        [-1, -1, -1, -1],  # Points (meta-layer band)
    ]

    # Column WTP / F-finding intensities (0–100 scale). Keys match the
    # `primitives` strings (which include a line break for "Rating\nFairness").
    col_values = {
        "Identity": 67.3,
        "Safety": 62.7,
        "Rating\nFairness": None,
        "Rewards": 48.3,
    }
    col_annot = {
        "Identity": "F3 mean: 67.3",
        "Safety": "F3 mean: 62.7",
        "Rating\nFairness": "F5 driver (N=19): 29.1",
        "Rewards": "F4 mean: 48.3",
    }

    n_rows = len(modules)
    n_cols = len(primitives)

    # --- Figure -----------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.6, 6.4))

    # Color normalization for the column-header band.
    cmap = get_cmap("Blues")
    norm = Normalize(vmin=20, vmax=80)

    # Coordinate system: keep x in [0, n_cols], y in [band_top, n_rows + pad].
    # Aspect is NOT equal — let the figure box stretch so columns are wide
    # enough to fit two-line headers cleanly.
    band_top = -1.6
    band_bot = 0.0
    band_h = band_bot - band_top
    ax.set_xlim(-0.6, n_cols + 0.05)
    ax.set_ylim(band_top - 0.15, n_rows + 0.7)
    ax.invert_yaxis()
    # ax.set_aspect("equal")  # intentionally relaxed

    for j, prim in enumerate(primitives):
        val = col_values[prim]
        if val is None:
            patch = mpatches.Rectangle(
                (j, band_top), 1, band_h,
                facecolor="#ECECEC", edgecolor="#7F8C8D",
                hatch="////", linewidth=0.8,
            )
        else:
            patch = mpatches.Rectangle(
                (j, band_top), 1, band_h,
                facecolor=cmap(norm(val)), edgecolor="#34495E", linewidth=0.8,
            )
        ax.add_patch(patch)
        # Decide text color for legibility on the colored band.
        if val is None or val < 55:
            text_color = "#1A1A1A"
            sub_color = "#2C3E50"
        else:
            text_color = "#FFFFFF"
            sub_color = "#F8F9FA"
        ax.text(
            j + 0.5, band_top + 0.50, prim,
            ha="center", va="center", fontsize=10.8, fontweight="bold",
            color=text_color, linespacing=1.05,
        )
        ax.text(
            j + 0.5, band_top + 1.32, col_annot[prim],
            ha="center", va="center", fontsize=8.8, style="italic",
            color=sub_color,
        )

    # --- Engagement cells -------------------------------------------------
    for i, _mod in enumerate(modules):
        for j, prim in enumerate(primitives):
            val = engagement[i][j]
            x0, y0 = j, i
            if val == -1:
                # Points meta-layer: greyed band cell, no symbol.
                cell = mpatches.Rectangle(
                    (x0, y0), 1, 1,
                    facecolor="#E5E7E9", edgecolor="#BDC3C7", linewidth=0.6,
                )
                ax.add_patch(cell)
                continue

            # Light tint background echoing the column band.
            col_val = col_values[prim]
            if col_val is None:
                cell = mpatches.Rectangle(
                    (x0, y0), 1, 1,
                    facecolor="#FAFAFA", edgecolor="#BDC3C7",
                    hatch="//", linewidth=0.6, alpha=0.55,
                )
            else:
                tint = cmap(norm(col_val) * 0.45 + 0.10)
                cell = mpatches.Rectangle(
                    (x0, y0), 1, 1,
                    facecolor=tint, edgecolor="#BDC3C7", linewidth=0.6,
                    alpha=0.45,
                )
            ax.add_patch(cell)

            # Draw symbol markers (pixel-sized; aspect-independent).
            cx, cy = x0 + 0.5, y0 + 0.5
            if val == 2:
                # intensive: two filled dark diamonds side-by-side
                ax.scatter(
                    [cx - 0.18, cx + 0.18], [cy, cy],
                    s=160, marker="D",
                    facecolor="#1B4F72", edgecolor="#0E2F45", linewidth=0.8,
                    zorder=5,
                )
            elif val == 1:
                # present: single filled medium-blue diamond
                ax.scatter(
                    [cx], [cy], s=200, marker="D",
                    facecolor="#2874A6", edgecolor="#1B4F72", linewidth=0.8,
                    zorder=5,
                )
            elif val == 0:
                # not applicable: open grey circle
                ax.scatter(
                    [cx], [cy], s=200, marker="o",
                    facecolor="none", edgecolor="#7F8C8D", linewidth=1.6,
                    zorder=5,
                )

    # Single label across the Points meta-layer row.
    ax.text(
        n_cols / 2.0, n_rows - 0.5, "(cross-module meta-layer)",
        ha="center", va="center", fontsize=10.5, style="italic",
        color="#566573",
    )

    # --- Row labels -------------------------------------------------------
    for i, mod in enumerate(modules):
        if mod == "Carpool":
            ax.text(
                -0.08, i + 0.5, mod,
                ha="right", va="center", fontsize=10.8, fontweight="bold",
                color="#C0392B",
            )
            # Star marker drawn as a patch (font-independent).
            ax.scatter(
                [-0.42], [i + 0.5], s=110, marker="*",
                facecolor="#C0392B", edgecolor="#7B241C", linewidth=0.8,
                clip_on=False, zorder=6,
            )
        else:
            ax.text(
                -0.08, i + 0.5, mod,
                ha="right", va="center", fontsize=10.5, color="#1A1A1A",
            )

    # Carpool deep-dive callout: a star + caption under the matrix.
    ax.scatter(
        [n_cols / 2.0 - 1.05], [n_rows + 0.32], s=110, marker="*",
        facecolor="#C0392B", edgecolor="#7B241C", linewidth=0.8,
        clip_on=False, zorder=6,
    )
    ax.text(
        n_cols / 2.0 - 0.95, n_rows + 0.32,
        "Carpool is the deep-dive subject in §5.7",
        ha="left", va="center", fontsize=9.0, style="italic",
        color="#C0392B",
    )

    # --- Borders ----------------------------------------------------------
    outer = mpatches.Rectangle(
        (0, 0), n_cols, n_rows,
        facecolor="none", edgecolor="#34495E", linewidth=1.4,
    )
    ax.add_patch(outer)
    band_outer = mpatches.Rectangle(
        (0, band_top), n_cols, band_h,
        facecolor="none", edgecolor="#34495E", linewidth=1.0,
    )
    ax.add_patch(band_outer)

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # --- Title ------------------------------------------------------------
    ax.set_title(
        "Design-primitive engagement across CampusRide modules",
        fontsize=12.5, fontweight="bold", pad=14,
    )

    # --- Legend ----------------------------------------------------------
    # Custom legend handles using filled diamonds / open ring.
    legend_handles = [
        _DiamondHandle("#1B4F72", count=2, label="intensive engagement"),
        _DiamondHandle("#2874A6", count=1, label="present"),
        _RingHandle("#7F8C8D", label="not applicable"),
        mpatches.Patch(facecolor=cmap(norm(67)), edgecolor="#34495E",
                       label="header band: F3/F4 mean WTP (0-100)"),
        mpatches.Patch(facecolor="#ECECEC", edgecolor="#7F8C8D",
                       hatch="////", label="hatched: F5 driver subset"),
    ]
    handler_map = {
        _DiamondHandle: _DiamondHandler(),
        _RingHandle: _RingHandler(),
    }
    ax.legend(
        handles=legend_handles, handler_map=handler_map,
        loc="lower center", bbox_to_anchor=(0.5, -0.20),
        ncol=3, frameon=False, fontsize=8.8, handlelength=1.6,
        columnspacing=1.4, handletextpad=0.7,
    )

    # Footnote
    fig.text(
        0.5, 0.005,
        "Symbols from §5.1 Table 2; column-band intensities from F3/F4/F5 "
        "survey means.",
        ha="center", va="bottom", fontsize=8.6, style="italic",
        color="#566573",
    )

    plt.tight_layout(rect=(0, 0.05, 1, 1))

    pdf, png = save_mpl("mbe_a2_module_primitive_matrix")
    register("mbe_a2_module_primitive_matrix", "ok", png_path=png)


# ---------------------------------------------------------------------------
# Helpers (drawing primitives + custom legend handlers)
# ---------------------------------------------------------------------------

def _draw_diamond(ax, cx, cy, size, facecolor, edgecolor):
    import matplotlib.patches as mpatches
    pts = [(cx, cy - size), (cx + size, cy),
           (cx, cy + size), (cx - size, cy)]
    poly = mpatches.Polygon(pts, closed=True,
                            facecolor=facecolor, edgecolor=edgecolor,
                            linewidth=0.8)
    ax.add_patch(poly)


class _DiamondHandle:
    """Sentinel handle for the legend; carries color + count + label."""
    def __init__(self, color, count, label):
        self.color = color
        self.count = count
        self._label = label

    def get_label(self):
        return self._label


class _RingHandle:
    def __init__(self, color, label):
        self.color = color
        self._label = label

    def get_label(self):
        return self._label


class _DiamondHandler:
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        from matplotlib.patches import Polygon
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        w, h = handlebox.width, handlebox.height
        cy = y0 + h / 2.0
        size = min(h, w) * 0.32
        if orig_handle.count == 2:
            cxs = [x0 + w * 0.32, x0 + w * 0.68]
        else:
            cxs = [x0 + w * 0.5]
        artists = []
        for cx in cxs:
            pts = [(cx, cy - size), (cx + size, cy),
                   (cx, cy + size), (cx - size, cy)]
            p = Polygon(pts, closed=True,
                        facecolor=orig_handle.color, edgecolor="#0E2F45",
                        linewidth=0.6, transform=handlebox.get_transform())
            handlebox.add_artist(p)
            artists.append(p)
        return artists[0]


class _RingHandler:
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        from matplotlib.patches import Circle
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        w, h = handlebox.width, handlebox.height
        cx = x0 + w / 2.0
        cy = y0 + h / 2.0
        r = min(h, w) * 0.32
        ring = Circle((cx, cy), r,
                      facecolor="none", edgecolor=orig_handle.color,
                      linewidth=1.4, transform=handlebox.get_transform())
        handlebox.add_artist(ring)
        return ring
