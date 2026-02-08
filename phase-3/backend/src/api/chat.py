from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID
from sqlmodel import Session, select
from ..services.db import get_session
from ..auth.dependencies import get_current_user
from ..models.conversation import Conversation
from ..models.message import Message
from ..agents.todo_agent import get_todo_agent
from agents import Runner
import logging

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID

@router.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user["id"]
    # 1. Conversation Init
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
             conversation = Conversation(user_id=user_id)
             session.add(conversation)
             session.commit()
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
    
    session.refresh(conversation)
    conv_id = conversation.id

    # 2. Persist User Message
    user_msg = Message(conversation_id=conv_id, role="user", content=request.message)
    session.add(user_msg)
    session.commit()

    # 3. Load History for Stateless Context
    history_stmt = select(Message).where(Message.conversation_id == conv_id).order_by(Message.created_at)
    db_messages = session.exec(history_stmt).all()
    
    # Format history + current message for the OpenAI Agents SDK
    formatted_messages = [{"role": m.role, "content": m.content} for m in db_messages]

    # 4. Run Agent using the Runner
    agent = get_todo_agent(user_id=user_id)
    
    try:
        import asyncio
        import litellm
        
        max_retries = 3
        retry_count = 0
        response_text = ""
        
        while retry_count < max_retries:
            try:
                # We use await Runner.run because FastAPI is already running in an event loop
                result = await Runner.run(
                    agent,
                    formatted_messages
                )
                response_text = result.final_output
                break # Success!
            except litellm.RateLimitError as e:
                retry_count += 1
                if retry_count == max_retries:
                    raise e
                logger.warning(f"Rate limit hit, retrying in 2s... ({retry_count}/{max_retries})")
                await asyncio.sleep(2) # Wait for Groq token bucket to refill
        
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        response_text = f"I encountered an error processing your request with the AI agent: {str(e)}"

    # 5. Persist Assistant Response
    asst_msg = Message(conversation_id=conv_id, role="assistant", content=response_text)
    session.add(asst_msg)
    session.commit()

    return ChatResponse(response=response_text, conversation_id=conv_id)
