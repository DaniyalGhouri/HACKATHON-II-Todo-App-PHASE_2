# Quickstart: Task CRUD Operations

## Prerequisites

- Python 3.13+
- Node.js 18+ (for Frontend)
- Neon PostgreSQL Connection String

## Environment Setup

1. **Backend**:
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database**:
   - Ensure `DATABASE_URL` is set in `backend/.env`.
   - Run migrations (if Alembic is configured, or let SQLModel create tables for dev).

## Running Tests

```bash
# Run backend tests
cd backend
pytest tests/
```

## Manual Verification

1. Start Backend: `uvicorn src.main:app --reload`
2. Start Frontend: `cd frontend && npm run dev`
3. Log in via UI.
4. Create a task.
5. Verify task appears in list.
6. Verify task exists in Neon DB using SQL client.
