"""
embed_chunks.py

Reads chunk JSONs from data/chunks/, computes embeddings for each chunk using
SentenceTransformers, builds a FAISS index for fast similarity search, and
saves both the index and metadata for retrieval.

Each chunk JSON should contain:
- text
- section
- publication_id
- chunk_index
"""

import ujson as json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from tqdm import tqdm

# Directories
CHUNKS_DIR = Path("data/chunks")
INDEX_DIR = Path("data/index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

# Model & batch parameters
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"  # fast, small
BATCH_SIZE = 64  # embed in batches to avoid OOM

# Initialize embedding model
model = SentenceTransformer(EMBED_MODEL_NAME)

def load_chunks(chunks_dir: Path):
    """
    Read all chunk JSONs and return a list of chunk dicts.
    """
    chunk_files = list(chunks_dir.glob("*.json"))
    if not chunk_files:
        print("No chunk files found in", chunks_dir)
        return []

    chunks = []
    for f in tqdm(chunk_files, desc="Loading Chunks"):
        c = json.load(open(f, "r", encoding="utf-8"))
        chunks.append(c)
    return chunks

def build_faiss_index(chunks):
    """
    Compute embeddings for all chunks, normalize them, and build a FAISS IndexFlatIP.
    Save embeddings, FAISS index, and metadata mapping to disk.
    """
    texts = [c["text"] for c in chunks]
    if not texts:
        print("No chunks to embed!")
        return

    # Compute embeddings in batches
    dim = model.get_sentence_embedding_dimension()
    xb = np.zeros((len(texts), dim), dtype="float32")

    for i in tqdm(range(0, len(texts), BATCH_SIZE), desc="Embedding batches"):
        batch_texts = texts[i:i + BATCH_SIZE]
        emb = model.encode(batch_texts, convert_to_numpy=True, show_progress_bar=False)
        xb[i:i + len(batch_texts)] = emb

    # Normalize for cosine similarity
    faiss.normalize_L2(xb)

    # Build FAISS index (inner product ≈ cosine similarity)
    index = faiss.IndexFlatIP(dim)
    index.add(xb)

    # Save index, embeddings, and metadata
    faiss.write_index(index, str(INDEX_DIR / "faiss.index"))
    np.save(INDEX_DIR / "embeddings.npy", xb)

    metadata = [
        {
            "publication_id": c["publication_id"],
            "section": c["section"],
            "chunk_index": c["chunk_index"],
            "text_preview": c["text"][:400],
        }
        for c in chunks
    ]
    with open(INDEX_DIR / "index_to_chunk.json", "w", encoding="utf-8") as fh:
        json.dump(metadata, fh)

    print(f"FAISS index built! Chunks: {len(chunks)}, dimension: {dim}")
    print(f"Index and metadata saved in {INDEX_DIR.resolve()}")

def main():
    chunks = load_chunks(CHUNKS_DIR)
    if chunks:
        build_faiss_index(chunks)

if __name__ == "__main__":
    main()
