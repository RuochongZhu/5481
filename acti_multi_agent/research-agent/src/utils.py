"""Shared utilities: rate limiting, logging, file I/O."""

from __future__ import annotations

import json
import os
import time
import logging
from collections import deque
from pathlib import Path


class RateLimiter:
    """Sliding-window rate limiter."""

    def __init__(self, max_calls: int = 100, window_sec: float = 300.0):
        self.max_calls = max_calls
        self.window_sec = window_sec
        self._timestamps: deque = deque()

    def wait(self):
        now = time.time()
        # Purge timestamps outside the window
        while self._timestamps and self._timestamps[0] < now - self.window_sec:
            self._timestamps.popleft()
        if len(self._timestamps) >= self.max_calls:
            sleep_for = self._timestamps[0] + self.window_sec - now + 0.1
            logging.info(f"Rate limit reached, sleeping {sleep_for:.1f}s")
            time.sleep(sleep_for)
        self._timestamps.append(time.time())


def setup_logging(log_dir: str, phase: int | None = None) -> logging.Logger:
    """Configure file + console logging."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    suffix = f"_phase{phase}" if phase else ""
    log_file = os.path.join(log_dir, f"run_{ts}{suffix}.log")

    logger = logging.getLogger("research_agent")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def atomic_write_json(filepath: str, data) -> None:
    """Write JSON atomically: write to .tmp then rename."""
    tmp = filepath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, filepath)


def load_json(filepath: str):
    """Load JSON file with error handling."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
