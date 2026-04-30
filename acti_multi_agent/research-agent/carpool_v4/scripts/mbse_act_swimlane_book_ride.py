"""mbse_act_swimlane_book_ride — Three-lane swimlane for the booking happy path.

Uses graphviz `cluster_*` subgraphs to render visual lanes.  Three columns:
    Rider | System | Driver
Source-of-truth:
  campusride-backend/src/controllers/carpooling.controller.js:511-709
  campusride-backend/src/services/rideCarpoolGroup.service.js:28-73
  campusride-backend/src/services/notification.service.js (fan-out)

Honesty correction:
  wxgroup_notice_record is INSERTed inside `createRide`, NOT inside `bookRide`.
  We annotate this explicitly to match draft §5.2.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import make_digraph, render_dot, register, renderer  # noqa: E402


# Per-lane palette
RIDER_FILL = "#D6EAF8"
RIDER_BORDER = "#1F618D"
SYS_FILL = "#FCF3CF"
SYS_BORDER = "#9A7D0A"
DRIVER_FILL = "#FADBD8"
DRIVER_BORDER = "#922B21"

ACTION_BORDER = "#34495E"
DECISION_FILL = "#FDEBD0"
DECISION_BORDER = "#CA6F1E"
DB_FILL = "#D5F5E3"
DB_BORDER = "#1E8449"
NOTIF_FILL = "#E8DAEF"
NOTIF_BORDER = "#76448A"
FORK_COLOR = "#1B2631"


@renderer("mbse_act_swimlane_book_ride")
def render():
    g = make_digraph("mbse_swimlane_book_ride", rankdir="TB")
    g.attr(
        ranksep="0.55", nodesep="0.35", splines="spline",
        label=(
            "Activity diagram — bookRide() happy path  "
            "(carpooling.controller.js:511-709)"
        ),
        labelloc="t", fontsize="14", compound="true",
    )
    g.attr("node", fontsize="10", fontname="Helvetica")
    g.attr("edge", fontsize="9")

    # ------------------------------------------------------------------
    # RIDER LANE
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_rider") as c:
        c.attr(
            label="Rider",
            style="rounded,filled", color=RIDER_BORDER,
            fillcolor=RIDER_FILL, fontsize="13", penwidth="1.6",
            fontcolor=RIDER_BORDER, labelloc="t", labeljust="l",
        )
        # initial node
        c.node("r_start", "", shape="circle", style="filled",
               fillcolor="#1B2631", color="#1B2631",
               width="0.25", height="0.25", fixedsize="true")
        c.node(
            "r_post",
            "POST /api/v1/carpooling/\nrides/:id/book",
            shape="box", style="rounded,filled",
            fillcolor="white", color=ACTION_BORDER, penwidth="1.4",
        )
        c.node(
            "r_recv",
            "Receives 200 +\nbooking row JSON",
            shape="box", style="rounded,filled",
            fillcolor="white", color=ACTION_BORDER, penwidth="1.4",
        )
        c.edge("r_start", "r_post", color=ACTION_BORDER)
        c.edge("r_post", "r_recv", style="invis")  # spacing

    # ------------------------------------------------------------------
    # SYSTEM LANE  (the big middle column)
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_system") as c:
        c.attr(
            label="System (Express + Supabase + Socket.IO)",
            style="rounded,filled", color=SYS_BORDER,
            fillcolor=SYS_FILL, fontsize="13", penwidth="1.6",
            fontcolor=SYS_BORDER, labelloc="t", labeljust="l",
        )
        # SELECT ride
        c.node(
            "s_select",
            "SELECT * FROM rides\nWHERE id = :id",
            shape="box", style="rounded,filled",
            fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
        )
        # decision
        c.node(
            "s_dec_seats",
            "status='active'\nAND seats > 0?",
            shape="diamond", style="filled",
            fillcolor=DECISION_FILL, color=DECISION_BORDER,
            penwidth="1.4", fontsize="9",
            width="2.0", height="1.2", fixedsize="true",
        )
        # INSERT booking
        c.node(
            "s_insert_booking",
            "INSERT ride_bookings\n(status='confirmed',\n payment_status='paid')",
            shape="box", style="rounded,filled",
            fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
        )
        # recompute seats
        c.node(
            "s_recompute",
            "Recompute seatsBooked",
            shape="box", style="rounded,filled",
            fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
        )
        # last seat decision
        c.node(
            "s_dec_full",
            "Last seat?",
            shape="diamond", style="filled",
            fillcolor=DECISION_FILL, color=DECISION_BORDER,
            penwidth="1.4", fontsize="9",
            width="1.6", height="1.0", fixedsize="true",
        )
        c.node(
            "s_set_full",
            "UPDATE rides\nSET status='full'",
            shape="box", style="rounded,filled",
            fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
        )
        # FORK bar (parallel notification fan-out)
        c.node(
            "s_fork",
            "",
            shape="box", style="filled",
            fillcolor=FORK_COLOR, color=FORK_COLOR,
            width="3.4", height="0.10", fixedsize="true",
        )
        # Six notification rows
        c.node(
            "s_notif_loop",
            "x6 notificationService.sendNotification\n"
            "{ride_new_booking(driver, high),\n"
            " ride_booking_confirmed(rider, med),\n"
            " ride_payment_confirmed(rider, med),\n"
            " ride_payment_received(driver, med),\n"
            " ride_rating_reminder(rider, high, +2h),\n"
            " ride_rating_reminder(driver, high, +2h)}",
            shape="box", style="rounded,filled",
            fillcolor=NOTIF_FILL, color=NOTIF_BORDER, penwidth="1.4",
            fontsize="9",
        )
        c.node(
            "s_socket_loop",
            "x6 socket.emit\non user:{recipientId}\n(real-time push)",
            shape="box", style="rounded,filled",
            fillcolor=NOTIF_FILL, color=NOTIF_BORDER, penwidth="1.4",
            fontsize="9",
        )
        # JOIN bar
        c.node(
            "s_join",
            "",
            shape="box", style="filled",
            fillcolor=FORK_COLOR, color=FORK_COLOR,
            width="3.4", height="0.10", fixedsize="true",
        )
        # Group ensure
        c.node(
            "s_ensure",
            "ensureRideCarpoolGroup\nOnBooking(rideId, riderId)",
            shape="box", style="rounded,filled",
            fillcolor="white", color=ACTION_BORDER, penwidth="1.4",
        )
        c.node(
            "s_grp_dec",
            "group exists\nfor ride_id?",
            shape="diamond", style="filled",
            fillcolor=DECISION_FILL, color=DECISION_BORDER,
            penwidth="1.4", fontsize="9",
            width="1.8", height="1.1", fixedsize="true",
        )
        c.node(
            "s_grp_insert",
            "INSERT groups\n(group_kind='ride_carpool',\n chat_expires=dep+1h)",
            shape="box", style="rounded,filled",
            fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
        )
        c.node(
            "s_mem_insert",
            "INSERT group_members\n(driver=creator, rider=member;\n idempotent on 23505)",
            shape="box", style="rounded,filled",
            fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
        )
        # Honesty annotation
        c.node(
            "s_wx_note",
            "wxgroup_notice_record row\nis INSERTed at createRide,\nNOT here in bookRide.\n(§5.2 honesty correction)",
            shape="note", style="filled",
            fillcolor="#FAE5D3", color="#CA6F1E", penwidth="1.2",
            fontsize="8.5", fontcolor="#7E5109",
        )
        c.node(
            "s_resp",
            "res.status(201).json\n({booking})",
            shape="box", style="rounded,filled",
            fillcolor="white", color=ACTION_BORDER, penwidth="1.4",
        )

        # System-internal edges
        c.edge("s_select", "s_dec_seats", color=ACTION_BORDER)
        c.edge("s_dec_seats", "s_insert_booking",
               label="Yes", color=DB_BORDER, fontcolor=DB_BORDER)
        c.edge("s_insert_booking", "s_recompute", color=DB_BORDER)
        c.edge("s_recompute", "s_dec_full", color=DB_BORDER)
        c.edge("s_dec_full", "s_set_full",
               label="Yes", color=DB_BORDER, fontcolor=DB_BORDER)
        c.edge("s_dec_full", "s_fork",
               label="No", color=ACTION_BORDER, fontcolor=ACTION_BORDER)
        c.edge("s_set_full", "s_fork", color=ACTION_BORDER)
        c.edge("s_fork", "s_notif_loop", color=NOTIF_BORDER)
        c.edge("s_fork", "s_socket_loop", color=NOTIF_BORDER)
        c.edge("s_notif_loop", "s_join", color=NOTIF_BORDER)
        c.edge("s_socket_loop", "s_join", color=NOTIF_BORDER)
        c.edge("s_join", "s_ensure", color=ACTION_BORDER)
        c.edge("s_ensure", "s_grp_dec", color=ACTION_BORDER)
        c.edge("s_grp_dec", "s_grp_insert",
               label="No", color=DB_BORDER, fontcolor=DB_BORDER)
        c.edge("s_grp_dec", "s_mem_insert",
               label="Yes", color=ACTION_BORDER, fontcolor=ACTION_BORDER)
        c.edge("s_grp_insert", "s_mem_insert", color=DB_BORDER)
        c.edge("s_mem_insert", "s_resp", color=ACTION_BORDER)
        c.edge("s_mem_insert", "s_wx_note",
               style="dashed", color="#CA6F1E", arrowhead="none",
               constraint="false")

    # ------------------------------------------------------------------
    # DRIVER LANE
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_driver") as c:
        c.attr(
            label="Driver",
            style="rounded,filled", color=DRIVER_BORDER,
            fillcolor=DRIVER_FILL, fontsize="13", penwidth="1.6",
            fontcolor=DRIVER_BORDER, labelloc="t", labeljust="l",
        )
        # Invisible spacer nodes push the Driver lane content downward so it
        # rank-aligns with the late stages of the system flow.
        for i in range(7):
            c.node(f"d_pad_{i}", "", shape="point",
                   style="invis", width="0.01", height="0.01")
        c.node(
            "d_recv",
            "Receives\n'ride_new_booking'\nnotification (push + socket)",
            shape="box", style="rounded,filled",
            fillcolor="white", color=ACTION_BORDER, penwidth="1.4",
        )
        c.node(
            "d_open",
            "Opens ride_carpool\ngroup chat (Messages tab)",
            shape="box", style="rounded,filled",
            fillcolor="white", color=ACTION_BORDER, penwidth="1.4",
        )
        c.node(
            "d_end",
            "",
            shape="doublecircle", style="filled",
            fillcolor="#1B2631", color="#1B2631",
            width="0.25", height="0.25", fixedsize="true",
        )
        # Padding chain forces driver nodes to lower ranks
        c.edge("d_pad_0", "d_pad_1", style="invis")
        c.edge("d_pad_1", "d_pad_2", style="invis")
        c.edge("d_pad_2", "d_pad_3", style="invis")
        c.edge("d_pad_3", "d_pad_4", style="invis")
        c.edge("d_pad_4", "d_pad_5", style="invis")
        c.edge("d_pad_5", "d_pad_6", style="invis")
        c.edge("d_pad_6", "d_recv", style="invis")
        c.edge("d_recv", "d_open", color=ACTION_BORDER)
        c.edge("d_open", "d_end", color=ACTION_BORDER)

    # ------------------------------------------------------------------
    # Cross-lane edges (constraint="false" to keep lane layout)
    # ------------------------------------------------------------------
    # Rider POST -> System SELECT
    g.edge("r_post", "s_select",
           color=RIDER_BORDER, penwidth="1.4",
           label="HTTP",
           ltail="cluster_rider", lhead="cluster_system",
           constraint="false")
    # System response -> rider receives
    g.edge("s_resp", "r_recv",
           color=ACTION_BORDER, penwidth="1.4",
           label="201 OK",
           ltail="cluster_system", lhead="cluster_rider",
           constraint="false")
    # Rider end node
    g.node("r_end", "", shape="doublecircle", style="filled",
           fillcolor="#1B2631", color="#1B2631",
           width="0.25", height="0.25", fixedsize="true")
    g.edge("r_recv", "r_end", color=ACTION_BORDER)
    # Notification fan-out -> driver (cross-lane)
    g.edge("s_notif_loop", "d_recv",
           color=NOTIF_BORDER, penwidth="1.4",
           label="push",
           constraint="false", style="dashed")
    # Group ready -> driver opens chat
    g.edge("s_mem_insert", "d_open",
           color=DRIVER_BORDER, penwidth="1.2",
           style="dashed", label="group ready",
           constraint="false")

    pdf, png = render_dot(g, "mbse_act_swimlane_book_ride")
    register("mbse_act_swimlane_book_ride", "ok", png_path=png)
    return pdf, png


if __name__ == "__main__":
    render()
