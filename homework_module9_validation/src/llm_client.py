"""Anthropic Claude client wrapper with retry/error classification.

Patterned after carpool_v4/src/api_client.py but simplified for this homework:
only Anthropic SDK, only chat completions, no Semantic Scholar / OpenAlex / etc.
"""
from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from typing import Optional

import anthropic

from .config import (
    BASE_BACKOFF_SEC,
    GEN_MAX_TOKENS,
    GEN_MODEL,
    GEN_TEMPERATURE,
    MAX_RETRIES,
    REVIEW_MAX_TOKENS,
    REVIEW_MODEL,
    REVIEW_TEMPERATURE,
)

log = logging.getLogger("hw_validator")


class APIKeyMissing(RuntimeError):
    """ANTHROPIC_API_KEY not in env."""


class TransientAPIError(RuntimeError):
    """Retry-eligible API error (rate limit, server overload)."""


class PermanentAPIError(RuntimeError):
    """Non-retryable API error (auth, invalid model, bad request)."""


@dataclass
class LLMResponse:
    text: str
    model: str
    usage: dict


def _client() -> anthropic.Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise APIKeyMissing(
            "ANTHROPIC_API_KEY not set. Ensure .env is present in the project "
            "root or one of the search paths in config._load_env()."
        )
    return anthropic.Anthropic(api_key=key)


def _classify_error(err: Exception) -> Exception:
    msg = str(err).lower()
    if isinstance(err, anthropic.APIStatusError):
        status = getattr(err, "status_code", None)
        if status == 429 or status == 529 or status in (500, 502, 503, 504):
            return TransientAPIError(f"Transient API error: {err}")
        if status in (401, 403):
            return PermanentAPIError(f"Auth error: {err}")
        if status == 404 or "model" in msg and "not" in msg:
            return PermanentAPIError(f"Model not found / 404: {err}")
        if status == 400:
            return PermanentAPIError(f"Bad request: {err}")
    if isinstance(err, (anthropic.APIConnectionError, anthropic.APITimeoutError)):
        return TransientAPIError(f"Connection/timeout: {err}")
    return TransientAPIError(f"Unknown API error: {err}")


def call_llm(
    *,
    system_prompt: str,
    user_message: str,
    model: str,
    temperature: float,
    max_tokens: int,
    retries: int = MAX_RETRIES,
) -> LLMResponse:
    """Call Anthropic Messages API with retry + error classification.

    Raises PermanentAPIError or TransientAPIError after `retries` failed attempts.
    """
    client = _client()
    last_err: Optional[Exception] = None
    for attempt in range(retries):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            text_blocks = [b.text for b in resp.content if hasattr(b, "text")]
            text = "\n".join(text_blocks).strip()
            usage = {
                "input_tokens": resp.usage.input_tokens,
                "output_tokens": resp.usage.output_tokens,
            }
            return LLMResponse(text=text, model=model, usage=usage)
        except anthropic.AnthropicError as e:
            classified = _classify_error(e)
            last_err = classified
            if isinstance(classified, PermanentAPIError):
                log.error("Permanent API error on attempt %d: %s", attempt + 1, classified)
                raise classified
            backoff = BASE_BACKOFF_SEC * (2 ** attempt)
            log.warning("Transient API error on attempt %d (sleeping %.1fs): %s",
                        attempt + 1, backoff, classified)
            time.sleep(backoff)
        except Exception as e:
            last_err = _classify_error(e)
            backoff = BASE_BACKOFF_SEC * (2 ** attempt)
            log.warning("Unexpected error on attempt %d (sleeping %.1fs): %s",
                        attempt + 1, backoff, e)
            time.sleep(backoff)
    raise last_err or TransientAPIError("Exhausted retries with no recorded error")


def call_generator(*, system_prompt: str, user_message: str) -> LLMResponse:
    return call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        model=GEN_MODEL,
        temperature=GEN_TEMPERATURE,
        max_tokens=GEN_MAX_TOKENS,
    )


def call_reviewer(*, system_prompt: str, user_message: str) -> LLMResponse:
    return call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        model=REVIEW_MODEL,
        temperature=REVIEW_TEMPERATURE,
        max_tokens=REVIEW_MAX_TOKENS,
    )
