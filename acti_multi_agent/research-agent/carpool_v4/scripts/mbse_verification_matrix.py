"""mbse_verification_matrix - Test-Procedure x Originating-Requirement matrix.

Classical V-model verification cross-reference table (TP rows x OR columns).
The OR-id pattern (OR.1, OR.3, OR.5, OR.11, OR.13, OR.16, OR.18, OR.20, OR.22,
OR.25) is preserved from the reference image for visual continuity, but each
maps to a real EC requirement enumerated in §5.16 HoQ of the v4.4 draft.

Cell encoding:
  - 'x' on the diagonal  -> light-blue verified cell
  - blank otherwise       -> white cell
  - TP.11 / TP.12 may add multi-cell coverage (inspection / E2E)
Right-margin columns: Verification Method, Status (Deployed/Pending color-coded).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


CELL_VERIFIED = "#D6EAF8"       # light-blue verified cell
CELL_BLANK = "#FFFFFF"
CELL_DIAG_BORDER = "#1F618D"
HEADER_FILL = "#1A2E44"
HEADER_TEXT = "#FFFFFF"
ZEBRA_A = "#F4F6F7"
ZEBRA_B = "#FFFFFF"

STATUS_COLORS = {
    "Deployed": ("#27AE60", "#FFFFFF"),
    "Deployed (no live data)": ("#52BE80", "#FFFFFF"),
    "Pending": ("#C0392B", "#FFFFFF"),
}

METHOD_COLORS = {
    "Test": ("#D5F5E3", "#1E8449"),
    "Inspection": ("#FCF3CF", "#9A7D0A"),
    "Demo": ("#FADBD8", "#922B21"),
    "Analysis": ("#D6EAF8", "#1F618D"),
}


@renderer("mbse_verification_matrix")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    # --- Data -------------------------------------------------------------
    or_columns = [
        ("OR.1", "EC1\n.edu Identity"),
        ("OR.3", "EC2\nJWT auth"),
        ("OR.5", "EC3\nRide state\nmachine"),
        ("OR.11", "EC4\n2h rating\ndelay"),
        ("OR.13", "EC5\nBidir.\nratings"),
        ("OR.16", "EC6\nRatings\nrecompute"),
        ("OR.18", "EC7\nUpdate-in-\nplace"),
        ("OR.20", "EC8\nRide-scoped\nchat"),
        ("OR.22", "EC9\nWeChat\noutreach"),
        ("OR.25", "EC10\nPoints\nledger"),
    ]
    n_or = len(or_columns)

    # (TP-id, description, [verified col indices], method, status)
    tps = [
        ("TP.1",  "Cornell.edu domain regex unit test",
         [0], "Test", "Deployed"),
        ("TP.2",  "Resend email send integration test",
         [1], "Test", "Deployed"),
        ("TP.3",  "ride.status state-machine assertion (active->full->completed)",
         [2], "Test", "Deployed"),
        ("TP.4",  "bookRide notification fan-out count assertion (5+2=7)",
         [3], "Test", "Deployed"),
        ("TP.5",  "Haversine within 100m unit test",
         [4], "Test", "Deployed"),
        ("TP.6",  "ratings UPSERT idempotent test",
         [5], "Test", "Deployed (no live data)"),
        ("TP.7",  "REPLY_REQUIRED HTTP 403 cold-DM test",
         [6], "Test", "Deployed"),
        ("TP.8",  "wxgroup_notice_record insert test on createRide",
         [7], "Test", "Deployed"),
        ("TP.9",  "group_members idempotent on 23505 test",
         [8], "Test", "Deployed"),
        ("TP.10", "users.avg_rating recompute trigger test",
         [9], "Test", "Deployed"),
        ("TP.11", "Manual review snapshot 2026-04-23 (multi-EC inspection)",
         [0, 1, 2, 3, 7, 9], "Inspection", "Deployed"),
        ("TP.12", "E2E happy-path browser test (TBD)",
         [0, 2, 3, 4, 7], "Demo", "Pending"),
    ]
    n_tp = len(tps)

    # --- Layout ----------------------------------------------------------
    # Column widths (axes-fraction). Left label + n_or matrix cols
    # + Verification Method + Status.
    left_w = 0.07         # TP-id
    desc_w = 0.26         # TP description
    cell_w = 0.034        # one OR cell
    matrix_w = cell_w * n_or
    method_w = 0.075
    status_w = 0.115
    total_w = left_w + desc_w + matrix_w + method_w + status_w
    # Re-normalize to fit 1.0.
    scale = 1.0 / total_w
    left_w *= scale
    desc_w *= scale
    cell_w *= scale
    matrix_w *= scale
    method_w *= scale
    status_w *= scale

    col_x = [0.0,
             left_w,
             left_w + desc_w]
    for k in range(n_or):
        col_x.append(col_x[-1] + cell_w)
    col_x.append(col_x[-1] + method_w)  # method end
    col_x.append(col_x[-1] + status_w)  # status end (== 1.0)

    # --- Figure ----------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 9))

    # Vertical layout bands (axes-fraction).
    title_band_top = 1.0
    subtitle_y = 0.965
    table_top = 0.92
    legend_band_top = 0.07
    legend_y = 0.015

    header_h = 0.13
    header_top = table_top
    header_bot = header_top - header_h
    body_top = header_bot
    body_bot = legend_band_top
    row_h = (body_top - body_bot) / n_tp

    # Title.
    ax.text(
        0.5, title_band_top - 0.005,
        "Verification Matrix - CampusRide v4.4 Test Procedures x Originating Requirements",
        ha="center", va="top", fontsize=15, fontweight="bold",
        color="#1A1A1A", transform=ax.transAxes,
    )
    ax.text(
        0.5, subtitle_y,
        "Originating Requirements OR.1..OR.25 map to §5.16 HoQ engineering "
        "characteristics EC1..EC10. Diagonal 'x' = primary verification.",
        ha="center", va="top", fontsize=9.6, style="italic",
        color="#566573", transform=ax.transAxes,
    )

    # Header row -------------------------------------------------------------

    # Header backgrounds.
    # 1) TP-id header
    ax.add_patch(mpatches.Rectangle(
        (col_x[0], header_bot), col_x[1] - col_x[0], header_h,
        facecolor=HEADER_FILL, edgecolor="#0E1B2A", linewidth=0.9,
        transform=ax.transAxes,
    ))
    ax.text(
        (col_x[0] + col_x[1]) / 2.0, header_bot + header_h / 2.0,
        "Test\nProc.",
        ha="center", va="center", fontsize=10.4, fontweight="bold",
        color=HEADER_TEXT, transform=ax.transAxes, linespacing=1.1,
    )

    # 2) Description header
    ax.add_patch(mpatches.Rectangle(
        (col_x[1], header_bot), col_x[2] - col_x[1], header_h,
        facecolor=HEADER_FILL, edgecolor="#0E1B2A", linewidth=0.9,
        transform=ax.transAxes,
    ))
    ax.text(
        (col_x[1] + col_x[2]) / 2.0, header_bot + header_h / 2.0,
        "Test Procedure",
        ha="center", va="center", fontsize=10.4, fontweight="bold",
        color=HEADER_TEXT, transform=ax.transAxes,
    )

    # 3) OR column headers: 2-line label, OR-id top + EC label below
    for k, (or_id, ec_label) in enumerate(or_columns):
        x0 = col_x[2 + k]
        x1 = col_x[2 + k + 1]
        ax.add_patch(mpatches.Rectangle(
            (x0, header_bot), x1 - x0, header_h,
            facecolor=HEADER_FILL, edgecolor="#0E1B2A", linewidth=0.7,
            transform=ax.transAxes,
        ))
        # OR-id band (top portion)
        id_band_h = 0.038
        ax.add_patch(mpatches.Rectangle(
            (x0, header_top - id_band_h), x1 - x0, id_band_h,
            facecolor="#5DADE2", edgecolor="#1F618D", linewidth=0.5,
            transform=ax.transAxes,
        ))
        ax.text(
            (x0 + x1) / 2.0, header_top - id_band_h / 2.0,
            or_id,
            ha="center", va="center", fontsize=9.2, fontweight="bold",
            color="#0E1B2A", transform=ax.transAxes,
        )
        # EC label (lower portion)
        ax.text(
            (x0 + x1) / 2.0,
            header_bot + (header_h - id_band_h) / 2.0,
            ec_label,
            ha="center", va="center", fontsize=7.6, fontweight="bold",
            color=HEADER_TEXT, transform=ax.transAxes, linespacing=1.05,
        )

    # 4) Method header
    mx0 = col_x[2 + n_or]
    mx1 = col_x[2 + n_or + 1]
    ax.add_patch(mpatches.Rectangle(
        (mx0, header_bot), mx1 - mx0, header_h,
        facecolor=HEADER_FILL, edgecolor="#0E1B2A", linewidth=0.9,
        transform=ax.transAxes,
    ))
    ax.text(
        (mx0 + mx1) / 2.0, header_bot + header_h / 2.0,
        "Verification\nMethod",
        ha="center", va="center", fontsize=10.0, fontweight="bold",
        color=HEADER_TEXT, transform=ax.transAxes, linespacing=1.1,
    )

    # 5) Status header
    sx0 = col_x[2 + n_or + 1]
    sx1 = col_x[2 + n_or + 2]
    ax.add_patch(mpatches.Rectangle(
        (sx0, header_bot), sx1 - sx0, header_h,
        facecolor=HEADER_FILL, edgecolor="#0E1B2A", linewidth=0.9,
        transform=ax.transAxes,
    ))
    ax.text(
        (sx0 + sx1) / 2.0, header_bot + header_h / 2.0,
        "Status",
        ha="center", va="center", fontsize=10.4, fontweight="bold",
        color=HEADER_TEXT, transform=ax.transAxes,
    )

    # --- Body rows -----------------------------------------------------------
    for i, (tp_id, desc, verified_cols, method, status) in enumerate(tps):
        y_top = header_bot - i * row_h
        y_bot = y_top - row_h
        zebra = ZEBRA_A if (i % 2 == 0) else ZEBRA_B

        # TP id cell
        ax.add_patch(mpatches.Rectangle(
            (col_x[0], y_bot), col_x[1] - col_x[0], row_h,
            facecolor="#EAECEE", edgecolor="#BDC3C7", linewidth=0.5,
            transform=ax.transAxes,
        ))
        ax.text(
            (col_x[0] + col_x[1]) / 2.0, y_bot + row_h / 2.0,
            tp_id,
            ha="center", va="center", fontsize=10.0, fontweight="bold",
            color="#1A1A1A", transform=ax.transAxes,
        )

        # Description cell (left aligned)
        ax.add_patch(mpatches.Rectangle(
            (col_x[1], y_bot), col_x[2] - col_x[1], row_h,
            facecolor=zebra, edgecolor="#BDC3C7", linewidth=0.5,
            transform=ax.transAxes,
        ))
        ax.text(
            col_x[1] + 0.006, y_bot + row_h / 2.0,
            desc,
            ha="left", va="center", fontsize=8.4,
            color="#1A1A1A", transform=ax.transAxes,
        )

        # OR matrix cells
        for k in range(n_or):
            x0 = col_x[2 + k]
            x1 = col_x[2 + k + 1]
            verified = (k in verified_cols)
            facecolor = CELL_VERIFIED if verified else CELL_BLANK
            ax.add_patch(mpatches.Rectangle(
                (x0, y_bot), x1 - x0, row_h,
                facecolor=facecolor, edgecolor="#BDC3C7", linewidth=0.5,
                transform=ax.transAxes,
            ))
            if verified:
                # Mark with bold 'x'.
                ax.text(
                    (x0 + x1) / 2.0, y_bot + row_h / 2.0,
                    "x",
                    ha="center", va="center", fontsize=12.5,
                    fontweight="bold", color=CELL_DIAG_BORDER,
                    transform=ax.transAxes,
                )

        # Method cell - colored swatch
        m_bg, m_fg = METHOD_COLORS.get(method, ("#ECF0F1", "#1A1A1A"))
        ax.add_patch(mpatches.Rectangle(
            (mx0, y_bot), mx1 - mx0, row_h,
            facecolor=zebra, edgecolor="#BDC3C7", linewidth=0.5,
            transform=ax.transAxes,
        ))
        pad_x = 0.005
        pad_y = row_h * 0.22
        method_badge = mpatches.FancyBboxPatch(
            (mx0 + pad_x, y_bot + pad_y),
            (mx1 - mx0) - 2 * pad_x, row_h - 2 * pad_y,
            boxstyle="round,pad=0.0,rounding_size=0.010",
            facecolor=m_bg, edgecolor=m_fg, linewidth=0.7,
            transform=ax.transAxes,
        )
        ax.add_patch(method_badge)
        ax.text(
            (mx0 + mx1) / 2.0, y_bot + row_h / 2.0,
            method,
            ha="center", va="center", fontsize=9.0, fontweight="bold",
            color=m_fg, transform=ax.transAxes,
        )

        # Status cell - colored badge
        s_bg, s_fg = STATUS_COLORS.get(status, ("#BDC3C7", "#1A1A1A"))
        ax.add_patch(mpatches.Rectangle(
            (sx0, y_bot), sx1 - sx0, row_h,
            facecolor=zebra, edgecolor="#BDC3C7", linewidth=0.5,
            transform=ax.transAxes,
        ))
        pad_x = 0.005
        pad_y = row_h * 0.22
        status_badge = mpatches.FancyBboxPatch(
            (sx0 + pad_x, y_bot + pad_y),
            (sx1 - sx0) - 2 * pad_x, row_h - 2 * pad_y,
            boxstyle="round,pad=0.0,rounding_size=0.010",
            facecolor=s_bg, edgecolor="#1A1A1A", linewidth=0.6,
            transform=ax.transAxes,
        )
        ax.add_patch(status_badge)
        ax.text(
            (sx0 + sx1) / 2.0, y_bot + row_h / 2.0,
            status,
            ha="center", va="center", fontsize=8.4, fontweight="bold",
            color=s_fg, transform=ax.transAxes,
        )

    # Outer frame around the whole table.
    outer = mpatches.Rectangle(
        (0, body_bot), 1.0, header_h + n_tp * row_h,
        facecolor="none", edgecolor="#1A1A1A", linewidth=1.4,
        transform=ax.transAxes,
    )
    ax.add_patch(outer)

    # --- Legend strip ----------------------------------------------------
    # Cell legend
    ax.text(
        0.005, legend_y + 0.018, "Cell:",
        ha="left", va="center", fontsize=9.0, fontweight="bold",
        color="#1A1A1A", transform=ax.transAxes,
    )
    cx = 0.045
    # verified swatch
    sw = mpatches.Rectangle(
        (cx, legend_y), 0.022, 0.030,
        facecolor=CELL_VERIFIED, edgecolor="#7F8C8D", linewidth=0.5,
        transform=ax.transAxes,
    )
    ax.add_patch(sw)
    ax.text(cx + 0.011, legend_y + 0.015, "x",
            ha="center", va="center", fontsize=10, fontweight="bold",
            color=CELL_DIAG_BORDER, transform=ax.transAxes)
    ax.text(cx + 0.026, legend_y + 0.015, "verified by TP",
            ha="left", va="center", fontsize=8.4, color="#1A1A1A",
            transform=ax.transAxes)

    cx2 = cx + 0.135
    sw2 = mpatches.Rectangle(
        (cx2, legend_y), 0.022, 0.030,
        facecolor=CELL_BLANK, edgecolor="#7F8C8D", linewidth=0.5,
        transform=ax.transAxes,
    )
    ax.add_patch(sw2)
    ax.text(cx2 + 0.026, legend_y + 0.015, "not addressed",
            ha="left", va="center", fontsize=8.4, color="#1A1A1A",
            transform=ax.transAxes)

    # Method legend
    mx = cx2 + 0.150
    ax.text(mx, legend_y + 0.018, "Method:",
            ha="left", va="center", fontsize=9.0, fontweight="bold",
            color="#1A1A1A", transform=ax.transAxes)
    mx += 0.055
    for label in ["Test", "Inspection", "Demo", "Analysis"]:
        bg, fg = METHOD_COLORS[label]
        bw = 0.075
        badge = mpatches.FancyBboxPatch(
            (mx, legend_y + 0.002), bw, 0.026,
            boxstyle="round,pad=0.0,rounding_size=0.010",
            facecolor=bg, edgecolor=fg, linewidth=0.6,
            transform=ax.transAxes,
        )
        ax.add_patch(badge)
        ax.text(mx + bw / 2.0, legend_y + 0.015, label,
                ha="center", va="center", fontsize=8.0, fontweight="bold",
                color=fg, transform=ax.transAxes)
        mx += bw + 0.006

    # Status legend
    sx = mx + 0.020
    ax.text(sx, legend_y + 0.018, "Status:",
            ha="left", va="center", fontsize=9.0, fontweight="bold",
            color="#1A1A1A", transform=ax.transAxes)
    sx += 0.045
    for label in ["Deployed", "Pending"]:
        bg, fg = STATUS_COLORS[label]
        bw = 0.075
        badge = mpatches.FancyBboxPatch(
            (sx, legend_y + 0.002), bw, 0.026,
            boxstyle="round,pad=0.0,rounding_size=0.010",
            facecolor=bg, edgecolor="#1A1A1A", linewidth=0.5,
            transform=ax.transAxes,
        )
        ax.add_patch(badge)
        ax.text(sx + bw / 2.0, legend_y + 0.015, label,
                ha="center", va="center", fontsize=8.0, fontweight="bold",
                color=fg, transform=ax.transAxes)
        sx += bw + 0.006

    # Cleanup.
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_axis_off()

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

    pdf, png = save_mpl("mbse_verification_matrix")
    register("mbse_verification_matrix", "ok", png_path=png)
