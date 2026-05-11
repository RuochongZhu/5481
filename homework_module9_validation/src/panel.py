"""5-reviewer panel: runs all reviewers on a single report and aggregates."""
from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from .config import (
    REVIEWER_CONCURRENCY,
    REVIEWER_IDS,
    REVIEWER_SCORES_DIR,
    REVIEW_WEIGHTS,
    SCORE_KEY,
)
from .data_variants import load_variant
from .reviewer import review_report_file, score_path

log = logging.getLogger("hw_validator")


def run_panel(
    *,
    prompt_id: str,
    variant_id: int | str,
    report_md_path: Path,
    skip_if_exists: bool = True,
) -> dict[str, Any]:
    """Run all 5 reviewers on a report (in parallel). Return aggregate dict."""
    digest = load_variant(variant_id)
    variant_stem = digest["meta"]["variant_id"]

    if not report_md_path.exists():
        raise FileNotFoundError(f"report not found: {report_md_path}")

    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=REVIEWER_CONCURRENCY) as ex:
        future_to_id = {
            ex.submit(
                review_report_file,
                rid,
                prompt_id=prompt_id,
                variant_id=variant_id,
                report_path=report_md_path,
                skip_if_exists=skip_if_exists,
            ): rid
            for rid in REVIEWER_IDS
        }
        for fut in as_completed(future_to_id):
            rid = future_to_id[fut]
            try:
                out_path = fut.result()
                results[rid] = json.loads(out_path.read_text(encoding="utf-8"))
            except Exception as e:
                log.error("reviewer %s failed: %s", rid, e)
                results[rid] = {
                    "dimension": rid,
                    SCORE_KEY: 0.0,
                    "_parse_status": "exception",
                    "_error": str(e),
                }

    composite = aggregate_composite(results)
    aggregate = {
        "prompt_id": prompt_id,
        "variant_id": variant_stem,
        "composite_score_0_10": composite,
        "scores": {rid: results[rid].get(SCORE_KEY, 0.0) for rid in REVIEWER_IDS},
        "would_publish_votes": {
            rid: results[rid].get("would_publish", "conditional") for rid in REVIEWER_IDS
        },
        "weights": REVIEW_WEIGHTS,
    }
    aggregate_path = REVIEWER_SCORES_DIR / f"{prompt_id}__{variant_stem}__AGGREGATE.json"
    aggregate_path.parent.mkdir(parents=True, exist_ok=True)
    aggregate_path.write_text(json.dumps(aggregate, indent=2), encoding="utf-8")
    return aggregate


def aggregate_composite(results: dict[str, dict[str, Any]]) -> float:
    total = 0.0
    for rid, weight in REVIEW_WEIGHTS.items():
        score = float(results.get(rid, {}).get(SCORE_KEY, 0.0))
        total += weight * score
    return round(total, 3)


def load_all_aggregates() -> list[dict[str, Any]]:
    """Load every AGGREGATE.json under outputs/reviewer_scores/."""
    out = []
    for p in sorted(REVIEWER_SCORES_DIR.glob("*__AGGREGATE.json")):
        out.append(json.loads(p.read_text(encoding="utf-8")))
    return out


def load_all_reviewer_results() -> list[dict[str, Any]]:
    """Load every per-reviewer JSON (not the aggregates)."""
    out = []
    for p in sorted(REVIEWER_SCORES_DIR.glob("*.json")):
        if "AGGREGATE" in p.name:
            continue
        out.append(json.loads(p.read_text(encoding="utf-8")))
    return out
