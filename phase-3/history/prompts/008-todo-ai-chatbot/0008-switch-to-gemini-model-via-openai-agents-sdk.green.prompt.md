---
id: 0008
title: Switch to Gemini Model via OpenAI Agents SDK
stage: green
date: 2026-02-08
surface: agent
model: gemini-2.0-flash-thinking-exp
feature: 008-todo-ai-chatbot
branch: 008-todo-ai-chatbot
user: unknown
command: /sp.implement
labels: ["gemini", "openai-agents-sdk", "custom-model", "tracing-off"]
links:
  spec: specs/008-todo-ai-chatbot/spec.md
  plan: specs/008-todo-ai-chatbot/plan.md
  tasks: specs/008-todo-ai-chatbot/tasks.md
files:
 - backend/src/agents/todo_agent.py
 - backend/src/api/chat.py
 - backend/.env.example
tests:
 - none
---

## Prompt

yes the second one , from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI ... like this and get GEMINI_API_KEY from env and use best free model from gemini also dont forget to turn off tracing

## Response snapshot

Reconfigured the Todo AI Assistant to use Google's `gemini-2.0-flash` model via the `openai-agents` SDK's `OpenAIChatCompletionsModel`. Integrated `AsyncOpenAI` for the connection and explicitly disabled tracing in the `Agent` definition.

## Outcome

- ✅ Impact: Successfully migrated the AI logic from a simulated heuristic to a live Gemini-powered agent, enhancing natural language understanding while maintaining stateless persistence.
- 🧪 Tests: none
- 📁 Files: backend/src/agents/todo_agent.py, backend/src/api/chat.py, backend/.env.example
- 🔁 Next prompts: none
- 🧠 Reflection: Using the `OpenAIChatCompletionsModel` bridge allows for easy provider switching while keeping the core agent logic intact.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): none
