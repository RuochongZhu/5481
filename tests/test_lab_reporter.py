from lab_ai_reporter import build_data_digest, make_prompt


def test_build_data_digest_contains_expected_aggregates():
    payload = {
        "meta": {"requested": {"starttime": "2026-01-01", "endtime": "2026-01-31"}},
        "events": [
            {"magnitude": 5.1, "place": "10 km NW of A", "time": "2026-01-10T00:00:00Z", "depth_km": 8.2, "tsunami": False},
            {"magnitude": 4.2, "place": "5 km E of A", "time": "2026-01-10T04:00:00Z", "depth_km": 4.0, "tsunami": False},
            {"magnitude": 6.0, "place": "Region B", "time": "2026-01-11T00:00:00Z", "depth_km": 18.0, "tsunami": True},
        ],
    }
    digest = build_data_digest(payload, sample_size=2)
    assert digest["summary"]["event_count"] == 3
    assert digest["summary"]["max_magnitude"] == 6.0
    assert digest["summary"]["min_magnitude"] == 4.2
    assert digest["summary"]["daily_counts"]["2026-01-10"] == 2
    assert len(digest["sample_events"]) == 2


def test_make_prompt_embeds_json_data():
    digest = {"summary": {"event_count": 10}}
    prompt = make_prompt("hello", digest)
    assert "DATA (JSON):" in prompt
    assert "\"event_count\": 10" in prompt
