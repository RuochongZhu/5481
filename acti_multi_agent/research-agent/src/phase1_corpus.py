"""Phase 1: Seed Corpus Assembly — 3-layer search (OpenAlex + S2 citations + arXiv) + import + dedup."""

import os
import logging
from .api_client import OpenAlexClient, S2Client, ArxivClient
from .importers import import_file
from .dedup import deduplicate
from .state_manager import complete_step, is_step_complete, update_step
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")


def run_phase1(state: dict, state_path: str, base_dir: str,
               oa: OpenAlexClient, s2: S2Client, arxiv: ArxivClient) -> dict:
    """Orchestrate all Phase 1 steps. Returns updated state."""
    config_dir = os.path.join(base_dir, "config")
    raw_dir = os.path.join(base_dir, "data", "raw")
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)

    all_papers = []

    # Step 1: Layer 1 — OpenAlex bulk search (primary)
    if not is_step_complete(state, 1, "openalex_search"):
        log.info("=== Phase 1.1: OpenAlex bulk search (Layer 1) ===")
        queries_cfg = load_json(os.path.join(config_dir, "search_queries.json"))
        oa_results = _run_openalex_search(oa, queries_cfg, raw_dir)
        state = complete_step(state, state_path, 1, "openalex_search", {
            "papers_found": len(oa_results),
            "queries_completed": len(queries_cfg["queries"]),
        })
    else:
        oa_path = os.path.join(raw_dir, "openalex_results.json")
        oa_results = load_json(oa_path) if os.path.exists(oa_path) else []
        log.info(f"OpenAlex search already done, loaded {len(oa_results)} papers")
    all_papers.extend(oa_results)

    # Step 2: Layer 2 — S2 citation chain expansion
    if not is_step_complete(state, 1, "s2_citation_expansion"):
        log.info("=== Phase 1.2: S2 citation expansion (Layer 2) ===")
        seeds_cfg = load_json(os.path.join(config_dir, "seed_papers.json"))
        s2_results = _run_s2_citation_expansion(s2, seeds_cfg, raw_dir)
        state = complete_step(state, state_path, 1, "s2_citation_expansion", {
            "seeds_processed": len(seeds_cfg["seeds"]),
            "papers_added": len(s2_results),
        })
    else:
        s2_path = os.path.join(raw_dir, "s2_citation_expansion.json")
        s2_results = load_json(s2_path) if os.path.exists(s2_path) else []
        log.info(f"S2 citation expansion already done, loaded {len(s2_results)} papers")
    all_papers.extend(s2_results)

    # Step 3: Layer 3 — arXiv preprint sweep
    if not is_step_complete(state, 1, "arxiv_search"):
        log.info("=== Phase 1.3: arXiv preprint sweep (Layer 3) ===")
        queries_cfg = load_json(os.path.join(config_dir, "search_queries.json"))
        arxiv_results = _run_arxiv_search(arxiv, queries_cfg, raw_dir)
        state = complete_step(state, state_path, 1, "arxiv_search", {
            "papers_found": len(arxiv_results),
        })
    else:
        ax_path = os.path.join(raw_dir, "arxiv_results.json")
        arxiv_results = load_json(ax_path) if os.path.exists(ax_path) else []
        log.info(f"arXiv search already done, loaded {len(arxiv_results)} papers")
    all_papers.extend(arxiv_results)

    # Step 4: Import manual exports from data/raw/
    if not is_step_complete(state, 1, "manual_import"):
        log.info("=== Phase 1.4: Manual imports ===")
        imported, files = _run_manual_imports(raw_dir)
        state = complete_step(state, state_path, 1, "manual_import", {
            "files_imported": files,
            "papers_added": len(imported),
        })
    else:
        imported = []
        log.info("Manual import already done")
    all_papers.extend(imported)

    # Step 5: Download PDFs for papers needing full-text extraction
    if not is_step_complete(state, 1, "pdf_download"):
        log.info("=== Phase 1.5: PDF download (for MinerU) ===")
        corpus_path = os.path.join(proc_dir, "corpus_unified.json")
        if os.path.exists(corpus_path):
            corpus = load_json(corpus_path)
        else:
            corpus = all_papers
        downloaded, skipped = _download_pdfs(corpus, os.path.join(base_dir, "data", "pdfs"))
        state = complete_step(state, state_path, 1, "pdf_download", {
            "downloaded": downloaded, "skipped": skipped,
        })
    else:
        log.info("PDF download already done")

    # Step 6: Deduplicate and merge
    if not is_step_complete(state, 1, "dedup_and_merge"):
        log.info("=== Phase 1.5: Dedup & merge ===")
        total_before = len(all_papers)
        corpus = deduplicate(all_papers)
        output_path = os.path.join(proc_dir, "corpus_unified.json")
        atomic_write_json(output_path, corpus)
        log.info(f"Unified corpus: {len(corpus)} papers saved")

        qc = _quality_check(corpus)
        state["phases"]["1"]["quality_check"] = qc
        state = complete_step(state, state_path, 1, "dedup_and_merge", {
            "total_before": total_before,
            "total_after": len(corpus),
        })
    else:
        log.info("Dedup already done")

    return state


# ---------------------------------------------------------------------------
# Layer 1: OpenAlex
# ---------------------------------------------------------------------------

def _run_openalex_search(oa: OpenAlexClient, queries_cfg: dict, raw_dir: str) -> list[dict]:
    """Run all search queries against OpenAlex."""
    all_raw = []
    for i, q in enumerate(queries_cfg["queries"]):
        query_text = q["query"]
        max_pages = q.get("max_pages", 3)
        log.info(f"  [{i+1}/{len(queries_cfg['queries'])}] OpenAlex: '{query_text}'")
        try:
            results = oa.search(query_text, max_pages=max_pages)
            all_raw.extend(results)
            log.info(f"    → {len(results)} results")
        except Exception as e:
            log.error(f"    → Failed: {e}")

    papers = [OpenAlexClient.to_unified(r) for r in all_raw if r.get("title")]
    atomic_write_json(os.path.join(raw_dir, "openalex_results.json"), papers)
    log.info(f"Total from OpenAlex: {len(papers)} papers")
    return papers


# ---------------------------------------------------------------------------
# Layer 2: S2 citation expansion
# ---------------------------------------------------------------------------

def _run_s2_citation_expansion(s2: S2Client, seeds_cfg: dict, raw_dir: str) -> list[dict]:
    """Resolve seed papers via S2, then expand references + citations."""
    all_papers = []
    resolved_seeds = []

    for seed in seeds_cfg["seeds"]:
        log.info(f"  Resolving seed: {seed['title'][:60]}...")
        paper = s2.resolve_seed(seed["lookup_query"], seed.get("doi"))
        if paper:
            resolved_seeds.append(paper)
            log.info(f"    → Found: {paper.get('paperId', '?')[:20]}")
        else:
            log.warning(f"    → Could not resolve: {seed['title'][:40]}")

    for paper in resolved_seeds:
        pid = paper["paperId"]
        log.info(f"  Expanding: {paper.get('title', pid)[:60]}...")
        try:
            refs = s2.get_references(pid, limit=100)
            log.info(f"    → {len(refs)} references")
            all_papers.extend(refs)
        except Exception as e:
            log.error(f"    → References failed: {e}")
        try:
            cits = s2.get_citations(pid, limit=100)
            log.info(f"    → {len(cits)} citations")
            all_papers.extend(cits)
        except Exception as e:
            log.error(f"    → Citations failed: {e}")

    papers = [S2Client.to_unified(r) for r in all_papers if r.get("paperId")]
    # Include resolved seeds themselves
    seed_papers = [S2Client.to_unified(s) for s in resolved_seeds if s.get("paperId")]
    papers.extend(seed_papers)

    atomic_write_json(os.path.join(raw_dir, "s2_citation_expansion.json"), papers)
    log.info(f"Total from S2 expansion: {len(papers)} papers")
    return papers


# ---------------------------------------------------------------------------
# Layer 3: arXiv
# ---------------------------------------------------------------------------

def _run_arxiv_search(arxiv: ArxivClient, queries_cfg: dict, raw_dir: str) -> list[dict]:
    """Search arXiv for cutting-edge preprints."""
    arxiv_queries_raw = queries_cfg.get("arxiv_queries", [
        {"query": 'all:"model collapse" AND all:"training data"'},
        {"query": 'all:"synthetic data" AND all:"generative model" AND all:"contamination"'},
        {"query": 'all:"data authenticity" AND all:"language model"'},
        {"query": 'all:"self-consuming" AND all:"generative"'},
        {"query": 'all:"entropy" AND all:"AI generated text"'},
    ])
    # Normalize: accept both dicts and plain strings
    arxiv_queries = [
        q["query"] if isinstance(q, dict) else q for q in arxiv_queries_raw
    ]

    all_raw = []
    for i, q in enumerate(arxiv_queries):
        log.info(f"  [{i+1}/{len(arxiv_queries)}] arXiv: '{q[:50]}'")
        try:
            results = arxiv.search(q, max_results=100)
            all_raw.extend(results)
            log.info(f"    → {len(results)} results")
        except Exception as e:
            log.error(f"    → Failed: {e}")

    papers = [ArxivClient.to_unified(r) for r in all_raw if r.get("title")]
    atomic_write_json(os.path.join(raw_dir, "arxiv_results.json"), papers)
    log.info(f"Total from arXiv: {len(papers)} preprints")
    return papers


# ---------------------------------------------------------------------------
# Manual imports
# ---------------------------------------------------------------------------

def _run_manual_imports(raw_dir: str) -> tuple[list[dict], list[str]]:
    """Scan raw_dir for CSV/BibTeX files and import them."""
    imported = []
    files_imported = []
    skip = {"openalex_results.json", "s2_citation_expansion.json", "arxiv_results.json"}

    for fname in sorted(os.listdir(raw_dir)):
        if fname in skip or fname.endswith(".json"):
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext in (".csv", ".bib", ".ris"):
            fpath = os.path.join(raw_dir, fname)
            log.info(f"  Importing: {fname}")
            try:
                papers = import_file(fpath)
                imported.extend(papers)
                files_imported.append(fname)
                log.info(f"    → {len(papers)} papers")
            except Exception as e:
                log.error(f"    → Import failed: {e}")

    return imported, files_imported


# ---------------------------------------------------------------------------
# Quality check
# ---------------------------------------------------------------------------

def _quality_check(corpus: list[dict]) -> dict:
    import datetime
    current_year = datetime.datetime.now().year
    total = len(corpus)
    recent = sum(1 for p in corpus if p.get("year", 0) >= current_year - 2)
    pct_recent = round(recent / total * 100, 1) if total else 0

    by_source = {}
    for p in corpus:
        src = p.get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1

    qc = {
        "total_papers": total,
        "recent_2yr": recent,
        "pct_recent": pct_recent,
        "by_source": by_source,
        "passed": total >= 100,
    }
    log.info(f"Quality: {total} papers, {pct_recent}% recent, sources={by_source}, passed={qc['passed']}")
    return qc


# ---------------------------------------------------------------------------
# PDF download (for MinerU in Phase 2.5)
# ---------------------------------------------------------------------------

def _download_pdfs(corpus: list[dict], pdf_dir: str) -> tuple[int, int]:
    """Download open-access PDFs for papers with short/missing abstracts.

    Only downloads papers where:
    1. Abstract is missing or < 200 chars (needs full text)
    2. openAccessPdf URL is available
    """
    import requests as req

    os.makedirs(pdf_dir, exist_ok=True)
    downloaded = 0
    skipped = 0

    candidates = [
        p for p in corpus
        if len(p.get("abstract") or "") < 200
        and p.get("openAccessPdf")
    ]
    log.info(f"  {len(candidates)} papers need PDF download (short/missing abstract)")

    for p in candidates:
        pid = p["paperId"]
        safe_name = pid.replace("/", "_").replace(":", "_")
        pdf_path = os.path.join(pdf_dir, f"{safe_name}.pdf")
        if os.path.exists(pdf_path):
            skipped += 1
            continue

        url = p["openAccessPdf"]
        if isinstance(url, dict):
            url = url.get("url", "")
        if not url:
            skipped += 1
            continue

        try:
            resp = req.get(url, timeout=30, stream=True)
            if resp.status_code == 200 and "pdf" in resp.headers.get("content-type", "").lower():
                with open(pdf_path, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        f.write(chunk)
                downloaded += 1
            else:
                skipped += 1
        except Exception as e:
            log.debug(f"  PDF download failed for {pid}: {e}")
            skipped += 1

    log.info(f"  PDFs: {downloaded} downloaded, {skipped} skipped")
    return downloaded, skipped
