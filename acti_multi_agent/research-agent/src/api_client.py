"""API clients: Anthropic agent_run() + OpenAlex + Semantic Scholar + arXiv."""

from __future__ import annotations

import json
import os
import time
import logging
from dataclasses import dataclass
from copy import deepcopy
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from .utils import RateLimiter

log = logging.getLogger("research_agent")

# Tiered model config: fast (high-volume) vs deep (low-volume, high-quality)
MODEL_FAST = os.getenv("MODEL_FAST", "claude-sonnet-4-6")
MODEL_DEEP = os.getenv("MODEL_DEEP", "claude-opus-4-6")
OPENAI_REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL", "gpt-5.4")
OPENAI_PROVIDER_FALLBACK_MODEL = os.getenv("OPENAI_PROVIDER_FALLBACK_MODEL", MODEL_DEEP)
DEFAULT_MODEL = MODEL_FAST  # backward compat
S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "paperId,title,year,abstract,citationCount,venue,authors,externalIds"
# tldr not supported on references/citations endpoints — only on paper search/details
S2_FIELDS_DETAIL = "paperId,title,year,abstract,citationCount,venue,authors,externalIds,tldr"
OA_BASE = "https://api.openalex.org/works"
ARXIV_BASE = "http://export.arxiv.org/api/query"
CROSSREF_BASE = "https://api.crossref.org"
OPENCITATIONS_INDEX_BASE = "https://api.opencitations.net/index/v2"
CONSENSUS_BASE = os.getenv("CONSENSUS_BASE_URL", "https://api.consensus.app")
LENS_BASE = "https://api.lens.org"


@dataclass(frozen=True)
class ModelSpec:
    """Provider-agnostic model selection."""

    name: str
    reasoning_effort: str | None = None


# Claude remains the extraction backbone.
BRAIN_FAST = ModelSpec(MODEL_FAST)
BRAIN_DEEP = ModelSpec(MODEL_DEEP)

# GPT-5.4 reasoning tiers for analysis / review work.
BRAIN_GPT_MEDIUM = ModelSpec(
    OPENAI_REASONING_MODEL,
    os.getenv("OPENAI_REASONING_MEDIUM", "medium"),
)
BRAIN_GPT_LOW = ModelSpec(
    OPENAI_REASONING_MODEL,
    os.getenv("OPENAI_REASONING_LOW", "low"),
)
BRAIN_GPT_HIGH = ModelSpec(
    OPENAI_REASONING_MODEL,
    os.getenv("OPENAI_REASONING_HIGH", "high"),
)
BRAIN_GPT_XHIGH = ModelSpec(
    OPENAI_REASONING_MODEL,
    os.getenv("OPENAI_REASONING_XHIGH", "xhigh"),
)

# Task-level brains.
BRAIN_PHASE2_CLASSIFIER = BRAIN_FAST
BRAIN_PHASE2_DEEP_EXTRACTOR = BRAIN_DEEP
BRAIN_PHASE3_RELATIONSHIP = BRAIN_GPT_LOW
BRAIN_PHASE3_GAP = BRAIN_GPT_MEDIUM
BRAIN_PHASE3_NARRATIVE = BRAIN_GPT_MEDIUM
BRAIN_PHASE3_CONTRADICTION = BRAIN_GPT_MEDIUM
BRAIN_PHASE4_EVIDENCE = BRAIN_GPT_MEDIUM

REVIEWER_BRAINS = {
    "narrative": BRAIN_GPT_MEDIUM,
    "contradiction": BRAIN_GPT_MEDIUM,
    "gap": BRAIN_GPT_MEDIUM,
    "coverage": BRAIN_GPT_LOW,
    "honesty": BRAIN_GPT_MEDIUM,
}


# ---------------------------------------------------------------------------
# Custom exceptions for clear error reporting
# ---------------------------------------------------------------------------

class APIKeyMissing(RuntimeError):
    """Raised when no API key is configured for a required service."""

class QuotaExhausted(RuntimeError):
    """Raised when API quota/credits are exhausted — retrying won't help."""

class ModelNotFound(RuntimeError):
    """Raised when the requested model ID doesn't exist or isn't accessible."""


# ---------------------------------------------------------------------------
# Runtime telemetry
# ---------------------------------------------------------------------------

_USAGE_PROVIDERS = (
    "anthropic",
    "openai",
    "s2",
    "openalex",
    "lens",
    "crossref",
    "opencitations",
    "arxiv",
)


def _empty_usage_payload() -> dict:
    return {
        "api_calls": {provider: 0 for provider in _USAGE_PROVIDERS},
        "tokens": {"input": 0, "output": 0, "total": 0},
        "estimated_cost_usd": 0.0,
    }


_USAGE_TOTALS = _empty_usage_payload()
_USAGE_PENDING = _empty_usage_payload()


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw in (None, ""):
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _cost_rates(provider: str, model_name: str | None = None) -> tuple[float, float]:
    model = (model_name or "").lower()
    if provider == "anthropic":
        if "opus" in model:
            return (
                _env_float("ANTHROPIC_OPUS_INPUT_COST_PER_1M", 15.0),
                _env_float("ANTHROPIC_OPUS_OUTPUT_COST_PER_1M", 75.0),
            )
        return (
            _env_float("ANTHROPIC_SONNET_INPUT_COST_PER_1M", 3.0),
            _env_float("ANTHROPIC_SONNET_OUTPUT_COST_PER_1M", 15.0),
        )
    if provider == "openai":
        return (
            _env_float("OPENAI_INPUT_COST_PER_1M", _env_float("GENERIC_LLM_INPUT_COST_PER_1M", 3.0)),
            _env_float("OPENAI_OUTPUT_COST_PER_1M", _env_float("GENERIC_LLM_OUTPUT_COST_PER_1M", 15.0)),
        )
    return (0.0, 0.0)


def _estimate_cost(provider: str, input_tokens: int, output_tokens: int, model_name: str | None = None) -> float:
    input_rate, output_rate = _cost_rates(provider, model_name)
    return (
        (max(0, input_tokens) / 1_000_000.0) * input_rate
        + (max(0, output_tokens) / 1_000_000.0) * output_rate
    )


def _record_usage(provider: str, api_calls: int = 0, input_tokens: int = 0,
                  output_tokens: int = 0, model_name: str | None = None):
    if provider not in _USAGE_PROVIDERS:
        return

    total_tokens = max(0, input_tokens) + max(0, output_tokens)
    estimated_cost = _estimate_cost(provider, input_tokens, output_tokens, model_name)

    for payload in (_USAGE_TOTALS, _USAGE_PENDING):
        payload["api_calls"][provider] += max(0, api_calls)
        payload["tokens"]["input"] += max(0, input_tokens)
        payload["tokens"]["output"] += max(0, output_tokens)
        payload["tokens"]["total"] += total_tokens
        payload["estimated_cost_usd"] = round(payload["estimated_cost_usd"] + estimated_cost, 6)


def drain_usage_delta() -> dict:
    """Return usage recorded since the last drain and reset the pending buffer."""
    global _USAGE_PENDING
    delta = deepcopy(_USAGE_PENDING)
    _USAGE_PENDING = _empty_usage_payload()
    return delta


# ---------------------------------------------------------------------------
# Anthropic wrappers
# ---------------------------------------------------------------------------

# Errors that should NOT be retried — fail fast
_FATAL_STATUS_CODES = {401, 403, 404}

def _coerce_model_spec(model: str | ModelSpec) -> ModelSpec:
    return model if isinstance(model, ModelSpec) else ModelSpec(model)


def _is_openai_model(model: str) -> bool:
    return model.startswith("gpt-")


def _extract_openai_output_text(data: dict) -> str:
    parts = []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    return "".join(parts).strip()


def _downgrade_openai_reasoning(spec: ModelSpec) -> ModelSpec | None:
    if spec.reasoning_effort == "xhigh":
        return ModelSpec(spec.name, "high")
    if spec.reasoning_effort == "high":
        return ModelSpec(spec.name, "medium")
    if spec.reasoning_effort == "medium":
        return ModelSpec(spec.name, "low")
    return None


def _openai_provider_fallback_spec(client, spec: ModelSpec) -> ModelSpec | None:
    """Use Anthropic when OpenAI quota is exhausted, if available."""
    fallback_name = (OPENAI_PROVIDER_FALLBACK_MODEL or "").strip()
    if not fallback_name or _is_openai_model(fallback_name):
        return None
    if client is not None or os.environ.get("ANTHROPIC_API_KEY"):
        return ModelSpec(fallback_name)
    return None


def _agent_run_via_openai(spec: ModelSpec, role: str, task: str, max_tokens: int) -> str:
    """Reasoning path via OpenAI Responses API."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise APIKeyMissing("OPENAI_API_KEY not set in .env")

    body = {
        "model": spec.name,
        "instructions": role,
        "input": task,
        "max_output_tokens": max_tokens,
    }
    if spec.reasoning_effort:
        body["reasoning"] = {"effort": spec.reasoning_effort}

    resp = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=body,
        timeout=180,
    )

    if resp.status_code == 404:
        raise ModelNotFound(
            f"OpenAI model '{spec.name}' not found. "
            f"Check OPENAI_REASONING_MODEL in .env. Original error: {resp.text[:300]}"
        )
    if resp.status_code in (401, 403):
        raise APIKeyMissing(
            f"OpenAI API authentication failed (HTTP {resp.status_code}). "
            f"Check OPENAI_API_KEY in .env. Original error: {resp.text[:300]}"
        )
    if resp.status_code == 429:
        raise QuotaExhausted(
            f"OpenAI API rate limited or quota exhausted (HTTP 429). "
            f"Original error: {resp.text[:300]}"
        )
    if resp.status_code >= 500:
        raise RuntimeError(f"OpenAI Responses API server error (HTTP {resp.status_code}): {resp.text[:300]}")

    resp.raise_for_status()
    data = resp.json()
    usage = data.get("usage") or {}
    _record_usage(
        "openai",
        api_calls=1,
        input_tokens=int(usage.get("input_tokens", 0) or 0),
        output_tokens=int(usage.get("output_tokens", 0) or 0),
        model_name=spec.name,
    )
    text = _extract_openai_output_text(data)
    if text:
        return text
    output_types = [item.get("type") for item in data.get("output", [])[:5]]
    raise RuntimeError(
        "OpenAI response missing output text. "
        f"Status={data.get('status')} "
        f"incomplete_details={data.get('incomplete_details')} "
        f"output_types={output_types}"
    )


def _agent_run_via_rest(role: str, task: str, model: str, max_tokens: int) -> str:
    """Fallback path for Anthropic when the Python SDK is blocked in this environment."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise APIKeyMissing("ANTHROPIC_API_KEY not set in .env")
    timeout_sec = int(os.environ.get("ANTHROPIC_REST_TIMEOUT_SEC", "180"))

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "system": role,
        "messages": [{"role": "user", "content": task}],
    }
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=body,
        timeout=timeout_sec,
    )

    if resp.status_code == 404:
        raise ModelNotFound(
            f"Model '{model}' not found. Check MODEL_FAST / MODEL_DEEP in .env. "
            f"Original error: {resp.text[:300]}"
        )
    if resp.status_code in (401, 403):
        raise APIKeyMissing(
            f"Anthropic API authentication failed (HTTP {resp.status_code}). "
            f"Original error: {resp.text[:300]}"
        )
    if resp.status_code == 529:
        raise QuotaExhausted(
            f"Anthropic API overloaded (HTTP 529). Try again later. "
            f"Original error: {resp.text[:300]}"
        )

    resp.raise_for_status()
    data = resp.json()
    usage = data.get("usage") or {}
    _record_usage(
        "anthropic",
        api_calls=1,
        input_tokens=int(usage.get("input_tokens", 0) or 0),
        output_tokens=int(usage.get("output_tokens", 0) or 0),
        model_name=model,
    )
    parts = data.get("content", [])
    text_parts = [p.get("text", "") for p in parts if p.get("type") == "text"]
    return "".join(text_parts).strip()


def agent_run(client, role: str, task: str, model: str | ModelSpec = DEFAULT_MODEL,
              max_tokens: int = 4096, retries: int = 3) -> str:
    """Single agent call with retry + exponential backoff.

    Distinguishes fatal errors (wrong key, wrong model, quota gone) from
    transient errors (network, rate limit) and only retries the latter.
    """
    spec = _coerce_model_spec(model)

    if _is_openai_model(spec.name):
        for attempt in range(retries):
            try:
                return _agent_run_via_openai(spec, role=role, task=task, max_tokens=max_tokens)
            except QuotaExhausted as e:
                provider_fallback = _openai_provider_fallback_spec(client, spec)
                if provider_fallback is not None:
                    log.warning(
                        "OpenAI quota exhausted for %s effort=%s; falling back to Anthropic model %s",
                        spec.name,
                        spec.reasoning_effort,
                        provider_fallback.name,
                    )
                    return agent_run(
                        client,
                        role,
                        task,
                        model=provider_fallback,
                        max_tokens=max_tokens,
                        retries=retries,
                    )
                raise e
            except (APIKeyMissing, ModelNotFound):
                raise
            except Exception as e:
                wait = 2 ** attempt
                remaining = retries - attempt - 1
                log.warning(
                    f"openai agent_run attempt {attempt+1}/{retries} failed: {e}. "
                    f"{'Retrying in ' + str(wait) + 's' if remaining > 0 else 'No retries left'}..."
                )
                if remaining > 0:
                    time.sleep(wait)
        fallback = _downgrade_openai_reasoning(spec)
        if fallback is not None:
            log.warning(
                f"OpenAI reasoning fallback: {spec.name} effort={spec.reasoning_effort} "
                f"-> effort={fallback.reasoning_effort}"
            )
            return agent_run(client, role, task, model=fallback, max_tokens=max_tokens, retries=retries)
        raise RuntimeError(
            f"OpenAI agent_run failed after {retries} retries. Last model: {spec.name}. "
            f"State has been saved — you can resume with --resume."
        )

    if client is None:
        if os.environ.get("ANTHROPIC_API_KEY"):
            return _agent_run_via_rest(role=role, task=task, model=spec.name, max_tokens=max_tokens)
        raise APIKeyMissing(
            "Anthropic client is None — ANTHROPIC_API_KEY not set in .env. "
            "Phase 1 works without it: python main.py --phase 1"
        )

    for attempt in range(retries):
        try:
            resp = client.messages.create(
                model=spec.name,
                max_tokens=max_tokens,
                system=role,
                messages=[{"role": "user", "content": task}],
            )
            usage = getattr(resp, "usage", None)
            _record_usage(
                "anthropic",
                api_calls=1,
                input_tokens=int(getattr(usage, "input_tokens", 0) or 0) if usage is not None else 0,
                output_tokens=int(getattr(usage, "output_tokens", 0) or 0) if usage is not None else 0,
                model_name=spec.name,
            )
            return resp.content[0].text
        except Exception as e:
            err_str = str(e)
            status = getattr(e, "status_code", None)

            # In this environment the official SDK may be blocked while direct REST works.
            if "blocked" in err_str.lower():
                log.warning("Anthropic SDK call was blocked; retrying via REST fallback")
                return _agent_run_via_rest(role=role, task=task, model=spec.name, max_tokens=max_tokens)

            # --- Fatal: wrong model ID ---
            if status == 404 or "not_found" in err_str.lower():
                raise ModelNotFound(
                    f"Model '{spec.name}' not found. Check MODEL_FAST / MODEL_DEEP in .env. "
                    f"Available: claude-sonnet-4-6, claude-opus-4-6. "
                    f"Original error: {e}"
                ) from e

            # --- Fatal: bad key or no permission ---
            if status in (401, 403):
                raise APIKeyMissing(
                    f"Anthropic API authentication failed (HTTP {status}). "
                    f"Check ANTHROPIC_API_KEY in .env. Original error: {e}"
                ) from e

            # --- Fatal: quota / credits exhausted ---
            if status == 529 or "overloaded" in err_str.lower():
                raise QuotaExhausted(
                    f"Anthropic API overloaded (HTTP 529). Try again later. "
                    f"Original error: {e}"
                ) from e
            if "额度" in err_str or "quota" in err_str.lower() or "insufficient" in err_str.lower():
                raise QuotaExhausted(
                    f"API quota exhausted. Check your billing at console.anthropic.com. "
                    f"Original error: {e}"
                ) from e

            # --- Transient: rate limit, network, etc — retry ---
            wait = 2 ** attempt
            remaining = retries - attempt - 1
            log.warning(
                f"agent_run attempt {attempt+1}/{retries} failed: {e}. "
                f"{'Retrying in ' + str(wait) + 's' if remaining > 0 else 'No retries left'}..."
            )
            if remaining > 0:
                time.sleep(wait)

    raise RuntimeError(
        f"agent_run failed after {retries} retries. Last model: {spec.name}. "
        f"State has been saved — you can resume with --resume."
    )


def agent_run_json(client, role: str, task: str, model: str | ModelSpec = DEFAULT_MODEL,
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
    candidates = []
    for candidate in (
        text,
        _extract_balanced_json_snippet(text),
        _trim_to_last_json_closer(text),
    ):
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    last_error = None
    for candidate in candidates:
        for repaired in (candidate, _close_unbalanced_json(candidate)):
            if not repaired:
                continue
            try:
                return json.loads(repaired)
            except Exception as e:
                last_error = e

    raise last_error or ValueError("agent_run_json could not parse a valid JSON payload")


def _extract_balanced_json_snippet(text: str) -> str:
    """Return the first balanced JSON object/array substring if available."""
    if not text:
        return ""

    start = next((i for i, ch in enumerate(text) if ch in "[{"), -1)
    if start == -1:
        return ""

    stack = []
    in_string = False
    escape = False
    for i, ch in enumerate(text[start:], start):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch in "[{":
            stack.append("]" if ch == "[" else "}")
        elif ch in "]}":
            if not stack or ch != stack[-1]:
                return ""
            stack.pop()
            if not stack:
                return text[start:i + 1]
    return ""


def _trim_to_last_json_closer(text: str) -> str:
    """Trim trailing commentary after the last JSON closer."""
    last = max(text.rfind("}"), text.rfind("]"))
    return text[:last + 1] if last != -1 else ""


def _close_unbalanced_json(text: str) -> str:
    """Append missing closing tokens for mildly truncated JSON."""
    if not text:
        return ""

    stack = []
    in_string = False
    escape = False
    for ch in text:
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch in "[{":
            stack.append("]" if ch == "[" else "}")
        elif ch in "]}":
            if stack and ch == stack[-1]:
                stack.pop()

    repaired = text
    if in_string:
        repaired += '"'
    if stack:
        repaired += "".join(reversed(stack))
    return repaired


# ---------------------------------------------------------------------------
# OpenAlex client (Layer 1 — primary bulk search, no key needed)
# ---------------------------------------------------------------------------

class OpenAlexClient:
    """OpenAlex API — polite pool with mailto, cursor pagination."""

    def __init__(self, mailto: str = "user@example.com", api_key: str | None = None):
        self.mailto = mailto
        self.api_key = api_key
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
            if self.api_key:
                params["api_key"] = self.api_key
            try:
                resp = self.session.get(OA_BASE, params=params, timeout=30)
                _record_usage("openalex", api_calls=1)
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
            "source_ids": {
                "openalex": work.get("id", ""),
                **({"doi": doi} if doi else {}),
            },
            "concepts": [c.get("display_name", "") for c in work.get("concepts", [])[:5]],
        }


# ---------------------------------------------------------------------------
# Crossref client (DOI authority / metadata integrity)
# ---------------------------------------------------------------------------

class CrossrefClient:
    """Crossref REST API — DOI authority and metadata enrichment."""

    def __init__(self, mailto: str = "user@example.com", tool_name: str = "research-agent",
                 plus_token: str | None = None):
        self.mailto = mailto
        self.tool_name = tool_name
        self.session = requests.Session()
        self.session.headers["User-Agent"] = f"{tool_name}/1.0 ({mailto})"
        if plus_token:
            self.session.headers["Crossref-Plus-API-Token"] = f"Bearer {plus_token}"
        self._limiter = RateLimiter(max_calls=20, window_sec=1.0)

    def _get(self, path: str, params: dict | None = None) -> dict:
        self._limiter.wait()
        query = dict(params or {})
        if self.mailto:
            query.setdefault("mailto", self.mailto)
        resp = self.session.get(f"{CROSSREF_BASE}{path}", params=query, timeout=30)
        _record_usage("crossref", api_calls=1)
        resp.raise_for_status()
        return resp.json()

    def get_work(self, doi: str) -> dict | None:
        norm = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
        if not norm:
            return None
        try:
            data = self._get(f"/works/{urllib.parse.quote(norm, safe='')}")
            return data.get("message")
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return None
            raise

    def search_works(self, query: str, rows: int = 5) -> list[dict]:
        data = self._get("/works", {"query.bibliographic": query, "rows": rows})
        return data.get("message", {}).get("items", [])


# ---------------------------------------------------------------------------
# OpenCitations client (citation/reference fallback)
# ---------------------------------------------------------------------------

class OpenCitationsClient:
    """OpenCitations Index API — DOI to DOI citation fallback."""

    def __init__(self, access_token: str | None = None):
        self.session = requests.Session()
        self.timeout_sec = float(os.getenv("OPENCITATIONS_TIMEOUT_SEC", "15"))
        if access_token:
            self.session.headers["authorization"] = access_token
            self.session.headers["access-token"] = access_token
        self._limiter = RateLimiter(max_calls=5, window_sec=1.0)

    def _get(self, path: str) -> list[dict]:
        self._limiter.wait()
        resp = self.session.get(
            f"{OPENCITATIONS_INDEX_BASE}{path}",
            timeout=(5, self.timeout_sec),
        )
        _record_usage("opencitations", api_calls=1)
        resp.raise_for_status()
        return resp.json()

    def get_references(self, doi: str) -> list[dict]:
        norm = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
        if not norm:
            return []
        return self._get(f"/references/{urllib.parse.quote(f'doi:{norm}', safe=':')}")

    def get_citations(self, doi: str) -> list[dict]:
        norm = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
        if not norm:
            return []
        return self._get(f"/citations/{urllib.parse.quote(f'doi:{norm}', safe=':')}")


# ---------------------------------------------------------------------------
# Consensus client (claim verification / honesty support)
# ---------------------------------------------------------------------------

class ConsensusClient:
    """Consensus API client used as a claim verification layer."""

    def __init__(self, api_key: str, base_url: str | None = None):
        self.base_url = (base_url or CONSENSUS_BASE).rstrip("/")
        self.session = requests.Session()
        self.session.headers["x-api-key"] = api_key
        self.timeout = (5, 30)

    def quick_search(self, query: str, limit: int = 8) -> dict:
        params_candidates = [
            {"query": query, "limit": limit},
            {"q": query, "limit": limit},
        ]
        last_error = None
        for params in params_candidates:
            try:
                resp = self.session.get(
                    f"{self.base_url}/v1/quick_search",
                    params=params,
                    timeout=self.timeout,
                )
                if resp.status_code == 401:
                    raise APIKeyMissing("Consensus API authentication failed. Check CONSENSUS_API_KEY.")
                if resp.status_code == 403:
                    raise APIKeyMissing("Consensus API rejected this key or lacks access for quick_search.")
                if resp.status_code == 404:
                    last_error = RuntimeError("Consensus quick_search endpoint not found.")
                    continue
                if resp.status_code == 429:
                    raise QuotaExhausted("Consensus API rate limited or quota exhausted.")
                if resp.status_code >= 400:
                    last_error = RuntimeError(
                        f"Consensus quick_search failed (HTTP {resp.status_code}): {resp.text[:300]}"
                    )
                    continue
                return resp.json()
            except requests.RequestException as e:
                last_error = e
        raise RuntimeError(f"Consensus quick_search failed: {last_error}")

    def summarize_quick_search(self, payload: dict) -> dict:
        hits = self._extract_hits(payload)
        top_hits = []
        for item in hits[:5]:
            top_hits.append({
                "title": self._pick(item, "title", "paper_title", "name"),
                "year": self._pick(item, "year", "publication_year"),
                "journal": self._pick(item, "journal", "venue", "publication_name"),
                "authors": self._normalize_authors(item.get("authors")),
                "doi": self._pick(item, "doi", "DOI"),
                "url": self._pick(item, "url", "paper_url", "link"),
            })
        return {
            "result_count": len(hits),
            "top_hits": top_hits,
            "raw_keys": sorted(payload.keys()) if isinstance(payload, dict) else [],
        }

    def _extract_hits(self, payload: dict) -> list[dict]:
        if not isinstance(payload, dict):
            return []
        for key in ("results", "papers", "data", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return []

    @staticmethod
    def _pick(item: dict, *keys):
        for key in keys:
            value = item.get(key)
            if value not in (None, "", []):
                return value
        return ""

    @staticmethod
    def _normalize_authors(value):
        if isinstance(value, list):
            names = []
            for author in value:
                if isinstance(author, str):
                    names.append(author)
                elif isinstance(author, dict):
                    names.append(author.get("name", ""))
            return [name for name in names if name][:6]
        return []


# ---------------------------------------------------------------------------
# Lens client (targeted scholarly supplementation)
# ---------------------------------------------------------------------------

class LensClient:
    """Lens Scholarly Works API used as a targeted coverage supplement."""

    def __init__(self, api_key: str | None = None):
        self.api_key = (api_key or "").strip()
        self.session = requests.Session()
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
            self.session.headers["Accept"] = "application/json"
        # Institutional user plan: 10 requests / minute
        self._limiter = RateLimiter(max_calls=8, window_sec=60.0)

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, size: int = 50) -> list[dict]:
        if not self.enabled:
            return []
        self._limiter.wait()
        body = {"query": query, "size": max(1, min(size, 100))}
        resp = self.session.post(f"{LENS_BASE}/scholarly/search", json=body, timeout=60)
        _record_usage("lens", api_calls=1)
        if resp.status_code == 401:
            raise APIKeyMissing("Lens API authentication failed. Check LENS_API_KEY in .env.")
        if resp.status_code == 403:
            raise APIKeyMissing("Lens API key lacks access to scholarly search.")
        if resp.status_code == 429:
            raise QuotaExhausted("Lens API rate limited. Reduce query volume and retry later.")
        resp.raise_for_status()
        data = resp.json()
        return [item for item in data.get("data", []) if isinstance(item, dict)]

    def usage(self) -> list[dict]:
        if not self.enabled:
            return []
        self._limiter.wait()
        resp = self.session.get(f"{LENS_BASE}/subscriptions/scholarly_api/usage", timeout=30)
        _record_usage("lens", api_calls=1)
        if resp.status_code == 401:
            raise APIKeyMissing("Lens scholarly usage endpoint rejected this key.")
        resp.raise_for_status()
        payload = resp.json()
        return payload if isinstance(payload, list) else []

    @staticmethod
    def to_unified(work: dict) -> dict:
        external_ids = {}
        for item in work.get("external_ids", []) or []:
            if not isinstance(item, dict):
                continue
            key = (item.get("type") or "").strip()
            value = (item.get("value") or "").strip()
            if key and value:
                external_ids[key] = value

        authors = []
        for author in work.get("authors", [])[:10]:
            if not isinstance(author, dict):
                continue
            parts = [
                author.get("first_name", "").strip(),
                author.get("last_name", "").strip(),
            ]
            name = " ".join(p for p in parts if p).strip()
            if not name:
                initials = author.get("initials", "").strip()
                last_name = author.get("last_name", "").strip()
                name = " ".join(p for p in (initials, last_name) if p).strip()
            if name:
                authors.append(name)

        source = work.get("source") or {}
        open_access = work.get("open_access") or {}
        locations = open_access.get("locations") or {}
        pdf_urls = locations.get("pdf_urls") or []
        oa_pdf = pdf_urls[0] if pdf_urls else ""

        doi = external_ids.get("doi") or None
        openalex = external_ids.get("openalex") or None
        arxiv = external_ids.get("arxiv") or external_ids.get("ArXiv") or None
        lens_id = work.get("lens_id", "")

        return {
            "paperId": f"lens:{lens_id}" if lens_id else "",
            "doi": doi,
            "title": work.get("title", ""),
            "authors": authors,
            "year": work.get("year_published") or 0,
            "venue": source.get("title", "") if isinstance(source, dict) else "",
            "abstract": work.get("abstract", "") or "",
            "citationCount": work.get("scholarly_citations_count") or work.get("referenced_by_count") or 0,
            "source": "lens",
            "externalIds": external_ids,
            "source_ids": {
                "lens": lens_id,
                **({"doi": doi} if doi else {}),
                **({"openalex": openalex} if openalex else {}),
                **({"arxiv": arxiv} if arxiv else {}),
            },
            "openAccessPdf": oa_pdf,
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
        _record_usage("s2", api_calls=1)
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
        _record_usage("s2", api_calls=1)
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
            "source_ids": {
                "s2": paper.get("paperId", ""),
                **(
                    {"doi": (paper.get("externalIds") or {}).get("DOI")}
                    if (paper.get("externalIds") or {}).get("DOI")
                    else {}
                ),
                **(
                    {"arxiv": (paper.get("externalIds") or {}).get("ArXiv")}
                    if (paper.get("externalIds") or {}).get("ArXiv")
                    else {}
                ),
            },
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
            _record_usage("arxiv", api_calls=1)
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
            "source_ids": {
                "arxiv": paper.get("arxiv_id", ""),
            },
        }
