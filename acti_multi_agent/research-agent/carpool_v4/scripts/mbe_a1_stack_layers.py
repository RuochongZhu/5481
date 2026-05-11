"""mbe_a1 — CampusRide stack layers (paper-style block diagram).

Four horizontal tiers (Client / API gateway / Service layer / Data tier)
with a right-side cluster of sidecars (real-time substrate, email,
external WeChat link). Snapshot row counts annotate the data tier as
findings (not implementation). The trip-booking entrypoint is highlighted
on the service tier as the central design artifact.

Style contract: see scripts/_mbe_style_guide.md. No file paths, no version
numbers, no route prefixes, no underscored table names.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import setup_mpl, save_mpl, register, renderer  # noqa: E402


# Tier palette (paper style: white cards over light tier-bands)
PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"
NEUTRAL = "#566573"

CLIENT_BAND = "#D6EAF8"
GATEWAY_BAND = "#D5F5E3"
SERVICE_BAND = "#FAE5D3"
DATA_BAND = "#E8DAEF"
SIDECAR_BAND = "#FCF3CF"

CLIENT_BORDER = "#2874A6"
GATEWAY_BORDER = "#229954"
SERVICE_BORDER = "#CA6F1E"
DATA_BORDER = "#7D3C98"
SIDECAR_BORDER = "#B7950B"


@renderer("mbe_a1_stack_layers")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 9.0))

    # ------------------------------------------------------------------
    # Canvas geometry
    # ------------------------------------------------------------------
    X_MIN, X_MAX = 0.0, 16.5
    MAIN_RIGHT = 11.6      # main column ends here; sidecars sit to the right
    SIDECAR_LEFT = 12.2

    # Tier vertical layout (top -> bottom: Client, Gateway, Service, Data)
    TIERS = [
        # (y_center, height, label, band_color, border_color)
        (8.6, 1.5, "Client tier",      CLIENT_BAND,  CLIENT_BORDER),
        (6.7, 1.3, "API gateway tier", GATEWAY_BAND, GATEWAY_BORDER),
        (4.6, 1.7, "Service layer",    SERVICE_BAND, SERVICE_BORDER),
        (2.2, 1.9, "Data tier",        DATA_BAND,    DATA_BORDER),
    ]

    # Draw tier bands across the main column only
    for y, h, label, band, border in TIERS:
        ax.add_patch(
            FancyBboxPatch(
                (X_MIN + 0.1, y - h / 2),
                MAIN_RIGHT - X_MIN - 0.1, h,
                boxstyle="round,pad=0.02",
                facecolor=band, edgecolor=border,
                alpha=0.45, linewidth=0.9,
            )
        )
        ax.text(
            X_MIN + 0.25, y + h / 2 - 0.18,
            label,
            ha="left", va="top",
            fontsize=11, fontweight="bold", color=border,
        )

    # Sidecar band (right column, spans gateway-through-data height)
    sc_y_top = TIERS[1][0] + TIERS[1][1] / 2
    sc_y_bot = TIERS[3][0] - TIERS[3][1] / 2
    sc_h = sc_y_top - sc_y_bot
    sc_y_center = (sc_y_top + sc_y_bot) / 2
    ax.add_patch(
        FancyBboxPatch(
            (SIDECAR_LEFT, sc_y_bot),
            X_MAX - SIDECAR_LEFT - 0.1, sc_h,
            boxstyle="round,pad=0.02",
            facecolor=SIDECAR_BAND, edgecolor=SIDECAR_BORDER,
            alpha=0.45, linewidth=0.9,
        )
    )
    ax.text(
        SIDECAR_LEFT + 0.2, sc_y_top - 0.18,
        "Sidecars",
        ha="left", va="top",
        fontsize=11, fontweight="bold", color=SIDECAR_BORDER,
    )

    # ------------------------------------------------------------------
    # Card helper
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, border, *, fc="white", fs=10,
             bold=False, lw=1.4):
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

    # ------------------------------------------------------------------
    # Tier 1 — Client (3 cards)
    # ------------------------------------------------------------------
    cy = TIERS[0][0]
    client_cards = [
        (2.6, "Web SPA\n(browser)"),
        (5.7, "Real-time client\n(WebSocket)"),
        (8.8, "WeChat mini-program\nwebview"),
    ]
    for x, label in client_cards:
        card(x, cy, 2.4, 0.85, label, CLIENT_BORDER)

    # ------------------------------------------------------------------
    # Tier 2 — API gateway (2 cards)
    # ------------------------------------------------------------------
    gy = TIERS[1][0]
    card(3.5, gy, 3.0, 0.85,
         "HTTP API gateway\n(auth, CORS, rate-limit)",
         GATEWAY_BORDER, bold=True)
    card(8.0, gy, 3.0, 0.85,
         "Real-time gateway\n(authenticated rooms)",
         GATEWAY_BORDER, bold=True)

    # ------------------------------------------------------------------
    # Tier 3 — Service layer
    # ------------------------------------------------------------------
    sy = TIERS[2][0]
    # Highlighted central artifact: trip booking entry
    card(2.6, sy + 0.25, 3.0, 0.95,
         "Trip booking entry\n(central design artifact)",
         ACCENT_COLOR, fc="#FEF5E7", bold=True, lw=1.8)
    # Other service-layer responsibilities (concept-level, no controllers/services split)
    card(6.0, sy + 0.25, 2.6, 0.95,
         "Identity &\nverification",
         SERVICE_BORDER)
    card(8.8, sy + 0.25, 2.4, 0.95,
         "Ratings,\npoints, chat",
         SERVICE_BORDER)
    # second row inside service tier
    card(4.3, sy - 0.55, 3.0, 0.6,
         "Trips, listings, activities, groups",
         SERVICE_BORDER, fs=9.5)
    card(8.5, sy - 0.55, 3.0, 0.6,
         "Notifications & outreach",
         SERVICE_BORDER, fs=9.5)
    # Subtitle inside the service tier
    ax.text(
        MAIN_RIGHT - 0.25, sy + 0.78,
        "service layer",
        ha="right", va="center",
        fontsize=9, style="italic", color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Tier 4 — Data
    # ------------------------------------------------------------------
    dy = TIERS[3][0]
    # Main relational store card with snapshot counts as small annotations
    card(4.0, dy + 0.30, 5.4, 1.05,
         "Relational store\n(user accounts, trips, trip bookings,\n"
         "ratings, marketplace listings, groups,\n"
         "messages, notifications, external-post queue)",
         DATA_BORDER, bold=True, fs=9.5)
    card(9.3, dy + 0.30, 3.6, 1.05,
         "Object storage\n(avatars, listing images)",
         DATA_BORDER, fs=10)

    # Snapshot row counts as small annotations *under* the relational card
    snap_y = dy - 0.55
    ax.text(
        4.0, snap_y,
        "Snapshot: 184 verified users  |  5 community groups  |  "
        "22 direct messages  |  82 outbound posts queued",
        ha="center", va="center",
        fontsize=8.5, style="italic", color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Sidecars (right column, vertical stack)
    # ------------------------------------------------------------------
    sc_x = (SIDECAR_LEFT + X_MAX) / 2 - 0.1
    sc_w = X_MAX - SIDECAR_LEFT - 0.6

    # Three sidecars vertically distributed in the sidecar band
    sc_top = sc_y_top - 0.7
    sc_bot = sc_y_bot + 0.4
    sc_positions = [
        (sc_top - 0.0, "Real-time substrate\n(pub/sub for rooms)"),
        ((sc_top + sc_bot) / 2, "Email service\n(verification mail)"),
        (sc_bot + 0.55, "External link API\n(WeChat short link)"),
    ]
    for sy_pos, label in sc_positions:
        card(sc_x, sy_pos, sc_w, 1.0, label, SIDECAR_BORDER, fs=9.5)

    # ------------------------------------------------------------------
    # Cross-tier arrows (vertical, main column)
    # ------------------------------------------------------------------
    cy_bot = cy - 0.45
    gy_top = gy + 0.45
    gy_bot = gy - 0.45
    sy_top = sy + 0.72
    sy_mid_bot = sy - 0.85
    dy_top = dy + 0.82

    # Client -> Gateway
    arrow(2.6, cy_bot, 3.5, gy_top, CLIENT_BORDER)
    arrow(5.7, cy_bot, 7.6, gy_top, CLIENT_BORDER, ls="--")
    arrow(8.8, cy_bot, 4.2, gy_top, CLIENT_BORDER, ls=":")

    # Gateway -> Service
    arrow(3.5, gy_bot, 2.8, sy_top, GATEWAY_BORDER)
    arrow(8.0, gy_bot, 8.6, sy_top, GATEWAY_BORDER, ls="--")

    # Service -> Data (a couple of representative arrows)
    arrow(2.8, sy_mid_bot, 3.5, dy_top, DATA_BORDER)
    arrow(6.2, sy_mid_bot, 4.4, dy_top, DATA_BORDER)
    arrow(8.6, sy_mid_bot, 9.1, dy_top, DATA_BORDER, ls="--")

    # ------------------------------------------------------------------
    # Sidecar arrows (horizontal, into right column)
    # ------------------------------------------------------------------
    # Real-time gateway -> real-time substrate
    arrow(8.0 + 1.5, gy, sc_x - sc_w / 2, sc_positions[0][0],
          SIDECAR_BORDER, ls="--")
    # Service layer (notifications) -> email
    arrow(MAIN_RIGHT - 0.3, sy - 0.55,
          sc_x - sc_w / 2, sc_positions[1][0],
          SIDECAR_BORDER)
    # Service layer (outreach) -> external link API
    arrow(MAIN_RIGHT - 0.3, sy - 0.85,
          sc_x - sc_w / 2, sc_positions[2][0],
          SIDECAR_BORDER, ls="--")

    # ------------------------------------------------------------------
    # Title + italic subtitle (design intent)
    # ------------------------------------------------------------------
    ax.set_title(
        "CampusRide deployed stack — four tiers and three sidecars",
        fontsize=14, fontweight="bold", pad=16,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 9.95,
        "A conventional layered architecture; the trip-booking entry is the "
        "central design artifact, and outreach is decoupled into sidecars.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Cosmetic
    # ------------------------------------------------------------------
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(0.4, 10.3)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_a1_stack_layers", dpi=300)
    register("mbe_a1_stack_layers", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
