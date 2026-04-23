"""Visualization module — 7 parallel visualization generators.

V1: Category Sunburst (plotly)
V2: Citation Force Graph (pyvis)
V3: Beat × Category Heatmap (seaborn/matplotlib)
V4: Publication Timeline (plotly)
V5: Contradiction Graph (networkx + matplotlib)
V6: Beat Sankey Flow (plotly)
V7: 3D Embedding Cloud (UMAP + plotly)
"""

from __future__ import annotations

import json
import logging
import os
from collections import Counter

log = logging.getLogger("research_agent")

CAT_NAMES = {
    "A": "Small-Town Transport Gap", "B": "P2P Ridesharing Trust",
    "C": "Grassroots Coordination", "D": "International Students",
    "E": "Identity Verification", "F": "Shared-Mobility Safety",
    "G": "Gamification", "H": "Rating Fairness",
    "I": "Super-Apps / Integrated Platforms", "J": "Algorithmic Mgmt Critique",
    "X": "Uncategorized",
}

BEAT_CATS = {
    "Beat 1: Transport Gap": ["A", "B"],
    "Beat 2: Grassroots + Super-App": ["C", "D", "I"],
    "Beat 3: Design Primitives": ["E", "F", "G", "H"],
    "Beat 4: Passenger Survey": [],
    "Beat 5: Driver Tolerance": ["F", "H"],
    "Beat 6: CampusRide Platform": [],
    "Beat 7: Adversarial Scoping": ["J", "H"],
}

CAT_COLORS = {
    "A": "#e74c3c", "B": "#e67e22", "C": "#f1c40f", "D": "#2ecc71",
    "E": "#1abc9c", "F": "#3498db", "G": "#9b59b6", "H": "#e91e63",
    "I": "#00bcd4", "J": "#ff9800", "X": "#95a5a6",
}


def run_all_visualizations(base_dir: str):
    """Run all 7 visualizations. Each is independent — failures don't block others."""
    fig_dir = os.path.join(base_dir, "output", "figures")
    os.makedirs(fig_dir, exist_ok=True)

    proc_dir = os.path.join(base_dir, "data", "processed")
    analysis_dir = os.path.join(base_dir, "analysis")

    from .utils import load_json

    # Load data
    classified_path = os.path.join(proc_dir, "classified.json")
    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return

    classified = load_json(classified_path)
    log.info(f"Generating visualizations for {len(classified)} papers")

    # Load optional data
    graph_path = os.path.join(proc_dir, "relationship_graph.json")
    graph_data = load_json(graph_path) if os.path.exists(graph_path) else None

    contradictions_path = os.path.join(analysis_dir, "contradictions.json")
    contradictions = load_json(contradictions_path) if os.path.exists(contradictions_path) else None

    chains_path = os.path.join(analysis_dir, "narrative_chains.json")
    chains = load_json(chains_path) if os.path.exists(chains_path) else None

    # Run each viz independently
    viz_funcs = [
        ("V1_sunburst", lambda: v1_category_sunburst(classified, fig_dir)),
        ("V2_force_graph", lambda: v2_citation_force_graph(classified, graph_data, fig_dir)),
        ("V3_heatmap", lambda: v3_beat_heatmap(classified, fig_dir)),
        ("V4_timeline", lambda: v4_publication_timeline(classified, fig_dir)),
        ("V5_contradiction", lambda: v5_contradiction_graph(contradictions, classified, fig_dir)),
        ("V6_sankey", lambda: v6_beat_sankey(classified, fig_dir)),
        ("V7_embedding", lambda: v7_embedding_cloud(classified, fig_dir)),
    ]

    results = {}
    for name, func in viz_funcs:
        try:
            path = func()
            results[name] = {"status": "ok", "path": path}
            log.info(f"  ✅ {name}: {path}")
        except ImportError as e:
            results[name] = {"status": "skip", "reason": f"Missing dependency: {e}"}
            log.warning(f"  ⏭ {name}: skipped (missing dependency: {e})")
        except Exception as e:
            results[name] = {"status": "error", "reason": str(e)}
            log.error(f"  ❌ {name}: {e}")

    from .utils import atomic_write_json
    atomic_write_json(os.path.join(fig_dir, "viz_results.json"), results)
    ok = sum(1 for v in results.values() if v["status"] == "ok")
    log.info(f"Visualizations complete: {ok}/{len(viz_funcs)} succeeded")


# ---------------------------------------------------------------------------
# V1: Category Sunburst
# ---------------------------------------------------------------------------

def v1_category_sunburst(classified: list[dict], fig_dir: str) -> str:
    """Hierarchical sunburst: Beat → Category → Paper count."""
    import plotly.graph_objects as go

    labels, parents, values, colors = [], [], [], []

    # Root
    labels.append("Corpus")
    parents.append("")
    values.append(0)
    colors.append("#ecf0f1")

    # Beat level
    for beat_name, cats in BEAT_CATS.items():
        beat_papers = [p for p in classified
                       if p.get("primary_category") in cats]
        labels.append(beat_name)
        parents.append("Corpus")
        values.append(len(beat_papers))
        colors.append("#bdc3c7")

        # Category level under each beat
        for cat in cats:
            cat_papers = [p for p in classified if p.get("primary_category") == cat]
            cat_label = f"{cat}: {CAT_NAMES.get(cat, cat)}"
            labels.append(cat_label)
            parents.append(beat_name)
            values.append(len(cat_papers))
            colors.append(CAT_COLORS.get(cat, "#95a5a6"))

    fig = go.Figure(go.Sunburst(
        labels=labels, parents=parents, values=values,
        marker=dict(colors=colors),
        branchvalues="total",
        hovertemplate="<b>%{label}</b><br>Papers: %{value}<extra></extra>",
    ))
    fig.update_layout(
        title="Paper Corpus: Beat → Category Distribution",
        width=800, height=800, margin=dict(t=50, l=0, r=0, b=0),
    )

    path = os.path.join(fig_dir, "v1_category_sunburst.html")
    fig.write_html(path)
    return path


# ---------------------------------------------------------------------------
# V2: Citation Force Graph
# ---------------------------------------------------------------------------

def v2_citation_force_graph(classified: list[dict], graph_data: dict | None,
                            fig_dir: str) -> str:
    """Interactive force-directed citation graph using pyvis."""
    from pyvis.network import Network

    net = Network(height="800px", width="100%", bgcolor="#1a1a2e",
                  font_color="white", directed=True)
    net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=150)

    by_id = {p["paperId"]: p for p in classified}

    # Add nodes
    for p in classified:
        cat = p.get("primary_category", "X")
        color = CAT_COLORS.get(cat, "#95a5a6")
        size = min(5 + (p.get("citationCount", 0) ** 0.5) * 2, 40)
        title = (f"<b>{p.get('title', '?')[:80]}</b><br>"
                 f"Year: {p.get('year', '?')}<br>"
                 f"Category: {cat} ({CAT_NAMES.get(cat, '')})<br>"
                 f"Citations: {p.get('citationCount', 0)}")
        net.add_node(p["paperId"], label=f"{p.get('year', '')}", title=title,
                     color=color, size=size)

    # Add edges from graph data
    if graph_data:
        edge_colors = {"builds_on": "#2ecc71", "contradicts": "#e74c3c",
                       "extends": "#3498db", "related": "#95a5a6"}
        for e in graph_data.get("edges", []):
            src, tgt = e.get("source", ""), e.get("target", "")
            if src in by_id and tgt in by_id:
                etype = e.get("type", "related")
                net.add_edge(src, tgt, color=edge_colors.get(etype, "#95a5a6"),
                             title=e.get("evidence", etype))

    path = os.path.join(fig_dir, "v2_citation_force_graph.html")
    net.save_graph(path)
    return path


# ---------------------------------------------------------------------------
# V3: Beat × Category Heatmap
# ---------------------------------------------------------------------------

def v3_beat_heatmap(classified: list[dict], fig_dir: str) -> str:
    """Heatmap showing paper density per Beat × Category."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    beats = list(BEAT_CATS.keys())
    cats = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

    matrix = np.zeros((len(beats), len(cats)))
    for i, (beat_name, beat_cats) in enumerate(BEAT_CATS.items()):
        for j, cat in enumerate(cats):
            if cat in beat_cats:
                count = sum(1 for p in classified if p.get("primary_category") == cat)
                matrix[i][j] = count

    fig, ax = plt.subplots(figsize=(14, 6))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")

    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels([f"{c}\n{CAT_NAMES.get(c, '')[:15]}" for c in cats],
                       fontsize=8, rotation=45, ha="right")
    ax.set_yticks(range(len(beats)))
    ax.set_yticklabels(beats, fontsize=10)

    # Annotate cells
    for i in range(len(beats)):
        for j in range(len(cats)):
            val = int(matrix[i][j])
            if val > 0:
                color = "white" if val > matrix.max() * 0.6 else "black"
                ax.text(j, i, str(val), ha="center", va="center",
                        fontsize=10, fontweight="bold", color=color)

    plt.colorbar(im, ax=ax, label="Paper Count")
    ax.set_title("Evidence Density: Beat × Category", fontsize=14, fontweight="bold")
    plt.tight_layout()

    path = os.path.join(fig_dir, "v3_beat_heatmap.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# V4: Publication Timeline
# ---------------------------------------------------------------------------

def v4_publication_timeline(classified: list[dict], fig_dir: str) -> str:
    """Interactive timeline showing publication year distribution by category."""
    import plotly.graph_objects as go

    cats = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
    years = sorted(set(p.get("year", 0) for p in classified if p.get("year", 0) > 2015))

    if not years:
        years = list(range(2020, 2027))

    fig = go.Figure()
    for cat in cats:
        cat_papers = [p for p in classified if p.get("primary_category") == cat]
        year_counts = Counter(p.get("year", 0) for p in cat_papers)
        y_vals = [year_counts.get(yr, 0) for yr in years]
        fig.add_trace(go.Bar(
            name=f"{cat}: {CAT_NAMES.get(cat, '')[:20]}",
            x=years, y=y_vals,
            marker_color=CAT_COLORS.get(cat, "#95a5a6"),
        ))

    fig.update_layout(
        barmode="stack",
        title="Publication Timeline by Category",
        xaxis_title="Year", yaxis_title="Paper Count",
        width=1000, height=500,
        legend=dict(font=dict(size=9)),
    )

    path = os.path.join(fig_dir, "v4_publication_timeline.html")
    fig.write_html(path)
    return path


# ---------------------------------------------------------------------------
# V5: Contradiction Graph
# ---------------------------------------------------------------------------

def v5_contradiction_graph(contradictions: dict | None, classified: list[dict],
                           fig_dir: str) -> str:
    """Graph showing contradicting paper pairs, colored by severity."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx

    if not contradictions or not contradictions.get("contradictions"):
        # Generate placeholder
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "No contradictions found yet.\nRun Phase 3.7 first.",
                ha="center", va="center", fontsize=14, transform=ax.transAxes)
        ax.set_axis_off()
        path = os.path.join(fig_dir, "v5_contradiction_graph.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    by_id = {p["paperId"]: p for p in classified}
    G = nx.Graph()

    severity_colors = {"critical": "#e74c3c", "moderate": "#f39c12", "minor": "#27ae60"}
    severity_widths = {"critical": 3.0, "moderate": 2.0, "minor": 1.0}

    for c in contradictions["contradictions"]:
        pa_id = c.get("paper_a", {}).get("paperId", "")
        pb_id = c.get("paper_b", {}).get("paperId", "")
        if not pa_id or not pb_id:
            continue

        for pid in (pa_id, pb_id):
            if pid not in G:
                p = by_id.get(pid, {})
                cat = p.get("primary_category", "X")
                G.add_node(pid, label=p.get("title", pid)[:30],
                           color=CAT_COLORS.get(cat, "#95a5a6"))

        severity = c.get("severity", "minor")
        G.add_edge(pa_id, pb_id, color=severity_colors.get(severity, "#95a5a6"),
                   width=severity_widths.get(severity, 1.0),
                   label=c.get("type", ""))

    fig, ax = plt.subplots(figsize=(12, 10))
    pos = nx.spring_layout(G, k=2, seed=42)

    node_colors = [G.nodes[n].get("color", "#95a5a6") for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=300, alpha=0.9)

    for u, v, d in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax,
                               edge_color=d.get("color", "#95a5a6"),
                               width=d.get("width", 1.0), alpha=0.7)

    labels = {n: G.nodes[n].get("label", n[:10]) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=7)

    ax.set_title("Contradiction Map", fontsize=14, fontweight="bold")
    ax.set_axis_off()

    # Legend
    for sev, color in severity_colors.items():
        ax.plot([], [], color=color, linewidth=severity_widths[sev], label=sev)
    ax.legend(loc="lower right", fontsize=9)

    plt.tight_layout()
    path = os.path.join(fig_dir, "v5_contradiction_graph.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# V6: Beat Sankey Flow
# ---------------------------------------------------------------------------

def v6_beat_sankey(classified: list[dict], fig_dir: str) -> str:
    """Sankey diagram: Category → Beat → Section mapping."""
    import plotly.graph_objects as go

    cats = sorted(set(p.get("primary_category", "X") for p in classified) - {"X"})
    beats = list(BEAT_CATS.keys())

    # Node indices: categories first, then beats
    cat_indices = {c: i for i, c in enumerate(cats)}
    beat_indices = {b: len(cats) + i for i, b in enumerate(beats)}

    labels = [f"{c}: {CAT_NAMES.get(c, '')[:20]}" for c in cats] + beats
    node_colors = [CAT_COLORS.get(c, "#95a5a6") for c in cats] + ["#bdc3c7"] * len(beats)

    sources, targets, values, link_colors = [], [], [], []

    for beat_name, beat_cats in BEAT_CATS.items():
        for cat in beat_cats:
            if cat not in cat_indices:
                continue
            count = sum(1 for p in classified if p.get("primary_category") == cat)
            if count > 0:
                sources.append(cat_indices[cat])
                targets.append(beat_indices[beat_name])
                values.append(count)
                # Convert hex to rgba for plotly Sankey compatibility
                hex_c = CAT_COLORS.get(cat, "#95a5a6")
                r, g, b = int(hex_c[1:3], 16), int(hex_c[3:5], 16), int(hex_c[5:7], 16)
                link_colors.append(f"rgba({r},{g},{b},0.5)")

    fig = go.Figure(go.Sankey(
        node=dict(pad=15, thickness=20, label=labels, color=node_colors),
        link=dict(source=sources, target=targets, value=values, color=link_colors),
    ))
    fig.update_layout(
        title="Literature Flow: Category → Beat",
        width=1000, height=600,
    )

    path = os.path.join(fig_dir, "v6_beat_sankey.html")
    fig.write_html(path)
    return path


# ---------------------------------------------------------------------------
# V7: 3D Embedding Cloud (UMAP)
# ---------------------------------------------------------------------------

def v7_embedding_cloud(classified: list[dict], fig_dir: str) -> str:
    """3D embedding visualization using SPECTER2 vectors + Nomic Atlas or UMAP fallback."""
    proc_dir = os.path.join(os.path.dirname(fig_dir), "..", "data", "processed")
    emb_path = os.path.join(proc_dir, "specter_embeddings.npy")
    meta_path = os.path.join(proc_dir, "specter_metadata.json")

    # Try SPECTER2 + Nomic Atlas first
    if os.path.exists(emb_path) and os.path.exists(meta_path):
        import numpy as np
        embeddings = np.load(emb_path)
        metadata = load_json_local(meta_path)

        # Try Nomic Atlas
        try:
            return _v7_nomic_atlas(embeddings, metadata, fig_dir)
        except Exception as e:
            log.warning(f"  Nomic Atlas failed ({e}), falling back to UMAP+plotly")

        # Fallback: SPECTER2 + UMAP + plotly
        try:
            return _v7_umap_plotly(embeddings, metadata, fig_dir)
        except Exception as e:
            log.warning(f"  SPECTER2 UMAP failed ({e}), falling back to TF-IDF")

    # Final fallback: TF-IDF + UMAP
    return _v7_tfidf_fallback(classified, fig_dir)


def _v7_nomic_atlas(embeddings, metadata: list[dict], fig_dir: str) -> str:
    """Upload to Nomic Atlas for interactive exploration."""
    import nomic
    from nomic import atlas
    from nomic.dataset import AtlasDataset
    import os as _os

    nomic_key = _os.environ.get("NOMIC_API_KEY")
    if not nomic_key:
        raise ValueError("NOMIC_API_KEY not set")

    nomic.login(nomic_key)

    # Prepare data with unique IDs (Nomic Atlas requires <= 36 chars)
    import hashlib
    for i, m in enumerate(metadata):
        raw_id = m.get("paperId", str(i))
        if len(raw_id) > 36:
            m["uid"] = hashlib.md5(raw_id.encode()).hexdigest()
        else:
            m["uid"] = raw_id
        m["cat_name"] = CAT_NAMES.get(m.get("category", "X"), "Unknown")

    dataset_name = "research-agent-paper-corpus"

    # Check if dataset already exists
    try:
        existing = AtlasDataset(dataset_name)
        atlas_url = f"https://atlas.nomic.ai/data/{existing.meta.get('organization_slug', 'unknown')}/{existing.meta.get('slug', dataset_name)}"
        log.info(f"  Nomic Atlas dataset already exists: {atlas_url}")
    except Exception:
        # Create new dataset
        project = atlas.map_data(
            embeddings=embeddings,
            data=metadata,
            id_field="uid",
            identifier=dataset_name,
            description="SPECTER2 embeddings of 200 papers for PhD thesis",
            topic_model=True,
        )
        atlas_url = f"https://atlas.nomic.ai/data/{project.meta.get('organization_slug', 'unknown')}/{project.meta.get('slug', dataset_name)}"
        log.info(f"  Nomic Atlas map created: {atlas_url}")

    # Save URL reference
    ref_path = os.path.join(fig_dir, "v7_nomic_atlas_url.txt")
    with open(ref_path, "w") as f:
        f.write(f"Nomic Atlas interactive map:\n{atlas_url}\n")
    return ref_path


def _v7_umap_plotly(embeddings, metadata: list[dict], fig_dir: str) -> str:
    """SPECTER2 embeddings → UMAP 3D → plotly."""
    from umap import UMAP
    import plotly.graph_objects as go

    n_neighbors = min(15, len(metadata) - 1)
    reducer = UMAP(n_components=3, n_neighbors=n_neighbors, min_dist=0.1,
                   metric="cosine", random_state=42)
    coords = reducer.fit_transform(embeddings)

    fig = go.Figure()
    cats = sorted(set(m.get("category", "X") for m in metadata))
    for cat in cats:
        mask = [i for i, m in enumerate(metadata) if m.get("category") == cat]
        if not mask:
            continue
        fig.add_trace(go.Scatter3d(
            x=[coords[i][0] for i in mask],
            y=[coords[i][1] for i in mask],
            z=[coords[i][2] for i in mask],
            mode="markers",
            name=f"{cat}: {CAT_NAMES.get(cat, '')[:20]}",
            marker=dict(size=4, color=CAT_COLORS.get(cat, "#95a5a6"), opacity=0.8),
            text=[f"{metadata[i].get('title', '?')[:60]}<br>"
                  f"Year: {metadata[i].get('year', '?')}<br>"
                  f"Cites: {metadata[i].get('citationCount', 0)}"
                  for i in mask],
            hoverinfo="text",
        ))

    fig.update_layout(
        title="Paper Embedding Space (SPECTER2 + UMAP 3D)",
        width=1000, height=800,
        scene=dict(xaxis_title="UMAP-1", yaxis_title="UMAP-2", zaxis_title="UMAP-3",
                   bgcolor="#1a1a2e"),
        paper_bgcolor="#1a1a2e", font=dict(color="white"),
        legend=dict(font=dict(size=9)),
    )

    path = os.path.join(fig_dir, "v7_embedding_cloud.html")
    fig.write_html(path)
    return path


def _v7_tfidf_fallback(classified: list[dict], fig_dir: str) -> str:
    """TF-IDF + UMAP fallback when no SPECTER2 embeddings available."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from umap import UMAP
    import plotly.graph_objects as go

    papers = [p for p in classified if p.get("abstract") and len(p["abstract"]) > 50]
    if len(papers) < 10:
        raise ValueError(f"Only {len(papers)} papers with abstracts — need at least 10")

    abstracts = [p["abstract"][:1000] for p in papers]
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(abstracts)

    n_neighbors = min(15, len(papers) - 1)
    reducer = UMAP(n_components=3, n_neighbors=n_neighbors, min_dist=0.1,
                   metric="cosine", random_state=42)
    coords = reducer.fit_transform(tfidf_matrix.toarray())

    fig = go.Figure()
    cats = sorted(set(p.get("primary_category", "X") for p in papers))
    for cat in cats:
        mask = [i for i, p in enumerate(papers) if p.get("primary_category") == cat]
        if not mask:
            continue
        fig.add_trace(go.Scatter3d(
            x=[coords[i][0] for i in mask],
            y=[coords[i][1] for i in mask],
            z=[coords[i][2] for i in mask],
            mode="markers",
            name=f"{cat}: {CAT_NAMES.get(cat, '')[:20]}",
            marker=dict(size=4, color=CAT_COLORS.get(cat, "#95a5a6"), opacity=0.8),
            text=[f"{papers[i].get('title', '?')[:60]}<br>"
                  f"Year: {papers[i].get('year', '?')}<br>"
                  f"Cites: {papers[i].get('citationCount', 0)}"
                  for i in mask],
            hoverinfo="text",
        ))

    fig.update_layout(
        title="Paper Embedding Space (TF-IDF + UMAP 3D)",
        width=1000, height=800,
        scene=dict(xaxis_title="UMAP-1", yaxis_title="UMAP-2", zaxis_title="UMAP-3",
                   bgcolor="#1a1a2e"),
        paper_bgcolor="#1a1a2e", font=dict(color="white"),
        legend=dict(font=dict(size=9)),
    )

    path = os.path.join(fig_dir, "v7_embedding_cloud.html")
    fig.write_html(path)
    return path


def load_json_local(path: str):
    """Local JSON loader to avoid circular imports."""
    import json
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
