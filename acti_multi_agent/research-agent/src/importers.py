"""Import CSV/BibTeX from Undermind, Elicit, ResearchRabbit into unified schema."""

import csv
import logging
import os

log = logging.getLogger("research_agent")


def _to_unified(raw: dict, source: str) -> dict:
    """Map any source format to the unified paper schema."""
    return {
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
    log.warning(f"Unknown format for {filepath}, trying generic CSV")
    return import_elicit_csv(filepath)
