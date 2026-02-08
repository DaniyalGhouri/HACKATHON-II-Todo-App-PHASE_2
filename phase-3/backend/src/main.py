# This file is a shim for local development.
# It allows 'uvicorn src.main:app' to work while the real entry point is in api/index.py for Vercel.

from api.index import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
