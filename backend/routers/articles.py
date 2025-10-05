from fastapi import APIRouter, Query, HTTPException
from supabase import create_client, Client 
from dotenv import load_dotenv
import os 

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")   

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)    

router = APIRouter(prefix="/api/articles", tags=["System"])

@router.get("/")
def get_articles(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=1000)):
    start = (page - 1) * page_size
    end = start + page_size - 1  # inclusive

    response = (
    supabase.table("articles")
    .select("*", count="exact")
    .range(start, end)
    .execute()
    )

    data = response.data if hasattr(response, "data") else response["data"]
    count = response.count if hasattr(response, "count") else response["count"]

    return {
        "page": page,
        "page_size": page_size,
        "articles": data,
        "total_count": count,
        "total_pages": (count + page_size - 1) // page_size,
    }

@router.get("/{article_id}")
def get_article(article_id: int):
    response = supabase.table("articles").select("*").eq("id", article_id).execute()

    return response