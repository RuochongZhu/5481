"""mbe_e1 — Research-Agent 8-Phase Pipeline.

Block diagram of the thesis-conditioned evidence pipeline used to ground the
CampusRide paper. Source: §3.2 + §6 of the v4.2 draft.

Phases (LR):
  P1 Corpus Assembly (Sonnet) -> corpus.json
  P2 Classification (Sonnet) -> classified.json (10 cats A-J)
  P2.5 Deep Extraction (Sonnet) -> extractions.json (7 fields)
  P3 Relationship Graph (Opus) -> relationship_graph.json
  P3.5 Narrative Chain (Opus) -> narrative_chains.json (7 beats)
  P3.7 Contradiction Map (Opus) -> contradictions.json (F1..F5)
  P4 Evidence Inventory (Sonnet) -> evidence_inventory.json
  P5 Five-Reviewer Eval (Opus) -> evaluation.json + results.tsv

Auto-backtrack: P5 -> {P3.5, P3.7, P4} (red dashed) when overall<0.85
or honesty<0.80, routed to weakest dimension's phase.

State invariants (footer): append-only corpus, --resume, state save before/
after, every API error classified (APIKeyMissing / ModelNotFound /
QuotaExhausted).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    make_digraph, render_dot, register, renderer,
)


# Tier fill colors
SONNET_FILL = "#D6EAF8"   # light blue
SONNET_BORDER = "#2874A6"
OPUS_FILL = "#E8DAEF"     # light purple
OPUS_BORDER = "#7D3C98"
SOURCE_FILL = "#D5F5E3"   # light green for external sources
SOURCE_BORDER = "#229954"
JSON_FILL = "#ECECEC"     # grey ovals for output JSON
JSON_BORDER = "#7F7F7F"
INVAR_FILL = "#FCF3CF"    # light yellow for invariants
INVAR_BORDER = "#B7950B"
BACKTRACK = "#C0392B"     # red dashed backtrack arrow


def _phase_node(g, nid: str, title: str, body: str, tier: str) -> None:
    """Add a phase block colored by model tier."""
    if tier == "sonnet":
        fill, border = SONNET_FILL, SONNET_BORDER
        tier_label = "Sonnet (fast)"
    else:
        fill, border = OPUS_FILL, OPUS_BORDER
        tier_label = "Opus (deep)"
    label = (
        f"<<B>{title}</B><BR/>"
        f"<FONT POINT-SIZE=\"9\">{body}</FONT><BR/>"
        f"<FONT POINT-SIZE=\"9\" COLOR=\"#555555\">[{tier_label}]</FONT>>"
    )
    g.node(nid, label=label, fillcolor=fill, color=border, penwidth="1.6",
           shape="box", style="rounded,filled")


def _json_node(g, jid: str, name: str) -> None:
    g.node(jid, name, shape="oval", style="filled",
           fillcolor=JSON_FILL, color=JSON_BORDER,
           fontsize="9", fontname="Helvetica-Oblique",
           width="1.7", height="0.40", margin="0.06,0.04")


@renderer("mbe_e1_research_agent_8phases")
def render():
    g = make_digraph("e1_pipeline", rankdir="LR")
    g.attr(ranksep="0.7", nodesep="0.4", splines="spline",
           compound="true", newrank="true",
           label="Research-Agent 8-Phase Pipeline (CampusRide v4.2)",
           labelloc="t", fontsize="14")
    g.attr("node", fontsize="10")

    # --- External sources (top-left, feed P1) ---
    with g.subgraph(name="cluster_sources") as c:
        c.attr(label="External corpus sources",
               style="rounded,filled", color=SOURCE_BORDER,
               fillcolor=SOURCE_FILL, fontsize="11", penwidth="1.3")
        c.node("src_oa", "OpenAlex",
               fillcolor="#FFFFFF", color=SOURCE_BORDER, fontsize="10")
        c.node("src_ss", "Semantic Scholar",
               fillcolor="#FFFFFF", color=SOURCE_BORDER, fontsize="10")
        c.node("src_arxiv", "arXiv",
               fillcolor="#FFFFFF", color=SOURCE_BORDER, fontsize="10")
        c.node("src_lens", "Lens",
               fillcolor="#FFFFFF", color=SOURCE_BORDER, fontsize="10")
        c.node("src_cr", "Crossref",
               fillcolor="#FFFFFF", color=SOURCE_BORDER, fontsize="10")

    # --- Phase nodes (LR chain) ---
    _phase_node(g, "p1",
                "P1 Corpus Assembly",
                "5 sources -&gt; DOI-keyed canonical IDs",
                "sonnet")
    _phase_node(g, "p2",
                "P2 Classification",
                "one of A..J per paper<BR/>"
                "conf&lt;0.6 -&gt; needs_review<BR/>"
                "abstract&lt;50w -&gt; incomplete",
                "sonnet")
    _phase_node(g, "p25",
                "P2.5 Deep Extraction",
                "MinerU md preferred over abstract<BR/>"
                "7 fields: key_claim, methods,<BR/>"
                "findings, evidence_type,<BR/>"
                "scope, limits, theory",
                "sonnet")
    _phase_node(g, "p3",
                "P3 Relationship Graph",
                "edges: cites, conceptual_overlap,<BR/>"
                "methodological_mirror,<BR/>"
                "temporal_succession, contradiction<BR/>"
                "+ per-cat evidence-sufficiency",
                "opus")
    _phase_node(g, "p35",
                "P3.5 Narrative Chain",
                "7 beats: spine + supporting + anchor<BR/>"
                "spine in citation time order<BR/>"
                "primary != motivation papers",
                "opus")
    _phase_node(g, "p37",
                "P3.7 Contradiction Map",
                "F1 Gap/Substitute, F2 Grassroots,<BR/>"
                "F3 .edu Trust, F4 Rating Fairness,<BR/>"
                "F5 Gamification Risk<BR/>"
                "severity: critical/moderate/minor",
                "opus")
    _phase_node(g, "p4",
                "P4 Evidence Inventory",
                "cross-ref findings F1..F6<BR/>"
                "vs corpus citations",
                "sonnet")
    _phase_node(g, "p5",
                "P5 Five-Reviewer Eval",
                "Narrative 25% / Coverage 25% /<BR/>"
                "Gap 20% / Contradiction 15% /<BR/>"
                "Honesty 15%<BR/>"
                "auto-backtrack if score gates fail",
                "opus")

    # --- Output JSON ovals (one per phase) ---
    _json_node(g, "j_corpus", "corpus.json")
    _json_node(g, "j_class", "classified.json")
    _json_node(g, "j_extr", "extractions.json")
    _json_node(g, "j_rel", "relationship_graph.json")
    _json_node(g, "j_narr", "narrative_chains.json")
    _json_node(g, "j_con", "contradictions.json")
    _json_node(g, "j_evi", "evidence_inventory.json")
    _json_node(g, "j_eval", "evaluation.json + results.tsv")

    # Pair each phase with its JSON oval on the same horizontal rank.
    # Each pair uses rank=same so the JSON sits beside (not above/below) the
    # phase node, while the LR chain p1->p2->...->p5 still flows horizontally.
    pair_list = [("p1", "j_corpus"), ("p2", "j_class"),
                 ("p25", "j_extr"), ("p3", "j_rel"),
                 ("p35", "j_narr"), ("p37", "j_con"),
                 ("p4", "j_evi"), ("p5", "j_eval")]
    for phase, j in pair_list:
        with g.subgraph() as r:
            r.attr(rank="same")
            r.node(phase)
            r.node(j)
        # dotted edge phase -> json (constraint=false so it does not
        # disrupt the main LR chain ordering)
        g.edge(phase, j, color=JSON_BORDER, style="dotted",
               arrowsize="0.55", constraint="false")

    # --- Source -> P1 ---
    for s in ("src_oa", "src_ss", "src_arxiv", "src_lens", "src_cr"):
        g.edge(s, "p1", color=SOURCE_BORDER, arrowsize="0.7")

    # --- Main LR phase chain ---
    main_chain = [
        ("p1", "p2"),
        ("p2", "p25"),
        ("p25", "p3"),
        ("p3", "p35"),
        ("p35", "p37"),
        ("p37", "p4"),
        ("p4", "p5"),
    ]
    for a, b in main_chain:
        g.edge(a, b, color="#34495E", penwidth="1.6", arrowsize="0.9",
               weight="5")

    # --- Auto-backtrack arrows from P5 -> P3.5 / P3.7 / P4 (red dashed) ---
    # constraint=false so they don't fight the LR rank ordering
    g.edge("p5", "p35",
           label="overall&lt;0.85 weakest=Narrative",
           color=BACKTRACK, fontcolor=BACKTRACK,
           style="dashed", penwidth="1.8", arrowsize="0.9",
           constraint="false")
    g.edge("p5", "p37",
           label="weakest=Contradiction",
           color=BACKTRACK, fontcolor=BACKTRACK,
           style="dashed", penwidth="1.6", arrowsize="0.9",
           constraint="false")
    g.edge("p5", "p4",
           label="honesty&lt;0.80 OR weakest=Coverage/Gap",
           color=BACKTRACK, fontcolor=BACKTRACK,
           style="dashed", penwidth="1.6", arrowsize="0.9",
           constraint="false")

    # --- State invariants box (right side, attached to p5 area) ---
    inv_label = (
        "<<B>State Invariants</B><BR ALIGN=\"LEFT\"/>"
        "&#8226; Append-only corpus<BR ALIGN=\"LEFT\"/>"
        "&#8226; Pipeline resumable via --resume<BR ALIGN=\"LEFT\"/>"
        "&#8226; State saved before/after each phase"
        "<BR ALIGN=\"LEFT\"/>"
        "&#8226; Every API error classified:"
        "<BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;APIKeyMissing / ModelNotFound /"
        "<BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;QuotaExhausted"
        "<BR ALIGN=\"LEFT\"/>"
        "<BR ALIGN=\"LEFT\"/>"
        "<B>Auto-backtrack rule</B><BR ALIGN=\"LEFT\"/>"
        "&#8226; overall &lt; 0.85 -&gt; weakest-dim phase"
        "<BR ALIGN=\"LEFT\"/>"
        "&#8226; honesty &lt; 0.80 -&gt; force P4"
        "<BR ALIGN=\"LEFT\"/>"
        "&#8226; results.tsv per iteration"
        "<BR ALIGN=\"LEFT\"/>>"
    )
    g.node("invariants", label=inv_label, shape="note",
           fillcolor=INVAR_FILL, color=INVAR_BORDER, penwidth="1.4",
           fontsize="10", margin="0.15,0.10")
    # Force invariants to live on right of P5 without altering main chain
    g.edge("p5", "invariants", style="invis", constraint="false",
           weight="1")

    # --- Tier legend (below sources / left side) ---
    legend_label = (
        "<<B>Legend</B><BR ALIGN=\"LEFT\"/>"
        f"<FONT COLOR=\"{SONNET_BORDER}\">&#9632;</FONT>"
        " Sonnet (fast): P1, P2, P2.5, P4"
        "<BR ALIGN=\"LEFT\"/>"
        f"<FONT COLOR=\"{OPUS_BORDER}\">&#9632;</FONT>"
        " Opus (deep): P3, P3.5, P3.7, P5"
        "<BR ALIGN=\"LEFT\"/>"
        f"<FONT COLOR=\"{SOURCE_BORDER}\">&#9632;</FONT>"
        " External corpus source"
        "<BR ALIGN=\"LEFT\"/>"
        f"<FONT COLOR=\"{JSON_BORDER}\">&#9711;</FONT>"
        " Output JSON artifact"
        "<BR ALIGN=\"LEFT\"/>"
        f"<FONT COLOR=\"{BACKTRACK}\">- - -</FONT>"
        " Auto-backtrack (P5 to weakest phase)"
        "<BR ALIGN=\"LEFT\"/>>"
    )
    g.node("legend", label=legend_label, shape="note",
           fillcolor="#F8F9F9", color="#566573", penwidth="1.2",
           fontsize="10", margin="0.15,0.10")
    g.edge("src_cr", "legend", style="invis", constraint="false")

    pdf, png = render_dot(g, "mbe_e1_research_agent_8phases", dpi=240)
    register("mbe_e1_research_agent_8phases", "ok", png_path=png)
    return pdf, png


if __name__ == "__main__":
    render()
