"""mbse_bdd_system_context - SysML Block Definition Diagram (system context).

Hub-and-spoke layout: the CampusRide platform sits at the center; human
actors and external systems orbit around it. Edges are labeled with the
concept-level interaction (no SQL, no file paths, no constants spelled
out). Visual contract follows `_mbe_style_guide.md` and the c1 reference.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
    RIDER_COLOR, DRIVER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"
GREY = "#566573"
EXT_FILL = "#FFFFFF"


@renderer("mbse_bdd_system_context")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(-7.8, 7.8)
    ax.set_ylim(-6.4, 6.5)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------
    # Title + subtitle (italic, design intent)
    # ------------------------------------------------------------------
    ax.set_title(
        "CampusRide system context",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        0, 5.55,
        "Identity-verified hub: the platform binds human roles to a small "
        "set of external substrates without leaking implementation detail.",
        ha="center", va="center", fontsize=10, style="italic",
        color=GREY,
    )

    # ------------------------------------------------------------------
    # Helpers (cards + connectors), styled per guide
    # ------------------------------------------------------------------
    def card(cx, cy, w, h, text, color, *, fc="white", fs=9.5,
             bold=False, lw=1.4):
        ax.add_patch(
            FancyBboxPatch(
                (cx - w / 2, cy - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=color, linewidth=lw,
            )
        )
        ax.text(
            cx, cy, text,
            ha="center", va="center",
            fontsize=fs, color="#1B2631",
            fontweight="bold" if bold else "normal",
            wrap=True,
        )

    def connector(p_src, p_dst, color, label=None, *,
                  lw=1.2, ls="-", label_pos=0.55, label_dx=0.0,
                  label_dy=0.0):
        sxp, syp = p_src
        dxp, dyp = p_dst
        ax.add_patch(
            FancyArrowPatch(
                (sxp, syp), (dxp, dyp),
                arrowstyle="-|>", mutation_scale=12,
                linewidth=lw, color=color, linestyle=ls,
            )
        )
        if label:
            lx = sxp + (dxp - sxp) * label_pos + label_dx
            ly = syp + (dyp - syp) * label_pos + label_dy
            ax.text(
                lx, ly, label,
                ha="center", va="center",
                fontsize=8.4, color=color, style="italic",
                bbox=dict(facecolor="white", edgecolor="none",
                          boxstyle="round,pad=0.18", alpha=0.92),
            )

    def edge_point(cx, cy, w, h, target_x, target_y):
        """Return the point on the rectangle border closest to target."""
        dx = target_x - cx
        dy = target_y - cy
        if dx == 0 and dy == 0:
            return cx, cy
        # scale so that |dx|/w_half == 1 OR |dy|/h_half == 1
        wh = w / 2
        hh = h / 2
        sx = wh / abs(dx) if dx != 0 else math.inf
        sy = hh / abs(dy) if dy != 0 else math.inf
        s = min(sx, sy)
        return cx + dx * s, cy + dy * s

    # ------------------------------------------------------------------
    # Center: CampusRide system block
    # ------------------------------------------------------------------
    SYS_W, SYS_H = 3.6, 1.8
    sys_cx, sys_cy = 0.0, 0.0
    ax.add_patch(
        FancyBboxPatch(
            (sys_cx - SYS_W / 2, sys_cy - SYS_H / 2), SYS_W, SYS_H,
            boxstyle="round,pad=0.05",
            facecolor=PLATFORM_COLOR, edgecolor=PLATFORM_COLOR, linewidth=1.8,
        )
    )
    ax.text(
        sys_cx, sys_cy + 0.45, "<<system>>",
        ha="center", va="center", fontsize=9.5, color="#D6EAF8",
        style="italic",
    )
    ax.text(
        sys_cx, sys_cy + 0.05, "CampusRide",
        ha="center", va="center", fontsize=15, fontweight="bold",
        color="white",
    )
    ax.text(
        sys_cx, sys_cy - 0.42,
        "identity-verified\nmulti-module campus platform",
        ha="center", va="center", fontsize=8.8, color="#EAF2F8",
        style="italic",
    )

    # ------------------------------------------------------------------
    # Spoke specification: name, kind, label, color, polar position
    # kind in {"rider", "driver", "actor", "ext", "accent"}
    # angle in degrees (0 = right, 90 = top, ...).  radius in axis units.
    # ------------------------------------------------------------------
    NODE_W, NODE_H = 2.6, 1.05

    spokes = [
        # Human actors (top half)
        dict(name="Riders", kind="rider", angle=130, radius=4.2,
             label="browse and book trips",
             sub="passenger-side demand"),
        dict(name="Drivers", kind="driver", angle=50, radius=4.2,
             label="publish trips",
             sub="driver-side supply"),
        dict(name="Activity organizers", kind="actor", angle=170, radius=4.6,
             label="post events",
             sub="campus event hosts"),
        dict(name="Marketplace sellers", kind="actor", angle=10, radius=4.6,
             label="list items",
             sub="peer marketplace"),
        # Identity authority - accent (highlights the design pivot)
        dict(name="Cornell email check", kind="accent", angle=90, radius=3.7,
             label="identity verification",
             sub="trust primitive"),
        # External systems (bottom half)
        dict(name="Verification email service", kind="ext", angle=210,
             radius=4.6,
             label="send verification mail",
             sub="transactional email", label_pos=0.55),
        dict(name="External outreach queue", kind="ext", angle=245,
             radius=4.7,
             label="cross-channel posts",
             sub="outreach push channel", label_pos=0.40),
        dict(name="Real-time substrate", kind="ext", angle=295, radius=4.7,
             label="live updates and chat",
             sub="push and sockets", label_pos=0.65),
        dict(name="Postgres data store", kind="ext", angle=330, radius=4.6,
             label="persisted records",
             sub="primary database", label_pos=0.55),
    ]

    # ------------------------------------------------------------------
    # Render spokes
    # ------------------------------------------------------------------
    color_for = {
        "rider": RIDER_COLOR,
        "driver": DRIVER_COLOR,
        "actor": GREY,
        "ext": GREY,
        "accent": ACCENT_COLOR,
    }

    for s in spokes:
        theta = math.radians(s["angle"])
        cx = s["radius"] * math.cos(theta)
        cy = s["radius"] * math.sin(theta)
        col = color_for[s["kind"]]
        fc = "#FEF5E7" if s["kind"] == "accent" else "white"
        bold = s["kind"] in {"rider", "driver", "accent"}
        # Two-line text: title + subtitle
        text = f"{s['name']}\n" + r"$\mathit{" + s["sub"].replace(" ", r"\ ") + "}$"
        # Avoid mathtext rendering of subtitle by drawing as two text calls
        # via a single FancyBboxPatch + two ax.text. Easier: draw card with
        # title only, then add italic subtitle below title.
        ax.add_patch(
            FancyBboxPatch(
                (cx - NODE_W / 2, cy - NODE_H / 2), NODE_W, NODE_H,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=col, linewidth=1.4,
            )
        )
        ax.text(
            cx, cy + 0.18, s["name"],
            ha="center", va="center",
            fontsize=10, fontweight="bold" if bold else "normal",
            color="#1B2631",
        )
        ax.text(
            cx, cy - 0.22, s["sub"],
            ha="center", va="center",
            fontsize=8.6, color=GREY, style="italic",
        )
        # Stereotype tag
        stereo = {
            "rider": "actor",
            "driver": "actor",
            "actor": "actor",
            "ext": "external system",
            "accent": "trust anchor",
        }[s["kind"]]
        ax.text(
            cx, cy + NODE_H / 2 + 0.18, f"<<{stereo}>>",
            ha="center", va="center", fontsize=8.0, color=col,
            style="italic",
        )

        # Connector from center block edge to spoke edge
        src = edge_point(sys_cx, sys_cy, SYS_W, SYS_H, cx, cy)
        dst = edge_point(cx, cy, NODE_W, NODE_H, sys_cx, sys_cy)
        ls = "-"
        lw = 1.6 if s["kind"] == "accent" else 1.2
        edge_color = col if s["kind"] in {"rider", "driver", "accent"} else GREY
        # Stagger label position along the line to reduce crowding among
        # adjacent external-system spokes.
        label_pos = s.get("label_pos", 0.55)
        connector(src, dst, edge_color, label=s["label"], lw=lw, ls=ls,
                  label_pos=label_pos)

    # ------------------------------------------------------------------
    # Cosmetic frame: a faint dashed ring suggests the "ring of context"
    # ------------------------------------------------------------------
    ring = plt.Circle(
        (0, 0), 4.4,
        fill=False, edgecolor=GREY, linewidth=0.6, linestyle=":", alpha=0.4,
    )
    ax.add_patch(ring)

    pdf, png = save_mpl("mbse_bdd_system_context", dpi=300)
    register("mbse_bdd_system_context", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
