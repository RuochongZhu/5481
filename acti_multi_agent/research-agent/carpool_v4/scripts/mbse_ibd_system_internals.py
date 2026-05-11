"""mbse_ibd — CampusRide internal block diagram (paper-style).

A SysML Internal Block Diagram of CampusRide, rendered in the unified
mbe figure style. The outer container is the platform itself; inside,
six modules sit as named blocks connected by concept-level data and
event flows. Two thin sidecar lanes (real-time substrate and external
outreach) sit alongside, decoupled from the core composition.

Style contract: see scripts/_mbe_style_guide.md. No file paths, no SQL,
no JS, no constants written out. Module names in plain English.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import setup_mpl, save_mpl, register, renderer  # noqa: E402


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"
NEUTRAL = "#566573"


@renderer("mbse_ibd_system_internals")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 8.6))

    # ------------------------------------------------------------------
    # Canvas geometry
    # ------------------------------------------------------------------
    X_MIN, X_MAX = 0.0, 16.5
    Y_MIN, Y_MAX = 0.0, 10.4

    # Outer container (the CampusRide platform itself)
    CONT_X0, CONT_Y0 = 0.4, 0.6
    CONT_W, CONT_H = 11.4, 8.6

    # Sidecar column (decoupled lanes)
    SIDE_X0 = 12.2
    SIDE_W = X_MAX - SIDE_X0 - 0.2

    # ------------------------------------------------------------------
    # Outer container ("CampusRide platform")
    # ------------------------------------------------------------------
    ax.add_patch(
        FancyBboxPatch(
            (CONT_X0, CONT_Y0), CONT_W, CONT_H,
            boxstyle="round,pad=0.04",
            facecolor="white", edgecolor=PLATFORM_COLOR,
            linewidth=2.0,
        )
    )
    # Soft tint behind the container header
    ax.add_patch(
        FancyBboxPatch(
            (CONT_X0 + 0.15, CONT_Y0 + CONT_H - 0.85),
            CONT_W - 0.3, 0.6,
            boxstyle="round,pad=0.02",
            facecolor=PLATFORM_COLOR, alpha=0.10,
            edgecolor=PLATFORM_COLOR, linewidth=0.8,
        )
    )
    ax.text(
        CONT_X0 + 0.45, CONT_Y0 + CONT_H - 0.55,
        "CampusRide platform",
        ha="left", va="center",
        fontsize=12, fontweight="bold", color=PLATFORM_COLOR,
    )

    # Sidecar lane band
    ax.add_patch(
        FancyBboxPatch(
            (SIDE_X0, CONT_Y0), SIDE_W, CONT_H,
            boxstyle="round,pad=0.03",
            facecolor=NEUTRAL, alpha=0.07,
            edgecolor=NEUTRAL, linewidth=0.9,
        )
    )
    ax.text(
        SIDE_X0 + 0.25, CONT_Y0 + CONT_H - 0.35,
        "Sidecars",
        ha="left", va="center",
        fontsize=11, fontweight="bold", color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Card helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, border, *, fc="white", fs=10,
             bold=False, lw=1.4, text_color="#1B2631"):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=border, linewidth=lw,
            )
        )
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color=text_color,
            fontweight="bold" if bold else "normal",
        )

    def arrow(x0, y0, x1, y1, color, *, lw=1.3, ls="-", rad=0.0,
              scale=12):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle="-|>", color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=scale,
                connectionstyle=f"arc3,rad={rad}",
            )
        )

    def edge_label(x, y, text, color, *, fs=8.6, italic=False):
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color=color,
            style="italic" if italic else "normal",
            bbox=dict(facecolor="white", edgecolor=color,
                      boxstyle="round,pad=0.18", linewidth=0.7,
                      alpha=0.95),
        )

    # ------------------------------------------------------------------
    # Six module blocks inside the container (3 columns x 2 rows)
    # Top row:    Carpool, Marketplace, Activities
    # Bottom row: Identity, Messaging, Outreach
    # The "highlighted flow" runs Carpool -> Messaging (accent).
    # ------------------------------------------------------------------
    # Column centers and row centers, fitted inside the container
    col_cx = [CONT_X0 + 2.10, CONT_X0 + 5.70, CONT_X0 + 9.30]
    row_cy_top = CONT_Y0 + CONT_H - 2.55
    row_cy_bot = CONT_Y0 + 1.95

    MOD_W, MOD_H = 3.10, 1.55

    modules = {
        "Carpool":     (col_cx[0], row_cy_top, "Trip publish, book,\nrate"),
        "Marketplace": (col_cx[1], row_cy_top, "List, browse,\nbuyer-seller chat"),
        "Activities":  (col_cx[2], row_cy_top, "Event publish &\ncheck-in"),
        "Identity":    (col_cx[0], row_cy_bot, "Cornell email check\n& guest fallback"),
        "Messaging":   (col_cx[1], row_cy_bot, "Direct chat &\ntrip-bound rooms"),
        "Outreach":    (col_cx[2], row_cy_bot, "Notifications &\noff-platform posts"),
    }

    # Identity is a primary block too — paint it in the platform color so
    # readers see it as foundational. Carpool gets the accent treatment as
    # the highlighted module (the paper's deep-dive). Other modules use
    # white cards with platform-color borders.
    primary_blocks = {"Identity"}
    accent_block = "Carpool"

    for name, (cx, cy, tag) in modules.items():
        if name == accent_block:
            # Highlighted module
            card(cx, cy, MOD_W, MOD_H,
                 "", ACCENT_COLOR, fc="#FEF5E7", lw=1.8)
            text_color = "#1B2631"
            title_color = "#1B2631"
        elif name in primary_blocks:
            card(cx, cy, MOD_W, MOD_H,
                 "", PLATFORM_COLOR, fc=PLATFORM_COLOR, lw=1.6)
            text_color = "white"
            title_color = "white"
        else:
            card(cx, cy, MOD_W, MOD_H,
                 "", PLATFORM_COLOR, lw=1.4)
            text_color = "#1B2631"
            title_color = PLATFORM_COLOR

        # «block» stereotype, name, and tagline rendered manually so the
        # vertical layout reads as a SysML block.
        ax.text(
            cx, cy + MOD_H / 2 - 0.22,
            "<<block>>",
            ha="center", va="center",
            fontsize=8.5, style="italic", color=text_color, alpha=0.85,
        )
        ax.text(
            cx, cy + 0.18,
            name,
            ha="center", va="center",
            fontsize=12, fontweight="bold", color=title_color,
        )
        ax.text(
            cx, cy - 0.40,
            tag,
            ha="center", va="center",
            fontsize=9, color=text_color, style="italic",
        )

    # ------------------------------------------------------------------
    # Port marks: small white squares on the edges to suggest SysML ports.
    # ------------------------------------------------------------------
    def port(cx, cy, side):
        s = 0.16
        if side == "right":
            x = cx + MOD_W / 2 - s / 2
            y = cy
        elif side == "left":
            x = cx - MOD_W / 2 - s / 2
            y = cy
        elif side == "top":
            x = cx
            y = cy + MOD_H / 2 - s / 2
        else:  # bottom
            x = cx
            y = cy - MOD_H / 2 - s / 2
        ax.add_patch(
            FancyBboxPatch(
                (x - s / 2, y - s / 2), s, s,
                boxstyle="square,pad=0.0",
                facecolor="white", edgecolor=PLATFORM_COLOR,
                linewidth=1.1, zorder=5,
            )
        )

    # Place ports on the relevant edges (one per active flow)
    for name in modules:
        cx, cy, _ = modules[name]
        if name == "Carpool":
            port(cx, cy, "bottom"); port(cx, cy, "right")
        elif name == "Marketplace":
            port(cx, cy, "bottom"); port(cx, cy, "right"); port(cx, cy, "left")
        elif name == "Activities":
            port(cx, cy, "bottom"); port(cx, cy, "left")
        elif name == "Identity":
            port(cx, cy, "top"); port(cx, cy, "right")
        elif name == "Messaging":
            port(cx, cy, "top"); port(cx, cy, "left"); port(cx, cy, "right")
        elif name == "Outreach":
            port(cx, cy, "top"); port(cx, cy, "left")

    # ------------------------------------------------------------------
    # Inter-module flows (port-to-port arrows)
    # ------------------------------------------------------------------
    cx_car, cy_car, _ = modules["Carpool"]
    cx_mkt, cy_mkt, _ = modules["Marketplace"]
    cx_act, cy_act, _ = modules["Activities"]
    cx_idt, cy_idt, _ = modules["Identity"]
    cx_msg, cy_msg, _ = modules["Messaging"]
    cx_out, cy_out, _ = modules["Outreach"]

    half_h = MOD_H / 2
    half_w = MOD_W / 2

    # 1) Carpool -> Messaging  (HIGHLIGHTED: trip-bound chat opens)
    arrow(
        cx_car + 0.35, cy_car - half_h,
        cx_msg - 0.65, cy_msg + half_h,
        ACCENT_COLOR, lw=1.9, rad=-0.10, scale=14,
    )
    edge_label(
        cx_car + 1.55, cy_car - half_h - 0.45,
        "Open trip-bound chat",
        ACCENT_COLOR, fs=8.8,
    )

    # 2) Marketplace -> Messaging  (buyer-seller direct chat)
    arrow(
        cx_mkt, cy_mkt - half_h,
        cx_msg, cy_msg + half_h,
        PLATFORM_COLOR, rad=0.0,
    )
    edge_label(
        cx_mkt + 0.05, (cy_mkt - half_h + cy_msg + half_h) / 2,
        "Buyer-seller chat",
        PLATFORM_COLOR,
    )

    # 3) Activities -> Messaging  (per-event chat room)
    arrow(
        cx_act - half_w, cy_act - 0.45,
        cx_msg + half_w, cy_msg + 0.45,
        PLATFORM_COLOR, rad=-0.20,
    )
    edge_label(
        (cx_act + cx_msg) / 2 + 0.20,
        (cy_act + cy_msg) / 2 - 0.25,
        "Per-event chat room",
        PLATFORM_COLOR,
    )

    # 4) Identity -> Carpool  (verified-only ride access)
    arrow(
        cx_idt, cy_idt + half_h,
        cx_car, cy_car - half_h,
        PLATFORM_COLOR,
    )
    edge_label(
        cx_idt - 0.05, (cy_idt + half_h + cy_car - half_h) / 2,
        "Verified-only access",
        PLATFORM_COLOR,
    )

    # 5) Identity -> Marketplace / Activities (lighter, sketched)
    arrow(
        cx_idt + half_w, cy_idt + 0.40,
        cx_mkt - half_w, cy_mkt - 0.40,
        PLATFORM_COLOR, ls="--", lw=1.0, rad=0.10,
    )
    arrow(
        cx_idt + half_w, cy_idt + 0.55,
        cx_act - half_w, cy_act - 0.55,
        PLATFORM_COLOR, ls="--", lw=1.0, rad=0.25,
    )

    # 6) Marketplace -> Outreach  (off-platform outreach posts)
    arrow(
        cx_mkt + half_w, cy_mkt - 0.55,
        cx_out - half_w, cy_out + 0.55,
        PLATFORM_COLOR, rad=-0.05,
    )
    edge_label(
        (cx_mkt + cx_out) / 2,
        (cy_mkt + cy_out) / 2 + 0.40,
        "Off-platform posts",
        PLATFORM_COLOR,
    )

    # 7) Carpool -> Outreach  (ride pushes)
    arrow(
        cx_car + half_w - 0.05, cy_car - 0.55,
        cx_out - half_w, cy_out + 0.55,
        PLATFORM_COLOR, ls="--", lw=1.0, rad=-0.30,
    )

    # ------------------------------------------------------------------
    # Sidecars (right column): two grey blocks for decoupled lanes
    # ------------------------------------------------------------------
    sc_cx = SIDE_X0 + SIDE_W / 2
    sc_w = SIDE_W - 0.5
    sc_top_cy = CONT_Y0 + CONT_H - 2.55
    sc_bot_cy = CONT_Y0 + 1.95

    card(sc_cx, sc_top_cy, sc_w, MOD_H,
         "", NEUTRAL, lw=1.4)
    ax.text(sc_cx, sc_top_cy + MOD_H / 2 - 0.22, "<<sidecar>>",
            ha="center", va="center",
            fontsize=8.5, style="italic", color=NEUTRAL, alpha=0.9)
    ax.text(sc_cx, sc_top_cy + 0.18, "Real-time substrate",
            ha="center", va="center",
            fontsize=11, fontweight="bold", color=NEUTRAL)
    ax.text(sc_cx, sc_top_cy - 0.40,
            "Live notifications &\nchat room delivery",
            ha="center", va="center",
            fontsize=9, color=NEUTRAL, style="italic")

    card(sc_cx, sc_bot_cy, sc_w, MOD_H,
         "", NEUTRAL, lw=1.4)
    ax.text(sc_cx, sc_bot_cy + MOD_H / 2 - 0.22, "<<sidecar>>",
            ha="center", va="center",
            fontsize=8.5, style="italic", color=NEUTRAL, alpha=0.9)
    ax.text(sc_cx, sc_bot_cy + 0.18, "External outreach",
            ha="center", va="center",
            fontsize=11, fontweight="bold", color=NEUTRAL)
    ax.text(sc_cx, sc_bot_cy - 0.40,
            "WeChat short-link\n& post queue",
            ha="center", va="center",
            fontsize=9, color=NEUTRAL, style="italic")

    # Sidecar links: Messaging -> Real-time substrate
    arrow(
        cx_msg + half_w, cy_msg + 0.20,
        sc_cx - sc_w / 2, sc_top_cy - 0.20,
        NEUTRAL, ls="--", rad=-0.15,
    )
    edge_label(
        (cx_msg + half_w + sc_cx - sc_w / 2) / 2,
        (cy_msg + 0.20 + sc_top_cy - 0.20) / 2 + 0.30,
        "Live delivery",
        NEUTRAL, italic=True, fs=8.4,
    )

    # Outreach -> External outreach
    arrow(
        cx_out + half_w, cy_out,
        sc_cx - sc_w / 2, sc_bot_cy,
        NEUTRAL, ls="--",
    )
    edge_label(
        (cx_out + half_w + sc_cx - sc_w / 2) / 2,
        (cy_out + sc_bot_cy) / 2 + 0.25,
        "Off-platform push",
        NEUTRAL, italic=True, fs=8.4,
    )

    # ------------------------------------------------------------------
    # Title and italic subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "CampusRide internal block diagram",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, Y_MAX - 0.25,
        "Six modules compose the platform; identity gates every module, "
        "and outreach is decoupled into a sidecar.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Cosmetic
    # ------------------------------------------------------------------
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(Y_MIN - 0.2, Y_MAX + 0.2)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbse_ibd_system_internals", dpi=300)
    register("mbse_ibd_system_internals", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
