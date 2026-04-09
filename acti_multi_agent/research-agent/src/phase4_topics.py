"""Phase 4: Evidence Inventory & Final Report Generation."""

from __future__ import annotations

import json
import logging
import os

from .api_client import agent_run_json, BRAIN_PHASE4_EVIDENCE, S2Client
from .prompts import TOPIC_SCORER
from .state_manager import complete_step, is_step_complete
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")


def run_phase4(state: dict, state_path: str, base_dir: str, client,
               s2: S2Client | None = None) -> dict:
    """Orchestrate Phase 4: evidence inventory + final report."""
    analysis_dir = os.path.join(base_dir, "analysis")
    output_dir = os.path.join(base_dir, "output")
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)

    evidence_path = os.path.join(analysis_dir, "gaps_ranked.json")
    classified_path = os.path.join(proc_dir, "classified.json")

    if not os.path.exists(evidence_path):
        log.error("gaps_ranked.json not found. Run Phase 3 first.")
        return state

    evidence = load_json(evidence_path)
    classified = load_json(classified_path) if os.path.exists(classified_path) else []

    # Step 1: Generate evidence inventory per beat
    if not is_step_complete(state, 4, "score_gaps"):
        log.info("=== Phase 4.1: Evidence inventory ===")
        inventory = _build_evidence_inventory(client, evidence, classified)
        atomic_write_json(os.path.join(analysis_dir, "evidence_inventory.json"), inventory)
        state = complete_step(state, state_path, 4, "score_gaps")
    else:
        inventory = load_json(os.path.join(analysis_dir, "evidence_inventory.json"))

    # Step 2: Skip advisor alignment (not relevant for evidence chain)
    if not is_step_complete(state, 4, "advisor_alignment"):
        log.info("=== Phase 4.2: Skipped (not applicable) ===")
        state = complete_step(state, state_path, 4, "advisor_alignment")

    # Step 3: Skip thesis generation (thesis is predetermined)
    if not is_step_complete(state, 4, "thesis_generation"):
        log.info("=== Phase 4.3: Skipped (thesis predetermined) ===")
        state = complete_step(state, state_path, 4, "thesis_generation")

    # Step 4: Final report
    if not is_step_complete(state, 4, "final_report"):
        log.info("=== Phase 4.4: Generate final reports ===")
        _generate_evidence_report(evidence, inventory, classified, output_dir)
        state = complete_step(state, state_path, 4, "final_report")

    return state


def _build_evidence_inventory(client, evidence: dict, classified: list[dict]) -> dict:
    """Use TOPIC_SCORER agent to generate structured evidence inventory per beat."""
    beats = evidence.get("beats", [])
    beats_summary = json.dumps(beats, indent=2, ensure_ascii=False)[:3000] if beats else "No beat analysis available"

    # Build per-category paper lists for the agent
    by_cat = {}
    for p in classified:
        cat = p.get("primary_category", "X")
        if cat == "X":
            continue
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append({
            "paperId": p.get("paperId", ""),
            "title": p.get("title", "")[:80],
            "year": p.get("year", 0),
            "citationCount": p.get("citationCount", 0),
            "one_sentence_contribution": p.get("one_sentence_contribution", "")[:100],
        })

    # Sort each category by citations, take top 10
    cat_summaries = {}
    for cat, papers in by_cat.items():
        papers.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
        cat_summaries[cat] = papers[:10]

    task = (
        f"Generate a structured evidence inventory for a 5-beat research paper.\n\n"
        f"## Evidence Sufficiency Analysis\n{beats_summary}\n\n"
        f"## Top Papers by Category\n{json.dumps(cat_summaries, indent=2, ensure_ascii=False)[:4000]}\n\n"
        f"For each beat, identify the 5-8 most important papers and the logical chain connecting them."
    )

    try:
        result = agent_run_json(client, role=TOPIC_SCORER, task=task, model=BRAIN_PHASE4_EVIDENCE, max_tokens=4096)
        log.info(f"Evidence inventory generated")
        return result
    except Exception as e:
        log.error(f"Evidence inventory failed: {e}")
        return {"evidence_inventory": [], "error": str(e)}


def _generate_evidence_report(evidence: dict, inventory: dict,
                               classified: list[dict], output_dir: str):
    """Write human-readable evidence reports."""

    # --- Report 1: Evidence Sufficiency ---
    lines = ["# Evidence Sufficiency Report\n"]
    lines.append("*Assessment of literature support for each beat of the paper*\n\n---\n")

    beats = evidence.get("beats", [])
    for b in beats:
        status_icon = {"strong": "🟢", "adequate": "🟡", "weak": "🟠", "critical_gap": "🔴"}.get(
            b.get("status", ""), "❓")
        lines.append(f"## Beat {b.get('beat', '?')}: {b.get('name', '')} {status_icon} {b.get('status', '')}\n")
        lines.append(f"Supporting papers: {b.get('supporting_papers', '?')}")
        if b.get("key_papers_present"):
            lines.append(f"Key papers present: {', '.join(b['key_papers_present'])}")
        if b.get("key_papers_missing"):
            lines.append(f"Key papers MISSING: {', '.join(b['key_papers_missing'])}")
        if b.get("weakness"):
            lines.append(f"Weakness: {b['weakness']}")
        if b.get("evidence_chain"):
            lines.append(f"\nEvidence chain:")
            for step in b["evidence_chain"]:
                lines.append(f"  → {step}")
        lines.append("\n---\n")

    overall = evidence.get("overall_assessment", "")
    if overall:
        lines.append(f"## Overall Assessment\n{overall}\n")

    missing = evidence.get("missing_papers", [])
    if missing:
        lines.append("## Missing Papers (search suggestions)\n")
        for m in missing:
            lines.append(f"- **{m.get('title', '?')}**: {m.get('why_needed', '')}")
            if m.get("search_suggestion"):
                lines.append(f"  Search: `{m['search_suggestion']}`")
        lines.append("")

    thread = evidence.get("strongest_narrative_thread", [])
    if thread:
        lines.append(f"## Strongest Narrative Thread\n{' → '.join(thread)}\n")

    report_path = os.path.join(output_dir, "evidence_sufficiency.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.info(f"Evidence sufficiency report: {report_path}")

    # --- Report 2: Evidence Inventory ---
    inv_lines = ["# Evidence Inventory by Beat\n"]
    inv_items = inventory.get("evidence_inventory", [])
    for item in inv_items:
        inv_lines.append(f"## Beat {item.get('beat', '?')}: {item.get('title', '')}\n")
        if item.get("narrative"):
            inv_lines.append(f"{item['narrative']}\n")
        for p in item.get("core_papers", []):
            inv_lines.append(f"- **{p.get('citation_note', p.get('title', '?'))}**")
            inv_lines.append(f"  Role: {p.get('role', '')}")
            inv_lines.append(f"  Finding: {p.get('key_finding', '')}")
        if item.get("remaining_gaps"):
            inv_lines.append(f"\nRemaining gaps:")
            for g in item["remaining_gaps"]:
                inv_lines.append(f"  ⚠ {g}")
        inv_lines.append("\n---\n")

    outline = inventory.get("suggested_paper_outline", {})
    if outline:
        inv_lines.append("## Suggested Paper Structure\n")
        for section, info in outline.items():
            inv_lines.append(f"- {section}: ~{info.get('papers', '?')} papers, {info.get('pages', '?')} pages")

    inv_path = os.path.join(output_dir, "evidence_inventory.md")
    with open(inv_path, "w", encoding="utf-8") as f:
        f.write("\n".join(inv_lines))
    log.info(f"Evidence inventory: {inv_path}")

    # --- Report 3: Category summary (quick reference) ---
    cat_lines = ["# Paper Corpus by Category\n"]
    by_cat = {}
    for p in classified:
        cat = p.get("primary_category", "X")
        if cat == "X":
            continue
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(p)

    cat_names = {
        "A": "Model Collapse Theory", "B": "Web Data Pollution & Scale",
        "C": "Detection & Reactive Limits", "D": "Information Theory + Text Quality",
        "E": "Data Quality & Curation", "F": "Human Data Value & RLHF",
        "G": "Platform & Provenance Design", "H": "Temporal Web Quality Measurement",
        "I": "Social Reasoning Benchmarks", "J": "Fine-tune Data Composition Ablation",
    }
    for cat in sorted(by_cat):
        papers = sorted(by_cat[cat], key=lambda x: x.get("citationCount", 0), reverse=True)
        cat_lines.append(f"## {cat}: {cat_names.get(cat, '')} ({len(papers)} papers)\n")
        for p in papers[:15]:
            cat_lines.append(
                f"- [{p.get('year', '?')}] {p.get('title', '?')[:80]} "
                f"(cites={p.get('citationCount', 0)})"
            )
            if p.get("one_sentence_contribution"):
                cat_lines.append(f"  → {p['one_sentence_contribution'][:100]}")
        if len(papers) > 15:
            cat_lines.append(f"  ... and {len(papers) - 15} more")
        cat_lines.append("")

    cat_path = os.path.join(output_dir, "corpus_by_category.md")
    with open(cat_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cat_lines))
    log.info(f"Corpus by category: {cat_path}")
