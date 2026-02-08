import jwt
import os
from datetime import datetime, timezone
from fastapi import HTTPException, status
from dotenv import load_dotenv # Import load_dotenv
from urllib.parse import unquote # Import unquote

load_dotenv() # Load environment variables here

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET is not set in environment variables")

def verify_token(token: str) -> dict:
    """
    Verifies the JWT token using the shared secret.
    Returns the payload if valid, raises HTTPException if invalid.
    """
    try:
        # URL-decode the token before validation
        decoded_token = unquote(token)
        print(f"--- [DEBUG] Attempting to decode token: {decoded_token} ---")
        
        payload = jwt.decode(decoded_token, BETTER_AUTH_SECRET, algorithms=["HS256"], leeway=10)
        print("--- [DEBUG] Token decoded successfully! ---")
        return payload
    except jwt.ExpiredSignatureError as e:
        print(f"--- [DEBUG] JWT Error: Expired Signature: {e} ---")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        print(f"--- [DEBUG] JWT Error: Invalid Token: {e} ---")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
