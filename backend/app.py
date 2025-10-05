# app.py
from fastapi import FastAPI
from routers import ask, health, reload_faiss
from db.client import supabase  # Import the supabase client
import uvicorn

app = FastAPI(title="NASA Hackathon RAG API", version="1.0")

# Register routers
app.include_router(ask.router)
app.include_router(health.router)
app.include_router(reload_faiss.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
response = supabase.table("chunks").select("*").execute()
print(response.data)  # Print the fetched data