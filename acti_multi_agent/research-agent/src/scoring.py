"""Scoring engine: 5-dimension evaluation + aggregator + auto-loop logic."""

from __future__ import annotations

import json
import logging
import os
from collections import Counter

from .utils import load_json, atomic_write_json
from .api_client import REVIEWER_BRAINS, agent_run_json

log = logging.getLogger("research_agent")

# Beat → category mapping
BEAT_CATEGORIES = {
    1: ["A", "B", "C"],
    2: ["D", "H"],
    3: ["D"],
    4: ["E", "F", "I", "J"],
    5: ["A", "G"],
}

# Target paper counts per category
CATEGORY_TARGETS = {
    "A": 30, "B": 17, "C": 12, "D": 22, "E": 22,
    "F": 17, "G": 12, "H": 12, "I": 12, "J": 12,
}

# Reviewer prompts (inline — these mirror the slash commands but as system prompts)
REVIEWER_PROMPTS = {
    "narrative": (
        "You are the Narrative Reviewer. You ONLY evaluate logical flow within each beat's paper chain. "
        "Score each beat 0-1 based on: temporal logic, clear problem establishment, gap-pointing conclusion, "
        "minimal dropped-in papers, readability for outsiders. "
        "Output STRICT JSON: {\"beat\": N, \"narrative_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"weakest_link\": \"...\", \"suggested_fix\": \"...\"}"
    ),
    "contradiction": (
        "You are Reviewer #2 — the hostile one. Find evidence AGAINST the thesis: "
        "'Web-scraped training data is degrading while physically-verified authentic human social behavioral data "
        "provides irreplaceable training signals.' "
        "Check if contradictions are acknowledged and rebutted. "
        "Output STRICT JSON: {\"contradiction_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"contradictions_found\": [...], \"verdict\": \"...\"}"
    ),
    "gap": (
        "You are the Methodologist. Verify the gap claim: "
        "'No study connects Gerstgrasser's accumulation principle to a concrete platform generating authentic "
        "behavioral data as a byproduct. No study quantifies authentic vs web-scraped data difference on social "
        "intelligence/reasoning tasks.' "
        "Output STRICT JSON: {\"gap_credibility_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"closest_existing_work\": [...], \"gap_refinement_suggestion\": \"...\", \"risk_assessment\": \"Low/Medium/High\"}"
    ),
    "coverage": (
        "You are the Coverage Checker. Count papers per category (A-J), check against targets: "
        "A:30 B:17 C:12 D:22 E:22 F:17 G:12 H:12 I:12 J:12. "
        "Output STRICT JSON: {\"coverage_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"category_counts\": {...}, \"underfilled\": [...], \"补搜_queries\": [...]}"
    ),
    "honesty": (
        "You are the Devil's Advocate for CampusGo. Check if Beat 5 is honest about limitations. "
        "GPS=strong? QR=strong? Rating=moderate? Chat=weak? Categories=indirect? "
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


# ---------------------------------------------------------------------------
# Data-driven scoring (no LLM needed)
# ---------------------------------------------------------------------------

def count_papers_per_category(classified: list[dict]) -> dict[str, int]:
    """Count papers in each category."""
    counts = Counter()
    for p in classified:
        cat = p.get("primary_category", "X")
        if cat != "X":
            counts[cat] += 1
    return dict(counts)


def count_strong_papers(classified: list[dict], beat: int) -> int:
    """Count papers with high confidence in a beat's categories."""
    cats = BEAT_CATEGORIES.get(beat, [])
    return sum(
        1 for p in classified
        if p.get("primary_category") in cats
        and p.get("confidence") in ("high", "medium")
    )


def count_empty_categories(classified: list[dict]) -> int:
    """Count how many of A-J have zero papers."""
    counts = count_papers_per_category(classified)
    return sum(1 for cat in "ABCDEFGHIJ" if counts.get(cat, 0) == 0)


def compute_data_scores(classified: list[dict]) -> dict:
    """Compute data-driven scores (no LLM calls)."""
    counts = count_papers_per_category(classified)

    # Evidence coverage: how many beats have ≥ 5 strong papers
    evidence_coverage = sum(
        1 for beat in range(1, 6)
        if count_strong_papers(classified, beat) >= 5
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
        "category_balance": empty,
        "category_counts": counts,
        "avg_fill_rate": round(avg_fill, 3),
        "total_papers": sum(counts.values()),
    }


# ---------------------------------------------------------------------------
# LLM-based reviewer scoring (Phase 5)
# ---------------------------------------------------------------------------

def run_reviewer(client, reviewer_name: str, base_dir: str) -> dict:
    """Run a single reviewer agent and return its JSON output."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    analysis_dir = os.path.join(base_dir, "analysis")

    # Build context for the reviewer
    classified = load_json(os.path.join(proc_dir, "classified.json"))

    context_parts = [f"Corpus: {len(classified)} classified papers."]

    # Category counts
    counts = count_papers_per_category(classified)
    context_parts.append(f"Category counts: {json.dumps(counts)}")

    # Load optional data
    for fname, label in [
        ("narrative_chains.json", "Narrative chains"),
        ("contradictions.json", "Contradictions"),
        ("gaps_ranked.json", "Gap analysis"),
        ("evidence_inventory.json", "Evidence inventory"),
    ]:
        path = os.path.join(analysis_dir, fname)
        if os.path.exists(path):
            data = load_json(path)
            # Truncate to avoid token overflow
            text = json.dumps(data, ensure_ascii=False)[:3000]
            context_parts.append(f"{label}:\n{text}")

    # Sample papers for narrative/contradiction reviewers
    if reviewer_name in ("narrative", "contradiction"):
        sample = classified[:30]  # Top 30 by position (already sorted by citations)
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

    try:
        result = agent_run_json(
            client, role=prompt, task=context,
            model=REVIEWER_BRAINS.get(reviewer_name), max_tokens=2048,
        )
        return result
    except Exception as e:
        log.error(f"Reviewer '{reviewer_name}' failed: {e}")
        return {"score": None, "error": str(e)}


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
    score_keys = {
        "narrative": "narrative_score",
        "contradiction": "contradiction_score",
        "gap": "gap_credibility_score",
        "coverage": "coverage_score",
        "honesty": "honesty_score",
    }
    key = score_keys.get(reviewer_name, "score")
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
    """Aggregate 5 reviewer scores into overall score + disagreement detection."""
    scores = {}
    for name in REVIEW_WEIGHTS:
        s = extract_score(reviews.get(name, {}), name)
        scores[name] = s if s is not None else 0.0

    overall = sum(scores[k] * REVIEW_WEIGHTS[k] for k in REVIEW_WEIGHTS)

    # Disagreement detection: any two reviewers differ by > 0.3
    disagreements = []
    names = list(scores.keys())
    for i, a in enumerate(names):
        for b in names[i+1:]:
            diff = abs(scores[a] - scores[b])
            if diff > 0.3:
                disagreements.append((a, b, round(diff, 3)))

    weakest = min(scores, key=scores.get)

    return {
        "overall_score": round(overall, 3),
        "individual_scores": scores,
        "disagreements": disagreements,
        "needs_human_review": len(disagreements) > 0,
        "weakest_dimension": weakest,
    }


# ---------------------------------------------------------------------------
# Auto-loop decision logic
# ---------------------------------------------------------------------------

def decide_action(aggregated: dict) -> dict:
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

    target_score = float(os.environ.get("TARGET_SCORE", "0.8"))
    if score >= target_score:
        return {"action": "done", "reason": f"Overall score {score} ≥ {target_score}. Pipeline complete."}

    # Map weakest dimension to phase to re-run
    phase_map = {
        "coverage": "1",          # Need more papers → re-search
        "narrative": "3.5",       # Narrative weak → re-run narrative chains
        "contradiction": "3.7",   # Contradictions unaddressed → re-run contradiction map
        "gap": "3",               # Gap not credible → re-run gap synthesis
        "honesty": "4",           # CampusGo overselling → re-run reports
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
