"""Persistent research knowledge graph + report + wiki export."""

from __future__ import annotations

import hashlib
import os
from collections import Counter, defaultdict

import networkx as nx

from .paper_identity import build_alias_lookup, canonicalize_paper_ref
from .utils import atomic_write_json

# Import centralized beat definitions
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.beat_definitions import BEAT_CATEGORIES as _BEAT_CATS, BEAT_NAMES as _BEAT_NAMES, ARGUMENT_LINES

BEAT_CATEGORIES = {
    beat: {"name": _BEAT_NAMES[beat], "categories": cats, "argument_line": ARGUMENT_LINES[beat]}
    for beat, cats in _BEAT_CATS.items()
}


def _safe_slug(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    cleaned = "".join(c if c.isalnum() else "_" for c in text)[:48].strip("_")
    return f"{cleaned or 'item'}_{digest}"


def _add_or_merge_edge(G: nx.DiGraph, src: str, tgt: str, relation: str, **attrs):
    if not src or not tgt or src == tgt:
        return

    if G.has_edge(src, tgt):
        edge = G[src][tgt]
        rels = set(edge.get("relation_types") or [edge.get("relation", relation)])
        rels.add(relation)
        edge["relation_types"] = sorted(r for r in rels if r)
        edge["relation"] = edge["relation_types"][0]
        for key, value in attrs.items():
            if value is None:
                continue
            if key not in edge or edge.get(key) in ("", None, []):
                edge[key] = value
    else:
        payload = {
            "relation": relation,
            "relation_types": [relation],
            **{k: v for k, v in attrs.items() if v is not None},
        }
        G.add_edge(src, tgt, **payload)


def build_research_knowledge_graph(papers: list[dict], relationship_graph: nx.DiGraph | None = None) -> nx.DiGraph:
    """Build a richer graph than the paper-only relationship graph.

    This graph keeps paper-paper edges but also adds category/beat/query/source nodes so
    agents can navigate the corpus structurally even when citation edges are sparse.
    """
    G = nx.DiGraph()
    alias_lookup = build_alias_lookup(papers)

    for cat in sorted({p.get("primary_category", "X") for p in papers} | {"X"}):
        cid = f"category:{cat}"
        G.add_node(cid, node_type="category", label=f"Category {cat}", category=cat)

    for beat, cfg in BEAT_CATEGORIES.items():
        bid = f"beat:{beat}"
        G.add_node(
            bid,
            node_type="beat",
            label=cfg["name"],
            beat=beat,
            categories=cfg["categories"],
        )

    for paper in papers:
        pid = paper["paperId"]
        primary = paper.get("primary_category") or paper.get("query_category") or "X"
        G.add_node(
            pid,
            node_type="paper",
            label=paper.get("title", pid),
            title=paper.get("title", ""),
            category=primary,
            secondary=paper.get("secondary_categories", []),
            year=paper.get("year", 0),
            citations=paper.get("citationCount", 0),
            source=paper.get("source", ""),
            retrieval_layer=paper.get("retrieval_layer", ""),
            source_ids=paper.get("source_ids", {}),
            canonical_id=paper.get("canonical_id", pid),
            doi=(paper.get("source_ids", {}) or {}).get("doi", ""),
            publisher=(paper.get("integrity", {}) or {}).get("publisher", ""),
            is_retracted=bool((paper.get("integrity", {}) or {}).get("is_retracted")),
            license_urls=(paper.get("integrity", {}) or {}).get("license_urls", []),
        )

        _add_or_merge_edge(
            G,
            pid,
            f"category:{primary}",
            "classified_as",
            confidence_label="EXTRACTED",
            provenance="phase2_classification",
        )

        for sec in paper.get("secondary_categories", []):
            _add_or_merge_edge(
                G,
                pid,
                f"category:{sec}",
                "secondary_category",
                confidence_label="INFERRED",
                provenance="phase2_classification",
            )

        source = paper.get("source") or "unknown"
        sid = f"source:{source}"
        if sid not in G:
            G.add_node(sid, node_type="source", label=source)
        _add_or_merge_edge(
            G,
            sid,
            pid,
            "provided_record",
            confidence_label="EXTRACTED",
        )

        retrieval_layer = paper.get("retrieval_layer")
        if retrieval_layer:
            lid = f"layer:{retrieval_layer}"
            if lid not in G:
                G.add_node(lid, node_type="layer", label=retrieval_layer)
            _add_or_merge_edge(
                G,
                lid,
                pid,
                "retrieved_via",
                confidence_label="EXTRACTED",
            )

        matched_query = (paper.get("matched_query") or "").strip()
        if matched_query:
            qid = f"query:{_safe_slug(matched_query)}"
            if qid not in G:
                G.add_node(qid, node_type="query", label=matched_query, query=matched_query)
            _add_or_merge_edge(
                G,
                qid,
                pid,
                "retrieved",
                confidence_label="EXTRACTED",
                query_category=paper.get("query_category"),
            )

        for beat, cfg in BEAT_CATEGORIES.items():
            cats = set(cfg["categories"])
            if primary in cats or any(sec in cats for sec in paper.get("secondary_categories", [])):
                _add_or_merge_edge(
                    G,
                    pid,
                    f"beat:{beat}",
                    "supports_beat",
                    confidence_label="INFERRED",
                )

    if relationship_graph is not None:
        for src, tgt, data in relationship_graph.edges(data=True):
            if src in G and tgt in G:
                _add_or_merge_edge(
                    G,
                    src,
                    tgt,
                    data.get("type", "related"),
                    confidence_label=data.get("confidence_label") or "INFERRED",
                    evidence=data.get("evidence", ""),
                    intents=data.get("intents", []),
                    isInfluential=data.get("isInfluential"),
                )
    else:
        for paper in papers:
            pid = paper["paperId"]
            for ref_id in paper.get("builds_on", []):
                canonical = canonicalize_paper_ref(ref_id, alias_lookup)
                if canonical and canonical in G:
                    _add_or_merge_edge(
                        G,
                        canonical,
                        pid,
                        "builds_on",
                        confidence_label="INFERRED",
                        provenance="phase2_classification",
                    )
            for ref_id in paper.get("contradicts", []):
                canonical = canonicalize_paper_ref(ref_id, alias_lookup)
                if canonical and canonical in G:
                    _add_or_merge_edge(
                        G,
                        canonical,
                        pid,
                        "contradicts",
                        confidence_label="INFERRED",
                        provenance="phase2_classification",
                    )

    return G


def assign_graph_communities(G: nx.DiGraph) -> dict[int, str]:
    """Cluster the graph and return human-readable community labels."""
    if G.number_of_nodes() == 0:
        return {}

    undirected = G.to_undirected()
    if undirected.number_of_edges() == 0:
        communities = [{n} for n in undirected.nodes()]
    else:
        communities = list(nx.algorithms.community.greedy_modularity_communities(undirected))

    labels = {}
    for cid, nodes in enumerate(sorted(communities, key=len, reverse=True)):
        for nid in nodes:
            G.nodes[nid]["community"] = cid

        paper_titles = [
            G.nodes[n].get("title") or G.nodes[n].get("label", "")
            for n in nodes
            if G.nodes[n].get("node_type") == "paper"
        ]
        category_labels = [
            G.nodes[n].get("label", "")
            for n in nodes
            if G.nodes[n].get("node_type") == "category"
        ]
        label = next((c for c in category_labels if c), None)
        if not label and paper_titles:
            label = paper_titles[0][:60]
        labels[cid] = label or f"Community {cid}"

    return labels


def summarize_research_graph(G: nx.DiGraph, community_labels: dict[int, str]) -> dict:
    node_type_counts = Counter(data.get("node_type", "unknown") for _, data in G.nodes(data=True))
    relation_counts = Counter(data.get("relation", "related") for _, _, data in G.edges(data=True))
    paper_nodes = [
        (nid, data)
        for nid, data in G.nodes(data=True)
        if data.get("node_type") == "paper"
    ]
    publisher_counts = Counter(
        data.get("publisher", "")
        for _, data in paper_nodes
        if data.get("publisher")
    )

    communities = defaultdict(list)
    for nid, data in G.nodes(data=True):
        communities[data.get("community", -1)].append(nid)

    community_summaries = []
    for cid, nodes in sorted(communities.items(), key=lambda item: len(item[1]), reverse=True):
        top_nodes = sorted(nodes, key=lambda n: G.degree(n), reverse=True)[:8]
        community_summaries.append({
            "community": cid,
            "label": community_labels.get(cid, f"Community {cid}"),
            "size": len(nodes),
            "top_nodes": [
                {
                    "id": nid,
                    "label": G.nodes[nid].get("label", nid),
                    "node_type": G.nodes[nid].get("node_type", "unknown"),
                    "degree": G.degree(nid),
                }
                for nid in top_nodes
            ],
        })

    top_hubs = sorted(G.nodes(), key=lambda n: G.degree(n), reverse=True)[:15]
    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "node_type_counts": dict(node_type_counts),
        "relation_counts": dict(relation_counts),
        "paper_integrity": {
            "paper_nodes": len(paper_nodes),
            "with_doi": sum(1 for _, data in paper_nodes if data.get("doi")),
            "with_publisher": sum(1 for _, data in paper_nodes if data.get("publisher")),
            "retracted_count": sum(1 for _, data in paper_nodes if data.get("is_retracted")),
            "top_publishers": [
                {"publisher": publisher, "count": count}
                for publisher, count in publisher_counts.most_common(10)
            ],
        },
        "communities": community_summaries,
        "top_hubs": [
            {
                "id": nid,
                "label": G.nodes[nid].get("label", nid),
                "node_type": G.nodes[nid].get("node_type", "unknown"),
                "degree": G.degree(nid),
            }
            for nid in top_hubs
        ],
    }


def serialize_graph(G: nx.DiGraph) -> dict:
    return {
        "nodes": [{"id": nid, **attrs} for nid, attrs in G.nodes(data=True)],
        "edges": [{"source": src, "target": tgt, **attrs} for src, tgt, attrs in G.edges(data=True)],
    }


def render_graph_report(summary: dict) -> str:
    lines = [
        "# Research Knowledge Graph Report",
        "",
        f"**Nodes:** {summary['total_nodes']}  ",
        f"**Edges:** {summary['total_edges']}",
        "",
        "## Node Types",
        "",
    ]

    for kind, count in sorted(summary.get("node_type_counts", {}).items()):
        lines.append(f"- {kind}: {count}")

    lines += ["", "## Relation Types", ""]
    for rel, count in sorted(summary.get("relation_counts", {}).items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {rel}: {count}")

    integrity = summary.get("paper_integrity", {})
    lines += ["", "## Integrity Signals", ""]
    lines.append(f"- Paper nodes: {integrity.get('paper_nodes', 0)}")
    lines.append(f"- With DOI: {integrity.get('with_doi', 0)}")
    lines.append(f"- With publisher metadata: {integrity.get('with_publisher', 0)}")
    lines.append(f"- Retracted flagged: {integrity.get('retracted_count', 0)}")
    for item in integrity.get("top_publishers", [])[:5]:
        lines.append(f"- Publisher: {item['publisher']} ({item['count']})")

    lines += ["", "## Top Hubs", ""]
    for item in summary.get("top_hubs", []):
        lines.append(f"- {item['label']} ({item['node_type']}, degree={item['degree']})")

    lines += ["", "## Communities", ""]
    for community in summary.get("communities", []):
        lines.append(f"### {community['label']} ({community['size']} nodes)")
        for node in community.get("top_nodes", [])[:5]:
            lines.append(f"- {node['label']} ({node['node_type']}, degree={node['degree']})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _safe_filename(name: str) -> str:
    return name.replace("/", "-").replace(" ", "_").replace(":", "-")


def export_wiki(G: nx.DiGraph, summary: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    communities = summary.get("communities", [])
    community_map = defaultdict(list)
    for nid, data in G.nodes(data=True):
        community_map[data.get("community", -1)].append(nid)

    index_lines = [
        "# Research Knowledge Wiki",
        "",
        "> Agent-readable graph wiki. Start here before scanning raw corpus files.",
        "",
        f"**{summary['total_nodes']} nodes · {summary['total_edges']} edges · {len(communities)} communities**",
        "",
        "## Communities",
        "",
    ]

    for community in communities:
        label = community["label"]
        index_lines.append(f"- [[{label}]] — {community['size']} nodes")

        nodes = community_map.get(community["community"], [])
        lines = [
            f"# {label}",
            "",
            f"> {community['size']} nodes in this community",
            "",
            "## Key Nodes",
            "",
        ]
        for node in community.get("top_nodes", []):
            lines.append(f"- **{node['label']}** ({node['node_type']}, degree={node['degree']})")

        lines += ["", "## Member Nodes", ""]
        for nid in sorted(nodes, key=lambda node_id: G.degree(node_id), reverse=True)[:40]:
            node = G.nodes[nid]
            lines.append(f"- {node.get('label', nid)} [{node.get('node_type', 'unknown')}]")

        lines += ["", "---", "", "*Auto-generated from the research knowledge graph.*"]
        with open(os.path.join(output_dir, f"{_safe_filename(label)}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    index_lines += ["", "## Top Hubs", ""]
    for item in summary.get("top_hubs", [])[:15]:
        index_lines.append(f"- {item['label']} ({item['node_type']}, degree={item['degree']})")

    with open(os.path.join(output_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines) + "\n")


def export_research_knowledge_base(
    papers: list[dict],
    relationship_graph: nx.DiGraph,
    proc_dir: str,
    analysis_dir: str,
    output_dir: str,
) -> dict:
    """Build and export the persistent graph layer used by downstream agents."""
    G = build_research_knowledge_graph(papers, relationship_graph)
    community_labels = assign_graph_communities(G)
    summary = summarize_research_graph(G, community_labels)

    atomic_write_json(os.path.join(proc_dir, "research_knowledge_graph.json"), serialize_graph(G))
    atomic_write_json(os.path.join(analysis_dir, "research_knowledge_graph_summary.json"), summary)

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "research_knowledge_graph.md"), "w", encoding="utf-8") as f:
        f.write(render_graph_report(summary))

    export_wiki(G, summary, os.path.join(output_dir, "knowledge_wiki"))
    return summary
