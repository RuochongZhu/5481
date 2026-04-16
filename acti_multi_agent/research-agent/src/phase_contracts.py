"""Minimal completion contracts for phase outputs.

These validators enforce the current standard:
- artifacts must exist
- shape must meet a minimal schema
- placeholder error payloads do not count as completed work
"""

from __future__ import annotations

from typing import Iterable


REVIEWER_SCORE_KEYS = {
    "narrative": "narrative_score",
    "contradiction": "contradiction_score",
    "gap": "gap_credibility_score",
    "coverage": "coverage_score",
    "honesty": "honesty_score",
}


class PhaseContractError(RuntimeError):
    """Raised when a phase artifact fails the completion contract."""


def _raise(errors: list[str], label: str):
    if errors:
        raise PhaseContractError(f"{label} invalid: {'; '.join(errors)}")


def _is_nonempty_str(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _looks_like_error_placeholder(value) -> bool:
    if not isinstance(value, str):
        return False
    text = value.strip().lower()
    return text.startswith("error:") or text.startswith("failed:")


def _require_keys(data: dict, keys: Iterable[str], label: str, errors: list[str]):
    for key in keys:
        if key not in data:
            errors.append(f"{label} missing '{key}'")


def ensure_relationship_analysis_valid(result: dict):
    errors = []
    if not isinstance(result, dict):
        raise PhaseContractError("relationship analysis invalid: result is not an object")

    _require_keys(result, ("edges", "orphans", "notes"), "relationship analysis", errors)
    if not isinstance(result.get("edges"), list):
        errors.append("relationship analysis 'edges' must be a list")
    if not isinstance(result.get("orphans"), list):
        errors.append("relationship analysis 'orphans' must be a list")
    notes = result.get("notes")
    if not isinstance(notes, str):
        errors.append("relationship analysis 'notes' must be a string")
    elif _looks_like_error_placeholder(notes):
        errors.append(f"relationship analysis notes contains error placeholder: {notes}")

    for idx, edge in enumerate(result.get("edges", [])):
        if not isinstance(edge, dict):
            errors.append(f"edge #{idx} is not an object")
            continue
        _require_keys(edge, ("source", "target", "type", "evidence"), f"edge #{idx}", errors)

    _raise(errors, "relationship analysis")
    return result


def ensure_gap_analysis_valid(result: dict):
    errors = []
    if not isinstance(result, dict):
        raise PhaseContractError("gap synthesis invalid: result is not an object")

    beats = result.get("beats")
    if not isinstance(beats, list):
        errors.append("gap synthesis 'beats' must be a list")
        beats = []
    elif len(beats) != 7:
        errors.append(f"gap synthesis must contain exactly 7 beats, got {len(beats)}")

    field_observations = result.get("field_observations")
    if isinstance(field_observations, dict) and field_observations.get("error"):
        errors.append(f"gap synthesis error placeholder: {field_observations['error']}")

    overall = result.get("overall_assessment")
    if not _is_nonempty_str(overall):
        errors.append("gap synthesis missing non-empty 'overall_assessment'")

    for idx, beat in enumerate(beats):
        if not isinstance(beat, dict):
            errors.append(f"beat #{idx} is not an object")
            continue
        _require_keys(
            beat,
            ("beat", "name", "status", "supporting_papers", "evidence_chain"),
            f"beat #{idx}",
            errors,
        )
        if not isinstance(beat.get("evidence_chain"), list):
            errors.append(f"beat #{idx} 'evidence_chain' must be a list")

    _raise(errors, "gap synthesis")
    return result


def ensure_narrative_chains_valid(chains: list[dict]):
    if not isinstance(chains, list):
        raise PhaseContractError("narrative chains invalid: result is not a list")

    errors = []
    if len(chains) != 7:
        errors.append(f"narrative chains must contain exactly 7 beats, got {len(chains)}")

    valid_beats = 0
    hard_failures = []
    for idx, chain in enumerate(chains):
        if not isinstance(chain, dict):
            errors.append(f"beat #{idx} is not an object")
            continue
        _require_keys(chain, ("beat", "beat_name"), f"beat #{idx}", errors)

        chain_error = chain.get("error")
        if chain_error:
            if chain_error != "no_papers":
                hard_failures.append(f"beat {chain.get('beat', '?')}: {chain_error}")
            continue

        valid_beats += 1
        anchor = chain.get("anchor_paper")
        if not isinstance(anchor, dict) or not _is_nonempty_str(anchor.get("paperId")):
            errors.append(f"beat {chain.get('beat', '?')} missing valid anchor_paper.paperId")

        spine = chain.get("spine")
        if not isinstance(spine, list) or not spine:
            errors.append(f"beat {chain.get('beat', '?')} missing non-empty spine")
        paragraphs = chain.get("paragraph_outline")
        if not isinstance(paragraphs, list) or not paragraphs:
            errors.append(f"beat {chain.get('beat', '?')} missing non-empty paragraph_outline")

    if hard_failures:
        errors.append("narrative beat failures: " + " | ".join(hard_failures))
    if valid_beats == 0:
        errors.append("all narrative chains are placeholders")

    _raise(errors, "narrative chains")
    return chains


def ensure_contradictions_valid(result: dict):
    errors = []
    if not isinstance(result, dict):
        raise PhaseContractError("contradiction map invalid: result is not an object")

    contradictions = result.get("contradictions")
    if not isinstance(contradictions, list):
        errors.append("contradictions must be a list")
        contradictions = []
    total_found = result.get("total_found")
    if not isinstance(total_found, int):
        errors.append("'total_found' must be an integer")
    elif total_found != len(contradictions):
        errors.append(f"total_found={total_found} does not match contradictions={len(contradictions)}")
    if not isinstance(result.get("critical_count"), int):
        errors.append("'critical_count' must be an integer")
    if not isinstance(result.get("thesis_risk_assessments"), list):
        errors.append("'thesis_risk_assessments' must be a list")

    scan_errors = result.get("scan_errors", [])
    if not isinstance(scan_errors, list):
        errors.append("'scan_errors' must be a list when present")
    elif scan_errors:
        errors.append(
            "focus pair scan failures present: "
            + " | ".join(str(item.get("error", item)) for item in scan_errors[:5])
        )

    # Auto-fix: remove malformed contradictions instead of crashing
    cleaned = []
    for idx, item in enumerate(contradictions):
        if not isinstance(item, dict):
            continue
        valid = True
        for side in ("paper_a", "paper_b"):
            side_data = item.get(side)
            if not isinstance(side_data, dict) or not _is_nonempty_str(side_data.get("paperId")):
                valid = False
                break
        if valid:
            cleaned.append(item)

    if len(cleaned) < len(contradictions):
        removed = len(contradictions) - len(cleaned)
        result["contradictions"] = cleaned
        result["total_found"] = len(cleaned)
        result["critical_count"] = sum(1 for c in cleaned if c.get("severity") == "critical")
        # Don't error — just log the cleanup
        import logging
        logging.getLogger("research_agent").warning(
            f"Removed {removed} malformed contradiction(s) during validation"
        )

    _raise(errors, "contradiction map")
    return result


def ensure_evidence_inventory_valid(result: dict):
    errors = []
    if not isinstance(result, dict):
        raise PhaseContractError("evidence inventory invalid: result is not an object")

    if result.get("error"):
        errors.append(f"evidence inventory error placeholder: {result['error']}")

    inventory = result.get("evidence_inventory")
    if not isinstance(inventory, list):
        errors.append("'evidence_inventory' must be a list")
        inventory = []
    elif len(inventory) != 7:
        errors.append(f"evidence inventory must contain exactly 7 beats, got {len(inventory)}")

    outline = result.get("suggested_paper_outline")
    if not isinstance(outline, dict) or not outline:
        errors.append("'suggested_paper_outline' must be a non-empty object")

    for idx, beat in enumerate(inventory):
        if not isinstance(beat, dict):
            errors.append(f"inventory beat #{idx} is not an object")
            continue
        _require_keys(beat, ("beat", "title", "core_papers"), f"inventory beat #{idx}", errors)
        core_papers = beat.get("core_papers")
        if not isinstance(core_papers, list) or not core_papers:
            errors.append(f"inventory beat #{idx} must contain non-empty core_papers")

    _raise(errors, "evidence inventory")
    return result


def ensure_reviewer_results_valid(result: dict):
    errors = []
    if not isinstance(result, dict):
        raise PhaseContractError("reviewer results invalid: result is not an object")

    for reviewer, score_key in REVIEWER_SCORE_KEYS.items():
        review = result.get(reviewer)
        if not isinstance(review, dict):
            errors.append(f"reviewer '{reviewer}' missing or not an object")
            continue
        if review.get("error"):
            errors.append(f"reviewer '{reviewer}' failed: {review['error']}")
        score = review.get(score_key, review.get("score"))
        if not isinstance(score, (int, float)):
            errors.append(f"reviewer '{reviewer}' missing numeric score '{score_key}'")
        checklist = review.get("checklist")
        if checklist is not None and not isinstance(checklist, list):
            errors.append(f"reviewer '{reviewer}' checklist must be a list when present")

    _raise(errors, "reviewer results")
    return result


def ensure_evaluation_result_valid(result: dict):
    errors = []
    if not isinstance(result, dict):
        raise PhaseContractError("evaluation result invalid: result is not an object")

    if not isinstance(result.get("iteration"), int):
        errors.append("'iteration' must be an integer")
    if not isinstance(result.get("data_scores"), dict):
        errors.append("'data_scores' must be an object")

    aggregated = result.get("aggregated")
    if not isinstance(aggregated, dict):
        errors.append("'aggregated' must be an object")
        aggregated = {}
    individual_scores = aggregated.get("individual_scores")
    if not isinstance(individual_scores, dict):
        errors.append("'aggregated.individual_scores' must be an object")
    else:
        for reviewer in REVIEWER_SCORE_KEYS:
            score = individual_scores.get(reviewer)
            if not isinstance(score, (int, float)):
                errors.append(f"aggregated score missing for '{reviewer}'")
    if not isinstance(aggregated.get("overall_score"), (int, float)):
        errors.append("'aggregated.overall_score' must be numeric")
    weakest = aggregated.get("weakest_dimension")
    if weakest not in REVIEWER_SCORE_KEYS:
        errors.append(f"unexpected weakest_dimension: {weakest!r}")

    action = result.get("action")
    if not isinstance(action, dict):
        errors.append("'action' must be an object")
        action = {}
    if action.get("action") not in {"done", "backtrack", "human"}:
        errors.append(f"unexpected action: {action.get('action')!r}")
    if not _is_nonempty_str(action.get("reason")):
        errors.append("action missing non-empty 'reason'")

    _raise(errors, "evaluation result")
    return result
