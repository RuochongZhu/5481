"""mbse_usecase_request_ride — Use-case diagram for the request-ride flow.

UML use-case style: stick-figure actors flank a system boundary; navy ovals
inside the boundary capture user-visible goals. Dashed arrows label
«include» and «extend» relationships. One use case is highlighted with the
accent colour to anchor the design intent.

Style contract: scripts/_mbe_style_guide.md (§1, §4 "Use case", §7).
Reference implementation: scripts/mbe_c1_booking_fanout.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, DRIVER_COLOR, RIDER_COLOR,
)


# Palette anchors (matches §1)
NAVY = "#1A5276"          # use-case ovals (the platform's responsibilities)
ACCENT_COLOR = "#F39C12"  # one highlighted use case
GREY = "#566573"          # system boundary, neutral lines, subtitle
INK = "#1B2631"           # body text


@renderer("mbse_usecase_request_ride")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 8.0))
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 16)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------
    # System boundary (rounded rectangle)
    # ------------------------------------------------------------------
    sys_x, sys_y, sys_w, sys_h = 6.0, 1.8, 16.0, 11.6
    ax.add_patch(
        FancyBboxPatch(
            (sys_x, sys_y), sys_w, sys_h,
            boxstyle="round,pad=0.10,rounding_size=0.30",
            facecolor="white", edgecolor=GREY, linewidth=1.4,
        )
    )
    ax.text(
        sys_x + sys_w / 2, sys_y + sys_h - 0.55,
        "Carpool system",
        ha="center", va="center",
        fontsize=11, fontweight="bold", color=GREY,
    )

    # ------------------------------------------------------------------
    # Stick-figure actor helper
    # ------------------------------------------------------------------
    def stick_figure(cx, cy, label, role_note, color):
        """Draw a stick figure centred at cx with feet at cy. Returns
        a dict of useful anchor points along the body."""
        head_r = 0.34
        head_y = cy + 2.30
        ax.add_patch(
            Ellipse((cx, head_y), 2 * head_r, 2 * head_r,
                    facecolor="white", edgecolor=color, linewidth=1.6)
        )
        # body
        ax.plot([cx, cx], [cy + 1.95, cy + 0.85],
                color=color, linewidth=1.6, solid_capstyle="round")
        # arms
        ax.plot([cx - 0.60, cx + 0.60], [cy + 1.45, cy + 1.45],
                color=color, linewidth=1.6, solid_capstyle="round")
        # legs
        ax.plot([cx, cx - 0.50], [cy + 0.85, cy],
                color=color, linewidth=1.6, solid_capstyle="round")
        ax.plot([cx, cx + 0.50], [cy + 0.85, cy],
                color=color, linewidth=1.6, solid_capstyle="round")
        # label
        ax.text(cx, cy - 0.35, label,
                ha="center", va="top",
                fontsize=11, fontweight="bold", color=color)
        if role_note:
            ax.text(cx, cy - 0.85, role_note,
                    ha="center", va="top",
                    fontsize=9, style="italic", color=GREY)
        return {
            "right": (cx + 0.60, cy + 1.45),
            "left":  (cx - 0.60, cy + 1.45),
        }

    # Three actors. Passenger and the verified user (a generalisation that
    # both actors specialise) sit on the LEFT; the driver sits on the RIGHT.
    rider = stick_figure(2.6, 11.0, "Passenger", "(rider)", RIDER_COLOR)
    verified = stick_figure(2.6, 4.6,
                            "Verified Cornell\nuser",
                            "(generalised actor)", GREY)
    driver = stick_figure(25.4, 7.8, "Driver", "(host)", DRIVER_COLOR)

    # ------------------------------------------------------------------
    # Use-case ovals
    # ------------------------------------------------------------------
    UC_W, UC_H = 4.2, 1.5

    def use_case(cx, cy, text, *, accent=False):
        ec = ACCENT_COLOR if accent else NAVY
        fc = "#FEF5E7" if accent else "white"
        lw = 1.8 if accent else 1.4
        ax.add_patch(
            Ellipse((cx, cy), UC_W, UC_H,
                    facecolor=fc, edgecolor=ec, linewidth=lw)
        )
        ax.text(cx, cy, text, ha="center", va="center",
                fontsize=10, color=INK,
                fontweight="bold" if accent else "normal")
        a, b = UC_W / 2, UC_H / 2
        return {
            "left":   (cx - a, cy),
            "right":  (cx + a, cy),
            "top":    (cx, cy + b),
            "bottom": (cx, cy - b),
            "center": (cx, cy),
        }

    # Vertically stacked ovals down the centre of the boundary.
    uc_find    = use_case(14.0, 11.4, "Find a ride")
    uc_book    = use_case(14.0,  8.6, "Book a seat", accent=True)
    uc_notify  = use_case(14.0,  5.8, "Receive notification")
    uc_rate    = use_case(14.0,  3.0, "Rate a trip")

    # ------------------------------------------------------------------
    # Solid actor associations (no arrowhead, plain line — UML convention)
    # ------------------------------------------------------------------
    def assoc(p0, p1, color):
        ax.add_patch(FancyArrowPatch(
            p0, p1, arrowstyle="-", color=color,
            linewidth=1.2, mutation_scale=8, alpha=0.85,
        ))

    # Passenger participates in find / book / notify / rate
    assoc(rider["right"], uc_find["left"], RIDER_COLOR)
    assoc(rider["right"], uc_book["left"], RIDER_COLOR)
    assoc(rider["right"], uc_notify["left"], RIDER_COLOR)
    assoc(rider["right"], uc_rate["left"], RIDER_COLOR)

    # Driver participates in find (offers it) / notify / rate
    assoc(driver["left"], uc_find["right"], DRIVER_COLOR)
    assoc(driver["left"], uc_notify["right"], DRIVER_COLOR)
    assoc(driver["left"], uc_rate["right"], DRIVER_COLOR)

    # Verified Cornell user is the generalised actor: passenger and driver
    # both specialise it. UML convention uses a hollow-triangle arrow (here
    # approximated with -|>) pointing FROM the specialised role TO the
    # generalised role. We route the line off to the side of the body so it
    # does not cross the stick-figure trunk.
    ax.add_patch(FancyArrowPatch(
        (rider["right"][0] - 1.20, rider["right"][1] - 1.60),
        (verified["right"][0] - 0.20, verified["right"][1] + 0.55),
        arrowstyle="-|>", color=GREY, linewidth=1.1,
        mutation_scale=14, alpha=0.85, linestyle=(0, (4, 2)),
        connectionstyle="arc3,rad=-0.30",
    ))
    ax.text(0.55, 8.0, "generalises",
            ha="center", va="center", rotation=90,
            fontsize=8.5, style="italic", color=GREY)

    # ------------------------------------------------------------------
    # «include» / «extend» dashed arrows between use cases
    # ------------------------------------------------------------------
    def stereotype_arrow(p0, p1, label, *, label_xy,
                         connectionstyle="arc3,rad=0.0"):
        ax.add_patch(FancyArrowPatch(
            p0, p1, arrowstyle="-|>", color=GREY,
            linewidth=1.2, linestyle="--", mutation_scale=12,
            connectionstyle=connectionstyle,
        ))
        ax.text(label_xy[0], label_xy[1], label,
                ha="center", va="center",
                fontsize=9, color=GREY, style="italic",
                bbox=dict(facecolor="white", edgecolor="none",
                          boxstyle="round,pad=0.18", alpha=0.95))

    # Book a seat «include» Find a ride (booking presupposes a found ride)
    stereotype_arrow(uc_book["top"], uc_find["bottom"],
                     "<<include>>",
                     label_xy=(15.7, 10.0),
                     connectionstyle="arc3,rad=0.0")

    # Receive notification «include» Book a seat (booking always notifies)
    stereotype_arrow(uc_notify["top"], uc_book["bottom"],
                     "<<include>>",
                     label_xy=(15.7, 7.2),
                     connectionstyle="arc3,rad=0.0")

    # Rate a trip «extend» Receive notification (rating is prompted but
    # optional — passenger may dismiss the prompt)
    stereotype_arrow(uc_rate["top"], uc_notify["bottom"],
                     "<<extend>>",
                     label_xy=(15.7, 4.4),
                     connectionstyle="arc3,rad=0.0")

    # ------------------------------------------------------------------
    # Title + italic subtitle (design intent)
    # ------------------------------------------------------------------
    ax.set_title(
        "Use-case view: requesting a carpool ride",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        14.0, 14.6,
        "Booking is the load-bearing goal; rating is an opt-in extension "
        "deferred to after the trip.",
        ha="center", va="center", fontsize=10, style="italic",
        color=GREY,
    )

    pdf, png = save_mpl("mbse_usecase_request_ride", dpi=300)
    register("mbse_usecase_request_ride", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
