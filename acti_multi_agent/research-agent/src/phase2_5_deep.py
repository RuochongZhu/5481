"""Phase 2.5: Deep Extraction — GROBID first, MinerU fallback, section-aware extraction."""

from __future__ import annotations

import os
import subprocess

from .api_client import agent_run_json, BRAIN_PHASE2_DEEP_EXTRACTOR
from .full_text import (
    GrobidClient,
    base_full_text_record,
    build_section_aware_text,
    load_parsed_full_text_records,
    paper_storage_id,
    parse_grobid_tei,
    parse_mineru_markdown,
    pdf_path_for_paper,
    save_parsed_full_text_records,
    structured_path_for_paper,
    tei_path_for_paper,
)
from .prompts import DEEP_EXTRACTOR
from .state_manager import complete_step, is_step_complete, update_step, save_state
from .utils import atomic_write_json, load_json, stable_fingerprint

import logging

log = logging.getLogger("research_agent")

BATCH_SIZE = int(os.getenv("DEEP_EXTRACTION_BATCH_SIZE", "4") or "4")


def run_phase2_5(state: dict, state_path: str, base_dir: str, client) -> dict:
    """Orchestrate Phase 2.5: full-text parsing + deep extraction."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    parsed_dir = os.path.join(base_dir, "data", "parsed")
    tei_dir = os.path.join(parsed_dir, "tei")
    structured_dir = os.path.join(parsed_dir, "structured")
    pdf_dir = os.path.join(base_dir, "data", "pdfs")
    md_dir = os.path.join(base_dir, "data", "markdown")
    classified_path = os.path.join(proc_dir, "classified.json")
    parsed_index_path = os.path.join(proc_dir, "parsed_full_text.json")

    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return state

    classified = load_json(classified_path)
    papers = [p for p in classified if p.get("primary_category", "X") != "X"]
    total = len(papers)
    log.info(f"Phase 2.5: deep extraction for {total} papers")

    # Step 0: GROBID PDF -> TEI -> structured full-text records
    if not is_step_complete(state, "2.5", "grobid_parse"):
        log.info("=== Phase 2.5.0: GROBID PDF → TEI → structured full text ===")
        parsed_records = _run_grobid_parse(
            papers,
            pdf_dir,
            tei_dir,
            structured_dir,
            parsed_index_path,
        )
        state = complete_step(state, state_path, "2.5", "grobid_parse", {
            "papers_considered": len(parsed_records),
            "parsed": sum(1 for item in parsed_records if item.get("parse_status") == "parsed"),
            "missing_pdf": sum(1 for item in parsed_records if item.get("pdf_status") != "present"),
            "failed": sum(
                1
                for item in parsed_records
                if item.get("parse_status") in {"parse_failed", "service_unavailable"}
            ),
        })
    else:
        parsed_records = load_parsed_full_text_records(parsed_index_path)
        log.info(f"GROBID parse already done, loaded {len(parsed_records)} full-text records")

    # Step 1: Optional MinerU fallback for PDFs GROBID could not parse
    if not is_step_complete(state, "2.5", "mineru_convert"):
        log.info("=== Phase 2.5.1: MinerU fallback (optional) ===")
        converted, parsed_records = _run_mineru_fallback(
            papers,
            parsed_records,
            pdf_dir,
            md_dir,
            structured_dir,
            parsed_index_path,
        )
        state = complete_step(state, state_path, "2.5", "mineru_convert", {
            "converted": converted,
        })
    else:
        parsed_records = load_parsed_full_text_records(parsed_index_path)
        log.info("MinerU fallback already done")

    # Step 2: Deep extraction via Claude using section-aware context
    if not is_step_complete(state, "2.5", "deep_extraction"):
        extracted = _run_deep_extraction(
            state,
            state_path,
            client,
            papers,
            proc_dir,
            parsed_records,
        )
        state = complete_step(state, state_path, "2.5", "deep_extraction", {
            "papers_extracted": len(extracted),
        })
    else:
        deep_path = os.path.join(proc_dir, "deep_extracted.json")
        extracted = load_json(deep_path) if os.path.exists(deep_path) else []
        log.info(f"Deep extraction already done, loaded {len(extracted)} papers")

    # Step 3: Merge back into classified.json
    if not is_step_complete(state, "2.5", "merge_deep"):
        log.info("=== Phase 2.5.3: Merging deep extraction into classified.json ===")
        _merge_deep_into_classified(classified, extracted, classified_path)
        state = complete_step(state, state_path, "2.5", "merge_deep")

    return state


def _run_grobid_parse(papers: list[dict], pdf_dir: str, tei_dir: str,
                      structured_dir: str, parsed_index_path: str) -> list[dict]:
    os.makedirs(tei_dir, exist_ok=True)
    os.makedirs(structured_dir, exist_ok=True)

    existing = {
        item.get("paperId"): item
        for item in load_parsed_full_text_records(parsed_index_path)
        if item.get("paperId")
    }

    grobid = GrobidClient()
    grobid_alive = grobid.is_alive()
    if grobid_alive:
        log.info("  GROBID service is alive")
    else:
        log.warning("  GROBID service unavailable — full-text parse_status will be recorded, extraction will fall back")

    records = []
    for paper in papers:
        paper_id = paper.get("paperId", "")
        pdf_path = pdf_path_for_paper(pdf_dir, paper_id)
        tei_path = tei_path_for_paper(tei_dir, paper_id)
        structured_path = structured_path_for_paper(structured_dir, paper_id)
        existing_record = existing.get(paper_id)

        if (
            existing_record
            and existing_record.get("parse_status") == "parsed"
            and os.path.exists(existing_record.get("structured_path") or structured_path)
            and os.path.exists(existing_record.get("tei_path") or tei_path)
        ):
            existing_record["pdf_path"] = pdf_path
            existing_record["tei_path"] = existing_record.get("tei_path") or tei_path
            existing_record["structured_path"] = existing_record.get("structured_path") or structured_path
            records.append(existing_record)
            continue

        record = base_full_text_record(paper, pdf_path)
        record["tei_path"] = tei_path
        record["structured_path"] = structured_path

        if not os.path.exists(pdf_path):
            record["parse_status"] = "missing_pdf"
            record["error"] = "PDF not present in local cache"
            records.append(record)
            continue

        if not grobid_alive:
            record["parse_status"] = "service_unavailable"
            record["error"] = "GROBID service is not reachable"
            records.append(record)
            continue

        try:
            tei_xml = grobid.process_fulltext(pdf_path)
            with open(tei_path, "w", encoding="utf-8") as handle:
                handle.write(tei_xml)
            record = parse_grobid_tei(tei_xml, paper, pdf_path, tei_path, structured_path)
        except Exception as e:
            record["parse_status"] = "parse_failed"
            record["error"] = str(e)

        records.append(record)

    save_parsed_full_text_records(records, parsed_index_path, structured_dir)
    log.info(
        "  Full-text parse records: parsed=%s missing_pdf=%s failed=%s",
        sum(1 for item in records if item.get("parse_status") == "parsed"),
        sum(1 for item in records if item.get("parse_status") == "missing_pdf"),
        sum(1 for item in records if item.get("parse_status") in {"parse_failed", "service_unavailable"}),
    )
    return records


def _run_mineru_fallback(papers: list[dict], parsed_records: list[dict], pdf_dir: str, md_dir: str,
                         structured_dir: str, parsed_index_path: str) -> tuple[int, list[dict]]:
    enable_fallback = os.getenv("ENABLE_MINERU_FALLBACK", "0").strip().lower() in {"1", "true", "yes"}
    if not enable_fallback:
        log.info("  MinerU fallback disabled (set ENABLE_MINERU_FALLBACK=1 to enable)")
        return 0, parsed_records

    os.makedirs(md_dir, exist_ok=True)

    try:
        subprocess.run(["mineru", "--version"], capture_output=True, check=True, timeout=10)
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        log.info("  MinerU not installed — skipping fallback")
        return 0, parsed_records

    record_map = {item.get("paperId"): dict(item) for item in parsed_records if item.get("paperId")}
    converted = 0

    for paper in papers:
        paper_id = paper.get("paperId", "")
        record = record_map.get(paper_id) or base_full_text_record(paper, pdf_path_for_paper(pdf_dir, paper_id))
        if record.get("parse_status") == "parsed":
            record_map[paper_id] = record
            continue

        pdf_path = pdf_path_for_paper(pdf_dir, paper_id)
        if not os.path.exists(pdf_path):
            record_map[paper_id] = record
            continue

        safe_id = paper_storage_id(paper_id)
        md_path = os.path.join(md_dir, f"{safe_id}.md")

        if not os.path.exists(md_path):
            try:
                result = subprocess.run(
                    ["mineru", "-p", pdf_path, "-o", md_dir, "-b", "pipeline"],
                    capture_output=True,
                    text=True,
                    timeout=180,
                )
                if result.returncode != 0:
                    record["error"] = (result.stderr or result.stdout or "").strip()[:300]
                    record_map[paper_id] = record
                    continue
            except Exception as e:
                record["error"] = str(e)
                record_map[paper_id] = record
                continue

        if os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8") as handle:
                markdown_text = handle.read()
            record = parse_mineru_markdown(
                markdown_text,
                paper,
                pdf_path,
                structured_path_for_paper(structured_dir, paper_id),
            )
            converted += 1

        record_map[paper_id] = record

    updated_records = list(record_map.values())
    save_parsed_full_text_records(updated_records, parsed_index_path, structured_dir)
    log.info(f"  MinerU fallback converted {converted} papers")
    return converted, updated_records


def _run_deep_extraction(state: dict, state_path: str, client,
                         papers: list[dict], proc_dir: str,
                         parsed_records: list[dict]) -> list[dict]:
    """Extract structured fields in batches via DEEP_EXTRACTOR agent."""
    deep_path = os.path.join(proc_dir, "deep_extracted.json")
    parsed_map = {item.get("paperId"): item for item in parsed_records if item.get("paperId")}
    papers_fingerprint = _deep_input_fingerprint(papers, parsed_map)
    step_state = state["phases"]["2.5"]["steps"]["deep_extraction"]
    stored_fingerprint = step_state.get("papers_fingerprint")

    start_idx = step_state.get("last_batch_index", 0)
    if start_idx > 0 and os.path.exists(deep_path) and stored_fingerprint == papers_fingerprint:
        extracted = load_json(deep_path)
        log.info(f"Resuming deep extraction from index {start_idx} ({len(extracted)} already done)")
    else:
        extracted = []
        if start_idx > 0 or os.path.exists(deep_path):
            log.info("Deep extraction inputs changed — restarting from scratch")
        update_step(state, "2.5", "deep_extraction", {
            "last_batch_index": 0,
            "papers_fingerprint": papers_fingerprint,
        })
        save_state(state_path, state)

    total = len(papers)
    for i in range(start_idx, total, BATCH_SIZE):
        batch = papers[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
        log.info(f"  Batch {batch_num}/{total_batches} (papers {i+1}-{min(i+BATCH_SIZE, total)})")

        batch_input = _format_batch_for_extraction(batch, parsed_map)
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
                for paper in batch:
                    extracted.append({"paperId": paper["paperId"], "method_type": "unknown", "key_claim": "", "error": "parse_failed"})
        except Exception as e:
            log.error(f"  Batch {batch_num} failed: {e}")
            for paper in batch:
                extracted.append({"paperId": paper["paperId"], "method_type": "unknown", "key_claim": "", "error": str(e)})

        atomic_write_json(deep_path, extracted)
        update_step(state, "2.5", "deep_extraction", {
            "last_batch_index": i + BATCH_SIZE,
            "papers_fingerprint": papers_fingerprint,
        })
        save_state(state_path, state)

    log.info(f"Deep extraction complete: {len(extracted)} papers")
    return extracted


def _deep_input_fingerprint(papers: list[dict], parsed_map: dict[str, dict]) -> str:
    signature = []
    for paper in papers:
        parsed = parsed_map.get(paper.get("paperId", ""), {})
        signature.append({
            "paperId": paper.get("paperId", ""),
            "title": paper.get("title", ""),
            "abstract": paper.get("abstract", ""),
            "year": paper.get("year", 0),
            "primary_category": paper.get("primary_category", "X"),
            "secondary_categories": paper.get("secondary_categories", []),
            "parse_status": parsed.get("parse_status", ""),
            "parser_used": parsed.get("parser_used", ""),
            "section_count": parsed.get("section_count", 0),
            "reference_count": parsed.get("reference_count", 0),
        })
    return stable_fingerprint(signature)


def _format_batch_for_extraction(papers: list[dict], parsed_map: dict[str, dict]) -> str:
    """Format papers for DEEP_EXTRACTOR, preferring section-aware full text over abstracts."""
    lines = []
    for i, paper in enumerate(papers, 1):
        paper_id = paper["paperId"]
        parsed = parsed_map.get(paper_id, {})
        full_text_excerpt = build_section_aware_text(parsed)
        if full_text_excerpt:
            text_source = (
                f"full_text_status: {parsed.get('parse_status', 'unknown')} via {parsed.get('parser_used', 'unknown')}\n"
                f"full_text_sections:\n{full_text_excerpt}"
            )
        else:
            abstract = (paper.get("abstract") or "")[:1000]
            text_source = (
                f"full_text_status: {parsed.get('parse_status', 'not_attempted')}\n"
                f"abstract: {abstract}"
            )

        lines.append(
            f"--- Paper {i} ---\n"
            f"paperId: {paper_id}\n"
            f"title: {paper.get('title', 'N/A')}\n"
            f"year: {paper.get('year', 'N/A')}\n"
            f"venue: {paper.get('venue', 'N/A')}\n"
            f"category: {paper.get('primary_category', 'X')}\n"
            f"section_count: {parsed.get('section_count', 0)}\n"
            f"reference_count: {parsed.get('reference_count', 0)}\n"
            f"{text_source}\n"
        )
    return "\n".join(lines)


def _merge_deep_into_classified(classified: list[dict], extracted: list[dict],
                                classified_path: str):
    by_id = {item["paperId"]: item for item in extracted if "paperId" in item}
    merged = 0
    for paper in classified:
        paper_id = paper.get("paperId", "")
        if paper_id not in by_id:
            continue
        ext = by_id[paper_id]
        for field in (
            "method_type",
            "key_claim",
            "methodology",
            "limitation",
            "what_it_does_NOT_address",
            "dataset_or_benchmark",
            "theoretical_framework",
        ):
            if field in ext:
                paper[field] = ext[field]
        merged += 1
    atomic_write_json(classified_path, classified)
    log.info(f"Merged deep extraction into {merged} papers in classified.json")
