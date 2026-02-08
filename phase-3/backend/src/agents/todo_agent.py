from agents import Agent, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from ..mcp.tools import add_task, list_tasks, update_task, complete_task, delete_task

load_dotenv()

# Disable tracing to avoid OPENAI_API_KEY requirement for trace exports
set_tracing_disabled(True)

# 1. Configure the Groq Client (OpenAI-compatible)
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# 2. Define the Groq Model
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=external_client
)

# 3. Agent System Prompt

BASE_SYSTEM_PROMPT = """
You are a high-performance 2026-grade Todo AI Assistant.
You help users manage their tasks with precision and intelligence.

Available Capabilities:
- add_task: Create new tasks. You can set title, description, due_date, and priority (low, medium, high).
- list_tasks: Retrieve user tasks. You can see completion status, priority, and due dates.
- update_task: Modify existing tasks, including changing priority or due dates.
- complete_task: Mark a task as finished.
- delete_task: Permanently remove a task.

Guidelines:
1. ALWAYS use the provided tools.
2. When listing tasks, summarize the counts of pending and completed tasks to show oversight.
3. Pay attention to due dates and priorities. If a task is high priority or overdue, mention it.
4. If a user doesn't specify priority, default to 'medium'.
5. Always be professional, concise, and helpful.
"""



# 4. Create the Agent

def get_todo_agent(user_id: str) -> Agent:

    # Inject user_id into instructions so the agent knows it for tool calls

    instructions = f"{BASE_SYSTEM_PROMPT}\n\nCRITICAL: The current user_id is '{user_id}'. You MUST pass this value as the 'user_id' parameter for every tool call."

    

    return Agent(
        name="TodoAssistant",
        instructions=instructions,
        model=llm_model,
        tools=[add_task, list_tasks, update_task, complete_task, delete_task]
    )
