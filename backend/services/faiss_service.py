import faiss
import ujson as json
from sentence_transformers import SentenceTransformer
from pathlib import Path
import numpy as np

INDEX_PATH = Path("data/index/faiss.index")
META_PATH = Path("data/index/index_to_chunk.json")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

# Global variables
index: faiss.Index = None
metadata = []
model: SentenceTransformer = None

def load_index_and_model():
    global index, metadata, model
    print("Loading FAISS index...")
    index = faiss.read_index(str(INDEX_PATH))
    print("Loading metadata...")
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    print("Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL_NAME)
    print("FAISS index, metadata, and model loaded successfully.")

def query_faiss(question: str, top_k: int):
    q_vec = model.encode([question])
    faiss.normalize_L2(q_vec)
    D, I = index.search(q_vec, top_k)
    results = []
    for score, idx in zip(D[0], I[0]):
        meta = metadata[idx]
        results.append({
            "chunk_id": meta["chunk_id"],
            "publication_id": meta["publication_id"],
            "section": meta["section"],
            "link": meta["link"],
            "text_preview": meta["text_preview"],
            "score": float(score)
        })
    return results

# Load at module import
if __name__ == "__main__":
    load_index_and_model()
