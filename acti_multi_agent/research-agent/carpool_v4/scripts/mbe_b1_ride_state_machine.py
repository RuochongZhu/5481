"""mbe_b1 — Ride + Booking State Machines.

Dual UML-style state machines on one canvas:
  - Top cluster: rides.status lifecycle (active / full / completed / cancelled)
  - Bottom cluster: ride_bookings.status lifecycle (confirmed / cancelled)

Inter-cluster dashed arrow shows the bookRide() side-effect that recomputes
seatsBooked and may transition the ride from `active` to `full`.

Source-of-truth:
  campusride-backend/src/controllers/carpooling.controller.js:511-709
  supabase/migrations/000_initial_schema.sql (rides.status, ride_bookings.status)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import make_digraph, render_dot, register  # noqa: E402


# State fill colors per the spec
ACTIVE_FILL = "#A9DFBF"      # green-tinted
FULL_FILL = "#F9E79F"        # yellow
COMPLETED_FILL = "#85C1E9"   # blue (final)
CANCELLED_FILL = "#F1948A"   # red (final)
CONFIRMED_FILL = "#A9DFBF"   # green-tinted (booking accepted)
INITIAL_BORDER = "#1B2631"   # near-black for filled circle

RIDE_BORDER = "#1F618D"
BOOK_BORDER = "#6C3483"
GUARD_COLOR = "#7B241C"


@renderer("mbe_b1_ride_state_machine")
def render():
    g = make_digraph("b1_ride_state_machine", rankdir="TB")
    g.attr(
        ranksep="0.9", nodesep="0.55", splines="spline",
        label=(
            "Ride + Booking state machines  "
            "(carpooling.controller.js:511-709, migration 000)"
        ),
        labelloc="t", fontsize="14",
    )
    g.attr("node", fontsize="11")
    g.attr("edge", fontsize="9")

    # =====================================================================
    # TOP cluster: rides.status state machine
    # =====================================================================
    with g.subgraph(name="cluster_ride") as c:
        c.attr(
            label="rides.status  (driver-owned ride lifecycle)",
            style="rounded,filled", color=RIDE_BORDER,
            fillcolor="#EBF5FB", fontsize="12", penwidth="1.4",
            rank="same",
        )
        c.attr("graph", rankdir="LR")

        # Initial pseudo-state (filled black circle)
        c.node(
            "ride_start", label="",
            shape="circle", style="filled", fillcolor=INITIAL_BORDER,
            color=INITIAL_BORDER, width="0.22", height="0.22", fixedsize="true",
        )

        # Real states — rounded boxes
        c.node(
            "ride_active",
            "active\n(seats remaining)",
            shape="box", style="rounded,filled",
            fillcolor=ACTIVE_FILL, color=RIDE_BORDER, penwidth="1.4",
        )
        c.node(
            "ride_full",
            "full\n(seatsBooked == available_seats)",
            shape="box", style="rounded,filled",
            fillcolor=FULL_FILL, color=RIDE_BORDER, penwidth="1.4",
        )
        # Final states use peripheries=2 to indicate UML final/terminal
        c.node(
            "ride_completed",
            "completed",
            shape="box", style="rounded,filled",
            fillcolor=COMPLETED_FILL, color=RIDE_BORDER,
            peripheries="2", penwidth="1.4",
        )
        c.node(
            "ride_cancelled",
            "cancelled",
            shape="box", style="rounded,filled",
            fillcolor=CANCELLED_FILL, color=RIDE_BORDER,
            peripheries="2", penwidth="1.4",
        )

        # Transitions
        c.edge(
            "ride_start", "ride_active",
            label=(
                "createRide(driver_id,\n"
                "  departure_time,\n"
                "  available_seats,\n"
                "  price_per_seat)"
            ),
            color=RIDE_BORDER, fontcolor=RIDE_BORDER,
        )
        c.edge(
            "ride_active", "ride_full",
            label=(
                "[server recompute]\n"
                "seatsBooked == available_seats\n"
                "(line 593-599)"
            ),
            color=RIDE_BORDER, fontcolor=RIDE_BORDER,
        )
        c.edge(
            "ride_full", "ride_completed",
            label=(
                "completeRide()\n"
                "guard: rater = driver_id"
            ),
            color=RIDE_BORDER, fontcolor=RIDE_BORDER,
        )
        c.edge(
            "ride_active", "ride_cancelled",
            label=(
                "cancelRide(reason)\n"
                "guard: now < departure_time\n"
                "(soft delete by driver)"
            ),
            color=GUARD_COLOR, fontcolor=GUARD_COLOR,
        )
        c.edge(
            "ride_full", "ride_cancelled",
            label=(
                "cancelRide(reason)\n"
                "guard: now < departure_time\n"
                "-> notify passengers\n"
                "(no payment integration)"
            ),
            color=GUARD_COLOR, fontcolor=GUARD_COLOR,
        )

        # Implicit invariant on update calls — annotate as a self-loop note
        c.node(
            "ride_inv",
            "guard on any update():\nstatus NOT IN\n(completed, cancelled)",
            shape="note", style="filled", fillcolor="#FDF2E9",
            color=GUARD_COLOR, fontcolor=GUARD_COLOR, fontsize="9",
        )
        c.edge(
            "ride_inv", "ride_active",
            style="dotted", color=GUARD_COLOR, arrowhead="none",
            constraint="false",
        )

    # =====================================================================
    # BOTTOM cluster: ride_bookings.status state machine
    # =====================================================================
    with g.subgraph(name="cluster_booking") as c:
        c.attr(
            label=(
                "ride_bookings.status  "
                "(passenger-owned booking lifecycle; demand-side default = confirmed, §5.2)"
            ),
            style="rounded,filled", color=BOOK_BORDER,
            fillcolor="#F4ECF7", fontsize="12", penwidth="1.4",
            rank="same",
        )
        c.attr("graph", rankdir="LR")

        c.node(
            "book_start", label="",
            shape="circle", style="filled", fillcolor=INITIAL_BORDER,
            color=INITIAL_BORDER, width="0.22", height="0.22", fixedsize="true",
        )
        c.node(
            "book_confirmed",
            "confirmed\n(default on insert)",
            shape="box", style="rounded,filled",
            fillcolor=CONFIRMED_FILL, color=BOOK_BORDER, penwidth="1.4",
        )
        c.node(
            "book_cancelled",
            "cancelled",
            shape="box", style="rounded,filled",
            fillcolor=CANCELLED_FILL, color=BOOK_BORDER,
            peripheries="2", penwidth="1.4",
        )

        c.edge(
            "book_start", "book_confirmed",
            label=(
                "bookRide(rideId,\n"
                "  passenger_id,\n"
                "  seats_booked)\n"
                "UNIQUE(ride_id, passenger_id)\n"
                "-> 5-effect fan-out (mbe_c1)"
            ),
            color=BOOK_BORDER, fontcolor=BOOK_BORDER,
        )
        c.edge(
            "book_confirmed", "book_cancelled",
            label=(
                "cancelBooking(reason)\n"
                "guard: now < departure_time"
            ),
            color=GUARD_COLOR, fontcolor=GUARD_COLOR,
        )

    # =====================================================================
    # Inter-cluster dashed trigger edge
    # confirmed (booking) -> ride.active (recompute) -> may go to ride.full
    # =====================================================================
    g.edge(
        "book_confirmed", "ride_active",
        label=(
            "side-effect:\n"
            "recompute seatsBooked;\n"
            "if == available_seats\n"
            "-> transitions ride to `full`"
        ),
        style="dashed", color="#7D6608", fontcolor="#7D6608",
        penwidth="1.4", arrowhead="vee", constraint="false",
        minlen="2",
    )

    pdf, png = render_dot(g, "mbe_b1_ride_state_machine")
    register("mbe_b1_ride_state_machine", "ok", png_path=png)
    return pdf, png
