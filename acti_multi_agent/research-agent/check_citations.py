"""
Citation Chain Verifier
查验论文框架中 spine papers 之间的实际引用关系
使用 Semantic Scholar API，无需 API key（公共端点，限速 100 req/5min）

用法: python check_citations.py
输出: citation_chains.json + 可读的终端报告
"""

import requests
import json
import time
import sys

# ============================================================
# 你的论文框架中最关键的 spine papers
# 按 section 分组，每组内的顺序就是 narrative chain 的顺序
# ============================================================

SPINE_PAPERS = {
    "Section 2: Collapse & Contamination": [
        {"id": "DOI:10.52591/lxai202312101", "short": "Self-Consuming MAD (2023)"},
        {"id": "DOI:10.1038/s41586-024-07566-y", "short": "Nature Collapse (2024)"},
        {"id": "DOI:10.48550/arxiv.2410.22812", "short": "π²/6 Pathway (2024)"},
        {"id": "DOI:10.48550/arxiv.2402.07087", "short": "Self-Correcting Loops (2024)"},
        {"id": "DOI:10.48550/arxiv.2407.09499", "short": "Curated Data Preferences (2024)"},
        {"id": "DOI:10.48550/arxiv.2303.11156", "short": "Can AI Text Be Detected (2023)"},
        {"id": "DOI:10.48550/arxiv.2301.10226", "short": "Watermark for LLMs (2023)"},
        {"id": "DOI:10.48550/arxiv.2303.13408", "short": "Paraphrasing Evades (2023)"},
    ],
    "Section 5: Fine-tuning & Social Reasoning": [
        {"id": "DOI:10.18653/v1/2022.emnlp-main.248", "short": "Neural Theory-of-Mind (2022)"},
        {"id": "DOI:10.48550/arxiv.2303.17548", "short": "Whose Opinions (2023)"},
        {"id": "DOI:10.48550/arxiv.2305.11206", "short": "LIMA (2023)"},
        {"id": "DOI:10.48550/arxiv.2305.18290", "short": "DPO (2023)"},
        {"id": "DOI:10.48550/arxiv.2309.00267", "short": "RLAIF (2023)"},
        {"id": "DOI:10.18653/v1/2024.eacl-long.138", "short": "Clever Hans ToM (2024)"},
        {"id": "DOI:10.48550/arxiv.2305.14387", "short": "AlpacaFarm (2023)"},
        {"id": "DOI:10.48550/arxiv.2310.16944", "short": "Zephyr (2023)"},
    ],
    "Section 4: L_auth Ingredients": [
        {"id": "DOI:10.1075/sl.22034.oh", "short": "Robust Complexity Indices (2022)"},
        {"id": "DOI:10.3390/e22040394", "short": "Rényi Entropy Topics (2020)"},
        {"id": "DOI:10.1103/rxxz-lk3n", "short": "Entropy & TTR Gigaword (2025)"},
        {"id": "DOI:10.18653/v1/2024.findings-naacl.228", "short": "Curious Decline Diversity (2024)"},
    ],
    "Cross-section bridges": [
        {"id": "DOI:10.48550/arxiv.2306.01116", "short": "RefinedWeb (2023)"},
        {"id": "DOI:10.48550/arxiv.2406.17557", "short": "FineWeb (2024)"},
        {"id": "DOI:10.48550/arxiv.2309.16671", "short": "Demystifying CLIP Data (2023)"},
        {"id": "DOI:10.48550/arxiv.2403.04652", "short": "Yi Foundation Models (2024)"},
        {"id": "DOI:10.1613/jair.1.15348", "short": "Human-in-the-Loop RL (2024)"},
        {"id": "DOI:10.48550/arxiv.2307.04657", "short": "BeaverTails (2023)"},
    ],
}

BASE_URL = "https://api.semanticscholar.org/graph/v1"
DELAY = 3.5  # seconds between requests (100 req / 5 min = 1 req / 3 sec)


def get_paper_references(paper_id: str) -> dict:
    """Get the list of papers that this paper references (its bibliography)."""
    url = f"{BASE_URL}/paper/{paper_id}/references"
    params = {"fields": "paperId,externalIds,title", "limit": 500}
    try:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"  ⚠ API returned {resp.status_code} for {paper_id}")
            return {"data": []}
    except Exception as e:
        print(f"  ⚠ Error fetching {paper_id}: {e}")
        return {"data": []}


def extract_all_ids(external_ids: dict) -> set:
    """Extract all possible IDs from a paper's externalIds for matching."""
    ids = set()
    if not external_ids:
        return ids
    for key, val in external_ids.items():
        if val:
            ids.add(f"{key}:{val}".upper())
            ids.add(str(val).upper())
    return ids


def normalize_id(paper_id: str) -> str:
    return paper_id.upper()


def main():
    # Collect all paper IDs
    all_papers = []
    for section, papers in SPINE_PAPERS.items():
        for p in papers:
            p["section"] = section
            all_papers.append(p)

    print(f"\n📚 Checking citation chains for {len(all_papers)} key papers...\n")

    # Build a lookup: normalized ID -> paper info
    id_lookup = {}
    for p in all_papers:
        id_lookup[normalize_id(p["id"])] = p

    # For each paper, fetch its references and check which other spine papers it cites
    results = []
    for i, paper in enumerate(all_papers):
        print(f"[{i+1}/{len(all_papers)}] Fetching references for: {paper['short']}")
        refs_data = get_paper_references(paper["id"])
        refs = refs_data.get("data") or []
        print(f"  → Found {len(refs)} references")

        # Check if any reference matches another spine paper
        for ref_entry in refs:
            cited_paper = ref_entry.get("citedPaper", {})
            if not cited_paper:
                continue
            cited_s2_id = cited_paper.get("paperId", "")
            cited_ext_ids = cited_paper.get("externalIds", {}) or {}
            cited_title = cited_paper.get("title", "")

            # Try to match against our spine papers
            all_cited_ids = extract_all_ids(cited_ext_ids)
            if cited_s2_id:
                all_cited_ids.add(cited_s2_id.upper())

            for target_id, target_paper in id_lookup.items():
                if target_paper["id"] == paper["id"]:
                    continue  # skip self
                # Check if any ID matches
                target_norm = normalize_id(target_paper["id"])
                # Extract the DOI/arxiv part
                target_parts = target_norm.split(":", 1)
                if len(target_parts) == 2:
                    target_value = target_parts[1]
                else:
                    target_value = target_norm

                matched = False
                for cid in all_cited_ids:
                    if target_value in cid or cid in target_value:
                        matched = True
                        break

                if matched:
                    edge = {
                        "from": paper["short"],
                        "from_section": paper["section"],
                        "to": target_paper["short"],
                        "to_section": target_paper["section"],
                        "type": "cites",
                    }
                    results.append(edge)
                    print(f"  ✅ CITES → {target_paper['short']}")

        time.sleep(DELAY)

    # Report
    print("\n" + "=" * 60)
    print(f"📊 CITATION CHAIN REPORT")
    print(f"=" * 60)
    print(f"\nTotal verified citation links: {len(results)}")

    # Group by section
    within_section = [r for r in results if r["from_section"] == r["to_section"]]
    cross_section = [r for r in results if r["from_section"] != r["to_section"]]

    print(f"\n--- Within-section links ({len(within_section)}) ---")
    for r in within_section:
        print(f"  {r['from']}  →  {r['to']}")

    print(f"\n--- Cross-section bridges ({len(cross_section)}) ---")
    for r in cross_section:
        print(f"  {r['from']} [{r['from_section']}]")
        print(f"    →  {r['to']} [{r['to_section']}]")

    # Identify gaps
    print(f"\n--- Spine papers with NO outgoing citations to other spine papers ---")
    papers_with_outgoing = {r["from"] for r in results}
    for p in all_papers:
        if p["short"] not in papers_with_outgoing:
            print(f"  ⚠ {p['short']} [{p['section']}]")

    print(f"\n--- Spine papers NEVER cited by another spine paper ---")
    papers_cited = {r["to"] for r in results}
    for p in all_papers:
        if p["short"] not in papers_cited:
            print(f"  ⚠ {p['short']} [{p['section']}]")

    # Save
    output = {
        "total_links": len(results),
        "within_section": len(within_section),
        "cross_section": len(cross_section),
        "edges": results,
        "uncited_papers": [p["short"] for p in all_papers if p["short"] not in papers_cited],
        "no_outgoing_papers": [p["short"] for p in all_papers if p["short"] not in papers_with_outgoing],
    }
    with open("citation_chains.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Results saved to citation_chains.json")


if __name__ == "__main__":
    main()
