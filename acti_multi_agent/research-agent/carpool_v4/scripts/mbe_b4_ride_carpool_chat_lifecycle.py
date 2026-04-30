"""mbe_b4 — Ride-Scoped Group Chat Lifecycle.

Lifecycle diagram for the auto-managed `group_kind='ride_carpool'` group that
is provisioned inline by `bookRide()`. Source-of-truth:
  campusride-backend/src/services/rideCarpoolGroup.service.js:28-73
  draft §5.7.5

Layout:
  - Main flow vertical (TB): bookRide -> service entry -> exists? decision
    -> INSERT groups (no) | reuse (yes) -> INSERT group_members (idempotent)
    -> Group ready / Socket.IO thread namespace
  - Side branches (dashed light grey):
      A) cancelBooking -> removePassengerFromRideGroup (member row delete)
      B) updateRide(departure_time) -> syncRideCarpoolGroupExpiry
      C) chat_expires_at reached -> read-only fallback
  - Snapshot footer (italic, 2026-04-23): 0 live ride_carpool rows; indirect
    evidence via 8 reminder rows + 16 wxgroup_notice_record pushes.
  - Limitation callout (orange, bottom-right):
      * 1-h post-departure expiry forecloses post-trip reconciliation
      * Migration-010 mute / message-delete affordances NOT inherited
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import make_digraph, render_dot, register  # noqa: E402


# Palette
SERVICE_FILL = "#D6EAF8"   # light blue — service-call nodes
DB_FILL = "#D5F5E3"        # light green — DB INSERT/UPDATE nodes
DECISION_FILL = "#FCF3CF"  # yellow — decision diamond
SIDE_FILL = "#F4F6F7"      # very light grey — side-branch nodes
CALLOUT_FILL = "#FAE5D3"   # orange-tinted — limitation callout
FOOTER_FILL = "#FDFEFE"    # near-white — snapshot footer

SERVICE_BORDER = "#1F618D"
DB_BORDER = "#1E8449"
DECISION_BORDER = "#B7950B"
SIDE_BORDER = "#909497"
CALLOUT_BORDER = "#CA6F1E"
FOOTER_BORDER = "#566573"


@renderer("mbe_b4_ride_carpool_chat_lifecycle")
def render():
    g = make_digraph("b4_ride_carpool_chat_lifecycle", rankdir="TB")
    g.attr(
        ranksep="0.55", nodesep="0.45", splines="spline",
        label=(
            "Ride-scoped group-chat lifecycle  "
            "(rideCarpoolGroup.service.js:28-73, draft §5.7.5)"
        ),
        labelloc="t", fontsize="14",
    )
    g.attr("node", fontsize="11")
    g.attr("edge", fontsize="9")

    # ------------------------------------------------------------------
    # Main vertical flow
    # ------------------------------------------------------------------
    # 1. bookRide entry
    g.node(
        "n1_book_ride",
        "bookRide(ride_id, passenger_id)\n"
        "[carpooling.controller.js:511-709]",
        shape="box", style="rounded,filled",
        fillcolor=SERVICE_FILL, color=SERVICE_BORDER, penwidth="1.4",
    )

    # 2. service entry
    g.node(
        "n2_ensure",
        "ensureRideCarpoolGroupOnBooking(ride_id, passenger_id)\n"
        "[rideCarpoolGroup.service.js:28-73]",
        shape="box", style="rounded,filled",
        fillcolor=SERVICE_FILL, color=SERVICE_BORDER, penwidth="1.4",
    )

    # 3. decision diamond
    g.node(
        "n3_exists",
        "SELECT * FROM groups\nWHERE ride_id = $1\n"
        "AND group_kind = 'ride_carpool'\nexists?",
        shape="diamond", style="filled",
        fillcolor=DECISION_FILL, color=DECISION_BORDER, penwidth="1.4",
        fontsize="10", height="1.6", width="2.6", fixedsize="false",
    )

    # 4a. INSERT groups (no branch)
    g.node(
        "n4a_insert_group",
        "INSERT INTO groups\n"
        "(group_kind = 'ride_carpool',\n"
        " name = 'Ride: <title>',\n"
        " creator_id = driver_id,\n"
        " ride_id,\n"
        " chat_expires_at = departure_time + 1h)",
        shape="box", style="rounded,filled",
        fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
    )

    # 4b. reuse existing group (yes branch)
    g.node(
        "n4b_reuse",
        "Group already exists; reuse\n(idempotent ensure)",
        shape="box", style="rounded,filled",
        fillcolor=SERVICE_FILL, color=SERVICE_BORDER, penwidth="1.2",
    )

    # 5. INSERT group_members (idempotent)
    g.node(
        "n5_insert_members",
        "INSERT INTO group_members\n"
        "(driver: role = 'creator';\n"
        " passenger: role = 'member')\n"
        "Duplicate-key (Postgres 23505)\n"
        "silently swallowed -> idempotent",
        shape="box", style="rounded,filled",
        fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
    )

    # 6. group ready
    g.node(
        "n6_ready",
        "Group ready;\n"
        "messaging-substrate inherits Socket.IO\n"
        "`thread:{thread_id}` namespace\n"
        "[messages.controller.js, mbe_a3]",
        shape="box", style="rounded,filled",
        fillcolor=SERVICE_FILL, color=SERVICE_BORDER, penwidth="1.4",
    )

    # Main-flow edges
    g.edge("n1_book_ride", "n2_ensure", color=SERVICE_BORDER)
    g.edge("n2_ensure", "n3_exists", color=SERVICE_BORDER)
    g.edge(
        "n3_exists", "n4a_insert_group",
        label="No", color=DB_BORDER, fontcolor=DB_BORDER,
    )
    g.edge(
        "n3_exists", "n4b_reuse",
        label="Yes", color=SERVICE_BORDER, fontcolor=SERVICE_BORDER,
    )
    g.edge("n4a_insert_group", "n5_insert_members", color=DB_BORDER)
    g.edge("n4b_reuse", "n5_insert_members", color=SERVICE_BORDER)
    g.edge("n5_insert_members", "n6_ready", color=SERVICE_BORDER)

    # ------------------------------------------------------------------
    # Side branches (dashed light grey)
    # ------------------------------------------------------------------
    # (A) cancelBooking -> removePassengerFromRideGroup
    g.node(
        "sA_cancel",
        "(A) cancelBooking(ride_id, passenger_id)\n"
        "  -> removePassengerFromRideGroup(...)\n"
        "  DELETE group_members WHERE\n"
        "  group_id = $1 AND user_id = $2;\n"
        "  group itself NOT deleted\n"
        "  (other passengers may remain)",
        shape="box", style="rounded,filled,dashed",
        fillcolor=SIDE_FILL, color=SIDE_BORDER, fontsize="9",
    )
    g.edge(
        "n5_insert_members", "sA_cancel",
        style="dashed", color=SIDE_BORDER, arrowhead="vee",
        constraint="false", minlen="2",
        label="on cancel", fontcolor=SIDE_BORDER,
    )

    # (B) updateRide(departure_time) -> syncRideCarpoolGroupExpiry
    g.node(
        "sB_sync",
        "(B) updateRide(departure_time)\n"
        "  -> syncRideCarpoolGroupExpiry(ride_id)\n"
        "  UPDATE groups SET\n"
        "  chat_expires_at = new_departure_time + 1h",
        shape="box", style="rounded,filled,dashed",
        fillcolor=SIDE_FILL, color=SIDE_BORDER, fontsize="9",
    )
    g.edge(
        "n6_ready", "sB_sync",
        style="dashed", color=SIDE_BORDER, arrowhead="vee",
        constraint="false", minlen="2",
        label="on departure_time edit", fontcolor=SIDE_BORDER,
    )

    # (C) chat_expires_at reached -> read-only fallback
    g.node(
        "sC_expired",
        "(C) on chat_expires_at reached\n"
        "  read-only fallback:\n"
        "  no new messages accepted;\n"
        "  existing thread visible until cleanup",
        shape="note", style="filled,dashed",
        fillcolor=SIDE_FILL, color=SIDE_BORDER, fontsize="9",
    )
    g.edge(
        "n6_ready", "sC_expired",
        style="dashed", color=SIDE_BORDER, arrowhead="vee",
        constraint="false", minlen="2",
        label="on TTL expiry", fontcolor=SIDE_BORDER,
    )

    # ------------------------------------------------------------------
    # Limitation callout (orange-tinted, off-flow, bottom-right)
    # ------------------------------------------------------------------
    g.node(
        "callout_limits",
        "Limitations (§7.2 scope):\n"
        "• 1-hour post-departure expiry forecloses\n"
        "  post-trip reconciliation chat\n"
        "  (lost items, fare corrections, rating disputes).\n"
        "• Group muting / message-deletion affordances\n"
        "  (migration 010) NOT inherited by\n"
        "  ride_carpool groups.",
        shape="box", style="rounded,filled",
        fillcolor=CALLOUT_FILL, color=CALLOUT_BORDER, penwidth="1.4",
        fontsize="10", fontcolor="#7E5109",
    )
    g.edge(
        "sC_expired", "callout_limits",
        style="invis", constraint="false",
    )
    # Light dotted reference into main flow so the callout is visually anchored
    g.edge(
        "n6_ready", "callout_limits",
        style="dotted", color=CALLOUT_BORDER, arrowhead="none",
        constraint="false",
    )

    # ------------------------------------------------------------------
    # Snapshot footer (italic, full-width)
    # ------------------------------------------------------------------
    g.node(
        "footer_snapshot",
        "<<i>2026-04-23 snapshot: 0 group_kind='ride_carpool' rows live. "
        "Indirect evidence via 8 ride_rating_reminder notification rows "
        "+ 16 ride wxgroup_notice_record pushes from historical bookings "
        "whose rides table entries were cleaned.</i>>",
        shape="box", style="rounded,filled",
        fillcolor=FOOTER_FILL, color=FOOTER_BORDER, penwidth="1.0",
        fontsize="9",
    )
    g.edge(
        "callout_limits", "footer_snapshot",
        style="invis", constraint="true",
    )
    g.edge(
        "n6_ready", "footer_snapshot",
        style="invis", constraint="true",
    )

    pdf, png = render_dot(g, "mbe_b4_ride_carpool_chat_lifecycle")
    register("mbe_b4_ride_carpool_chat_lifecycle", "ok", png_path=png)
    return pdf, png
