from __future__ import annotations

import time
from datetime import datetime
from typing import Any

import requests

from .base import EarthquakeProvider


class USGSEarthquakeProvider(EarthquakeProvider):
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    _cache_ttl_seconds = 60
    _cache: dict[tuple[tuple[str, Any], ...], tuple[float, dict[str, Any]]] = {}

    @classmethod
    def _cache_key(cls, params: dict[str, Any]) -> tuple[tuple[str, Any], ...]:
        return tuple(sorted(params.items()))

    def fetch_events(
        self,
        *,
        starttime: str,
        endtime: str,
        minmagnitude: float,
        limit: int,
        orderby: str,
    ) -> dict[str, Any]:
        params = {
            "format": "geojson",
            "starttime": starttime,
            "endtime": endtime,
            "minmagnitude": minmagnitude,
            "limit": limit,
            "orderby": orderby,
        }

        key = self._cache_key(params)
        now_ts = time.time()
        cached = self._cache.get(key)
        if cached and now_ts - cached[0] <= self._cache_ttl_seconds:
            return cached[1]

        response = None
        for attempt in range(3):
            response = requests.get(self.base_url, params=params, timeout=30)
            if response.status_code != 429:
                break
            retry_after = response.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                wait_seconds = min(int(retry_after), 10)
            else:
                wait_seconds = min(2**attempt, 4)
            time.sleep(wait_seconds)

        assert response is not None
        response.raise_for_status()

        payload = response.json()
        features = payload.get("features", [])

        events: list[dict[str, Any]] = []
        for item in features:
            props = item.get("properties", {})
            coords = item.get("geometry", {}).get("coordinates", [None, None, None])
            ts_ms = props.get("time")
            event_time = (
                datetime.utcfromtimestamp(ts_ms / 1000).isoformat() + "Z" if ts_ms else None
            )
            events.append(
                {
                    "id": item.get("id"),
                    "magnitude": props.get("mag"),
                    "place": props.get("place"),
                    "time": event_time,
                    "tsunami": bool(props.get("tsunami")),
                    "type": props.get("type"),
                    "url": props.get("url"),
                    "longitude": coords[0],
                    "latitude": coords[1],
                    "depth_km": coords[2],
                }
            )

        magnitudes = [e["magnitude"] for e in events if isinstance(e.get("magnitude"), (int, float))]
        summary = {
            "count": len(events),
            "max_magnitude": max(magnitudes) if magnitudes else None,
            "min_magnitude": min(magnitudes) if magnitudes else None,
            "avg_magnitude": round(sum(magnitudes) / len(magnitudes), 2) if magnitudes else None,
        }

        result = {
            "provider": "usgs",
            "meta": {
                "requested": params,
                "source": "USGS Earthquake Catalog API",
                "documentation": "https://earthquake.usgs.gov/fdsnws/event/1/",
            },
            "summary": summary,
            "events": events,
            "raw_metadata": payload.get("metadata", {}),
        }
        self._cache[key] = (time.time(), result)
        return result
