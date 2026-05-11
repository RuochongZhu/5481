"""mbe_c2 — Identity verification: a three-phase user journey.

A conceptual user-journey strip (HCI-paper-ready), not an engineering
call-graph. Three temporal phases — sign up, email verify, authenticated
use — with a small dashed parallel branch for guest read-only access.

Design principles:
  - No file/line, no SQL, no JS, no JWT payload literals, no regex.
  - Snapshot numbers (184 / 100% / 170) live in a footnote box, not in
    the primary cards.
  - The two-tier verification model is shown collapsing into a single
    automatic tier (no manual review queue).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, RIDER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"   # verified-badge highlight
NEUTRAL = "#566573"
GHOST = "#B2BABB"          # collapsed/unwired second tier


@renderer("mbe_c2_identity_verification_flow")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 6.6))

    X_MIN, X_MAX = 0.0, 16.5

    # ------------------------------------------------------------------
    # Y geometry
    # ------------------------------------------------------------------
    Y_GUEST = 4.6     # parallel guest branch (above main flow)
    Y_MAIN = 2.7      # primary user-journey strip
    Y_TIER = 1.45     # collapsed second-tier indicator
    Y_AXIS = 0.55     # phase labels (a)/(b)/(c)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, color, *, fc="white", fs=10.0,
             bold=False, alpha=1.0, ls="-"):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=color,
                linewidth=1.4, alpha=alpha, linestyle=ls,
            )
        )
        ax.text(
            x, y, text,
            ha="center", va="center", fontsize=fs,
            color="#1B2631",
            fontweight="bold" if bold else "normal",
            wrap=True,
        )

    def arrow(x0, y0, x1, y1, color, *, lw=1.4, ls="-",
              style="-|>", ms=12):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle=style, color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=ms,
            )
        )

    # ------------------------------------------------------------------
    # Phase backdrop bands: (a) sign up | (b) verify | (c) authenticated
    # ------------------------------------------------------------------
    PHASES = [
        ("(a) Sign up",          1.2,  5.7,  RIDER_COLOR),
        ("(b) Email verify",     5.9,  10.7, ACCENT_COLOR),
        ("(c) Authenticated use", 10.9, 16.3, PLATFORM_COLOR),
    ]
    band_top, band_bot = 5.7, 1.05
    for label, x0, x1, color in PHASES:
        ax.add_patch(
            FancyBboxPatch(
                (x0, band_bot),
                x1 - x0, band_top - band_bot,
                boxstyle="round,pad=0.02",
                facecolor=color, alpha=0.06,
                edgecolor=color, linewidth=0.8,
            )
        )
        ax.text(
            (x0 + x1) / 2, band_top - 0.22, label,
            ha="center", va="top", fontsize=11,
            fontweight="bold", color=color,
        )

    # ------------------------------------------------------------------
    # Main journey cards (left to right)
    # ------------------------------------------------------------------
    # 1. Cornell student opens the app
    card(2.6, Y_MAIN, 2.4, 0.85,
         "Student opens app\nenters Cornell email",
         RIDER_COLOR, bold=True)

    # 2. Platform performs the .edu check (the contribution: identity primitive)
    card(5.0, Y_MAIN, 2.0, 0.85,
         "Cornell email check\n(automatic)",
         PLATFORM_COLOR)
    arrow(3.85, Y_MAIN, 3.95, Y_MAIN, NEUTRAL)

    # 3. Verification email sent (accent-highlighted: the design pivot)
    card(7.6, Y_MAIN, 2.4, 0.85,
         "Verification email\nsent to inbox",
         ACCENT_COLOR, fc="#FEF5E7", bold=True)
    arrow(6.05, Y_MAIN, 6.35, Y_MAIN, PLATFORM_COLOR)

    # 4. User taps the link
    card(10.0, Y_MAIN, 2.0, 0.85,
         "User taps\nverification link",
         RIDER_COLOR)
    arrow(8.85, Y_MAIN, 8.95, Y_MAIN, ACCENT_COLOR)

    # 5. Verified badge granted -> authenticated session
    card(13.0, Y_MAIN, 2.6, 0.95,
         "Verified badge granted\nAuthenticated session",
         PLATFORM_COLOR, bold=True)
    arrow(11.05, Y_MAIN, 11.65, Y_MAIN, ACCENT_COLOR, lw=1.8)

    # Small accent badge tag near the final card
    ax.add_patch(
        FancyBboxPatch(
            (13.0 - 0.55, Y_MAIN + 0.62), 1.1, 0.32,
            boxstyle="round,pad=0.02",
            facecolor=ACCENT_COLOR, edgecolor=ACCENT_COLOR,
            linewidth=1.0,
        )
    )
    ax.text(
        13.0, Y_MAIN + 0.78, "verified",
        ha="center", va="center", fontsize=9,
        fontweight="bold", color="white",
    )

    # 6. Continued authenticated platform use (terminal hint)
    card(15.5, Y_MAIN, 1.5, 0.85,
         "Books rides,\nposts, chats",
         PLATFORM_COLOR)
    arrow(14.35, Y_MAIN, 14.7, Y_MAIN, PLATFORM_COLOR)

    # ------------------------------------------------------------------
    # Collapsed second tier (manual review never wired up)
    # ------------------------------------------------------------------
    card(7.6, Y_TIER, 5.0, 0.7,
         "Designed second tier: manual review queue  —  not wired in production",
         GHOST, fc="#F4F6F7", ls="--", fs=9.5)
    # Dotted descender from the .edu check to the ghost tier
    arrow(5.0, Y_MAIN - 0.45, 5.6, Y_TIER + 0.32,
          GHOST, ls=":", lw=1.0, ms=10)
    # Dotted reconnector showing it would have flowed back into authenticated use
    arrow(9.9, Y_TIER + 0.32, 12.0, Y_MAIN - 0.5,
          GHOST, ls=":", lw=1.0, ms=10)

    # ------------------------------------------------------------------
    # Parallel guest branch (above the main strip)
    # ------------------------------------------------------------------
    card(2.6, Y_GUEST, 2.4, 0.7,
         "Visitor opens app\n(no Cornell email)",
         NEUTRAL, fc="#F8F9F9", ls="--", fs=9.5)
    card(7.6, Y_GUEST, 3.0, 0.7,
         "Guest read-only access\n(browse, no booking)",
         NEUTRAL, fc="#F8F9F9", ls="--", fs=9.5)
    card(13.0, Y_GUEST, 2.6, 0.7,
         "Read-only browsing\ncontinues",
         NEUTRAL, fc="#F8F9F9", ls="--", fs=9.5)
    arrow(3.85, Y_GUEST, 6.05, Y_GUEST, NEUTRAL, ls="--", lw=1.0)
    arrow(9.15, Y_GUEST, 11.65, Y_GUEST, NEUTRAL, ls="--", lw=1.0)

    # Small label for the guest lane (tucked into left margin)
    ax.text(
        0.15, Y_GUEST, "Guest\nbranch",
        ha="left", va="center", fontsize=9.5,
        style="italic", color=NEUTRAL,
    )
    ax.text(
        0.15, Y_MAIN, "Verified\njourney",
        ha="left", va="center", fontsize=9.5,
        style="italic", color=PLATFORM_COLOR, fontweight="bold",
    )

    # ------------------------------------------------------------------
    # Snapshot footnote box (numbers are findings, kept in figure)
    # ------------------------------------------------------------------
    fn_y = -0.25
    ax.add_patch(
        FancyBboxPatch(
            (0.4, fn_y - 0.45), X_MAX - 0.8, 0.85,
            boxstyle="round,pad=0.02",
            facecolor="#FEF9E7", edgecolor="#7D6608",
            linewidth=0.9,
        )
    )
    ax.text(
        (X_MAX) / 2, fn_y,
        "Production snapshot (April 2026):  184 registered users   "
        "100% Cornell email   170 verified (92.4%).   "
        "The designed two-tier model collapses to one automatic tier "
        "in practice — no manual review queue is wired up.",
        ha="center", va="center", fontsize=9.5, color="#7D6608",
    )

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Identity verification as a three-phase user journey",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MAX) / 2, 6.15,
        "Cornell email is the only identity primitive; "
        "guests retain a parallel read-only branch.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.95, 6.4)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_c2_identity_verification_flow", dpi=300)
    register("mbe_c2_identity_verification_flow", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
