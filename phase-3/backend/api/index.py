from fastapi import FastAPI, Request, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import os
import logging
from contextlib import asynccontextmanager
from src.services.db import init_db
from src.api import chat, tasks

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log environment for debugging
logger.info(f"--- [ENV DEBUG] NODE_ENV: {os.getenv('NODE_ENV')} ---")
logger.info(f"--- [ENV DEBUG] ENV: {os.getenv('ENV')} ---")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Trigger DB Init on startup (more stable for HF)
    try:
        if os.getenv("DATABASE_URL"):
            init_db()
            logger.info("Database initialized successfully")
        else:
            logger.warning("DATABASE_URL not found, skipping init_db")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    yield

app = FastAPI(title="Todo AI Chatbot", lifespan=lifespan)

# Add ProxyHeadersMiddleware to ensure correct protocol detection (HTTP vs HTTPS)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )

allowed_origins = [
    "https://hackathon-ii-todo-app-phase-2-5k4v.vercel.app",
    "https://hackathon-ii-todo-app-phase-2.vercel.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
def read_root():
    return {"message": "Phase 3 Todo AI API is Live", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include Routers
app.include_router(chat.router)
app.include_router(tasks.router)