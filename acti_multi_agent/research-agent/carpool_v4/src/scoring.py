"""Scoring engine: 5-dimension evaluation + aggregator + auto-loop logic."""

from __future__ import annotations

import json
import logging
import os
import re
from collections import Counter

from .utils import load_json, atomic_write_json, filter_active_papers
from .api_client import REVIEWER_BRAINS, agent_run

log = logging.getLogger("research_agent")

# Import centralized beat definitions
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.beat_definitions import (
    BEAT_CATEGORIES, BEAT_NAMES, ARGUMENT_LINES, NUM_BEATS,
    CATEGORY_TARGETS, HONESTY_CONSTRAINTS, CATEGORY_SEQUENCE,
)

# Target paper counts per category (re-exported for backward compat)
# Already imported from config.beat_definitions

# Shared reviewer preamble injected into every reviewer task context so all
# five reviewers evaluate the v4 CampusRide paper on a consistent yardstick.
# See pipeline_v4_migration_and_config.md Part 5.1.
PAPER_CONTEXT_V4 = (
    "EVALUATION CONTEXT — READ BEFORE SCORING:\n\n"
    "This is a 12-15 page design case study paper for a mid-tier HCI conference "
    "or extended workshop submission. It has THREE contribution claims:\n"
    "  (1) CampusRide — an identity-verified multi-module campus platform "
    "(carpool, marketplace, activities, groups, messaging, points);\n"
    "  (2) a deep-dive case on the carpool module, grounded in an N=117 formative survey;\n"
    "  (3) research-agent — a thesis-conditioned evidence pipeline supporting the "
    "literature synthesis.\n\n"
    "Evaluate accordingly, not as a PhD-length empirical paper:\n\n"
    "- NOVELTY BAR: a well-scoped design case with survey-informed evidence and "
    "honest framing IS sufficient. Controlled experiments and deployment evaluation "
    "are NOT required.\n"
    "- EVIDENCE BAR: N=117 formative survey (N<=33 on individual ordinal items) is a "
    "reasonable formative-stage sample. Do NOT apply inferential-statistics standards. "
    "No t-tests or p-values are expected or appropriate.\n"
    "- SAMPLE SKEW: 82% Mandarin-native respondents is DISCLOSED as a scope-setting "
    "property. Evaluate whether the paper scopes its claims accordingly — NOT whether "
    "the sample is demographically balanced.\n"
    "- MULTI-MODULE SCOPE: the paper claims a multi-module platform but deep-dives only "
    "on carpool. This is a deliberate scoping choice. Other modules are described at "
    "overview level. Evaluate whether the carpool deep-dive transferability argument "
    "for other modules is honest — NOT whether each module is independently validated.\n"
    "- METHODOLOGY CONTRIBUTION: the research-agent pipeline is presented as a "
    "methodology tool used by this paper, not as a stand-alone validated research "
    "agent. Do NOT evaluate the pipeline itself — evaluate how the paper uses it and "
    "whether that use is honestly framed.\n"
    "- VERB DISCIPLINE: the paper is expected to use 'motivates', 'suggests', 'informs', "
    "'scopes' rather than 'proves', 'validates', 'demonstrates'. Do NOT penalize the "
    "paper for cautious verbs; DO penalize over-claiming verbs.\n"
)

# Reviewer prompts (inline — these mirror the slash commands but as system prompts).
# Every reviewer is evaluated under PAPER_CONTEXT_V4 (injected by run_reviewer).
REVIEWER_PROMPTS = {
    "narrative": (
        "You are the Narrative Reviewer for the v4 CampusRide paper. Evaluate whether the 7-beat "
        "evidence chain provides a defensible, writing-ready structure for related-work prose and "
        "paper sections §2.1, §2.2, §2.3, §4.1, §4.2, §5, §7.2. "
        "The paper has motivation beats (1-2 = small-town transport gap + grassroots/super-app), "
        "a framework beat (3 = four design primitives), a primary evidence line (4-5 = formative "
        "survey passenger and driver sides), a core-contribution artifact beat (6 = CampusRide "
        "platform with carpool deep-dive), and an adversarial scoping beat (7 = algorithmic "
        "management critique + sample skew + no deployment). "
        "IMPORTANT: Beats 4 and 6 are primary_data / artifact beats; they legitimately use "
        "pseudo-anchors ('local:CornellCarpoolSurvey2026', 'local:CampusRideSystem2026'). Do NOT "
        "penalize them for lacking a real literature anchor. "
        "Score based on: "
        "(1) each literature beat has a clear anchor paper and 3-6 spine items in citation or "
        "thematic order, (2) transitions between spine items are justified, (3) motivation beats "
        "do not serve as the direct evidence base for the primary survey findings, (4) weak beats "
        "(2, 5, 6, 7) explicitly admit their limitations rather than forcing certainty, (5) the "
        "overall 7-beat structure reads as a coherent, scoped argument tied to the three "
        "contribution claims. "
        "Do NOT penalize beats for having thin evidence if the pipeline honestly flags the weakness. "
        "Output STRICT JSON: {\"beat\": N, \"narrative_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"weakest_link\": \"...\", \"suggested_fix\": \"...\"}"
    ),
    "contradiction": (
        "You are the Contradiction Reviewer for the v4 CampusRide paper. Evaluate whether the "
        "pipeline surfaced the strongest counterevidence and scope tensions against the thesis, and "
        "whether those tensions are explicitly acknowledged. "
        "Expected focus questions: F1 Gap vs. Substitute (small-town transport), F2 Grassroots "
        "Legitimacy (formalization risk), F3 .edu Trust Primitive, F4 Rating Fairness as "
        "independent design concern, F5 Gamification Risk (overjustification / gaming). "
        "Check that contradictions are correctly attributed by argument line (motivation / "
        "framework / primary / core_contribution / adversarial / cross-line). "
        "Do not reward rhetorical confidence; reward honest exposure of disagreement and "
        "concrete handling advice. Beat 7 adversarial scoping should cite at least 3-5 "
        "critical contradictions / scope limiters. "
        "Output STRICT JSON: {\"contradiction_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"contradictions_found\": [...], \"verdict\": \"...\"}"
    ),
    "gap": (
        "You are the Gap Reviewer for the v4 CampusRide paper. Evaluate whether the gap / "
        "evidence analysis honestly distinguishes supported beats from unsupported beats across "
        "the 7-beat structure. The gap output is diagnostic, not a novelty-sales pitch. "
        "Reward accurate identification of missing literature, weak evidence chains, and "
        "overclaim risk. Specifically check: "
        "(a) Beat 2 super-app / integrated-platform literature is thin — framed as 'initial "
        "inquiry' not 'established design space', "
        "(b) Beat 5 driver-side observation (F5, N=30) is not over-generalized to all peer "
        "rating systems, "
        "(c) Beat 6 does NOT confuse deployment with validated downstream evaluation, "
        "(d) Beat 7 honestly surfaces algorithmic management critique as real scope limiters. "
        "Do NOT reward gap claims that reach beyond the 10-category A-J corpus. "
        "Output STRICT JSON: {\"gap_credibility_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"closest_existing_work\": [...], \"gap_refinement_suggestion\": \"...\", \"risk_assessment\": \"Low/Medium/High\"}"
    ),
    "coverage": (
        "You are the Coverage Checker for the v4 CampusRide paper. Evaluate coverage against the "
        "migrated v4 7-beat structure and A-J 10-category taxonomy (K from the prior L_auth run "
        "has been removed; do NOT expect K coverage). "
        "Beats 4 and 6 are primary_data / artifact beats with no required category support — "
        "evaluate the contextualizing literature only, not as if Beat 4/6 need full category spines. "
        "Count papers per category (A-J), compare with targets, and judge whether each of the 7 "
        "beats has enough credible support for its current rhetorical role. Penalize heavy X "
        "spillover, empty categories, and single-paper beats. "
        "Highest-priority active targets: A:8, B:10, F:10, H:10, J:10. C:8, D:8, I:8 are thin "
        "coverage targets that may need Lens supplement. E:8, G:8 should remain strong. "
        "If a paper was retrieved for a target category and retains that target as a secondary "
        "category, treat it as partial coverage evidence rather than a total miss. "
        "Output STRICT JSON: {\"coverage_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"category_counts\": {...}, \"underfilled\": [...], \"补搜_queries\": [...]}"
    ),
    "honesty": (
        "You are the Honesty Reviewer for the v4 CampusRide paper. Check whether the final "
        "evidence outputs stay within what the corpus and the N=117 formative survey actually "
        "support. Key checks (aligned with the paper's verb discipline table): "
        "(1) Beat 1: frame small-town transport gap as motivated / documented, NOT empirically "
        "quantified at scale. "
        "(2) Beat 2: grassroots coordination is documented; super-app literature is sparser and "
        "should be framed as 'initial inquiry'. Do NOT claim CampusRide is the first multi-module "
        "campus platform. "
        "(3) Beat 3: four design primitives are presented as parallel, NOT value-ranked. "
        "(4) Beats 4-5: descriptive statistics only. No 'significantly', no inferential claims. "
        "82% Mandarin-native is disclosed as scope, not masked as bias. F5 rating-fairness "
        "observation at N=30 'resonates with' not 'replicates' algorithmic management literature. "
        "(5) Beat 6: platform is DESIGNED and IMPLEMENTED, not validated. Each design decision "
        "must reference a survey finding (F3/F4/F5). Six-module claim acknowledges only carpool "
        "is deep-dived. Use 'we designed' / 'motivated by' / 'in response to finding X'; "
        "flag any use of 'effective', 'successful', 'proves', 'validates'. "
        "(6) Beat 7: each adversarial paragraph must cite at least one counterevidence paper; "
        "use 'may reproduce', 'we acknowledge', 'scope-limited'. Flag any 'we address', "
        "'we prevent', 'we solve'. "
        "Penalize extrapolation from indirect papers, unsupported causal leaps, and claims that "
        "ignore contradictions. "
        "Output STRICT JSON: {\"honesty_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"overselling_detected\": [...], \"what_author_should_admit\": \"...\"}"
    ),
}

REVIEW_WEIGHTS = {
    "narrative": 0.25,
    "contradiction": 0.15,
    "gap": 0.20,
    "coverage": 0.25,
    "honesty": 0.15,
}

SCORE_KEYS = {
    "narrative": "narrative_score",
    "contradiction": "contradiction_score",
    "gap": "gap_credibility_score",
    "coverage": "coverage_score",
    "honesty": "honesty_score",
}


# ---------------------------------------------------------------------------
# Data-driven scoring (no LLM needed)
# ---------------------------------------------------------------------------

def count_papers_per_category(classified: list[dict]) -> dict[str, int]:
    """Count papers in each category."""
    classified = filter_active_papers(classified)
    counts = Counter()
    for p in classified:
        cat = p.get("primary_category", "X")
        if cat != "X":
            counts[cat] += 1
    return dict(counts)


def count_strong_papers(classified: list[dict], beat: int) -> int:
    """Count strong-support papers in a beat's categories.

    Manual overrides are treated as strong evidence because they reflect
    explicit post-classification curation for required anchors.
    """
    classified = filter_active_papers(classified)
    cats = BEAT_CATEGORIES.get(beat, [])
    return sum(
        1 for p in classified
        if p.get("primary_category") in cats
        and p.get("confidence") in ("high", "medium", "manual")
    )


def count_empty_categories(classified: list[dict]) -> int:
    """Count how many of A-J have zero papers."""
    counts = count_papers_per_category(classified)
    return sum(1 for cat in CATEGORY_SEQUENCE if counts.get(cat, 0) == 0)


def compute_data_scores(classified: list[dict]) -> dict:
    """Compute data-driven scores (no LLM calls)."""
    classified = filter_active_papers(classified)
    counts = count_papers_per_category(classified)
    beat_support_counts = {
        str(beat): count_strong_papers(classified, beat)
        for beat in range(1, NUM_BEATS + 1)
    }

    # Evidence coverage: how many beats have ≥ 5 strong papers
    evidence_coverage = sum(
        1 for beat, strong_count in beat_support_counts.items()
        if strong_count >= 5
    )

    # Category balance: empty categories (lower is better)
    empty = count_empty_categories(classified)

    # Category fill rate: average % of target met
    fill_rates = []
    for cat, target in CATEGORY_TARGETS.items():
        actual = counts.get(cat, 0)
        fill_rates.append(min(actual / target, 1.0))
    avg_fill = sum(fill_rates) / len(fill_rates) if fill_rates else 0

    return {
        "evidence_coverage": evidence_coverage,
        "beat_support_counts": beat_support_counts,
        "category_balance": empty,
        "empty_categories": empty,
        "all_categories_populated": empty == 0,
        "category_counts": counts,
        "avg_fill_rate": round(avg_fill, 3),
        "total_papers": sum(counts.values()),
        "x_papers": sum(1 for p in classified if p.get("primary_category", "X") == "X"),
        "x_ratio": round(sum(1 for p in classified if p.get("primary_category", "X") == "X") / max(len(classified), 1), 3),
    }


# ---------------------------------------------------------------------------
# LLM-based reviewer scoring (Phase 5)
# ---------------------------------------------------------------------------

def run_reviewer(client, reviewer_name: str, base_dir: str) -> dict:
    """Run a single reviewer agent and return its JSON output."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    analysis_dir = os.path.join(base_dir, "analysis")

    # Build context for the reviewer
    classified = filter_active_papers(load_json(os.path.join(proc_dir, "classified.json")))
    ranked_classified = sorted(classified, key=lambda x: x.get("citationCount", 0), reverse=True)
    data_scores = compute_data_scores(classified)
    paper_title_lookup = {
        p.get("paperId", ""): p.get("title", "")
        for p in classified
        if p.get("paperId")
    }

    context_parts = [
        PAPER_CONTEXT_V4,
        "Evaluation standard: honest failure is better than false completion. "
        "Gap outputs are diagnostic; do not reward speculative novelty claims.",
        f"Corpus: {len(classified)} classified papers.",
        _format_data_scores_context(data_scores),
    ]

    # Category counts
    counts = count_papers_per_category(classified)
    context_parts.append(f"Category counts: {json.dumps(counts)}")

    # Load optional data
    for fname, label in [
        ("narrative_chains.json", "Narrative chains"),
        ("contradictions.json", "Contradictions"),
        ("gaps_ranked.json", "Gap analysis"),
        ("evidence_inventory.json", "Evidence inventory"),
        ("consensus_claim_checks.json", "Consensus claim checks"),
    ]:
        path = os.path.join(analysis_dir, fname)
        if os.path.exists(path):
            data = load_json(path)
            if reviewer_name == "contradiction" and fname == "contradictions.json":
                text = _build_contradiction_reviewer_context(data)
            elif fname == "narrative_chains.json" and reviewer_name in ("narrative", "gap", "honesty"):
                text = _build_narrative_reviewer_context(data, paper_title_lookup)
            elif fname == "gaps_ranked.json" and reviewer_name in ("gap", "honesty", "narrative"):
                text = _build_gap_reviewer_context(data)
            elif fname == "evidence_inventory.json" and reviewer_name in ("narrative", "gap", "honesty"):
                text = _build_evidence_inventory_reviewer_context(data, paper_title_lookup)
            else:
                # Truncate to avoid token overflow
                text = json.dumps(data, ensure_ascii=False)[:3000]
            context_parts.append(f"{label}:\n{text}")

    # Sample papers for narrative/contradiction reviewers
    if reviewer_name in ("narrative", "contradiction", "gap", "honesty"):
        sample = ranked_classified[:25]
        papers_text = json.dumps(
            [{"paperId": p["paperId"], "title": p.get("title", "")[:60],
              "category": p.get("primary_category", "X"),
              "key_claim": p.get("key_claim", p.get("one_sentence_contribution", ""))[:100],
              "year": p.get("year", 0)}
             for p in sample],
            ensure_ascii=False
        )
        context_parts.append(f"Sample papers:\n{papers_text}")

    context = "\n\n".join(context_parts)
    prompt = REVIEWER_PROMPTS[reviewer_name]

    model = REVIEWER_BRAINS.get(reviewer_name)

    try:
        raw = agent_run(client, role=prompt, task=context, model=model, max_tokens=2048)
        return _parse_reviewer_json(raw)
    except Exception as first_error:
        log.warning(f"Reviewer '{reviewer_name}' parse retry: {first_error}")
        retry_prompt = prompt + " Return minified JSON only. No prose, no markdown, no trailing commentary."
        compact_context = _compact_reviewer_context(context)
        try:
            raw = agent_run(client, role=retry_prompt, task=compact_context, model=model, max_tokens=1536)
            return _parse_reviewer_json(raw)
        except Exception as second_error:
            log.error(f"Reviewer '{reviewer_name}' failed after retry: {second_error}")
            return _fallback_review(reviewer_name, second_error)


def run_all_reviewers(client, base_dir: str) -> dict:
    """Run all 5 reviewers and return their results."""
    results = {}
    for name in REVIEW_WEIGHTS:
        log.info(f"  Running reviewer: {name}")
        result = run_reviewer(client, name, base_dir)
        results[name] = result
    return results


def extract_score(review: dict, reviewer_name: str) -> float | None:
    """Extract the score from a reviewer's output (different key names)."""
    key = SCORE_KEYS.get(reviewer_name, "score")
    val = review.get(key)
    if val is None:
        val = review.get("score")
    if isinstance(val, (int, float)):
        return float(val)
    return None


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------

def aggregate_reviews(reviews: dict) -> dict:
    """Aggregate 5 reviewer scores into overall score + disagreement detection.

    v4 tolerance: the gap/coverage axis is a known structural tension — gap
    reviewer measures thesis credibility, coverage measures corpus density.
    When gap > coverage by 0.30-0.35, it is DIAGNOSTIC (thesis is sound but
    corpus is thin), NOT malfunction. We only escalate to human when the
    disagreement exceeds 0.35 OR involves a non-gap/coverage pair.
    """
    scores = {}
    for name in REVIEW_WEIGHTS:
        s = extract_score(reviews.get(name, {}), name)
        scores[name] = s if s is not None else 0.0

    overall = sum(scores[k] * REVIEW_WEIGHTS[k] for k in REVIEW_WEIGHTS)

    # Disagreement detection with v4 tolerance.
    disagreements = []
    escalate_disagreements = []
    names = list(scores.keys())
    for i, a in enumerate(names):
        for b in names[i+1:]:
            diff = abs(scores[a] - scores[b])
            if diff <= 0.3:
                continue
            pair = tuple(sorted([a, b]))
            disagreements.append((a, b, round(diff, 3)))
            # gap/coverage structural tension up to 0.35 is acceptable for v4.
            if pair == ("coverage", "gap") and diff <= 0.35:
                continue
            escalate_disagreements.append((a, b, round(diff, 3)))

    weakest = min(scores, key=scores.get)

    return {
        "overall_score": round(overall, 3),
        "individual_scores": scores,
        "disagreements": disagreements,
        "needs_human_review": len(escalate_disagreements) > 0,
        "escalate_disagreements": escalate_disagreements,
        "weakest_dimension": weakest,
    }


# ---------------------------------------------------------------------------
# Auto-loop decision logic
# ---------------------------------------------------------------------------

def _has_placeholders(base_dir: str) -> bool:
    """Check whether fallback placeholders remain in key analysis artifacts."""
    analysis_dir = os.path.join(base_dir, "analysis")
    paths = [
        os.path.join(analysis_dir, "narrative_chains.json"),
        os.path.join(analysis_dir, "evidence_inventory.json"),
        os.path.join(analysis_dir, "gaps_ranked.json"),
        os.path.join(analysis_dir, "contradictions.json"),
    ]
    markers = ("fallback:", "no candidate paper found", "retry failed", "fallback warning")

    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            payload = json.dumps(load_json(path), ensure_ascii=False).lower()
        except Exception:
            continue
        if any(marker in payload for marker in markers):
            return True
    return False


def _adversarial_focus_covered(base_dir: str) -> bool:
    """Require the contradiction map to include the Category J adversarial focus with >=3 papers.

    v4 (CampusRide) drops K and concentrates adversarial scoping in Category J
    (algorithmic management / platform labor critique). Beat 7 success depends
    on this focus being populated.
    """
    path = os.path.join(base_dir, "analysis", "contradictions.json")
    if not os.path.exists(path):
        return False
    try:
        contradictions = load_json(path)
    except Exception:
        return False
    focus_summary = contradictions.get("focus_summary", [])
    for item in focus_summary:
        categories = item.get("categories", [])
        if "J" in categories and int(item.get("candidate_papers", item.get("count", 0)) or 0) >= 3:
            return True
    return False


def decide_action(aggregated: dict, base_dir: str | None = None, data_scores: dict | None = None) -> dict:
    """Based on scores, decide what to do next.

    Returns: {"action": "done|backtrack|human", "target_phase": "1|2|3|3.5|3.7", "reason": "..."}
    """
    score = aggregated["overall_score"]
    weakest = aggregated["weakest_dimension"]

    if aggregated["needs_human_review"]:
        return {
            "action": "human",
            "reason": f"Reviewer disagreement detected: {aggregated['disagreements']}. "
                      f"Human review needed before continuing.",
        }

    target_score = float(os.environ.get("TARGET_SCORE", "0.85"))
    if score >= target_score:
        # Also check honesty minimum
        honesty_min = float(os.environ.get("HONESTY_MIN", "0.80"))
        honesty_score = aggregated["individual_scores"].get("honesty", 0)
        if honesty_score < honesty_min:
            return {
                "action": "backtrack",
                "target_phase": "4",
                "weakest": "honesty",
                "score": honesty_score,
                "reason": f"Overall score {score} ≥ {target_score}, but honesty {honesty_score:.2f} < {honesty_min}. "
                          f"Backtracking to Phase 4 to reduce overselling.",
            }
        category_j_count = int((data_scores or {}).get("category_counts", {}).get("J", 0))
        if category_j_count < 3:
            return {
                "action": "backtrack",
                "target_phase": "1",
                "weakest": "coverage",
                "score": category_j_count,
                "reason": f"Overall score passes, but Category J (adversarial) active coverage is only {category_j_count}; need at least 3 papers before completion.",
            }
        if base_dir and not _adversarial_focus_covered(base_dir):
            return {
                "action": "backtrack",
                "target_phase": "3.7",
                "weakest": "contradiction",
                "score": aggregated["individual_scores"].get("contradiction", 0),
                "reason": "Overall score passes, but the Category J adversarial contradiction focus is not populated with enough evidence.",
            }
        if base_dir and _has_placeholders(base_dir):
            return {
                "action": "backtrack",
                "target_phase": "4",
                "weakest": "gap",
                "score": aggregated["individual_scores"].get("gap", 0),
                "reason": "Overall score passes, but fallback placeholders remain in analysis artifacts.",
            }
        return {"action": "done", "reason": f"Overall score {score} ≥ {target_score}. Pipeline complete."}

    # Map weakest dimension to phase to re-run
    phase_map = {
        "coverage": "1",          # Need more papers → re-search
        "narrative": "3.5",       # Narrative weak → re-run narrative chains
        "contradiction": "3.7",   # Contradictions unaddressed → re-run contradiction map
        "gap": "3",               # Gap not credible → re-run gap synthesis
        "honesty": "4",           # Over-claiming verbs / scope drift → re-run reports
    }

    target_phase = phase_map.get(weakest, "3")
    return {
        "action": "backtrack",
        "target_phase": target_phase,
        "weakest": weakest,
        "score": aggregated["individual_scores"][weakest],
        "reason": f"Weakest dimension: {weakest} ({aggregated['individual_scores'][weakest]:.2f}). "
                  f"Backtracking to Phase {target_phase}.",
    }


# ---------------------------------------------------------------------------
# Results tracking
# ---------------------------------------------------------------------------

def append_results_tsv(base_dir: str, iteration: int, aggregated: dict, action: dict):
    """Append a row to results.tsv for tracking iterations."""
    tsv_path = os.path.join(base_dir, "results.tsv")
    header = "iteration\toverall\tnarrative\tcontradiction\tgap\tcoverage\thonesty\tweakest\taction\n"

    if not os.path.exists(tsv_path):
        with open(tsv_path, "w") as f:
            f.write(header)

    scores = aggregated["individual_scores"]
    row = (
        f"{iteration}\t"
        f"{aggregated['overall_score']}\t"
        f"{scores.get('narrative', 0)}\t"
        f"{scores.get('contradiction', 0)}\t"
        f"{scores.get('gap', 0)}\t"
        f"{scores.get('coverage', 0)}\t"
        f"{scores.get('honesty', 0)}\t"
        f"{aggregated['weakest_dimension']}\t"
        f"{action.get('action', '?')}\n"
    )
    with open(tsv_path, "a") as f:
        f.write(row)


def _compact_reviewer_context(context: str, limit: int = 5000) -> str:
    """Trim reviewer context for retry runs."""
    normalized = re.sub(r"\n{3,}", "\n\n", context).strip()
    return normalized[:limit]


def _format_data_scores_context(data_scores: dict) -> str:
    counts = data_scores.get("category_counts", {}) or {}
    if counts:
        high_cat, high_count = max(counts.items(), key=lambda item: item[1])
        low_cat, low_count = min(counts.items(), key=lambda item: item[1])
        spread = f"category_range={high_cat}:{high_count} to {low_cat}:{low_count}"
    else:
        spread = "category_range=unavailable"

    empty = data_scores.get("empty_categories", data_scores.get("category_balance", "?"))
    empty_note = "all A-J populated" if empty == 0 else f"{empty} empty categories"
    return (
        "Data summary: "
        f"evidence_coverage={data_scores.get('evidence_coverage', '?')}/{NUM_BEATS}; "
        f"beat_support_counts={data_scores.get('beat_support_counts', {})}; "
        f"empty_categories={empty} ({empty_note}); "
        f"avg_fill_rate={data_scores.get('avg_fill_rate', '?')}; "
        f"total_papers={data_scores.get('total_papers', '?')}; "
        f"x_ratio={data_scores.get('x_ratio', '?')}; "
        f"{spread}."
    )


def _build_narrative_reviewer_context(data: list[dict], paper_title_lookup: dict[str, str], limit: int = 7000) -> str:
    """Summarize all beats so reviewers do not only see the first truncated beats."""
    if not isinstance(data, list):
        return json.dumps(data, ensure_ascii=False)[:limit]

    beat_map = {}
    for beat in data:
        if not isinstance(beat, dict):
            continue
        beat_num = beat.get("beat", "?")
        beat_map[beat_num] = beat

    lines = ["Narrative structure summary:"]
    if beat_map:
        lines.append(
            "Beats 1-2 motivate the problem, Beat 3 defines the framework, "
            "Beats 4-5 carry the primary evidence line, Beat 6 presents deployed infrastructure, "
            "and Beat 7 narrows causal claims by surfacing genuine competing mechanisms."
        )

    beat6 = beat_map.get(6)
    beat7 = beat_map.get(7)
    if isinstance(beat6, dict) and isinstance(beat7, dict):
        beat6_notes = re.sub(r"\s+", " ", str(beat6.get("writing_notes", "")).strip())[:180]
        beat7_notes = re.sub(r"\s+", " ", str(beat7.get("writing_notes", "")).strip())[:220]
        lines.append(
            "Critical bridge 6->7: Beat 6 is feasibility/requirements only, so Beat 7 must explicitly state "
            "that downstream gains cannot be attributed to provenance alone because inference-time scaling, "
            "structured deliberation, supervision, and steering remain live alternatives."
        )
        if beat6_notes:
            lines.append(f"Beat 6 scope note={beat6_notes}")
        if beat7_notes:
            lines.append(f"Beat 7 scope note={beat7_notes}")

    lines.append("Beat roster:")
    for beat_num in range(1, NUM_BEATS + 1):
        beat = beat_map.get(beat_num)
        if not isinstance(beat, dict):
            lines.append(f"Beat {beat_num} missing from narrative output.")
            continue

        beat_name = beat.get("beat_name", "Unknown beat")
        line = beat.get("argument_line", "unknown")
        anchor = beat.get("anchor_paper", {}) or {}
        anchor_id = anchor.get("paperId", "")
        anchor_title = paper_title_lookup.get(anchor_id, anchor_id) or anchor_id
        anchor_why = re.sub(r"\s+", " ", str(anchor.get("why", "")).strip())[:160]
        spine = beat.get("spine", []) or []
        supporting = beat.get("supporting", []) or []
        paragraphs = beat.get("paragraph_outline", []) or []

        spine_titles = []
        transitions = []
        for item in spine[:3]:
            pid = item.get("paperId", "")
            title = paper_title_lookup.get(pid, pid)
            title = re.sub(r"\s+", " ", str(title).strip())[:48]
            if title:
                spine_titles.append(title)
            transition = re.sub(r"\s+", " ", str(item.get("transition_to_next", "")).strip())[:90]
            if transition:
                transitions.append(transition)

        notes = re.sub(r"\s+", " ", str(beat.get("writing_notes", "")).strip())
        note_limit = 160 if beat_num in (6, 7) else 110
        roster_line = (
            f"Beat {beat_num} [{line}] {beat_name} | anchor={anchor_title[:72]} | "
            f"spine={len(spine)} support={len(supporting)} paragraphs={len(paragraphs)}"
        )
        lines.append(roster_line)
        if spine_titles:
            lines.append("  chain=" + " -> ".join(spine_titles))
        if anchor_why and beat_num in (6, 7):
            lines.append(f"  anchor_why={anchor_why}")
        if transitions:
            transition_limit = 2 if beat_num in (1, 2, 3, 4, 5) else 3
            lines.append("  transitions=" + " | ".join(transitions[:transition_limit]))
        if paragraphs and beat_num in (5, 6, 7):
            topics = [re.sub(r"\s+", " ", str(p.get('topic', '')).strip())[:70] for p in paragraphs[:2]]
            lines.append("  paragraph_topics=" + " | ".join(t for t in topics if t))
        if notes:
            lines.append(f"  writing_notes={notes[:note_limit]}")

    text = "\n".join(lines).strip()
    return text[:limit] if text else json.dumps(data, ensure_ascii=False)[:limit]


def _build_gap_reviewer_context(data: dict, limit: int = 5000) -> str:
    """Compact all-beat gap summary for reviewers."""
    beats = data.get("beats", [])
    if not isinstance(beats, list):
        return json.dumps(data, ensure_ascii=False)[:limit]

    lines = []
    for beat in beats:
        if not isinstance(beat, dict):
            continue
        lines.append(
            f"Beat {beat.get('beat', '?')} {beat.get('name', 'Unknown')} | "
            f"status={beat.get('status', 'unknown')} | "
            f"supporting_papers={beat.get('supporting_papers', 0)}"
        )
        weakness = re.sub(r"\s+", " ", str(beat.get("weakness", "")).strip())
        if weakness:
            lines.append(f"  weakness={weakness[:220]}")
        chain = beat.get("evidence_chain", []) or []
        if chain:
            lines.append("  chain=" + " | ".join(re.sub(r"\s+", " ", str(item).strip())[:120] for item in chain[:4]))

    overall = re.sub(r"\s+", " ", str(data.get("overall_assessment", "")).strip())
    if overall:
        lines.append(f"Overall assessment={overall[:320]}")

    text = "\n".join(lines).strip()
    return text[:limit] if text else json.dumps(data, ensure_ascii=False)[:limit]


def _build_evidence_inventory_reviewer_context(data: dict, paper_title_lookup: dict[str, str], limit: int = 5000) -> str:
    """Compact evidence inventory so later beats remain visible to reviewers."""
    inventory = data.get("evidence_inventory", [])
    if not isinstance(inventory, list):
        return json.dumps(data, ensure_ascii=False)[:limit]

    beat_map = {}
    for beat in inventory:
        if not isinstance(beat, dict):
            continue
        beat_num = beat.get("beat", "?")
        beat_map[beat_num] = beat

    lines = ["Evidence inventory summary:"]
    beat7 = beat_map.get(7)
    if isinstance(beat7, dict):
        lines.append(
            "Beat 7 must stay visible here because it is an adversarial scoping beat: the point is to show "
            "live alternative mechanisms, not to balance the thesis rhetorically."
        )

    for beat_num in range(1, NUM_BEATS + 1):
        beat = beat_map.get(beat_num)
        if not isinstance(beat, dict):
            lines.append(f"Beat {beat_num} missing from evidence inventory.")
            continue

        lines.append(
            f"Beat {beat.get('beat', '?')} {beat.get('title', 'Unknown')} | "
            f"core_papers={len(beat.get('core_papers', []) or [])}"
        )
        core_titles = []
        for item in (beat.get("core_papers", []) or [])[:4]:
            if not isinstance(item, dict):
                continue
            pid = item.get("paperId", "")
            core_titles.append(paper_title_lookup.get(pid, item.get("title", pid)))
        if core_titles:
            lines.append("  core=" + " | ".join(re.sub(r"\s+", " ", str(t).strip())[:80] for t in core_titles))
        narrative = re.sub(r"\s+", " ", str(beat.get("narrative", "")).strip())
        if narrative:
            note_limit = 240 if beat_num in (6, 7) else 140
            lines.append(f"  narrative={narrative[:note_limit]}")
        gaps = [
            g for g in (beat.get("remaining_gaps", []) or [])
            if "schema" not in str(g).lower()
            and "fallback" not in str(g).lower()
            and "retry" not in str(g).lower()
        ]
        if gaps:
            gap_limit = 180 if beat_num == 7 else 120
            lines.append("  remaining_gaps=" + " | ".join(re.sub(r"\s+", " ", str(g).strip())[:gap_limit] for g in gaps[:2]))

    text = "\n".join(lines).strip()
    return text[:limit] if text else json.dumps(data, ensure_ascii=False)[:limit]


def _build_contradiction_reviewer_context(data: dict, limit: int = 6000) -> str:
    """Provide contradiction reviewer a compact but representative cross-focus summary."""
    review_summary = data.get("review_summary", {})
    focus_summary = data.get("focus_summary", [])
    contradictions = data.get("contradictions", [])

    lines = []

    limiters = review_summary.get("must_address_limiters", [])
    if limiters:
        lines.append("Top thesis limiters:")
        for idx, item in enumerate(limiters[:6], start=1):
            lines.append(
                f"{idx}. [{item.get('source_question', 'N/A')}] "
                f"{item.get('question', 'N/A')} | handling={item.get('handling', 'N/A')}"
            )

    if focus_summary:
        lines.append("Focus coverage:")
        for item in focus_summary[:8]:
            lines.append(
                f"- categories={item.get('categories', [])} "
                f"count={item.get('count', 0)} "
                f"focus={item.get('focus_question', 'N/A')}"
            )
            stance_labels = item.get("stance_labels", {})
            stance_counts = item.get("stance_counts", {})
            if stance_labels and stance_counts:
                lines.append(
                    "  stance_balance="
                    f"{stance_labels.get('side_a', 'side_a')}:{stance_counts.get('side_a', 0)}, "
                    f"{stance_labels.get('side_b', 'side_b')}:{stance_counts.get('side_b', 0)}, "
                    f"{stance_labels.get('ambiguous', 'ambiguous')}:{stance_counts.get('ambiguous', 0)}"
                )

    line_coverage = review_summary.get("line_coverage", [])
    if line_coverage:
        lines.append("Argument-line coverage:")
        for item in line_coverage[:6]:
            lines.append(
                f"- {item.get('label', 'N/A')} | count={item.get('count', 0)} | "
                f"focuses={item.get('source_questions', [])} | "
                f"representative={item.get('representative_question', 'N/A')}"
            )

    tensions = review_summary.get("unresolved_tensions") or data.get("unresolved_tensions") or []
    if tensions:
        lines.append("Unresolved tensions:")
        for item in tensions[:8]:
            lines.append(f"- {item}")

    structural_limitations = review_summary.get("structural_limitations") or data.get("structural_limitations") or []
    if structural_limitations:
        lines.append("Structural limitations:")
        for item in structural_limitations[:6]:
            lines.append(f"- {item}")

    if contradictions:
        lines.append("Representative contradictions:")
        for item in contradictions[:12]:
            lines.append(
                f"- line={item.get('argument_line', 'N/A')} | "
                f"{item.get('source_question', 'N/A')} | {item.get('type', 'N/A')} | "
                f"{item.get('paper_a', {}).get('paperId', 'N/A')} vs {item.get('paper_b', {}).get('paperId', 'N/A')} | "
                f"{item.get('question', 'N/A')} | handling={item.get('suggested_handling', 'N/A')[:260]}"
            )

    text = "\n".join(lines).strip()
    if text:
        return text[:limit]
    return json.dumps(data, ensure_ascii=False)[:limit]


def _parse_reviewer_json(raw: str) -> dict:
    """Parse reviewer output with lightweight repair attempts."""
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

    raise last_error or ValueError("Reviewer output did not contain a valid JSON object")


def _extract_balanced_json(text: str) -> str:
    """Return the first balanced JSON object/array substring if available."""
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
    """Trim trailing commentary after the last closer."""
    last = max(text.rfind("}"), text.rfind("]"))
    return text[:last + 1] if last != -1 else ""


def _close_unbalanced_json(text: str) -> str:
    """Append missing closing braces/brackets for mildly truncated output."""
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


def _fallback_review(reviewer_name: str, error: Exception) -> dict:
    """Return a contract-compliant conservative fallback review."""
    message = f"Fallback due to reviewer parse failure: {error}"
    score_key = SCORE_KEYS[reviewer_name]
    base = {
        score_key: 0.0,
        "checklist": [0, 0, 0, 0, 0],
        "error": str(error),
    }

    if reviewer_name == "narrative":
        base.update({"beat": 0, "weakest_link": message, "suggested_fix": "Retry reviewer with smaller context."})
    elif reviewer_name == "contradiction":
        base.update({"contradictions_found": [], "verdict": message})
    elif reviewer_name == "gap":
        base.update({"closest_existing_work": [], "gap_refinement_suggestion": message, "risk_assessment": "High"})
    elif reviewer_name == "coverage":
        base.update({"category_counts": {}, "underfilled": [], "补搜_queries": []})
    elif reviewer_name == "honesty":
        base.update({"overselling_detected": [message], "what_author_should_admit": "Reviewer parse failed; treat this as a conservative fallback."})
    return base
