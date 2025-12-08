"""Chat API endpoints - Conversational AI for pharmaceutical queries."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import asyncio
import json
import uuid

router = APIRouter()


# === Request/Response Models ===

class ChatMessage(BaseModel):
    """Chat message model."""
    role: str  # user, assistant, system
    content: str
    sources: Optional[List[dict]] = None
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Request model for chat messages."""
    message: str
    analysis_id: Optional[str] = None  # Optional context from analysis
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat."""
    conversation_id: str
    message: ChatMessage
    suggested_questions: Optional[List[str]] = None


# === In-memory storage ===
conversations_store: dict = {}


# === Endpoints ===

@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    """
    Send a chat message and get AI response.
    Optionally provide analysis_id for context-aware responses.
    """
    # Get or create conversation
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    if conversation_id not in conversations_store:
        conversations_store[conversation_id] = {
            "id": conversation_id,
            "messages": [],
            "analysis_id": request.analysis_id,
            "created_at": datetime.utcnow().isoformat()
        }
    
    conversation = conversations_store[conversation_id]
    
    # Add user message
    user_message = ChatMessage(
        role="user",
        content=request.message,
        timestamp=datetime.utcnow().isoformat()
    )
    conversation["messages"].append(user_message.model_dump())
    
    # Generate AI response
    from app.agents.chat_agent import ChatAgent
    
    chat_agent = ChatAgent()
    response = await chat_agent.respond(
        message=request.message,
        conversation_history=conversation["messages"],
        analysis_id=request.analysis_id
    )
    
    # Add assistant message
    assistant_message = ChatMessage(
        role="assistant",
        content=response["content"],
        sources=response.get("sources"),
        timestamp=datetime.utcnow().isoformat()
    )
    conversation["messages"].append(assistant_message.model_dump())
    
    return ChatResponse(
        conversation_id=conversation_id,
        message=assistant_message,
        suggested_questions=response.get("suggested_questions")
    )


@router.post("/chat/stream")
async def stream_chat_response(request: ChatRequest):
    """
    Stream chat response using Server-Sent Events.
    Provides real-time token-by-token response.
    """
    from app.agents.chat_agent import ChatAgent
    
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    async def generate():
        chat_agent = ChatAgent()
        
        async for chunk in chat_agent.stream_response(
            message=request.message,
            analysis_id=request.analysis_id
        ):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.get("/chat/{conversation_id}/history", response_model=dict)
async def get_conversation_history(conversation_id: str):
    """Get conversation history."""
    if conversation_id not in conversations_store:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations_store[conversation_id]


@router.delete("/chat/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    if conversation_id not in conversations_store:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del conversations_store[conversation_id]
    return {"status": "deleted", "conversation_id": conversation_id}
