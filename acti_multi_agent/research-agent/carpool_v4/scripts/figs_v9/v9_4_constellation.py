"""v9_4_constellation.py — Knowledge graph constellation of the 100-paper corpus.

Layout: force-directed, paper nodes only.
Node size  ∝ log(citationCount + 1)
Node color = category (A-J) using a 10-color palette
Edges:
  - methodological_mirror (80) — soft purple solid
  - contradiction (16)         — RED dashed (highlighted)
  - builds_on (3) / extends (3) — gold solid
  - conceptual_overlap (sample) — light gray very thin (background)
  - temporal_succession (skip)  — too dense, would flood

Output: output/figures/v9_4_constellation.{pdf,png}
"""
from __future__ import annotations
import json, math, os, random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import networkx as nx

# ----- style ---------------------------------------------------------------
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.bottom"] = False
plt.rcParams["axes.spines.left"] = False

# ----- paths --------------------------------------------------------------
CV = "/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/carpool_v4"
GRAPH = f"{CV}/data/processed/research_knowledge_graph.json"
OUT_PDF = f"{CV}/output/figures/v9_4_constellation.pdf"
OUT_PNG = f"{CV}/output/figures/v9_4_constellation.png"

# ----- palette: 10 categories ---------------------------------------------
CAT_COLOR = {
    "A": "#2E8B89",   # teal  - small-town transport gap
    "B": "#2D6CDF",   # blue  - p2p ridesharing trust
    "C": "#E8893B",   # orange - grassroots messaging
    "D": "#845EC2",   # purple - international students
    "E": "#5BAE6E",   # green  - .edu identity
    "F": "#C5454F",   # red    - safety
    "G": "#D4AC2A",   # gold   - gamification
    "H": "#5598B8",   # steel  - rating fairness
    "I": "#B8497B",   # magenta- super-app
    "J": "#7A6C57",   # taupe  - algo management
}
CAT_NAME = {
    "A": "Campus transport gap",
    "B": "P2P rideshare trust",
    "C": "Grassroots messaging",
    "D": "Intl. students",
    "E": ".edu identity",
    "F": "Shared-mobility safety",
    "G": "Gamification",
    "H": "Rating fairness",
    "I": "Super-app / integrated",
    "J": "Algo. management",
}

EDGE_STYLE = {
    "methodological_mirror": dict(color="#845EC2", width=0.6, alpha=0.45, ls="-"),
    "contradiction":        dict(color="#C5454F", width=1.6, alpha=0.95, ls=(0,(4,2))),
    "builds_on":            dict(color="#D4AC2A", width=1.0, alpha=0.85, ls="-"),
    "extends":              dict(color="#D4AC2A", width=1.0, alpha=0.85, ls="-"),
    "conceptual_overlap":   dict(color="#BDBDBD", width=0.20, alpha=0.18, ls="-"),
}

random.seed(42)

# ----- load --------------------------------------------------------------
with open(GRAPH) as f:
    g = json.load(f)
papers = [n for n in g["nodes"] if n.get("node_type") == "paper"]
pids   = {p["id"] for p in papers}
edges  = [e for e in g["edges"] if e["source"] in pids and e["target"] in pids]
print(f"papers={len(papers)} edges={len(edges)}")

# Sample conceptual_overlap to ~120 to keep canvas readable while still showing density
co_edges = [e for e in edges if e.get("relation") == "conceptual_overlap"]
co_sample = random.sample(co_edges, min(120, len(co_edges)))

# All hard edges
hard = [e for e in edges if e.get("relation") in
        ("methodological_mirror","contradiction","builds_on","extends")]
draw_edges = co_sample + hard
print(f"drawing {len(draw_edges)} edges (CO sampled to {len(co_sample)} + {len(hard)} hard)")

# ----- build NX graph for layout -----------------------------------------
G = nx.Graph()
for p in papers:
    G.add_node(p["id"], **p)
for e in draw_edges:
    G.add_edge(e["source"], e["target"], relation=e["relation"])

# Connect isolates with a phantom super-edge so spring layout doesn't dump them at infinity
isolates = [n for n in G.nodes if G.degree(n) == 0]
for n in isolates:
    G.add_edge(n, papers[0]["id"], relation="_anchor", weight=0.01)

pos = nx.spring_layout(G, k=0.45, iterations=200, seed=42, weight=None)

# ----- figure -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(17, 11))
fig.patch.set_facecolor("#FBFBF8")
ax.set_facecolor("#FBFBF8")

# 1) draw conceptual_overlap first (background)
for e in co_sample:
    s, t = pos[e["source"]], pos[e["target"]]
    st = EDGE_STYLE["conceptual_overlap"]
    ax.plot([s[0], t[0]], [s[1], t[1]], color=st["color"],
            lw=st["width"], alpha=st["alpha"], ls=st["ls"], zorder=1)

# 2) methodological_mirror
for e in [x for x in hard if x["relation"]=="methodological_mirror"]:
    s, t = pos[e["source"]], pos[e["target"]]
    st = EDGE_STYLE["methodological_mirror"]
    ax.plot([s[0], t[0]], [s[1], t[1]], color=st["color"],
            lw=st["width"], alpha=st["alpha"], ls=st["ls"], zorder=2)

# 3) builds_on / extends
for e in [x for x in hard if x["relation"] in ("builds_on","extends")]:
    s, t = pos[e["source"]], pos[e["target"]]
    st = EDGE_STYLE[e["relation"]]
    ax.plot([s[0], t[0]], [s[1], t[1]], color=st["color"],
            lw=st["width"], alpha=st["alpha"], ls=st["ls"], zorder=3)

# 4) contradiction (highlight on top)
for e in [x for x in hard if x["relation"]=="contradiction"]:
    s, t = pos[e["source"]], pos[e["target"]]
    st = EDGE_STYLE["contradiction"]
    ax.plot([s[0], t[0]], [s[1], t[1]], color=st["color"],
            lw=st["width"], alpha=st["alpha"], ls=st["ls"], zorder=4)

# 5) nodes
for p in papers:
    pid = p["id"]
    if pid not in pos: continue
    x, y = pos[pid]
    cites = max(0, int(p.get("citations") or 0))
    cat = p.get("category", "X")
    color = CAT_COLOR.get(cat, "#777777")
    r = 28 + 78 * math.log1p(cites) / math.log1p(2000)   # scale: 0 cites → 28, 2000+ → ~106
    ax.scatter([x],[y], s=r, color=color, edgecolor="#1d1d1d",
               linewidth=0.6, alpha=0.92, zorder=5)

# Highlight the top-3 most-cited papers with text labels
top3 = sorted(papers, key=lambda p: int(p.get("citations") or 0), reverse=True)[:3]
for p in top3:
    if p["id"] not in pos: continue
    x, y = pos[p["id"]]
    title = (p.get("label") or "")[:40] + ("…" if len(p.get("label") or "") > 40 else "")
    ax.annotate(f"{title}\n({p.get('citations')} cites)",
                xy=(x, y), xytext=(x+0.06, y+0.05),
                fontsize=7, color="#222",
                arrowprops=dict(arrowstyle="-", color="#777", lw=0.5),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#aaa", lw=0.4),
                zorder=6)

# Title + caption
ax.set_title("CampusRide knowledge graph — 100 papers, 5,044 paper→paper edges",
             fontsize=15, weight="semibold", pad=18, color="#1d1d1d")
caption = ("Force-directed layout. Node colour = category (A-J), node size ∝ log(citation count). "
           "Background grey = sampled conceptual_overlap (120 of 2,542 shown for legibility); "
           "purple = methodological_mirror (80); gold = builds_on/extends (6); "
           "red dashed = contradiction (16). Top-3 most-cited papers labelled.")
ax.text(0.5, -0.045, caption, transform=ax.transAxes, ha="center", va="top",
        fontsize=8.5, color="#444", wrap=True)

# Legend: categories (left) + edge types (right)
ax.set_xticks([]); ax.set_yticks([])
ax.set_aspect("equal")
ax.margins(0.02)

cat_handles = [
    Line2D([0],[0], marker="o", linestyle="",
           markerfacecolor=CAT_COLOR[c], markeredgecolor="#1d1d1d",
           markersize=8, label=f"{c} · {CAT_NAME[c]}")
    for c in "ABCDEFGHIJ"
]
edge_handles = [
    Line2D([0],[0], color=EDGE_STYLE["conceptual_overlap"]["color"], lw=1.2, label="conceptual_overlap (sampled)"),
    Line2D([0],[0], color=EDGE_STYLE["methodological_mirror"]["color"], lw=1.2, label="methodological_mirror"),
    Line2D([0],[0], color="#D4AC2A", lw=1.2, label="builds_on / extends"),
    Line2D([0],[0], color=EDGE_STYLE["contradiction"]["color"], lw=1.4,
           ls=(0,(4,2)), label="contradiction"),
]
leg1 = ax.legend(handles=cat_handles, loc="upper left", bbox_to_anchor=(1.01, 1.0),
                 frameon=False, fontsize=8.5, title="Category",
                 title_fontsize=9, alignment="left")
leg2 = ax.legend(handles=edge_handles, loc="lower left", bbox_to_anchor=(1.01, 0.0),
                 frameon=False, fontsize=8.5, title="Edge type",
                 title_fontsize=9, alignment="left")
ax.add_artist(leg1)

plt.subplots_adjust(left=0.02, right=0.80, top=0.92, bottom=0.07)
plt.savefig(OUT_PDF, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.savefig(OUT_PNG, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Wrote {OUT_PDF}\nWrote {OUT_PNG}")
