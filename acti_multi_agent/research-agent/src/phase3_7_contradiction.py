"""Phase 3.7: Contradiction Map — identify disagreements between papers."""

from __future__ import annotations

import json
import logging
import os

from .api_client import agent_run_json, BRAIN_PHASE3_CONTRADICTION
from .phase_contracts import ensure_contradictions_valid
from .prompts import CONTRADICTION_MAPPER
from .state_manager import complete_step, is_step_complete
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")

# Import centralized beat definitions
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.beat_definitions import ARGUMENT_LINES, HONESTY_CONSTRAINTS

TYPE_PRIORITY = {
    "direct_contradiction": 0,
    "scope_disagreement": 1,
    "methodological_tension": 2,
    "implicit_tension": 3,
}

FALLBACK_FOCUS_HEURISTICS = {
    ("A", "E"): {
        "question": "Can curated synthetic data or correction mechanisms prevent collapse without fresh human data every round?",
        "type": "direct_contradiction",
        "severity": "critical",
        "beat": 1,
        "side_a_keywords": [
            "collapse",
            "irreversible",
            "forget",
            "autophagy",
            "tail",
            "fresh real data",
            "fresh human data",
            "degradation",
        ],
        "side_b_keywords": [
            "avoid collapse",
            "prevent collapse",
            "stable",
            "stability",
            "self-improve",
            "synthetic augmentation",
            "verification",
            "correction",
            "negative guidance",
            "preserve",
        ],
        "relevance": (
            "This narrows any universal claim that recursive synthetic reuse must fail in all settings. "
            "The honest framing is conditional: collapse papers establish a real risk, while curation/correction papers claim bounded mitigations."
        ),
        "handling": (
            "Frame this as a conditional dispute. Say collapse risk is well-supported under recursive reuse, "
            "but note that verification, retained real anchors, or correction functions are proposed mitigations rather than dismissing them."
        ),
        "unresolved": [
            "Whether mitigation papers genuinely eliminate dependence on human-grounded anchors or simply hide that dependence in the verifier/correction signal.",
            "Whether anti-collapse results transfer from bounded or stylized settings to socially grounded web-scale language data.",
        ],
    },
    ("B", "C"): {
        "question": "Is AI-generated web pollution practically detectable at scale, or are current detectors too brittle?",
        "type": "direct_contradiction",
        "severity": "critical",
        "beat": 2,
        "side_a_keywords": [
            "detect",
            "detection",
            "watermark",
            "retrieval-based",
            "provenance",
            "trace",
            "effective defense",
            "robust",
        ],
        "side_b_keywords": [
            "evade",
            "evasion",
            "brittle",
            "fragile",
            "break",
            "adversarial",
            "spoof",
            "undetectable",
            "fails",
        ],
        "relevance": (
            "This determines whether Beat 2 can claim contamination is observable in practice or only a plausible risk. "
            "If detectors are brittle, the argument must rely on measured prevalence and provenance-limited defenses rather than simple detectability claims."
        ),
        "handling": (
            "Separate detector success in cooperative or provider-controlled settings from adversarial open-web conditions. "
            "Do not write as if current detection tooling has solved contamination measurement."
        ),
        "unresolved": [
            "Whether provenance-style defenses scale outside provider-controlled ecosystems.",
            "How much detector robustness survives paraphrase, human editing, and mixed-authorship settings.",
        ],
    },
    ("D", "H"): {
        "question": "Has measurable live-web drift already made web-only pretraining unreliable, or is the evidence still partial?",
        "type": "scope_disagreement",
        "severity": "critical",
        "beat": 2,
        "side_a_keywords": [
            "contamination",
            "drift",
            "decline",
            "degradation",
            "temporal",
            "lower bounds",
            "ai-generated content",
            "measurable",
        ],
        "side_b_keywords": [
            "filtered",
            "deduplicated",
            "outperform",
            "competitive",
            "web data alone",
            "properly filtered",
            "still train",
            "documented",
        ],
        "relevance": (
            "This is the main limiter on Beat 2. Measured contamination growth does not automatically prove that web-only corpora are already unusable if filtered-web training papers still perform strongly."
        ),
        "handling": (
            "Narrow the claim to rising contamination risk plus incomplete measurement. "
            "Treat filtered-web success as a scope limiter, not as proof that contamination is harmless."
        ),
        "unresolved": [
            "Whether measured contamination in a few platforms or corpora generalizes to broad web pretraining mixtures.",
            "How much current filtering pipelines are already offsetting contamination without making the risk disappear.",
        ],
    },
    ("E", "F"): {
        "question": "Where does human data remain necessary despite synthetic curation, AI feedback, or self-alignment success?",
        "type": "direct_contradiction",
        "severity": "critical",
        "beat": 4,
        "side_a_keywords": [
            "human",
            "human feedback",
            "human-centric",
            "grounded",
            "socially grounded",
            "annotation",
            "preference",
            "human-in-the-loop",
        ],
        "side_b_keywords": [
            "self-alignment",
            "minimal human",
            "almost no human",
            "rlaif",
            "synthetic",
            "ai feedback",
            "principle-driven",
            "self-instruct",
        ],
        "relevance": (
            "This limits how strongly the thesis can claim that fresh human data is indispensable. "
            "The stronger honest position is that human-grounded data remains especially valuable for socially grounded, safety-sensitive, or evaluator-defining tasks."
        ),
        "handling": (
            "Acknowledge minimal-human and AI-feedback success cases directly, then state that these do not fully settle tasks needing social grounding, evaluator choice, or external validation."
        ),
        "unresolved": [
            "Whether self-alignment papers truly eliminate human dependence or simply move it upstream into constitutions, reward models, or evaluation design.",
            "Which tasks still fail without fresh human-grounded supervision even when synthetic or AI-feedback pipelines look strong.",
        ],
    },
    ("F", "J"): {
        "question": "How far can synthetic instruction data and AI feedback reduce reliance on human-authored supervision?",
        "type": "scope_disagreement",
        "severity": "moderate",
        "beat": 5,
        "side_a_keywords": [
            "self-instruct",
            "synthetic instruction",
            "rlaif",
            "ai feedback",
            "distill",
            "self-alignment",
            "preference optimization",
        ],
        "side_b_keywords": [
            "social reasoning",
            "commonsense",
            "theory of mind",
            "behavior",
            "grounded",
            "human-authored",
            "socially grounded",
        ],
        "relevance": (
            "This keeps Beat 6 from overselling platform value or synthetic substitution. Synthetic instruction pipelines can work well for many tasks, while socially grounded reasoning may still expose missing human signals."
        ),
        "handling": (
            "Write Beat 6 as a targeted platform proposal for high-value data niches, not a blanket claim that all future training must shift away from web/synthetic mixtures."
        ),
        "unresolved": [
            "Which downstream tasks actually benefit from the proposed human-grounded data collection pipeline rather than generic synthetic instruction expansion.",
        ],
    },
    ("B", "E", "H"): {
        "question": "Do filtered or documented corpora complicate a simple contamination-to-quality-decline story?",
        "type": "scope_disagreement",
        "severity": "critical",
        "beat": 2,
        "side_a_keywords": [
            "contamination",
            "decline",
            "pollution",
            "drift",
            "ai-generated content",
            "quality decline",
        ],
        "side_b_keywords": [
            "filtered",
            "documented",
            "curated",
            "deduplicated",
            "competitive",
            "web data alone",
        ],
        "relevance": (
            "This warns against a one-step story from contamination to collapse. Documentation and filtering work can partially absorb contamination, so the thesis must be framed as risk escalation rather than inevitable present failure."
        ),
        "handling": (
            "Explicitly separate measured contamination growth from claims about downstream model failure. "
            "Use documented or filtered corpora as boundary conditions on the argument."
        ),
        "unresolved": [
            "How much current curation practice actually offsets contamination in large web mixtures.",
        ],
    },
    ("I", "J"): {
        "question": "Does social reasoning weakness reflect a real human-data gap, or can data composition fixes close it?",
        "type": "scope_disagreement",
        "severity": "moderate",
        "beat": 4,
        "side_a_keywords": [
            "social reasoning",
            "commonsense",
            "theory of mind",
            "weakness",
            "stress testing",
            "fails",
            "behavior",
        ],
        "side_b_keywords": [
            "data composition",
            "ablation",
            "improve",
            "instruction tuning",
            "mixture",
            "benchmark gains",
            "fine-tuning",
        ],
        "relevance": (
            "This determines whether the proposed human-grounded data source is addressing a genuine evidence gap or only one of several possible interventions."
        ),
        "handling": (
            "Present social reasoning as an evidence-backed niche where data composition matters, while admitting that not every benchmark failure uniquely implies missing human-behavior data."
        ),
        "unresolved": [
            "Whether observed social reasoning gains come from genuinely new human signal or from improved task formatting and instruction mixtures.",
        ],
    },
}

# Categories that are most likely to contain contradictions relevant to our thesis
CONTRADICTION_FOCUS_CONFIGS = [
    {
        "categories": ["A", "E"],
        "question": "When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation)",
        "priority_papers": [
            "doi:10.1038/s41586-024-07566-y",
            "doi:10.52591/lxai202312101",
            "doi:10.48550/arxiv.2407.09499",
            "doi:10.48550/arxiv.2406.07515",
            "doi:10.48550/arxiv.2410.22812",
        ],
        "guidance": (
            "You must surface the strongest pro-curation and pro-verification counterexamples, "
            "not only collapse papers."
        ),
    },
    {
        "categories": ["B", "C"],
        "question": "Is web pollution detectable? (pollution scale vs detection limits)",
        "priority_papers": [
            "doi:10.1145/3774904.3792955",
            "doi:10.48550/arxiv.2602.16136",
            "doi:10.48550/arxiv.2303.13408",
            "doi:10.1613/jair.1.16665",
        ],
        "guidance": (
            "Distinguish brittle classifier-style detection from retrieval or provenance-based defenses. "
            "If a paper is a scope-limited prevalence study, treat it as partial evidence, not direct proof of web-scale contamination."
        ),
    },
    {
        "categories": ["D", "H"],
        "question": "How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement)",
        "priority_papers": [
            "doi:10.18653/v1/2024.findings-naacl.228",
            "doi:10.1145/3590152",
            "doi:10.48550/arxiv.2406.17557",
            "doi:10.48550/arxiv.2306.01116",
        ],
        "guidance": (
            "Look for both support and limitations: metric papers, longitudinal corpora, and filtered-web results should jointly test how far Beat 2 can really go."
        ),
    },
    {
        "categories": ["E", "F"],
        "question": "Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF)",
        "priority_papers": [
            "doi:10.48550/arxiv.2309.00267",
            "doi:10.48550/arxiv.2305.18290",
            "doi:10.48550/arxiv.2304.05302",
            "doi:10.48550/arxiv.2305.14387",
        ],
        "guidance": (
            "Make sure AI-feedback and preference-optimization success cases are treated as real counterevidence, not side notes."
        ),
    },
    {
        "categories": ["F", "J"],
        "question": "How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision?",
        "priority_papers": [
            "doi:10.18653/v1/2023.acl-long.754",
            "doi:10.48550/arxiv.2304.12244",
            "doi:10.48550/arxiv.2304.07327",
            "doi:10.48550/arxiv.2309.00267",
            "doi:10.48550/arxiv.2310.16944",
            "doi:10.48550/arxiv.2305.14387",
        ],
        "guidance": (
            "Prioritize the strongest synthetic-data and open-alignment success papers such as Self-Instruct, WizardLM, OpenAssistant, RLAIF, Zephyr, and AlpacaFarm if present."
        ),
    },
    {
        "categories": ["B", "E", "H"],
        "question": "Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story?",
        "priority_papers": [
            "doi:10.48550/arxiv.2306.01116",
            "doi:10.18653/v1/2021.emnlp-main.98",
            "doi:10.48550/arxiv.2406.17557",
            "doi:10.1145/3774904.3792955",
            "doi:10.18653/v1/2024.wikinlp-1.12",
        ],
        "guidance": (
            "Explicitly surface filtered-web success and corpus-documentation papers as scope limiters against a simple contamination-equals-decline story."
        ),
    },
    {
        "categories": ["I", "J"],
        "question": "Does data composition matter for social reasoning? (benchmarks vs ablation)",
        "priority_papers": [
            "doi:10.48550/arxiv.2305.11206",
            "doi:10.18653/v1/2023.emnlp-main.183",
            "doi:10.18653/v1/2022.emnlp-main.248",
        ],
        "guidance": (
            "Prefer direct tensions between social-benchmark weakness and data-composition successes, not generic dialogue papers."
        ),
    },
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
        ensure_contradictions_valid(contradictions)
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
    scan_errors = []
    fallback_warnings = []
    focus_evidence_balance = {}

    unresolved_tensions = []

    for config in CONTRADICTION_FOCUS_CONFIGS:
        categories = config["categories"]
        question = config["question"]
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

        selected_papers = _select_contradiction_input_papers(
            papers,
            categories,
            priority_papers=config.get("priority_papers", []),
        )
        focus_evidence_balance[question] = _summarize_focus_evidence_balance(
            categories,
            papers,
            selected_papers,
        )
        papers_input = _format_papers_for_contradiction(selected_papers)

        try:
            result = _run_contradiction_agent(
                client,
                categories,
                question,
                papers,
                selected_papers,
                papers_input,
                guidance=config.get("guidance", ""),
                priority_papers=config.get("priority_papers", []),
            )
            if isinstance(result, dict):
                result = _postprocess_contradiction_result(result, categories)
                for c in result.get("contradictions", []):
                    c["source_categories"] = categories
                    c["source_question"] = question
                    all_contradictions.append(c)
                if result.get("thesis_risk_assessment"):
                    thesis_risks.append(result["thesis_risk_assessment"])
                for tension in result.get("unresolved_tensions", []) or []:
                    if tension not in unresolved_tensions:
                        unresolved_tensions.append(tension)
                log.info(f"  Found {len(result.get('contradictions', []))} contradictions")
        except Exception as e:
            log.error(f"  Contradiction scan failed for {categories}: {e}")
            fallback = _fallback_contradiction_focus(
                categories,
                question,
                selected_papers,
                guidance=config.get("guidance", ""),
                error=e,
            )
            fallback = _postprocess_contradiction_result(fallback, categories)
            fallback_warnings.append({
                "categories": categories,
                "question": question,
                "error": str(e),
            })
            for c in fallback.get("contradictions", []):
                c["source_categories"] = categories
                c["source_question"] = question
                all_contradictions.append(c)
            if fallback.get("thesis_risk_assessment"):
                thesis_risks.append(fallback["thesis_risk_assessment"])
            for tension in fallback.get("unresolved_tensions", []) or []:
                if tension not in unresolved_tensions:
                    unresolved_tensions.append(tension)

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

    # Sort by severity, while front-loading breadth across focus questions.
    severity_order = {"critical": 0, "moderate": 1, "minor": 2}
    unique.sort(
        key=lambda c: (
            severity_order.get(c.get("severity", "minor"), 3),
            TYPE_PRIORITY.get(c.get("type", ""), 99),
        )
    )
    ordered = _prioritize_contradiction_order(unique)
    focus_summary = _build_focus_summary(ordered, focus_evidence_balance)
    structural_limitations = _build_structural_limitations(classified, focus_evidence_balance)
    review_summary = _build_review_summary(
        ordered,
        unresolved_tensions,
        focus_summary,
        structural_limitations,
    )

    return {
        "review_summary": review_summary,
        "focus_summary": focus_summary,
        "structural_limitations": structural_limitations,
        "contradictions": ordered,
        "total_found": len(ordered),
        "critical_count": sum(1 for c in ordered if c.get("severity") == "critical"),
        "thesis_risk_assessments": thesis_risks,
        "unresolved_tensions": unresolved_tensions,
        "scan_errors": scan_errors,
        "fallback_warnings": fallback_warnings,
    }


def _prioritize_contradiction_order(contradictions: list[dict]) -> list[dict]:
    """Put one representative contradiction per focus question up front."""
    if not contradictions:
        return []

    grouped: dict[str, list[dict]] = {}
    for item in contradictions:
        grouped.setdefault(item.get("source_question", "unknown"), []).append(item)

    ordered = []
    seen = set()

    for question, items in grouped.items():
        ranked = sorted(
            items,
            key=lambda c: (
                TYPE_PRIORITY.get(c.get("type", ""), 99),
                0 if c.get("severity") == "critical" else 1,
                -(c.get("beat_affected") or 0),
            ),
        )
        best = ranked[0]
        ordered.append(best)
        seen.add(id(best))

    for item in contradictions:
        if id(item) not in seen:
            ordered.append(item)

    return ordered


def _build_focus_summary(contradictions: list[dict], focus_evidence_balance: dict[str, dict] | None = None) -> list[dict]:
    """Summarize contradiction coverage per focus question."""
    focus_evidence_balance = focus_evidence_balance or {}
    grouped: dict[str, list[dict]] = {}
    for item in contradictions:
        grouped.setdefault(item.get("source_question", "unknown"), []).append(item)

    summary = []
    for question, items in grouped.items():
        representative = items[0]
        item = {
            "focus_question": question,
            "categories": representative.get("source_categories", []),
            "count": len(items),
            "representative_question": representative.get("question", ""),
            "top_contradiction_type": representative.get("type", ""),
            "top_relevance": representative.get("relevance_to_thesis", ""),
        }
        balance = focus_evidence_balance.get(question)
        if balance:
            item.update(balance)
        summary.append(item)
    return summary


def _build_review_summary(contradictions: list[dict], unresolved_tensions: list[str],
                          focus_summary: list[dict],
                          structural_limitations: list[str] | None = None) -> dict:
    """Create a compact contradiction summary optimized for downstream review."""
    top_limiters = []
    for item in contradictions[:6]:
        top_limiters.append({
            "source_question": item.get("source_question", ""),
            "question": item.get("question", ""),
            "handling": item.get("suggested_handling", ""),
        })

    focus_coverage = [
        {
            "focus_question": item.get("focus_question", ""),
            "categories": item.get("categories", []),
            "count": item.get("count", 0),
        }
        for item in focus_summary
    ]

    return {
        "must_address_limiters": top_limiters,
        "focus_coverage": focus_coverage,
        "unresolved_tensions": unresolved_tensions[:8],
        "structural_limitations": (structural_limitations or [])[:6],
    }


def _select_contradiction_input_papers(papers: list[dict], categories: list[str],
                                       priority_papers: list[str] | None = None,
                                       max_total: int = 18, per_category: int = 9) -> list[dict]:
    """Keep contradiction scans focused on the highest-signal papers."""
    by_id = {}
    selected = []
    papers_by_id = {p["paperId"]: p for p in papers}

    for pid in priority_papers or []:
        paper = papers_by_id.get(pid)
        if paper and pid not in by_id:
            by_id[pid] = paper
            selected.append(paper)

    for category in categories:
        cat_papers = [
            p for p in papers
            if p.get("primary_category") == category
            or category in p.get("secondary_categories", [])
        ]
        cat_papers.sort(key=lambda x: (x.get("citationCount", 0), x.get("year", 0)), reverse=True)
        for paper in cat_papers[:per_category]:
            pid = paper["paperId"]
            if pid not in by_id:
                by_id[pid] = paper
                selected.append(paper)

    if len(selected) < max_total:
        ranked = sorted(papers, key=lambda x: (x.get("citationCount", 0), x.get("year", 0)), reverse=True)
        for paper in ranked:
            pid = paper["paperId"]
            if pid not in by_id:
                by_id[pid] = paper
                selected.append(paper)
            if len(selected) >= max_total:
                break

    return selected[:max_total]


def _looks_like_truncation_error(error: Exception) -> bool:
    text = str(error).lower()
    return (
        "unterminated string" in text
        or "max_output_tokens" in text
        or "missing output text" in text
        or "incomplete" in text
        or "read timed out" in text
        or "expecting ',' delimiter" in text
        or "could not parse a valid json" in text
    )


def _run_contradiction_agent(client, categories: list[str], question: str,
                             candidate_papers: list[dict], selected_papers: list[dict],
                             papers_input: str, guidance: str = "",
                             priority_papers: list[str] | None = None) -> dict:
    selected_by_id = {p["paperId"]: p for p in selected_papers}
    priority_titles = [
        f"{pid} :: {selected_by_id[pid].get('title', '')}"
        for pid in (priority_papers or [])
        if pid in selected_by_id
    ]
    task = (
        f"Identify contradictions among these papers.\n"
        f"Focus question: {question}\n"
        f"Categories: {categories}\n"
        f"There are {len(candidate_papers)} candidate papers; you are seeing the top "
        f"{len(selected_papers)} selected for signal density.\n"
        f"Additional guidance: {guidance or 'Prioritize the strongest thesis-limiting counterevidence.'}\n"
        f"Priority papers present: {' | '.join(priority_titles) if priority_titles else 'none'}\n"
        f"Return at most 6 strongest contradictions for this focus question.\n\n"
        f"{papers_input}"
    )
    try:
        return agent_run_json(
            client,
            role=CONTRADICTION_MAPPER,
            model=BRAIN_PHASE3_CONTRADICTION,
            task=task,
            max_tokens=8192,
        )
    except Exception as e:
        if not _looks_like_truncation_error(e) or len(selected_papers) <= 12:
            raise

        compact_papers = selected_papers[:12]
        compact_input = _format_papers_for_contradiction(compact_papers)
        compact_task = (
            f"Identify contradictions among these papers.\n"
            f"Focus question: {question}\n"
            f"Categories: {categories}\n"
            f"The first attempt overflowed. Use this compact subset of {len(compact_papers)} papers only.\n"
            f"Additional guidance: {guidance or 'Prioritize the strongest thesis-limiting counterevidence.'}\n"
            f"Priority papers present: {' | '.join(priority_titles) if priority_titles else 'none'}\n"
            f"Return at most 4 strongest contradictions. Keep evidence strings concise.\n\n"
            f"{compact_input}"
        )
        log.warning(
            "  Contradiction scan retrying with compact input for %s (%s papers)",
            categories,
            len(compact_papers),
        )
        return agent_run_json(
            client,
            role=CONTRADICTION_MAPPER,
            model=BRAIN_PHASE3_CONTRADICTION,
            task=compact_task,
            max_tokens=8192,
        )


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
            f"abstract: {(p.get('abstract') or '')[:220]}\n"
            f"---"
        )
    return "\n".join(lines)


def _fallback_contradiction_focus(categories: list[str], question: str, selected_papers: list[dict],
                                  guidance: str, error: Exception) -> dict:
    """Deterministic fallback when model contradiction mapping fails."""
    heuristic = FALLBACK_FOCUS_HEURISTICS.get(tuple(categories), {
        "question": question,
        "type": "scope_disagreement",
        "severity": "moderate",
        "beat": None,
        "side_a_keywords": ["risk", "decline", "human", "contamination"],
        "side_b_keywords": ["works", "improve", "filtered", "synthetic"],
        "relevance": (
            "This fallback contradiction is heuristic and should be read as a scope limiter rather than a definitive contradiction judgment."
        ),
        "handling": (
            "Use cautious wording and verify the cited pair manually before treating it as a central thesis limiter."
        ),
        "unresolved": [
            "Fallback heuristic could not rely on a validated model scan for this focus pair; manual review is still advised for the top papers.",
        ],
    })

    left_pool = _rank_fallback_side(
        selected_papers,
        heuristic.get("side_a_keywords", []),
        opposite_keywords=heuristic.get("side_b_keywords", []),
    )
    right_pool = _rank_fallback_side(
        selected_papers,
        heuristic.get("side_b_keywords", []),
        opposite_keywords=heuristic.get("side_a_keywords", []),
    )

    if not left_pool:
        left_pool = _category_fallback_pool(selected_papers, categories[:1])
    if not right_pool:
        right_pool = _category_fallback_pool(selected_papers, categories[1:] or categories[:1])

    contradictions = []
    used_pairs = set()
    pair_index = 1

    for left in left_pool:
        for right in right_pool:
            left_paper = left["paper"]
            right_paper = right["paper"]
            if left_paper.get("paperId") == right_paper.get("paperId"):
                continue
            pair_key = tuple(sorted([left_paper.get("paperId", ""), right_paper.get("paperId", "")]))
            if pair_key in used_pairs:
                continue
            contradictions.append(_build_fallback_contradiction(
                heuristic,
                pair_index,
                left,
                right,
                guidance=guidance,
            ))
            used_pairs.add(pair_key)
            pair_index += 1
            if len(contradictions) >= 2:
                break
        if len(contradictions) >= 2:
            break

    if not contradictions and selected_papers:
        ranked = sorted(
            selected_papers,
            key=lambda paper: (paper.get("citationCount", 0), paper.get("year", 0)),
            reverse=True,
        )
        if len(ranked) >= 2:
            left = {"paper": ranked[0], "hits": [], "score": 0}
            right = {"paper": ranked[1], "hits": [], "score": 0}
            contradictions.append(_build_fallback_contradiction(
                heuristic,
                1,
                left,
                right,
                guidance=guidance,
            ))

    titles = " vs ".join(
        item["paper"]["title"][:50]
        for item in ([left_pool[0]] if left_pool else []) + ([right_pool[0]] if right_pool else [])
    ) or "top candidate papers"
    risk_assessment = (
        "Heuristic contradiction fallback used after model failure. "
        f"Treat the strongest tension around '{titles}' as a scope limiter for this focus question, not as a settled verdict. "
        f"Original error: {error}"
    )
    unresolved = list(heuristic.get("unresolved", []))
    unresolved.append(
        f"Fallback heuristic used for {question}; review the cited pair manually if this focus question becomes central in the prose."
    )

    return {
        "contradictions": contradictions,
        "thesis_risk_assessment": risk_assessment,
        "unresolved_tensions": unresolved,
        "fallback_warning": str(error),
    }


def _postprocess_contradiction_result(result: dict, categories: list[str]) -> dict:
    """Add conservative caveats so contradiction handling does not overclaim."""
    category_key = tuple(categories)
    for item in result.get("contradictions", []):
        handling = str(item.get("suggested_handling", "")).strip()
        caveats = []

        if category_key in {("A", "E")}:
            caveats.append(
                "Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided."
            )
        if category_key in {("D", "H"), ("B", "E", "H")}:
            caveats.append(
                "State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure."
            )
        if category_key in {("E", "F"), ("F", "J"), ("I", "J")}:
            caveats.append(
                "State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result."
            )

        if caveats:
            existing = handling.lower()
            additions = [c for c in caveats if c.lower() not in existing]
            if additions:
                item["suggested_handling"] = (handling + " " + " ".join(additions)).strip()
    return result


def _summarize_focus_evidence_balance(categories: list[str], candidate_papers: list[dict],
                                      selected_papers: list[dict]) -> dict:
    heuristic = FALLBACK_FOCUS_HEURISTICS.get(tuple(categories), {})
    side_a_label, side_b_label = _focus_side_labels(categories)
    stance_counts = {"side_a": 0, "side_b": 0, "ambiguous": 0}
    side_a_examples = []
    side_b_examples = []

    for paper in candidate_papers:
        stance = _classify_focus_stance(paper, heuristic)
        stance_counts[stance] += 1
        if stance == "side_a" and len(side_a_examples) < 3:
            side_a_examples.append(paper.get("paperId", ""))
        elif stance == "side_b" and len(side_b_examples) < 3:
            side_b_examples.append(paper.get("paperId", ""))

    return {
        "candidate_papers": len(candidate_papers),
        "selected_papers": len(selected_papers),
        "stance_counts": stance_counts,
        "stance_labels": {
            "side_a": side_a_label,
            "side_b": side_b_label,
            "ambiguous": "mixed or weakly signaled papers",
        },
        "stance_examples": {
            "side_a": side_a_examples,
            "side_b": side_b_examples,
        },
    }


def _focus_side_labels(categories: list[str]) -> tuple[str, str]:
    mapping = {
        ("A", "E"): ("collapse-risk papers", "curation / mitigation papers"),
        ("B", "C"): ("detection / provenance support papers", "detection-limit / evasion papers"),
        ("D", "H"): ("drift / contamination evidence papers", "filtered-web resilience papers"),
        ("E", "F"): ("human-data-necessary papers", "AI-feedback / synthetic-substitution papers"),
        ("F", "J"): ("synthetic supervision works papers", "human-grounded limits papers"),
        ("B", "E", "H"): ("contamination-risk papers", "filtering / documentation limiters"),
        ("I", "J"): ("social-reasoning weakness papers", "data-composition intervention papers"),
    }
    return mapping.get(tuple(categories), ("side A papers", "side B papers"))


def _classify_focus_stance(paper: dict, heuristic: dict) -> str:
    if not heuristic:
        return "ambiguous"
    text = _paper_contradiction_text(paper)
    side_a_hits = sum(1 for kw in heuristic.get("side_a_keywords", []) if kw in text)
    side_b_hits = sum(1 for kw in heuristic.get("side_b_keywords", []) if kw in text)
    if side_a_hits > side_b_hits and side_a_hits > 0:
        return "side_a"
    if side_b_hits > side_a_hits and side_b_hits > 0:
        return "side_b"
    return "ambiguous"


def _build_structural_limitations(classified: list[dict], focus_evidence_balance: dict[str, dict]) -> list[str]:
    counts = {}
    for paper in classified:
        cat = paper.get("primary_category", "X")
        if cat == "X":
            continue
        counts[cat] = counts.get(cat, 0) + 1

    limitations = []
    if counts:
        high_cat, high_count = max(counts.items(), key=lambda item: item[1])
        low_cat, low_count = min(counts.items(), key=lambda item: item[1])
        limitations.append(
            f"All categories are populated, but the corpus is still asymmetric: {high_cat}={high_count} while {low_cat}={low_count}; treat this as uneven evidence density rather than balanced coverage."
        )

    if "How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement)" in focus_evidence_balance:
        limitations.append(
            "No paper in the current corpus directly provides a broad post-2022 web-scale contamination audit; Beat 2 remains a multi-paper inference chain rather than a single-study demonstration."
        )

    if (
        "Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF)" in focus_evidence_balance
        or "How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision?" in focus_evidence_balance
    ):
        limitations.append(
            "The corpus contains strong AI-feedback and self-alignment success papers, but it does not directly show those methods failing on social-reasoning tasks; that scope boundary is still hypothetical."
        )

    limitations.append(
        "Contradiction handling should distinguish evidence-backed scope limits from proposed thesis-saving explanations; when the corpus lacks a direct bridge, say so explicitly."
    )
    return limitations


def _rank_fallback_side(papers: list[dict], keywords: list[str],
                        opposite_keywords: list[str] | None = None) -> list[dict]:
    ranked = []
    opposite_keywords = opposite_keywords or []
    for paper in papers:
        text = _paper_contradiction_text(paper)
        hits = [kw for kw in keywords if kw in text]
        opposite_hits = [kw for kw in opposite_keywords if kw in text]
        score = len(hits) - len(opposite_hits)
        if score <= 0:
            continue
        ranked.append({
            "paper": paper,
            "hits": hits,
            "score": score,
        })

    ranked.sort(
        key=lambda item: (
            item["score"],
            item["paper"].get("citationCount", 0),
            item["paper"].get("year", 0),
        ),
        reverse=True,
    )
    return ranked[:5]


def _category_fallback_pool(papers: list[dict], categories: list[str]) -> list[dict]:
    ranked = []
    for paper in papers:
        primary = paper.get("primary_category")
        secondary = paper.get("secondary_categories", [])
        if primary in categories or any(cat in categories for cat in secondary):
            ranked.append({"paper": paper, "hits": [], "score": 0})

    ranked.sort(
        key=lambda item: (
            item["paper"].get("citationCount", 0),
            item["paper"].get("year", 0),
        ),
        reverse=True,
    )
    return ranked[:5]


def _paper_contradiction_text(paper: dict) -> str:
    fields = [
        paper.get("title", ""),
        paper.get("key_claim", ""),
        paper.get("one_sentence_contribution", ""),
        paper.get("limitation", ""),
        paper.get("abstract", ""),
        paper.get("methodology", ""),
    ]
    return " ".join(str(field).lower() for field in fields if field)


def _build_fallback_contradiction(heuristic: dict, index: int, left: dict, right: dict,
                                  guidance: str) -> dict:
    left_paper = left["paper"]
    right_paper = right["paper"]
    left_claim = left_paper.get("key_claim") or left_paper.get("one_sentence_contribution") or "Key claim unavailable."
    right_claim = right_paper.get("key_claim") or right_paper.get("one_sentence_contribution") or "Key claim unavailable."
    left_hits = ", ".join(left.get("hits") or []) or "category-priority selection"
    right_hits = ", ".join(right.get("hits") or []) or "category-priority selection"

    return {
        "id": f"H{index}",
        "type": heuristic.get("type", "scope_disagreement"),
        "severity": heuristic.get("severity", "moderate"),
        "question": heuristic.get("question", "What is the strongest scope-limiting tension here?"),
        "paper_a": {
            "paperId": left_paper.get("paperId", ""),
            "claim": left_claim[:280],
            "evidence": f"Fallback evidence via key claim and keyword hits: {left_hits}.",
        },
        "paper_b": {
            "paperId": right_paper.get("paperId", ""),
            "claim": right_claim[:280],
            "evidence": f"Fallback evidence via key claim and keyword hits: {right_hits}.",
        },
        "relevance_to_thesis": heuristic.get("relevance", ""),
        "suggested_handling": " ".join(
            part for part in (
                heuristic.get("handling", ""),
                guidance.strip(),
                "This pair came from the deterministic fallback, so keep the prose cautious and verify the pair manually before making it central.",
            )
            if part
        ).strip(),
        "beat_affected": heuristic.get("beat"),
    }


def _generate_contradiction_report(contradictions: dict, classified: list[dict],
                                    output_dir: str):
    """Generate human-readable contradiction report."""
    by_id = {p["paperId"]: p for p in classified}

    lines = ["# Contradiction & Tension Map\n"]
    lines.append("*Papers that disagree — must be addressed in Related Work for academic honesty*\n\n---\n")

    review_summary = contradictions.get("review_summary", {})
    if review_summary:
        lines.append("## Executive Summary\n")
        for idx, item in enumerate(review_summary.get("must_address_limiters", []), start=1):
            lines.append(
                f"{idx}. {item.get('source_question', 'N/A')} "
                f"→ {item.get('question', 'N/A')}"
            )
            lines.append(f"   Handling: {item.get('handling', 'N/A')}")
        lines.append("")

    focus_summary = contradictions.get("focus_summary", [])
    if focus_summary:
        lines.append("## Focus Coverage\n")
        for item in focus_summary:
            cats = ", ".join(item.get("categories", []))
            lines.append(
                f"- [{cats}] {item.get('focus_question', 'N/A')} "
                f"(count={item.get('count', 0)})"
            )
            lines.append(f"  Representative: {item.get('representative_question', 'N/A')}")
        lines.append("\n---\n")

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

    tensions = contradictions.get("unresolved_tensions", [])
    if tensions:
        lines.append(f"\n## Unresolved Tensions\n")
        for tension in tensions:
            lines.append(f"- {tension}")

    report_path = os.path.join(output_dir, "contradiction_map.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.info(f"Contradiction report: {report_path}")
