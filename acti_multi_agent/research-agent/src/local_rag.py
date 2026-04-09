"""Local RAG: ChromaDB + SPECTER2 for on-demand paper retrieval.

Used by:
- Reviewers (P5): retrieve relevant papers instead of stuffing full corpus into prompt
- STORM debate: retrieve supporting evidence for debaters
- Narrative chains: find semantically similar papers across categories
"""

from __future__ import annotations

import json
import logging
import os

import numpy as np

log = logging.getLogger("research_agent")


def build_local_rag(base_dir: str):
    """Build ChromaDB collection from classified papers + SPECTER2 embeddings.

    Returns the collection object, or None if dependencies/data missing.
    """
    try:
        import chromadb
    except ImportError:
        log.warning("chromadb not installed — local RAG disabled (pip install chromadb)")
        return None

    proc_dir = os.path.join(base_dir, "data", "processed")
    db_path = os.environ.get("CHROMADB_PATH", os.path.join(base_dir, "data", "chromadb"))

    classified_path = os.path.join(proc_dir, "classified.json")
    emb_path = os.path.join(proc_dir, "specter_embeddings.npy")
    meta_path = os.path.join(proc_dir, "specter_metadata.json")

    if not os.path.exists(classified_path):
        log.warning("classified.json not found — cannot build RAG")
        return None

    with open(classified_path, "r", encoding="utf-8") as f:
        classified = json.load(f)

    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(
        name="research_corpus",
        metadata={"hnsw:space": "cosine"},
    )

    # Check if already populated
    if collection.count() >= len(classified) * 0.8:
        log.info(f"RAG collection already has {collection.count()} docs, skipping rebuild")
        return collection

    # Load SPECTER2 embeddings if available
    has_embeddings = os.path.exists(emb_path) and os.path.exists(meta_path)
    if has_embeddings:
        embeddings = np.load(emb_path)
        with open(meta_path, "r", encoding="utf-8") as f:
            emb_metadata = json.load(f)
        emb_by_id = {}
        for i, m in enumerate(emb_metadata):
            emb_by_id[m["paperId"]] = embeddings[i].tolist()
        log.info(f"Loaded {len(emb_by_id)} SPECTER2 embeddings for RAG")
    else:
        emb_by_id = {}
        log.info("No SPECTER2 embeddings — RAG will use ChromaDB's default embedding")

    # Insert papers in batches
    batch_size = 100
    ids, docs, metas, embs = [], [], [], []

    for p in classified:
        pid = p.get("paperId", "")
        if not pid:
            continue

        # Truncate ID for ChromaDB (max 512 chars)
        safe_id = pid[:512]
        abstract = p.get("abstract", "") or ""
        claim = p.get("key_claim", p.get("one_sentence_contribution", "")) or ""
        doc_text = f"{p.get('title', '')}. {abstract[:500]} {claim}"

        if not doc_text.strip():
            continue

        ids.append(safe_id)
        docs.append(doc_text)
        metas.append({
            "category": p.get("primary_category", "X"),
            "year": p.get("year", 0),
            "title": (p.get("title", "") or "")[:200],
            "citations": p.get("citationCount", 0),
        })

        if safe_id in emb_by_id:
            embs.append(emb_by_id[safe_id])
        elif pid in emb_by_id:
            embs.append(emb_by_id[pid])
        else:
            embs.append(None)

    # Split into with/without embeddings
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_docs = docs[i:i + batch_size]
        batch_metas = metas[i:i + batch_size]
        batch_embs = embs[i:i + batch_size]

        # Only pass embeddings if ALL in batch have them
        if all(e is not None for e in batch_embs):
            collection.add(ids=batch_ids, documents=batch_docs,
                           metadatas=batch_metas, embeddings=batch_embs)
        else:
            collection.add(ids=batch_ids, documents=batch_docs,
                           metadatas=batch_metas)

    log.info(f"RAG collection built: {collection.count()} documents in {db_path}")
    return collection


def query_rag(collection, question: str, n_results: int = 10,
              filter_category: str = None) -> list[dict]:
    """Retrieve most relevant papers for a question.

    Returns list of dicts with: id, title, category, year, distance, document.
    """
    if collection is None:
        return []

    where_filter = {"category": filter_category} if filter_category else None

    try:
        results = collection.query(
            query_texts=[question],
            n_results=min(n_results, collection.count()),
            where=where_filter,
        )
    except Exception as e:
        log.warning(f"RAG query failed: {e}")
        return []

    papers = []
    if results and results.get("ids"):
        for i, pid in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i] if results.get("metadatas") else {}
            dist = results["distances"][0][i] if results.get("distances") else None
            doc = results["documents"][0][i] if results.get("documents") else ""
            papers.append({
                "paperId": pid,
                "title": meta.get("title", ""),
                "category": meta.get("category", "X"),
                "year": meta.get("year", 0),
                "distance": dist,
                "document": doc[:300],
            })

    return papers


def query_for_debate(collection, claim: str, category: str = None,
                     n_results: int = 5) -> str:
    """Retrieve supporting evidence for a STORM debate round.

    Returns formatted text ready to inject into debater's prompt.
    """
    papers = query_rag(collection, claim, n_results=n_results,
                       filter_category=category)
    if not papers:
        return "No supporting evidence found in corpus."

    lines = ["Supporting evidence from corpus:"]
    for p in papers:
        lines.append(f"- [{p['year']}] {p['title'][:60]} (cat={p['category']})")
        lines.append(f"  {p['document'][:150]}")
    return "\n".join(lines)
