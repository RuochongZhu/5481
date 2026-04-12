"""Scoring engine: 5-dimension evaluation + aggregator + auto-loop logic."""

from __future__ import annotations

import json
import logging
import os
import re
from collections import Counter

from .utils import load_json, atomic_write_json
from .api_client import REVIEWER_BRAINS, agent_run

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
        "You are the Narrative Reviewer. Evaluate whether the 5-beat evidence chain is readable and defensible "
        "as related-work prose, not whether the thesis is exciting. Score based on: coherent beat progression, "
        "clear anchor papers, justified transitions, minimal arbitrary paper drops, and whether weak beats are "
        "admitted instead of papered over. "
        "Output STRICT JSON: {\"beat\": N, \"narrative_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"weakest_link\": \"...\", \"suggested_fix\": \"...\"}"
    ),
    "contradiction": (
        "You are the Contradiction Reviewer. Evaluate whether the pipeline surfaced the strongest counterevidence "
        "and scope tensions against the fixed thesis, and whether those tensions are explicitly acknowledged. "
        "Do not reward rhetorical confidence; reward honest exposure of disagreement and concrete handling advice. "
        "Output STRICT JSON: {\"contradiction_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"contradictions_found\": [...], \"verdict\": \"...\"}"
    ),
    "gap": (
        "You are the Gap Reviewer. Evaluate whether the gap/evidence analysis honestly distinguishes supported "
        "beats from unsupported beats. The gap output is diagnostic, not a novelty-sales pitch. Reward accurate "
        "identification of missing literature, weak evidence chains, and overclaim risk. "
        "Output STRICT JSON: {\"gap_credibility_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"closest_existing_work\": [...], \"gap_refinement_suggestion\": \"...\", \"risk_assessment\": \"Low/Medium/High\"}"
    ),
    "coverage": (
        "You are the Coverage Checker. Count papers per category (A-J), compare with targets, and judge whether "
        "each beat has enough credible support to be argued. Penalize heavy X spillover, empty categories, and "
        "single-paper beats. Targets: A:30 B:17 C:12 D:22 E:22 F:17 G:12 H:12 I:12 J:12. "
        "Output STRICT JSON: {\"coverage_score\": 0.X, \"checklist\": [0/1,0/1,0/1,0/1,0/1], "
        "\"category_counts\": {...}, \"underfilled\": [...], \"补搜_queries\": [...]}"
    ),
    "honesty": (
        "You are the Honesty Reviewer. Check whether the final evidence outputs stay within what the corpus "
        "actually supports, especially for Beat 5 / platform claims. Penalize extrapolation from indirect papers, "
        "unsupported causal leaps, and claims that ignore contradictions or missing literature. "
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
    beat_support_counts = {
        str(beat): count_strong_papers(classified, beat)
        for beat in range(1, 6)
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
    classified = load_json(os.path.join(proc_dir, "classified.json"))
    ranked_classified = sorted(classified, key=lambda x: x.get("citationCount", 0), reverse=True)
    data_scores = compute_data_scores(classified)

    context_parts = [
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
        f"evidence_coverage={data_scores.get('evidence_coverage', '?')}/5; "
        f"beat_support_counts={data_scores.get('beat_support_counts', {})}; "
        f"empty_categories={empty} ({empty_note}); "
        f"avg_fill_rate={data_scores.get('avg_fill_rate', '?')}; "
        f"total_papers={data_scores.get('total_papers', '?')}; "
        f"x_ratio={data_scores.get('x_ratio', '?')}; "
        f"{spread}."
    )


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
        for item in contradictions[:10]:
            lines.append(
                f"- {item.get('source_question', 'N/A')} | {item.get('type', 'N/A')} | "
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
