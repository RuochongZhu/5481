"""Phase 3.5: Narrative Chain Construction — per-beat writing-ready paper ordering."""

import json
import logging
import os

from .api_client import agent_run_json, MODEL_DEEP, S2Client, S2_FIELDS
from .prompts import NARRATIVE_ANALYST
from .state_manager import complete_step, is_step_complete, save_state
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")

# Beat → category mapping
BEAT_CATEGORIES = {
    1: ["A", "B", "C"],
    2: ["D", "H"],
    3: ["D"],
    4: ["E", "F", "I", "J"],
    5: ["A", "G"],
}

BEAT_NAMES = {
    1: "Crisis Exists",
    2: "Empirical Degradation",
    3: "Theoretical Framework",
    4: "Validation Experiment",
    5: "Platform Solution",
}


def run_phase3_5(state: dict, state_path: str, base_dir: str, client,
                 s2: S2Client | None = None) -> dict:
    """Orchestrate Phase 3.5: narrative chain construction per beat."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    analysis_dir = os.path.join(base_dir, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    classified_path = os.path.join(proc_dir, "classified.json")
    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return state

    classified = load_json(classified_path)
    log.info(f"Phase 3.5: building narrative chains for {len(classified)} papers")

    # Step 1: Expand citation graph (full pairwise references)
    if not is_step_complete(state, "3.5", "citation_expansion"):
        log.info("=== Phase 3.5.1: Full citation expansion ===")
        citation_map = _expand_full_citations(classified, s2, proc_dir)
        state = complete_step(state, state_path, "3.5", "citation_expansion", {
            "papers_expanded": len(citation_map),
        })
    else:
        cite_path = os.path.join(proc_dir, "full_citation_map.json")
        citation_map = load_json(cite_path) if os.path.exists(cite_path) else {}
        log.info(f"Citation map loaded: {len(citation_map)} papers")

    # Step 2: Build narrative chains per beat
    if not is_step_complete(state, "3.5", "narrative_chains"):
        log.info("=== Phase 3.5.2: Narrative chain construction ===")
        chains = _build_narrative_chains(client, classified, citation_map)
        atomic_write_json(os.path.join(analysis_dir, "narrative_chains.json"), chains)
        state = complete_step(state, state_path, "3.5", "narrative_chains", {
            "beats_processed": len(chains),
        })
    else:
        chains = load_json(os.path.join(analysis_dir, "narrative_chains.json"))

    # Step 3: Generate writing-ready outline
    if not is_step_complete(state, "3.5", "writing_outline"):
        log.info("=== Phase 3.5.3: Writing outline generation ===")
        _generate_writing_outline(chains, classified, os.path.join(base_dir, "output"))
        state = complete_step(state, state_path, "3.5", "writing_outline")

    return state


def _expand_full_citations(classified: list[dict], s2: S2Client | None,
                           proc_dir: str) -> dict:
    """For each paper in corpus, fetch its references list from S2.

    This builds a full directed citation graph: paper → [papers it cites].
    Only tracks citations within our corpus (internal edges).
    """
    cite_path = os.path.join(proc_dir, "full_citation_map.json")

    # Load existing progress
    if os.path.exists(cite_path):
        citation_map = load_json(cite_path)
    else:
        citation_map = {}

    if s2 is None:
        log.warning("No S2 client — skipping citation expansion, using existing edges only")
        return citation_map

    # Build set of all paper IDs in corpus for filtering
    corpus_ids = {p["paperId"] for p in classified}

    # Only expand papers we haven't done yet
    to_expand = [p for p in classified
                 if p["paperId"] not in citation_map
                 and not p["paperId"].startswith("arxiv:")  # arXiv IDs need resolution
                 and p["paperId"]]

    log.info(f"Expanding citations for {len(to_expand)} papers ({len(citation_map)} already done)")

    for i, p in enumerate(to_expand):
        pid = p["paperId"]
        try:
            refs = s2.get_references(pid, limit=200, fields="paperId")
            ref_ids = [r.get("paperId", "") for r in refs if r.get("paperId")]
            # Only keep references that are in our corpus
            internal_refs = [rid for rid in ref_ids if rid in corpus_ids]
            citation_map[pid] = internal_refs
            if (i + 1) % 20 == 0:
                log.info(f"  Expanded {i+1}/{len(to_expand)} papers")
                atomic_write_json(cite_path, citation_map)
        except Exception as e:
            log.warning(f"  Failed to expand {pid}: {e}")
            citation_map[pid] = []

    atomic_write_json(cite_path, citation_map)
    total_edges = sum(len(v) for v in citation_map.values())
    log.info(f"Full citation map: {len(citation_map)} papers, {total_edges} internal edges")
    return citation_map


def _build_narrative_chains(client, classified: list[dict],
                            citation_map: dict) -> list[dict]:
    """For each beat, use NARRATIVE_ANALYST to construct the narrative chain."""
    chains = []

    for beat_num, categories in BEAT_CATEGORIES.items():
        beat_name = BEAT_NAMES[beat_num]
        log.info(f"  Beat {beat_num} ({beat_name}): categories {categories}")

        # Collect papers for this beat
        beat_papers = [
            p for p in classified
            if p.get("primary_category") in categories
            or any(c in categories for c in p.get("secondary_categories", []))
        ]

        if not beat_papers:
            log.warning(f"  No papers for Beat {beat_num}, skipping")
            chains.append({"beat": beat_num, "beat_name": beat_name,
                           "error": "no_papers", "spine": [], "supporting": []})
            continue

        # Build citation subgraph for these papers
        beat_ids = {p["paperId"] for p in beat_papers}
        citation_edges = []
        for p in beat_papers:
            pid = p["paperId"]
            refs = citation_map.get(pid, [])
            for ref_id in refs:
                if ref_id in beat_ids:
                    citation_edges.append({"from": pid, "to": ref_id})

        # Format input for agent
        papers_input = _format_beat_papers(beat_papers, citation_edges)

        try:
            result = agent_run_json(
                client,
                role=NARRATIVE_ANALYST,
                model=MODEL_DEEP,
                task=(
                    f"Construct the narrative chain for Beat {beat_num}: {beat_name}.\n\n"
                    f"This beat covers categories {categories} and has {len(beat_papers)} papers.\n\n"
                    f"{papers_input}"
                ),
                max_tokens=4096,
            )
            result["beat"] = beat_num
            result["beat_name"] = beat_name
            result["paper_count"] = len(beat_papers)
            chains.append(result)
            spine_len = len(result.get("spine", []))
            log.info(f"  Beat {beat_num}: spine={spine_len} papers, "
                     f"supporting={len(result.get('supporting', []))} papers")
        except Exception as e:
            log.error(f"  Beat {beat_num} narrative failed: {e}")
            chains.append({"beat": beat_num, "beat_name": beat_name,
                           "error": str(e), "spine": [], "supporting": []})

    return chains


def _format_beat_papers(papers: list[dict], citation_edges: list[dict]) -> str:
    """Format papers and citation edges for the NARRATIVE_ANALYST."""
    lines = ["## Papers\n"]
    for p in sorted(papers, key=lambda x: x.get("year", 0)):
        lines.append(
            f"paperId: {p['paperId']}\n"
            f"title: {p.get('title', 'N/A')}\n"
            f"year: {p.get('year', 'N/A')}\n"
            f"category: {p.get('primary_category', 'X')}\n"
            f"key_claim: {p.get('key_claim', p.get('one_sentence_contribution', 'N/A'))}\n"
            f"method_type: {p.get('method_type', 'N/A')}\n"
            f"citations: {p.get('citationCount', 0)}\n"
            f"---"
        )

    if citation_edges:
        lines.append(f"\n## Citation Edges ({len(citation_edges)} internal edges)\n")
        for e in citation_edges[:100]:  # Cap at 100 edges
            lines.append(f"{e['from']} → {e['to']}")

    return "\n".join(lines)


def _generate_writing_outline(chains: list[dict], classified: list[dict],
                               output_dir: str):
    """Generate a human-readable writing outline from narrative chains."""
    os.makedirs(output_dir, exist_ok=True)
    by_id = {p["paperId"]: p for p in classified}

    lines = ["# Related Work Writing Outline\n"]
    lines.append("*Auto-generated narrative structure for each beat*\n\n---\n")

    for chain in chains:
        beat = chain.get("beat", "?")
        name = chain.get("beat_name", "")
        lines.append(f"## Beat {beat}: {name}\n")

        if chain.get("error"):
            lines.append(f"⚠ Error: {chain['error']}\n\n---\n")
            continue

        # Anchor paper
        anchor = chain.get("anchor_paper", {})
        if anchor:
            pid = anchor.get("paperId", "")
            p = by_id.get(pid, {})
            lines.append(f"**Anchor paper**: {p.get('title', pid)}")
            lines.append(f"  Why: {anchor.get('why', 'N/A')}\n")

        # Spine
        spine = chain.get("spine", [])
        if spine:
            lines.append(f"**Narrative spine** ({len(spine)} papers):\n")
            for s in spine:
                pid = s.get("paperId", "")
                p = by_id.get(pid, {})
                title = p.get("title", pid)[:70]
                lines.append(f"  {s.get('position', '?')}. [{p.get('year', '?')}] {title}")
                lines.append(f"     Role: {s.get('role_in_narrative', 'N/A')}")
                if s.get("transition_to_next"):
                    lines.append(f"     → {s['transition_to_next']}")
            lines.append("")

        # Paragraph outline
        paras = chain.get("paragraph_outline", [])
        if paras:
            lines.append("**Paragraph structure**:\n")
            for para in paras:
                lines.append(f"  ¶{para.get('paragraph', '?')}: {para.get('topic', '')}")
                if para.get("opening_sentence"):
                    lines.append(f"    Opening: \"{para['opening_sentence']}\"")
                paper_ids = para.get("papers", [])
                for pid in paper_ids:
                    p = by_id.get(pid, {})
                    lines.append(f"    - {p.get('title', pid)[:60]} ({p.get('year', '?')})")
            lines.append("")

        # Writing notes
        notes = chain.get("writing_notes", "")
        if notes:
            lines.append(f"**Writing notes**: {notes}\n")

        lines.append("---\n")

    outline_path = os.path.join(output_dir, "writing_outline.md")
    with open(outline_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.info(f"Writing outline: {outline_path}")
