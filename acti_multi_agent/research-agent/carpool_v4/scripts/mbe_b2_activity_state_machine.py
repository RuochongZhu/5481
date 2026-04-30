"""mbe_b2 — Activity Lifecycle + Participant Lifecycle.

Two co-located state machines:
  Top:    activities.status            (draft / published / ongoing / completed / cancelled)
  Bottom: activity_participants.attendance_status
          (registered / checked_in / absent / no_show)

Source-of-truth:
  integration-production/campusride-backend/src/services/activity-checkin.service.js:31-191
  supabase/migrations/000_complete_schema.sql  (activities, activity_participants,
  triggers: increment current_participants, RPC: calculate_distance, increment_user_points)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import make_digraph, render_dot, register  # noqa: E402


# State palette (per spec)
STATE_FILL = {
    "draft":     "#BDC3C7",  # grey
    "published": "#2ECC71",  # green
    "ongoing":   "#3498DB",  # blue
    "completed": "#8E44AD",  # purple
    "cancelled": "#E74C3C",  # red
}
STATE_BORDER = {
    "draft":     "#7F8C8D",
    "published": "#1E8449",
    "ongoing":   "#1F618D",
    "completed": "#5B2C6F",
    "cancelled": "#922B21",
}

# Participant palette (re-uses the activity-side hues but distinct enough)
P_STATE_FILL = {
    "registered": "#F4D03F",   # warm yellow (pending)
    "checked_in": "#27AE60",   # rich green (success terminal)
    "absent":     "#7F8C8D",   # grey terminal
    "no_show":    "#C0392B",   # red terminal
}
P_STATE_BORDER = {
    "registered": "#9A7D0A",
    "checked_in": "#196F3D",
    "absent":     "#566573",
    "no_show":    "#641E16",
}


def _state_node(graph, node_id: str, label: str, fill: str, border: str,
                fontcolor: str = "white", penwidth: str = "1.6") -> None:
    graph.node(
        node_id,
        label=label,
        shape="box",
        style="rounded,filled,bold",
        fillcolor=fill,
        color=border,
        fontcolor=fontcolor,
        fontname="Helvetica-Bold",
        fontsize="12",
        penwidth=penwidth,
        margin="0.18,0.10",
    )


def _start_node(graph, node_id: str) -> None:
    graph.node(
        node_id,
        label="",
        shape="circle",
        style="filled",
        fillcolor="#2C3E50",
        color="#1A252F",
        width="0.28",
        height="0.28",
        fixedsize="true",
    )


def _terminal_ring(graph, node_id: str, label: str, fill: str, border: str) -> None:
    """Render a terminal state with a double border (peripheries=2)."""
    graph.node(
        node_id,
        label=label,
        shape="box",
        style="rounded,filled,bold",
        fillcolor=fill,
        color=border,
        fontcolor="white",
        fontname="Helvetica-Bold",
        fontsize="12",
        peripheries="2",
        penwidth="1.6",
        margin="0.18,0.10",
    )


@renderer("mbe_b2_activity_state_machine")
def render():
    g = make_digraph("b2_activity_state_machine", rankdir="LR")
    g.attr(
        ranksep="0.95", nodesep="0.45", splines="spline",
        compound="true", newrank="true",
        label=("Activity & Participant State Machines  "
               "(activity-checkin.service.js:31-191; "
               "migrations/000_complete_schema.sql)"),
        labelloc="t", fontsize="14", fontname="Helvetica-Bold",
    )
    g.attr("edge", fontsize="9")

    # =========================================================================
    # TOP CLUSTER: ACTIVITY STATE MACHINE  (activities.status)
    # =========================================================================
    with g.subgraph(name="cluster_activity") as a:
        a.attr(
            label=("Activity  —  activities.status\\n"
                   "(transitions in activity.controller / scheduler / "
                   "activity-cleanup.service)"),
            style="rounded,filled",
            fillcolor="#FBFCFC",
            color="#1F618D",
            penwidth="2.0",
            fontname="Helvetica-Bold",
            fontsize="12",
            margin="16",
        )

        _start_node(a, "a_start")
        _state_node(a, "a_draft",     "draft",
                    STATE_FILL["draft"], STATE_BORDER["draft"],
                    fontcolor="#2C3E50")
        _state_node(a, "a_published",
                    "published\\ncheckin_enabled flag\\nopens geo-checkin (mbe_c4)",
                    STATE_FILL["published"], STATE_BORDER["published"])
        _state_node(a, "a_ongoing",   "ongoing",
                    STATE_FILL["ongoing"], STATE_BORDER["ongoing"])
        _state_node(a, "a_completed", "completed",
                    STATE_FILL["completed"], STATE_BORDER["completed"])
        _state_node(a, "a_cancelled", "cancelled",
                    STATE_FILL["cancelled"], STATE_BORDER["cancelled"])

        # Forward path
        a.edge("a_start", "a_draft",
               label="createActivity()",
               color=STATE_BORDER["draft"], fontcolor=STATE_BORDER["draft"],
               penwidth="1.4")
        a.edge("a_draft", "a_published",
               label="publishActivity()",
               color=STATE_BORDER["published"],
               fontcolor=STATE_BORDER["published"], penwidth="1.4")
        a.edge("a_published", "a_ongoing",
               label="auto @ start_time\\n(scheduler / on-demand check)",
               color=STATE_BORDER["ongoing"],
               fontcolor=STATE_BORDER["ongoing"], penwidth="1.4")
        a.edge("a_ongoing", "a_completed",
               label="auto @ end_time  OR\\ncompleteActivity()",
               color=STATE_BORDER["completed"],
               fontcolor=STATE_BORDER["completed"], penwidth="1.4")

        # Cancellation edges (any -> cancelled per spec: published / ongoing)
        a.edge("a_published", "a_cancelled",
               label="cancelActivity()",
               color=STATE_BORDER["cancelled"],
               fontcolor=STATE_BORDER["cancelled"],
               style="dashed", penwidth="1.2")
        a.edge("a_ongoing", "a_cancelled",
               label="cancelActivity()",
               color=STATE_BORDER["cancelled"],
               fontcolor=STATE_BORDER["cancelled"],
               style="dashed", penwidth="1.2")
        a.edge("a_draft", "a_cancelled",
               label="cancelActivity()",
               color=STATE_BORDER["cancelled"],
               fontcolor=STATE_BORDER["cancelled"],
               style="dotted", penwidth="1.0",
               constraint="false")

    # =========================================================================
    # BOTTOM CLUSTER: PARTICIPANT STATE MACHINE
    #   activity_participants.attendance_status
    # =========================================================================
    with g.subgraph(name="cluster_participant") as p:
        p.attr(
            label=("Participant  —  activity_participants.attendance_status\\n"
                   "(performCheckin gated by is_checkin_period AND "
                   "Haversine distance ≤ verification_radius)"),
            style="rounded,filled",
            fillcolor="#FBFCFC",
            color="#196F3D",
            penwidth="2.0",
            fontname="Helvetica-Bold",
            fontsize="12",
            margin="16",
        )

        _start_node(p, "p_start")
        _state_node(p, "p_registered", "registered",
                    P_STATE_FILL["registered"], P_STATE_BORDER["registered"],
                    fontcolor="#1B2631")
        _terminal_ring(p, "p_checked_in",
                       "checked_in\\n(points awarded)",
                       P_STATE_FILL["checked_in"], P_STATE_BORDER["checked_in"])
        _terminal_ring(p, "p_absent", "absent",
                       P_STATE_FILL["absent"], P_STATE_BORDER["absent"])
        _terminal_ring(p, "p_no_show", "no_show",
                       P_STATE_FILL["no_show"], P_STATE_BORDER["no_show"])

        # Entry: registration triggers PL/pgSQL increment of current_participants
        p.edge("p_start", "p_registered",
               label=("registerActivity()\\n"
                      "trigger: current_participants += 1"),
               color=P_STATE_BORDER["registered"],
               fontcolor=P_STATE_BORDER["registered"], penwidth="1.4")

        # registered -> checked_in (the load-bearing edge)
        p.edge("p_registered", "p_checked_in",
               label=("performCheckin()\\n"
                      "guard: is_checkin_period (default ±30 min)\\n"
                      "guard: calculate_distance (Haversine RPC)\\n"
                      "        ≤ verification_radius (default 100m)\\n"
                      "effect: increment_user_points('activity_checkin', 5)"),
               color=P_STATE_BORDER["checked_in"],
               fontcolor=P_STATE_BORDER["checked_in"], penwidth="1.8")

        # registered -> absent (organizer-driven)
        p.edge("p_registered", "p_absent",
               label="organizer marks absent\\n(during / after activity)",
               color=P_STATE_BORDER["absent"],
               fontcolor=P_STATE_BORDER["absent"],
               style="dashed", penwidth="1.2")

        # registered -> no_show (auto on completion if not checked_in)
        p.edge("p_registered", "p_no_show",
               label=("auto on activity.status -> completed\\n"
                      "if checked_in = false"),
               color=P_STATE_BORDER["no_show"],
               fontcolor=P_STATE_BORDER["no_show"],
               style="dashed", penwidth="1.2")

    # ---- Cross-cluster contextual link (visually ties the two SMs) ----------
    # An invisible-style link from activity 'completed' to participant 'no_show'
    # makes the temporal causation legible (completion fires the no_show check).
    g.edge("a_completed", "p_no_show",
           label=("on completion:\\n"
                  "WHERE checked_in = false  →  no_show"),
           color="#7F8C8D", fontcolor="#566573",
           style="dotted", penwidth="1.0",
           ltail="cluster_activity", lhead="cluster_participant",
           constraint="false")

    # Legend (compact)
    legend_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"4\">"
        "<TR><TD COLSPAN=\"2\"><B>Legend</B></TD></TR>"
        "<TR><TD BGCOLOR=\"#BDC3C7\" WIDTH=\"18\"></TD>"
        "<TD ALIGN=\"LEFT\">draft</TD></TR>"
        "<TR><TD BGCOLOR=\"#2ECC71\"></TD>"
        "<TD ALIGN=\"LEFT\">published</TD></TR>"
        "<TR><TD BGCOLOR=\"#3498DB\"></TD>"
        "<TD ALIGN=\"LEFT\">ongoing</TD></TR>"
        "<TR><TD BGCOLOR=\"#8E44AD\"></TD>"
        "<TD ALIGN=\"LEFT\">completed</TD></TR>"
        "<TR><TD BGCOLOR=\"#E74C3C\"></TD>"
        "<TD ALIGN=\"LEFT\">cancelled</TD></TR>"
        "<TR><TD COLSPAN=\"2\"><FONT POINT-SIZE=\"9\">"
        "double border = terminal participant state"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node("legend", label=legend_label,
           shape="box", style="rounded,filled",
           fillcolor="#FDFEFE", color="#34495E",
           fontname="Helvetica", fontsize="10", margin="0.10")

    pdf, png = render_dot(g, "mbe_b2_activity_state_machine", dpi=300)
    register("mbe_b2_activity_state_machine", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
