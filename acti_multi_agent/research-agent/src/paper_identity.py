"""Paper identity helpers: normalize aliases, choose canonical IDs, and resolve S2 lookups."""

from __future__ import annotations

import hashlib
import re


_OPENALEX_RE = re.compile(r"(?:https?://openalex\.org/)?(W\d+)", re.I)
_ARXIV_RE = re.compile(r"(?:arxiv:)?([A-Za-z\-\.]+/\d{7}|\d{4}\.\d{4,5}(?:v\d+)?)", re.I)
_S2_HEX_RE = re.compile(r"^[0-9a-f]{20,64}$", re.I)
_LENS_RE = re.compile(r"(?:lens:)?([0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9]{3})", re.I)


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    doi = value.strip()
    doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    doi = doi.replace("doi:", "").strip().lower()
    return doi or None


def normalize_openalex_id(value: str | None) -> str | None:
    if not value:
        return None
    match = _OPENALEX_RE.search(value.strip())
    if not match:
        return None
    return f"https://openalex.org/{match.group(1).upper()}"


def normalize_arxiv_id(value: str | None) -> str | None:
    if not value:
        return None
    match = _ARXIV_RE.search(value.strip())
    if not match:
        return None
    return match.group(1)


def normalize_lens_id(value: str | None) -> str | None:
    if not value:
        return None
    match = _LENS_RE.search(value.strip())
    if not match:
        return None
    return match.group(1)


def looks_like_s2_paper_id(value: str | None) -> bool:
    if not value:
        return False
    raw = value.strip()
    if not raw or raw.startswith("https://openalex.org/") or raw.startswith("arxiv:"):
        return False
    if raw.startswith("doi:") or raw.startswith("local_"):
        return False
    return bool(_S2_HEX_RE.match(raw))


def extract_source_ids(paper: dict) -> dict[str, str]:
    """Extract normalized source-specific identifiers from a paper record."""
    source_ids = dict(paper.get("source_ids") or {})
    external_ids = paper.get("externalIds") or {}
    legacy_paper_id = paper.get("paperId") or ""

    doi = normalize_doi(
        source_ids.get("doi")
        or paper.get("doi")
        or external_ids.get("DOI")
    )
    if doi:
        source_ids["doi"] = doi

    openalex = normalize_openalex_id(
        source_ids.get("openalex")
        or external_ids.get("OpenAlex")
        or legacy_paper_id
    )
    if openalex:
        source_ids["openalex"] = openalex

    arxiv = normalize_arxiv_id(
        source_ids.get("arxiv")
        or external_ids.get("ArXiv")
        or external_ids.get("Arxiv")
        or legacy_paper_id
    )
    if arxiv:
        source_ids["arxiv"] = arxiv

    lens_id = normalize_lens_id(
        source_ids.get("lens")
        or external_ids.get("lens")
        or external_ids.get("Lens")
        or legacy_paper_id
    )
    if lens_id:
        source_ids["lens"] = lens_id

    s2_id = source_ids.get("s2")
    if not s2_id and looks_like_s2_paper_id(legacy_paper_id):
        s2_id = legacy_paper_id
    if not s2_id:
        for key in ("SemanticScholar", "S2", "CorpusId"):
            raw = external_ids.get(key)
            if looks_like_s2_paper_id(raw):
                s2_id = raw
                break
    if s2_id:
        source_ids["s2"] = s2_id.strip()

    return source_ids


def merge_source_ids(primary: dict | None, duplicate: dict | None) -> dict[str, str]:
    merged = {}
    for source in (primary or {}, duplicate or {}):
        for key, value in (source or {}).items():
            if value and key not in merged:
                merged[key] = value
    return merged


def canonical_id_for_paper(paper: dict) -> str:
    """Choose a stable internal ID used across the pipeline."""
    source_ids = extract_source_ids(paper)
    if source_ids.get("doi"):
        return f"doi:{source_ids['doi']}"
    if source_ids.get("s2"):
        return f"s2:{source_ids['s2']}"
    if source_ids.get("openalex"):
        return f"openalex:{source_ids['openalex'].rsplit('/', 1)[-1]}"
    if source_ids.get("arxiv"):
        return f"arxiv:{source_ids['arxiv']}"
    if source_ids.get("lens"):
        return f"lens:{source_ids['lens']}"

    title = (paper.get("title") or "").strip().lower()
    digest = hashlib.sha256(title.encode()).hexdigest()[:16]
    return f"local:{digest}"


def alias_ids_for_paper(paper: dict) -> list[str]:
    """Collect every identifier we may need to resolve back to the canonical node."""
    source_ids = extract_source_ids(paper)
    aliases = set(paper.get("alias_ids") or [])

    paper_id = paper.get("paperId")
    if paper_id:
        aliases.add(paper_id)

    canonical = paper.get("canonical_id") or canonical_id_for_paper(paper)
    aliases.add(canonical)

    if source_ids.get("doi"):
        aliases.add(source_ids["doi"])
        aliases.add(f"doi:{source_ids['doi']}")
        aliases.add(f"DOI:{source_ids['doi']}")
    if source_ids.get("s2"):
        aliases.add(source_ids["s2"])
        aliases.add(f"s2:{source_ids['s2']}")
    if source_ids.get("openalex"):
        aliases.add(source_ids["openalex"])
        aliases.add(f"openalex:{source_ids['openalex'].rsplit('/', 1)[-1]}")
    if source_ids.get("arxiv"):
        aliases.add(source_ids["arxiv"])
        aliases.add(f"arxiv:{source_ids['arxiv']}")
        aliases.add(f"ARXIV:{source_ids['arxiv']}")
    if source_ids.get("lens"):
        aliases.add(source_ids["lens"])
        aliases.add(f"lens:{source_ids['lens']}")
        aliases.add(f"LENS:{source_ids['lens']}")

    return sorted(a for a in aliases if a)


def finalize_paper_identity(paper: dict) -> dict:
    """Normalize identity fields and promote a stable canonical ID into paperId."""
    record = dict(paper)
    source_ids = extract_source_ids(record)
    canonical = canonical_id_for_paper(record)
    original_paper_id = record.get("paperId")

    if original_paper_id and original_paper_id != canonical:
        record.setdefault("legacy_paper_ids", [])
        if original_paper_id not in record["legacy_paper_ids"]:
            record["legacy_paper_ids"].append(original_paper_id)

    record["source_ids"] = source_ids
    record["canonical_id"] = canonical
    record["paperId"] = canonical
    record["alias_ids"] = alias_ids_for_paper(record)
    return record


def get_s2_lookup_id(paper: dict) -> str | None:
    """Return the identifier that should be sent to Semantic Scholar endpoints."""
    source_ids = extract_source_ids(paper)
    if source_ids.get("s2"):
        return source_ids["s2"]

    paper_id = paper.get("paperId") or ""
    if looks_like_s2_paper_id(paper_id):
        return paper_id
    return None


def build_alias_lookup(papers: list[dict]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for paper in papers:
        canonical = paper.get("paperId") or paper.get("canonical_id") or canonical_id_for_paper(paper)
        for alias in alias_ids_for_paper(paper):
            lookup[alias] = canonical
            lookup[alias.lower()] = canonical
    return lookup


def canonicalize_paper_ref(ref_id, alias_lookup: dict[str, str]) -> str | None:
    if not ref_id:
        return None
    if isinstance(ref_id, dict):
        for key in ("paperId", "canonical_id", "id", "doi"):
            value = ref_id.get(key)
            if value:
                return canonicalize_paper_ref(value, alias_lookup)
        return None
    if not isinstance(ref_id, str):
        ref_id = str(ref_id)
    raw = ref_id.strip()
    if raw in alias_lookup:
        return alias_lookup[raw]
    if raw.lower() in alias_lookup:
        return alias_lookup[raw.lower()]
    if raw in alias_lookup.values():
        return raw
    return None
