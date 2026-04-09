"""Paper deduplication: DOI match + title Jaccard similarity."""

from __future__ import annotations

import hashlib
import logging
from collections import defaultdict

from .paper_identity import (
    extract_source_ids,
    finalize_paper_identity,
    merge_source_ids,
)

log = logging.getLogger("research_agent")


def _normalize_title(title: str) -> set[str]:
    """Lowercase, strip punctuation, split into word tokens."""
    cleaned = "".join(c if c.isalnum() or c.isspace() else " " for c in title.lower())
    return set(cleaned.split())


def title_similarity(t1: str, t2: str) -> float:
    """Jaccard similarity on lowercased word tokens."""
    s1, s2 = _normalize_title(t1), _normalize_title(t2)
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


def _get_doi(paper: dict) -> str | None:
    """Extract DOI from paper record."""
    return extract_source_ids(paper).get("doi")


def _make_id(paper: dict) -> str:
    """Generate a stable ID from title if no paperId."""
    if paper.get("paperId"):
        return paper["paperId"]
    h = hashlib.sha256(paper.get("title", "").lower().encode()).hexdigest()[:16]
    return f"local_{h}"


def merge_records(existing: dict, duplicate: dict) -> dict:
    """Merge metadata from duplicate into existing, preferring non-null fields."""
    for key in ("abstract", "venue", "citationCount", "year", "doi", "externalIds", "tldr"):
        if not existing.get(key) and duplicate.get(key):
            existing[key] = duplicate[key]
    # Merge sources
    src_e = existing.get("source", "")
    src_d = duplicate.get("source", "")
    if src_d and src_d not in src_e:
        existing["source"] = f"{src_e}+{src_d}" if src_e else src_d
    existing["source_ids"] = merge_source_ids(
        extract_source_ids(existing),
        extract_source_ids(duplicate),
    )
    alias_ids = set(existing.get("alias_ids") or [])
    alias_ids.update(duplicate.get("alias_ids") or [])
    if duplicate.get("paperId"):
        alias_ids.add(duplicate["paperId"])
    existing["alias_ids"] = sorted(a for a in alias_ids if a)

    for key in ("query_category", "matched_query", "retrieval_layer"):
        if not existing.get(key) and duplicate.get(key):
            existing[key] = duplicate[key]
    return existing


def _prepare_identity(paper: dict) -> dict:
    prepared = dict(paper)
    prepared["paperId"] = _make_id(prepared)
    prepared["source_ids"] = merge_source_ids(
        extract_source_ids(prepared),
        prepared.get("source_ids") or {},
    )
    alias_ids = set(prepared.get("alias_ids") or [])
    alias_ids.add(prepared["paperId"])
    prepared["alias_ids"] = sorted(a for a in alias_ids if a)
    return prepared


def deduplicate(papers: list[dict], jaccard_threshold: float = 0.8) -> list[dict]:
    """Deduplicate papers. Primary: DOI match. Fallback: title Jaccard > threshold."""
    # Phase 1: group by DOI
    doi_map: dict[str, dict] = {}
    no_doi: list[dict] = []

    for raw in papers:
        p = _prepare_identity(raw)
        doi = _get_doi(p)
        if doi:
            if doi in doi_map:
                doi_map[doi] = merge_records(doi_map[doi], p)
            else:
                doi_map[doi] = p
        else:
            no_doi.append(p)

    unique = list(doi_map.values())

    # Phase 2: title similarity for papers without DOI
    for p in no_doi:
        matched = False
        for u in unique:
            if title_similarity(p.get("title", ""), u.get("title", "")) > jaccard_threshold:
                merge_records(u, p)
                matched = True
                break
        if not matched:
            unique.append(p)

    unique = [finalize_paper_identity(p) for p in unique]

    before = len(papers)
    after = len(unique)
    log.info(f"Dedup: {before} → {after} papers ({before - after} duplicates removed)")
    return unique
