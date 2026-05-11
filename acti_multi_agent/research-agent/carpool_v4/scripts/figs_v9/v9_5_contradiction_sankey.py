"""v9_5_contradiction_sankey.py — 3-stage Sankey of 28 contradictions.

Flow:  argument_line  →  beat  →  severity
       (4)              (7)      (3)

Style: MBE-consistent (DejaVu, soft pastel + accent severity colors).
Each node is a rounded rectangle; ribbons are bezier-blended polygons.
Output: output/figures/v9_5_contradiction_sankey.{pdf,png}
"""
from __future__ import annotations
import json
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, PathPatch
from matplotlib.path import Path
from matplotlib.lines import Line2D

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["pdf.fonttype"] = 42
for s in ("top","right","bottom","left"):
    plt.rcParams[f"axes.spines.{s}"] = False

# ----- paths --------------------------------------------------------------
CV = "/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/carpool_v4"
SRC = f"{CV}/analysis/contradictions.json"
OUT_PDF = f"{CV}/output/figures/v9_5_contradiction_sankey.pdf"
OUT_PNG = f"{CV}/output/figures/v9_5_contradiction_sankey.png"

# ----- palette -----------------------------------------------------------
ARG_COLOR = {
    "motivation":   "#2E8B89",   # teal
    "framework":    "#2D6CDF",   # blue
    "primary":      "#5BAE6E",   # green (Beat 4/5 primary survey)
    "adversarial":  "#C5454F",   # red
    "cross-line":   "#845EC2",   # purple
    "core_contribution": "#E8893B",  # orange (Beat 6 artifact)
}
BEAT_COLOR = {
    "1":   "#3FA0AE",   # Beat 1 (motivation A/B)
    "2":   "#3FA0AE",
    "3":   "#5C8EE6",   # Beat 3 (framework)
    "4":   "#7BBF8F",   # Beat 4 (primary survey rider)
    "5":   "#7BBF8F",   # Beat 5 (primary driver subset)
    "6":   "#F0A45E",   # Beat 6 (artifact)
    "7":   "#D86670",   # Beat 7 (adversarial)
    "2+7": "#9D7DD9",   # cross
    "3+7": "#9D7DD9",
    "2+6": "#9D7DD9",
}
SEV_COLOR = {
    "critical": "#C5454F",
    "moderate": "#E8893B",
    "minor":    "#D4AC2A",
}

# ----- load --------------------------------------------------------------
items = json.load(open(SRC))
items = items if isinstance(items, list) else items.get("contradictions", items)
print(f"Loaded {len(items)} contradictions")

# Make sure beat is filled (post-process if any None)
for c in items:
    if not c.get("beat"):
        c["beat"] = "?"
    if not c.get("argument_line"):
        c["argument_line"] = "unknown"
    if not c.get("severity"):
        c["severity"] = "moderate"

# Stage counts
arg_order  = ["motivation", "framework", "primary", "core_contribution", "adversarial", "cross-line"]
beat_order = ["1", "2", "3", "4", "5", "6", "7", "2+6", "2+7", "3+7"]
sev_order  = ["critical", "moderate", "minor"]

arg_counts  = Counter(c["argument_line"] for c in items)
beat_counts = Counter(c["beat"] for c in items)
sev_counts  = Counter(c["severity"] for c in items)

# Filter orders to only categories present
arg_order  = [a for a in arg_order  if a in arg_counts]
beat_order = [b for b in beat_order if b in beat_counts]
sev_order  = [s for s in sev_order  if s in sev_counts]

# Flow tables
arg_to_beat  = Counter((c["argument_line"], c["beat"])     for c in items)
beat_to_sev  = Counter((c["beat"], c["severity"])          for c in items)

# ----- layout ------------------------------------------------------------
# Stages at x = 0.10, 0.50, 0.90; nodes occupy a vertical column
# Total height normalised: each contradiction = 1 unit; gap between nodes = 0.5 unit.
GAP = 0.45
NODE_W = 0.07   # node width as fraction of figure
COL_X = {"arg": 0.12, "beat": 0.50, "sev": 0.88}
TOTAL = len(items)

def column_positions(order, counts, x_center):
    """Return dict: name -> (x_left, x_right, y_top, y_bottom, mid_y)
    Stacked vertically with GAP between nodes.
    Total stack height = TOTAL units + GAP*(n-1)."""
    n = len(order)
    total_h = TOTAL + GAP * (n - 1)
    y = total_h / 2     # start from top
    out = OrderedDict()
    for name in order:
        h = counts[name]
        y_top = y
        y_bot = y - h
        mid_y = (y_top + y_bot) / 2
        out[name] = dict(x_left=x_center - NODE_W/2,
                         x_right=x_center + NODE_W/2,
                         y_top=y_top, y_bot=y_bot, mid_y=mid_y, h=h)
        y = y_bot - GAP
    return out

arg_pos  = column_positions(arg_order,  arg_counts,  COL_X["arg"])
beat_pos = column_positions(beat_order, beat_counts, COL_X["beat"])
sev_pos  = column_positions(sev_order,  sev_counts,  COL_X["sev"])

# Each node has internal "top-down running cursor" for ribbon allocation
def fresh_cursor(positions):
    return {name: positions[name]["y_top"] for name in positions}

cur_arg_out  = fresh_cursor(arg_pos)
cur_beat_in  = fresh_cursor(beat_pos)
cur_beat_out = fresh_cursor(beat_pos)
cur_sev_in   = fresh_cursor(sev_pos)

# ----- figure ------------------------------------------------------------
fig = plt.figure(figsize=(15, 10))
fig.patch.set_facecolor("#FBFBF8")
ax = fig.add_subplot(111)
ax.set_facecolor("#FBFBF8")

def bezier_band(x_l, y_l_top, y_l_bot, x_r, y_r_top, y_r_bot, color, alpha=0.45):
    """Draw a band as a horizontal bezier ribbon between two columns."""
    # Two cubic beziers — one for the top edge, one for the bottom edge — joined
    cx = (x_l + x_r) / 2
    verts = [
        (x_l, y_l_top),
        (cx,  y_l_top),
        (cx,  y_r_top),
        (x_r, y_r_top),
        (x_r, y_r_bot),
        (cx,  y_r_bot),
        (cx,  y_l_bot),
        (x_l, y_l_bot),
        (x_l, y_l_top),
    ]
    codes = [Path.MOVETO,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(verts, codes), facecolor=color, edgecolor="none",
                           alpha=alpha, lw=0, zorder=2))

# Allocate stage-1 → stage-2 ribbons (color by argument_line)
for arg in arg_order:
    for beat in beat_order:
        v = arg_to_beat.get((arg, beat), 0)
        if v == 0: continue
        y_l_top = cur_arg_out[arg]
        y_l_bot = y_l_top - v
        cur_arg_out[arg] = y_l_bot

        y_r_top = cur_beat_in[beat]
        y_r_bot = y_r_top - v
        cur_beat_in[beat] = y_r_bot

        bezier_band(arg_pos[arg]["x_right"], y_l_top, y_l_bot,
                    beat_pos[beat]["x_left"], y_r_top, y_r_bot,
                    color=ARG_COLOR.get(arg, "#888"), alpha=0.38)

# Allocate stage-2 → stage-3 ribbons (color by severity)
for beat in beat_order:
    for sev in sev_order:
        v = beat_to_sev.get((beat, sev), 0)
        if v == 0: continue
        y_l_top = cur_beat_out[beat]
        y_l_bot = y_l_top - v
        cur_beat_out[beat] = y_l_bot

        y_r_top = cur_sev_in[sev]
        y_r_bot = y_r_top - v
        cur_sev_in[sev] = y_r_bot

        bezier_band(beat_pos[beat]["x_right"], y_l_top, y_l_bot,
                    sev_pos[sev]["x_left"], y_r_top, y_r_bot,
                    color=SEV_COLOR.get(sev, "#888"), alpha=0.55)

# ----- draw nodes --------------------------------------------------------
def draw_node(p, label, color, side="left", count=None):
    rect = FancyBboxPatch(
        (p["x_left"], p["y_bot"]),
        p["x_right"] - p["x_left"], p["y_top"] - p["y_bot"],
        boxstyle="round,pad=0.01,rounding_size=0.4",
        linewidth=0.6, edgecolor="#1d1d1d", facecolor=color, alpha=0.95,
        zorder=4)
    ax.add_patch(rect)
    if side == "left":
        ax.text(p["x_left"] - 0.012, p["mid_y"],
                f"{label}  (n={count})",
                ha="right", va="center", fontsize=10.5, color="#222", zorder=5)
    elif side == "right":
        ax.text(p["x_right"] + 0.012, p["mid_y"],
                f"{label}  (n={count})",
                ha="left", va="center", fontsize=10.5, color="#222", zorder=5)
    else:  # middle: print INSIDE the box (vertically centered)
        # Use white text on the colored fill for legibility
        ax.text((p["x_left"] + p["x_right"]) / 2, p["mid_y"],
                f"B{label}\n({count})", ha="center", va="center",
                fontsize=8.2, color="white", weight="semibold", zorder=5)

# Argument-line column (left)
for name, p in arg_pos.items():
    draw_node(p, name, ARG_COLOR.get(name, "#888"),
              side="left", count=arg_counts[name])

# Beat column (middle) - labels above
for name, p in beat_pos.items():
    draw_node(p, name, BEAT_COLOR.get(name, "#888"),
              side="middle", count=beat_counts[name])

# Severity column (right)
for name, p in sev_pos.items():
    draw_node(p, name, SEV_COLOR.get(name, "#888"),
              side="right", count=sev_counts[name])

# ----- column headers ---------------------------------------------------
# Compute the actual y span across all three columns so headers + ylim are sane
all_y_top = max(arg_pos[arg_order[0]]["y_top"],
                beat_pos[beat_order[0]]["y_top"],
                sev_pos[sev_order[0]]["y_top"])
all_y_bot = min(arg_pos[arg_order[-1]]["y_bot"],
                beat_pos[beat_order[-1]]["y_bot"],
                sev_pos[sev_order[-1]]["y_bot"])
header_y = all_y_top + 1.8
ax.text(COL_X["arg"],  header_y, "ARGUMENT LINE", ha="center", va="bottom",
        fontsize=10, color="#444", weight="semibold", zorder=6)
ax.text(COL_X["beat"], header_y, "BEAT", ha="center", va="bottom",
        fontsize=10, color="#444", weight="semibold", zorder=6)
ax.text(COL_X["sev"],  header_y, "SEVERITY", ha="center", va="bottom",
        fontsize=10, color="#444", weight="semibold", zorder=6)

# Title + caption
fig.suptitle(f"Contradiction map — {TOTAL} flagged contradictions across the 7-beat structure",
             fontsize=15, weight="semibold", y=0.96, color="#1d1d1d")

caption = ("Flow: each contradiction is a unit of vertical thickness. Left band colour = argument line "
           "(motivation/framework/primary/adversarial/cross-line). Right band colour = severity "
           "(critical/moderate/minor). Beat tags encode primary attachment in the 7-beat paper "
           "structure; '2+7' and '3+7' denote cross-beat span. Beat 6 has no contradictions because "
           "it is the artifact-description beat — claims are about implementation, not literature.")
fig.text(0.5, 0.06, caption, ha="center", va="top", fontsize=8.5, color="#444", wrap=True)

# ----- finish -----------------------------------------------------------
ax.set_xlim(0, 1)
ax.set_ylim(all_y_bot - 2.5, all_y_top + 4)
ax.set_xticks([]); ax.set_yticks([])
ax.set_aspect("auto")
plt.subplots_adjust(left=0.10, right=0.92, top=0.90, bottom=0.14)

plt.savefig(OUT_PDF, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.savefig(OUT_PNG, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Wrote {OUT_PDF}\nWrote {OUT_PNG}")
