"""End-to-end pipeline: generate reports + run reviewer panel + summarize."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable

from .config import (
    N_VARIANTS,
    PROMPT_IDS,
    REPORT_CONCURRENCY,
    REPORTS_DIR,
    REVIEWER_IDS,
    REVIEWER_SCORES_DIR,
    RESULTS_DIR,
    VARIANT_DIR,
)
from .data_variants import build_variants, list_variants, load_variant
from .panel import run_panel
from .report_generator import generate_report, report_path


def _ensure_variants():
    if not list_variants():
        logging.info("no variants found, building...")
        build_variants()


def _setup_logging(verbosity: int = 0):
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def run_one(prompt_id: str, variant_index: int, *, resume: bool = True) -> dict:
    digest = load_variant(variant_index)
    variant_stem = digest["meta"]["variant_id"]
    md_path = generate_report(prompt_id, variant_index, skip_if_exists=resume)
    aggregate = run_panel(
        prompt_id=prompt_id,
        variant_id=variant_index,
        report_md_path=md_path,
        skip_if_exists=resume,
    )
    return aggregate


def run_pipeline(
    *,
    prompts: Iterable[str] = PROMPT_IDS,
    n_variants: int = N_VARIANTS,
    resume: bool = True,
) -> list[dict]:
    _ensure_variants()
    n_avail = len(list_variants())
    if n_variants > n_avail:
        logging.warning(
            "Requested %d variants but only %d available; using %d",
            n_variants, n_avail, n_avail,
        )
        n_variants = n_avail

    tasks = [(p, v) for p in prompts for v in range(n_variants)]
    aggregates: list[dict] = []
    print(f"Running {len(tasks)} (prompt × variant) jobs "
          f"({len(list(prompts))} prompts × {n_variants} variants)...",
          file=sys.stderr)

    with ThreadPoolExecutor(max_workers=REPORT_CONCURRENCY) as ex:
        future_to_task = {
            ex.submit(run_one, p, v, resume=resume): (p, v)
            for (p, v) in tasks
        }
        done = 0
        for fut in as_completed(future_to_task):
            (p, v) = future_to_task[fut]
            try:
                agg = fut.result()
                aggregates.append(agg)
                done += 1
                composite = agg["composite_score_0_10"]
                print(f"[{done}/{len(tasks)}] {p}/{agg['variant_id']} composite={composite:.2f}",
                      file=sys.stderr)
            except Exception as e:
                logging.exception("task failed for %s/v%d", p, v)
                done += 1
    return aggregates


def main():
    ap = argparse.ArgumentParser(description="Run the AI-report validation experiment.")
    ap.add_argument("--smoke", action="store_true",
                    help="Run only 2 variants per prompt (quick test).")
    ap.add_argument("--prompts", nargs="+", default=list(PROMPT_IDS),
                    help=f"Prompt IDs to use (default: {list(PROMPT_IDS)})")
    ap.add_argument("--n-variants", type=int, default=N_VARIANTS,
                    help=f"Number of variants per prompt (default: {N_VARIANTS})")
    ap.add_argument("--no-resume", action="store_true",
                    help="Re-generate / re-score even if outputs exist")
    ap.add_argument("-v", "--verbose", action="count", default=0)
    args = ap.parse_args()

    _setup_logging(args.verbose)
    n_variants = 2 if args.smoke else args.n_variants

    aggregates = run_pipeline(
        prompts=args.prompts,
        n_variants=n_variants,
        resume=not args.no_resume,
    )

    # Print summary
    print("\n=== SUMMARY ===")
    by_prompt: dict[str, list[float]] = {p: [] for p in args.prompts}
    for a in aggregates:
        by_prompt.setdefault(a["prompt_id"], []).append(a["composite_score_0_10"])
    for p in args.prompts:
        scores = by_prompt.get(p, [])
        if not scores:
            print(f"  {p}: no results")
            continue
        mean = sum(scores) / len(scores)
        mn, mx = min(scores), max(scores)
        print(f"  {p}: n={len(scores)}  mean={mean:.2f}  range={mn:.2f}-{mx:.2f}")

    # Write summary file
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = RESULTS_DIR / "pipeline_summary.json"
    summary_path.write_text(json.dumps(aggregates, indent=2), encoding="utf-8")
    print(f"\nWrote: {summary_path}")
    print(f"Reports:  {REPORTS_DIR}")
    print(f"Reviews:  {REVIEWER_SCORES_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
