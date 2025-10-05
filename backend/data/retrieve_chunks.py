"""
retrieve_chunks.py

Example of retrieving top-k relevant chunks from the FAISS index
for a user query.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import ujson as json
from pathlib import Path

# Directories
INDEX_DIR = Path("data/index")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

# Load embedding model
print("Loading embedding model")
model = SentenceTransformer(EMBED_MODEL_NAME)
print("Model loaded")

# Load FAISS index
print("Loading FAISS index")
index = faiss.read_index(str(INDEX_DIR / "faiss.index"))
print("FAISS index loaded")

# Load metadata mapping
with open(INDEX_DIR / "index_to_chunk.json", "r", encoding="utf-8") as fh:
    metadata = json.load(fh)

print(f"Loaded metadata for {len(metadata)} chunks")


def retrieve_top_k(query: str, k=5):
    """
    Returns top-k chunks relevant to the query.
    """
    # Compute query embedding
    q_emb = model.encode([query], convert_to_numpy=True)
    # Normalize for cosine similarity
    faiss.normalize_L2(q_emb)

    # Search index
    D, I = index.search(q_emb, k)
    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(metadata):
            chunk_info = metadata[idx].copy()
            chunk_info["score"] = float(score)
            results.append(chunk_info)
    return results


if __name__ == "__main__":
    query = input("Enter your query: ")
    top_chunks = retrieve_top_k(query, k=10)
    for i, c in enumerate(top_chunks, 1):
        print(f"\n--- Chunk {i} (score: {c['score']:.4f}) ---")
        print(f"Publication ID: {c['publication_id']}")
        print(f"Section: {c['section']}")
        print(c["text_preview"])
