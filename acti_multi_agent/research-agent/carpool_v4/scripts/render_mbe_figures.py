"""Model-based-engineer figures (mbe_*) for the CampusRide paper.

20 figures grouped A–E. Each `render_<stem>()` is independent and writes
both PDF (vector for LaTeX \\includegraphics) and PNG (300 dpi raster for
inspection) to carpool_v4/output/figures/.

CLI:
    python scripts/render_mbe_figures.py --all
    python scripts/render_mbe_figures.py mbe_a1_stack_layers mbe_b1_ride_state_machine
"""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

THIS = Path(__file__).resolve()
sys.path.insert(0, str(THIS.parent))

from _mbe_helpers import (  # noqa: E402
    CAT_COLORS, DRIVER_COLOR, RIDER_COLOR, BEAT_COLORS, MODULE_COLORS,
    OUT_DIR, make_digraph, render_dot, save_mpl, setup_mpl, register,
    aggregate_status, RENDERERS, renderer,
)


# --- per-figure renderers will be registered in mbe_<group>_*.py modules ---

# Auto-import all sibling mbe_* modules so their @renderer decorations register.
def _load_all() -> None:
    for pattern in ("mbe_*.py", "mbse_*.py"):
        for p in THIS.parent.glob(pattern):
            mod_name = p.stem
            if mod_name == "mbe_helpers":
                continue
            __import__(mod_name)


def main() -> None:
    _load_all()
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="*", help="figure stems to render")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        for k in sorted(RENDERERS):
            print(k)
        return

    targets = sorted(RENDERERS) if args.all or not args.targets else args.targets
    failed: list[str] = []
    for stem in targets:
        if stem not in RENDERERS:
            print(f"[skip] unknown {stem}")
            continue
        try:
            print(f"[run]  {stem}")
            RENDERERS[stem]()
            print(f"[ok]   {stem}")
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            register(stem, "error", note=str(e))
            failed.append(stem)
            print(f"[err]  {stem}: {e}")
    if failed:
        sys.exit(2)


if __name__ == "__main__":
    main()
