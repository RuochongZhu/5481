from __future__ import annotations

from .base import EarthquakeProvider
from .usgs import USGSEarthquakeProvider


PROVIDERS: dict[str, type[EarthquakeProvider]] = {
    "usgs": USGSEarthquakeProvider,
}


def get_provider(name: str) -> EarthquakeProvider:
    provider_cls = PROVIDERS.get(name)
    if not provider_cls:
        supported = ", ".join(sorted(PROVIDERS.keys()))
        raise ValueError(f"Unknown provider {name}. Supported providers: {supported}")
    return provider_cls()
