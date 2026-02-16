import jwt
import os
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, text
from ..services.db import get_session

# Load secret for JWT verification (Option B)
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

security = HTTPBearer(auto_error=False)

def get_current_user(
    request: Request, 
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: Session = Depends(get_session)
) -> dict:
    """
    Hybrid Authentication: 
    1. Tries to decode as JWT (Stateless/Option B)
    2. Falls back to Database Session lookup (Stateful/Option C)
    """
    token = None
    if credentials:
        token = credentials.credentials
    if not token:
        token = request.cookies.get("better-auth.session_token")
        
    if not token:
        # Fallback for local development
        if os.getenv("ENV") == "development":
            return {"id": "dev-user", "email": "dev@example.com", "name": "Dev User"}
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # --- STEP 1: JWT DECODE (Option B) ---
    if BETTER_AUTH_SECRET:
        try:
            payload = jwt.decode(
                token, 
                BETTER_AUTH_SECRET, 
                algorithms=["HS256"], 
                options={"verify_aud": False, "verify_iss": False},
                leeway=60
            )
            return {
                "id": payload.get("id") or payload.get("sub"),
                "email": payload.get("email"),
                "name": payload.get("name")
            }
        except Exception:
            pass # Fall through to DB

    # --- STEP 2: DATABASE LOOKUP (Option C) ---
    try:
        # Check standard camelCase first, then fallback to lowercase
        session_query = text('SELECT "userId" FROM "session" WHERE "token" = :token LIMIT 1')
        result = db_session.execute(session_query, {"token": token}).first()
        
        if not result:
            session_query = text('SELECT userid FROM session WHERE token = :token LIMIT 1')
            result = db_session.execute(session_query, {"token": token}).first()

        if result:
            user_id = result[0]
            user_query = text('SELECT "id", "email", "name" FROM "user" WHERE "id" = :id LIMIT 1')
            user_record = db_session.execute(user_query, {"id": user_id}).first()
            
            if not user_record:
                user_query = text('SELECT id, email, name FROM "user" WHERE id = :id LIMIT 1')
                user_record = db_session.execute(user_query, {"id": user_id}).first()

            if user_record:
                return {"id": user_record[0], "email": user_record[1], "name": user_record[2]}

    except Exception as e:
        print(f"Auth Database Error: {e}")

    raise HTTPException(status_code=401, detail="Invalid session or token")

def get_current_user_id(user: dict = Depends(get_current_user)) -> str:
    return user["id"]