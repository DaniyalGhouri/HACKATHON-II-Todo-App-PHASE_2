from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .services.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB
    init_db()
    yield
    # Shutdown

app = FastAPI(title="Todo AI Chatbot", lifespan=lifespan)

# CORS Configuration
origins = [
    "http://localhost:3000", # Frontend
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Phase 3 Todo AI API is Live", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

from .api import chat, tasks
app.include_router(chat.router)
app.include_router(tasks.router)