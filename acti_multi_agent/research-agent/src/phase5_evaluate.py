"""Phase 5: Auto-Evaluate — run 5 reviewers, aggregate, decide next action."""

import json
import logging
import os

from .scoring import (
    run_all_reviewers, aggregate_reviews, decide_action,
    append_results_tsv, compute_data_scores,
)
from .state_manager import complete_step, is_step_complete
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")


def run_phase5(state: dict, state_path: str, base_dir: str, client,
               iteration: int = 1) -> dict:
    """Orchestrate Phase 5: evaluation + auto-loop decision."""
    analysis_dir = os.path.join(base_dir, "analysis")
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(analysis_dir, exist_ok=True)

    classified_path = os.path.join(proc_dir, "classified.json")
    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return state

    classified = load_json(classified_path)

    # Step 1: Data-driven scores (no LLM)
    if not is_step_complete(state, "5", "data_scores"):
        log.info("=== Phase 5.1: Data-driven scoring ===")
        data_scores = compute_data_scores(classified)
        atomic_write_json(os.path.join(analysis_dir, "data_scores.json"), data_scores)
        log.info(f"  Evidence coverage: {data_scores['evidence_coverage']}/5 beats")
        log.info(f"  Empty categories: {data_scores['category_balance']}")
        log.info(f"  Avg fill rate: {data_scores['avg_fill_rate']}")
        log.info(f"  Total papers: {data_scores['total_papers']}")
        state = complete_step(state, state_path, "5", "data_scores")
    else:
        data_scores = load_json(os.path.join(analysis_dir, "data_scores.json"))

    # Step 2: Run 5 LLM reviewers
    if not is_step_complete(state, "5", "reviewer_eval"):
        log.info("=== Phase 5.2: Running 5 reviewers ===")
        reviews = run_all_reviewers(client, base_dir)
        atomic_write_json(os.path.join(analysis_dir, "reviewer_results.json"), reviews)
        state = complete_step(state, state_path, "5", "reviewer_eval")
    else:
        reviews = load_json(os.path.join(analysis_dir, "reviewer_results.json"))

    # Step 3: Aggregate + decide
    if not is_step_complete(state, "5", "aggregate"):
        log.info("=== Phase 5.3: Aggregating scores ===")
        aggregated = aggregate_reviews(reviews)
        action = decide_action(aggregated)

        result = {
            "iteration": iteration,
            "data_scores": data_scores,
            "aggregated": aggregated,
            "action": action,
        }
        atomic_write_json(os.path.join(analysis_dir, "evaluation_result.json"), result)
        append_results_tsv(base_dir, iteration, aggregated, action)

        _print_evaluation(aggregated, action)
        state = complete_step(state, state_path, "5", "aggregate")
    else:
        result = load_json(os.path.join(analysis_dir, "evaluation_result.json"))
        action = result.get("action", {})
        aggregated = result.get("aggregated", {})
        _print_evaluation(aggregated, action)

    # Step 4: Generate evaluation report
    if not is_step_complete(state, "5", "eval_report"):
        log.info("=== Phase 5.4: Evaluation report ===")
        _generate_eval_report(result, base_dir)
        state = complete_step(state, state_path, "5", "eval_report")

    return state


def _print_evaluation(aggregated: dict, action: dict):
    """Print evaluation results to console."""
    scores = aggregated.get("individual_scores", {})
    overall = aggregated.get("overall_score", 0)

    log.info(f"\n{'='*50}")
    log.info(f"  EVALUATION RESULTS")
    log.info(f"{'='*50}")
    log.info(f"  Overall score: {overall:.3f}")
    log.info(f"  ─────────────────────────")
    for name, score in scores.items():
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        log.info(f"  {name:15s} {score:.2f} {bar}")
    log.info(f"  ─────────────────────────")
    log.info(f"  Weakest: {aggregated.get('weakest_dimension', '?')}")

    if aggregated.get("disagreements"):
        log.info(f"  ⚠ Reviewer disagreements: {aggregated['disagreements']}")

    act = action.get("action", "?")
    if act == "done":
        log.info(f"  ✅ {action['reason']}")
    elif act == "backtrack":
        log.info(f"  🔄 {action['reason']}")
    elif act == "human":
        log.info(f"  🛑 {action['reason']}")
    log.info(f"{'='*50}\n")


def _generate_eval_report(result: dict, base_dir: str):
    """Generate human-readable evaluation report."""
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    agg = result.get("aggregated", )
    action = result.get("action", {})
    data = result.get("data_scores", {})
    scores = agg.get("individual_scores", {})

    lines = ["# Evaluation Report\n"]
    lines.append(f"Iteration: {result.get('iteration', '?')}\n")
    lines.append(f"Overall score: **{agg.get('overall_score', 0):.3f}**\n")

    lines.append("## Dimension Scores\n")
    lines.append("| Dimension | Score | Weight |")
    lines.append("|-----------|-------|--------|")
    weights = {"narrative": 0.25, "contradiction": 0.15, "gap": 0.20,
               "coverage": 0.25, "honesty": 0.15}
    for name in weights:
        s = scores.get(name, 0)
        w = weights[name]
        lines.append(f"| {name} | {s:.2f} | {w:.0%} |")

    lines.append(f"\n## Data Metrics\n")
    lines.append(f"- Total papers: {data.get('total_papers', '?')}")
    lines.append(f"- Evidence coverage: {data.get('evidence_coverage', '?')}/5 beats")
    lines.append(f"- Empty categories: {data.get('category_balance', '?')}")
    lines.append(f"- Avg fill rate: {data.get('avg_fill_rate', '?')}")

    if agg.get("disagreements"):
        lines.append(f"\n## ⚠ Reviewer Disagreements\n")
        for a, b, diff in agg["disagreements"]:
            lines.append(f"- {a} vs {b}: Δ{diff}")

    lines.append(f"\n## Decision\n")
    lines.append(f"Action: **{action.get('action', '?')}**")
    lines.append(f"Reason: {action.get('reason', 'N/A')}")
    if action.get("target_phase"):
        lines.append(f"Target phase: {action['target_phase']}")

    report_path = os.path.join(output_dir, "evaluation_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.info(f"Evaluation report: {report_path}")
