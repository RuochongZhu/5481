"""Import CSV/BibTeX/JSON supplements into the unified paper schema."""

from __future__ import annotations

import csv
import json
import logging
import os
import re
from urllib.parse import parse_qs, urlparse

log = logging.getLogger("research_agent")


def _to_unified(raw: dict, source: str) -> dict:
    """Map any source format to the unified paper schema."""
    record = {
        "paperId": raw.get("paperId") or raw.get("id") or None,
        "doi": raw.get("doi") or raw.get("DOI") or None,
        "title": raw.get("title", "").strip(),
        "authors": raw.get("authors", []),
        "year": _safe_int(raw.get("year") or raw.get("Year")),
        "venue": raw.get("venue") or raw.get("journal") or raw.get("Venue") or "",
        "abstract": raw.get("abstract") or raw.get("Abstract") or "",
        "citationCount": _safe_int(raw.get("citationCount") or raw.get("Citation Count") or raw.get("citations")),
        "source": source,
        "externalIds": raw.get("externalIds", {}),
        "elicit_extraction": raw.get("elicit_extraction"),
    }
    for key in (
        "source_ids",
        "openAccessPdf",
        "query_category",
        "matched_query",
        "retrieval_layer",
        "manual_core_include",
        "manual_core_reason",
        "legacy_paper_ids",
        "supplement_id",
        "supplement_priority",
    ):
        value = raw.get(key)
        if value not in (None, "", [], {}):
            record[key] = value
    return record


def _safe_int(val) -> int:
    if val is None:
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


def _parse_authors(raw: str) -> list[str]:
    """Parse author string like 'Smith, J.; Doe, A.' into list."""
    if not raw:
        return []
    # Try semicolon split first, then comma
    if ";" in raw:
        return [a.strip() for a in raw.split(";") if a.strip()]
    if " and " in raw.lower():
        return [a.strip() for a in raw.replace(" And ", " and ").split(" and ") if a.strip()]
    return [raw.strip()]


def import_undermind_csv(filepath: str) -> list[dict]:
    """Parse Undermind CSV export."""
    papers = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = {
                "title": row.get("Title") or row.get("title", ""),
                "authors": _parse_authors(row.get("Authors") or row.get("authors", "")),
                "year": row.get("Year") or row.get("year"),
                "abstract": row.get("Abstract") or row.get("abstract", ""),
                "doi": row.get("DOI") or row.get("doi"),
                "venue": row.get("Source") or row.get("Journal") or "",
                "citationCount": row.get("Citations") or row.get("Citation Count"),
            }
            papers.append(_to_unified(raw, "undermind"))
    log.info(f"Imported {len(papers)} papers from Undermind CSV: {filepath}")
    return papers


def import_elicit_csv(filepath: str) -> list[dict]:
    """Parse Elicit CSV export. Preserves custom extraction columns."""
    papers = []
    extraction_cols = {"method", "finding", "limitation", "gap", "research_question",
                       "dataset", "theoretical_framework", "Method", "Finding",
                       "Limitation", "Gap", "Research Question", "Dataset"}
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = {
                "title": row.get("Title") or row.get("title", ""),
                "authors": _parse_authors(row.get("Authors") or row.get("authors", "")),
                "year": row.get("Year") or row.get("year"),
                "abstract": row.get("Abstract") or row.get("abstract", ""),
                "doi": row.get("DOI") or row.get("doi"),
                "citationCount": row.get("Citation Count") or row.get("citations"),
                "venue": row.get("Venue") or row.get("Journal") or "",
            }
            # Capture Elicit custom extraction columns
            extraction = {}
            for col in extraction_cols:
                if col in row and row[col]:
                    extraction[col.lower().replace(" ", "_")] = row[col]
            if extraction:
                raw["elicit_extraction"] = extraction
            papers.append(_to_unified(raw, "elicit"))
    log.info(f"Imported {len(papers)} papers from Elicit CSV: {filepath}")
    return papers


def import_bibtex(filepath: str) -> list[dict]:
    """Parse BibTeX file using bibtexparser."""
    try:
        import bibtexparser
    except ImportError:
        log.error("bibtexparser not installed. Run: pip install bibtexparser")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        bib_db = bibtexparser.load(f)

    papers = []
    for entry in bib_db.entries:
        raw = {
            "title": entry.get("title", "").replace("{", "").replace("}", ""),
            "authors": _parse_authors(entry.get("author", "")),
            "year": entry.get("year"),
            "abstract": entry.get("abstract", ""),
            "doi": entry.get("doi"),
            "venue": entry.get("journal") or entry.get("booktitle") or "",
        }
        papers.append(_to_unified(raw, "bibtex"))
    log.info(f"Imported {len(papers)} papers from BibTeX: {filepath}")
    return papers


def _canonical_seed_id(doi: str | None, arxiv: str | None, title: str) -> str:
    if doi:
        return f"doi:{doi.strip().lower()}"
    if arxiv:
        return f"arxiv:{arxiv.strip()}"
    slug = re.sub(r"[^a-z0-9]+", "-", title.strip().lower()).strip("-")
    return f"local:{slug[:80] or 'supplement'}"


def _derive_pdf_url(entry: dict) -> str:
    arxiv = (entry.get("arxiv") or "").strip()
    if arxiv:
        return f"https://arxiv.org/pdf/{arxiv}.pdf"

    url = (entry.get("url") or "").strip()
    if not url:
        return ""
    if url.lower().endswith(".pdf"):
        return url

    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path or ""

    if "openreview.net" in host:
        query = parse_qs(parsed.query)
        paper_id = (query.get("id") or [""])[0]
        if paper_id:
            return f"https://openreview.net/pdf?id={paper_id}"

    if "proceedings.mlr.press" in host and path.endswith(".html"):
        stem = os.path.splitext(os.path.basename(path))[0]
        if stem:
            return url.replace(f"/{stem}.html", f"/{stem}/{stem}.pdf")

    if "aclanthology.org" in host:
        acl_id = path.strip("/").split("/")[0]
        if acl_id:
            return f"https://aclanthology.org/{acl_id}.pdf"

    if "pnas.org" in host and "/doi/" in path:
        return url.replace("/doi/", "/doi/pdf/")

    if "nature.com" in host and "/articles/" in path:
        return url.rstrip("/") + ".pdf"

    return ""


def import_supplement_json(filepath: str) -> list[dict]:
    """Parse the custom supplement-search JSON format used for targeted additions."""
    with open(filepath, "r", encoding="utf-8") as f:
        payload = json.load(f)

    papers = []
    for entry in payload.get("papers", []):
        title = (entry.get("title") or "").strip()
        if not title:
            continue

        doi = (entry.get("doi") or "").strip() or None
        arxiv = (entry.get("arxiv") or "").strip() or None
        categories = entry.get("categories") or []
        primary_category = categories[0] if categories else "X"
        integration = entry.get("integration") or {}
        abstract_parts = [
            entry.get("key_finding", "").strip(),
            integration.get("role_in_narrative", "").strip(),
            "Search hints: " + "; ".join(entry.get("search_queries") or []),
        ]
        abstract = " ".join(part for part in abstract_parts if part)

        external_ids = {}
        source_ids = {}
        if doi:
            external_ids["DOI"] = doi
            source_ids["doi"] = doi
        if arxiv:
            external_ids["ArXiv"] = arxiv
            source_ids["arxiv"] = arxiv

        raw = {
            "paperId": _canonical_seed_id(doi, arxiv, title),
            "doi": doi,
            "title": title,
            "authors": entry.get("authors") or [],
            "year": entry.get("year"),
            "venue": entry.get("venue") or "",
            "abstract": abstract,
            "citationCount": 0,
            "externalIds": external_ids,
            "source_ids": source_ids,
            "openAccessPdf": _derive_pdf_url(entry),
            "query_category": primary_category,
            "matched_query": (entry.get("search_queries") or [title])[0],
            "retrieval_layer": "supplement_json",
            "manual_core_include": primary_category != "X",
            "manual_core_reason": integration.get("role_in_narrative")
            or f"Supplement import {entry.get('id', '').strip()}",
            "supplement_id": entry.get("id", "").strip(),
            "supplement_priority": entry.get("priority", "").strip(),
        }
        papers.append(_to_unified(raw, "supplement_json"))

    log.info(f"Imported {len(papers)} papers from supplement JSON: {filepath}")
    return papers


def detect_format(filepath: str) -> str:
    """Auto-detect file format from extension."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".bib":
        return "bibtex"
    if ext == ".csv":
        # Peek at headers to distinguish Undermind vs Elicit
        with open(filepath, "r", encoding="utf-8") as f:
            header = f.readline().lower()
        if "relevance" in header or "source" in header:
            return "undermind"
        return "elicit"
    if ext == ".json" or ext == "":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if isinstance(payload, dict) and isinstance(payload.get("papers"), list):
                return "supplement_json"
        except Exception:
            return "unknown"
    if ext == ".ris":
        return "ris"
    return "unknown"


def import_file(filepath: str) -> list[dict]:
    """Auto-detect format and import."""
    fmt = detect_format(filepath)
    if fmt == "bibtex":
        return import_bibtex(filepath)
    if fmt == "undermind":
        return import_undermind_csv(filepath)
    if fmt == "elicit":
        return import_elicit_csv(filepath)
    if fmt == "supplement_json":
        return import_supplement_json(filepath)
    log.warning(f"Unknown format for {filepath}, trying generic CSV")
    return import_elicit_csv(filepath)
