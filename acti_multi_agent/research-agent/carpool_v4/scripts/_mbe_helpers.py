"""Helpers shared across model-based-engineer figures (mbe_*).

Run figures via render_mbe_figures.py. Each figure registers itself in
viz_results.json (status="ok"|"error", path, ts).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[2]
CARPOOL_ROOT = REPO_ROOT / "carpool_v4"
OUT_DIR = CARPOOL_ROOT / "output" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIZ_REGISTRY = OUT_DIR / "viz_results.json"
STATUS_DIR = OUT_DIR / "_mbe_status"
STATUS_DIR.mkdir(parents=True, exist_ok=True)

# Reuse palette from src/visualize.py
CAT_COLORS = {
    "A": "#e74c3c", "B": "#e67e22", "C": "#f1c40f", "D": "#2ecc71",
    "E": "#1abc9c", "F": "#3498db", "G": "#9b59b6", "H": "#e91e63",
    "I": "#00bcd4", "J": "#ff9800", "X": "#95a5a6",
}
DRIVER_COLOR = "#C0392B"
RIDER_COLOR = "#2980B9"

# Argument-line colors for beat structure
BEAT_COLORS = {
    "motivation": "#7F8C8D",
    "framework": "#16A085",
    "primary": "#C0392B",
    "core_contribution": "#8E44AD",
    "adversarial": "#E67E22",
}

# Module palette (6 modules)
MODULE_COLORS = {
    "Carpool": "#3498db",
    "Marketplace": "#e67e22",
    "Activities": "#2ecc71",
    "Groups": "#9b59b6",
    "Messages": "#1abc9c",
    "Points": "#f1c40f",
}

GRAPHVIZ_DEFAULTS = {
    "graph": {
        "rankdir": "TB",
        "splines": "ortho",
        "nodesep": "0.4",
        "ranksep": "0.55",
        "fontname": "Helvetica",
        "bgcolor": "white",
    },
    "node": {
        "fontname": "Helvetica",
        "fontsize": "11",
        "shape": "box",
        "style": "rounded,filled",
        "fillcolor": "#ECF0F1",
        "color": "#34495E",
        "penwidth": "1.2",
    },
    "edge": {
        "fontname": "Helvetica",
        "fontsize": "10",
        "color": "#34495E",
        "penwidth": "1.0",
    },
}


RENDERERS: dict = {}


def renderer(stem: str):
    """Decorator: register the function as the renderer for `stem`.

    Lives in _mbe_helpers (not in render_mbe_figures) so the registry survives
    the `__main__` vs module re-import quirk when the CLI is run directly.
    """
    def deco(fn):
        RENDERERS[stem] = fn
        return fn
    return deco


def setup_mpl() -> None:
    """Match the survey-radar style."""
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    plt.rcParams["pdf.fonttype"] = 42  # TrueType for editable text in PDF
    plt.rcParams["ps.fonttype"] = 42
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False


def make_digraph(name: str, comment: str = "", rankdir: str = "TB"):
    """Return a graphviz.Digraph with the project defaults pre-applied."""
    import graphviz
    g = graphviz.Digraph(name=name, comment=comment)
    g.attr(rankdir=rankdir, splines="spline", nodesep="0.45", ranksep="0.6",
           fontname="Helvetica", bgcolor="white")
    g.attr("node", fontname="Helvetica", fontsize="11", shape="box",
           style="rounded,filled", fillcolor="#ECF0F1", color="#34495E",
           penwidth="1.2")
    g.attr("edge", fontname="Helvetica", fontsize="10", color="#34495E",
           penwidth="1.0")
    return g


def render_dot(g, stem: str, dpi: int = 300) -> tuple[Path, Path]:
    """Render a graphviz Digraph to both PDF and PNG. Return (pdf, png) paths.

    `stem` is e.g. 'mbe_a1_stack_layers'. Files written under OUT_DIR.
    """
    pdf_target = OUT_DIR / f"{stem}.pdf"
    png_target = OUT_DIR / f"{stem}.png"

    g_pdf = g.copy()
    g_pdf.format = "pdf"
    g_pdf.render(filename=stem, directory=str(OUT_DIR), cleanup=True)

    g_png = g.copy()
    g_png.format = "png"
    g_png.attr(dpi=str(dpi))
    g_png.render(filename=stem, directory=str(OUT_DIR), cleanup=True)

    return pdf_target, png_target


def save_mpl(stem: str, dpi: int = 300) -> tuple[Path, Path]:
    """Save the current matplotlib figure to PDF + PNG. Return (pdf, png)."""
    pdf_target = OUT_DIR / f"{stem}.pdf"
    png_target = OUT_DIR / f"{stem}.png"
    plt.savefig(pdf_target, bbox_inches="tight")
    plt.savefig(png_target, dpi=dpi, bbox_inches="tight")
    return pdf_target, png_target


def register(stem: str, status: str, png_path: Path | None = None,
             note: str = "") -> None:
    """Write a per-stem status JSON (race-free under parallel renders).

    Aggregation into viz_results.json is performed by aggregate_status().
    """
    payload = {
        "stem": stem,
        "status": status,
        "path": str(png_path.relative_to(CARPOOL_ROOT)) if png_path else None,
        "ts": int(time.time()),
        "note": note,
    }
    (STATUS_DIR / f"{stem}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False)
    )


def aggregate_status() -> dict:
    """Merge per-stem status files into viz_results.json. Return merged dict."""
    if VIZ_REGISTRY.exists():
        data = json.loads(VIZ_REGISTRY.read_text())
    else:
        data = {}
    for p in sorted(STATUS_DIR.glob("*.json")):
        entry = json.loads(p.read_text())
        data[entry["stem"]] = entry
    VIZ_REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return data


def file_line(rel_path: str, lines: str) -> str:
    """Helper to format file:line annotations on graphviz nodes."""
    return f"\\n[{rel_path}:{lines}]"
