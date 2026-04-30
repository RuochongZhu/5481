"""mbse_fmea_table - Failure Mode & Effects Analysis (FMEA) for CampusRide v4.4.

12-row FMEA mirrored on classical MBSE/MIL-STD-1629A reliability tables.
Severity (S), Occurrence (O), Detection (D) each scored 1-5; RPN = S*O*D.
Each row anchored to a real subsystem in the v4.4 deployment snapshot
(see draft.md §5.10, §5.16, §6, §7.2).

Color encoding:
  - Severity / Occurrence / Detection cells: yellow (low) -> red (high)
  - RPN cell: green (low) -> red (high) gradient
  - Risk Level cell: badge-style colored fill
  - Header row: dark navy with white text
  - Alternating zebra body rows for readability
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


# --- Color helpers ----------------------------------------------------------

def _yellow_to_red(v: int, vmin: int = 1, vmax: int = 5):
    """Map 1..5 to a yellow->orange->red gradient (low risk = yellow)."""
    from matplotlib.cm import get_cmap
    from matplotlib.colors import Normalize
    cmap = get_cmap("YlOrRd")
    norm = Normalize(vmin=vmin - 0.5, vmax=vmax + 0.5)
    return cmap(norm(v))


def _rpn_color(rpn: int):
    """Map RPN to green (low) -> yellow -> red (high)."""
    from matplotlib.cm import get_cmap
    from matplotlib.colors import Normalize
    cmap = get_cmap("RdYlGn_r")  # reversed so green=low, red=high
    norm = Normalize(vmin=1, vmax=80)
    return cmap(norm(min(rpn, 80)))


def _risk_badge_color(level: str):
    """Return (facecolor, textcolor) for the Risk Level badge."""
    palette = {
        "Low": ("#27AE60", "#FFFFFF"),
        "Medium": ("#F39C12", "#1A1A1A"),
        "Medium-High": ("#E67E22", "#FFFFFF"),
        "High": ("#C0392B", "#FFFFFF"),
        "Critical": ("#7B241C", "#FFFFFF"),
    }
    # Strip parenthetical suffix, e.g. "Medium-High (F5-validated)" -> "Medium-High".
    base = level.split("(")[0].strip()
    base = base.split(",")[0].strip()
    return palette.get(base, ("#BDC3C7", "#1A1A1A"))


def _text_on_color(rgba) -> str:
    """Pick black or white text for legibility on the given RGBA cell color."""
    r, g, b = rgba[0], rgba[1], rgba[2]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "#1A1A1A" if luminance > 0.6 else "#FFFFFF"


@renderer("mbse_fmea_table")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    # --- Data -------------------------------------------------------------
    # (#, Subsystem, Failure Mode, Failure Effects, Possible Cause,
    #  Detection Conditions, S, O, D, RPN, Risk Level)
    headers = [
        "#", "Subsystem", "Failure Mode", "Failure Effects",
        "Possible Cause", "Detection Conditions",
        "S", "O", "D", "RPN", "Risk Level",
    ]
    rows = [
        (1, "Auth / Resend Email",
         "Verification email\nnot delivered",
         "Users stuck in pending\nstate; cannot log in",
         "Resend rate-limit or\nemail flagged as spam",
         "Login-failure rate spike;\nResend dashboard 4xx",
         4, 2, 2, 16, "Medium-High"),
        (2, "Ride-Match",
         "Race on last seat ->\ndouble-booking",
         "Two riders confirmed\nfor same seat; conflict",
         "Concurrent POST without\nrow-level lock on rides",
         "seats_remaining < 0\nin ride table logs",
         4, 2, 2, 16, "Medium-High"),
        (3, "Cost-Splitting / Payment",
         "Payment gateway not\nintegrated",
         "Manual settlement only;\nno escrow protection",
         "Design-only in v4.4;\nStripe not wired",
         "N/A current; design risk\ndocumented in §7.2",
         3, 4, 4, 48, "High (design risk)"),
        (4, "SOS / Safety",
         "SOS button not wired\nto emergency contacts",
         "Rider in distress lacks\nautomated escalation",
         "Design-only stub;\nno backend service",
         "Zero invocations to date;\nfeature flag off",
         5, 3, 4, 60, "High"),
        (5, "Group-Chat Auto-create",
         "Duplicate-key 23505 on\nfirst booking insert",
         "Brief 500 to client;\nchat eventually OK",
         "Postgres unique constraint\non (ride_id, user_id)",
         "Backend log shows code\n23505 swallowed",
         1, 2, 2, 4, "Low"),
        (6, "Notification Bundle",
         "6-notification fan-out\nfails partway",
         "Driver missing booking\nnotice; rider notified",
         "Partial sendNotification\nfailure; no transaction",
         "notifications.unread per\nride mismatched",
         3, 2, 2, 12, "Medium"),
        (7, "Rating System",
         "Update-in-place allows\ndownward revision",
         "Driver retaliation risk;\nF5-validated concern",
         "No dispute window;\nno rating freeze logic",
         "F5 driver subset N=19\nsignals rating-anxiety",
         4, 3, 2, 24, "Medium-High"),
        (8, "Points Subsystem",
         "point_rules empty;\npoint_transactions missing",
         "Points always 0;\nmotivation gap",
         "Migration not run on\nRailway production DB",
         "REST returns PGRST205\non point_transactions",
         3, 5, 1, 15, "Medium"),
        (9, "WeChat Outreach",
         "Mini-program short-link\nexpires; H5 fallback fails",
         "Outbound push silently\nbroken; no WeChat reach",
         "wechat-link.service\nexception not retried",
         "wxgroup_notice_record\ndispatch_status='failed'",
         3, 2, 2, 12, "Medium"),
        (10, ".edu Whitelist",
         "Single-tenant: only\n@cornell.edu accepted",
         "Multi-campus expansion\nblocked; EC12 pending",
         "Institution-domain\nwhitelist hard-coded",
         "Manual test fails for\nnon-Cornell .edu addr",
         3, 4, 1, 12, "Medium"),
        (11, "Geo-Checkin",
         "User fakes GPS to claim\nactivity points",
         "Inflated points balance;\nfraudulent rewards",
         "No device attestation;\nclient-trusted geo",
         "device_info JSONB\ninspection (manual)",
         2, 2, 3, 12, "Low"),
        (12, "Group Discovery",
         "All 5 community groups\nhave member_count=1",
         "No flywheel; community\nmodule cold-start",
         "Discovery UI not yet\nsurfaced in app shell",
         "Manual review of groups;\nDB count check",
         3, 4, 2, 24, "Medium"),
    ]

    n_rows = len(rows)
    n_cols = len(headers)

    # Column relative widths (sum -> normalized later).
    col_widths = [
        0.5,   # #
        1.7,   # Subsystem
        2.4,   # Failure Mode
        2.6,   # Failure Effects
        2.5,   # Possible Cause
        2.6,   # Detection Conditions
        0.5,   # S
        0.5,   # O
        0.5,   # D
        0.7,   # RPN
        1.7,   # Risk Level
    ]
    total_w = sum(col_widths)
    col_widths = [w / total_w for w in col_widths]
    col_x = [0.0]
    for w in col_widths:
        col_x.append(col_x[-1] + w)

    # --- Figure -----------------------------------------------------------
    fig, ax = plt.subplots(figsize=(18, 10.5))

    # Vertical layout: reserve top band for title/subtitle, bottom band for legend.
    title_band_top = 0.995
    subtitle_y = 0.955
    table_top = 0.915
    legend_band_top = 0.06  # space above the legend strip
    legend_y = 0.018

    header_h = 0.062
    header_top = table_top
    header_bot = header_top - header_h
    body_top = header_bot
    body_bot = legend_band_top
    row_h = (body_top - body_bot) / n_rows

    # Title.
    ax.text(
        0.5, title_band_top - 0.005,
        "FMEA - CampusRide v4.4 subsystem failure-mode analysis",
        ha="center", va="top", fontsize=16, fontweight="bold",
        color="#1A1A1A", transform=ax.transAxes,
    )
    ax.text(
        0.5, subtitle_y,
        "RPN = Severity x Occurrence x Detection. "
        "Anchored to draft.md §5.10 deployment snapshot, §5.16 HoQ, §6 audit, §7.2 limits.",
        ha="center", va="top", fontsize=10, style="italic",
        color="#566573", transform=ax.transAxes,
    )

    # Header row.
    for j, h in enumerate(headers):
        x0 = col_x[j]
        w = col_widths[j]
        rect = mpatches.Rectangle(
            (x0, header_bot), w, header_h,
            facecolor="#1A2E44", edgecolor="#0E1B2A", linewidth=0.9,
            transform=ax.transAxes,
        )
        ax.add_patch(rect)
        ax.text(
            x0 + w / 2.0, header_bot + header_h / 2.0, h,
            ha="center", va="center", fontsize=10.4, fontweight="bold",
            color="white", transform=ax.transAxes,
        )

    # Body rows.
    for i, row in enumerate(rows):
        y_top = header_bot - i * row_h
        y_bot = y_top - row_h
        zebra = "#F4F6F7" if (i % 2 == 0) else "#FFFFFF"

        for j, val in enumerate(row):
            x0 = col_x[j]
            w = col_widths[j]
            cell_facecolor = zebra
            text_color = "#1A1A1A"
            text_weight = "normal"
            text_size = 8.4

            # Special coloring per column index.
            if j == 0:  # row #
                cell_facecolor = "#EAECEE"
                text_weight = "bold"
                text_size = 9.5
            elif j == 1:  # Subsystem
                text_weight = "bold"
                text_size = 9.0
            elif j in (6, 7, 8):  # S, O, D
                color = _yellow_to_red(int(val))
                cell_facecolor = color
                text_color = _text_on_color(color)
                text_weight = "bold"
                text_size = 10.5
            elif j == 9:  # RPN
                color = _rpn_color(int(val))
                cell_facecolor = color
                text_color = _text_on_color(color)
                text_weight = "bold"
                text_size = 10.5
            elif j == 10:  # Risk Level
                bg, fg = _risk_badge_color(str(val))
                cell_facecolor = bg
                text_color = fg
                text_weight = "bold"
                text_size = 8.8

            rect = mpatches.Rectangle(
                (x0, y_bot), w, row_h,
                facecolor=cell_facecolor, edgecolor="#BDC3C7", linewidth=0.5,
                transform=ax.transAxes,
            )
            ax.add_patch(rect)

            # For Risk Level, draw a rounded badge inside the cell.
            if j == 10:
                pad_x = 0.006
                pad_y = row_h * 0.18
                badge = mpatches.FancyBboxPatch(
                    (x0 + pad_x, y_bot + pad_y),
                    w - 2 * pad_x, row_h - 2 * pad_y,
                    boxstyle="round,pad=0.0,rounding_size=0.012",
                    facecolor=cell_facecolor, edgecolor="#1A1A1A",
                    linewidth=0.6, transform=ax.transAxes,
                )
                # Repaint the cell area so the rounded badge sits cleanly on
                # the zebra background.
                bg_rect = mpatches.Rectangle(
                    (x0, y_bot), w, row_h,
                    facecolor=zebra, edgecolor="#BDC3C7", linewidth=0.5,
                    transform=ax.transAxes,
                )
                # Clear the previously drawn cell by overpainting.
                ax.add_patch(bg_rect)
                ax.add_patch(badge)

            text_val = str(val)
            ha = "center"
            if j in (1, 2, 3, 4, 5):  # text-heavy cells: left align
                ha = "left"
                text_x = x0 + 0.005
            else:
                text_x = x0 + w / 2.0

            ax.text(
                text_x, y_bot + row_h / 2.0, text_val,
                ha=ha, va="center", fontsize=text_size, fontweight=text_weight,
                color=text_color, transform=ax.transAxes, linespacing=1.05,
            )

    # Outer frame around the whole table.
    outer = mpatches.Rectangle(
        (0, body_bot), 1.0, header_h + n_rows * row_h,
        facecolor="none", edgecolor="#1A1A1A", linewidth=1.4,
        transform=ax.transAxes,
    )
    ax.add_patch(outer)

    # --- Legend / scale strip --------------------------------------------
    # S / O / D scale: 5 swatches.
    ax.text(
        0.005, legend_y + 0.018, "Scale (S, O, D):",
        ha="left", va="center", fontsize=9.0, fontweight="bold",
        color="#1A1A1A", transform=ax.transAxes,
    )
    sw_x = 0.10
    for v in range(1, 6):
        color = _yellow_to_red(v)
        sw = mpatches.Rectangle(
            (sw_x, legend_y), 0.022, 0.030,
            facecolor=color, edgecolor="#7F8C8D", linewidth=0.5,
            transform=ax.transAxes,
        )
        ax.add_patch(sw)
        ax.text(
            sw_x + 0.011, legend_y + 0.015, str(v),
            ha="center", va="center", fontsize=8.6, fontweight="bold",
            color=_text_on_color(color), transform=ax.transAxes,
        )
        sw_x += 0.024

    # RPN gradient: continuous bar with min/max ticks.
    ax.text(
        sw_x + 0.025, legend_y + 0.018, "RPN gradient (1 -> 80):",
        ha="left", va="center", fontsize=9.0, fontweight="bold",
        color="#1A1A1A", transform=ax.transAxes,
    )
    bar_x0 = sw_x + 0.16
    bar_w = 0.14
    n_ticks = 36
    for k in range(n_ticks):
        rpn_v = 1 + (80 - 1) * k / (n_ticks - 1)
        color = _rpn_color(int(round(rpn_v)))
        seg = mpatches.Rectangle(
            (bar_x0 + k * (bar_w / n_ticks), legend_y),
            bar_w / n_ticks + 0.0005, 0.030,
            facecolor=color, edgecolor="none",
            transform=ax.transAxes,
        )
        ax.add_patch(seg)
    # Bar border.
    bar_border = mpatches.Rectangle(
        (bar_x0, legend_y), bar_w, 0.030,
        facecolor="none", edgecolor="#1A1A1A", linewidth=0.6,
        transform=ax.transAxes,
    )
    ax.add_patch(bar_border)
    ax.text(bar_x0, legend_y - 0.012, "low",
            ha="left", va="top", fontsize=8.2, color="#1A1A1A",
            transform=ax.transAxes)
    ax.text(bar_x0 + bar_w, legend_y - 0.012, "high",
            ha="right", va="top", fontsize=8.2, color="#1A1A1A",
            transform=ax.transAxes)

    # Risk-level badge legend.
    badge_x = bar_x0 + bar_w + 0.025
    ax.text(
        badge_x, legend_y + 0.018, "Risk:",
        ha="left", va="center", fontsize=9.0, fontweight="bold",
        color="#1A1A1A", transform=ax.transAxes,
    )
    badge_x += 0.040
    for label in ["Low", "Medium", "Medium-High", "High"]:
        bg, fg = _risk_badge_color(label)
        bw = 0.064
        badge = mpatches.FancyBboxPatch(
            (badge_x, legend_y + 0.002), bw, 0.026,
            boxstyle="round,pad=0.0,rounding_size=0.010",
            facecolor=bg, edgecolor="#1A1A1A", linewidth=0.5,
            transform=ax.transAxes,
        )
        ax.add_patch(badge)
        ax.text(
            badge_x + bw / 2.0, legend_y + 0.015, label,
            ha="center", va="center", fontsize=7.6, fontweight="bold",
            color=fg, transform=ax.transAxes,
        )
        badge_x += bw + 0.005

    # Figure-level cleanup.
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_axis_off()

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

    pdf, png = save_mpl("mbse_fmea_table")
    register("mbse_fmea_table", "ok", png_path=png)
