"""Phase 3.7: Contradiction Map — identify disagreements between papers."""

from __future__ import annotations

import json
import logging
import os

from .api_client import agent_run_json, BRAIN_PHASE3_CONTRADICTION
from .phase_contracts import ensure_contradictions_valid
from .prompts import CONTRADICTION_MAPPER
from .state_manager import complete_step, is_step_complete
from .utils import atomic_write_json, load_json, filter_active_papers

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
    "competing_mechanism": 4,
}

ARGUMENT_LINE_BUCKETS = {
    "motivation": ("motivation", "Motivation / Background"),
    "framework": ("framework", "Design Primitives Framework"),
    "primary": ("primary", "Primary Evidence (Formative Survey)"),
    "core_contribution": ("core_contribution", "Core Contribution (CampusRide Platform)"),
    "cross-line": ("cross_line", "Cross-line"),
    "adversarial": ("adversarial", "Adversarial / Algorithmic Management Critique"),
}

ARGUMENT_LINE_BUCKET_ORDER = (
    "motivation",
    "framework",
    "primary",
    "core_contribution",
    "cross_line",
    "adversarial",
)

FALLBACK_FOCUS_HEURISTICS = {
    ("A", "B"): {
        "question": "Do commercial rideshare (Uber/Lyft) services actually underserve small-town university settings?",
        "type": "scope_disagreement",
        "severity": "moderate",
        "beat": 1,
        "side_a_keywords": ["gap", "underserved", "expensive", "availability", "rural", "small town", "peer-to-peer"],
        "side_b_keywords": ["adequate service", "well served", "low demand", "substitute", "shuttle", "public transit", "campus bus"],
        "relevance": (
            "This is the foundational motivation claim of Beat 1. Counterevidence suggests substitutes or"
            " that commercial rideshare is adequate in some small-town settings; this narrows the gap claim"
            " to specific contexts rather than a universal underservice."
        ),
        "handling": (
            "Frame small-town underservice as documented and motivated, not universally empirically quantified."
        ),
        "unresolved": "Whether the documented gap is national across US small-town universities or concentrated in specific settings.",
    },
    ("C", "D"): {
        "question": "Is WeChat/WhatsApp grassroots coordination already adequate without formalization into a platform?",
        "type": "scope_disagreement",
        "severity": "critical",
        "beat": 2,
        "side_a_keywords": ["grassroots", "self-organized", "community autonomy", "informal infrastructure", "adequate", "preserve"],
        "side_b_keywords": ["formalization", "platform design", "scaling limits", "coordination failure", "trust deficit", "needs design"],
        "relevance": (
            "The platform thesis depends on formalization being worthwhile. Counterevidence suggests"
            " grassroots coordination already works, or that formalization risks community autonomy loss."
        ),
        "handling": (
            "Acknowledge grassroots adequacy for many purposes; frame CampusRide as formalization of specific"
            " coordination patterns (identity verification, safety, rating) rather than replacement of informal channels."
        ),
        "unresolved": "Whether formalization preserves or degrades grassroots-community trust and autonomy.",
    },
    ("E", "F"): {
        "question": "Does .edu institutional identity verification meaningfully reduce rideshare safety risk?",
        "type": "scope_disagreement",
        "severity": "critical",
        "beat": 3,
        "side_a_keywords": [".edu verification", "institutional identity", "trust uplift", "closed community", "credential"],
        "side_b_keywords": ["verification failure", "harassment despite verification", "identity is not behavior", "campus incident", "fraud"],
        "relevance": (
            "The platform uses .edu identity as its primary trust primitive. Counterevidence shows that"
            " institutional identity does not prevent behavioral harm; this narrows the primitive claim."
        ),
        "handling": (
            "Frame .edu verification as a trust signal that reduces anonymity-based risk, not as a substitute"
            " for ongoing behavioral safety design. State explicitly: identity verification is necessary but not sufficient."
        ),
        "unresolved": "Whether verified-identity platforms reduce actual incident rates vs only perceived safety.",
    },
    ("H",): {
        "question": "Does peer rating fairness need dedicated design, or do stronger identity signals alone suffice?",
        "type": "methodological_tension",
        "severity": "critical",
        "beat": 5,
        "side_a_keywords": ["rating fairness", "algorithmic management", "rating anxiety", "driver precarity", "contested rating"],
        "side_b_keywords": ["rating works", "identity solves", "no fairness needed", "reputation stability"],
        "relevance": (
            "Survey finding F5 suggests drivers are especially sensitive to unfair ratings. Counterevidence"
            " would show rating systems work adequately without dedicated fairness mechanisms."
        ),
        "handling": (
            "Present F5 as a campus-scale observation resonating with algorithmic management literature;"
            " the design response (bidirectional rating with explanation, dispute window) is a hypothesis, not validation."
        ),
        "unresolved": "Whether design-level rating-fairness features actually reduce driver anxiety at deployment.",
    },
    ("G", "J"): {
        "question": "Does gamification in carpooling produce unintended effects (gaming behavior, motivation crowding)?",
        "type": "competing_mechanism",
        "severity": "moderate",
        "beat": 7,
        "side_a_keywords": ["gamification", "points", "rewards", "behavioral change", "engagement"],
        "side_b_keywords": ["crowding out", "intrinsic motivation", "gaming behavior", "quality degradation", "overjustification"],
        "relevance": (
            "Survey finding F4 shows gamification as a secondary motivator; design response keeps points"
            " auxiliary. Counterevidence (overjustification / gaming) narrows the gamification claim further."
        ),
        "handling": (
            "Frame gamification as auxiliary; acknowledge overjustification and gaming as live risks that warrant"
            " monitoring at deployment time."
        ),
        "unresolved": "Whether cross-module points induce gaming in carpool specifically (fake trips, ride stacking).",
    },
}

# Categories that are most likely to contain contradictions relevant to our thesis
CONTRADICTION_FOCUS_CONFIGS = [
    {
        "categories": ["A", "B"],
        "question": "F1 Gap vs. Substitute: Does commercial rideshare really underserve small-town universities, or do substitutes (shuttles, transit) adequately fill the gap?",
        "priority_papers": [],
        "guidance": (
            "Surface the strongest substitute / adequacy counterevidence (campus shuttles, taxis, public"
            " transit). The pro-gap claim should be narrowed to specific small-town contexts rather than"
            " universal underservice."
        ),
    },
    {
        "categories": ["C", "D"],
        "question": "F2 Grassroots Legitimacy: Does grassroots WeChat/WhatsApp coordination need formalization, or is it already adequate (and does formalization risk community autonomy)?",
        "priority_papers": [],
        "guidance": (
            "Surface counterevidence arguing informal coordination is already adequate or that formalization"
            " damages community autonomy / trust. Look for CSCW literature on informal-to-formal platform shifts."
        ),
    },
    {
        "categories": ["E", "F"],
        "question": "F3 .edu as Trust Primitive: Does institutional identity verification meaningfully reduce harm, or does it merely shift risk?",
        "priority_papers": [],
        "guidance": (
            "Surface case studies, incident reports, or critical analyses showing institutional identity"
            " verification (.edu, campus card) failing to prevent fraud, harassment, or unsafe behavior."
        ),
    },
    {
        "categories": ["H"],
        "question": "F4 Rating Fairness as Independent Design Concern: Do peer rating systems need dedicated fairness design, or is strong identity verification enough?",
        "priority_papers": [],
        "guidance": (
            "Surface literature arguing peer rating systems work without dedicated fairness mechanisms, or"
            " that rating-fairness concerns are overstated relative to identity and governance."
        ),
    },
    {
        "categories": ["G", "J"],
        "question": "F5 Gamification Risk: Does gamification produce unintended effects (motivation crowding, gaming behavior, equity concerns) in mobility / coordination contexts?",
        "priority_papers": [],
        "guidance": (
            "Surface overjustification / gaming-behavior literature and any gamification-in-mobility"
            " failure cases. The pro-gamification claim should be narrowed to auxiliary use cases."
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

    classified = filter_active_papers(load_json(classified_path))
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

    line_coverage = []
    for bucket_key in ARGUMENT_LINE_BUCKET_ORDER:
        bucket_items = []
        label = bucket_key.replace("_", " ").title()
        source_questions = []
        for item in contradictions:
            item_bucket, item_label = _argument_line_bucket(item.get("argument_line", ""))
            if item_bucket != bucket_key:
                continue
            bucket_items.append(item)
            label = item_label
            source_question = item.get("source_question", "")
            if source_question and source_question not in source_questions:
                source_questions.append(source_question)
        if bucket_items:
            line_coverage.append({
                "bucket": bucket_key,
                "label": label,
                "count": len(bucket_items),
                "source_questions": source_questions[:4],
                "representative_question": bucket_items[0].get("question", ""),
            })

    return {
        "must_address_limiters": top_limiters,
        "focus_coverage": focus_coverage,
        "line_coverage": line_coverage,
        "unresolved_tensions": unresolved_tensions[:8],
        "structural_limitations": (structural_limitations or [])[:6],
    }


def _argument_line_bucket(argument_line: str) -> tuple[str, str]:
    """Collapse detailed argument lines into reviewer-facing buckets."""
    key = str(argument_line or "").strip()
    return ARGUMENT_LINE_BUCKETS.get(key, ("cross_line", "Cross-line"))


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
        "side_a_keywords": ["gap", "risk", "harm", "unfair", "precarity"],
        "side_b_keywords": ["adequate", "works", "effective", "sufficient", "substitute"],
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

        if category_key == ("A", "B"):
            caveats.append(
                "Frame small-town university underservice as motivated and contextually documented, not as a universally empirically quantified gap; acknowledge substitutes (shuttles, transit) where present."
            )
        if category_key == ("C", "D"):
            caveats.append(
                "Acknowledge that grassroots WeChat/WhatsApp coordination is adequate for many coordination needs; frame CampusRide as formalization of specific patterns rather than replacement of informal channels."
            )
        if category_key == ("E", "F"):
            caveats.append(
                "State explicitly that .edu identity verification is a trust signal that reduces anonymity-based risk, not a substitute for ongoing behavioral safety design."
            )
        if category_key == ("H",):
            item["argument_line"] = "adversarial"
            item["beat_affected"] = 5
            caveats.append(
                "Present the rating-fairness observation (F5, N=30) as resonating with algorithmic management literature rather than replicating it; the design response is a hypothesis, not a validation."
            )
        if category_key == ("G", "J"):
            item["argument_line"] = "adversarial"
            item["beat_affected"] = 7
            if item.get("type") not in TYPE_PRIORITY:
                item["type"] = "competing_mechanism"
            caveats.append(
                "Treat gamification-induced gaming behavior and motivation crowding as genuine risks; keep points auxiliary rather than primary in design arguments."
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
        ("A", "B"): ("gap-documentation papers", "substitute / adequacy papers"),
        ("C", "D"): ("grassroots-adequate papers", "formalization-needed papers"),
        ("E", "F"): ("identity-verification-effective papers", "identity-verification-fails / harm-documented papers"),
        ("H",): ("rating-fairness-needs-design papers", "rating-works-without-fairness-features papers"),
        ("G", "J"): ("gamification-works papers", "gamification-risk / overjustification papers"),
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

    if any(
        key in focus_evidence_balance
        for key in [
            "F1 Gap vs. Substitute: Does commercial rideshare really underserve small-town universities, or do substitutes (shuttles, transit) adequately fill the gap?",
        ]
    ):
        limitations.append(
            "The small-town gap claim rests on scattered documentation rather than a single systematic multi-university audit; present it as motivated and contextually documented, not universally quantified."
        )

    if "F3 .edu as Trust Primitive: Does institutional identity verification meaningfully reduce harm, or does it merely shift risk?" in focus_evidence_balance:
        limitations.append(
            "The corpus contains .edu identity verification design claims but limited incident-level evidence on whether verification reduces behavioral harm; keep the trust-primitive claim scope-limited."
        )

    if "F5 Gamification Risk: Does gamification produce unintended effects (motivation crowding, gaming behavior, equity concerns) in mobility / coordination contexts?" in focus_evidence_balance:
        limitations.append(
            "Category G and J papers must be treated as adversarial scope evidence for gamification; do not write as if points-based incentives are self-justifying."
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
        "argument_line": "adversarial" if heuristic.get("beat") == 7 else "cross-line",
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

    line_coverage = review_summary.get("line_coverage", [])
    if line_coverage:
        lines.append("## Argument-Line Coverage\n")
        for item in line_coverage:
            lines.append(
                f"- {item.get('label', 'N/A')} "
                f"(count={item.get('count', 0)})"
            )
            source_questions = item.get("source_questions", [])
            if source_questions:
                lines.append(f"  Focuses: {' | '.join(source_questions)}")
            representative = item.get("representative_question", "")
            if representative:
                lines.append(f"  Representative: {representative}")
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

    structural_limitations = review_summary.get("structural_limitations") or contradictions.get("structural_limitations", [])
    if structural_limitations:
        lines.append("## Structural Limitations\n")
        for item in structural_limitations:
            lines.append(f"- {item}")
        lines.append("")

    severity_icons = {"critical": "🔴", "moderate": "🟡", "minor": "🟢"}
    grouped = {bucket: [] for bucket in ARGUMENT_LINE_BUCKET_ORDER}
    for item in contradictions.get("contradictions", []):
        bucket, _label = _argument_line_bucket(item.get("argument_line", ""))
        grouped.setdefault(bucket, []).append(item)

    for bucket_key in ARGUMENT_LINE_BUCKET_ORDER:
        items = grouped.get(bucket_key, [])
        if not items:
            continue
        _bucket, bucket_label = _argument_line_bucket(items[0].get("argument_line", ""))
        lines.append(f"## {bucket_label}\n")

        for c in items:
            cid = c.get("id", "?")
            severity = c.get("severity", "?")
            icon = severity_icons.get(severity, "❓")
            ctype = c.get("type", "?")

            lines.append(f"### {cid}: {icon} {severity.upper()} — {ctype}\n")
            lines.append(f"**Source focus**: {c.get('source_question', 'N/A')}")
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
