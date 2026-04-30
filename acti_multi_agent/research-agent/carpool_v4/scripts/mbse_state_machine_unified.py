"""mbse_state_machine_unified - Combined UML state machine.

Three entity lifecycles drawn on one canvas as separate UML clusters
plus cross-cluster (dashed) trigger edges:

  - Ride            : active -> full -> completed | cancelled
  - RideBooking     : confirmed -> cancelled
  - Group(group_kind='ride_carpool') : created -> active -> expired

Cross-entity triggers:

  bookRide        - may flip Ride to `full` (if last seat) AND
                    may create the Group on first booking AND
                    adds a GroupMember row
  cancelBooking   - may un-flag Ride from `full` AND removes a GroupMember
  updateRide(departure_time) - updates Group.chat_expires_at
  completeRide    - no transitions on bookings or group
                    (group expires on its own departure+1h timer)

UML notation:
  - Initial pseudo-state: filled black circle
  - Final pseudo-state:   double-circled bullet (peripheries=2)
  - Transition labels in trigger[guard]/effect form
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import make_digraph, render_dot, register, renderer  # noqa: E402


# State fill colors
INITIAL_BORDER = "#1B2631"
ACTIVE_FILL = "#A9DFBF"
FULL_FILL = "#F9E79F"
COMPLETED_FILL = "#85C1E9"
CANCELLED_FILL = "#F1948A"
CONFIRMED_FILL = "#A9DFBF"
CREATED_FILL = "#FAD7A0"
GROUP_ACTIVE_FILL = "#A9DFBF"
EXPIRED_FILL = "#D7DBDD"

RIDE_BORDER = "#1F618D"
BOOK_BORDER = "#6C3483"
GROUP_BORDER = "#1E8449"
TRIGGER_COLOR = "#7D6608"
GUARD_COLOR = "#7B241C"


@renderer("mbse_state_machine_unified")
def render():
    g = make_digraph("mbse_state_machine_unified", rankdir="TB")
    g.attr(
        ranksep="1.20", nodesep="0.55", splines="spline", newrank="true",
        label=(
            "Combined UML State Machine - Ride + RideBooking + ride_carpool Group\n"
            "Solid = within-entity transitions; dashed = cross-entity triggers"
        ),
        labelloc="t", fontsize="14",
    )
    g.attr("node", fontsize="10")
    g.attr("edge", fontsize="9")

    # ==========================================================
    # Cluster 1 - Ride lifecycle
    # ==========================================================
    with g.subgraph(name="cluster_ride") as c:
        c.attr(
            label="Ride  (rides.status)",
            style="rounded,filled", color=RIDE_BORDER,
            fillcolor="#EBF5FB", fontsize="12", penwidth="1.4",
            labeljust="l", fontcolor=RIDE_BORDER,
        )
        c.attr("graph", rankdir="LR")

        c.node("ride_init", label="",
               shape="circle", style="filled",
               fillcolor=INITIAL_BORDER, color=INITIAL_BORDER,
               width="0.22", height="0.22", fixedsize="true")

        c.node("ride_active", "active\n(seats remaining)",
               shape="box", style="rounded,filled",
               fillcolor=ACTIVE_FILL, color=RIDE_BORDER, penwidth="1.4")

        c.node("ride_full", "full\n(seats exhausted)",
               shape="box", style="rounded,filled",
               fillcolor=FULL_FILL, color=RIDE_BORDER, penwidth="1.4")

        c.node("ride_completed", "completed",
               shape="box", style="rounded,filled",
               fillcolor=COMPLETED_FILL, color=RIDE_BORDER,
               peripheries="2", penwidth="1.4")

        c.node("ride_cancelled", "cancelled\n(soft-delete)",
               shape="box", style="rounded,filled",
               fillcolor=CANCELLED_FILL, color=RIDE_BORDER,
               peripheries="2", penwidth="1.4")

        # Transitions
        c.edge("ride_init", "ride_active",
               label="createRide(driver_id, departure_time,\n"
                     "  total_seats, price)/\n"
                     "INSERT rides (status='active')",
               color=RIDE_BORDER, fontcolor=RIDE_BORDER)

        c.edge("ride_active", "ride_full",
               label="seatsBooked == total_seats /\n"
                     "UPDATE rides SET status='full'",
               color=RIDE_BORDER, fontcolor=RIDE_BORDER)

        c.edge("ride_full", "ride_active",
               label="cancelBooking [seatsBooked < total_seats] /\n"
                     "UPDATE rides SET status='active'",
               color=RIDE_BORDER, fontcolor=RIDE_BORDER, style="dotted")

        c.edge("ride_active", "ride_completed",
               label="completeRide()\n[rater = driver_id]",
               color=RIDE_BORDER, fontcolor=RIDE_BORDER)
        c.edge("ride_full", "ride_completed",
               label="completeRide()\n[rater = driver_id]",
               color=RIDE_BORDER, fontcolor=RIDE_BORDER)

        c.edge("ride_active", "ride_cancelled",
               label="cancelRide(reason)\n[now < departure_time]",
               color=GUARD_COLOR, fontcolor=GUARD_COLOR)
        c.edge("ride_full", "ride_cancelled",
               label="cancelRide(reason)\n[now < departure_time]",
               color=GUARD_COLOR, fontcolor=GUARD_COLOR)

    # ==========================================================
    # Cluster 2 - RideBooking lifecycle (placed second so the
    # cross-cluster booking->ride and booking->group edges stay short)
    # ==========================================================
    with g.subgraph(name="cluster_booking") as c:
        c.attr(
            label="RideBooking  (ride_bookings.status)",
            style="rounded,filled", color=BOOK_BORDER,
            fillcolor="#F4ECF7", fontsize="12", penwidth="1.4",
            labeljust="l", fontcolor=BOOK_BORDER,
        )
        c.attr("graph", rankdir="LR")

        c.node("book_init", label="",
               shape="circle", style="filled",
               fillcolor=INITIAL_BORDER, color=INITIAL_BORDER,
               width="0.22", height="0.22", fixedsize="true")

        c.node("book_confirmed", "confirmed\n(default on insert)",
               shape="box", style="rounded,filled",
               fillcolor=CONFIRMED_FILL, color=BOOK_BORDER, penwidth="1.4")

        c.node("book_cancelled", "cancelled",
               shape="box", style="rounded,filled",
               fillcolor=CANCELLED_FILL, color=BOOK_BORDER,
               peripheries="2", penwidth="1.4")

        c.edge("book_init", "book_confirmed",
               label="bookRide(ride_id, rider_id, seats)\n"
                     "[seats > 0] /\nINSERT ride_bookings (status='confirmed')",
               color=BOOK_BORDER, fontcolor=BOOK_BORDER)

        c.edge("book_confirmed", "book_cancelled",
               label="cancelBooking()\n[now < ride.departure_time] /\n"
                     "UPDATE ride_bookings SET status='cancelled'",
               color=GUARD_COLOR, fontcolor=GUARD_COLOR)

    # ==========================================================
    # Cluster 3 - Group(group_kind='ride_carpool') lifecycle
    # ==========================================================
    with g.subgraph(name="cluster_group") as c:
        c.attr(
            label="Group  (group_kind='ride_carpool')",
            style="rounded,filled", color=GROUP_BORDER,
            fillcolor="#EAFAF1", fontsize="12", penwidth="1.4",
            labeljust="l", fontcolor=GROUP_BORDER,
        )
        c.attr("graph", rankdir="LR")

        c.node("grp_init", label="",
               shape="circle", style="filled",
               fillcolor=INITIAL_BORDER, color=INITIAL_BORDER,
               width="0.22", height="0.22", fixedsize="true")

        c.node("grp_created", "created\n(on first booking)",
               shape="box", style="rounded,filled",
               fillcolor=CREATED_FILL, color=GROUP_BORDER, penwidth="1.4")

        c.node("grp_active", "active\n(during chat window)",
               shape="box", style="rounded,filled",
               fillcolor=GROUP_ACTIVE_FILL, color=GROUP_BORDER, penwidth="1.4")

        c.node("grp_expired", "expired\n(read-only)",
               shape="box", style="rounded,filled",
               fillcolor=EXPIRED_FILL, color=GROUP_BORDER,
               peripheries="2", penwidth="1.4")

        c.edge("grp_init", "grp_created",
               label="ensureRideCarpoolGroupOnBooking()\n"
                     "[no prior group for ride_id] /\n"
                     "INSERT groups,\n"
                     "  chat_expires_at = departure_time + 1h",
               color=GROUP_BORDER, fontcolor=GROUP_BORDER)

        c.edge("grp_created", "grp_active",
               label="first GroupMessage / immediate",
               color=GROUP_BORDER, fontcolor=GROUP_BORDER)

        c.edge("grp_active", "grp_expired",
               label="now >= chat_expires_at /\n"
                     "(read-only fallback)",
               color=GROUP_BORDER, fontcolor=GROUP_BORDER)

    # Anchor the three cluster init nodes to the same rank so the clusters
    # arrange as three side-by-side horizontal bands rather than stacking.
    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("ride_init")
        s.node("book_init")
        s.node("grp_init")

    # ==========================================================
    # Cross-cluster trigger edges (dashed)
    # ==========================================================
    # bookRide -> may create Group
    g.edge(
        "book_confirmed", "grp_created",
        label="bookRide() side-effect:\n"
              "ensureRideCarpoolGroupOnBooking\n"
              "  + INSERT group_members",
        style="dashed", color=TRIGGER_COLOR,
        fontcolor=TRIGGER_COLOR, penwidth="1.3",
        arrowhead="vee", constraint="false", minlen="2",
    )
    # bookRide -> may flip Ride to `full`
    g.edge(
        "book_confirmed", "ride_full",
        label="recompute seatsBooked /\n"
              "if last seat -> Ride.full",
        style="dashed", color=TRIGGER_COLOR,
        fontcolor=TRIGGER_COLOR, penwidth="1.3",
        arrowhead="vee", constraint="false", minlen="2",
    )
    # cancelBooking -> may un-flag Ride from `full`
    g.edge(
        "book_cancelled", "ride_active",
        label="cancelBooking side-effect:\n"
              "if Ride was full -> Ride.active\n"
              "  + DELETE group_members row",
        style="dashed", color=TRIGGER_COLOR,
        fontcolor=TRIGGER_COLOR, penwidth="1.3",
        arrowhead="vee", constraint="false", minlen="2",
    )
    # updateRide(departure_time) -> updates Group.chat_expires_at
    g.edge(
        "ride_active", "grp_active",
        label="updateRide(departure_time) /\n"
              "Group.chat_expires_at =\n"
              "  new departure + 1h",
        style="dashed", color=TRIGGER_COLOR,
        fontcolor=TRIGGER_COLOR, penwidth="1.3",
        arrowhead="vee", constraint="false", minlen="2",
    )
    # completeRide note - no booking/group transition
    g.node(
        "complete_note",
        "completeRide() does NOT\n"
        "trigger booking or group\n"
        "transitions; Group expires\n"
        "on its own departure+1h timer",
        shape="note", style="filled",
        fillcolor="#FDF2E9", color=GUARD_COLOR,
        fontcolor=GUARD_COLOR, fontsize="9",
    )
    g.edge(
        "ride_completed", "complete_note",
        style="dotted", color=GUARD_COLOR,
        arrowhead="none", constraint="false",
    )

    # ==========================================================
    # Legend cluster (placed below grp_expired so it stays at bottom)
    # ==========================================================
    with g.subgraph(name="cluster_legend") as c:
        c.attr(
            label="Legend", style="rounded,filled",
            color="#566573", fillcolor="#FBFCFC",
            fontsize="11", penwidth="1.2", labeljust="l", labelloc="t",
        )
        c.attr("graph", rankdir="LR")
        c.node("leg_initial", "initial pseudo-state",
               shape="circle", style="filled",
               fillcolor=INITIAL_BORDER, color=INITIAL_BORDER,
               width="0.20", height="0.20", fixedsize="true",
               fontcolor=INITIAL_BORDER, fontsize="9")
        c.node("leg_state", "state",
               shape="box", style="rounded,filled",
               fillcolor=ACTIVE_FILL, color=RIDE_BORDER,
               penwidth="1.2", fontsize="9")
        c.node("leg_final", "final pseudo-state",
               shape="box", style="rounded,filled",
               fillcolor=COMPLETED_FILL, color=RIDE_BORDER,
               peripheries="2", penwidth="1.2", fontsize="9")
        c.node("leg_cross",
               "cross-entity\ntrigger / side-effect",
               shape="plaintext", fontcolor=TRIGGER_COLOR,
               fontsize="9")
        c.edge("leg_initial", "leg_state", style="invis")
        c.edge("leg_state", "leg_final", style="invis")
        c.edge("leg_final", "leg_cross", style="invis")

    # Legend floats off-graph; no constraint.
    g.edge("grp_expired", "leg_initial",
           style="invis", constraint="false")

    pdf, png = render_dot(g, "mbse_state_machine_unified")
    register("mbse_state_machine_unified", "ok", png_path=png)
    return pdf, png


if __name__ == "__main__":
    render()
