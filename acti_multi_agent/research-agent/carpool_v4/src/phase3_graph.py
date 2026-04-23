"""Phase 3: Relationship Graph & Gap Analysis — networkx + Claude agents."""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
from collections import Counter, defaultdict

import networkx as nx

from .api_client import (
    BRAIN_PHASE3_GAP,
    BRAIN_PHASE3_RELATIONSHIP,
    OpenCitationsClient,
    agent_run,
    agent_run_json,
)
from .knowledge_base import export_research_knowledge_base
from .paper_identity import (
    build_alias_lookup,
    canonicalize_paper_ref,
    extract_source_ids,
    get_s2_lookup_id,
)
from .phase_contracts import ensure_gap_analysis_valid, ensure_relationship_analysis_valid
from .prompts import RELATIONSHIP_ANALYST, GAP_SYNTHESIZER
from .state_manager import complete_step, is_step_complete, save_state
from .utils import atomic_write_json, load_json, filter_active_papers

import sys as _sys_alias
_sys_alias.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.beat_definitions import CATEGORY_SEQUENCE  # noqa: E402

log = logging.getLogger("research_agent")

BEAT_REQUIREMENTS = {
    1: {
        "name": "Small-Town Campus Transportation & Coordination Gaps",
        "argument_line": "motivation",
        "categories": ["A", "B"],
        "pairs": ["A-B"],
        "missing_titles": [
            "Shaheen & Cohen shared mobility review anchor",
            "Small-town / rural university rideshare coverage anchor",
            "Campus mobility access empirical study anchor",
        ],
    },
    2: {
        "name": "Grassroots Coordination & Integrated Campus Platforms",
        "argument_line": "motivation",
        "categories": ["C", "D", "I"],
        "pairs": ["C-D", "D-I"],
        "missing_titles": [
            "WeChat / WhatsApp grassroots coordination anchor",
            "International students US-university digital-practice anchor",
            "Super-app / integrated-platform campus-scope anchor",
        ],
    },
    3: {
        "name": "Design Primitives: Identity, Safety, Rating Fairness, Rewards",
        "argument_line": "framework",
        "categories": ["E", "F", "G", "H"],
        "pairs": ["E-F", "F-H", "G-H"],
        "missing_titles": [
            "Institutional / .edu identity verification design anchor",
            "Rideshare safety real-time-location + SOS anchor",
            "Peer rating fairness + algorithmic management anchor",
            "Gamification in mobility / coordination anchor",
        ],
    },
    4: {
        "name": "Formative Survey: Passenger-Side WTP & Motivations",
        "argument_line": "primary",
        "categories": [],
        "pairs": [],
        "beat_type": "primary_data",
        "primary_anchor": "local:CornellCarpoolSurvey2026",
        "missing_titles": [],
    },
    5: {
        "name": "Formative Survey: Driver-Side Tolerance & Rating-Fairness Asymmetry",
        "argument_line": "primary",
        "categories": ["F", "H"],
        "pairs": ["F-H"],
        "missing_titles": [
            "Rosenblat & Stark / Lee et al. algorithmic management anchor",
            "Driver experience + rating fairness empirical anchor",
        ],
    },
    6: {
        "name": "CampusRide Multi-Module Platform Design with Carpool Deep-Dive",
        "argument_line": "core_contribution",
        "categories": [],
        "pairs": [],
        "beat_type": "artifact",
        "primary_anchor": "local:CampusRideSystem2026",
        "missing_titles": [],
    },
    7: {
        "name": "Adversarial Scoping: Formalization Risk, Sample Skew, No Deployment",
        "argument_line": "adversarial",
        "categories": ["J", "H"],
        "pairs": ["H-J"],
        "missing_titles": [
            "Rosenblat & Stark algorithmic management critique anchor",
            "Lee et al. gig-worker experience anchor",
            "Gamification overjustification / gaming-behavior anchor",
            "Platform-labor / rideshare driver precarity anchor",
            "Sample-skew acknowledgment (international-student overrepresentation) anchor",
        ],
    },
}


# ---------------------------------------------------------------------------
# v4.2 Extended Edge Extraction (Prompt D)
# ---------------------------------------------------------------------------
# Stopwords that MUST be filtered out of CONCEPTUAL_OVERLAP keyword matching.
# The v4.2 guide is explicit: generic nouns ("user", "study", "design",
# "system", "paper", "model", "research", "approach", "work", "result") cause
# false-positive keyword overlaps to explode. Keep this list conservative but
# cover the most common surface forms (plurals, common English stopwords,
# and a handful of paper-writing boilerplate tokens).
DOMAIN_STOPWORDS: set[str] = {
    # guide-mandated exclusions
    "user", "users", "study", "studies", "design", "designs",
    "system", "systems", "paper", "papers", "model", "models",
    "research", "approach", "approaches", "work", "works",
    "result", "results",
    # trivial English stopwords that sneak through word-split tokenization
    "the", "and", "for", "with", "that", "this", "from", "into", "are",
    "was", "were", "have", "has", "had", "but", "not", "our", "their",
    "its", "they", "them", "these", "those", "such", "also", "can",
    "may", "will", "been", "being", "more", "most", "other", "than",
    "between", "across", "over", "under", "through", "both", "all",
    "any", "each", "some", "many", "few", "new", "novel",
    # boilerplate research-prose tokens
    "abstract", "introduction", "method", "methods", "methodology",
    "methodologies", "finding", "findings", "data", "datum", "analysis",
    "analyses", "conclusion", "conclusions", "discussion", "future",
    "propose", "proposed", "present", "presented", "show", "shows",
    "demonstrate", "demonstrates", "using", "use", "used", "based",
    "towards", "toward", "paper's", "we", "authors", "author",
}


# Coarse methodology shape patterns. Each key maps to a set of substrings that,
# when present in an abstract (or methodology field when we have it), mark the
# paper as that shape. A pair of papers sharing a shape gets a
# METHODOLOGICAL_MIRROR edge (weight 0.5).
METHODOLOGY_SHAPE_PATTERNS: dict[str, tuple[str, ...]] = {
    "formative_survey": (
        "formative survey", "formative study", "survey study",
        "questionnaire study", "online survey", "n=", "n =",
        "respondents", "survey respondents",
    ),
    "design_case_study": (
        "design case", "case study", "design study", "field deployment",
        "deployed", "in-the-wild", "in the wild",
    ),
    "system_plus_evaluation": (
        "system and evaluation", "system + evaluation", "we built",
        "we designed and evaluated", "prototype and evaluation",
        "implementation and evaluation", "system implementation",
        "user evaluation", "usability evaluation",
    ),
    "qualitative_interview": (
        "qualitative interview", "semi-structured interview",
        "semistructured interview", "interview study", "focus group",
        "thematic analysis", "grounded theory",
    ),
}


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

    papers = filter_active_papers(load_json(classified_path))
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
        ensure_relationship_analysis_valid(refined)

        graph_path = os.path.join(proc_dir, "relationship_graph.json")
        alias_lookup = build_alias_lookup(papers)

        # Merge LLM-refined edges back into graph (existing v4.1 logic).
        if refined and "edges" in refined:
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

        # v4.2 Prompt D: compute extended edges (conceptual_overlap,
        # methodological_mirror, temporal_succession, contradiction) AFTER
        # the LLM extraction so heuristic edges only fill gaps the LLM left.
        contradictions_path = os.path.join(analysis_dir, "contradictions.json")
        contradictions_data = (
            load_json(contradictions_path)
            if os.path.exists(contradictions_path) else None
        )
        citation_map_path = os.path.join(proc_dir, "full_citation_map.json")
        citation_map_data = (
            load_json(citation_map_path)
            if os.path.exists(citation_map_path) else None
        )

        extended_edges = compute_extended_edges(
            classified=papers,
            contradictions=contradictions_data,
            citation_map=citation_map_data,
        )
        added_counts = _merge_extended_edges_into_graph(
            G, extended_edges, alias_lookup
        )
        log.info(
            "Phase 3.4 v4.2 extended edges added: %s (computed=%d)",
            added_counts, len(extended_edges),
        )

        # v4.2 hard requirement: back up the prior relationship_graph.json
        # BEFORE we overwrite it so we can A/B compare / roll back.
        backup_path = os.path.join(
            proc_dir, "relationship_graph_v4.1_backup.json"
        )
        if os.path.exists(graph_path) and not os.path.exists(backup_path):
            try:
                shutil.copyfile(graph_path, backup_path)
                log.info(
                    "Phase 3.4: backed up v4.1 relationship graph to %s",
                    backup_path,
                )
            except Exception as e:
                log.warning(
                    "Phase 3.4: relationship_graph backup failed: %s", e,
                )

        _save_graph(G, graph_path)
        v42_metrics = _log_extended_edge_metrics(G)
        atomic_write_json(
            os.path.join(analysis_dir, "relationship_edge_metrics_v4_2.json"),
            {
                "added_edges": added_counts,
                "computed_edges": len(extended_edges),
                **v42_metrics,
            },
        )
        state = complete_step(state, state_path, 3, "relationship_analysis")
    else:
        refined = load_json(os.path.join(analysis_dir, "relationship_analysis.json"))

    # Step 5: Gap Synthesizer agent
    if not is_step_complete(state, 3, "gap_synthesis"):
        log.info("=== Phase 3.5: Gap Synthesizer agent ===")
        gaps = _run_gap_synthesizer(client, papers, metrics, matrix, cat_stats)
        atomic_write_json(os.path.join(analysis_dir, "gaps_ranked.json"), gaps)
        ensure_gap_analysis_valid(gaps)
        state = complete_step(state, state_path, 3, "gap_synthesis")

    else:
        log.info("Gap synthesis already done")
        gaps = load_json(os.path.join(analysis_dir, "gaps_ranked.json"))
        ensure_gap_analysis_valid(gaps)

    # Quality check: this step is now beat-level evidence assessment, not
    # open-ended gap discovery.
    state["phases"]["3"]["quality_check"] = _gap_quality_check(gaps)
    save_state(state_path, state)

    summary = export_research_knowledge_base(papers, G, proc_dir, analysis_dir, output_dir)
    log.info(
        "Knowledge base exported: %s nodes, %s edges",
        summary.get("total_nodes", 0),
        summary.get("total_edges", 0),
    )

    return state


def _gap_quality_check(gaps: dict) -> dict:
    beats = gaps.get("beats", []) if isinstance(gaps, dict) else []
    return {
        "passed": isinstance(beats, list) and len(beats) == len(BEAT_REQUIREMENTS),
        "beat_statuses": dict(Counter(
            b.get("status", "unknown")
            for b in beats
            if isinstance(b, dict)
        )),
    }


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
    categories = list(CATEGORY_SEQUENCE)
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
    categories = list(CATEGORY_SEQUENCE) + ["X"]
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
# v4.2 Extended edge computation (Prompt D)
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"[a-z][a-z\-]{2,}")


def _paper_keywords(paper: dict) -> set[str]:
    """Domain-specific keyword set for a paper, with stopwords stripped.

    Pulls from title + abstract (+ any explicit concepts field). Filters against
    DOMAIN_STOPWORDS and requires length >= 4 so that very short fragments
    ("use", "web") cannot drive a CONCEPTUAL_OVERLAP match.
    """
    text_parts = [
        str(paper.get("title", "") or ""),
        str(paper.get("abstract", "") or ""),
    ]
    for concept in paper.get("concepts", []) or []:
        if isinstance(concept, dict):
            text_parts.append(str(concept.get("name", "") or ""))
        elif isinstance(concept, str):
            text_parts.append(concept)
    text = " ".join(text_parts).lower()
    tokens = {
        tok for tok in _WORD_RE.findall(text)
        if len(tok) >= 4 and tok not in DOMAIN_STOPWORDS
    }
    return tokens


def _methodology_shape(paper: dict) -> set[str]:
    """Return the set of methodology-shape labels matched by a paper.

    Uses abstract + title as the haystack. A paper can match multiple shapes
    (e.g. formative_survey AND qualitative_interview); METHODOLOGICAL_MIRROR
    fires on any shape overlap.
    """
    haystack = " ".join(
        str(paper.get(k, "") or "") for k in ("title", "abstract")
    ).lower()
    matched: set[str] = set()
    for shape, patterns in METHODOLOGY_SHAPE_PATTERNS.items():
        if any(p in haystack for p in patterns):
            matched.add(shape)
    return matched


def _keyword_in_abstract(keywords: set[str], abstract: str) -> str | None:
    """Return the first keyword from `keywords` that appears as a whole word in
    `abstract` (case-insensitive), else None. Used by TEMPORAL_SUCCESSION.
    """
    if not abstract or not keywords:
        return None
    lowered = abstract.lower()
    for kw in keywords:
        # whole-word match
        if re.search(rf"\b{re.escape(kw)}\b", lowered):
            return kw
    return None


def compute_extended_edges(
    classified: list[dict],
    contradictions: dict | list | None,
    citation_map: dict | None,
) -> list[dict]:
    """Compute v4.2 extended edges: conceptual_overlap, methodological_mirror,
    temporal_succession, and contradiction.

    Returns a list of edge dicts in the same schema the Relationship Analyst
    produces: {source, target, type, evidence, weight, provenance}. The caller
    is responsible for canonicalizing ids against the graph before insertion.

    Args:
        classified: active papers (already filter_active_papers'd).
        contradictions: parsed contradictions.json (dict with
            "contradictions" list) — used for CONTRADICTION edges.
        citation_map: reserved for future ranking; currently unused, but kept
            in the signature to match the v4.2 spec and to let future
            iterations prefer already-cited pairs.

    All edges use lowercase snake_case `type` strings and carry a
    `phase3_extended_edges_v4_2` provenance tag so they can be counted /
    rolled back independently of LLM-authored edges.
    """
    _ = citation_map  # held for future citation-aware ranking; see docstring.
    edges: list[dict] = []

    # Pre-compute per-paper features
    features: dict[str, dict] = {}
    for p in classified:
        pid = p.get("paperId")
        if not pid:
            continue
        features[pid] = {
            "paper": p,
            "keywords": _paper_keywords(p),
            "methodology": _methodology_shape(p),
            "category": p.get("primary_category", "X"),
            "year": p.get("year") or 0,
            "abstract": (p.get("abstract") or "").lower(),
        }

    pids = list(features.keys())
    n = len(pids)

    # ---- 1) CONCEPTUAL_OVERLAP (weight 0.7) ------------------------------
    # >=3 shared domain-specific keywords. Cross-category pairs preferred
    # (but same-category still emitted if they clear the threshold).
    # ---- 2) METHODOLOGICAL_MIRROR (weight 0.5) ---------------------------
    # >=1 shared methodology shape.
    # ---- 3) TEMPORAL_SUCCESSION (weight 0.6) -----------------------------
    # year diff >=3 AND one paper has a keyword from the other's abstract.
    # Emitted older -> newer.
    for i in range(n):
        pi = pids[i]
        fi = features[pi]
        for j in range(i + 1, n):
            pj = pids[j]
            fj = features[pj]

            # CONCEPTUAL_OVERLAP
            shared_kw = fi["keywords"] & fj["keywords"]
            if len(shared_kw) >= 3:
                sample_terms = sorted(shared_kw)[:5]
                cross_cat = fi["category"] != fj["category"]
                edges.append({
                    "source": pi,
                    "target": pj,
                    "type": "conceptual_overlap",
                    "weight": 0.7,
                    "evidence": (
                        f"{len(shared_kw)} shared domain keywords "
                        f"({', '.join(sample_terms)})"
                        + (" across categories "
                           f"{fi['category']}/{fj['category']}" if cross_cat
                           else " within category "
                           f"{fi['category']}")
                    ),
                    "cross_category": cross_cat,
                    "shared_keyword_count": len(shared_kw),
                    "provenance": "phase3_extended_edges_v4_2",
                    "confidence_label": "INFERRED",
                })

            # METHODOLOGICAL_MIRROR
            shared_shapes = fi["methodology"] & fj["methodology"]
            if shared_shapes:
                edges.append({
                    "source": pi,
                    "target": pj,
                    "type": "methodological_mirror",
                    "weight": 0.5,
                    "evidence": (
                        "shared methodology shape(s): "
                        + ", ".join(sorted(shared_shapes))
                    ),
                    "methodology_shapes": sorted(shared_shapes),
                    "provenance": "phase3_extended_edges_v4_2",
                    "confidence_label": "INFERRED",
                })

            # TEMPORAL_SUCCESSION
            yi, yj = fi["year"], fj["year"]
            if yi and yj and abs(yi - yj) >= 3:
                if yi <= yj:
                    older_id, newer_id = pi, pj
                    older_kw, newer_abs = fi["keywords"], fj["abstract"]
                    older_abs, newer_kw = fi["abstract"], fj["keywords"]
                    older_year, newer_year = yi, yj
                else:
                    older_id, newer_id = pj, pi
                    older_kw, newer_abs = fj["keywords"], fi["abstract"]
                    older_abs, newer_kw = fj["abstract"], fi["keywords"]
                    older_year, newer_year = yj, yi
                # one paper must carry a keyword from the other's abstract
                hit = (
                    _keyword_in_abstract(older_kw, newer_abs)
                    or _keyword_in_abstract(newer_kw, older_abs)
                )
                if hit:
                    edges.append({
                        "source": older_id,
                        "target": newer_id,
                        "type": "temporal_succession",
                        "weight": 0.6,
                        "evidence": (
                            f"{newer_year - older_year}-year gap "
                            f"({older_year} -> {newer_year}); "
                            f"shared term '{hit}'"
                        ),
                        "year_gap": newer_year - older_year,
                        "provenance": "phase3_extended_edges_v4_2",
                        "confidence_label": "INFERRED",
                    })

    # ---- 4) CONTRADICTION (weight 1.0) -----------------------------------
    # Every focus pair in contradictions.json MUST emit a CONTRADICTION edge.
    if isinstance(contradictions, dict):
        contradiction_list = contradictions.get("contradictions") or []
    elif isinstance(contradictions, list):
        contradiction_list = contradictions
    else:
        contradiction_list = []

    for c in contradiction_list:
        if not isinstance(c, dict):
            continue
        pa = c.get("paper_a") or {}
        pb = c.get("paper_b") or {}
        sa = pa.get("paperId") if isinstance(pa, dict) else None
        tb = pb.get("paperId") if isinstance(pb, dict) else None
        if not sa or not tb or sa == tb:
            continue
        edges.append({
            "source": sa,
            "target": tb,
            "type": "contradiction",
            "weight": 1.0,
            "evidence": (
                f"contradictions.json {c.get('id', '?')} "
                f"({c.get('severity', 'unknown')}): "
                f"{(c.get('question') or '')[:140]}"
            ),
            "contradiction_id": c.get("id"),
            "severity": c.get("severity"),
            "argument_line": c.get("argument_line"),
            "focus": c.get("source_question") or c.get("question"),
            "provenance": "phase3_extended_edges_v4_2",
            "confidence_label": "EXTRACTED",
        })

    return edges


def _merge_extended_edges_into_graph(
    G: nx.DiGraph,
    extended_edges: list[dict],
    alias_lookup: dict[str, str],
) -> dict[str, int]:
    """Insert extended edges into G, de-duping against existing edges of the
    same type. Returns a per-type count of edges actually added.
    """
    added: Counter = Counter()
    for edge in extended_edges:
        src = canonicalize_paper_ref(edge.get("source"), alias_lookup)
        tgt = canonicalize_paper_ref(edge.get("target"), alias_lookup)
        if not src or not tgt or not G.has_node(src) or not G.has_node(tgt):
            continue
        etype = edge.get("type", "related")
        # Skip if an edge of the same type already exists between these nodes
        # (any direction, since conceptual/methodological edges are
        # undirected in spirit).
        directional = etype in {"temporal_succession", "contradiction"}
        if directional:
            if G.has_edge(src, tgt) and G[src][tgt].get("type") == etype:
                continue
        else:
            if (G.has_edge(src, tgt) and G[src][tgt].get("type") == etype) or (
                G.has_edge(tgt, src) and G[tgt][src].get("type") == etype
            ):
                continue
        attrs = {k: v for k, v in edge.items()
                 if k not in ("source", "target")}
        attrs.setdefault("confidence_label", "INFERRED")
        attrs.setdefault("provenance", "phase3_extended_edges_v4_2")
        G.add_edge(src, tgt, **attrs)
        added[etype] += 1
    return dict(added)


def _log_extended_edge_metrics(G: nx.DiGraph) -> dict:
    """Emit the v4.2 target metrics: avg outgoing edges / paper, CONTRADICTION
    edge count, and min_edges_per_chain map. Returns the metrics dict.
    """
    n_nodes = G.number_of_nodes() or 1
    n_edges = G.number_of_edges()
    avg_out = n_edges / n_nodes

    type_counts: Counter = Counter(
        d.get("type", "unknown") for _, _, d in G.edges(data=True)
    )
    contradiction_count = type_counts.get("contradiction", 0)

    # Min-edges-per-chain target map (from paper_outline_v4.2 Part 5 table).
    # Chain index i corresponds to beat i+1.
    min_edges_per_chain = {
        1: 8, 2: 8, 3: 8, 4: 5, 5: 8, 6: 5, 7: 6,
    }

    log.info(
        "Phase 3 v4.2 edge metrics: avg_outgoing_edges/paper=%.2f "
        "(target >=4), total_edges=%d, contradiction_edges=%d "
        "(target >=15), edge_type_counts=%s",
        avg_out, n_edges, contradiction_count, dict(type_counts),
    )
    log.info(
        "Phase 3 v4.2 min_edges_per_chain targets: %s (sum=%d, overall "
        "edge target >=80 per outline Part 5)",
        min_edges_per_chain, sum(min_edges_per_chain.values()),
    )
    return {
        "avg_outgoing_edges_per_paper": round(avg_out, 3),
        "total_edges": n_edges,
        "contradiction_edge_count": contradiction_count,
        "edge_type_counts": dict(type_counts),
        "min_edges_per_chain": min_edges_per_chain,
    }


# ---------------------------------------------------------------------------
# Agent calls
# ---------------------------------------------------------------------------

def _run_relationship_analyst(client, papers: list[dict], G: nx.DiGraph) -> dict:
    """Send top papers to Relationship Analyst for edge refinement."""
    # Keep the prompt compact enough for stable reasoning responses.
    top_papers = sorted(papers, key=lambda p: p.get("citationCount", 0), reverse=True)[:25]
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
            max_tokens=8192,
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
        raw = agent_run(
            client,
            role=GAP_SYNTHESIZER,
            model=BRAIN_PHASE3_GAP,
            task=summary,
            max_tokens=8192,
        )
        result = _parse_json_object(raw)
        ensure_gap_analysis_valid(result)
        result = _reconcile_gap_assessment(result, papers)
        _log_gap_synthesizer_summary(result)
        return result
    except Exception as first_error:
        log.warning(f"Gap Synthesizer retrying with compact context: {first_error}")
        retry_role = (
            GAP_SYNTHESIZER
            + "\nReturn minified JSON only. No prose, no markdown, no trailing commentary. "
              "The JSON must contain exactly 7 beats plus a non-empty overall_assessment."
        )
        retry_task = _build_compact_gap_synthesis_input(metrics, matrix, cat_stats)
        try:
            raw = agent_run(
                client,
                role=retry_role,
                model=BRAIN_PHASE3_GAP,
                task=retry_task,
                max_tokens=4096,
            )
            result = _parse_json_object(raw)
            ensure_gap_analysis_valid(result)
            result = _reconcile_gap_assessment(result, papers)
            log.info("Gap Synthesizer generated valid JSON after compact retry")
            _log_gap_synthesizer_summary(result)
            return result
        except Exception as second_error:
            log.error(f"Gap Synthesizer failed after retry: {second_error}")
            return _fallback_gap_synthesis(papers, metrics, matrix, cat_stats, second_error)


def _log_gap_synthesizer_summary(result: dict):
    if isinstance(result, dict) and isinstance(result.get("beats"), list):
        statuses = Counter(
            b.get("status", "unknown")
            for b in result["beats"]
            if isinstance(b, dict)
        )
        log.info(
            "Gap Synthesizer produced %s beat assessments: %s",
            len(result["beats"]),
            dict(statuses),
        )
    else:
        gap_count = len(result.get("gaps", [])) if isinstance(result, dict) else 0
        log.info(f"Gap Synthesizer identified {gap_count} research gaps")


def _build_compact_gap_synthesis_input(metrics: dict, matrix: dict, cat_stats: dict) -> str:
    cat_summary = {
        cat: {
            "count": stats.get("count", 0),
            "median_year": stats.get("median_year", 0),
            "median_citations": stats.get("median_citations", 0),
        }
        for cat, stats in sorted(cat_stats.items())
        if cat != "X" and stats.get("count", 0) > 0
    }
    sparse_pairs = {
        pair: {
            "edge_count": data.get("edge_count", 0),
            "bridging_papers": data.get("bridging_papers", 0),
        }
        for pair, data in sorted(matrix.items())
        if data.get("edge_count", 0) <= 1 or data.get("bridging_papers", 0) <= 1
    }
    beat_requirements = {
        beat: {
            "name": info["name"],
            "categories": info["categories"],
            "pairs": info["pairs"],
            "required_papers": [item["label"] for item in info.get("required_papers", [])],
        }
        for beat, info in BEAT_REQUIREMENTS.items()
    }
    return (
        "Assess evidence sufficiency for exactly 7 beats.\n"
        f"Beat requirements: {json.dumps(beat_requirements, ensure_ascii=False)}\n"
        f"Category counts: {json.dumps(cat_summary, ensure_ascii=False)}\n"
        f"Sparse category pairs: {json.dumps(sparse_pairs, ensure_ascii=False)[:1800]}\n"
        f"Graph summary: nodes={metrics.get('total_nodes', 0)}, edges={metrics.get('total_edges', 0)}, "
        f"components={metrics.get('num_components', 0)}, isolated={metrics.get('isolated_count', 0)}\n"
        "Return a conservative beat-by-beat assessment with explicit weaknesses and missing-paper suggestions."
    )


def _fallback_gap_synthesis(papers: list[dict], metrics: dict, matrix: dict, cat_stats: dict, error: Exception) -> dict:
    category_counts = {
        cat: stats.get("count", 0)
        for cat, stats in cat_stats.items()
        if cat != "X"
    }
    required_presence = _compute_required_paper_presence(papers)
    beats = []
    weakest = []
    for beat, info in BEAT_REQUIREMENTS.items():
        counts = {cat: category_counts.get(cat, 0) for cat in info["categories"]}
        total = sum(counts.values())
        sparse_pairs = [
            pair for pair in info["pairs"]
            if matrix.get(pair, {}).get("edge_count", 0) <= 1
            and matrix.get(pair, {}).get("bridging_papers", 0) <= 1
        ]
        weak_categories = [cat for cat, count in counts.items() if count < 8]

        if any(count == 0 for count in counts.values()) or total < 8:
            status = "critical_gap"
        elif total < 14 or len(weak_categories) >= 2:
            status = "weak"
        elif sparse_pairs or weak_categories:
            status = "adequate"
        else:
            status = "strong"

        if status in {"critical_gap", "weak"}:
            weakest.append(f"Beat {beat} ({info['name']})")

        weakness_parts = []
        if weak_categories:
            weakness_parts.append(
                "thin categories: " + ", ".join(f"{cat}={counts[cat]}" for cat in weak_categories)
            )
        if sparse_pairs:
            weakness_parts.append("broken bridges: " + ", ".join(sparse_pairs))
        if not weakness_parts:
            weakness_parts.append("no major structural weakness detected in fallback heuristic")

        present_labels = [
            item["label"]
            for item in required_presence.get(beat, {}).get("present", [])
        ]
        missing_labels = [
            item["label"]
            for item in required_presence.get(beat, {}).get("missing", [])
        ]
        fallback_missing = list(missing_labels)
        for title in info["missing_titles"]:
            if len(fallback_missing) >= 2:
                break
            if title not in fallback_missing:
                fallback_missing.append(title)

        beats.append({
            "beat": beat,
            "name": info["name"],
            "status": status,
            "supporting_papers": total,
            "key_papers_present": (
                present_labels
                + [f"{cat}={counts[cat]}" for cat in info["categories"] if counts[cat] > 0]
            ),
            "key_papers_missing": fallback_missing[:2] if status != "strong" else [],
            "weakness": "; ".join(weakness_parts),
            "evidence_chain": [
                f"Category support counts: {', '.join(f'{cat}={counts[cat]}' for cat in info['categories'])}",
                (
                    "Sparse cross-category links: " + ", ".join(sparse_pairs)
                    if sparse_pairs
                    else "Cross-category links are not the main blocker in fallback analysis"
                ),
                "Fallback heuristic generated this assessment because model JSON could not be validated",
            ],
        })

    overall = (
        "Fallback gap synthesis generated from category counts and graph sparsity because the "
        f"model response could not be validated ({error}). "
        + (
            "The weakest beats remain " + ", ".join(weakest) + "."
            if weakest else
            "No beat looks structurally broken under the heuristic, but a successful model rerun is still preferred."
        )
    )
    missing = []
    for beat, info in BEAT_REQUIREMENTS.items():
        if len(missing) >= 3:
            break
        counts = [category_counts.get(cat, 0) for cat in info["categories"]]
        required_missing = required_presence.get(beat, {}).get("missing", [])
        if any(count < 8 for count in counts):
            missing.append({
                "title": (
                    required_missing[0]["label"]
                    if required_missing else
                    info["missing_titles"][0]
                ),
                "why_needed": f"Beat {beat} lacks dense coverage in categories {', '.join(info['categories'])}.",
                "search_suggestion": f"targeted search for {' / '.join(info['categories'])} anchors supporting Beat {beat}",
            })

    return {
        "beats": beats,
        "overall_assessment": overall,
        "missing_papers": missing,
        "strongest_narrative_thread": [],
        "field_observations": {
            "fallback_warning": f"Gap synthesis retry failed: {error}",
            "graph_components": metrics.get("num_components", 0),
            "isolated_nodes": metrics.get("isolated_count", 0),
        },
    }


def _parse_json_object(raw: str) -> dict:
    text = raw.strip()
    match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    first_brace = min(
        [idx for idx in (text.find("{"), text.find("[")) if idx != -1],
        default=-1,
    )
    if first_brace != -1:
        text = text[first_brace:]

    candidates = []
    for candidate in (text, _extract_balanced_json(text), _trim_to_last_json_closer(text)):
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    last_error = None
    for candidate in candidates:
        for repaired in (candidate, _close_unbalanced_json(candidate)):
            if not repaired:
                continue
            try:
                parsed = json.loads(repaired)
                if isinstance(parsed, dict):
                    return parsed
            except Exception as e:
                last_error = e

    raise last_error or ValueError("Model output did not contain a valid JSON object")


def _extract_balanced_json(text: str) -> str:
    if not text:
        return ""
    start = next((i for i, ch in enumerate(text) if ch in "[{"), -1)
    if start == -1:
        return ""

    stack = []
    in_string = False
    escape = False
    for i, ch in enumerate(text[start:], start):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch in "[{":
            stack.append("]" if ch == "[" else "}")
        elif ch in "]}":
            if not stack or ch != stack[-1]:
                return ""
            stack.pop()
            if not stack:
                return text[start:i + 1]
    return ""


def _trim_to_last_json_closer(text: str) -> str:
    last = max(text.rfind("}"), text.rfind("]"))
    return text[:last + 1] if last != -1 else ""


def _close_unbalanced_json(text: str) -> str:
    if not text:
        return ""

    stack = []
    in_string = False
    escape = False
    for ch in text:
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch in "[{":
            stack.append("]" if ch == "[" else "}")
        elif ch in "]}":
            if stack and ch == stack[-1]:
                stack.pop()

    repaired = text
    if in_string:
        repaired += '"'
    if stack:
        repaired += "".join(reversed(stack))
    return repaired


def _format_papers_for_analyst(papers: list[dict]) -> str:
    """Format papers for the Relationship Analyst."""
    lines = []
    for p in papers:
        lines.append(
            f"paperId: {p['paperId']}\n"
            f"title: {p.get('title', 'N/A')}\n"
            f"category: {p.get('primary_category', 'X')}\n"
            f"year: {p.get('year', 'N/A')}\n"
            f"abstract: {(p.get('abstract') or '')[:180]}\n"
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

    present_required = _compute_required_paper_presence(papers)
    required_summary = {
        str(beat): {
            "present": [item["label"] for item in presence["present"]],
            "missing": [item["label"] for item in presence["missing"]],
        }
        for beat, presence in present_required.items()
        if presence["present"] or presence["missing"]
    }

    return (
        f"Assess evidence sufficiency for a 7-beat research paper using this corpus of {len(papers)} papers.\n\n"
        f"## Foundational Papers (highest in-degree)\n{found_str}\n\n"
        f"## Category Intersection Matrix\n{matrix_str}\n\n"
        f"## Category Statistics\n{cat_str}\n\n"
        f"## Required Paper Presence\n{json.dumps(required_summary, ensure_ascii=False, indent=2)}\n\n"
        f"## Per-Category Gaps (what papers leave unaddressed)\n{gaps_str}\n\n"
        f"## Graph Summary\n"
        f"  Nodes: {metrics.get('total_nodes', 0)}, Edges: {metrics.get('total_edges', 0)}\n"
        f"  Components: {metrics.get('num_components', 0)}, Isolated: {metrics.get('isolated_count', 0)}\n"
        f"  Edge types: {metrics.get('edge_type_counts', {})}\n\n"
        f"Assess each beat's evidence strength. Identify missing key papers and the strongest narrative thread."
    )


def _normalize_text_match(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def _paper_matches_requirement(paper: dict, requirement: dict) -> bool:
    if not isinstance(paper, dict) or not isinstance(requirement, dict):
        return False

    required_id = (requirement.get("paperId") or "").strip().lower()
    if required_id:
        aliases = {
            str(alias).strip().lower()
            for alias in (
                [paper.get("paperId"), paper.get("canonical_id"), *(paper.get("alias_ids") or [])]
            )
            if alias
        }
        if required_id in aliases:
            return True

    title_norm = _normalize_text_match(paper.get("title", ""))
    for raw_substring in requirement.get("match_substrings", []) or []:
        needle = _normalize_text_match(raw_substring)
        if needle and needle in title_norm:
            return True

    label = _normalize_text_match(requirement.get("label", ""))
    return bool(label and label in title_norm)


def _compute_required_paper_presence(papers: list[dict]) -> dict[int, dict[str, list[dict]]]:
    presence = {}
    for beat, info in BEAT_REQUIREMENTS.items():
        present = []
        missing = []
        for requirement in info.get("required_papers", []) or []:
            if any(_paper_matches_requirement(paper, requirement) for paper in papers):
                present.append(requirement)
            else:
                missing.append(requirement)
        presence[beat] = {"present": present, "missing": missing}
    return presence


def _reconcile_gap_assessment(result: dict, papers: list[dict]) -> dict:
    if not isinstance(result, dict):
        return result

    presence = _compute_required_paper_presence(papers)
    beats = result.get("beats")
    if not isinstance(beats, list):
        return result

    for beat_entry in beats:
        if not isinstance(beat_entry, dict):
            continue
        beat_num = beat_entry.get("beat")
        if beat_num not in presence:
            continue

        present_labels = [item["label"] for item in presence[beat_num]["present"]]
        missing_labels = [item["label"] for item in presence[beat_num]["missing"]]

        present_existing = [
            label for label in (beat_entry.get("key_papers_present") or [])
            if label not in present_labels
        ]
        missing_existing = [
            label for label in (beat_entry.get("key_papers_missing") or [])
            if label not in present_labels and label not in missing_labels
        ]

        beat_entry["key_papers_present"] = present_labels + present_existing
        beat_entry["key_papers_missing"] = missing_labels + missing_existing

    if isinstance(result.get("missing_papers"), list):
        filtered_missing = []
        present_labels = {
            req["label"]
            for beat_presence in presence.values()
            for req in beat_presence["present"]
        }
        for item in result["missing_papers"]:
            if not isinstance(item, dict):
                continue
            if item.get("title") in present_labels:
                continue
            filtered_missing.append(item)
        result["missing_papers"] = filtered_missing

    return result


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
