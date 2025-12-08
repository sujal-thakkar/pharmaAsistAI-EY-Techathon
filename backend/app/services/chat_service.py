"""Chat Service - Manages chat interactions and history."""
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime
import uuid
import logging

from app.agents.chat_agent import ChatAgent
from app.services.rag_service import rag_service
from app.services.llm_service import get_llm_service
from app.models.chat import ChatMessage, ChatRequest, ChatResponse

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat interactions."""
    
    def __init__(self):
        self.chat_agent = ChatAgent()
        self.conversations: Dict[str, List[ChatMessage]] = {}
        self.feedback: Dict[str, Dict[str, Any]] = {}
    
    async def process_message(
        self,
        request: ChatRequest
    ) -> ChatResponse:
        """
        Process a chat message and generate response.
        
        Args:
            request: Chat request with message and optional context
            
        Returns:
            Chat response with content and metadata
        """
        conversation_id = request.conversation_id or f"conv-{uuid.uuid4().hex[:8]}"
        
        logger.info(f"💬 Processing message in conversation {conversation_id}")
        
        # Get conversation history
        history = self.conversations.get(conversation_id, [])
        
        # Add user message to history
        user_message = ChatMessage(
            role="user",
            content=request.message,
            timestamp=datetime.utcnow()
        )
        history.append(user_message)
        
        # Get relevant context from RAG if available
        rag_context = await rag_service.get_context_for_query(request.message)
        
        # Get LLM service
        llm = get_llm_service()
        
        # Generate response
        if llm.is_available:
            # Use LLM with RAG context
            system_prompt = self._build_system_prompt(rag_context, request.analysis_id)
            response_content = await llm.generate_completion(
                prompt=request.message,
                system_prompt=system_prompt
            )
            sources = self._extract_sources(rag_context)
            suggested = self._generate_suggestions(request.message)
        else:
            # Use mock chat agent
            result = await self.chat_agent.respond(
                message=request.message,
                conversation_history=[m.model_dump() for m in history],
                analysis_id=request.analysis_id
            )
            response_content = result["content"]
            sources = result.get("sources", [])
            suggested = result.get("suggested_questions", [])
        
        # Add assistant message to history
        assistant_message = ChatMessage(
            role="assistant",
            content=response_content,
            timestamp=datetime.utcnow()
        )
        history.append(assistant_message)
        
        # Save conversation
        self.conversations[conversation_id] = history
        
        return ChatResponse(
            content=response_content,
            sources=sources,
            suggested_questions=suggested,
            conversation_id=conversation_id
        )
    
    async def stream_response(
        self,
        request: ChatRequest
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat response token by token.
        
        Args:
            request: Chat request
            
        Yields:
            Response tokens
        """
        conversation_id = request.conversation_id or f"conv-{uuid.uuid4().hex[:8]}"
        
        # Get RAG context
        rag_context = await rag_service.get_context_for_query(request.message)
        
        # Get LLM service
        llm = get_llm_service()
        
        if llm.is_available:
            system_prompt = self._build_system_prompt(rag_context, request.analysis_id)
            async for token in llm.stream_completion(
                prompt=request.message,
                system_prompt=system_prompt
            ):
                yield token
        else:
            async for token in self.chat_agent.stream_response(
                message=request.message,
                analysis_id=request.analysis_id
            ):
                yield token
    
    def get_conversation_history(
        self,
        conversation_id: str
    ) -> List[ChatMessage]:
        """Get conversation history."""
        return self.conversations.get(conversation_id, [])
    
    def add_feedback(
        self,
        message_id: str,
        rating: int,
        feedback_text: Optional[str] = None
    ) -> bool:
        """Add feedback for a message."""
        self.feedback[message_id] = {
            "rating": rating,
            "feedback_text": feedback_text,
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.info(f"📝 Feedback added for message {message_id}: {rating}/5")
        return True
    
    def _build_system_prompt(
        self,
        rag_context: str,
        analysis_id: Optional[str] = None
    ) -> str:
        """Build system prompt with context."""
        base_prompt = """You are PharmaAssist AI, an expert pharmaceutical research assistant. 
You provide accurate, detailed information about drugs, clinical trials, market data, and regulatory status.

Guidelines:
- Provide evidence-based information
- Cite sources when possible
- Acknowledge limitations in knowledge
- Recommend consulting healthcare professionals for medical decisions
- Be concise but comprehensive"""

        if rag_context:
            base_prompt += f"""

Relevant context from knowledge base:
{rag_context}

Use this context to inform your response, but don't mention that you're using a knowledge base."""

        if analysis_id:
            base_prompt += f"""

The user has an active analysis (ID: {analysis_id}). Reference insights from this analysis when relevant."""

        return base_prompt
    
    def _extract_sources(self, rag_context: str) -> List[Dict[str, str]]:
        """Extract source references from RAG context."""
        # In production, this would parse actual source metadata
        return [
            {"title": "Knowledge Base", "url": "#", "type": "internal"},
            {"title": "FDA Database", "url": "https://www.fda.gov", "type": "regulatory"}
        ]
    
    def _generate_suggestions(self, message: str) -> List[str]:
        """Generate follow-up question suggestions."""
        message_lower = message.lower()
        
        if "clinical" in message_lower or "trial" in message_lower:
            return [
                "What are the primary endpoints?",
                "How does safety compare to alternatives?",
                "What is the patient enrollment status?"
            ]
        elif "market" in message_lower or "revenue" in message_lower:
            return [
                "Who are the main competitors?",
                "What's the growth forecast?",
                "What are the pricing trends?"
            ]
        else:
            return [
                "What is the mechanism of action?",
                "What are the approved indications?",
                "What is the market size?"
            ]


# Singleton instance
chat_service = ChatService()
