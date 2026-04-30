"""mbse_seq_book_ride — UML Sequence Diagram for the bookRide flow.

Six lifelines (vertical bars with name boxes at top), top-to-bottom messages,
activation bars, alt/loop fragment boxes, and async messages with open
arrowheads.

The WeChat Outreach Worker lifeline is rendered faded because it is invoked
only indirectly — it actually fires on createRide, not on bookRide; the
faded "(not in this flow)" annotation makes that scope-correction explicit.

Source-of-truth:
  campusride-backend/src/controllers/carpooling.controller.js:511-709 (bookRide)
  campusride-backend/src/services/notification.service.js:55-150 (sendNotification)
  campusride-backend/src/services/rideCarpoolGroup.service.js:16-72
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import setup_mpl, save_mpl, register, renderer  # noqa: E402


# Palette ---------------------------------------------------------------------
RIDER_COLOR = "#2980B9"
CTRL_COLOR = "#1A5276"
DB_COLOR = "#7D6608"
NOTIF_COLOR = "#117A65"
SOCK_COLOR = "#7D3C98"
WECHAT_COLOR = "#922B21"

LIFELINE_DASH = (0, (4, 3))
ACTIVATION_FILL = "#FBFCFC"

ALT_FRAME = "#9C640C"
LOOP_FRAME = "#117A65"


@renderer("mbse_seq_book_ride")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

    # Larger canvas — sequence diagrams need vertical room
    fig, ax = plt.subplots(figsize=(15, 13))

    # ------------------------------------------------------------------
    # Lifeline definitions — (label, x, color, faded?)
    # ------------------------------------------------------------------
    LIFELINES = [
        ("Rider Browser\n(client)",                    1.5,  RIDER_COLOR,  False),
        ("carpoolingController.bookRide\n(Express)",   4.6,  CTRL_COLOR,   False),
        ("Supabase\nPostgres",                          7.7,  DB_COLOR,     False),
        ("NotificationService",                        10.4, NOTIF_COLOR,  False),
        ("Socket.IO Hub\n(Redis adapter)",             13.0, SOCK_COLOR,   False),
        ("WeChat Outreach\nWorker",                    15.5, WECHAT_COLOR, True),
    ]
    LANE_HALF = 1.15  # half-width of the name box

    X_MIN = 0.0
    X_MAX = max(x for _, x, _, _ in LIFELINES) + LANE_HALF + 0.3

    # Top of name boxes is Y_TOP; messages start below that.
    Y_TOP_BOX = 38.5
    Y_BOX_BOT = 36.5
    Y_BOTTOM = -1.0

    # Lifeline name boxes + dashed vertical lines
    for label, x, color, faded in LIFELINES:
        alpha = 0.30 if faded else 1.0
        ax.add_patch(
            FancyBboxPatch(
                (x - LANE_HALF, Y_BOX_BOT),
                LANE_HALF * 2, Y_TOP_BOX - Y_BOX_BOT,
                boxstyle="round,pad=0.04",
                facecolor="white", edgecolor=color, linewidth=1.8,
                alpha=alpha, zorder=4,
            )
        )
        ax.text(
            x, (Y_TOP_BOX + Y_BOX_BOT) / 2, label,
            ha="center", va="center", fontsize=11, fontweight="bold",
            color=color, alpha=alpha, zorder=5,
        )
        ax.plot(
            [x, x], [Y_BOX_BOT, Y_BOTTOM],
            linestyle=LIFELINE_DASH, color=color, linewidth=1.0,
            alpha=alpha * 0.75, zorder=1,
        )

    # caption above the faded WeChat lane
    ax.text(
        LIFELINES[-1][1], Y_TOP_BOX + 0.45,
        "(faded — not in this flow;\nfires on createRide)",
        ha="center", va="bottom", fontsize=9, style="italic",
        color=WECHAT_COLOR, alpha=0.75,
    )

    # ------------------------------------------------------------------
    # Helper: add an activation bar on a lifeline between y_top..y_bot
    # (y_top > y_bot since y descends down the page)
    # ------------------------------------------------------------------
    def activation(x, y_top, y_bot, color):
        ax.add_patch(
            Rectangle(
                (x - 0.16, y_bot), 0.32, y_top - y_bot,
                facecolor=ACTIVATION_FILL, edgecolor=color,
                linewidth=1.0, zorder=2.5,
            )
        )

    # ------------------------------------------------------------------
    # Helper: horizontal message
    # ------------------------------------------------------------------
    def msg(x0, x1, y, text, *, color="#1B2631", style="solid",
            arrow="-|>", lw=1.5, label_offset=0.30, alpha=1.0,
            fontsize=10, italic=False):
        # Slightly inset the arrow start/end from the activation-bar edge
        sign = 1 if x1 > x0 else -1
        x0a = x0 + sign * 0.16
        x1a = x1 - sign * 0.16
        ax.add_patch(
            FancyArrowPatch(
                (x0a, y), (x1a, y),
                arrowstyle=arrow, color=color, linewidth=lw,
                linestyle=style, mutation_scale=14, alpha=alpha, zorder=3.5,
            )
        )
        ax.text(
            (x0 + x1) / 2, y + label_offset, text,
            ha="center", va="bottom", fontsize=fontsize, color=color,
            alpha=alpha, style="italic" if italic else "normal", zorder=5,
        )

    def self_msg(x, y_top, y_bot, text, *, color="#1B2631"):
        loop_w = 0.8
        ax.add_patch(
            FancyArrowPatch(
                (x + 0.16, y_top), (x + 0.16 + loop_w, y_top),
                arrowstyle="-", color=color, linewidth=1.3, zorder=3.5,
            )
        )
        ax.add_patch(
            FancyArrowPatch(
                (x + 0.16 + loop_w, y_top), (x + 0.16 + loop_w, y_bot),
                arrowstyle="-", color=color, linewidth=1.3, zorder=3.5,
            )
        )
        ax.add_patch(
            FancyArrowPatch(
                (x + 0.16 + loop_w, y_bot), (x + 0.16, y_bot),
                arrowstyle="-|>", color=color, linewidth=1.3,
                mutation_scale=14, zorder=3.5,
            )
        )
        ax.text(
            x + 0.16 + loop_w + 0.18, (y_top + y_bot) / 2, text,
            ha="left", va="center", fontsize=10, color=color, zorder=5,
        )

    # ------------------------------------------------------------------
    # Helper: alt/loop combined fragment
    # ------------------------------------------------------------------
    def fragment(x0, x1, y_top, y_bot, kind, label, *, color=ALT_FRAME):
        ax.add_patch(
            Rectangle(
                (x0, y_bot), x1 - x0, y_top - y_bot,
                facecolor="none", edgecolor=color, linewidth=1.5,
                linestyle=(0, (5, 3)), zorder=1.5,
            )
        )
        # tab in upper-left corner
        tab_w, tab_h = 0.95, 0.45
        ax.add_patch(
            Rectangle(
                (x0, y_top - tab_h), tab_w, tab_h,
                facecolor=color, edgecolor=color, linewidth=1.5,
                zorder=1.7,
            )
        )
        ax.text(
            x0 + tab_w / 2, y_top - tab_h / 2, kind,
            ha="center", va="center", fontsize=10, fontweight="bold",
            color="white", zorder=2,
        )
        # guard label
        ax.text(
            x0 + tab_w + 0.20, y_top - tab_h / 2, f"[{label}]",
            ha="left", va="center", fontsize=9.5, color=color,
            style="italic", zorder=2,
        )

    # ------------------------------------------------------------------
    # X aliases
    # ------------------------------------------------------------------
    x_rider  = LIFELINES[0][1]
    x_ctrl   = LIFELINES[1][1]
    x_db     = LIFELINES[2][1]
    x_notif  = LIFELINES[3][1]
    x_sock   = LIFELINES[4][1]
    # x_wechat = LIFELINES[5][1]  # unused — lifeline only

    # ------------------------------------------------------------------
    # Y schedule — every step gets at least 1.4 units; alt/loop body
    # gets margin so the dashed frame doesn't kiss the messages.
    # Larger y = higher on the page (top).
    # ------------------------------------------------------------------
    DY = 1.5

    # Outer activation: controller is busy from the first inbound POST until
    # the final 200 OK. We compute its top/bottom after laying out msgs.
    y = 35.0

    # 1 — Rider POST -> Controller
    msg(x_rider, x_ctrl, y,
        "POST /api/v1/carpooling/rides/:id/book",
        color=RIDER_COLOR)
    y_ctrl_top = y - 0.05  # controller activation starts at the inbound POST

    # 2 — Controller -> Postgres SELECT (with row lock)
    y -= DY
    msg(x_ctrl, x_db, y,
        "SELECT * FROM rides WHERE id=:id AND status='active'   (row-locked)",
        color=CTRL_COLOR)
    y_sel_top = y + 0.10

    # 3 — return ride row
    y -= DY
    msg(x_db, x_ctrl, y, "ride row",
        color=DB_COLOR, style="dashed", arrow="->")
    y_sel_bot = y - 0.10
    activation(x_db, y_sel_top, y_sel_bot, color=DB_COLOR)

    # 4 — alt: validate seats remaining > 0  (self message + 409 on failure)
    y -= DY * 0.9
    y_alt1_top = y + 0.55
    self_msg(x_ctrl, y + 0.35, y - 0.20,
             "validate seats_remaining > 0", color=CTRL_COLOR)
    y -= DY * 1.05
    msg(x_ctrl, x_rider, y,
        "409 Conflict   (seats_remaining = 0)",
        color=ALT_FRAME, style="dashed", arrow="->", italic=True)
    y_alt1_bot = y - 0.45
    fragment(x_rider - LANE_HALF - 0.05, x_db + LANE_HALF + 0.05,
             y_alt1_top, y_alt1_bot,
             "alt", "seats_remaining = 0", color=ALT_FRAME)

    # 5 — INSERT booking
    y = y_alt1_bot - DY * 0.9
    msg(x_ctrl, x_db, y,
        "INSERT INTO ride_bookings (status='confirmed')",
        color=CTRL_COLOR)
    y_ins_top = y + 0.10
    activation(x_db, y_ins_top, y - 0.10, color=DB_COLOR)

    # 6 — alt: UPDATE rides SET status='full'  (only on last seat)
    y -= DY * 1.2
    y_alt2_top = y + 0.95
    msg(x_ctrl, x_db, y,
        "UPDATE rides SET status='full'", color=CTRL_COLOR)
    activation(x_db, y + 0.10, y - 0.10, color=DB_COLOR)
    y_alt2_bot = y - 0.55
    fragment(x_ctrl - LANE_HALF - 0.05, x_db + LANE_HALF + 0.05,
             y_alt2_top, y_alt2_bot,
             "alt", "last seat just booked", color=ALT_FRAME)

    # 7 — Loop x6 over notification types  (extra gap from alt2)
    # Increase top padding so the loop tab + 6-types sub-line sit above the
    # first arrow without overlap.
    y_loop_top = y_alt2_bot - DY * 1.1
    y = y_loop_top - 2.10  # leave room under the loop tab + sub-label

    msg(x_ctrl, x_notif, y,
        "sendNotification(type, recipient_id, data)",
        color=CTRL_COLOR)
    y_n_top = y + 0.10

    y -= DY
    msg(x_notif, x_db, y,
        "INSERT INTO notifications", color=NOTIF_COLOR)
    activation(x_db, y + 0.10, y - 0.10, color=DB_COLOR)

    y -= DY
    msg(x_notif, x_sock, y,
        "emit('notification', payload)   on   user:{recipient_id}",
        color=NOTIF_COLOR, arrow="->", lw=1.3)  # async open arrowhead
    activation(x_sock, y + 0.10, y - 0.10, color=SOCK_COLOR)
    activation(x_notif, y_n_top, y - 0.20, color=NOTIF_COLOR)

    y_loop_bot = y - 0.55
    fragment(x_ctrl - LANE_HALF - 0.05, x_sock + LANE_HALF + 0.05,
             y_loop_top, y_loop_bot,
             "loop",
             "for each of 6 notification types",
             color=LOOP_FRAME)
    # Sub-line listing the 6 types — placed below the tab band but well
    # above the first message arrow inside the loop body.
    ax.text(
        (x_ctrl + x_sock) / 2, y_loop_top - 0.95,
        "(driver_book,  rider_confirmed,  payment x2,  rating_reminder x2)",
        ha="center", va="top", fontsize=9, style="italic",
        color=LOOP_FRAME, alpha=0.9, zorder=2,
    )

    # 8 — ensureRideCarpoolGroupOnBooking (self call into the co-located
    #     rideCarpoolGroup service — drawn as a self-message on the controller
    #     lane)
    y = y_loop_bot - DY * 0.95
    self_msg(x_ctrl, y + 0.35, y - 0.20,
             "ensureRideCarpoolGroupOnBooking(ride_id, driver_id, rider_id)",
             color=CTRL_COLOR)

    # 9 — INSERT INTO groups (idempotent — silent swallow of 23505)
    y -= DY * 1.1
    msg(x_ctrl, x_db, y,
        "INSERT INTO groups   (idempotent — silent swallow of 23505)",
        color=CTRL_COLOR, italic=True)
    activation(x_db, y + 0.10, y - 0.10, color=DB_COLOR)

    # 10 — INSERT INTO group_members (idempotent, both driver & rider)
    y -= DY
    msg(x_ctrl, x_db, y,
        "INSERT INTO group_members   (driver: 'creator',   rider: 'member')",
        color=CTRL_COLOR, italic=True)
    activation(x_db, y + 0.10, y - 0.10, color=DB_COLOR)

    # 11 — return 200 OK
    y -= DY
    msg(x_ctrl, x_rider, y,
        "200 OK + booking row",
        color=CTRL_COLOR, style="dashed", arrow="->")

    # Outer controller activation bar covers the entire flow
    y_ctrl_bot = y - 0.20
    activation(x_ctrl, y_ctrl_top, y_ctrl_bot, color=CTRL_COLOR)

    # ------------------------------------------------------------------
    # Title + caption
    # ------------------------------------------------------------------
    ax.set_title(
        "Sequence Diagram — bookRide (POST /api/v1/carpooling/rides/:id/book)",
        fontsize=15, fontweight="bold", pad=18,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, y_ctrl_bot - 1.0,
        "Conventions:  filled arrowheads = synchronous;   open arrowheads = "
        "async;   dashed = return;   rectangles on lifelines = activation "
        "bars;   alt / loop = UML combined fragments.",
        ha="center", va="top", fontsize=9.5, style="italic", color="#566573",
    )

    # ------------------------------------------------------------------
    # Cosmetic — set y range to comfortably fit everything
    # ------------------------------------------------------------------
    ax.set_xlim(X_MIN, X_MAX + 0.2)
    ax.set_ylim(y_ctrl_bot - 2.0, Y_TOP_BOX + 2.2)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbse_seq_book_ride", dpi=300)
    register("mbse_seq_book_ride", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
