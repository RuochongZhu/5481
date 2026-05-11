"""Build a reproducible earthquake-digest seed and 12 derived variants.

We synthesize a realistic seed digest rather than calling the live USGS API
so the experiment is fully reproducible offline. The seed mirrors the
structure that lab_ai_reporter.py:build_data_digest produces, so prompts
can be reused verbatim.

Run:
    python -m src.data_variants
"""
from __future__ import annotations

import json
import random
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .config import N_VARIANTS, SEED_DIGEST_PATH, VARIANT_DIR

# Reproducibility
SEED = 42

# Region pool (mirrors top regions in the existing reports)
REGIONS = [
    ("Tobelo, Indonesia",         0.18),
    ("Mohr, Iran",                0.08),
    ("Nikolski, Alaska",          0.07),
    ("Tual, Indonesia",           0.07),
    ("Kuril'sk, Russia",          0.06),
    ("La Tirana, Chile",          0.06),
    ("Hachinohe, Japan",          0.05),
    ("Levídion, Greece",          0.04),
    ("San Alejandro, Peru",       0.04),
    ("Calongbuyan, Philippines",  0.04),
    ("Lata, Solomon Islands",     0.04),
    ("South Sandwich Islands",    0.03),
    ("Vanuatu region",            0.03),
    ("Kermadec Islands",          0.03),
    ("Aleutian Islands, Alaska",  0.03),
    ("Mariana Islands region",    0.02),
    ("Off coast of Honshu, Japan",0.03),
    ("Banda Sea",                 0.03),
    ("Fiji region",               0.02),
    ("Tonga region",              0.03),
    ("New Britain region, PNG",   0.02),
]


def _normalize(weights: list[float]) -> list[float]:
    total = sum(weights)
    return [w / total for w in weights]


def _build_seed(end_date: datetime, days: int = 30, n_events: int = 150) -> dict[str, Any]:
    """Synthesize a USGS-style digest. Magnitudes 4.0-6.4, realistic depth and regions."""
    rng = random.Random(SEED)
    start_date = end_date - timedelta(days=days)
    place_names, weights = zip(*REGIONS)
    norm_weights = _normalize(list(weights))

    events: list[dict[str, Any]] = []
    for _ in range(n_events):
        # Time uniformly across the window
        offset_sec = rng.uniform(0, days * 86400)
        ts = (start_date + timedelta(seconds=offset_sec)).astimezone(timezone.utc)

        # Magnitude: log-tail distribution clipped to [4.0, 6.4]
        mag = round(4.0 + rng.expovariate(1.5), 1)
        if mag > 6.4:
            mag = round(rng.uniform(4.0, 5.2), 1)

        # Depth: bimodal — shallow crustal (1-30km) or deep subduction (60-200km)
        if rng.random() < 0.6:
            depth = round(rng.uniform(1.0, 30.0), 1)
        else:
            depth = round(rng.uniform(60.0, 200.0), 1)

        # Place: weighted choice
        place = rng.choices(place_names, weights=norm_weights, k=1)[0]
        # Use a prefix like "X km E of <region>" half the time
        if rng.random() < 0.5:
            place = f"{rng.randint(3, 120)} km E of {place}"

        # Tsunami: rare flag, only for shallow + M>=5.5
        tsunami = mag >= 5.5 and depth < 30 and rng.random() < 0.15

        events.append({
            "time": ts.isoformat().replace("+00:00", "Z"),
            "magnitude": mag,
            "place": place,
            "depth_km": depth,
            "tsunami": bool(tsunami),
        })

    events.sort(key=lambda e: e["time"], reverse=True)  # most recent first
    return _digest_from_events(events, start_date, end_date, provider="usgs-synthetic")


def _digest_from_events(
    events: list[dict[str, Any]],
    start_date: datetime,
    end_date: datetime,
    *,
    provider: str = "usgs-synthetic",
    sample_size: int = 30,
) -> dict[str, Any]:
    magnitudes = [e["magnitude"] for e in events]

    region_counts: Counter[str] = Counter()
    daily_counts: Counter[str] = Counter()
    for e in events:
        # Match lab_ai_reporter.build_data_digest heuristic
        region = e["place"].split(" of ")[-1].strip()
        region_counts[region] += 1
        # Parse date
        try:
            dt = datetime.fromisoformat(e["time"].replace("Z", "+00:00"))
            daily_counts[dt.date().isoformat()] += 1
        except Exception:
            pass

    return {
        "meta": {
            "provider": provider,
            "starttime": start_date.date().isoformat(),
            "endtime": end_date.date().isoformat(),
            "queried_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        },
        "summary": {
            "event_count": len(events),
            "max_magnitude": max(magnitudes) if magnitudes else None,
            "min_magnitude": min(magnitudes) if magnitudes else None,
            "avg_magnitude": round(sum(magnitudes) / len(magnitudes), 2) if magnitudes else None,
            "top_regions": region_counts.most_common(5),
            "daily_counts": dict(sorted(daily_counts.items())),
        },
        "sample_events": events[:sample_size],
    }


def _filter_events(
    events: list[dict[str, Any]],
    *,
    min_mag: float | None = None,
    max_age_days: int | None = None,
    end_date: datetime | None = None,
    region_substring: str | None = None,
    subsample_frac: float | None = None,
    rng_seed: int | None = None,
) -> list[dict[str, Any]]:
    out = list(events)
    if min_mag is not None:
        out = [e for e in out if e["magnitude"] >= min_mag]
    if max_age_days is not None and end_date is not None:
        cutoff = end_date - timedelta(days=max_age_days)
        out = [
            e for e in out
            if datetime.fromisoformat(e["time"].replace("Z", "+00:00")) >= cutoff
        ]
    if region_substring is not None:
        sub = region_substring.lower()
        out = [e for e in out if sub in e["place"].lower()]
    if subsample_frac is not None:
        rng = random.Random(rng_seed if rng_seed is not None else SEED)
        keep = max(1, int(len(out) * subsample_frac))
        out = sorted(rng.sample(out, k=keep), key=lambda e: e["time"], reverse=True)
    return out


def build_variants(end_date: datetime | None = None) -> list[Path]:
    """Generate N=12 variants from the seed digest.

    Layout:
        variants 0-3: date-window slices (last 7d, 14d, 21d, 30d)
        variants 4-7: magnitude-floor slices (>=4.0, >=4.5, >=5.0, >=5.5)
        variants 8-11: region-focus + subsample slices
    """
    end_date = end_date or datetime(2026, 2, 16, tzinfo=timezone.utc)
    seed = _build_seed(end_date=end_date, days=30, n_events=150)
    SEED_DIGEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    SEED_DIGEST_PATH.write_text(json.dumps(seed, indent=2), encoding="utf-8")

    full_events = seed["sample_events"][:]  # only sample is exposed in digest
    # For variants we need access to ALL events, not just sample.
    # Regenerate the underlying event set deterministically.
    rng = random.Random(SEED)
    days = 30
    n_events = 150
    start_date = end_date - timedelta(days=days)
    place_names, weights = zip(*REGIONS)
    norm_weights = _normalize(list(weights))
    full_events = []
    for _ in range(n_events):
        offset_sec = rng.uniform(0, days * 86400)
        ts = (start_date + timedelta(seconds=offset_sec)).astimezone(timezone.utc)
        mag = round(4.0 + rng.expovariate(1.5), 1)
        if mag > 6.4:
            mag = round(rng.uniform(4.0, 5.2), 1)
        if rng.random() < 0.6:
            depth = round(rng.uniform(1.0, 30.0), 1)
        else:
            depth = round(rng.uniform(60.0, 200.0), 1)
        place = rng.choices(place_names, weights=norm_weights, k=1)[0]
        if rng.random() < 0.5:
            place = f"{rng.randint(3, 120)} km E of {place}"
        tsunami = mag >= 5.5 and depth < 30 and rng.random() < 0.15
        full_events.append({
            "time": ts.isoformat().replace("+00:00", "Z"),
            "magnitude": mag,
            "place": place,
            "depth_km": depth,
            "tsunami": bool(tsunami),
        })
    full_events.sort(key=lambda e: e["time"], reverse=True)

    specs: list[tuple[str, dict]] = [
        # Variants 0-3: date window
        ("variant_00_last_7d",      {"max_age_days": 7,  "end_date": end_date}),
        ("variant_01_last_14d",     {"max_age_days": 14, "end_date": end_date}),
        ("variant_02_last_21d",     {"max_age_days": 21, "end_date": end_date}),
        ("variant_03_last_30d",     {"max_age_days": 30, "end_date": end_date}),
        # Variants 4-7: magnitude floor
        ("variant_04_mag_ge_40",    {"min_mag": 4.0}),
        ("variant_05_mag_ge_45",    {"min_mag": 4.5}),
        ("variant_06_mag_ge_50",    {"min_mag": 5.0}),
        ("variant_07_mag_ge_55",    {"min_mag": 5.5}),
        # Variants 8-11: region focus + subsample
        ("variant_08_indonesia",    {"region_substring": "indonesia"}),
        ("variant_09_alaska_ring",  {"region_substring": "alaska"}),
        ("variant_10_subsample_50", {"subsample_frac": 0.5, "rng_seed": 101}),
        ("variant_11_subsample_30", {"subsample_frac": 0.3, "rng_seed": 102}),
    ]

    VARIANT_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for name, kwargs in specs:
        events = _filter_events(full_events, **kwargs)
        if not events:
            raise RuntimeError(f"variant {name} produced 0 events; adjust spec")
        # window for digest meta
        if "max_age_days" in kwargs:
            sd = end_date - timedelta(days=kwargs["max_age_days"])
        elif kwargs.get("region_substring") or kwargs.get("subsample_frac"):
            sd = start_date
        else:
            sd = start_date
        digest = _digest_from_events(events, sd, end_date, provider="usgs-synthetic")
        digest["meta"]["variant_id"] = name
        digest["meta"]["filter"] = {k: v for k, v in kwargs.items() if k != "end_date"}
        path = VARIANT_DIR / f"{name}.json"
        path.write_text(json.dumps(digest, indent=2), encoding="utf-8")
        paths.append(path)
    return paths


def load_variant(variant_id: int | str) -> dict[str, Any]:
    """Load a variant by integer index or by variant_NN_* filename stem."""
    if isinstance(variant_id, int):
        candidates = sorted(VARIANT_DIR.glob(f"variant_{variant_id:02d}_*.json"))
        if not candidates:
            raise FileNotFoundError(f"no variant_{variant_id:02d}_* found in {VARIANT_DIR}")
        path = candidates[0]
    else:
        path = VARIANT_DIR / (variant_id if variant_id.endswith(".json") else f"{variant_id}.json")
    return json.loads(path.read_text(encoding="utf-8"))


def list_variants() -> list[Path]:
    return sorted(VARIANT_DIR.glob("variant_*.json"))


if __name__ == "__main__":
    paths = build_variants()
    print(f"Built {len(paths)} variants and seed:")
    for p in paths:
        d = json.loads(p.read_text())
        print(f"  {p.name}: {d['summary']['event_count']} events, "
              f"mag {d['summary']['min_magnitude']}-{d['summary']['max_magnitude']}")
    print(f"Seed at: {SEED_DIGEST_PATH}")
