"""mbse_fmea_table - Failure Mode & Effects Analysis for CampusRide.

A reliability-style table that names where the deployed platform can fail and
how visible the failure is. The goal is HCI-readable (no SQL, no code paths,
no constants); failure modes are named in plain English so reviewers can
reason about user impact rather than implementation.

Risk priority numbers (RPN = Severity x Occurrence x Detection) are kept --
they are findings, not engineering machinery. Severity tiers are coloured
under the unified palette: green (low) -> amber (medium) -> red (high), and
the high-risk rows are flagged on the left margin with ACCENT orange.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


# Unified palette
NAVY = "#1A5276"          # headers
ACCENT = "#F39C12"         # high-risk row marker
GREY = "#566573"           # axis / secondary text
INK = "#1B2631"            # primary text


# --- Severity-tier colours (green / yellow / red gradient) -----------------

def _tier_color(score: int):
    """Map a 1..5 score to a green->yellow->red gradient cell colour."""
    # Three discrete tiers keep the figure readable on print:
    #   1-2 = low (green), 3 = medium (yellow), 4-5 = high (red)
    if score <= 2:
        return "#A9DFBF"  # soft green
    if score == 3:
        return "#F9E79F"  # soft yellow
    return "#F5B7B1"      # soft red


def _rpn_tier_color(rpn: int):
    """RPN tier colour for the RPN cell."""
    if rpn < 15:
        return "#A9DFBF"
    if rpn < 30:
        return "#F9E79F"
    return "#F5B7B1"


def _risk_label(rpn: int) -> str:
    if rpn < 15:
        return "Low"
    if rpn < 30:
        return "Medium"
    if rpn < 50:
        return "High"
    return "Critical"


def _risk_badge_color(level: str):
    """Plain (facecolor, textcolor) badges for the rightmost column."""
    return {
        "Low":      ("#A9DFBF", INK),
        "Medium":   ("#F9E79F", INK),
        "High":     ("#F5B7B1", INK),
        "Critical": ("#C0392B", "white"),
    }.get(level, ("#EAECEE", INK))


@renderer("mbse_fmea_table")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    # ------------------------------------------------------------------
    # Data: failure modes phrased for HCI readers, not engineers.
    # Columns: Subsystem, Failure mode, User-visible effect, Likely cause,
    #          How we would notice, S, O, D
    # ------------------------------------------------------------------
    headers = [
        "#", "Subsystem", "Failure mode", "User-visible effect",
        "Likely cause", "How we would notice",
        "S", "O", "D", "RPN", "Risk",
    ]

    rows = [
        ("Sign-in",
         "Verification email\nnever arrives",
         "New users stuck in\npending state",
         "Resend throttle or\nspam-folder filtering",
         "Spike in failed sign-ins;\nsupport tickets",
         4, 2, 2),
        ("Ride matching",
         "Two riders confirmed\nfor the last seat",
         "One rider double-booked;\nmanual reconciliation",
         "Concurrent bookings without\nseat-level locking",
         "Trip shows negative\nseats remaining",
         4, 2, 2),
        ("Cost split / payment",
         "No in-app payment;\nsettled by hand",
         "No escrow protection\nfor either side",
         "Payment integration is\ndesign-only in v4.4",
         "Documented gap; cited\nin scoping section",
         3, 4, 4),
        ("Safety / SOS",
         "Distress button has no\nescalation path",
         "Rider in distress lacks\nautomated help",
         "Backend service not yet\nbuilt for SOS",
         "Feature flag remains off;\nzero invocations",
         5, 3, 4),
        ("Trip-bound chat",
         "First booking briefly\nfails, then succeeds",
         "Momentary error toast,\nchat opens on retry",
         "Idempotent insert path\nwith silent retry",
         "Backend flag for\nharmless duplicate",
         1, 2, 2),
        ("Notification fan-out",
         "Driver misses booking\nnotification",
         "Driver unaware of new\nrider until trip time",
         "Partial delivery without\nbatch transaction",
         "Mismatch between rider\nand driver inboxes",
         3, 2, 2),
        ("Rating system",
         "Driver can revise rider\nscore downward later",
         "Retaliation risk;\nF5 rating-anxiety",
         "No dispute window or\nrating freeze",
         "Driver subset (N=19)\nflags fairness concern",
         4, 3, 2),
        ("Points / rewards",
         "Balance always shows\nzero",
         "Motivation gap; users\nstop engaging",
         "Points ledger not yet\nprovisioned in production",
         "Points API returns\nempty results",
         3, 5, 1),
        ("External outreach",
         "WeChat short-link\nexpires before clicked",
         "Outbound push silently\nfails to reach group",
         "Link service exception\nis not retried",
         "Outreach queue marked\nfailed",
         3, 2, 2),
        ("Campus whitelist",
         "Only Cornell email\naddresses accepted",
         "Multi-campus expansion\nblocked",
         "Single institution domain\nhard-coded",
         "Sign-up rejected for\nnon-Cornell .edu",
         3, 4, 1),
        ("Geo check-in",
         "Spoofed GPS earns\nactivity points",
         "Inflated balance;\nfraudulent rewards",
         "Client-trusted location\nwith no attestation",
         "Manual review of device\nmetadata",
         2, 2, 3),
        ("Group discovery",
         "Community groups all\nstart at one member",
         "No flywheel; cold-start\non community module",
         "Discovery surface not\nyet exposed in app",
         "Manual count of group\nmembership",
         3, 4, 2),
    ]

    # Compute RPN + tier server-side so the figure stays purely declarative.
    enriched = []
    for i, r in enumerate(rows, start=1):
        sub, fm, eff, cause, notice, s, o, d = r
        rpn = s * o * d
        enriched.append((i, sub, fm, eff, cause, notice, s, o, d, rpn,
                          _risk_label(rpn)))

    n_rows = len(enriched)
    n_cols = len(headers)

    col_widths = [
        0.04,   # #
        0.105,  # Subsystem
        0.135,  # Failure mode
        0.140,  # Effect
        0.135,  # Cause
        0.140,  # Notice
        0.035,  # S
        0.035,  # O
        0.035,  # D
        0.050,  # RPN
        0.146,  # Risk
    ]
    # normalise to exactly 1.0
    total = sum(col_widths)
    col_widths = [w / total for w in col_widths]
    col_x = [0.0]
    for w in col_widths:
        col_x.append(col_x[-1] + w)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(18, 10.5))

    title_y = 0.985
    subtitle_y = 0.945
    table_top = 0.905
    legend_band_top = 0.07
    header_h = 0.058
    header_top = table_top
    header_bot = header_top - header_h
    body_top = header_bot
    body_bot = legend_band_top
    row_h = (body_top - body_bot) / n_rows

    # Title (14pt bold pad=14, but rendering as ax text since we run axis-off)
    ax.text(
        0.5, title_y,
        "Where the platform can fail and how we would see it",
        ha="center", va="top", fontsize=14, fontweight="bold",
        color=INK, transform=ax.transAxes,
    )
    # Italic subtitle in grey, stating design intent
    ax.text(
        0.5, subtitle_y,
        "Failure modes phrased for users, not engineers; "
        "high-risk rows are flagged on the left so the eye lands "
        "on what to fix first.",
        ha="center", va="top", fontsize=10, style="italic",
        color=GREY, transform=ax.transAxes,
    )

    # ------------------------------------------------------------------
    # Header row (navy)
    # ------------------------------------------------------------------
    for j, h in enumerate(headers):
        x0 = col_x[j]
        w = col_widths[j]
        ax.add_patch(mpatches.Rectangle(
            (x0, header_bot), w, header_h,
            facecolor=NAVY, edgecolor=NAVY, linewidth=0.0,
            transform=ax.transAxes,
        ))
        ax.text(
            x0 + w / 2.0, header_bot + header_h / 2.0, h,
            ha="center", va="center", fontsize=10.5, fontweight="bold",
            color="white", transform=ax.transAxes,
        )

    # ------------------------------------------------------------------
    # Body rows
    # ------------------------------------------------------------------
    for i, row in enumerate(enriched):
        y_top = header_bot - i * row_h
        y_bot = y_top - row_h
        idx, sub, fm, eff, cause, notice, s, o, d, rpn, level = row
        zebra = "#FBFCFC" if (i % 2 == 0) else "#FFFFFF"
        is_high = level in ("High", "Critical")

        # Left-margin accent for high-risk rows
        if is_high:
            ax.add_patch(mpatches.Rectangle(
                (col_x[0], y_bot), col_widths[0] * 0.28, row_h,
                facecolor=ACCENT, edgecolor="none",
                transform=ax.transAxes,
            ))

        for j in range(n_cols):
            x0 = col_x[j]
            w = col_widths[j]
            cell_face = zebra
            cell_text_color = INK
            cell_weight = "normal"
            cell_size = 8.6

            if j == 0:
                cell_face = "#EAECEE" if not is_high else "#FDEBD0"
                cell_weight = "bold"
                cell_size = 9.5
                txt = str(idx)
            elif j == 1:
                cell_weight = "bold"
                cell_size = 9.0
                txt = sub
            elif j == 2:
                txt = fm
            elif j == 3:
                txt = eff
            elif j == 4:
                txt = cause
            elif j == 5:
                txt = notice
            elif j == 6:
                cell_face = _tier_color(s)
                cell_weight = "bold"
                cell_size = 10.5
                txt = str(s)
            elif j == 7:
                cell_face = _tier_color(o)
                cell_weight = "bold"
                cell_size = 10.5
                txt = str(o)
            elif j == 8:
                cell_face = _tier_color(d)
                cell_weight = "bold"
                cell_size = 10.5
                txt = str(d)
            elif j == 9:
                cell_face = _rpn_tier_color(rpn)
                cell_weight = "bold"
                cell_size = 10.5
                txt = str(rpn)
            else:  # Risk badge
                txt = level

            # Cell rectangle
            ax.add_patch(mpatches.Rectangle(
                (x0, y_bot), w, row_h,
                facecolor=cell_face if j != 10 else zebra,
                edgecolor="#D5D8DC", linewidth=0.5,
                transform=ax.transAxes,
            ))

            if j == 10:
                bg, fg = _risk_badge_color(level)
                pad_x = 0.010
                pad_y = row_h * 0.22
                ax.add_patch(mpatches.FancyBboxPatch(
                    (x0 + pad_x, y_bot + pad_y),
                    w - 2 * pad_x, row_h - 2 * pad_y,
                    boxstyle="round,pad=0.0,rounding_size=0.012",
                    facecolor=bg, edgecolor=GREY, linewidth=0.6,
                    transform=ax.transAxes,
                ))
                ax.text(
                    x0 + w / 2.0, y_bot + row_h / 2.0, level,
                    ha="center", va="center",
                    fontsize=9.0, fontweight="bold",
                    color=fg, transform=ax.transAxes,
                )
                continue

            # Text alignment
            if j in (1, 2, 3, 4, 5):
                ha = "left"
                tx = x0 + 0.006
            else:
                ha = "center"
                tx = x0 + w / 2.0

            ax.text(
                tx, y_bot + row_h / 2.0, txt,
                ha=ha, va="center",
                fontsize=cell_size, fontweight=cell_weight,
                color=cell_text_color, transform=ax.transAxes,
                linespacing=1.1,
            )

    # Outer frame (subtle, navy)
    ax.add_patch(mpatches.Rectangle(
        (0, body_bot), 1.0, header_h + n_rows * row_h,
        facecolor="none", edgecolor=NAVY, linewidth=1.2,
        transform=ax.transAxes,
    ))

    # ------------------------------------------------------------------
    # Legend strip
    # ------------------------------------------------------------------
    leg_y = 0.020
    leg_label_y = leg_y + 0.018

    ax.text(
        0.012, leg_label_y, "Severity / Occurrence / Detection",
        ha="left", va="center", fontsize=9.0, fontweight="bold",
        color=GREY, transform=ax.transAxes,
    )

    sw_x = 0.205
    for label, value in [("low", 1), ("low", 2), ("medium", 3),
                         ("high", 4), ("high", 5)]:
        c = _tier_color(value)
        ax.add_patch(mpatches.Rectangle(
            (sw_x, leg_y), 0.024, 0.030,
            facecolor=c, edgecolor=GREY, linewidth=0.5,
            transform=ax.transAxes,
        ))
        ax.text(sw_x + 0.012, leg_y + 0.015, str(value),
                ha="center", va="center", fontsize=8.6,
                fontweight="bold", color=INK,
                transform=ax.transAxes)
        sw_x += 0.026
    ax.text(0.205, leg_y - 0.014, "low",
            ha="left", va="top", fontsize=8.4, color=GREY,
            transform=ax.transAxes)
    ax.text(0.205 + 5 * 0.026 - 0.005, leg_y - 0.014, "high",
            ha="right", va="top", fontsize=8.4, color=GREY,
            transform=ax.transAxes)

    # Risk-level badges
    badge_x = 0.42
    ax.text(
        badge_x, leg_label_y, "Risk tier",
        ha="left", va="center", fontsize=9.0, fontweight="bold",
        color=GREY, transform=ax.transAxes,
    )
    badge_x += 0.062
    for label in ["Low", "Medium", "High", "Critical"]:
        bg, fg = _risk_badge_color(label)
        bw = 0.072
        ax.add_patch(mpatches.FancyBboxPatch(
            (badge_x, leg_y + 0.002), bw, 0.026,
            boxstyle="round,pad=0.0,rounding_size=0.010",
            facecolor=bg, edgecolor=GREY, linewidth=0.5,
            transform=ax.transAxes,
        ))
        ax.text(badge_x + bw / 2.0, leg_y + 0.015, label,
                ha="center", va="center", fontsize=8.0,
                fontweight="bold", color=fg,
                transform=ax.transAxes)
        badge_x += bw + 0.006

    # Accent-row note
    accent_x = 0.84
    ax.add_patch(mpatches.Rectangle(
        (accent_x, leg_y + 0.006), 0.014, 0.022,
        facecolor=ACCENT, edgecolor="none",
        transform=ax.transAxes,
    ))
    ax.text(
        accent_x + 0.020, leg_y + 0.016,
        "left margin = high-risk row",
        ha="left", va="center", fontsize=8.6,
        color=GREY, style="italic",
        transform=ax.transAxes,
    )

    # Caption note (RPN definition) just below legend
    ax.text(
        0.5, leg_y - 0.014,
        "RPN = Severity x Occurrence x Detection (each scored 1-5).",
        ha="center", va="top", fontsize=8.6, style="italic",
        color=GREY, transform=ax.transAxes,
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_axis_off()

    plt.subplots_adjust(left=0.012, right=0.988, top=0.99, bottom=0.01)

    pdf, png = save_mpl("mbse_fmea_table", dpi=300)
    register("mbse_fmea_table", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
