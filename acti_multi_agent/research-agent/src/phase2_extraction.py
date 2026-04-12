"""Phase 2: Structured Extraction — Claude agent classification of papers."""

from __future__ import annotations

import json
import logging
import os
from .api_client import agent_run_json, BRAIN_PHASE2_CLASSIFIER
from .prompts import LITERATURE_SCANNER
from .state_manager import complete_step, is_step_complete, update_step, save_state
from .utils import atomic_write_json, load_json, stable_fingerprint

log = logging.getLogger("research_agent")

BATCH_SIZE = 10  # Papers per API call


def run_phase2(state: dict, state_path: str, base_dir: str, client) -> dict:
    """Orchestrate Phase 2. Resumable from last classified paper index."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    config_dir = os.path.join(base_dir, "config")
    manual_overrides = _load_manual_category_overrides(config_dir)
    # Prefer filtered corpus_200.json if available, else fall back to full corpus
    corpus_path = os.path.join(proc_dir, "corpus_200.json")
    if not os.path.exists(corpus_path):
        corpus_path = os.path.join(proc_dir, "corpus_unified.json")

    if not os.path.exists(corpus_path):
        log.error("No corpus file found. Run Phase 1 first.")
        return state

    corpus = load_json(corpus_path)
    total = len(corpus)
    log.info(f"Phase 2: classifying {total} papers")

    # Step 1: Classification
    if not is_step_complete(state, 2, "classification"):
        classified = _run_classification(state, state_path, client, corpus, proc_dir, manual_overrides)
        state = complete_step(state, state_path, 2, "classification", {
            "papers_classified": len(classified),
            "total_papers": total,
        })
    else:
        classified_path = os.path.join(proc_dir, "classified.json")
        classified = load_json(classified_path) if os.path.exists(classified_path) else []
        log.info(f"Classification already done, loaded {len(classified)} papers")

    # Step 2: Consistency check (optional second run)
    if not is_step_complete(state, 2, "consistency_check"):
        log.info("=== Phase 2.2: Consistency check ===")
        disagreements = _consistency_check(classified)
        rate = round(len(disagreements) / max(len(classified), 1) * 100, 1)
        state["phases"]["2"]["quality_check"] = {
            "na_rate": _compute_na_rate(classified),
            "disagreement_rate": rate,
            "passed": rate < 5.0,
        }
        if disagreements:
            atomic_write_json(os.path.join(proc_dir, "disagreements.json"), disagreements)
            log.warning(f"  {len(disagreements)} papers flagged for review ({rate}%)")
        state = complete_step(state, state_path, 2, "consistency_check", {
            "disagreement_count": len(disagreements),
            "disagreement_rate": rate,
        })

    return state


def _run_classification(state: dict, state_path: str, client, corpus: list[dict],
                        proc_dir: str, manual_overrides: dict[str, dict]) -> list[dict]:
    """Classify papers in batches via Literature Scanner agent."""
    classified_path = os.path.join(proc_dir, "classified.json")
    corpus_fingerprint = _corpus_fingerprint(corpus)
    step_state = state["phases"]["2"]["steps"]["classification"]
    stored_fingerprint = step_state.get("corpus_fingerprint")

    # Resume from last batch index
    start_idx = step_state.get("last_batch_index", 0)
    if (
        start_idx > 0
        and os.path.exists(classified_path)
        and stored_fingerprint == corpus_fingerprint
    ):
        classified = load_json(classified_path)
        log.info(f"Resuming classification from index {start_idx} ({len(classified)} already done)")
    else:
        classified = []
        if start_idx > 0 or os.path.exists(classified_path):
            if stored_fingerprint and stored_fingerprint != corpus_fingerprint:
                log.info("Corpus changed since previous classification run — restarting from scratch")
            else:
                log.info("Starting fresh classification run")
        update_step(state, 2, "classification", {
            "last_batch_index": 0,
            "corpus_fingerprint": corpus_fingerprint,
        })
        save_state(state_path, state)

    total = len(corpus)
    for i in range(start_idx, total, BATCH_SIZE):
        batch = corpus[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
        log.info(f"  Batch {batch_num}/{total_batches} (papers {i+1}-{min(i+BATCH_SIZE, total)})")

        # Prepare batch input
        batch_input = _format_batch_for_agent(batch)
        try:
            results = agent_run_json(
                client,
                role=LITERATURE_SCANNER,
                task=f"Classify the following {len(batch)} papers:\n\n{batch_input}",
                model=BRAIN_PHASE2_CLASSIFIER,
                max_tokens=4096,
            )
            if isinstance(results, list):
                # Merge classification results back into paper records
                results_by_id = {r["paperId"]: r for r in results if "paperId" in r}
                for paper in batch:
                    pid = paper["paperId"]
                    if pid in results_by_id:
                        paper.update(results_by_id[pid])
                    else:
                        paper["primary_category"] = "X"
                        paper["confidence"] = "low"
                classified.extend(batch)
            else:
                log.warning(f"  Unexpected response format, marking batch as uncategorized")
                for paper in batch:
                    paper["primary_category"] = "X"
                    paper["confidence"] = "low"
                classified.extend(batch)
        except Exception as e:
            log.error(f"  Batch {batch_num} failed: {e}")
            for paper in batch:
                paper["primary_category"] = "X"
                paper["confidence"] = "error"
            classified.extend(batch)

        _apply_manual_category_overrides(batch, manual_overrides)

        # Save progress after each batch
        atomic_write_json(classified_path, classified)
        update_step(state, 2, "classification", {
            "last_batch_index": i + BATCH_SIZE,
            "corpus_fingerprint": corpus_fingerprint,
        })
        save_state(state_path, state)

    log.info(f"Classification complete: {len(classified)} papers")
    return classified


def _load_manual_category_overrides(config_dir: str) -> dict[str, dict]:
    cfg_path = os.path.join(config_dir, "manual_category_overrides.json")
    if not os.path.exists(cfg_path):
        return {}

    cfg = load_json(cfg_path)
    overrides = {}
    for item in cfg.get("papers", []):
        pid = (item.get("paperId") or "").strip()
        category = (item.get("primary_category") or "").strip()
        if pid and category:
            overrides[pid] = {
                "primary_category": category,
                "reason": item.get("reason", "").strip(),
            }
    return overrides


def _apply_manual_category_overrides(papers: list[dict], overrides: dict[str, dict]):
    if not overrides:
        return

    applied = 0
    for paper in papers:
        pid = paper.get("paperId")
        if pid not in overrides:
            continue
        override = overrides[pid]
        original_primary = paper.get("primary_category")
        original_confidence = paper.get("confidence")
        paper["model_primary_category"] = original_primary
        paper["model_confidence"] = original_confidence
        paper["primary_category"] = override["primary_category"]
        paper["confidence"] = "manual"
        paper["manual_category_override"] = True
        paper["manual_override_reason"] = override.get("reason", "")
        secondary = paper.get("secondary_categories") or []
        if original_primary and original_primary != paper["primary_category"] and original_primary != "X":
            if original_primary not in secondary:
                secondary = [original_primary] + secondary
        paper["secondary_categories"] = secondary
        applied += 1

    if applied:
        log.info(f"  Applied {applied} manual category overrides")


def _corpus_fingerprint(corpus: list[dict]) -> str:
    """Fingerprint the current classification input to detect stale resumes."""
    signature = [
        {
            "paperId": p.get("paperId", ""),
            "canonical_id": p.get("canonical_id", ""),
            "title": p.get("title", ""),
            "abstract": p.get("abstract", ""),
            "year": p.get("year", 0),
            "venue": p.get("venue", ""),
            "query_category": p.get("query_category", ""),
        }
        for p in corpus
    ]
    return stable_fingerprint(signature)


def _format_batch_for_agent(papers: list[dict]) -> str:
    """Format a batch of papers as numbered entries for the agent."""
    lines = []
    for i, p in enumerate(papers, 1):
        abstract = (p.get("abstract") or "")[:500]  # Truncate long abstracts
        lines.append(
            f"--- Paper {i} ---\n"
            f"paperId: {p['paperId']}\n"
            f"retrieval_prior_category: {p.get('query_category', 'N/A')}\n"
            f"retrieval_score: {p.get('selection_score', 'N/A')}\n"
            f"matched_query: {(p.get('matched_query') or '')[:180]}\n"
            f"title: {p.get('title', 'N/A')}\n"
            f"year: {p.get('year', 'N/A')}\n"
            f"venue: {p.get('venue', 'N/A')}\n"
            f"citationCount: {p.get('citationCount', 0)}\n"
            f"abstract: {abstract}\n"
        )
    return "\n".join(lines)


def _consistency_check(classified: list[dict]) -> list[dict]:
    """Check for low-confidence or uncategorized papers."""
    flagged = []
    for p in classified:
        if p.get("primary_category") == "X":
            flagged.append({"paperId": p["paperId"], "reason": "uncategorized"})
        elif p.get("confidence") in ("low", "error"):
            flagged.append({"paperId": p["paperId"], "reason": f"confidence={p.get('confidence')}"})
    return flagged


def _compute_na_rate(classified: list[dict]) -> float:
    """Compute the rate of papers with missing key fields."""
    if not classified:
        return 0.0
    na_count = sum(
        1 for p in classified
        if not p.get("one_sentence_contribution") or not p.get("gap_it_leaves")
    )
    return round(na_count / len(classified) * 100, 1)
