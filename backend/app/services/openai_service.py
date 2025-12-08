"""OpenAI Service - Handles interactions with OpenAI API."""
from typing import Optional, List, Dict, Any, AsyncGenerator
import logging
from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI API interactions."""
    
    def __init__(self):
        self.client: Optional[AsyncOpenAI] = None
        self.model = settings.llm_model
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client if API key is available."""
        if settings.openai_api_key and settings.openai_api_key != "your-openai-api-key-here":
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            logger.info("✅ OpenAI client initialized")
        else:
            logger.warning("⚠️ OpenAI API key not configured - using mock responses")
    
    @property
    def is_available(self) -> bool:
        """Check if OpenAI client is available."""
        return self.client is not None
    
    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate a completion using OpenAI.
        
        Falls back to mock response if API is not available.
        """
        if not self.is_available:
            return self._mock_completion(prompt)
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return self._mock_completion(prompt)
    
    async def stream_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> AsyncGenerator[str, None]:
        """
        Stream a completion using OpenAI.
        
        Falls back to mock streaming if API is not available.
        """
        if not self.is_available:
            async for chunk in self._mock_stream_completion(prompt):
                yield chunk
            return
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"OpenAI streaming error: {str(e)}")
            async for chunk in self._mock_stream_completion(prompt):
                yield chunk
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for texts using OpenAI.
        
        Falls back to mock embeddings if API is not available.
        """
        if not self.is_available:
            return self._mock_embeddings(texts)
        
        try:
            response = await self.client.embeddings.create(
                model=settings.embedding_model,
                input=texts
            )
            
            return [item.embedding for item in response.data]
            
        except Exception as e:
            logger.error(f"OpenAI embeddings error: {str(e)}")
            return self._mock_embeddings(texts)
    
    def _mock_completion(self, prompt: str) -> str:
        """Generate mock completion for testing."""
        return f"""Based on your query about pharmaceutical research:

This is a mock response as the OpenAI API is not configured. In production, this would provide:

1. **Detailed Analysis** - Comprehensive insights based on the query
2. **Source Citations** - References to clinical trials, FDA databases, and market reports
3. **Recommendations** - Strategic guidance based on the analysis

To enable real AI responses, please configure your OpenAI API key in the environment variables.

Query received: {prompt[:100]}..."""

    async def _mock_stream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        """Generate mock streaming completion for testing."""
        import asyncio
        
        response = self._mock_completion(prompt)
        words = response.split()
        
        for word in words:
            yield word + " "
            await asyncio.sleep(0.03)
    
    def _mock_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate mock embeddings for testing."""
        import random
        
        # Generate random 1536-dimensional embeddings (OpenAI's embedding size)
        return [[random.uniform(-1, 1) for _ in range(1536)] for _ in texts]


# Singleton instance
openai_service = OpenAIService()
