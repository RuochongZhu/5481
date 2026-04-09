"""Phase 1: Seed Corpus Assembly — 3-layer search (OpenAlex + S2 citations + arXiv) + import + dedup."""

from __future__ import annotations

import os
import logging
import math
import re
from .api_client import ArxivClient, CrossrefClient, OpenAlexClient, S2Client
from .importers import import_file
from .dedup import deduplicate
from .paper_identity import (
    extract_source_ids,
    finalize_paper_identity,
    merge_source_ids,
    normalize_doi,
)
from .state_manager import complete_step, is_step_complete, update_step
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")

CORE_TARGETS = {
    "A": 30, "B": 17, "C": 12, "D": 22, "E": 22,
    "F": 17, "G": 12, "H": 12, "I": 12, "J": 12,
}

CATEGORY_KEYWORDS = {
    "A": {
        "anchors": [
            "model collapse", "self-consuming", "autophagy", "recursively generated",
            "recursive training", "collapse", "synthetic data degradation",
        ],
        "secondary": ["mad", "tail collapse", "distribution shift", "generated data"],
    },
    "B": {
        "anchors": [
            "commoncrawl", "web data", "web pollution", "contamination",
            "ai generated content", "synthetic text", "bot content",
        ],
        "secondary": ["web-scraped", "bot traffic", "internet text", "crawl"],
    },
    "C": {
        "anchors": ["watermark", "detection", "detector", "ai text detection"],
        "secondary": ["adversarial", "reactive", "classifier", "watermarking"],
    },
    "D": {
        "anchors": [
            "entropy", "perplexity", "kl divergence", "renyi", "type-token",
            "lexical diversity",
        ],
        "secondary": ["diversity metric", "text quality", "distribution analysis", "ttr"],
    },
    "E": {
        "anchors": [
            "data quality", "curation", "deduplication", "filtering", "pretraining data",
            "textbook quality",
        ],
        "secondary": ["scaling laws", "mixing ratio", "data mixture", "quality filtering"],
    },
    "F": {
        "anchors": ["rlhf", "human feedback", "preference data", "human annotation"],
        "secondary": ["alignment", "human-in-the-loop", "labeling", "reward model"],
    },
    "G": {
        "anchors": ["provenance", "data lineage", "community platform", "append-only", "platform design"],
        "secondary": ["verification", "anti-algorithmic", "community", "traceability"],
    },
    "H": {
        "anchors": [
            "temporal", "longitudinal", "over time", "corpus linguistics",
            "web quality", "commoncrawl quality",
        ],
        "secondary": ["trend", "evolution", "quality degradation", "time series"],
    },
    "I": {
        "anchors": [
            "social reasoning", "socialiqa", "empathetic dialogues", "empathy benchmark",
            "social intelligence", "social commonsense",
        ],
        "secondary": ["dialogue benchmark", "commonsense reasoning", "social task"],
    },
    "J": {
        "anchors": [
            "lora", "qlora", "fine-tune", "fine-tuning", "data composition",
            "ablation", "data mixture",
        ],
        "secondary": ["instruction tuning", "mixture effect", "quality versus quantity"],
    },
}

CATEGORY_GROUP_RULES = {
    "H": [
        ["temporal", "longitudinal", "over time", "historical", "evolution"],
        ["web", "text", "corpus", "commoncrawl", "quality", "readability"],
    ],
    "I": [
        ["social reasoning", "socialiqa", "theory of mind", "social commonsense", "empathetic"],
    ],
    "J": [
        ["lora", "qlora", "fine-tune", "fine-tuning", "instruction tuning", "adapter"],
        ["data composition", "data mixture", "quality", "quantity", "ablation", "training data", "synthetic data"],
    ],
}


def run_phase1(state: dict, state_path: str, base_dir: str,
               oa: OpenAlexClient, s2: S2Client, arxiv: ArxivClient) -> dict:
    """Orchestrate all Phase 1 steps. Returns updated state."""
    config_dir = os.path.join(base_dir, "config")
    raw_dir = os.path.join(base_dir, "data", "raw")
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)
    crossref = CrossrefClient(
        mailto=os.environ.get("CROSSREF_MAILTO", os.environ.get("OPENALEX_MAILTO", "user@example.com")),
        tool_name=os.environ.get("CROSSREF_TOOL_NAME", "research-agent"),
        plus_token=os.environ.get("CROSSREF_PLUS_API_TOKEN") or None,
    )

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
        core = _select_core_corpus(corpus)
        core = _enrich_core_with_crossref(core, crossref)
        core = _resolve_core_source_ids(core, s2)
        atomic_write_json(os.path.join(proc_dir, "corpus_200.json"), core)
        log.info(f"Core corpus: {len(core)} papers saved to corpus_200.json")

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
    papers = []
    for i, q in enumerate(queries_cfg["queries"]):
        query_text = q["query"]
        max_pages = q.get("max_pages", 3)
        category = q.get("category", "X")
        log.info(f"  [{i+1}/{len(queries_cfg['queries'])}] OpenAlex: '{query_text}'")
        try:
            results = oa.search(query_text, max_pages=max_pages)
            for raw in results:
                if not raw.get("title"):
                    continue
                paper = OpenAlexClient.to_unified(raw)
                paper["query_category"] = category
                paper["matched_query"] = query_text
                paper["retrieval_layer"] = "openalex"
                papers.append(paper)
            log.info(f"    → {len(results)} results")
        except Exception as e:
            log.error(f"    → Failed: {e}")

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

    for idx, seed in enumerate(seeds_cfg["seeds"]):
        log.info(f"  Resolving seed: {seed['title'][:60]}...")
        paper = s2.resolve_seed(seed["lookup_query"], seed.get("doi"))
        if paper:
            paper["_seed_index"] = idx
            paper["_seed_title"] = seed["title"]
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

    papers = []
    for r in all_papers:
        if not r.get("paperId"):
            continue
        paper = S2Client.to_unified(r)
        paper["retrieval_layer"] = "s2_citation"
        papers.append(paper)
    # Include resolved seeds themselves
    seed_papers = []
    for s in resolved_seeds:
        if not s.get("paperId"):
            continue
        paper = S2Client.to_unified(s)
        paper["retrieval_layer"] = "s2_seed"
        paper["matched_query"] = s.get("_seed_title", "")
        paper["query_category"] = "D" if "entropy" in s.get("_seed_title", "").lower() else "A"
        seed_papers.append(paper)
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
    arxiv_queries = []
    for q in arxiv_queries_raw:
        if isinstance(q, dict):
            arxiv_queries.append(q)
        else:
            arxiv_queries.append({"query": q, "category": "X"})

    papers = []
    for i, q in enumerate(arxiv_queries):
        query_text = q["query"]
        category = q.get("category", "X")
        log.info(f"  [{i+1}/{len(arxiv_queries)}] arXiv: '{query_text[:50]}'")
        try:
            results = arxiv.search(query_text, max_results=100)
            for raw in results:
                if not raw.get("title"):
                    continue
                paper = ArxivClient.to_unified(raw)
                paper["query_category"] = category
                paper["matched_query"] = query_text
                paper["retrieval_layer"] = "arxiv"
                papers.append(paper)
            log.info(f"    → {len(results)} results")
        except Exception as e:
            log.error(f"    → Failed: {e}")

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


def _normalize_text(paper: dict) -> str:
    parts = [
        paper.get("title", ""),
        paper.get("abstract", "") or "",
        paper.get("venue", "") or "",
        " ".join(paper.get("concepts", []) or []),
    ]
    return " ".join(parts).lower()


def _score_paper_for_category(text: str, year: int, citations: int, category: str) -> float:
    group_rules = CATEGORY_GROUP_RULES.get(category, [])
    if group_rules and not all(any(term in text for term in group) for group in group_rules):
        return 0.0

    cfg = CATEGORY_KEYWORDS[category]
    anchor_hits = sum(1 for kw in cfg["anchors"] if kw in text)
    if anchor_hits == 0:
        return 0.0

    secondary_hits = sum(1 for kw in cfg["secondary"] if kw in text)
    recent_bonus = 2.0 if year >= 2024 else 1.0 if year >= 2022 else 0.0
    citation_bonus = min(math.log10(max(citations, 1)), 3.0)
    return anchor_hits * 5.0 + secondary_hits * 1.5 + recent_bonus + citation_bonus


def _select_core_corpus(corpus: list[dict]) -> list[dict]:
    """Build a focused top corpus for Phase 2 instead of classifying the full 4k+ papers.

    Strategy:
    - Score each paper against A-J taxonomy using domain keywords
    - Select the top papers per category according to CORE_TARGETS
    - Deduplicate across categories, then fill remaining slots from global scores
    """
    scored = []
    for paper in corpus:
        text = _normalize_text(paper)
        year = int(paper.get("year", 0) or 0)
        cites = int(paper.get("citationCount", 0) or 0)
        scores = {cat: _score_paper_for_category(text, year, cites, cat) for cat in CORE_TARGETS}
        query_category = paper.get("query_category")
        if query_category in scores and scores[query_category] > 0:
            scores[query_category] += 8.0
        best_cat = max(scores, key=scores.get)
        best_score = scores[best_cat]
        if best_score <= 0:
            continue

        item = dict(paper)
        item["query_category"] = best_cat
        item["selection_score"] = round(best_score, 3)
        item["selection_scores"] = {k: round(v, 3) for k, v in scores.items() if v > 0}
        scored.append(item)

    ranked_by_cat = {
        cat: sorted(
            [p for p in scored if p["selection_scores"].get(cat, 0) > 0],
            key=lambda p: (
                p["selection_scores"].get(cat, 0),
                p.get("citationCount", 0),
                p.get("year", 0),
            ),
            reverse=True,
        )
        for cat in CORE_TARGETS
    }

    selected = []
    seen = set()
    for cat, target in CORE_TARGETS.items():
        count = 0
        for paper in ranked_by_cat[cat]:
            pid = paper.get("paperId")
            if not pid or pid in seen:
                continue
            paper = dict(paper)
            paper["query_category"] = cat
            selected.append(paper)
            seen.add(pid)
            count += 1
            if count >= target:
                break

    target_total = sum(CORE_TARGETS.values())
    if len(selected) < target_total:
        global_ranked = sorted(
            scored,
            key=lambda p: (
                p.get("selection_score", 0),
                p.get("citationCount", 0),
                p.get("year", 0),
            ),
            reverse=True,
        )
        for paper in global_ranked:
            pid = paper.get("paperId")
            if not pid or pid in seen:
                continue
            selected.append(paper)
            seen.add(pid)
            if len(selected) >= target_total:
                break

    selected.sort(
        key=lambda p: (
            p.get("query_category", "X"),
            -(p.get("selection_scores", {}).get(p.get("query_category", "X"), p.get("selection_score", 0))),
            -(p.get("citationCount", 0)),
        )
    )
    log.info(
        "Core corpus category counts: %s",
        {cat: sum(1 for p in selected if p.get("query_category") == cat) for cat in CORE_TARGETS}
    )
    return selected[:target_total]


def _resolve_core_source_ids(core: list[dict], s2: S2Client | None) -> list[dict]:
    """Resolve missing S2 identities for the focused core corpus only.

    This keeps Phase 1 affordable while giving later graph phases a stable ID layer.
    """
    if s2 is None:
        return [finalize_paper_identity(p) for p in core]

    resolved = 0
    checked = 0
    enriched_core = []

    for paper in core:
        item = finalize_paper_identity(paper)
        ids = extract_source_ids(item)
        if ids.get("s2"):
            enriched_core.append(item)
            continue

        checked += 1
        s2_result = None
        doi = ids.get("doi")
        arxiv = ids.get("arxiv")

        try:
            if doi:
                s2_result = s2.get_paper(f"DOI:{doi}", fields="paperId,externalIds")
            if not s2_result and arxiv:
                s2_result = s2.get_paper(f"ARXIV:{arxiv}", fields="paperId,externalIds")
        except Exception as e:
            log.debug(f"  Core ID resolve failed for {item.get('title', '')[:60]}: {e}")

        if s2_result and s2_result.get("paperId"):
            s2_unified = S2Client.to_unified(s2_result)
            merged_external = dict(item.get("externalIds") or {})
            merged_external.update(s2_unified.get("externalIds") or {})
            item["externalIds"] = merged_external
            item["source_ids"] = merge_source_ids(
                item.get("source_ids") or {},
                s2_unified.get("source_ids") or {},
            )
            item = finalize_paper_identity(item)
            resolved += 1

        enriched_core.append(item)

    if checked:
        log.info(f"Resolved S2 identities for {resolved}/{checked} core papers missing S2 IDs")
    return enriched_core


def _enrich_core_with_crossref(core: list[dict], crossref: CrossrefClient | None) -> list[dict]:
    """Enrich the focused core corpus with DOI-authoritative metadata."""
    if crossref is None:
        return [finalize_paper_identity(p) for p in core]

    enriched = []
    resolved = 0
    searched = 0

    for paper in core:
        item = finalize_paper_identity(paper)
        source_ids = extract_source_ids(item)
        work = None

        try:
            if source_ids.get("doi"):
                work = crossref.get_work(source_ids["doi"])
            else:
                searched += 1
                query = item.get("title", "")
                hits = crossref.search_works(query, rows=3) if query else []
                title_norm = re.sub(r"\W+", " ", query).strip().lower()
                for hit in hits:
                    candidate = (hit.get("title") or [""])[0]
                    candidate_norm = re.sub(r"\W+", " ", candidate).strip().lower()
                    if title_norm and candidate_norm and (
                        title_norm == candidate_norm
                        or title_norm in candidate_norm
                        or candidate_norm in title_norm
                    ):
                        work = hit
                        break
        except Exception as e:
            log.debug(f"  Crossref enrich failed for {item.get('title', '')[:60]}: {e}")

        if work:
            resolved += 1
            doi = normalize_doi(work.get("DOI"))
            if doi:
                item["doi"] = doi
                item["source_ids"] = merge_source_ids(item.get("source_ids") or {}, {"doi": doi})
                ext = dict(item.get("externalIds") or {})
                ext["DOI"] = doi
                item["externalIds"] = ext

            licenses = [lic.get("URL") for lic in work.get("license", []) if lic.get("URL")]
            relation = work.get("relation") or {}
            updates = []
            for rel_values in relation.values():
                if isinstance(rel_values, list):
                    for rel_item in rel_values:
                        if isinstance(rel_item, dict) and rel_item.get("id"):
                            updates.append(rel_item["id"])

            item["integrity"] = {
                "publisher": work.get("publisher", ""),
                "type": work.get("type", ""),
                "license_urls": licenses,
                "is_retracted": bool((work.get("update-to") or []) or relation.get("is-retracted-by")),
                "update_targets": updates,
                "crossref_reference_count": work.get("reference-count", 0),
                "crossref_is_referenced_by_count": work.get("is-referenced-by-count", 0),
            }
            item["crossref"] = {
                "indexed": work.get("indexed", {}).get("date-time", ""),
                "created": work.get("created", {}).get("date-time", ""),
            }
            item = finalize_paper_identity(item)

        enriched.append(item)

    if core:
        log.info(f"Crossref enriched {resolved}/{len(core)} core papers ({searched} title-search attempts)")
    return enriched


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
