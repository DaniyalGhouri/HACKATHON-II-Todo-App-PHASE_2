from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
from .utils import verify_token

load_dotenv()

security = HTTPBearer(auto_error=False)

def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Authenticates the user via Bearer token or session cookie.
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
        # In a real app with Better Auth, you'd verify the session/token properly
        # For now, we use our verify_token utility or mock it
        payload = verify_token(token)
        return payload
    except Exception as e:
        # Fallback for prototype: if verify_token fails but we have a token,
        # and it's not a JWT (e.g. raw user id in dev), handle it.
        # But here we should be strict or provide a clear dev path.
        if os.getenv("ENV") == "development":
             return {"id": token, "email": "dev@example.com"}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def get_current_user_id(user: dict = Depends(get_current_user)) -> str:
    return user["id"]
