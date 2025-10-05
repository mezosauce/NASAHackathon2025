# app.py
from importlib import reload
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers import ask, health, reload_faiss
from db.client import supabase  # Import the supabase client
import uvicorn

reload_faiss.load_index_and_model() # Initial load of FAISS

app = FastAPI(title="NASA Hackathon RAG API", version="1.0")

# Register routers
app.include_router(ask.router)
app.include_router(health.router)
app.include_router(reload_faiss.router)

# Simple home route
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>My API Home</title>
        </head>
        <body>
            <h1>API is running!</h1>
            <p>Visit <a href="/docs">/docs</a> for interactive API docs (Swagger UI).</p>
            <p>Visit <a href="/redoc">/redoc</a> for alternative API docs (ReDoc).</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)