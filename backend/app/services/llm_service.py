"""
LLM Service - Unified interface for Gemini and OpenAI.

Supports Google Gemini (default) and OpenAI as LLM providers.
"""
from typing import Optional, List, Dict, Any, AsyncGenerator
import logging
import asyncio

from app.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Unified LLM service supporting Gemini and OpenAI."""
    
    def __init__(self):
        self.provider = settings.llm_provider
        self.model = settings.llm_model
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client."""
        if self.provider == "gemini":
            self._initialize_gemini()
        else:
            self._initialize_openai()
    
    def _initialize_gemini(self):
        """Initialize Google Gemini client."""
        try:
            import google.generativeai as genai
            
            if settings.gemini_api_key and settings.gemini_api_key != "your-gemini-api-key-here":
                genai.configure(api_key=settings.gemini_api_key)
                self.client = genai.GenerativeModel(self.model)
                logger.info(f"✅ Gemini client initialized with model: {self.model}")
            else:
                logger.warning("⚠️ Gemini API key not configured - using mock responses")
        except ImportError:
            logger.error("❌ google-generativeai not installed. Run: pip install google-generativeai")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
    
    def _initialize_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import AsyncOpenAI
            
            if settings.openai_api_key and settings.openai_api_key != "your-openai-api-key-here":
                self.client = AsyncOpenAI(api_key=settings.openai_api_key)
                logger.info(f"✅ OpenAI client initialized with model: {self.model}")
            else:
                logger.warning("⚠️ OpenAI API key not configured - using mock responses")
        except ImportError:
            logger.error("❌ openai not installed. Run: pip install openai")
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI: {e}")
    
    @property
    def is_available(self) -> bool:
        """Check if LLM client is available."""
        return self.client is not None
    
    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate a completion using the configured LLM provider.
        
        Falls back to mock response if API is not available.
        """
        if not self.is_available:
            return self._mock_completion(prompt)
        
        try:
            if self.provider == "gemini":
                return await self._gemini_completion(prompt, system_prompt, temperature, max_tokens)
            else:
                return await self._openai_completion(prompt, system_prompt, temperature, max_tokens)
        except Exception as e:
            logger.error(f"LLM API error: {str(e)}")
            return self._mock_completion(prompt)
    
    async def _gemini_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate completion using Gemini."""
        import google.generativeai as genai
        
        # Combine system prompt with user prompt for Gemini
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        # Gemini's generate_content is synchronous, run in executor
        loop = asyncio.get_event_loop()
        
        def generate():
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            response = self.client.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            return response.text
        
        result = await loop.run_in_executor(None, generate)
        return result or ""
    
    async def _openai_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate completion using OpenAI."""
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
    
    async def stream_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """
        Stream a completion using the configured LLM provider.
        
        Falls back to mock streaming if API is not available.
        """
        if not self.is_available:
            async for chunk in self._mock_stream_completion(prompt):
                yield chunk
            return
        
        try:
            if self.provider == "gemini":
                async for chunk in self._gemini_stream(prompt, system_prompt, temperature, max_tokens):
                    yield chunk
            else:
                async for chunk in self._openai_stream(prompt, system_prompt, temperature, max_tokens):
                    yield chunk
        except Exception as e:
            logger.error(f"LLM streaming error: {str(e)}")
            async for chunk in self._mock_stream_completion(prompt):
                yield chunk
    
    async def _gemini_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Stream completion using Gemini."""
        import google.generativeai as genai
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        # Gemini streaming is synchronous, need to handle differently
        loop = asyncio.get_event_loop()
        
        def stream_generate():
            response = self.client.generate_content(
                full_prompt,
                generation_config=generation_config,
                stream=True
            )
            chunks = []
            for chunk in response:
                if chunk.text:
                    chunks.append(chunk.text)
            return chunks
        
        chunks = await loop.run_in_executor(None, stream_generate)
        for chunk in chunks:
            yield chunk
    
    async def _openai_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """Stream completion using OpenAI."""
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
    
    def _mock_completion(self, prompt: str) -> str:
        """Generate mock completion for development/testing."""
        prompt_lower = prompt.lower()
        
        if "clinical" in prompt_lower or "trial" in prompt_lower:
            return """## Clinical Trial Analysis

Based on the available data, here are the key clinical findings:

1. **Phase 3 Trials**: Multiple successful Phase 3 trials have demonstrated efficacy
2. **Primary Endpoints**: Met primary endpoints with statistical significance (p < 0.001)
3. **Patient Population**: Studied in over 10,000 patients across diverse demographics
4. **Safety Profile**: Generally well-tolerated with manageable side effects
5. **Duration**: Long-term studies show sustained efficacy over 52 weeks

The clinical evidence strongly supports the therapeutic use of this molecule for the indicated conditions."""

        elif "market" in prompt_lower or "revenue" in prompt_lower:
            return """## Market Analysis

Key market insights for this pharmaceutical compound:

1. **Market Size**: The global market is valued at approximately $45.2 billion
2. **Growth Rate**: CAGR of 8.5% projected through 2028
3. **Market Share**: Currently holds 23% of the therapeutic segment
4. **Competitive Position**: Ranked #2 among branded therapies
5. **Pricing**: Premium pricing strategy with strong payer coverage

The market dynamics indicate continued growth potential with expanding indications."""

        elif "regulatory" in prompt_lower or "fda" in prompt_lower:
            return """## Regulatory Status

Current regulatory landscape:

1. **FDA Status**: Approved - New Drug Application (NDA) approved
2. **EMA Status**: Approved - Marketing Authorization granted
3. **Approved Indications**: 3 therapeutic indications across regions
4. **Post-Marketing Requirements**: Ongoing safety monitoring studies
5. **Patent Protection**: Core patents valid until 2032

The molecule has achieved broad regulatory acceptance across major markets."""

        elif "patent" in prompt_lower or "ip" in prompt_lower:
            return """## Patent & IP Analysis

Intellectual property portfolio assessment:

1. **Core Patents**: 5 active patents protecting the compound
2. **Formulation Patents**: 3 additional formulation patents
3. **Method of Use**: 2 patents covering novel therapeutic uses
4. **Expiry Timeline**: Primary patent expires 2032, extensions possible
5. **Generic Risk**: Limited generic entry expected before 2034

Strong IP protection provides extended market exclusivity."""

        else:
            return """## Pharmaceutical Analysis Summary

Comprehensive analysis completed for the requested molecule:

1. **Mechanism of Action**: Well-characterized with clear therapeutic rationale
2. **Efficacy Profile**: Strong clinical evidence supporting use
3. **Safety Profile**: Acceptable benefit-risk balance
4. **Market Position**: Competitive positioning in therapeutic area
5. **Future Outlook**: Positive trajectory with pipeline expansion

This molecule demonstrates strong potential for continued success in its therapeutic category."""

    async def _mock_stream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        """Generate mock streaming completion."""
        response = self._mock_completion(prompt)
        words = response.split()
        
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            await asyncio.sleep(0.02)  # Simulate streaming delay


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


# Create singleton for direct import
llm_service = get_llm_service()
