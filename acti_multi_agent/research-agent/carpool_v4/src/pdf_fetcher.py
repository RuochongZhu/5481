"""Layered full-text PDF acquisition with legal-first fallback.

Layer order (configurable):
  1. OpenAlex `oa_url` / `pdf_url` (legal Open Access)
  2. Unpaywall API (legal Open Access locator)
  3. arXiv abs page → PDF (legal preprints)
  4. Sci-Hub mirror — DISABLED by default. Set ENABLE_SCIHUB=true to opt in.
     Sci-Hub aggregates copyrighted PDFs without publisher consent; usage may
     violate publisher terms and your institution's acceptable-use policy.
     This module exposes the hook but does not run it unless explicitly enabled.

Env vars:
  PDF_DOWNLOAD_MAX_PAPERS — cap (int). 0 disables the layer.
  PDF_DOWNLOAD_USER_AGENT — User-Agent string.
  UNPAYWALL_EMAIL        — required for Unpaywall API (it is keyed on email).
  ENABLE_SCIHUB          — "true" to enable layer 4. Default false.
  SCIHUB_MIRROR          — base URL, e.g. "https://sci-hub.se" (user supplies).
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Iterable

import requests

DEFAULT_UA = os.environ.get("PDF_DOWNLOAD_USER_AGENT", "research-agent/1.0")
DEFAULT_TIMEOUT = 30


class PDFFetchResult:
    __slots__ = ("paper_id", "doi", "arxiv_id", "layer", "url", "path", "size", "error")

    def __init__(self, paper_id, doi=None, arxiv_id=None, layer=None,
                 url=None, path=None, size=0, error=None):
        self.paper_id = paper_id
        self.doi = doi
        self.arxiv_id = arxiv_id
        self.layer = layer
        self.url = url
        self.path = path
        self.size = size
        self.error = error

    def to_dict(self) -> dict:
        return {k: getattr(self, k) for k in self.__slots__}


def _safe_filename(paper_id: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in paper_id)[:120]


def _http_get_pdf(url: str, dest: Path, log) -> tuple[bool, int, str | None]:
    """Try to download a PDF. Returns (ok, size_bytes, error_msg)."""
    try:
        r = requests.get(url, headers={"User-Agent": DEFAULT_UA},
                         timeout=DEFAULT_TIMEOUT, stream=True, allow_redirects=True)
        ct = r.headers.get("content-type", "").lower()
        if r.status_code != 200:
            return False, 0, f"http {r.status_code}"
        if "pdf" not in ct and not url.lower().endswith(".pdf"):
            return False, 0, f"non-pdf content-type: {ct[:60]}"
        dest.parent.mkdir(parents=True, exist_ok=True)
        size = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)
                    size += len(chunk)
        if size < 1024:
            dest.unlink(missing_ok=True)
            return False, 0, f"too small: {size}b"
        return True, size, None
    except Exception as e:
        return False, 0, str(e)[:200]


# ---------------------------------------------------------------------------
# Layer 1: OpenAlex oa_url
# ---------------------------------------------------------------------------

def _try_openalex(paper: dict, dest: Path, log) -> tuple[bool, int, str | None]:
    for key in ("pdf_url", "oa_url", "open_access_pdf"):
        url = paper.get(key)
        if isinstance(url, dict):
            url = url.get("url")
        if not url:
            continue
        ok, size, err = _http_get_pdf(url, dest, log)
        if ok:
            return ok, size, None
    return False, 0, "no openalex oa_url / pdf_url field"


# ---------------------------------------------------------------------------
# Layer 2: Unpaywall
# ---------------------------------------------------------------------------

def _try_unpaywall(paper: dict, dest: Path, log) -> tuple[bool, int, str | None]:
    doi = paper.get("doi")
    email = os.environ.get("UNPAYWALL_EMAIL") or os.environ.get("OPENALEX_MAILTO") \
            or os.environ.get("CROSSREF_MAILTO")
    if not doi or not email:
        return False, 0, "missing doi or email"
    try:
        r = requests.get(
            f"https://api.unpaywall.org/v2/{doi}",
            params={"email": email},
            headers={"User-Agent": DEFAULT_UA},
            timeout=DEFAULT_TIMEOUT,
        )
        if r.status_code != 200:
            return False, 0, f"unpaywall http {r.status_code}"
        data = r.json()
        best = data.get("best_oa_location") or {}
        url = best.get("url_for_pdf") or best.get("url")
        if not url:
            return False, 0, "unpaywall: no url_for_pdf"
        return _http_get_pdf(url, dest, log)
    except Exception as e:
        return False, 0, f"unpaywall error: {str(e)[:120]}"


# ---------------------------------------------------------------------------
# Layer 3: arXiv direct
# ---------------------------------------------------------------------------

def _try_arxiv(paper: dict, dest: Path, log) -> tuple[bool, int, str | None]:
    aid = paper.get("arxiv_id")
    if not aid and paper.get("source") == "arxiv":
        aid = (paper.get("id") or "").split("/")[-1]
    if not aid:
        return False, 0, "no arxiv_id"
    aid = aid.replace("arXiv:", "").strip()
    url = f"https://arxiv.org/pdf/{aid}.pdf"
    return _http_get_pdf(url, dest, log)


# ---------------------------------------------------------------------------
# Layer 4: Sci-Hub mirror — OPT-IN ONLY
# ---------------------------------------------------------------------------

def _try_scihub(paper: dict, dest: Path, log) -> tuple[bool, int, str | None]:
    """Sci-Hub fallback. Disabled by default. User must opt in via env.

    Note: This layer is provided as a hook for users whose research workflow
    already uses Sci-Hub. It is not enabled by default. Whether to use Sci-Hub
    is a personal / institutional choice with copyright implications; this
    module does not endorse or recommend its use, only documents the slot.
    """
    if os.environ.get("ENABLE_SCIHUB", "false").strip().lower() not in ("1", "true", "yes", "on"):
        return False, 0, "scihub disabled (ENABLE_SCIHUB!=true)"
    mirror = os.environ.get("SCIHUB_MIRROR", "").rstrip("/")
    if not mirror:
        return False, 0, "scihub: no SCIHUB_MIRROR set"
    doi = paper.get("doi")
    if not doi:
        return False, 0, "scihub: no doi"
    try:
        landing = requests.get(
            f"{mirror}/{doi}",
            headers={"User-Agent": DEFAULT_UA},
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True,
        )
        if landing.status_code != 200:
            return False, 0, f"scihub landing http {landing.status_code}"
        import re
        m = re.search(r'(?:src|href)=["\']([^"\']+\.pdf)', landing.text)
        if not m:
            return False, 0, "scihub: no pdf url in landing page"
        pdf_url = m.group(1)
        if pdf_url.startswith("//"):
            pdf_url = "https:" + pdf_url
        elif pdf_url.startswith("/"):
            pdf_url = mirror + pdf_url
        return _http_get_pdf(pdf_url, dest, log)
    except Exception as e:
        return False, 0, f"scihub error: {str(e)[:120]}"


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------

LAYERS = [
    ("openalex", _try_openalex),
    ("unpaywall", _try_unpaywall),
    ("arxiv", _try_arxiv),
    ("scihub", _try_scihub),
]


def fetch_pdfs(papers: Iterable[dict], pdf_dir: Path, log,
               max_papers: int = 0, sleep_seconds: float = 0.5) -> list[PDFFetchResult]:
    """Iterate papers, attempt PDF fetch via layered fallback. Skips already-cached PDFs."""
    results: list[PDFFetchResult] = []
    pdf_dir = Path(pdf_dir)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    attempts = 0
    for paper in papers:
        if max_papers and attempts >= max_papers:
            break
        pid = paper.get("id") or paper.get("doi") or paper.get("arxiv_id")
        if not pid:
            continue
        dest = pdf_dir / f"{_safe_filename(pid)}.pdf"
        if dest.exists() and dest.stat().st_size >= 1024:
            results.append(PDFFetchResult(pid, doi=paper.get("doi"),
                                          arxiv_id=paper.get("arxiv_id"),
                                          layer="cached", url=str(dest),
                                          path=str(dest), size=dest.stat().st_size))
            continue

        attempts += 1
        result = PDFFetchResult(pid, doi=paper.get("doi"), arxiv_id=paper.get("arxiv_id"))
        for layer_name, fn in LAYERS:
            ok, size, err = fn(paper, dest, log)
            if ok:
                result.layer = layer_name
                result.path = str(dest)
                result.size = size
                log.info(f"PDF fetched [{layer_name}] {pid} ({size//1024}KB)")
                break
            else:
                log.debug(f"PDF [{layer_name}] {pid}: {err}")
                result.error = err  # last error wins
        if result.path is None:
            log.warning(f"PDF MISS {pid}: {result.error}")
        results.append(result)
        time.sleep(sleep_seconds)
    return results


def fetch_for_classified(classified_path: str, pdf_dir: str, log,
                         max_papers: int = 0) -> dict:
    """Convenience: read classified.json, run fetch_pdfs, write report."""
    classified = json.load(open(classified_path))
    if isinstance(classified, dict) and "papers" in classified:
        classified = classified["papers"]
    results = fetch_pdfs(classified, Path(pdf_dir), log, max_papers=max_papers)
    by_layer: dict[str, int] = {}
    for r in results:
        by_layer[r.layer or "miss"] = by_layer.get(r.layer or "miss", 0) + 1
    report = {
        "total_attempted": len(results),
        "by_layer": by_layer,
        "miss": sum(1 for r in results if r.path is None),
        "results": [r.to_dict() for r in results],
    }
    return report
