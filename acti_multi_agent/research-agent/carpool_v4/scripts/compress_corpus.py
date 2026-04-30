"""Compress unified corpus to ≤500 papers via quality + topical relevance filter.

Strategy:
  1. Force-keep all papers already in classified.json (the 88 existing anchors).
  2. Apply a hard quality filter to the rest:
       - year >= 2008 (older only by exception)
       - tier-based citation threshold (newer papers get a lower bar)
       - abstract OR DOI present, title length sane
       - at least ONE topical-vocabulary hit in title+abstract
  3. Rank survivors by composite score:
       score = log(citationCount+1) * topical_density * year_weight
  4. Cap surviving non-anchors at 500 - len(anchors).
  5. Backup, write back corpus_unified.json + diagnostics.

Run:
  .venv/bin/python carpool_v4/scripts/compress_corpus.py
  .venv/bin/python carpool_v4/scripts/compress_corpus.py --target 500
  .venv/bin/python carpool_v4/scripts/compress_corpus.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2] / "carpool_v4"
PROC = REPO / "data" / "processed"
UNIFIED_PATH = PROC / "corpus_unified.json"
CLASSIFIED_PATH = PROC / "classified.json"
CORPUS_200_PATH = PROC / "corpus_200.json"

# ---------------------------------------------------------------------------
# Topical vocabulary — must hit at least one to be considered relevant
# ---------------------------------------------------------------------------

EXISTING_VOCAB = {
    # A: campus transportation gap
    "small town", "small-town", "rural", "campus transportation", "rideshare", "uber",
    "lyft", "transit gap", "campus shuttle", "mobility access", "first-mile", "last-mile",
    "underserved", "transportation gap", "intercity", "campus mobility",
    # B: peer rideshare / sharing economy trust
    "peer-to-peer", "p2p", "sharing economy", "airbnb", "trust signal", "verification",
    "stranger trust", "personal photos", "online platform economy", "peer trust",
    # C: grassroots / informal coordination
    "wechat", "whatsapp", "messaging app", "group chat", "informal coordination",
    "grassroots", "self-organized", "instant messaging", "community platform",
    # D: international students / digital practice
    "international student", "chinese student", "digital acculturation", "immigrant student",
    "cross-cultural", "us university", "american campus", "overseas student",
    # E: institutional identity
    ".edu", "edu email", "institutional identity", "campus-scoped", "closed community",
    "institutional verification", "campus id", "yik yak", "facebook social capital",
    # F: rideshare safety
    "rideshare safety", "real-time location", "sos", "panic button", "emergency button",
    "women safety", "ride tracking", "trip sharing", "safety feature", "shared mobility risk",
    # G: gamification
    "gamification", "points system", "rewards", "leaderboard", "behavior change",
    "intrinsic motivation", "extrinsic reward", "engagement", "badge",
    # H: rating fairness
    "rating fairness", "peer rating", "reputation system", "rating bias", "feedback design",
    "two-sided rating", "amateur driver", "occasional driver", "blablacar",
    # I: integrated platform / super-app / multi-campus / continuous deployment / QFD (extended)
    "super app", "super-app", "integrated platform", "multi-module", "one-stop",
    "campus platform", "kakaotalk", "line app",
    "house of quality", "quality function deployment", "qfd", "voice of customer",
    "engineering characteristic", "requirements engineering", "requirements traceability",
    "multi-campus", "multi campus", "multi-site", "multi-institution", "cross-institution",
    "cross-campus", "campus app", "university software", "design transferability",
    "context transfer", "continuous deployment", "continuous delivery", "release engineering",
    "soft launch", "longitudinal deployment", "in the wild", "in-the-wild",
    "iterative design", "agile", "field deployment", "telemetry", "usage analytics",
    "sustained engagement", "adoption funnel", "field study",
    # J: algorithmic management / platform labor
    "algorithmic management", "algorithmic control", "gig worker", "gig economy",
    "platform labor", "platform-mediated work", "driver precarity", "algorithmic opacity",
    "worker wellbeing", "labor precarity",
    # Cross-cutting design-research / HCI
    "csCW", "cscw", "chi 20", "hci", "human factors", "user-centered design",
    "design case", "formative study", "field trial",
}

EXISTING_VOCAB = {v.lower() for v in EXISTING_VOCAB}


# ---------------------------------------------------------------------------
# Quality filter
# ---------------------------------------------------------------------------

CITE_TIERS = [
    (2024, math.inf,  0),
    (2020, 2023,      3),
    (2015, 2019,     10),
    (2010, 2014,     30),
    (2005, 2009,     80),
    (1900, 2004,    150),
]


def cite_threshold(year: int) -> int:
    for lo, hi, thr in CITE_TIERS:
        if lo <= year <= hi:
            return thr
    return 9999


def year_weight(year: int) -> float:
    if year >= 2020:
        return 1.0
    if year >= 2015:
        return 0.85
    if year >= 2010:
        return 0.55
    if year >= 2005:
        return 0.30
    return 0.10


def paper_text(p: dict) -> str:
    parts = [p.get("title") or ""]
    abstract = p.get("abstract") or ""
    if isinstance(abstract, list):
        abstract = " ".join(str(x) for x in abstract)
    parts.append(abstract)
    return " ".join(parts).lower()


def topical_density(text: str) -> int:
    """Count distinct topical terms appearing in the text."""
    return sum(1 for term in EXISTING_VOCAB if term in text)


def passes_quality(p: dict) -> tuple[bool, str]:
    year = int(p.get("year") or 0)
    if year < 2008:
        return False, "year_too_old"
    cites = int(p.get("citationCount") or 0)
    if cites < cite_threshold(year):
        return False, f"cites_below_tier(year={year},cites={cites})"
    title = (p.get("title") or "").strip()
    if len(title) < 20:
        return False, "title_too_short"
    abstract = p.get("abstract") or ""
    if isinstance(abstract, list):
        abstract = " ".join(str(x) for x in abstract)
    if len(abstract) < 100 and not p.get("doi"):
        return False, "no_abstract_no_doi"
    if topical_density(paper_text(p)) < 1:
        return False, "no_topical_match"
    return True, "ok"


def composite_score(p: dict) -> float:
    cites = int(p.get("citationCount") or 0)
    year = int(p.get("year") or 2010)
    td = topical_density(paper_text(p))
    return math.log(cites + 1) * (td ** 0.7) * year_weight(year)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=500,
                    help="Total target corpus size (anchors force-included; rest ranked).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print stats without writing files.")
    args = ap.parse_args()

    if not UNIFIED_PATH.exists():
        sys.exit(f"missing: {UNIFIED_PATH}")
    unified = json.load(open(UNIFIED_PATH))
    if isinstance(unified, dict) and "papers" in unified:
        unified = unified["papers"]
    print(f"Loaded unified_corpus.json: {len(unified)} papers")

    # Force-keep anchors from classified.json (CLAUDE.md invariant: append-only)
    classified_papers: list[dict] = []
    anchor_ids: set[str] = set()
    if CLASSIFIED_PATH.exists():
        classified_papers = json.load(open(CLASSIFIED_PATH))
        if isinstance(classified_papers, dict) and "papers" in classified_papers:
            classified_papers = classified_papers["papers"]
        anchor_ids = {p.get("paperId") for p in classified_papers if p.get("paperId")}
        print(f"Loaded classified.json: {len(classified_papers)} anchor papers (force-kept)")
    else:
        print("classified.json not found — no anchor force-keep")

    # Partition: anchors-in-unified vs others
    anchors_in_unified: list[dict] = []
    others: list[dict] = []
    seen_paperids: set[str] = set()
    for p in unified:
        pid = p.get("paperId")
        if pid in anchor_ids:
            anchors_in_unified.append(p)
            seen_paperids.add(pid)
        else:
            others.append(p)
            if pid:
                seen_paperids.add(pid)
    # Anchors that exist in classified but NOT in current unified — add them back
    missing_anchors = [p for p in classified_papers
                       if p.get("paperId") and p.get("paperId") not in seen_paperids]
    print(f"Anchors in unified: {len(anchors_in_unified)} | "
          f"Anchors missing from unified (rescued): {len(missing_anchors)} | "
          f"Others (filter pool): {len(others)}")
    anchors = anchors_in_unified + missing_anchors

    # Apply quality filter to others
    survived = []
    drop_reasons: Counter[str] = Counter()
    for p in others:
        ok, why = passes_quality(p)
        if ok:
            p["_score"] = round(composite_score(p), 4)
            survived.append(p)
        else:
            drop_reasons[why] += 1
    print(f"Quality filter: {len(survived)}/{len(others)} survived")
    print("  Drop reasons:")
    for r, n in drop_reasons.most_common():
        print(f"    {r}: {n}")

    # Rank and cap
    survived.sort(key=lambda p: p["_score"], reverse=True)
    cap_others = max(0, args.target - len(anchors))
    kept_others = survived[:cap_others]
    print(f"Top-{cap_others} kept by composite score; lowest score in keep: "
          f"{kept_others[-1]['_score'] if kept_others else 'N/A'}")
    print(f"Highest score in drop:    "
          f"{survived[cap_others]['_score'] if len(survived) > cap_others else 'N/A'}")

    # Strip the temporary _score field
    for p in kept_others:
        p.pop("_score", None)

    final = anchors + kept_others
    print(f"FINAL corpus: {len(final)} papers (anchors {len(anchors)} + filtered {len(kept_others)})")

    # Diagnostics — distribution by year + retrieval_layer + has-doi
    year_hist = Counter(int(p.get("year") or 0) // 5 * 5 for p in final)
    layer_hist = Counter(p.get("retrieval_layer") or "unknown" for p in final)
    print("  By half-decade (year):")
    for y, n in sorted(year_hist.items()):
        print(f"    {y}: {n}")
    print("  By retrieval_layer:")
    for l, n in layer_hist.most_common():
        print(f"    {l}: {n}")

    if args.dry_run:
        print("\n--dry-run: not writing files.")
        return

    # Backup
    ts = time.strftime("%Y%m%d_%H%M%S")
    backup = UNIFIED_PATH.with_name(f"corpus_unified.json.bak_compress_{ts}")
    shutil.copy(UNIFIED_PATH, backup)
    print(f"Backup → {backup.name}")

    # Save compressed
    UNIFIED_PATH.write_text(json.dumps(final, indent=2, ensure_ascii=False))
    print(f"Wrote {UNIFIED_PATH.relative_to(REPO.parent)} ({len(final)} papers)")

    # Diagnostics file
    diag = {
        "timestamp": ts,
        "before": {"total": len(unified)},
        "anchors_kept": len(anchors),
        "filter_pool": len(others),
        "survived_filter": len(survived),
        "kept_after_cap": len(kept_others),
        "final_total": len(final),
        "drop_reasons": dict(drop_reasons),
        "year_histogram": {str(k): v for k, v in sorted(year_hist.items())},
        "retrieval_layer_histogram": dict(layer_hist),
    }
    diag_path = PROC / f"compress_diagnostics_{ts}.json"
    diag_path.write_text(json.dumps(diag, indent=2))
    print(f"Wrote {diag_path.relative_to(REPO.parent)}")


if __name__ == "__main__":
    main()
