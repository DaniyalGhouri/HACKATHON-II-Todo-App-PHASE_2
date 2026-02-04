---
id: 002
title: Update Project Constitution
stage: constitution
date: 2026-01-19
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: Admin
command: /sp.constitution
labels: ["governance", "phase-2", "web-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

/sp.constitution You are defining the project constitution using Spec-Kit Plus.

Project: Hackathon Phase II – Todo Full-Stack Web App

Non-negotiable rules:
- Spec-driven development only
- No manual coding
- All features must support multi-user isolation
- JWT authentication required for all API access
- Backend must verify JWT independently
- Frontend uses Better Auth
- Database must be Neon Serverless PostgreSQL
- REST API only (no RPC or GraphQL)
- All changes must be traceable to specs

Output a formal constitution.

## Response snapshot

Updated constitution to v2.0.0 reflecting Full-Stack Web App requirements (Neon, Better Auth, REST).

## Outcome

- ✅ Impact: Constitution updated to v2.0.0.
- 🧪 Tests: N/A
- 📁 Files: Modified constitution.md
- 🔁 Next prompts: /sp.specify
- 🧠 Reflection: Shifted from CLI to Web App context.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
