from fastapi import APIRouter, Query
from db.client import supabase

router = APIRouter(prefix="/api/articles", tags=["System"])

@router.get("/")
def get_articles(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """
    Fetch articles with pagination.
    - page: which page of results (1-based)
    - page_size: number of items per page (max 100)
    """
    start = (page - 1) * page_size
    end = start + page_size - 1  # Supabase range is inclusive

    response = (
        supabase.table("articles")
        .select("*")
        .range(start, end)
        .execute()
    )

    if response.error:
        return {"error": str(response.error)}

    return {
        "page": page,
        "page_size": page_size,
        "articles": response.data,
        "total": len(response.data),  # optional, for current page count
    }
