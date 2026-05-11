"""mbse_verification_matrix - Requirements x Verification methods matrix.

A V-model verification cross-reference: each row is a requirement (in plain
English) and each column is a verification method (Test / Inspection /
Analysis / Demonstration). Cell color encodes verification status (planned,
in-progress, done, deferred). Snapshot status (e.g., "0 of N done in
production") are findings, not implementation notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402
from render_mbe_figures import renderer  # noqa: E402


HEADER_NAVY = "#1A5276"
ACCENT = "#F39C12"          # in-progress
DONE_GREEN = "#1E8449"
DEFERRED_GREY = "#566573"
PLANNED_BLUE = "#2980B9"
GRID_GREY = "#BDC3C7"
SUBTITLE_GREY = "#566573"


@renderer("mbse_verification_matrix")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyBboxPatch

    # ------------------------------------------------------------------
    # Verification status palette (cell colors)
    # ------------------------------------------------------------------
    # Each entry: (fill, text-color, glyph)
    STATUS = {
        "done":         (DONE_GREEN,    "#FFFFFF", "done"),
        "in-progress":  (ACCENT,        "#FFFFFF", "in progress"),
        "planned":      (PLANNED_BLUE,  "#FFFFFF", "planned"),
        "deferred":     (DEFERRED_GREY, "#FFFFFF", "deferred"),
    }

    # ------------------------------------------------------------------
    # Rows: requirements in plain English
    # Columns: verification methods
    # Cell value: status key (or None for not-applicable)
    # ------------------------------------------------------------------
    methods = ["Test", "Inspection", "Analysis", "Demonstration"]

    # (requirement label, [status per method])
    rows = [
        ("Cornell email check",
         ["done", "done", None, "planned"]),
        ("Guest read-only access",
         ["done", "done", None, "planned"]),
        ("Trip lifecycle (open to full to completed)",
         ["done", "done", "in-progress", "planned"]),
        ("Booking fan-out and notifications",
         ["done", "done", "in-progress", "planned"]),
        ("Venue radius (~100 m) and check-in window",
         ["done", "done", "done", "planned"]),
        ("Bidirectional rating with 2-hour delay",
         ["done", "in-progress", "in-progress", "planned"]),
        ("Recompute average rating on submit",
         ["done", "done", "in-progress", "planned"]),
        ("Cold-DM gating (reply required)",
         ["done", "done", None, "planned"]),
        ("Trip-bound chat (expires 1 h after trip)",
         ["done", "done", None, "planned"]),
        ("WeChat post queue for outreach",
         ["done", "done", None, "deferred"]),
        ("Group membership idempotency",
         ["done", "done", None, "deferred"]),
        ("Points ledger and atomic balance",
         ["done", "in-progress", "in-progress", "planned"]),
    ]

    n_rows = len(rows)
    n_cols = len(methods)

    # ------------------------------------------------------------------
    # Figure layout
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(13.5, 8.0))

    # Geometry (data coords). We keep generous margins for labels.
    LABEL_W = 5.6                    # row-label column width
    CELL_W = 1.9                     # method cell width
    HEADER_H = 0.85
    ROW_H = 0.55

    x0_label = 0.0
    x0_matrix = x0_label + LABEL_W
    x1_matrix = x0_matrix + CELL_W * n_cols

    y_top = HEADER_H + ROW_H * n_rows
    y_header_bot = ROW_H * n_rows
    y_bot = 0.0

    # ------------------------------------------------------------------
    # Header band: row-label column header
    # ------------------------------------------------------------------
    ax.add_patch(Rectangle(
        (x0_label, y_header_bot), LABEL_W, HEADER_H,
        facecolor=HEADER_NAVY, edgecolor=HEADER_NAVY, linewidth=0.0,
    ))
    ax.text(
        x0_label + 0.18, y_header_bot + HEADER_H / 2.0,
        "Requirement",
        ha="left", va="center",
        fontsize=11, fontweight="bold", color="#FFFFFF",
    )

    # Method column headers
    for j, m in enumerate(methods):
        x0 = x0_matrix + j * CELL_W
        ax.add_patch(Rectangle(
            (x0, y_header_bot), CELL_W, HEADER_H,
            facecolor=HEADER_NAVY, edgecolor="#FFFFFF", linewidth=1.0,
        ))
        ax.text(
            x0 + CELL_W / 2.0, y_header_bot + HEADER_H / 2.0,
            m,
            ha="center", va="center",
            fontsize=10.5, fontweight="bold", color="#FFFFFF",
        )

    # ------------------------------------------------------------------
    # Body cells
    # ------------------------------------------------------------------
    for i, (label, statuses) in enumerate(rows):
        # Row index 0 is the top row visually; flip via y-coordinate.
        y_row_bot = y_header_bot - (i + 1) * ROW_H

        # Row label cell (light alternating background)
        zebra = "#FFFFFF" if (i % 2 == 0) else "#F4F6F7"
        ax.add_patch(Rectangle(
            (x0_label, y_row_bot), LABEL_W, ROW_H,
            facecolor=zebra, edgecolor=GRID_GREY, linewidth=0.6,
        ))
        ax.text(
            x0_label + 0.18, y_row_bot + ROW_H / 2.0,
            label,
            ha="left", va="center",
            fontsize=9.5, color="#1B2631",
        )

        # Method cells
        for j, status in enumerate(statuses):
            x0 = x0_matrix + j * CELL_W
            if status is None:
                # Not applicable: light hatched grey with em-dash
                ax.add_patch(Rectangle(
                    (x0, y_row_bot), CELL_W, ROW_H,
                    facecolor="#ECF0F1", edgecolor=GRID_GREY, linewidth=0.6,
                ))
                ax.text(
                    x0 + CELL_W / 2.0, y_row_bot + ROW_H / 2.0,
                    "n/a",
                    ha="center", va="center", fontsize=9,
                    color=DEFERRED_GREY, style="italic",
                )
                continue
            fill, txt_color, glyph = STATUS[status]
            # Background tile
            ax.add_patch(Rectangle(
                (x0, y_row_bot), CELL_W, ROW_H,
                facecolor=zebra, edgecolor=GRID_GREY, linewidth=0.6,
            ))
            # Inner rounded badge with status color
            pad_x = 0.08
            pad_y = 0.07
            ax.add_patch(FancyBboxPatch(
                (x0 + pad_x, y_row_bot + pad_y),
                CELL_W - 2 * pad_x, ROW_H - 2 * pad_y,
                boxstyle="round,pad=0.02,rounding_size=0.06",
                facecolor=fill, edgecolor=fill, linewidth=1.0,
            ))
            ax.text(
                x0 + CELL_W / 2.0, y_row_bot + ROW_H / 2.0,
                glyph,
                ha="center", va="center",
                fontsize=9.2, fontweight="bold", color=txt_color,
            )

    # Outer border around the whole table
    ax.add_patch(Rectangle(
        (x0_label, y_bot), x1_matrix - x0_label, y_top - y_bot,
        facecolor="none", edgecolor=DEFERRED_GREY, linewidth=1.2,
    ))

    # ------------------------------------------------------------------
    # Legend strip (status swatches) — placed below the table
    # ------------------------------------------------------------------
    legend_y = y_bot - 0.95
    legend_x = x0_label
    swatch_w = 0.50
    swatch_h = 0.40
    label_gap = 0.10        # space between swatch and its label
    label_width = 1.35      # reserved horizontal space for label text
    item_gap = 0.20         # space between (swatch+label) groups

    legend_order = ["done", "in-progress", "planned", "deferred"]
    cursor = legend_x
    for key in legend_order:
        fill, txt_color, glyph = STATUS[key]
        ax.add_patch(FancyBboxPatch(
            (cursor, legend_y), swatch_w, swatch_h,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=fill, edgecolor=fill, linewidth=1.0,
        ))
        ax.text(
            cursor + swatch_w + label_gap, legend_y + swatch_h / 2.0,
            glyph,
            ha="left", va="center",
            fontsize=9.5, color="#1B2631",
        )
        cursor += swatch_w + label_gap + label_width + item_gap

    # n/a swatch
    ax.add_patch(Rectangle(
        (cursor, legend_y + 0.04), swatch_w, swatch_h - 0.08,
        facecolor="#ECF0F1", edgecolor=GRID_GREY, linewidth=0.8,
    ))
    ax.text(
        cursor + swatch_w + label_gap, legend_y + swatch_h / 2.0,
        "not applicable",
        ha="left", va="center",
        fontsize=9.5, color="#1B2631",
    )

    # ------------------------------------------------------------------
    # Snapshot finding (its own line below the legend)
    # ------------------------------------------------------------------
    finding_y = legend_y - 0.55
    ax.text(
        x0_label, finding_y,
        "Snapshot: 0 of 12 requirements have completed full demonstration "
        "in production.",
        ha="left", va="center",
        fontsize=9.5, style="italic", color=SUBTITLE_GREY,
    )

    # ------------------------------------------------------------------
    # Title + italic subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Verification matrix - requirements covered by each method",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (x0_label + x1_matrix) / 2.0, y_top + 0.30,
        "Most requirements are covered by Test and Inspection today; "
        "Demonstration in production is intentionally deferred.",
        ha="center", va="bottom",
        fontsize=10, style="italic", color=SUBTITLE_GREY,
    )

    # ------------------------------------------------------------------
    # Axes cosmetics
    # ------------------------------------------------------------------
    ax.set_xlim(x0_label - 0.3, x1_matrix + 0.3)
    ax.set_ylim(finding_y - 0.6, y_top + 0.95)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbse_verification_matrix", dpi=300)
    register("mbse_verification_matrix", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
