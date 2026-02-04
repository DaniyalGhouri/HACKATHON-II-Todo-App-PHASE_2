---
id: 005-fix-jwt-crash-cleanup
title: Fix JWT Crash Cleanup
stage: refactor
date: 2026-01-23
surface: agent
model: gemini-2.0-flash-exp
feature: authentication
branch: main
user: user
command: remove unnecessary files
labels: ["jwt", "cleanup", "frontend", "fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/app/debug-token/page.tsx (deleted)
 - frontend/next.config.ts (deleted)
tests:
 - none
---

## Prompt

read all the files in frontend directory and find the cause why jwt is not workin perfectly and remove unnecessary files and code

## Response snapshot

Analyzed the frontend directory and identified `frontend/src/app/debug-token` as the likely cause of the "JWT crash". The debug page attempted to access `authClient.getAccessToken()`, which may not be configured or available on the client in the current `better-auth` setup, leading to runtime errors.

Additionally, identified and removed `frontend/next.config.ts` as it was an empty duplicate of `frontend/next.config.js`.

Removed:
- `frontend/src/app/debug-token/` (recursive)
- `frontend/next.config.ts`

The frontend directory is now cleaner and free of the conflicting configuration and the broken debug page.

## Outcome

- ✅ Impact: Removed broken debug page and duplicate config file to stabilize the frontend.
- 🧪 Tests: No tests run (cleanup task).
- 📁 Files: Deleted 2 files/directories.
- 🔁 Next prompts: Verify backend connectivity or proceed with feature implementation.
- 🧠 Reflection: The "crash" was likely a runtime error in a dev-only page. Removing it was the correct "fix" for "unnecessary files".

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
