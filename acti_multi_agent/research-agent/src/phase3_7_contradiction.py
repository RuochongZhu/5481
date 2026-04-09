"""Phase 3.7: Contradiction Map — identify disagreements between papers."""

from __future__ import annotations

import json
import logging
import os

from .api_client import agent_run_json, BRAIN_PHASE3_CONTRADICTION
from .prompts import CONTRADICTION_MAPPER
from .state_manager import complete_step, is_step_complete
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")

# Categories that are most likely to contain contradictions relevant to our thesis
CONTRADICTION_FOCUS_PAIRS = [
    (["A", "E"], "Can synthetic data replace human data? (collapse vs curation)"),
    (["B", "C"], "Is web pollution detectable? (pollution scale vs detection limits)"),
    (["D", "H"], "Is web quality actually declining? (metrics vs temporal measurement)"),
    (["E", "F"], "Human data vs curated synthetic? (curation vs RLHF)"),
    (["I", "J"], "Does data composition matter for social reasoning? (benchmarks vs ablation)"),
]


def run_phase3_7(state: dict, state_path: str, base_dir: str, client) -> dict:
    """Orchestrate Phase 3.7: contradiction mapping."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    analysis_dir = os.path.join(base_dir, "analysis")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(analysis_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    classified_path = os.path.join(proc_dir, "classified.json")
    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return state

    classified = load_json(classified_path)
    log.info(f"Phase 3.7: contradiction mapping for {len(classified)} papers")

    # Step 1: Identify contradictions per focus pair
    if not is_step_complete(state, "3.7", "contradiction_scan"):
        log.info("=== Phase 3.7.1: Contradiction scanning ===")
        contradictions = _scan_contradictions(client, classified)
        atomic_write_json(os.path.join(analysis_dir, "contradictions.json"), contradictions)
        state = complete_step(state, state_path, "3.7", "contradiction_scan", {
            "contradictions_found": len(contradictions.get("contradictions", [])),
        })
    else:
        contradictions = load_json(os.path.join(analysis_dir, "contradictions.json"))

    # Step 2: Generate contradiction report
    if not is_step_complete(state, "3.7", "contradiction_report"):
        log.info("=== Phase 3.7.2: Contradiction report ===")
        _generate_contradiction_report(contradictions, classified, output_dir)
        state = complete_step(state, state_path, "3.7", "contradiction_report")

    return state


def _scan_contradictions(client, classified: list[dict]) -> dict:
    """Use CONTRADICTION_MAPPER agent to find disagreements."""
    all_contradictions = []
    thesis_risks = []

    for categories, question in CONTRADICTION_FOCUS_PAIRS:
        log.info(f"  Scanning categories {categories}: {question}")

        # Collect papers from these categories
        papers = [
            p for p in classified
            if p.get("primary_category") in categories
            or any(c in categories for c in p.get("secondary_categories", []))
        ]

        if len(papers) < 2:
            log.info(f"  Only {len(papers)} papers, skipping")
            continue

        # Sort by citations, take top 30 for analysis
        papers.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
        papers = papers[:30]

        papers_input = _format_papers_for_contradiction(papers)

        try:
            result = agent_run_json(
                client,
                role=CONTRADICTION_MAPPER,
                model=BRAIN_PHASE3_CONTRADICTION,
                task=(
                    f"Identify contradictions among these {len(papers)} papers.\n"
                    f"Focus question: {question}\n"
                    f"Categories: {categories}\n\n"
                    f"{papers_input}"
                ),
                max_tokens=4096,
            )
            if isinstance(result, dict):
                for c in result.get("contradictions", []):
                    c["source_categories"] = categories
                    c["source_question"] = question
                    all_contradictions.append(c)
                if result.get("thesis_risk_assessment"):
                    thesis_risks.append(result["thesis_risk_assessment"])
                log.info(f"  Found {len(result.get('contradictions', []))} contradictions")
        except Exception as e:
            log.error(f"  Contradiction scan failed for {categories}: {e}")

    # Deduplicate by paper pair
    seen_pairs = set()
    unique = []
    for c in all_contradictions:
        pa = c.get("paper_a", {}).get("paperId", "")
        pb = c.get("paper_b", {}).get("paperId", "")
        pair = tuple(sorted([pa, pb]))
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            unique.append(c)

    # Sort by severity
    severity_order = {"critical": 0, "moderate": 1, "minor": 2}
    unique.sort(key=lambda c: severity_order.get(c.get("severity", "minor"), 3))

    return {
        "contradictions": unique,
        "total_found": len(unique),
        "critical_count": sum(1 for c in unique if c.get("severity") == "critical"),
        "thesis_risk_assessments": thesis_risks,
    }


def _format_papers_for_contradiction(papers: list[dict]) -> str:
    """Format papers for the CONTRADICTION_MAPPER agent."""
    lines = []
    for p in papers:
        key_claim = p.get("key_claim", p.get("one_sentence_contribution", "N/A"))
        limitation = p.get("limitation", "N/A")
        lines.append(
            f"paperId: {p['paperId']}\n"
            f"title: {p.get('title', 'N/A')}\n"
            f"year: {p.get('year', 'N/A')}\n"
            f"category: {p.get('primary_category', 'X')}\n"
            f"key_claim: {key_claim}\n"
            f"method_type: {p.get('method_type', 'N/A')}\n"
            f"limitation: {limitation}\n"
            f"abstract: {(p.get('abstract') or '')[:400]}\n"
            f"---"
        )
    return "\n".join(lines)


def _generate_contradiction_report(contradictions: dict, classified: list[dict],
                                    output_dir: str):
    """Generate human-readable contradiction report."""
    by_id = {p["paperId"]: p for p in classified}

    lines = ["# Contradiction & Tension Map\n"]
    lines.append("*Papers that disagree — must be addressed in Related Work for academic honesty*\n\n---\n")

    severity_icons = {"critical": "🔴", "moderate": "🟡", "minor": "🟢"}

    for c in contradictions.get("contradictions", []):
        cid = c.get("id", "?")
        severity = c.get("severity", "?")
        icon = severity_icons.get(severity, "❓")
        ctype = c.get("type", "?")

        lines.append(f"## {cid}: {icon} {severity.upper()} — {ctype}\n")
        lines.append(f"**Question**: {c.get('question', 'N/A')}\n")

        pa = c.get("paper_a", {})
        pb = c.get("paper_b", {})
        pa_paper = by_id.get(pa.get("paperId", ""), {})
        pb_paper = by_id.get(pb.get("paperId", ""), {})

        lines.append(f"**Paper A**: {pa_paper.get('title', pa.get('paperId', '?'))[:80]}")
        lines.append(f"  Claim: {pa.get('claim', 'N/A')}")
        lines.append(f"  Evidence: {pa.get('evidence', 'N/A')}\n")

        lines.append(f"**Paper B**: {pb_paper.get('title', pb.get('paperId', '?'))[:80]}")
        lines.append(f"  Claim: {pb.get('claim', 'N/A')}")
        lines.append(f"  Evidence: {pb.get('evidence', 'N/A')}\n")

        lines.append(f"**Relevance to thesis**: {c.get('relevance_to_thesis', 'N/A')}")
        lines.append(f"**Beat affected**: {c.get('beat_affected', 'N/A')}")
        lines.append(f"**Suggested handling**: {c.get('suggested_handling', 'N/A')}\n")
        lines.append("---\n")

    # Summary
    total = contradictions.get("total_found", 0)
    critical = contradictions.get("critical_count", 0)
    lines.append(f"\n## Summary\n")
    lines.append(f"Total contradictions: {total}")
    lines.append(f"Critical (must address): {critical}")

    risks = contradictions.get("thesis_risk_assessments", [])
    if risks:
        lines.append(f"\n## Thesis Risk Assessments\n")
        for r in risks:
            lines.append(f"- {r}")

    report_path = os.path.join(output_dir, "contradiction_map.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.info(f"Contradiction report: {report_path}")
