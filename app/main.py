from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from app.providers.factory import get_provider

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")


@app.get("/")
def index() -> object:
    return send_from_directory(STATIC_DIR, "index.html")


@app.get("/api/v1/health")
def health() -> object:
    return jsonify({"status": "ok", "service": "seismic-intel-hub"})


@app.get("/api/v1/earthquakes")
def earthquakes() -> object:
    now = datetime.utcnow().date()
    default_start = now - timedelta(days=30)

    provider_name = request.args.get("provider", "usgs")
    starttime = request.args.get("starttime", default_start.isoformat())
    endtime = request.args.get("endtime", now.isoformat())

    try:
        minmagnitude = float(request.args.get("minmagnitude", 4.0))
        limit = int(request.args.get("limit", 80))
    except ValueError:
        return jsonify({"error": "minmagnitude must be float and limit must be integer"}), 400

    orderby = request.args.get("orderby", "time")

    try:
        provider = get_provider(provider_name)
        result = provider.fetch_events(
            starttime=starttime,
            endtime=endtime,
            minmagnitude=minmagnitude,
            limit=max(1, min(limit, 500)),
            orderby=orderby,
        )
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"Failed to fetch earthquake data: {exc}"}), 502


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
