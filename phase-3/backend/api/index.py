from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from src.services.db import init_db
from src.api import chat, tasks
from better_auth import BetterAuth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB
    init_db()
    yield

app = FastAPI(title="Todo AI Chatbot", lifespan=lifespan)

# PROPER PRODUCTION CORS
# We must list the specific origins to allow credentials (cookies)
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

# Initialize Better Auth
auth = BetterAuth(
    secret=os.getenv("BETTER_AUTH_SECRET"),
    database_url=os.getenv("DATABASE_URL")
)

# Better Auth Route Handler - Added "OPTIONS" for Preflight support
@app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def auth_handler(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=204)
    return await auth.handler(request)

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
