"""mbse_ibd_system_internals - SysML-style Internal Block Diagram.

Renders the internal composition of the CampusRide v4.4 system: the 6
modules (Carpool, Marketplace, Activities, Groups, Messages, Points)
sitting on top of 4 shared substrate layers (.edu Identity,
Notification + Socket.IO, Supabase Postgres + RLS, WeChat outreach
pipeline).

Inter-module flows shown:
  - Carpool -> Messages: ride_carpool group auto-create
  - Marketplace -> WeChat: 62 outreach pushes
  - Activities -> Points: geo-checkin reward (designed but inert)
  - Activities -> Messages: activity_chat_messages
  - Marketplace -> Messages: context_type='marketplace' DM
  - Points -> all modules: cross-module meta-layer (translucent ring)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, MODULE_COLORS,
)


@renderer("mbse_ibd_system_internals")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    from matplotlib.lines import Line2D

    # ------------------------------------------------------------------
    # Canvas (A4-readable, landscape).  All coords in inches-equivalent
    # data units; we choose ranges that give plenty of label room.
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 20)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------
    # Outer system boundary: a SysML «system» block envelopes everything.
    # ------------------------------------------------------------------
    sys_box = FancyBboxPatch(
        (0.6, 0.6), 28.8, 18.8,
        boxstyle="round,pad=0.05,rounding_size=0.6",
        linewidth=2.4, edgecolor="#0E2F44",
        facecolor="#F4F8FB", zorder=1,
    )
    ax.add_patch(sys_box)
    ax.text(
        1.4, 19.0, "<<system>>",
        fontsize=11, color="#566573", style="italic",
        ha="left", va="center", zorder=3,
    )
    ax.text(
        1.4, 18.45, "CampusRide v4.4 - Internal Block Diagram (IBD)",
        fontsize=15, fontweight="bold", color="#0E2F44",
        ha="left", va="center", zorder=3,
    )
    ax.text(
        28.6, 18.7,
        "snapshot 2026-04-23  -  184 verified users",
        fontsize=9, color="#566573", style="italic",
        ha="right", va="center", zorder=3,
    )

    # ------------------------------------------------------------------
    # 6 modules in a 3x2 grid in the upper portion.
    # Layout: top row Carpool, Marketplace, Activities
    #         bot row Groups,  Messages,    Points (top of substrate)
    # We keep Points as a translucent overlay ring across the modules.
    # ------------------------------------------------------------------
    mod_w, mod_h = 7.4, 3.4
    mod_y_top = 13.2
    mod_y_bot = 8.6
    col_x = [1.6, 11.4, 21.2]   # left edges per column

    modules = {
        "Carpool":     {"pos": (col_x[0], mod_y_top),
                        "ports": ["ride_carpool group port",
                                  "rating port (2h delay)"]},
        "Marketplace": {"pos": (col_x[1], mod_y_top),
                        "ports": ["item context DM port",
                                  "WeChat outreach port"]},
        "Activities":  {"pos": (col_x[2], mod_y_top),
                        "ports": ["geo-checkin port",
                                  "activity_chat port"]},
        "Groups":      {"pos": (col_x[0], mod_y_bot),
                        "ports": ["group_members port",
                                  "ride_carpool kind port"]},
        "Messages":    {"pos": (col_x[1], mod_y_bot),
                        "ports": ["thread:{id} room port",
                                  "context_type DM port"]},
        # Points module rendered as a translucent ring overlay below; we
        # still place a small block in the third bot column to give it a
        # visual anchor and a regular legend entry.
        "Points":      {"pos": (col_x[2], mod_y_bot),
                        "ports": ["increment_user_points RPC",
                                  "rule registry (point_rules)"]},
    }

    def draw_module(name: str, x: float, y: float, w: float, h: float,
                    ports: list[str]):
        face = MODULE_COLORS[name]
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.04,rounding_size=0.32",
            linewidth=1.6, edgecolor="#1A1A1A",
            facecolor=face, alpha=0.92, zorder=4,
        )
        ax.add_patch(box)
        # «block» stereotype
        ax.text(
            x + w / 2, y + h - 0.45, "<<block>>",
            fontsize=9, color="#FFFFFF", style="italic",
            ha="center", va="center", zorder=6, alpha=0.9,
        )
        ax.text(
            x + w / 2, y + h - 1.05, name,
            fontsize=15, fontweight="bold", color="white",
            ha="center", va="center", zorder=6,
        )
        # Port list (rendered as small rounded chips on the bottom edge)
        for i, p in enumerate(ports):
            chip_w = w / len(ports) - 0.35
            chip_x = x + 0.20 + i * (chip_w + 0.35)
            chip_y = y + 0.30
            chip = FancyBboxPatch(
                (chip_x, chip_y), chip_w, 0.95,
                boxstyle="round,pad=0.02,rounding_size=0.18",
                linewidth=0.8, edgecolor="#1A1A1A",
                facecolor="white", alpha=0.92, zorder=5,
            )
            ax.add_patch(chip)
            ax.text(
                chip_x + chip_w / 2, chip_y + 0.48, p,
                fontsize=8.0, color="#1A1A1A",
                ha="center", va="center", zorder=6,
            )
        # Mid-row tagline (between title and ports)
        taglines = {
            "Carpool":     "ride publish &harr; book &harr; rate (5+2 fan-out)",
            "Marketplace": "list / browse / context-DM (15 items removed)",
            "Activities":  "publish event + geo-checkin (0 rows live)",
            "Groups":      "auto + community (5 single-member groups)",
            "Messages":    "DM + group chat + typing indicator",
            "Points":      "rule + transaction (inert: 0 point_rules)",
        }
        ax.text(
            x + w / 2, y + h - 1.65, taglines[name].replace("&harr;", "<->"),
            fontsize=8.6, color="#FFFFFF", style="italic",
            ha="center", va="center", zorder=6, alpha=0.95,
        )

    for name, meta in modules.items():
        mx, my = meta["pos"]
        draw_module(name, mx, my, mod_w, mod_h, meta["ports"])

    # Module center coords (used for arrows below)
    def center(name: str) -> tuple[float, float]:
        x, y = modules[name]["pos"]
        return x + mod_w / 2, y + mod_h / 2

    def edge_point(name: str, side: str) -> tuple[float, float]:
        x, y = modules[name]["pos"]
        if side == "right":
            return x + mod_w, y + mod_h / 2
        if side == "left":
            return x, y + mod_h / 2
        if side == "top":
            return x + mod_w / 2, y + mod_h
        if side == "bottom":
            return x + mod_w / 2, y
        if side == "tr":
            return x + mod_w, y + mod_h * 0.78
        if side == "tl":
            return x, y + mod_h * 0.78
        if side == "br":
            return x + mod_w, y + mod_h * 0.22
        if side == "bl":
            return x, y + mod_h * 0.22
        return center(name)

    # ------------------------------------------------------------------
    # Translucent Points ring (cross-module meta-layer) - per §5.7.4
    # We draw it as a wide rounded rectangle behind all the module blocks
    # and tag it as the meta-layer.
    # ------------------------------------------------------------------
    ring_box = FancyBboxPatch(
        (1.0, 8.0), 28.0, 8.5,
        boxstyle="round,pad=0.02,rounding_size=0.50",
        linewidth=2.0, edgecolor=MODULE_COLORS["Points"],
        facecolor=MODULE_COLORS["Points"], alpha=0.10,
        linestyle=(0, (4, 3)), zorder=2.5,
    )
    ax.add_patch(ring_box)
    # Place ring label just above the ring (between modules and title bar)
    ax.text(
        15.0, 17.20,
        "Points overlay - cross-module meta-layer (rule -> transaction)",
        fontsize=10.0, color="#7D6608", fontweight="bold", style="italic",
        ha="center", va="center", zorder=3,
        bbox=dict(facecolor="#FCF3CF", edgecolor=MODULE_COLORS["Points"],
                  boxstyle="round,pad=0.20", linewidth=0.8, alpha=0.90),
    )

    # ------------------------------------------------------------------
    # Inter-module flow arrows (port-to-port)
    # ------------------------------------------------------------------
    flow_color = "#34495E"

    def flow(src_name, src_side, dst_name, dst_side, label,
             style="-", color=flow_color, rad=0.0, lw=1.4,
             label_offset=(0, 0)):
        sx, sy = edge_point(src_name, src_side)
        dx, dy = edge_point(dst_name, dst_side)
        arrow = FancyArrowPatch(
            (sx, sy), (dx, dy),
            arrowstyle="-|>", mutation_scale=14,
            linewidth=lw, color=color,
            connectionstyle=f"arc3,rad={rad}",
            linestyle=style, zorder=7,
        )
        ax.add_patch(arrow)
        # Label at midpoint with optional offset
        mx, my = (sx + dx) / 2 + label_offset[0], (sy + dy) / 2 + label_offset[1]
        ax.text(
            mx, my, label,
            fontsize=8.4, color=color, ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor=color,
                      boxstyle="round,pad=0.20", linewidth=0.8, alpha=0.95),
            zorder=8,
        )

    # 1) Carpool -> Messages : ride_carpool group auto-create
    flow("Carpool", "bottom", "Messages", "top",
         "ride_carpool group\nauto-create on first booking",
         rad=-0.18, label_offset=(-1.2, 0.0))

    # 2) Marketplace -> WeChat (a substrate layer, drawn below)
    #    We draw this when we draw the substrate.
    # 3) Activities -> Points : geo-checkin reward (designed but inert)
    flow("Activities", "left", "Points", "top",
         "geo-checkin reward\n(designed; 0 point_rules)",
         rad=0.20, style="--", color="#7D6608",
         label_offset=(0.0, 0.6))

    # 4) Activities -> Messages : activity_chat_messages
    flow("Activities", "bottom", "Messages", "right",
         "activity_chat_messages\n(activity:{id} room)",
         rad=-0.20, label_offset=(0.6, 0.4))

    # 5) Marketplace -> Messages : context_type='marketplace' DM
    flow("Marketplace", "bottom", "Messages", "top",
         "context_type='marketplace' DM",
         rad=0.10, label_offset=(1.2, 0.0))

    # ------------------------------------------------------------------
    # Substrate layers (4 horizontal bars below the modules)
    # ------------------------------------------------------------------
    layers = [
        {
            "name": ".edu Identity layer",
            "fill": "#1A5276", "fontcolor": "white",
            "sub": ("authoritative @cornell.edu issuance  -  "
                    "JWT bearer  -  guest fallback  -  "
                    "170/184 verified (92.4%)"),
        },
        {
            "name": "Notification + Socket.IO substrate",
            "fill": "#1E8449", "fontcolor": "white",
            "sub": ("Socket.IO server (rooms: user / activity / thread / ride) "
                    "-  notification.service  -  Redis adapter  -  "
                    "54 notifications across 10 event types"),
        },
        {
            "name": "Supabase Postgres + RLS",
            "fill": "#7D3C98", "fontcolor": "white",
            "sub": ("project bwimyvkwkenrtumsfjzt  -  RLS-scoped tables  -  "
                    "RPC: increment_user_points, calculate_distance  -  "
                    "Storage (avatars, listings)"),
        },
        {
            "name": "WeChat outreach pipeline",
            "fill": "#B7950B", "fontcolor": "white",
            "sub": ("wechat-link.service  -  short-link + H5 fallback  -  "
                    "cron poller -> wxgroup_notice_record  -  "
                    "82 pushes (62 marketplace / 16 ride / 4 activity)"),
        },
    ]

    layer_top = 7.5
    layer_h = 1.30
    layer_gap = 0.25
    for i, layer in enumerate(layers):
        y = layer_top - i * (layer_h + layer_gap)
        bar = FancyBboxPatch(
            (1.6, y - layer_h), 26.8, layer_h,
            boxstyle="round,pad=0.02,rounding_size=0.18",
            linewidth=1.4, edgecolor="#1A1A1A",
            facecolor=layer["fill"], alpha=0.95, zorder=4,
        )
        ax.add_patch(bar)
        ax.text(
            2.2, y - 0.40, "<<substrate>>",
            fontsize=8.5, color=layer["fontcolor"], style="italic",
            ha="left", va="center", zorder=6, alpha=0.9,
        )
        ax.text(
            2.2, y - 0.78, layer["name"],
            fontsize=12, color=layer["fontcolor"], fontweight="bold",
            ha="left", va="center", zorder=6,
        )
        ax.text(
            27.8, y - 0.65, layer["sub"],
            fontsize=8.2, color="white", style="italic",
            ha="right", va="center", zorder=6, alpha=0.95,
        )

    # ------------------------------------------------------------------
    # Bus-style edges from modules down to the substrate stack.
    # We draw a single short stub from each module bottom into the top
    # substrate bar to convey "all modules sit on these layers".
    # ------------------------------------------------------------------
    substrate_top_y = 7.5  # top of first substrate bar
    for name in ("Groups", "Messages", "Points"):
        x, y = modules[name]["pos"]
        cx = x + mod_w / 2
        ax.add_line(Line2D(
            [cx, cx], [y, substrate_top_y],
            color="#566573", linewidth=1.0, linestyle=(0, (2, 2)),
            zorder=3.5,
        ))

    # ------------------------------------------------------------------
    # Mark the Marketplace -> WeChat substrate flow specifically.
    # ------------------------------------------------------------------
    # WeChat substrate is the 4th layer (bottom).
    wechat_y_top = layer_top - 3 * (layer_h + layer_gap)
    mx, my = edge_point("Marketplace", "bottom")
    arrow = FancyArrowPatch(
        (mx, my), (mx, wechat_y_top),
        arrowstyle="-|>", mutation_scale=14,
        linewidth=1.6, color="#B7950B",
        connectionstyle="arc3,rad=0.0", zorder=7,
    )
    ax.add_patch(arrow)
    ax.text(
        mx + 0.25, (my + wechat_y_top) / 2,
        "62 marketplace\noutreach pushes",
        fontsize=8.4, color="#7D6608", fontweight="bold",
        ha="left", va="center",
        bbox=dict(facecolor="white", edgecolor="#B7950B",
                  boxstyle="round,pad=0.20", linewidth=0.8, alpha=0.95),
        zorder=8,
    )

    # ------------------------------------------------------------------
    # Legend (lower-left within figure margin)
    # ------------------------------------------------------------------
    legend_handles = [
        mpatches.Patch(facecolor=MODULE_COLORS["Carpool"],
                       edgecolor="#1A1A1A", label="«block»  module"),
        Line2D([0], [0], color="#34495E", linewidth=1.4,
               label="port-to-port flow"),
        Line2D([0], [0], color="#7D6608", linewidth=1.4, linestyle="--",
               label="designed but inert (no production rows)"),
        mpatches.Patch(facecolor=MODULE_COLORS["Points"], alpha=0.30,
                       edgecolor=MODULE_COLORS["Points"],
                       label="Points overlay (cross-module meta-layer)"),
        mpatches.Patch(facecolor="#1A5276", edgecolor="#1A1A1A",
                       label="«substrate»  shared layer"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left", bbox_to_anchor=(0.025, 0.012),
        frameon=True, fontsize=9.0, handlelength=1.6,
        handletextpad=0.7, ncol=5, columnspacing=1.2,
        framealpha=0.95, edgecolor="#566573",
    )

    plt.tight_layout(pad=0.4)

    pdf, png = save_mpl("mbse_ibd_system_internals", dpi=300)
    register("mbse_ibd_system_internals", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
