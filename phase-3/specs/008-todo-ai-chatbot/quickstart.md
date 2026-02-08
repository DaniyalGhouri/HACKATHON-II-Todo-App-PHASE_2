# Quickstart: Phase III Todo AI Chatbot

## Setup

1. **Environment Variables**:
   ```env
   DATABASE_URL=postgresql://... (Neon URL)
   OPENAI_API_KEY=sk-...
   BETTER_AUTH_SECRET=...
   ```

2. **Backend**:
   - Install dependencies: `pip install -r backend/requirements.txt`
   - Run migrations: `python backend/src/db.py` (ensure tables created)
   - Start server: `uvicorn backend.src.main:app --reload`

3. **Frontend**:
   - Install dependencies: `npm install`
   - Start development: `npm run dev`

## Verification Steps

1. **Natural Language Input**:
   - Access the ChatKit UI.
   - Send: "Add a task to prepare the hackathon presentation for Monday."
   - Expected: Assistant confirms task creation.

2. **Persistence Check**:
   - Refresh the page or restart the server.
   - Send: "What was that task I just added?"
   - Expected: Assistant correctly identifies the "hackathon presentation" task.

3. **Multi-tenancy Check**:
   - Log in as a different user.
   - Expected: Previous user's tasks and conversations are NOT visible.
