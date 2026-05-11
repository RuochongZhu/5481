"""mbse_component_diagram - Component view of CampusRide.

Paper-ready block diagram. Three logical tiers (people, platform services,
shared substrates), each rendered as a band of plain-English service blocks.
Arrows are concept-level flows ("sign in", "open trip-bound chat on booking",
"send notification"), not interface lollipops or socket names.

Style contract: see scripts/_mbe_style_guide.md. No controller / service
identifiers, no .js suffixes, no IJWTAuth-style interface tokens, no UML
package stereotypes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, DRIVER_COLOR, RIDER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"
NEUTRAL = "#566573"


@renderer("mbse_component_diagram")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 9.0))

    # ------------------------------------------------------------------
    # Canvas geometry
    # ------------------------------------------------------------------
    X_MIN, X_MAX = 0.0, 16.5

    # Three tier bands stacked vertically.
    # (y_center, height, label, accent-color)
    TIERS = [
        (8.7, 1.6, "People who use the platform",        NEUTRAL),
        (5.5, 3.2, "Platform services (one campus app)", PLATFORM_COLOR),
        (1.8, 1.9, "Shared substrates and outreach",     NEUTRAL),
    ]

    band_colors = ["#EAF2F8", "#FBEEE6", "#F4F6F7"]
    band_borders = ["#AEB6BF", "#E59866", "#AEB6BF"]
    for (y, h, label, _), bc, bb in zip(TIERS, band_colors, band_borders):
        ax.add_patch(
            FancyBboxPatch(
                (X_MIN + 0.1, y - h / 2),
                X_MAX - X_MIN - 0.2, h,
                boxstyle="round,pad=0.02",
                facecolor=bc, edgecolor=bb,
                alpha=0.45, linewidth=0.8,
            )
        )
        ax.text(
            X_MIN + 0.3, y + h / 2 - 0.22,
            label,
            ha="left", va="top",
            fontsize=11, fontweight="bold", color=bb,
            style="italic",
        )

    # ------------------------------------------------------------------
    # Card / arrow helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, edge, *, fc="white", fs=10.5,
             bold=False, lw=1.4, ls="-"):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=edge, linewidth=lw, linestyle=ls,
            )
        )
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color="#1B2631",
            fontweight="bold" if bold else "normal",
        )

    def arrow(x0, y0, x1, y1, color, *, lw=1.2, ls="-"):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle="-|>", color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=12,
            )
        )

    def edge_label(x, y, text, color=NEUTRAL, fs=8.5):
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color=color, style="italic",
            bbox=dict(boxstyle="round,pad=0.18",
                      facecolor="white", edgecolor="none", alpha=0.9),
        )

    # ------------------------------------------------------------------
    # Tier 1 - Actors (clients)
    # ------------------------------------------------------------------
    cy = TIERS[0][0]
    card(4.6, cy, 3.6, 0.95,
         "Rider\n(verified Cornell student)",
         RIDER_COLOR, fc="#EAF2F8", bold=True)
    card(11.9, cy, 3.6, 0.95,
         "Driver\n(verified Cornell student)",
         DRIVER_COLOR, fc="#FDEDEC", bold=True)

    # ------------------------------------------------------------------
    # Tier 2 - Platform services
    # ------------------------------------------------------------------
    sy = TIERS[1][0]

    # Top-of-tier: gatekeeper that all traffic crosses first.
    card(8.25, sy + 1.30, 6.0, 0.85,
         "Identity verification (verified-only access)",
         PLATFORM_COLOR, bold=True)

    # Middle row: four user-facing services.
    svc_y = sy + 0.0
    card(2.7, svc_y, 2.8, 1.05,
         "Carpool service\n(publish & join trips)",
         PLATFORM_COLOR, bold=True)
    card(6.0, svc_y, 2.6, 1.05,
         "Marketplace service\n(listings & inquiries)",
         PLATFORM_COLOR)
    card(9.2, svc_y, 2.6, 1.05,
         "Activities service\n(events & check-in)",
         PLATFORM_COLOR)
    card(12.7, svc_y, 3.4, 1.05,
         "Groups & trip-bound chat\n(short-lived conversations)",
         PLATFORM_COLOR)

    # Bottom row of tier 2: cross-cutting services.
    cross_y = sy - 1.05
    # Highlight: rating service (design contribution - deferred two-sided window)
    card(3.4, cross_y, 3.6, 0.85,
         "Rating service\n(deferred two-sided window)",
         ACCENT_COLOR, fc="#FEF5E7", bold=True, lw=1.8)
    card(8.0, cross_y, 3.4, 0.85,
         "Messaging service\n(direct messages)",
         PLATFORM_COLOR)
    card(12.5, cross_y, 3.6, 0.85,
         "Points ledger\n(not yet provisioned)",
         NEUTRAL, fs=10, lw=1.2, ls="--")

    # ------------------------------------------------------------------
    # Tier 3 - Shared substrates and outreach
    # ------------------------------------------------------------------
    by = TIERS[2][0]
    card(3.0, by, 3.8, 1.0,
         "Real-time substrate\n(notifications & live rooms)",
         NEUTRAL, bold=True)
    card(8.0, by, 3.4, 1.0,
         "Email service\n(verification mail)",
         NEUTRAL)
    card(12.7, by, 3.6, 1.0,
         "External outreach\n(WeChat post queue)",
         NEUTRAL)

    # ------------------------------------------------------------------
    # Arrows: tier 1 -> tier 2 (rider / driver enter through identity check)
    # ------------------------------------------------------------------
    auth_top = sy + 1.30 + 0.45
    arrow(4.6, cy - 0.5, 6.5, auth_top, RIDER_COLOR)
    arrow(11.9, cy - 0.5, 10.0, auth_top, DRIVER_COLOR)
    edge_label(5.0, (cy - 0.5 + auth_top) / 2,
               "sign in", color=RIDER_COLOR)
    edge_label(11.5, (cy - 0.5 + auth_top) / 2,
               "sign in", color=DRIVER_COLOR)

    # ------------------------------------------------------------------
    # Arrows: identity -> each user-facing service (fan-out)
    # ------------------------------------------------------------------
    auth_bot = sy + 1.30 - 0.45
    for sx in (2.7, 6.0, 9.2, 12.7):
        arrow(8.25 + (sx - 8.25) * 0.30, auth_bot - 0.05,
              sx, svc_y + 0.55, PLATFORM_COLOR, ls="--")

    # ------------------------------------------------------------------
    # Concept-level flows between services (dotted; same-tier)
    # ------------------------------------------------------------------
    # Carpool -> Groups & trip-bound chat. Route as a curve that bulges
    # UPWARD into the strip between identity verification and service row.
    ax.add_patch(
        FancyArrowPatch(
            (2.7 + 1.4, svc_y + 0.40), (12.7 - 1.7, svc_y + 0.40),
            arrowstyle="-|>", color=PLATFORM_COLOR,
            linewidth=1.2, linestyle=":",
            mutation_scale=12,
            connectionstyle="arc3,rad=-0.18",
        )
    )
    edge_label(7.7, svc_y + 0.85,
               "open trip-bound chat on booking")

    # Carpool -> Rating service (after trip ends)
    arrow(2.7 - 0.6, svc_y - 0.55, 3.4 - 0.6, cross_y + 0.45, ACCENT_COLOR)
    edge_label(1.8, (svc_y - 0.55 + cross_y + 0.45) / 2,
               "after trip ends", color=ACCENT_COLOR)

    # Marketplace / Activities -> Messaging
    arrow(6.0 + 0.6, svc_y - 0.55, 7.4, cross_y + 0.45,
          PLATFORM_COLOR, ls="--")
    arrow(9.2 - 0.6, svc_y - 0.55, 8.6, cross_y + 0.45,
          PLATFORM_COLOR, ls="--")
    edge_label(8.0, (svc_y - 0.55 + cross_y + 0.45) / 2,
               "contact each other")

    # Groups & trip-bound chat -> Points ledger (planned)
    arrow(12.7, svc_y - 0.55, 12.5, cross_y + 0.45,
          NEUTRAL, ls=":")
    edge_label(13.6, (svc_y - 0.55 + cross_y + 0.45) / 2,
               "earn points\n(planned)", color=NEUTRAL)

    # ------------------------------------------------------------------
    # Tier 2 -> Tier 3 (push to shared substrates)
    # ------------------------------------------------------------------
    # Rating + Messaging both push to the real-time substrate.
    arrow(3.4 - 0.4, cross_y - 0.45, 3.0 - 0.4, by + 0.5, NEUTRAL)
    edge_label(2.3, (cross_y - 0.45 + by + 0.5) / 2,
               "send notification")
    arrow(8.0 - 0.4, cross_y - 0.45, 3.4, by + 0.5,
          NEUTRAL, ls="--")

    # Identity verification -> Email service (long vertical drop on the right
    # side of the identity block, away from the trip-bound-chat arc).
    arrow(8.25 + 1.5, sy + 0.95 - 0.45, 8.0 + 0.4, by + 0.5, NEUTRAL)
    edge_label(9.5, (sy + 0.95 - 0.45 + by + 0.5) / 2,
               "send verification mail")

    # External outreach (WeChat post queue) sourced from the trip-bound chat.
    arrow(12.7 + 0.6, cross_y + 0.45 - 0.10, 12.7 + 0.6, by + 0.5,
          NEUTRAL, ls="--")
    edge_label(14.0, (cross_y - 0.20 + by + 0.5) / 2,
               "post to external chat")

    # ------------------------------------------------------------------
    # Title + italic subtitle (design intent)
    # ------------------------------------------------------------------
    ax.set_title(
        "Component view of CampusRide",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 10.0,
        "All traffic clears identity verification first; carpool, marketplace, "
        "activities, and groups share one rating, messaging, and notification "
        "substrate.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Cosmetic
    # ------------------------------------------------------------------
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(0.4, 10.4)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbse_component_diagram", dpi=300)
    register("mbse_component_diagram", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
