"""API clients: Anthropic agent_run() + OpenAlex + Semantic Scholar + arXiv."""

import json
import os
import time
import logging
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from .utils import RateLimiter

log = logging.getLogger("research_agent")

# Tiered model config: fast (high-volume) vs deep (low-volume, high-quality)
MODEL_FAST = os.getenv("MODEL_FAST", "claude-sonnet-4-20250514")
MODEL_DEEP = os.getenv("MODEL_DEEP", "claude-opus-4-20250514")
DEFAULT_MODEL = MODEL_FAST  # backward compat
S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "paperId,title,year,abstract,citationCount,venue,authors,externalIds"
# tldr not supported on references/citations endpoints — only on paper search/details
S2_FIELDS_DETAIL = "paperId,title,year,abstract,citationCount,venue,authors,externalIds,tldr"
OA_BASE = "https://api.openalex.org/works"
ARXIV_BASE = "http://export.arxiv.org/api/query"


# ---------------------------------------------------------------------------
# Anthropic wrappers
# ---------------------------------------------------------------------------

def agent_run(client, role: str, task: str, model: str = DEFAULT_MODEL,
              max_tokens: int = 4096, retries: int = 3) -> str:
    """Single agent call with retry + exponential backoff."""
    for attempt in range(retries):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=role,
                messages=[{"role": "user", "content": task}],
            )
            return resp.content[0].text
        except Exception as e:
            wait = 2 ** attempt
            log.warning(f"agent_run attempt {attempt+1} failed: {e}. Retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"agent_run failed after {retries} retries")


def agent_run_json(client, role: str, task: str, model: str = DEFAULT_MODEL,
                   max_tokens: int = 4096) -> list | dict:
    """Agent call that parses response as JSON. Strips markdown fences if present."""
    import re
    raw = agent_run(client, role, task, model, max_tokens)
    text = raw.strip()
    # Strip ```json ... ``` fences
    match = re.search(r'```(?:json)?\s*\n?(.*?)```', text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    # Try to find JSON array or object in the response
    if not text.startswith(('[', '{')):
        # Look for first [ or { in the text
        for i, c in enumerate(text):
            if c in ('[', '{'):
                text = text[i:]
                break
    # Find matching end
    if text.startswith('['):
        depth = 0
        for i, c in enumerate(text):
            if c == '[': depth += 1
            elif c == ']': depth -= 1
            if depth == 0:
                text = text[:i+1]
                break
    elif text.startswith('{'):
        depth = 0
        for i, c in enumerate(text):
            if c == '{': depth += 1
            elif c == '}': depth -= 1
            if depth == 0:
                text = text[:i+1]
                break
    return json.loads(text)


# ---------------------------------------------------------------------------
# OpenAlex client (Layer 1 — primary bulk search, no key needed)
# ---------------------------------------------------------------------------

class OpenAlexClient:
    """OpenAlex API — polite pool with mailto, cursor pagination."""

    def __init__(self, mailto: str = "user@example.com"):
        self.mailto = mailto
        self.session = requests.Session()
        # polite pool: ~10 req/s with mailto
        self._limiter = RateLimiter(max_calls=8, window_sec=1.0)

    def search(self, query: str, max_pages: int = 3, per_page: int = 100,
               year_from: int = 2020) -> list[dict]:
        """Cursor-paginated search. Returns up to max_pages * per_page results."""
        results = []
        cursor = "*"
        page = 0
        while cursor and page < max_pages:
            self._limiter.wait()
            params = {
                "search": query,
                "filter": f"from_publication_date:{year_from}-01-01,type:article|preprint",
                "select": "id,doi,title,publication_year,cited_by_count,authorships,"
                          "primary_location,abstract_inverted_index,concepts",
                "sort": "cited_by_count:desc",
                "per_page": per_page,
                "cursor": cursor,
                "mailto": self.mailto,
            }
            try:
                resp = self.session.get(OA_BASE, params=params, timeout=30)
                if resp.status_code == 429:
                    wait = 2 ** (page + 1)
                    log.warning(f"OpenAlex rate limited, backing off {wait}s")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                log.error(f"OpenAlex request failed: {e}")
                break

            works = data.get("results", [])
            if not works:
                break
            results.extend(works)
            cursor = data.get("meta", {}).get("next_cursor")
            page += 1
            log.debug(f"  OpenAlex '{query[:40]}': page {page}, got {len(works)}")

        return results

    @staticmethod
    def to_unified(work: dict) -> dict:
        """Convert OpenAlex work to unified paper schema."""
        # Reconstruct abstract from inverted index
        abstract = ""
        inv = work.get("abstract_inverted_index")
        if inv:
            word_positions = []
            for word, positions in inv.items():
                for pos in positions:
                    word_positions.append((pos, word))
            word_positions.sort()
            abstract = " ".join(w for _, w in word_positions)

        authors = []
        for a in work.get("authorships", [])[:10]:
            name = a.get("author", {}).get("display_name", "")
            if name:
                authors.append(name)

        loc = work.get("primary_location") or {}
        source = loc.get("source") or {}
        venue = source.get("display_name", "")

        doi_raw = work.get("doi") or ""
        doi = doi_raw.replace("https://doi.org/", "").strip() if doi_raw else None

        return {
            "paperId": work.get("id", ""),
            "doi": doi,
            "title": work.get("title", ""),
            "authors": authors,
            "year": work.get("publication_year") or 0,
            "venue": venue,
            "abstract": abstract,
            "citationCount": work.get("cited_by_count") or 0,
            "source": "openalex",
            "externalIds": {"OpenAlex": work.get("id", "")},
            "concepts": [c.get("display_name", "") for c in work.get("concepts", [])[:5]],
        }


# ---------------------------------------------------------------------------
# Semantic Scholar client (Layer 2 — citation graph only)
# ---------------------------------------------------------------------------

class S2Client:
    """Semantic Scholar API — used for citation chain expansion, not bulk search."""

    def __init__(self, api_key: str | None = None):
        self.session = requests.Session()
        if api_key:
            self.session.headers["x-api-key"] = api_key
            self._limiter = RateLimiter(max_calls=9, window_sec=1.0)
        else:
            # No key: 1 request per 5 seconds to avoid 429 storms
            self._limiter = RateLimiter(max_calls=1, window_sec=5.0)

    def _get(self, url: str, params: dict | None = None, _depth: int = 0) -> dict:
        self._limiter.wait()
        resp = self.session.get(url, params=params, timeout=30)
        if resp.status_code == 429:
            if _depth >= 5:
                log.error("S2 max retries exceeded")
                return {}
            wait = 3 * (2 ** _depth)  # 3s, 6s, 12s, 24s, 48s
            log.warning(f"S2 429, backing off {wait}s (attempt {_depth+1})")
            time.sleep(wait)
            return self._get(url, params, _depth + 1)
        resp.raise_for_status()
        return resp.json()

    def _post(self, url: str, json_body: dict, params: dict | None = None) -> dict:
        self._limiter.wait()
        resp = self.session.post(url, json=json_body, params=params, timeout=30)
        if resp.status_code == 429:
            time.sleep(5)
            return self._post(url, json_body, params)
        resp.raise_for_status()
        return resp.json()

    def search(self, query: str, limit: int = 100, fields: str = S2_FIELDS_DETAIL,
               year: str | None = None) -> list[dict]:
        """Paginated paper search."""
        results = []
        offset = 0
        while offset < limit:
            batch = min(100, limit - offset)
            params = {"query": query, "limit": batch, "offset": offset, "fields": fields}
            if year:
                params["year"] = year
            data = self._get(f"{S2_BASE}/paper/search", params)
            papers = data.get("data", [])
            if not papers:
                break
            results.extend(papers)
            if data.get("next") is None or len(papers) < batch:
                break
            offset += batch
        return results

    def get_paper(self, paper_id: str, fields: str = S2_FIELDS_DETAIL) -> dict | None:
        try:
            return self._get(f"{S2_BASE}/paper/{paper_id}", {"fields": fields})
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return None
            raise

    def get_references(self, paper_id: str, limit: int = 100,
                       fields: str = S2_FIELDS) -> list[dict]:
        """Get papers this paper cites."""
        data = self._get(
            f"{S2_BASE}/paper/{paper_id}/references",
            {"fields": fields, "limit": limit},
        )
        return [r.get("citedPaper", r) for r in data.get("data", [])]

    def get_citations(self, paper_id: str, limit: int = 100,
                      fields: str = S2_FIELDS) -> list[dict]:
        """Get papers that cite this paper."""
        data = self._get(
            f"{S2_BASE}/paper/{paper_id}/citations",
            {"fields": fields, "limit": limit},
        )
        return [c.get("citingPaper", c) for c in data.get("data", [])]

    def resolve_seed(self, lookup_query: str, doi: str | None = None) -> dict | None:
        """Resolve a seed paper: try DOI first, then search."""
        if doi:
            paper = self.get_paper(f"DOI:{doi}")
            if paper:
                return paper
        hits = self.search(lookup_query, limit=5)
        return hits[0] if hits else None

    @staticmethod
    def to_unified(paper: dict) -> dict:
        """Convert S2 response to unified schema."""
        authors = []
        for a in paper.get("authors", []):
            if isinstance(a, dict):
                authors.append(a.get("name", ""))
            elif isinstance(a, str):
                authors.append(a)

        tldr = paper.get("tldr")
        tldr_text = tldr.get("text", "") if isinstance(tldr, dict) else ""

        return {
            "paperId": paper.get("paperId", ""),
            "doi": (paper.get("externalIds") or {}).get("DOI"),
            "title": paper.get("title", ""),
            "authors": authors,
            "year": paper.get("year") or 0,
            "venue": paper.get("venue", ""),
            "abstract": paper.get("abstract", "") or "",
            "citationCount": paper.get("citationCount") or 0,
            "source": "s2",
            "externalIds": paper.get("externalIds") or {},
            "tldr": tldr_text,
        }


# ---------------------------------------------------------------------------
# arXiv client (Layer 3 — cutting-edge preprints)
# ---------------------------------------------------------------------------

class ArxivClient:
    """arXiv API — fully open, no key needed."""

    def __init__(self):
        self._limiter = RateLimiter(max_calls=1, window_sec=3.0)

    def search(self, query: str, max_results: int = 100) -> list[dict]:
        """Search arXiv. Query uses arXiv search syntax (all:, ti:, au:)."""
        self._limiter.wait()
        params = urllib.parse.urlencode({
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        })
        url = f"{ARXIV_BASE}?{params}"

        try:
            response = urllib.request.urlopen(url, timeout=30)
            root = ET.fromstring(response.read())
        except Exception as e:
            log.error(f"arXiv request failed: {e}")
            return []

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        results = []
        for entry in root.findall("atom:entry", ns):
            arxiv_id_raw = entry.find("atom:id", ns)
            if arxiv_id_raw is None:
                continue
            arxiv_id = arxiv_id_raw.text.split("/abs/")[-1]

            title_el = entry.find("atom:title", ns)
            abstract_el = entry.find("atom:summary", ns)
            published_el = entry.find("atom:published", ns)

            authors = [
                a.find("atom:name", ns).text
                for a in entry.findall("atom:author", ns)
                if a.find("atom:name", ns) is not None
            ]
            categories = [c.attrib.get("term", "") for c in entry.findall("atom:category", ns)]

            results.append({
                "arxiv_id": arxiv_id,
                "title": (title_el.text or "").strip().replace("\n", " ") if title_el is not None else "",
                "abstract": (abstract_el.text or "").strip().replace("\n", " ") if abstract_el is not None else "",
                "authors": authors[:10],
                "published": (published_el.text or "")[:10] if published_el is not None else "",
                "categories": categories,
            })

        log.debug(f"  arXiv '{query[:40]}': {len(results)} results")
        return results

    @staticmethod
    def to_unified(paper: dict) -> dict:
        """Convert arXiv result to unified schema."""
        year = 0
        pub = paper.get("published", "")
        if pub and len(pub) >= 4:
            try:
                year = int(pub[:4])
            except ValueError:
                pass

        return {
            "paperId": f"arxiv:{paper.get('arxiv_id', '')}",
            "doi": None,
            "title": paper.get("title", ""),
            "authors": paper.get("authors", []),
            "year": year,
            "venue": "arXiv",
            "abstract": paper.get("abstract", ""),
            "citationCount": 0,
            "source": "arxiv",
            "externalIds": {"ArXiv": paper.get("arxiv_id", "")},
        }
