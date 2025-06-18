# main.py

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.lifespan import lifespan
from app.routers import chat as chat_router # Alias to avoid name conflict with chat function

# --- Setup Logging ---
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app with the lifespan manager
app = FastAPI(
    title="RAG Chatbot API (No GPU)",
    description="A Retrieval Augmented Generation (RAG) chatbot API that uses a local dataset (InflationRates.csv) and falls back to internet search if local data is not sufficiently relevant. Powered by CPU-only LLMs.",
    version="1.0.0",
    lifespan=lifespan # Integrate the lifespan context manager
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development. Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FastAPI Endpoints ---

# Mount static files (your frontend HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serves the main HTML page for the chatbot."""
    return FileResponse("static/index.html")

# Include your API routers
app.include_router(chat_router.router) # Now it's chat_router.router