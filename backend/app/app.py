"""
app.py

FastAPI backend for querying NASA bioscience publications using:
- FAISS vector index for retrieval
- Ollama LLM for generating answers
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import ujson as json
from pathlib import Path
from ollama import Ollama  # assuming you installed ollama Python SDK

# Directories
INDEX_DIR = Path("data/index")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

# Initialize FastAPI
app = FastAPI(title="NASA Bio Publications QA API")

# Load embedding model
model = SentenceTransformer(EMBED_MODEL_NAME)

# Load FAISS index and metadata
faiss_index = faiss.read_index(str(INDEX_DIR / "faiss.index"))
with open(INDEX_DIR / "index_to_chunk.json", "r", encoding="utf-8") as fh:
    metadata = json.load(fh)

# Initialize Ollama client
ollama_client = Ollama(model="llama2")  # replace with your local Ollama model

# Pydantic model for request
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

def retrieve_top_k(query: str, k=5):
    """
    Retrieve top-k relevant chunks from FAISS index.
    """
    q_emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = faiss_index.search(q_emb, k)
    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(metadata):
            chunk_info = metadata[idx].copy()
            chunk_info["score"] = float(score)
            results.append(chunk_info)
    return results

@app.post("/ask")
def ask(query_request: QueryRequest):
    """
    Endpoint to ask a question.
    Returns the top-k retrieved chunks + Ollama-generated answer.
    """
    query = query_request.query
    top_k = query_request.top_k

    # Retrieve top chunks
    chunks = retrieve_top_k(query, top_k)
    context_text = "\n\n".join([c["text_preview"] for c in chunks])

    # Prepare prompt for Ollama
    prompt = f"Answer the question based on the following context:\n\n{context_text}\n\nQuestion: {query}\nAnswer:"

    # Call Ollama
    response = ollama_client.generate(prompt)

    return {
        "query": query,
        "top_chunks": chunks,
        "answer": response.text  # depends on Ollama SDK
    }

def main():
    app.run(app, host="127.0.0.1", port=80)

if __name__ == "__main__":
    main()