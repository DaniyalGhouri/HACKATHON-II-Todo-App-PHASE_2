# Quickstart: Authentication

## Prerequisites

- `BETTER_AUTH_SECRET` set in `.env` (Must be identical for Frontend and Backend).
- `DATABASE_URL` set in `.env`.

## Environment Variables

```bash
# .env
BETTER_AUTH_SECRET=your_super_secret_key_at_least_32_chars
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://user:pass@host:5432/db
```

## Running Auth (Frontend)

1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Go to `http://localhost:3000/signup`.

## Verifying Auth (Backend)

1. `cd backend`
2. `pip install -r requirements.txt`
3. `uvicorn src.main:app --reload`
4. Send a request to a protected endpoint with the token from the frontend:
   ```bash
   curl -H "Authorization: Bearer <token>" http://localhost:8000/api/protected
   ```
