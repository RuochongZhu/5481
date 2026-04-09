"""Phase 3: Relationship Graph & Gap Analysis — networkx + Claude agents."""

from __future__ import annotations

import json
import logging
import os
import re
from collections import Counter

import networkx as nx

from .api_client import (
    BRAIN_PHASE3_GAP,
    BRAIN_PHASE3_RELATIONSHIP,
    OpenCitationsClient,
    agent_run_json,
)
from .knowledge_base import export_research_knowledge_base
from .paper_identity import (
    build_alias_lookup,
    canonicalize_paper_ref,
    extract_source_ids,
    get_s2_lookup_id,
)
from .prompts import RELATIONSHIP_ANALYST, GAP_SYNTHESIZER
from .state_manager import complete_step, is_step_complete, save_state
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")


def run_phase3(state: dict, state_path: str, base_dir: str, client,
               s2=None) -> dict:
    """Orchestrate Phase 3."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    analysis_dir = os.path.join(base_dir, "analysis")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(analysis_dir, exist_ok=True)

    classified_path = os.path.join(proc_dir, "classified.json")
    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return state

    papers = load_json(classified_path)
    log.info(f"Phase 3: analyzing {len(papers)} classified papers")

    # Step 1: Build graph
    if not is_step_complete(state, 3, "build_graph"):
        log.info("=== Phase 3.1: Build relationship graph ===")
        G = build_graph(papers)
        _save_graph(G, os.path.join(proc_dir, "relationship_graph.json"))
        state = complete_step(state, state_path, 3, "build_graph", {
            "nodes": G.number_of_nodes(), "edges": G.number_of_edges()
        })
    else:
        G = _load_graph(os.path.join(proc_dir, "relationship_graph.json"), papers)
        log.info(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Step 1.5: Enrich edges with citationIntent + isInfluential from S2
    if not is_step_complete(state, 3, "citation_intent"):
        log.info("=== Phase 3.1.5: Citation intent enrichment ===")
        enriched = _enrich_citation_intent(G, papers, s2, proc_dir)
        state = complete_step(state, state_path, 3, "citation_intent", {
            "edges_enriched": enriched,
        })
    else:
        log.info("Citation intent already enriched")

    # Step 2: Compute metrics
    if not is_step_complete(state, 3, "compute_metrics"):
        log.info("=== Phase 3.2: Compute graph metrics ===")
        metrics = compute_graph_metrics(G)
        atomic_write_json(os.path.join(analysis_dir, "graph_metrics.json"), metrics)
        state = complete_step(state, state_path, 3, "compute_metrics")
    else:
        metrics = load_json(os.path.join(analysis_dir, "graph_metrics.json"))

    # Step 3: Intersection matrix
    if not is_step_complete(state, 3, "intersection_matrix"):
        log.info("=== Phase 3.3: Category intersection matrix ===")
        matrix = category_intersection_matrix(G)
        cat_stats = category_statistics(papers)
        atomic_write_json(os.path.join(analysis_dir, "intersection_matrix.json"), matrix)
        atomic_write_json(os.path.join(analysis_dir, "category_stats.json"), cat_stats)
        state = complete_step(state, state_path, 3, "intersection_matrix")
    else:
        matrix = load_json(os.path.join(analysis_dir, "intersection_matrix.json"))
        cat_stats = load_json(os.path.join(analysis_dir, "category_stats.json"))

    # Step 4: Relationship Analyst agent
    if not is_step_complete(state, 3, "relationship_analysis"):
        log.info("=== Phase 3.4: Relationship Analyst agent ===")
        refined = _run_relationship_analyst(client, papers, G)
        atomic_write_json(os.path.join(analysis_dir, "relationship_analysis.json"), refined)
        # Merge refined edges back into graph
        if refined and "edges" in refined:
            alias_lookup = build_alias_lookup(papers)
            for edge in refined["edges"]:
                src = canonicalize_paper_ref(edge.get("source"), alias_lookup)
                tgt = canonicalize_paper_ref(edge.get("target"), alias_lookup)
                if src and tgt and G.has_node(src) and G.has_node(tgt):
                    G.add_edge(
                        src,
                        tgt,
                        type=edge.get("type", "related"),
                        evidence=edge.get("evidence", ""),
                        confidence_label="INFERRED",
                        provenance="phase3_relationship_analyst",
                    )
            _save_graph(G, os.path.join(proc_dir, "relationship_graph.json"))
        state = complete_step(state, state_path, 3, "relationship_analysis")
    else:
        refined = load_json(os.path.join(analysis_dir, "relationship_analysis.json"))

    # Step 5: Gap Synthesizer agent
    if not is_step_complete(state, 3, "gap_synthesis"):
        log.info("=== Phase 3.5: Gap Synthesizer agent ===")
        gaps = _run_gap_synthesizer(client, papers, metrics, matrix, cat_stats)
        atomic_write_json(os.path.join(analysis_dir, "gaps_ranked.json"), gaps)
        state = complete_step(state, state_path, 3, "gap_synthesis")

        # Quality check
        qc = {"passed": bool(gaps and gaps.get("gaps"))}
        state["phases"]["3"]["quality_check"] = qc
        save_state(state_path, state)
    else:
        log.info("Gap synthesis already done")

    summary = export_research_knowledge_base(papers, G, proc_dir, analysis_dir, output_dir)
    log.info(
        "Knowledge base exported: %s nodes, %s edges",
        summary.get("total_nodes", 0),
        summary.get("total_edges", 0),
    )

    return state


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_graph(papers: list[dict]) -> nx.DiGraph:
    """Construct directed graph from classified papers."""
    G = nx.DiGraph()
    paper_ids = {p["paperId"] for p in papers}
    alias_lookup = build_alias_lookup(papers)

    for p in papers:
        G.add_node(p["paperId"],
                    title=p.get("title", ""),
                    category=p.get("primary_category", "X"),
                    secondary=p.get("secondary_categories", []),
                    year=p.get("year", 0),
                    citations=p.get("citationCount", 0),
                    source_ids=p.get("source_ids", {}),
                    retrieval_layer=p.get("retrieval_layer", ""),
                    canonical_id=p.get("canonical_id", p["paperId"]))

    for p in papers:
        pid = p["paperId"]
        for ref_id in p.get("builds_on", []):
            canonical = canonicalize_paper_ref(ref_id, alias_lookup)
            if canonical in paper_ids and canonical != pid:
                G.add_edge(
                    canonical,
                    pid,
                    type="builds_on",
                    confidence_label="INFERRED",
                    provenance="phase2_classification",
                )
        for ref_id in p.get("contradicts", []):
            canonical = canonicalize_paper_ref(ref_id, alias_lookup)
            if canonical in paper_ids and canonical != pid:
                G.add_edge(
                    canonical,
                    pid,
                    type="contradicts",
                    confidence_label="INFERRED",
                    provenance="phase2_classification",
                )

    log.info(f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


def _save_graph(G: nx.DiGraph, path: str):
    """Save graph as JSON edge list + node attributes."""
    data = {
        "nodes": [{"id": n, **d} for n, d in G.nodes(data=True)],
        "edges": [{"source": u, "target": v, **d} for u, v, d in G.edges(data=True)],
    }
    atomic_write_json(path, data)


def _load_graph(path: str, papers: list[dict]) -> nx.DiGraph:
    """Load graph from JSON, falling back to rebuild from papers."""
    if os.path.exists(path):
        data = load_json(path)
        G = nx.DiGraph()
        for n in data.get("nodes", []):
            nid = n.get("id")
            attrs = {k: v for k, v in n.items() if k != "id"}
            G.add_node(nid, **attrs)
        for e in data.get("edges", []):
            src = e.get("source")
            tgt = e.get("target")
            attrs = {k: v for k, v in e.items() if k not in ("source", "target")}
            G.add_edge(src, tgt, **attrs)
        return G
    return build_graph(papers)


# ---------------------------------------------------------------------------
# Graph analysis
# ---------------------------------------------------------------------------

def compute_graph_metrics(G: nx.DiGraph) -> dict:
    """Compute key graph metrics."""
    if G.number_of_nodes() == 0:
        return {"empty": True}

    in_deg = dict(G.in_degree())
    out_deg = dict(G.out_degree())

    # Foundational papers: high in-degree, low out-degree
    foundational = sorted(
        [(n, in_deg[n]) for n in G.nodes() if in_deg[n] > 0],
        key=lambda x: x[1], reverse=True
    )[:10]

    # Survey/synthesis papers: high out-degree
    surveys = sorted(
        [(n, out_deg[n]) for n in G.nodes() if out_deg[n] > 0],
        key=lambda x: x[1], reverse=True
    )[:10]

    # Connected components (undirected view)
    components = list(nx.weakly_connected_components(G))

    # Betweenness centrality (top 10)
    try:
        bc = nx.betweenness_centrality(G)
        top_bc = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:10]
    except Exception:
        top_bc = []

    # Isolated nodes (no edges at all)
    isolated = [n for n in G.nodes() if G.degree(n) == 0]

    metrics = {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "foundational_papers": [{"paperId": n, "in_degree": d,
                                  "title": G.nodes[n].get("title", "")} for n, d in foundational],
        "survey_papers": [{"paperId": n, "out_degree": d,
                           "title": G.nodes[n].get("title", "")} for n, d in surveys],
        "num_components": len(components),
        "largest_component_size": max(len(c) for c in components) if components else 0,
        "isolated_count": len(isolated),
        "top_betweenness": [{"paperId": n, "centrality": round(c, 4)} for n, c in top_bc],
        "edge_type_counts": dict(Counter(d.get("type", "unknown") for _, _, d in G.edges(data=True))),
    }
    log.info(f"Graph metrics: {metrics['total_nodes']} nodes, {metrics['total_edges']} edges, "
             f"{metrics['num_components']} components, {metrics['isolated_count']} isolated")
    return metrics


def category_intersection_matrix(G: nx.DiGraph) -> dict:
    """For each category pair: edge count, bridging papers, edge types."""
    categories = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    cat_nodes = {}
    for cat in categories:
        cat_nodes[cat] = {n for n, d in G.nodes(data=True) if d.get("category") == cat}

    matrix = {}
    for i, c1 in enumerate(categories):
        for c2 in categories[i+1:]:
            n1, n2 = cat_nodes[c1], cat_nodes[c2]
            cross_edges = [
                (u, v, d) for u, v, d in G.edges(data=True)
                if (u in n1 and v in n2) or (u in n2 and v in n1)
            ]
            # Papers with secondary category bridging
            bridging = [
                n for n, d in G.nodes(data=True)
                if (d.get("category") == c1 and c2 in d.get("secondary", []))
                or (d.get("category") == c2 and c1 in d.get("secondary", []))
            ]
            key = f"{c1}-{c2}"
            matrix[key] = {
                "edge_count": len(cross_edges),
                "bridging_papers": len(bridging),
                "edge_types": dict(Counter(d.get("type", "unknown") for _, _, d in cross_edges)),
            }

    # Log sparse pairs
    sparse = [k for k, v in matrix.items() if v["edge_count"] == 0 and v["bridging_papers"] == 0]
    if sparse:
        log.info(f"Sparse category pairs (potential gaps): {sparse}")

    return matrix


def category_statistics(papers: list[dict]) -> dict:
    """Per-category: paper count, median year, median citations, gaps."""
    import statistics
    categories = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "X"]
    stats = {}
    for cat in categories:
        cat_papers = [p for p in papers if p.get("primary_category") == cat]
        if not cat_papers:
            stats[cat] = {"count": 0}
            continue
        years = [p.get("year", 0) for p in cat_papers if p.get("year")]
        cites = [p.get("citationCount", 0) for p in cat_papers]
        gaps = [p.get("gap_it_leaves", "") for p in cat_papers if p.get("gap_it_leaves")]
        stats[cat] = {
            "count": len(cat_papers),
            "median_year": statistics.median(years) if years else 0,
            "median_citations": statistics.median(cites) if cites else 0,
            "top_gaps": gaps[:10],  # First 10 gaps for the agent
        }
    return stats


# ---------------------------------------------------------------------------
# Agent calls
# ---------------------------------------------------------------------------

def _run_relationship_analyst(client, papers: list[dict], G: nx.DiGraph) -> dict:
    """Send top papers to Relationship Analyst for edge refinement."""
    # Select top 50 papers by citation count for deeper analysis
    top_papers = sorted(papers, key=lambda p: p.get("citationCount", 0), reverse=True)[:50]
    batch_input = _format_papers_for_analyst(top_papers)

    try:
        result = agent_run_json(
            client,
            role=RELATIONSHIP_ANALYST,
            model=BRAIN_PHASE3_RELATIONSHIP,
            task=(
                f"Analyze relationships between these {len(top_papers)} papers. "
                f"The current graph has {G.number_of_edges()} edges. "
                f"Identify additional builds_on, contradicts, and extends relationships.\n\n"
                f"{batch_input}"
            ),
            max_tokens=4096,
        )
        edges_found = len(result.get("edges", [])) if isinstance(result, dict) else 0
        log.info(f"Relationship Analyst found {edges_found} additional edges")
        return result
    except Exception as e:
        log.error(f"Relationship Analyst failed: {e}")
        return {"edges": [], "orphans": [], "notes": f"Error: {e}"}


def _run_gap_synthesizer(client, papers: list[dict], metrics: dict,
                          matrix: dict, cat_stats: dict) -> dict:
    """Send analysis to Gap Synthesizer for research gap identification."""
    # Build a concise summary for the agent
    summary = _build_gap_synthesis_input(papers, metrics, matrix, cat_stats)

    try:
        result = agent_run_json(
            client,
            role=GAP_SYNTHESIZER,
            model=BRAIN_PHASE3_GAP,
            task=summary,
            max_tokens=4096,
        )
        gap_count = len(result.get("gaps", [])) if isinstance(result, dict) else 0
        log.info(f"Gap Synthesizer identified {gap_count} research gaps")
        return result
    except Exception as e:
        log.error(f"Gap Synthesizer failed: {e}")
        return {"gaps": [], "field_observations": {"error": str(e)}}


def _format_papers_for_analyst(papers: list[dict]) -> str:
    """Format papers for the Relationship Analyst."""
    lines = []
    for p in papers:
        lines.append(
            f"paperId: {p['paperId']}\n"
            f"title: {p.get('title', 'N/A')}\n"
            f"category: {p.get('primary_category', 'X')}\n"
            f"year: {p.get('year', 'N/A')}\n"
            f"abstract: {(p.get('abstract') or '')[:300]}\n"
            f"---"
        )
    return "\n".join(lines)


def _build_gap_synthesis_input(papers: list[dict], metrics: dict,
                                matrix: dict, cat_stats: dict) -> str:
    """Build the structured input for the Gap Synthesizer agent."""
    # Foundational papers summary
    found_str = "\n".join(
        f"  - {f['title'][:80]} (in_degree={f['in_degree']})"
        for f in metrics.get("foundational_papers", [])[:5]
    )

    # Intersection matrix summary
    matrix_lines = []
    for pair, data in sorted(matrix.items()):
        matrix_lines.append(f"  {pair}: edges={data['edge_count']}, bridging={data['bridging_papers']}")
    matrix_str = "\n".join(matrix_lines)

    # Category stats summary
    cat_lines = []
    for cat, s in sorted(cat_stats.items()):
        if cat == "X" or s.get("count", 0) == 0:
            continue
        cat_lines.append(
            f"  {cat}: {s['count']} papers, median_year={s.get('median_year', 'N/A')}, "
            f"median_cites={s.get('median_citations', 'N/A')}"
        )
    cat_str = "\n".join(cat_lines)

    # Aggregated gaps
    all_gaps = []
    for cat, s in cat_stats.items():
        for g in s.get("top_gaps", []):
            all_gaps.append(f"  [{cat}] {g}")
    gaps_str = "\n".join(all_gaps[:30])  # Limit to 30

    return (
        f"Assess evidence sufficiency for a 5-beat research paper using this corpus of {len(papers)} papers.\n\n"
        f"## Foundational Papers (highest in-degree)\n{found_str}\n\n"
        f"## Category Intersection Matrix\n{matrix_str}\n\n"
        f"## Category Statistics\n{cat_str}\n\n"
        f"## Per-Category Gaps (what papers leave unaddressed)\n{gaps_str}\n\n"
        f"## Graph Summary\n"
        f"  Nodes: {metrics.get('total_nodes', 0)}, Edges: {metrics.get('total_edges', 0)}\n"
        f"  Components: {metrics.get('num_components', 0)}, Isolated: {metrics.get('isolated_count', 0)}\n"
        f"  Edge types: {metrics.get('edge_type_counts', {})}\n\n"
        f"Assess each beat's evidence strength. Identify missing key papers and the strongest narrative thread."
    )


# ---------------------------------------------------------------------------
# Citation Intent enrichment (S2 API)
# ---------------------------------------------------------------------------

def _enrich_citation_intent(G: nx.DiGraph, papers: list[dict],
                             s2, proc_dir: str) -> int:
    """Fetch citationIntent + isInfluential for edges via S2 API.

    S2 returns intents as: Background, Methodology, ResultComparison.
    This enriches existing graph edges and discovers new ones.
    If S2 lookup fails or yields no internal matches, fall back to DOI-to-DOI
    citations from OpenCitations.
    """
    corpus_ids = {p["paperId"] for p in papers}
    alias_lookup = build_alias_lookup(papers)
    oc = OpenCitationsClient(access_token=os.environ.get("OPENCITATIONS_ACCESS_TOKEN") or None)
    candidates = [
        p for p in papers
        if get_s2_lookup_id(p) or extract_source_ids(p).get("doi")
    ]

    if s2 is None:
        log.warning("No S2 client — Phase 3 will use OpenCitations fallback only where DOI is available")

    enriched = 0
    intent_path = os.path.join(proc_dir, "citation_intents.json")

    # Load existing progress
    if os.path.exists(intent_path):
        from .utils import load_json as _lj
        intent_data = _lj(intent_path)
    else:
        intent_data = {}

    for i, p in enumerate(candidates):
        pid = p["paperId"]
        if pid in intent_data:
            continue
        paper_doi = extract_source_ids(p).get("doi")
        edges = []
        try:
            s2_pid = get_s2_lookup_id(p)
            if s2 is not None and s2_pid:
                data = s2._get(
                    f"https://api.semanticscholar.org/graph/v1/paper/{s2_pid}/citations",
                    {"fields": "paperId,intents,isInfluential", "limit": 200}
                )
                citations = data.get("data", [])
                for c in citations:
                    citing = c.get("citingPaper", {})
                    citing_id = canonicalize_paper_ref(citing.get("paperId", ""), alias_lookup)
                    if citing_id in corpus_ids:
                        intents = c.get("intents", [])
                        influential = c.get("isInfluential", False)
                        edges.append({
                            "citing": citing_id,
                            "intents": intents,
                            "isInfluential": influential,
                            "provenance": "semantic_scholar",
                        })
                        _merge_citation_edge(
                            G,
                            citing_id,
                            pid,
                            intents=intents,
                            influential=influential,
                            source_name="semantic_scholar",
                            provenance="s2_citation_intent",
                        )
                        enriched += 1

            if not edges and paper_doi:
                fallback_edges = _enrich_with_opencitations(
                    G,
                    oc,
                    target_id=pid,
                    target_doi=paper_doi,
                    corpus_ids=corpus_ids,
                    alias_lookup=alias_lookup,
                )
                edges.extend(fallback_edges)
                enriched += len(fallback_edges)
        except Exception as e:
            if (i + 1) % 50 == 0:
                log.warning(f"  Intent fetch failed for {pid}: {e}")
            if paper_doi and not edges:
                fallback_edges = _enrich_with_opencitations(
                    G,
                    oc,
                    target_id=pid,
                    target_doi=paper_doi,
                    corpus_ids=corpus_ids,
                    alias_lookup=alias_lookup,
                )
                edges.extend(fallback_edges)
                enriched += len(fallback_edges)

        intent_data[pid] = edges

        if (i + 1) % 20 == 0:
            log.info(f"  Intent enrichment: {i+1}/{len(candidates)} papers, {enriched} edges enriched")
            atomic_write_json(intent_path, intent_data)

    atomic_write_json(intent_path, intent_data)
    _save_graph(G, os.path.join(proc_dir, "relationship_graph.json"))

    # Count intent distribution
    intent_counts = Counter()
    for edges in intent_data.values():
        for e in edges:
            for intent in e.get("intents", []):
                intent_counts[intent] += 1
    log.info(f"Citation intents: {dict(intent_counts)}, {enriched} edges enriched")
    return enriched


def _extract_dois_from_oc_field(value: str) -> list[str]:
    if not value:
        return []
    return re.findall(r"doi:([^\s;]+)", value, flags=re.I)


def _merge_citation_edge(G: nx.DiGraph, citing_id: str, cited_id: str,
                         intents: list[str], influential, source_name: str,
                         provenance: str):
    if G.has_edge(citing_id, cited_id):
        edge = G[citing_id][cited_id]
        edge.setdefault("intents", [])
        if intents:
            merged_intents = sorted(set(edge.get("intents", [])) | set(intents))
            edge["intents"] = merged_intents
        if influential is not None:
            edge["isInfluential"] = influential
        sources = set(edge.get("citation_sources", []))
        sources.add(source_name)
        edge["citation_sources"] = sorted(sources)
        edge.setdefault("confidence_label", "EXTRACTED")
        edge.setdefault("provenance", provenance)
        return

    if G.has_node(citing_id) and G.has_node(cited_id):
        G.add_edge(
            citing_id,
            cited_id,
            type="cites",
            intents=intents,
            isInfluential=influential,
            confidence_label="EXTRACTED",
            provenance=provenance,
            citation_sources=[source_name],
        )


def _enrich_with_opencitations(G: nx.DiGraph, oc: OpenCitationsClient, target_id: str,
                               target_doi: str, corpus_ids: set[str],
                               alias_lookup: dict[str, str]) -> list[dict]:
    """Fallback DOI-to-DOI citation expansion for incoming citations."""
    try:
        citations = oc.get_citations(target_doi)
    except Exception as e:
        log.debug(f"  OpenCitations fallback failed for DOI {target_doi}: {e}")
        return []

    edges = []
    seen = set()
    for row in citations:
        for citing_doi in _extract_dois_from_oc_field(row.get("citing", "")):
            canonical = canonicalize_paper_ref(citing_doi.lower(), alias_lookup)
            if canonical not in corpus_ids:
                canonical = canonicalize_paper_ref(f"doi:{citing_doi.lower()}", alias_lookup)
            if canonical in corpus_ids and canonical != target_id and canonical not in seen:
                seen.add(canonical)
                edges.append({
                    "citing": canonical,
                    "intents": [],
                    "isInfluential": None,
                    "provenance": "opencitations",
                })
                _merge_citation_edge(
                    G,
                    canonical,
                    target_id,
                    intents=[],
                    influential=None,
                    source_name="opencitations",
                    provenance="opencitations_fallback",
                )
    return edges
