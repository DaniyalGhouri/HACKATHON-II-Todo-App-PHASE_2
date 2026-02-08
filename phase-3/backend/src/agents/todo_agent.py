from agents import Agent, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import os
from dotenv import load_dotenv
from ..mcp.tools import add_task, list_tasks, update_task, complete_task, delete_task

load_dotenv()

set_tracing_disabled(True)

llm_model = LitellmModel(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

BASE_SYSTEM_PROMPT = """
You are a high-performance 2026-grade Todo AI Assistant.

Available Tools:
- add_task: (title, description, due_date, priority)
- list_tasks: (status_filter: 'all'|'completed'|'pending')
- update_task: (task_id: int, title, description, due_date, priority)
- complete_task: (task_id: int)
- delete_task: (task_id: int)

CRITICAL RULES:
1. TOOL FORMAT: You MUST use exactly: <function=tool_name>{"arg": "val"}</function>
2. NO COMMAS: Do NOT put a comma between the tool name and the JSON bracket. (Correct: <function=list_tasks>{"status_filter":"all"}...)
3. NO NULL IDs: Never send 'task_id': null. If you don't know the ID, call list_tasks first to find it.
4. REQUIRED ARGS: Always include 'user_id' and 'status_filter' in list_tasks calls.
5. WORKFLOW: If a user asks to update/delete a task but you haven't listed them yet, call list_tasks first to find the ID.
"""

def get_todo_agent(user_id: str) -> Agent:
    # Inject current date and user_id into instructions
    from datetime import datetime
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    
    instructions = f"{BASE_SYSTEM_PROMPT}\n\nCRITICAL:\n- Today is {current_date}.\n- The current user_id is '{user_id}'. Include 'user_id': '{user_id}' in every tool call JSON."

    return Agent(
        name="TodoAssistant",
        instructions=instructions,
        model=llm_model,
        tools=[add_task, list_tasks, update_task, complete_task, delete_task]
    )