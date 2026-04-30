"""mbse_ffbd_platform — Functional Flow Block Diagram for the v4.4 platform.

A classical FFBD (cf. NASA SE Handbook): numbered functional blocks F.1..F.12
laid out left-to-right, with explicit logical OR / AND gate nodes (drawn as
ovals) joining branched paths. A dashed feedback arrow returns from F.12 back
to F.1 to indicate the continuous-optimization loop. A side legend marks
deployed vs not-yet-deployed blocks; F.11 (points award/deduct) is flagged
with a red striped border because point_rules is empty and
point_transactions is not provisioned as a table.

Source-of-truth (v4.4 platform):
  - Authentication: src/services/email.service.js + Resend loop
  - Browse/match/book: src/controllers/carpooling.controller.js:511-709
  - Group fan-out:    src/services/rideCarpoolGroup.service.js
  - WeChat outreach:  src/app.js:165-281, 313-328 (fires on createRide)
  - Rating delay:     RIDE_RATING_REMINDER_DELAY_MS = 2h
  - Points:           src/services/points.service.js (point_rules empty)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import renderer, make_digraph, render_dot, register  # noqa: E402


# Palette ---------------------------------------------------------------------
DEPLOYED_FILL = "#D6EAF8"
DEPLOYED_BORDER = "#1A5276"

GAP_FILL = "#FADBD8"
GAP_BORDER = "#922B21"

GATE_FILL = "#FCF3CF"
GATE_BORDER = "#7D6608"

ALT_FILL = "#FDEBD0"
ALT_BORDER = "#9C640C"

LEGEND_FILL = "#FBFCFC"
LEGEND_BORDER = "#566573"

NOTE_FILL = "#FEF9E7"
NOTE_BORDER = "#7E5109"


def _html_escape(s: str) -> str:
    """Escape &, <, > for use inside graphviz HTML-like labels."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
    )


def _block(g, node_id, num, title, sub, *, fill=DEPLOYED_FILL,
           border=DEPLOYED_BORDER, penwidth="1.6", striped=False):
    """One numbered FFBD block. Box with bold "F.x" header and subtitle.

    Newlines in `title`/`sub` are translated to graphviz HTML <BR/> tags so
    multi-line labels render correctly inside HTML-like labels. Special
    characters (&, <, >) are HTML-escaped first.
    """
    style = "rounded,filled,bold" if striped else "rounded,filled"
    title_html = _html_escape(title).replace("\n", "<BR/>")
    sub_html = _html_escape(sub).replace("\n", "<BR/>")
    g.node(
        node_id,
        label=(
            f"<<FONT POINT-SIZE=\"13\"><B>F.{num}</B></FONT><BR/>"
            f"<FONT POINT-SIZE=\"11\"><B>{title_html}</B></FONT><BR/>"
            f"<FONT POINT-SIZE=\"9\">{sub_html}</FONT>>"
        ),
        shape="box", style=style,
        fillcolor=fill, color=border, penwidth=penwidth,
        width="2.0", height="1.4", fixedsize="false", margin="0.18,0.12",
    )


def _gate(g, node_id, kind):
    """Logical gate (OR / AND) drawn as an oval."""
    g.node(
        node_id,
        label=f"<<B>{kind}</B>>",
        shape="oval", style="filled",
        fillcolor=GATE_FILL, color=GATE_BORDER, penwidth="1.8",
        width="0.7", height="0.5", fixedsize="true", fontsize="11",
    )


@renderer("mbse_ffbd_platform")
def render():
    g = make_digraph("mbse_ffbd", rankdir="LR")
    g.attr(
        nodesep="0.55", ranksep="0.95", splines="spline",
        label=(
            "Functional Flow Block Diagram — CampusRide v4.4 Platform-wide Flow\\n"
            "F.1..F.12 sequenced left-to-right; OR/AND gates drawn as ovals; "
            "dashed feedback arrow F.12 → F.1 closes the optimization loop.\\n"
            "Deployed = blue; Alt / off-path = tan; Deployment gap = red striped; "
            "OR/AND logic = yellow oval."
        ),
        labelloc="t", labeljust="c", fontsize="16", fontname="Helvetica-Bold",
        newrank="true",
    )
    g.attr("node", fontsize="11")
    g.attr("edge", fontsize="10", arrowhead="vee", color="#34495E")

    # ---- Main horizontal spine -------------------------------------------
    _block(g, "f1", "1",
           "Authenticate User\n& Provision .edu Identity",
           "Resend email-OTP loop;\nuser scope = *.edu")
    _block(g, "f2", "2",
           "Browse / Search\nAcross Modules",
           "carpool · marketplace ·\nactivities · groups")
    _block(g, "f3", "3",
           "Match Ride Request\nwith Available Driver",
           "rides.status='active'\nseats_remaining > 0")

    # OR gate after F.3
    _gate(g, "or_match", "OR")

    _block(g, "f3_alt", "3.alt",
           "Suggest TCAT or\nScheduled Ride",
           "fallback path —\nno-match outcome",
           fill=ALT_FILL, border=ALT_BORDER, penwidth="1.4")

    _block(g, "f4", "4",
           "Confirm Booking &\nSend Notification Bundle",
           "5 immediate +\n2 delayed = 7 notifs")
    _block(g, "f5", "5",
           "Auto-create Ride-scoped\nGroup Chat",
           "groups.group_kind=\n'ride_carpool'")
    _block(g, "f6", "6",
           "WeChat Outreach Push",
           "mini-program short-link\n+ H5 fallback\n(fires on createRide)",
           fill=ALT_FILL, border=ALT_BORDER, penwidth="1.4")

    # AND gate joining F.5/F.6 back into the main spine before F.7
    _gate(g, "and_join", "AND")

    _block(g, "f7", "7",
           "Trip Execution &\nReal-time Location/Chat",
           "Socket.IO room:\nthread:{thread_id}")
    _block(g, "f8", "8",
           "Geo-verified\nActivity Check-in",
           "Haversine ≤ 100 m")
    _block(g, "f9", "9",
           "Post-trip 2h Delay →\nRating Window Opens",
           "RATING_READY_\nDELAY_MS")
    _block(g, "f10", "10",
           "Rating UPSERT →\nRecompute avg_rating",
           "users.avg_rating\nrolling mean")

    # F.11 — deployment gap, striped/red border
    _block(g, "f11", "11",
           "Award / Deduct Points",
           "INERT: point_rules = 0 rows\n(point_transactions table\nnot provisioned)",
           fill=GAP_FILL, border=GAP_BORDER, penwidth="2.4", striped=True)

    _block(g, "f12", "12",
           "Continuous Optimization\nLoop",
           "monthly HoQ refresh\n+ survey re-fielding")

    # ---- Forward edges (single LR spine, F.3.alt off-rank) ---------------
    g.edge("f1", "f2")
    g.edge("f2", "f3")
    g.edge("f3", "or_match")

    # OR branches: matched continues in main spine; no-match goes off-rank
    g.edge("or_match", "f4",
           label="match found", fontcolor=DEPLOYED_BORDER, color=DEPLOYED_BORDER)
    g.edge("or_match", "f3_alt",
           label="no match", fontcolor=ALT_BORDER, color=ALT_BORDER, style="dashed",
           constraint="false")
    g.edge("f3_alt", "f4",
           style="dotted", color=ALT_BORDER, fontcolor=ALT_BORDER,
           label="user re-queries", constraint="false")

    # F.4 → F.5 → AND join (F.5 in spine; F.6 off-rank as createRide branch)
    g.edge("f4", "f5")
    g.edge("f5", "and_join")
    g.edge("f4", "f6", style="dashed", color=ALT_BORDER, fontcolor=ALT_BORDER,
           label="(createRide path)", constraint="false")
    g.edge("f6", "and_join", style="dashed", color=ALT_BORDER, constraint="false")

    # AND → F.7..F.12 main spine
    g.edge("and_join", "f7")
    g.edge("f7", "f8")
    g.edge("f8", "f9")
    g.edge("f9", "f10")
    g.edge("f10", "f11")
    g.edge("f11", "f12")

    # ---- Feedback loop F.12 -> F.1 (dashed, non-constraining) ------------
    g.edge("f12", "f1",
           style="dashed", color="#7D3C98", fontcolor="#7D3C98",
           label="continuous improvement\nfeedback (dashed)",
           penwidth="1.4", constraint="false",
           arrowhead="vee", arrowsize="0.9")

    # ---- F.11 honesty annotation ----------------------------------------
    g.node(
        "note_f11",
        label=(
            "Deployment-gap flag (F.11):\\l"
            "  • point_rules: empty in production snapshot\\l"
            "  • point_transactions: not yet provisioned as a table\\l"
            "→ awarding/deducting is wired in code but inert.\\l"
        ),
        shape="note", style="filled",
        fillcolor=NOTE_FILL, color=NOTE_BORDER, fontsize="9",
    )
    g.edge("f11", "note_f11", style="dotted", arrowhead="none",
           color=NOTE_BORDER, constraint="false")

    # ---- F.6 honesty annotation -----------------------------------------
    g.node(
        "note_f6",
        label=(
            "Honesty correction (F.6):\\l"
            "WeChat outreach push fires on createRide,\\l"
            "not on bookRide. Drawn off the main spine\\l"
            "as a dashed branch — it is contemporaneous with\\l"
            "ride creation, not booking.\\l"
        ),
        shape="note", style="filled",
        fillcolor=NOTE_FILL, color=NOTE_BORDER, fontsize="9",
    )
    g.edge("f6", "note_f6", style="dotted", arrowhead="none",
           color=NOTE_BORDER, constraint="false")

    # ---- Pin off-rank branches close to their parents -------------------
    # Force F.3.alt to share a horizontal rank with F.4 (just below the spine
    # near its parent F.3 / OR gate). Force F.6 to share a rank with F.5
    # (just below the spine near its parent F.4). This keeps the alt branches
    # visually connected to the spine instead of orphaned far below.
    with g.subgraph() as r:
        r.attr(rank="same")
        r.node("f3_alt")
        r.node("f6")
    # Pin the honesty annotations to a lower rank so they stack neatly below
    with g.subgraph() as r:
        r.attr(rank="same")
        r.node("note_f6")
        r.node("note_f11")

    # Legend is intentionally omitted from the figure body to avoid the
    # mid-canvas floating-block problem; legend text is folded into the
    # graphviz title above (and into the LaTeX \caption in the paper).

    pdf, png = render_dot(g, "mbse_ffbd_platform", dpi=220)
    register("mbse_ffbd_platform", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
