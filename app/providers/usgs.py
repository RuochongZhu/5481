from __future__ import annotations

from datetime import datetime
from typing import Any

import requests

from .base import EarthquakeProvider


class USGSEarthquakeProvider(EarthquakeProvider):
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

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

        response = requests.get(self.base_url, params=params, timeout=30)
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

        return {
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
