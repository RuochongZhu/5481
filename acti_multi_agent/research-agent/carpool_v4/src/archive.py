"""Pre-run archive snapshots + restore-from-archive for explicit run control."""

from __future__ import annotations

import json
import os
import shutil
import time
from typing import Any

ARCHIVE_TARGETS_BASE: list[str] = [
    "state.json",
    "analysis",
    "output",
    "data/processed",
]
ARCHIVE_TARGETS_RAW: list[str] = ["data/raw"]


def _ts() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def archive_pre_run(
    base_dir: str,
    mode: str,
    label: str | None,
    include_raw: bool,
    log: Any,
) -> str:
    ts = _ts()
    name = f"run_{ts}_{mode}" + (f"_{label}" if label else "")
    dest = os.path.join(base_dir, "archive", name)
    targets = list(ARCHIVE_TARGETS_BASE) + (ARCHIVE_TARGETS_RAW if include_raw else [])
    try:
        os.makedirs(dest, exist_ok=False)
        copied: list[str] = []
        for rel in targets:
            src = os.path.join(base_dir, rel)
            if not os.path.exists(src):
                continue
            dst = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=False)
            else:
                shutil.copy2(src, dst)
            copied.append(rel)
        manifest = {
            "timestamp": ts,
            "mode": mode,
            "label": label,
            "include_raw": include_raw,
            "targets_requested": targets,
            "targets_copied": copied,
        }
        with open(os.path.join(dest, "MANIFEST.json"), "w") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        log.info(f"Archived pre-run snapshot → archive/{name} ({len(copied)} target(s))")
        return dest
    except Exception as e:
        log.error(f"Pre-run archive failed: {e}")
        raise SystemExit(
            f"Pre-run archive failed: {e}\n"
            f"Use --no-archive (or set ARCHIVE_BEFORE_RUN=false) to bypass."
        )


def restore_from_archive(base_dir: str, archive_path: str, log: Any) -> None:
    if not os.path.isabs(archive_path):
        archive_path = os.path.join(base_dir, archive_path)
    if not os.path.isdir(archive_path):
        raise SystemExit(f"--from-archive: {archive_path} not found or not a directory")
    manifest_path = os.path.join(archive_path, "MANIFEST.json")
    if not os.path.exists(manifest_path):
        raise SystemExit(f"--from-archive: missing MANIFEST.json in {archive_path}")
    with open(manifest_path) as f:
        manifest = json.load(f)
    targets = manifest.get("targets_copied") or manifest.get("targets_requested") or []
    log.info(
        f"Restoring from archive: {archive_path} "
        f"(mode={manifest.get('mode')}, ts={manifest.get('timestamp')}, "
        f"{len(targets)} target(s))"
    )
    restored = 0
    for rel in targets:
        src = os.path.join(archive_path, rel)
        dst = os.path.join(base_dir, rel)
        if not os.path.exists(src):
            continue
        if os.path.exists(dst):
            if os.path.isdir(dst) and not os.path.islink(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        restored += 1
    log.info(f"Restored {restored} target(s) from archive")
