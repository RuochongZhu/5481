#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${GROBID_BASE_URL:-http://localhost:8070}"
curl -fsS "$BASE_URL/api/isalive"
