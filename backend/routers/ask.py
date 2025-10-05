from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.faiss_service import query_faiss
from services.ollama_service import ask_ollama

router = APIRouter(prefix="/api/ask", tags=["System"])

TOP_K_DEFAULT = 5

# Pydantic models
class AskRequest(BaseModel):
    question: str
    top_k: int = TOP_K_DEFAULT

class ChunkResult(BaseModel):
    chunk_id: str
    publication_id: str
    section: str
    link: str
    text_preview: str
    score: float

class AskResponse(BaseModel):
    answer: str
    context: List[ChunkResult]

@router.post("/", response_model=AskResponse)
def ask(request: AskRequest):
    top_chunks = query_faiss(request.question, request.top_k)
    context_text = "\n\n".join([c["text_preview"] for c in top_chunks])
    prompt = f"Use the following context to answer the question:\n\n{context_text}\n\nQuestion: {request.question}\nAnswer:"
    answer = ask_ollama(prompt)
    return AskResponse(answer=answer, context=[ChunkResult(**c) for c in top_chunks])
