from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, text
import os
from dotenv import load_dotenv
from ..services.db import get_session

load_dotenv()

security = HTTPBearer(auto_error=False)

def get_current_user(
    request: Request, 
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> dict:
    """
    Authenticates the user via Bearer token or session cookie by checking the database.
    This works with Better Auth's shared database strategy.
    """
    token = None
    
    # Try Bearer token first
    if credentials:
        token = credentials.credentials
    
    # Try cookie if no Bearer token
    if not token:
        token = request.cookies.get("better-auth.session_token")
        
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # 1. Look up session in Better Auth's session table
        # We try standard camelCase first (Better Auth default), then fallback to lowercase
        try:
            session_query = text('SELECT "userId", "expiresAt" FROM "session" WHERE "token" = :token LIMIT 1')
            session_record = session.execute(session_query, {"token": token}).first()
        except Exception:
            session_query = text('SELECT userid, expiresat FROM session WHERE token = :token LIMIT 1')
            session_record = session.execute(session_query, {"token": token}).first()
        
        if not session_record:
            # Fallback for development if token is just a user ID
            if os.getenv("ENV") == "development":
                return {"id": token, "email": "dev@example.com"}
            raise HTTPException(status_code=401, detail="Invalid session")

        user_id, expires_at = session_record

        # 2. Get user details from 'user' table
        try:
            user_query = text('SELECT "id", "email", "name" FROM "user" WHERE "id" = :id LIMIT 1')
            user_record = session.execute(user_query, {"id": user_id}).first()
        except Exception:
            user_query = text('SELECT id, email, name FROM "user" WHERE id = :id LIMIT 1')
            user_record = session.execute(user_query, {"id": user_id}).first()
        
        if not user_record:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "id": user_record[0], 
            "email": user_record[1], 
            "name": user_record[2]
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"--- [ERROR] Database Auth Failed: {str(e)} ---")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )

def get_current_user_id(user: dict = Depends(get_current_user)) -> str:
    return user["id"]
