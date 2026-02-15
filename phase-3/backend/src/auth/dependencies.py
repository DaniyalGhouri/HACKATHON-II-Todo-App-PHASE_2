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
    db_session: Session = Depends(get_session)
) -> dict:
    """
    Authenticates the user via Bearer token or session cookie by checking the database.
    """
    token = None
    
    # DEBUG: Log all relevant auth headers
    auth_header = request.headers.get("Authorization")
    cookie_header = request.headers.get("Cookie")
    print(f"--- [AUTH DEBUG] Auth Header: {auth_header[:20] if auth_header else 'None'} ---")
    print(f"--- [AUTH DEBUG] Cookie Present: {bool(cookie_header)} ---")

    # Try Bearer token first
    if credentials:
        token = credentials.credentials
    
    # Try cookie if no Bearer token
    if not token:
        token = request.cookies.get("better-auth.session_token")
        
    if not token:
        print("--- [AUTH DEBUG] No token found in request ---")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # 1. Look up session in Better Auth's session table
        print(f"--- [AUTH DEBUG] Looking up token in DB: {token[:10]}... ---")
        try:
            session_query = text('SELECT "userId", "expiresAt" FROM "session" WHERE "token" = :token LIMIT 1')
            session_record = db_session.execute(session_query, {"token": token}).first()
        except Exception as sql_err:
            print(f"--- [AUTH DEBUG] camelCase query failed, trying lowercase: {sql_err} ---")
            session_query = text('SELECT userid, expiresat FROM session WHERE token = :token LIMIT 1')
            session_record = db_session.execute(session_query, {"token": token}).first()
        
        if not session_record:
            print(f"--- [AUTH DEBUG] Session record NOT found in database ---")
            # Fallback for development if token is just a user ID
            if os.getenv("ENV") == "development":
                return {"id": token, "email": "dev@example.com"}
            raise HTTPException(status_code=401, detail="Invalid session")

        user_id, expires_at = session_record
        print(f"--- [AUTH DEBUG] Session found for user_id: {user_id} ---")

        # 2. Get user details from 'user' table
        try:
            user_query = text('SELECT "id", "email", "name" FROM "user" WHERE "id" = :id LIMIT 1')
            user_record = db_session.execute(user_query, {"id": user_id}).first()
        except Exception:
            user_query = text('SELECT id, email, name FROM "user" WHERE id = :id LIMIT 1')
            user_record = db_session.execute(user_query, {"id": user_id}).first()
        
        if not user_record:
            print(f"--- [AUTH DEBUG] User record NOT found in database for ID: {user_id} ---")
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "id": user_record[0], 
            "email": user_record[1], 
            "name": user_record[2]
        }

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
