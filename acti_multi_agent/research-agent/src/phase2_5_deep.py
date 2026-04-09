"""Phase 2.5: Deep Extraction — MinerU PDF→MD + Claude structured field extraction."""

from __future__ import annotations

import json
import logging
import os
import subprocess

from .api_client import agent_run_json, BRAIN_PHASE2_DEEP_EXTRACTOR
from .prompts import DEEP_EXTRACTOR
from .state_manager import complete_step, is_step_complete, update_step, save_state
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")

BATCH_SIZE = 8  # Smaller batches — extraction is heavier than classification


def run_phase2_5(state: dict, state_path: str, base_dir: str, client) -> dict:
    """Orchestrate Phase 2.5: MinerU convert + deep extraction."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    pdf_dir = os.path.join(base_dir, "data", "pdfs")
    md_dir = os.path.join(base_dir, "data", "markdown")
    classified_path = os.path.join(proc_dir, "classified.json")

    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return state

    classified = load_json(classified_path)
    papers = [p for p in classified if p.get("primary_category", "X") != "X"]
    total = len(papers)
    log.info(f"Phase 2.5: deep extraction for {total} papers")

    # Step 0: MinerU PDF → Markdown conversion (local, free)
    if not is_step_complete(state, "2.5", "mineru_convert"):
        log.info("=== Phase 2.5.0: MinerU PDF → Markdown ===")
        converted = _run_mineru_convert(papers, pdf_dir, md_dir)
        state = complete_step(state, state_path, "2.5", "mineru_convert", {
            "converted": converted,
        })
    else:
        log.info("MinerU conversion already done")

    # Step 1: Deep extraction via Claude
    if not is_step_complete(state, "2.5", "deep_extraction"):
        extracted = _run_deep_extraction(state, state_path, client, papers, proc_dir, md_dir)
        state = complete_step(state, state_path, "2.5", "deep_extraction", {
            "papers_extracted": len(extracted),
        })
    else:
        deep_path = os.path.join(proc_dir, "deep_extracted.json")
        extracted = load_json(deep_path) if os.path.exists(deep_path) else []
        log.info(f"Deep extraction already done, loaded {len(extracted)} papers")

    # Step 2: Merge back into classified.json
    if not is_step_complete(state, "2.5", "merge_deep"):
        log.info("=== Phase 2.5.2: Merging deep extraction into classified.json ===")
        _merge_deep_into_classified(classified, extracted, classified_path)
        state = complete_step(state, state_path, "2.5", "merge_deep")

    return state


def _run_mineru_convert(papers: list[dict], pdf_dir: str, md_dir: str) -> int:
    """Convert downloaded PDFs to clean Markdown using MinerU (local, no API cost).

    Only converts PDFs that exist in data/pdfs/ and don't already have markdown.
    """
    os.makedirs(md_dir, exist_ok=True)

    if not os.path.isdir(pdf_dir):
        log.info("  No PDF directory found — skipping MinerU (will use abstracts only)")
        return 0

    # Check if mineru is available
    try:
        subprocess.run(["mineru", "--version"], capture_output=True, check=True, timeout=10)
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        log.info("  MinerU not installed — skipping PDF conversion (pip install mineru)")
        return 0

    converted = 0
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    log.info(f"  Found {len(pdf_files)} PDFs to convert")

    for fname in pdf_files:
        paper_id = fname.replace(".pdf", "")
        md_file = os.path.join(md_dir, f"{paper_id}.md")
        if os.path.exists(md_file):
            continue

        pdf_path = os.path.join(pdf_dir, fname)
        try:
            result = subprocess.run(
                ["mineru", "-p", pdf_path, "-o", md_dir, "-b", "pipeline"],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode == 0:
                converted += 1
            else:
                log.warning(f"  MinerU failed for {fname}: {result.stderr[:100]}")
        except subprocess.TimeoutExpired:
            log.warning(f"  MinerU timeout for {fname}")
        except Exception as e:
            log.warning(f"  MinerU error for {fname}: {e}")

    log.info(f"  MinerU converted {converted} PDFs to Markdown")
    return converted


def _run_deep_extraction(state: dict, state_path: str, client,
                         papers: list[dict], proc_dir: str, md_dir: str) -> list[dict]:
    """Extract structured fields in batches via DEEP_EXTRACTOR agent.

    If MinerU markdown exists for a paper, use that instead of abstract.
    """
    deep_path = os.path.join(proc_dir, "deep_extracted.json")

    # Resume support
    start_idx = state["phases"]["2.5"]["steps"]["deep_extraction"].get("last_batch_index", 0)
    if start_idx > 0 and os.path.exists(deep_path):
        extracted = load_json(deep_path)
        log.info(f"Resuming deep extraction from index {start_idx} ({len(extracted)} already done)")
    else:
        extracted = []

    total = len(papers)
    for i in range(start_idx, total, BATCH_SIZE):
        batch = papers[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
        log.info(f"  Batch {batch_num}/{total_batches} (papers {i+1}-{min(i+BATCH_SIZE, total)})")

        batch_input = _format_batch_for_extraction(batch, md_dir)
        try:
            results = agent_run_json(
                client,
                role=DEEP_EXTRACTOR,
                task=f"Extract structured fields from these {len(batch)} papers:\n\n{batch_input}",
                model=BRAIN_PHASE2_DEEP_EXTRACTOR,
                max_tokens=4096,
            )
            if isinstance(results, list):
                extracted.extend(results)
            else:
                log.warning(f"  Unexpected response format for batch {batch_num}")
                for p in batch:
                    extracted.append({"paperId": p["paperId"], "method_type": "unknown",
                                      "key_claim": "", "error": "parse_failed"})
        except Exception as e:
            log.error(f"  Batch {batch_num} failed: {e}")
            for p in batch:
                extracted.append({"paperId": p["paperId"], "method_type": "unknown",
                                  "key_claim": "", "error": str(e)})

        # Save progress
        atomic_write_json(deep_path, extracted)
        update_step(state, "2.5", "deep_extraction", {"last_batch_index": i + BATCH_SIZE})
        save_state(state_path, state)

    log.info(f"Deep extraction complete: {len(extracted)} papers")
    return extracted


def _format_batch_for_extraction(papers: list[dict], md_dir: str) -> str:
    """Format papers for the DEEP_EXTRACTOR agent.

    Prefers MinerU markdown over abstract when available.
    """
    lines = []
    for i, p in enumerate(papers, 1):
        pid = p["paperId"]
        # Check for MinerU markdown
        md_content = None
        if md_dir and os.path.isdir(md_dir):
            # Try sanitized filename
            safe_id = pid.replace("/", "_").replace(":", "_")
            for candidate in [f"{safe_id}.md", f"{pid}.md"]:
                md_path = os.path.join(md_dir, candidate)
                if os.path.exists(md_path):
                    try:
                        with open(md_path, "r", encoding="utf-8") as f:
                            md_content = f.read()[:2000]  # Cap at 2000 chars
                    except Exception:
                        pass
                    break

        if md_content:
            text_source = f"full_text_markdown (MinerU):\n{md_content}"
        else:
            abstract = (p.get("abstract") or "")[:800]
            text_source = f"abstract: {abstract}"

        lines.append(
            f"--- Paper {i} ---\n"
            f"paperId: {pid}\n"
            f"title: {p.get('title', 'N/A')}\n"
            f"year: {p.get('year', 'N/A')}\n"
            f"venue: {p.get('venue', 'N/A')}\n"
            f"category: {p.get('primary_category', 'X')}\n"
            f"{text_source}\n"
        )
    return "\n".join(lines)


def _merge_deep_into_classified(classified: list[dict], extracted: list[dict],
                                 classified_path: str):
    """Merge deep extraction results back into classified.json."""
    by_id = {e["paperId"]: e for e in extracted if "paperId" in e}
    merged = 0
    for p in classified:
        pid = p.get("paperId", "")
        if pid in by_id:
            ext = by_id[pid]
            for field in ("method_type", "key_claim", "methodology", "limitation",
                          "what_it_does_NOT_address", "dataset_or_benchmark",
                          "theoretical_framework"):
                if field in ext:
                    p[field] = ext[field]
            merged += 1
    atomic_write_json(classified_path, classified)
    log.info(f"Merged deep extraction into {merged} papers in classified.json")
