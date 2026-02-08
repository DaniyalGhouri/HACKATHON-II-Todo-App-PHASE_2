---
id: 0010
title: Optimize Agent for Tool Call Accuracy
stage: green
date: 2026-02-08
surface: agent
model: gemini-2.0-flash-thinking-exp
feature: 008-todo-ai-chatbot
branch: 008-todo-ai-chatbot
user: unknown
command: /sp.implement
labels: ["optimization", "agent-context", "tool-precision"]
links:
  spec: specs/008-todo-ai-chatbot/spec.md
  plan: specs/008-todo-ai-chatbot/plan.md
  tasks: specs/008-todo-ai-chatbot/tasks.md
files:
 - backend/src/agents/todo_agent.py
 - backend/src/api/chat.py
tests:
 - none
---

## Prompt

System: Please continue. (Context: Refining implementation after fixing import bug).

## Response snapshot

Optimized the AI Agent by injecting the current `user_id` into its system instructions. This ensures the agent can accurately provide the required `user_id` parameter to MCP tool calls in a stateless environment.

## Outcome

- ✅ Impact: Improved reliability of tool calls by providing explicit user context to the Gemini model.
- 🧪 Tests: none
- 📁 Files: backend/src/agents/todo_agent.py, backend/src/api/chat.py
- 🔁 Next prompts: none
- 🧠 Reflection: In a stateless system, passing critical identifiers like `user_id` through the agent's instructions is a reliable way to ensure correct tool parameterization.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): none
