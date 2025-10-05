# app.py
from importlib import reload
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import ask, health, reload_faiss, articles
from db.client import supabase  # Import the supabase client
import uvicorn

reload_faiss.load_index_and_model() # Initial load of FAISS

app = FastAPI(title="NASA Hackathon RAG API", version="1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["http://localhost:3000"] if using React
    allow_credentials=True,
    allow_methods=["*"],   # or restrict to ["GET", "POST"]
    allow_headers=["*"],   # or restrict to specific headers
)

# Register routers
app.include_router(ask.router)
app.include_router(health.router)
app.include_router(reload_faiss.router)
app.include_router(articles.router)

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