from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from src.services.db import init_db
from src.api import chat, tasks
from better_auth import BetterAuth
from fastapi import Request, Response

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB
    init_db()
    yield

app = FastAPI(title="Todo AI Chatbot", lifespan=lifespan)

# Initialize Better Auth
auth = BetterAuth(
    secret=os.getenv("BETTER_AUTH_SECRET"),
    database_url=os.getenv("DATABASE_URL")
)

# Better Auth Route Handler
@app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_handler(request: Request):
    return await auth.handler(request)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hackathon-ii-todo-app-phase-2-5k4v.vercel.app",
        "https://hackathon-ii-todo-app-phase-2.vercel.app",
        "http://localhost:3000"
    ],
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