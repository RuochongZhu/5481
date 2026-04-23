"""Full-text parsing helpers: PDF storage IDs, GROBID parsing, normalized schema."""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

import requests

from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}

SECTION_KIND_RULES = {
    "abstract": ["abstract"],
    "introduction": ["introduction", "background"],
    "related_work": ["related work", "literature review", "previous work"],
    "methods": ["method", "methods", "methodology", "materials", "experimental setup", "approach"],
    "results": ["result", "results", "findings", "evaluation", "experiments", "analysis"],
    "discussion": ["discussion"],
    "limitations": ["limitation", "limitations", "threats to validity"],
    "conclusion": ["conclusion", "conclusions", "concluding remarks"],
    "appendix": ["appendix", "supplementary"],
    "acknowledgements": ["acknowledg", "funding"],
}

SECTION_PRIORITY = [
    "abstract",
    "introduction",
    "methods",
    "results",
    "discussion",
    "limitations",
    "conclusion",
    "related_work",
]


class GrobidClient:
    """Thin client for local GROBID service."""

    def __init__(self, base_url: str | None = None, timeout_sec: float | None = None):
        self.base_url = (base_url or os.getenv("GROBID_BASE_URL", "http://localhost:8070")).rstrip("/")
        self.timeout_sec = float(timeout_sec or os.getenv("GROBID_TIMEOUT_SEC", "180"))
        self.session = requests.Session()

    def is_alive(self) -> bool:
        try:
            resp = self.session.get(f"{self.base_url}/api/isalive", timeout=10)
            resp.raise_for_status()
            return resp.text.strip().lower() == "true"
        except Exception:
            return False

    def process_fulltext(self, pdf_path: str) -> str:
        with open(pdf_path, "rb") as handle:
            files = {
                "input": (os.path.basename(pdf_path), handle, "application/pdf"),
            }
            data = {
                "consolidateHeader": os.getenv("GROBID_CONSOLIDATE_HEADER", "1"),
                "consolidateCitations": os.getenv("GROBID_CONSOLIDATE_CITATIONS", "0"),
            }
            resp = self.session.post(
                f"{self.base_url}/api/processFulltextDocument",
                files=files,
                data=data,
                timeout=self.timeout_sec,
            )
        if resp.status_code >= 400:
            detail = (resp.text or "").strip()[:500]
            raise RuntimeError(
                f"GROBID full-text parse failed (HTTP {resp.status_code}) for {os.path.basename(pdf_path)}. "
                f"{detail or 'Check GROBID logs and pdfalto runtime dependencies.'}"
            )
        return resp.text


def paper_storage_id(paper_id: str) -> str:
    """Return a filesystem-safe identifier for a canonical paper id."""
    return (paper_id or "").replace("/", "_").replace(":", "_")


def pdf_path_for_paper(pdf_dir: str, paper_id: str) -> str:
    return os.path.join(pdf_dir, f"{paper_storage_id(paper_id)}.pdf")


def tei_path_for_paper(tei_dir: str, paper_id: str) -> str:
    return os.path.join(tei_dir, f"{paper_storage_id(paper_id)}.tei.xml")


def structured_path_for_paper(structured_dir: str, paper_id: str) -> str:
    return os.path.join(structured_dir, f"{paper_storage_id(paper_id)}.json")


def load_parsed_full_text_records(index_path: str) -> list[dict]:
    if not os.path.exists(index_path):
        return []
    return load_json(index_path)


def save_parsed_full_text_records(records: list[dict], index_path: str, structured_dir: str) -> None:
    os.makedirs(structured_dir, exist_ok=True)
    atomic_write_json(index_path, records)
    for record in records:
        paper_id = record.get("paperId")
        if not paper_id:
            continue
        atomic_write_json(structured_path_for_paper(structured_dir, paper_id), record)


def base_full_text_record(paper: dict, pdf_path: str) -> dict:
    pdf_url = paper.get("openAccessPdf")
    if isinstance(pdf_url, dict):
        pdf_url = pdf_url.get("url", "")
    pdf_status = "present" if os.path.exists(pdf_path) else "missing_pdf"
    if pdf_status == "missing_pdf" and not pdf_url:
        pdf_status = "no_open_access_pdf"

    return {
        "paperId": paper.get("paperId", ""),
        "title": paper.get("title", ""),
        "year": paper.get("year", 0),
        "source": paper.get("source", ""),
        "source_pdf_url": pdf_url or "",
        "pdf_path": pdf_path,
        "pdf_status": pdf_status,
        "parser_used": "",
        "parse_status": "pending",
        "tei_path": "",
        "structured_path": "",
        "sections": [],
        "references": [],
        "section_count": 0,
        "reference_count": 0,
        "error": "",
        "updated_at": _now(),
    }


def parse_grobid_tei(tei_xml: str, paper: dict, pdf_path: str, tei_path: str,
                     structured_path: str) -> dict:
    root = ET.fromstring(tei_xml)
    abstract_text = _extract_abstract(root)
    sections = []
    if abstract_text:
        sections.append({
            "index": 1,
            "title": "Abstract",
            "kind": "abstract",
            "text": abstract_text,
            "word_count": _word_count(abstract_text),
        })

    body = root.find(".//tei:text/tei:body", TEI_NS)
    next_index = len(sections) + 1
    if body is not None:
        for div in body.findall("./tei:div", TEI_NS):
            next_index = _collect_div_sections(div, sections, next_index)

    references = _extract_references(root)

    return {
        "paperId": paper.get("paperId", ""),
        "title": paper.get("title", ""),
        "year": paper.get("year", 0),
        "source": paper.get("source", ""),
        "source_pdf_url": _normalize_pdf_url(paper.get("openAccessPdf")),
        "pdf_path": pdf_path,
        "pdf_status": "present" if os.path.exists(pdf_path) else "missing_pdf",
        "parser_used": "grobid",
        "parse_status": "parsed",
        "tei_path": tei_path,
        "structured_path": structured_path,
        "sections": sections,
        "references": references,
        "section_count": len(sections),
        "reference_count": len(references),
        "error": "",
        "updated_at": _now(),
    }


def parse_mineru_markdown(markdown_text: str, paper: dict, pdf_path: str,
                          structured_path: str) -> dict:
    sections = _markdown_sections(markdown_text)
    return {
        "paperId": paper.get("paperId", ""),
        "title": paper.get("title", ""),
        "year": paper.get("year", 0),
        "source": paper.get("source", ""),
        "source_pdf_url": _normalize_pdf_url(paper.get("openAccessPdf")),
        "pdf_path": pdf_path,
        "pdf_status": "present" if os.path.exists(pdf_path) else "missing_pdf",
        "parser_used": "mineru",
        "parse_status": "parsed_via_mineru",
        "tei_path": "",
        "structured_path": structured_path,
        "sections": sections,
        "references": [],
        "section_count": len(sections),
        "reference_count": 0,
        "error": "",
        "updated_at": _now(),
    }


def build_section_aware_text(record: dict, max_section_chars: int = 700,
                             max_total_chars: int = 4000) -> str:
    """Format a compact section-aware excerpt for downstream extraction."""
    sections = record.get("sections", []) or []
    if not sections:
        return ""

    selected = []
    seen_indexes = set()

    for kind in SECTION_PRIORITY:
        for section in sections:
            if section.get("kind") == kind and section.get("index") not in seen_indexes:
                selected.append(section)
                seen_indexes.add(section.get("index"))
                break

    if len(selected) < 6:
        for section in sorted(sections, key=lambda item: item.get("word_count", 0), reverse=True):
            if section.get("index") in seen_indexes:
                continue
            selected.append(section)
            seen_indexes.add(section.get("index"))
            if len(selected) >= 6:
                break

    remaining = max_total_chars
    blocks = []
    for section in selected:
        if remaining <= 0:
            break
        title = section.get("title", "Untitled")
        kind = section.get("kind", "body")
        text = (section.get("text") or "").strip()
        if not text:
            continue
        snippet = text[: min(max_section_chars, remaining)]
        blocks.append(f"[{kind.upper()}] {title}\n{snippet}")
        remaining -= len(snippet)

    references = record.get("references", []) or []
    if references:
        ref_titles = [ref.get("title", "") for ref in references[:5] if ref.get("title")]
        if ref_titles and remaining > 0:
            ref_block = "Referenced works extracted: " + "; ".join(ref_titles)
            blocks.append(ref_block[:remaining])

    return "\n\n".join(blocks).strip()


def _collect_div_sections(div, sections: list[dict], start_index: int) -> int:
    title = _clean_text(_first_child_text(div, "head"))
    text_parts = []
    for child in list(div):
        tag = _local_name(child.tag)
        if tag in {"p", "ab", "quote", "list", "formula", "figDesc", "table"}:
            text = _clean_text(" ".join(child.itertext()))
            if text:
                text_parts.append(text)
    text = "\n\n".join(text_parts).strip()
    if text:
        sections.append({
            "index": start_index,
            "title": title or f"Section {start_index}",
            "kind": _classify_section_kind(title or ""),
            "text": text,
            "word_count": _word_count(text),
        })
        start_index += 1

    for child_div in div.findall("./tei:div", TEI_NS):
        start_index = _collect_div_sections(child_div, sections, start_index)

    return start_index


def _extract_abstract(root) -> str:
    abstract = root.find(".//tei:profileDesc/tei:abstract", TEI_NS)
    if abstract is None:
        return ""
    return _clean_text(" ".join(abstract.itertext()))


def _extract_references(root) -> list[dict]:
    refs = []
    for idx, bibl in enumerate(root.findall(".//tei:listBibl/tei:biblStruct", TEI_NS), start=1):
        analytic_title = bibl.find("./tei:analytic/tei:title", TEI_NS)
        monogr_title = bibl.find("./tei:monogr/tei:title", TEI_NS)
        date = bibl.find(".//tei:date", TEI_NS)
        doi = bibl.find(".//tei:idno[@type='DOI']", TEI_NS)
        title = _clean_text(
            (analytic_title.text if analytic_title is not None else "")
            or (monogr_title.text if monogr_title is not None else "")
        )
        authors = []
        for author in bibl.findall(".//tei:author", TEI_NS):
            name = _clean_text(" ".join(author.itertext()))
            if name:
                authors.append(name)
        refs.append({
            "index": idx,
            "title": title,
            "doi": _clean_text(doi.text if doi is not None and doi.text else ""),
            "year": _extract_year(date),
            "authors": authors[:8],
            "raw_text": _clean_text(" ".join(bibl.itertext()))[:1200],
        })
    return refs


def _markdown_sections(markdown_text: str) -> list[dict]:
    sections = []
    current_title = "Body"
    current_kind = "body"
    buffer = []
    index = 1

    def flush():
        nonlocal index, buffer, current_title, current_kind
        text = _clean_text("\n".join(buffer))
        if not text:
            return
        sections.append({
            "index": index,
            "title": current_title,
            "kind": current_kind,
            "text": text,
            "word_count": _word_count(text),
        })
        index += 1
        buffer = []

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            flush()
            current_title = stripped.lstrip("#").strip() or f"Section {index}"
            current_kind = _classify_section_kind(current_title)
            continue
        buffer.append(line)
    flush()

    if not sections and markdown_text.strip():
        text = _clean_text(markdown_text)
        sections.append({
            "index": 1,
            "title": "Body",
            "kind": "body",
            "text": text,
            "word_count": _word_count(text),
        })
    return sections


def _classify_section_kind(title: str) -> str:
    lowered = (title or "").strip().lower()
    for kind, patterns in SECTION_KIND_RULES.items():
        if any(pattern in lowered for pattern in patterns):
            return kind
    return "body"


def _first_child_text(parent, local_name: str) -> str:
    child = parent.find(f"./tei:{local_name}", TEI_NS)
    return "" if child is None else "".join(child.itertext())


def _extract_year(date_node) -> str:
    if date_node is None:
        return ""
    when = date_node.attrib.get("when", "")
    if when:
        return when[:4]
    text = _clean_text("".join(date_node.itertext()))
    return text[:4] if text[:4].isdigit() else ""


def _normalize_pdf_url(value) -> str:
    if isinstance(value, dict):
        return value.get("url", "") or ""
    return value or ""


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _clean_text(text: str) -> str:
    return " ".join((text or "").split())


def _word_count(text: str) -> int:
    return len((text or "").split())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
