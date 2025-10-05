from fastapi import APIRouter
from services.faiss_service import load_index_and_model

router = APIRouter(prefix="/api/reload", tags=["System"])

@router.post("/")
def reload_index():
    load_index_and_model()
    return {"status": "success", "message": "FAISS index, metadata, and model reloaded."}
