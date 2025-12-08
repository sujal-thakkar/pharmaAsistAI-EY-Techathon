"""Pydantic models for Chat endpoints."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str  # user, assistant
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Request model for chat."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    analysis_id: Optional[str] = Field(None, description="Associated analysis ID for context")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for history")


class ChatSource(BaseModel):
    """Source reference in chat response."""
    title: str
    url: str
    type: str  # regulatory, clinical, market, etc.


class ChatResponse(BaseModel):
    """Response model for chat."""
    content: str
    sources: List[ChatSource] = []
    suggested_questions: List[str] = []
    conversation_id: Optional[str] = None


class ChatStreamChunk(BaseModel):
    """Streaming chunk for chat response."""
    type: str  # content, source, suggestion, done
    content: Optional[str] = None
    sources: Optional[List[ChatSource]] = None
    suggested_questions: Optional[List[str]] = None


class ConversationHistory(BaseModel):
    """Conversation history."""
    conversation_id: str
    messages: List[ChatMessage]
    analysis_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ChatFeedback(BaseModel):
    """Feedback on chat response."""
    message_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    feedback_text: Optional[str] = Field(None, max_length=500)
