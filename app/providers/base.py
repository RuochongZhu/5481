from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class EarthquakeProvider(ABC):
    """Provider interface so more earthquake data sources can be plugged in later."""

    @abstractmethod
    def fetch_events(
        self,
        *,
        starttime: str,
        endtime: str,
        minmagnitude: float,
        limit: int,
        orderby: str,
    ) -> dict[str, Any]:
        raise NotImplementedError
