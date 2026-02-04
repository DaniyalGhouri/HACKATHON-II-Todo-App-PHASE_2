from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from src.auth.utils import verify_token
from sqlmodel import Session
from sqlalchemy import text
from src.db import get_session
from datetime import datetime

# Define the scheme. 
# Note: Better Auth uses cookies by default, but we mandated Bearer header for API calls in the spec.
# We set auto_error=False to allow us to check for the cookie if the header is missing.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_current_user(
    request: Request, 
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
    db: Session = Depends(get_session)
):
    """
    Dependency to validate the Bearer token or Session Cookie and return the user payload.
    Checks both JWT (stateless) and DB Session (stateful).
    """
    if not token:
        token = request.cookies.get("better-auth.session_token")

    if not token:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 1. Try JWT Verification
    try:
        payload = verify_token(token)
        user_id = payload.get("sub") or payload.get("id")
        if user_id:
            return {"id": user_id, "email": payload.get("email")}
    except Exception:
        # JWT failed (likely not a JWT), fall through to DB check
        pass

    # 2. Try DB Session Verification (Opaque Token)
    try:
        # Better Auth tables are usually snake_case in Postgres: "session", "user"
        # Columns: "token", "expiresAt" or "expires_at", "userId" or "user_id"
        # We try standard snake_case first (Postgres default for Better Auth)
        # Note: We need to handle potential camelCase if Better Auth configured it so.
        
        # Handle Signed Cookie Tokens (format: raw_token.signature)
        # The DB stores the raw token, but the cookie has a signature.
        token_to_check = token
        if "." in token:
            token_to_check = token.split(".")[0]

        # Query session table
        # We quote columns because they are CamelCase in the DB
        # confirmed by debug_auth.py: userId, expiresAt
        query = text('SELECT "userId", "expiresAt" FROM "session" WHERE "token" = :token')
        
        try:
            result = db.exec(query, params={"token": token_to_check}).first()
        except Exception as e:
             print(f"DB Query Error: {e}")
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Handle row access
        # result is (userId, expiresAt)
        user_id = result[0]
        expires_at = result[1]

        if not user_id or not expires_at:
             raise HTTPException(status_code=401, detail="Corrupt session data")
             
        # Ensure expires_at is timezone-aware if the DB returns one, or naive. 
        # datetime.now() is naive. datetime.now(timezone.utc) is aware.
        # DB usually returns aware if type is TIMESTAMPTZ.
        now = datetime.now(expires_at.tzinfo) if expires_at.tzinfo else datetime.now()

        if expires_at < now:
             raise HTTPException(status_code=401, detail="Session expired")

        # Fetch user email
        # User table also likely uses CamelCase or lowercase? 
        # Debug output showed 'user' table exists. 
        # We assume standard 'id' and 'email' columns, but quoting 'id' is safer if camelCase used elsewhere.
        user_query = text('SELECT "email" FROM "user" WHERE "id" = :uid')
        user_res = db.exec(user_query, params={"uid": user_id}).first()
        email = user_res[0] if user_res else "unknown"

        return {"id": user_id, "email": email}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
