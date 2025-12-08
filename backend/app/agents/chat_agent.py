"""Chat Agent - Handles conversational AI for pharmaceutical queries."""
from typing import Dict, Any, Optional, List, AsyncGenerator
import asyncio

from app.config import settings


class ChatAgent:
    """Agent for handling chat-based interactions about pharmaceutical research."""
    
    def __init__(self):
        self.context_window = []
        self.max_context = 10
    
    async def respond(
        self,
        message: str,
        conversation_history: Optional[List[Dict]] = None,
        analysis_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a response to user message.
        
        In production, this would use LangChain + OpenAI with RAG.
        Currently returns intelligent mock responses.
        """
        message_lower = message.lower()
        
        # Simulate processing delay
        await asyncio.sleep(0.5)
        
        # Determine response based on message content
        response_content = self._get_contextual_response(message_lower)
        
        # Generate follow-up questions
        suggested_questions = self._get_suggested_questions(message_lower)
        
        # Mock sources
        sources = [
            {
                "title": "FDA Drug Database",
                "url": "https://www.fda.gov/drugs",
                "type": "regulatory"
            },
            {
                "title": "ClinicalTrials.gov",
                "url": "https://clinicaltrials.gov",
                "type": "clinical"
            }
        ]
        
        return {
            "content": response_content,
            "sources": sources,
            "suggested_questions": suggested_questions
        }
    
    async def stream_response(
        self,
        message: str,
        analysis_id: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream response token by token.
        
        In production, this would stream from OpenAI API.
        """
        response = self._get_contextual_response(message.lower())
        
        # Simulate streaming by yielding words
        words = response.split()
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            await asyncio.sleep(0.05)  # Simulate token delay
    
    def _get_contextual_response(self, message: str) -> str:
        """Generate contextual response based on message content."""
        
        if any(word in message for word in ["clinical", "trial", "study"]):
            return """Based on my analysis of the clinical trial landscape:

**Active Clinical Trials:**
- Multiple Phase 3 trials are currently recruiting patients
- Key endpoints focus on efficacy and long-term safety outcomes
- Average trial duration is approximately 52 weeks

**Key Findings:**
1. Primary endpoints have shown statistically significant improvements
2. Safety profile is consistent with the drug class
3. Sub-group analyses show benefit across demographics

Would you like me to dive deeper into any specific trial or phase?"""

        elif any(word in message for word in ["market", "revenue", "sales", "growth"]):
            return """Here's the market intelligence summary:

**Market Overview:**
- Current market size: Approximately $15-20 billion globally
- Projected CAGR: 15-25% through 2028
- Market share: Leading position in the therapeutic category

**Revenue Trends:**
- Strong year-over-year growth driven by expanded indications
- Increasing adoption in primary care setting
- Geographic expansion contributing to growth

**Competitive Position:**
- First-mover advantage in key markets
- Premium pricing maintained due to clinical differentiation

Would you like more details on market trends or competitive dynamics?"""

        elif any(word in message for word in ["patent", "ip", "exclusivity"]):
            return """Regarding intellectual property and exclusivity:

**Patent Status:**
- Primary patent protection extends through 2030+
- Multiple patents covering formulation and delivery
- Patent challenges have been successfully defended

**Exclusivity Periods:**
- New chemical entity exclusivity: Active
- Orphan drug designation for specific indications
- Pediatric exclusivity extension obtained

**Risk Assessment:**
- Generic/biosimilar entry expected post-patent expiry
- Lifecycle management strategies in place

Do you want more information about specific patents or the competitive threat from biosimilars?"""

        elif any(word in message for word in ["safety", "side effect", "adverse"]):
            return """Here's the safety profile analysis:

**Common Adverse Events:**
- Most events are mild to moderate in severity
- Gastrointestinal effects are most frequently reported
- Events typically resolve with continued treatment

**Serious Adverse Events:**
- Black box warnings address specific risks
- Risk mitigation strategies recommended in labeling
- Post-marketing surveillance ongoing

**Comparative Safety:**
- Favorable safety profile vs. alternatives in class
- Long-term safety data supports continued use

Would you like details on specific adverse events or safety monitoring recommendations?"""

        elif any(word in message for word in ["competitor", "competition", "alternative"]):
            return """Competitive landscape analysis:

**Key Competitors:**
1. **Direct Competitors:** Several drugs in the same class
2. **Indirect Competitors:** Alternative therapeutic approaches
3. **Emerging Threats:** New mechanisms in development

**Differentiation Factors:**
- Superior efficacy on key endpoints
- Convenient dosing schedule
- Established safety profile

**Pipeline Threats:**
- Next-generation therapies in Phase 2/3
- Combination therapies under investigation

Should I elaborate on any specific competitor or competitive dynamic?"""

        elif any(word in message for word in ["fda", "ema", "approval", "regulatory"]):
            return """Regulatory status summary:

**FDA Status:**
- Currently approved for multiple indications
- Recent label expansions granted
- REMS program in place for safety monitoring

**EMA Status:**
- Marketing authorization granted
- Indicated for similar conditions as FDA approval
- Pharmacovigilance commitments ongoing

**Recent Regulatory Actions:**
- Supplemental approvals for new indications
- Label updates reflecting new safety data
- Post-marketing requirements progressing on schedule

Would you like information about pending regulatory submissions or specific approval details?"""

        else:
            return """I'm your pharmaceutical research assistant. I can help you with:

📊 **Market Intelligence** - Market size, growth trends, competitive landscape
🔬 **Clinical Trials** - Active studies, phases, endpoints, results
📋 **Regulatory Status** - FDA/EMA approvals, label information
🔒 **Patent Analysis** - IP protection, exclusivity periods
⚠️ **Safety Profile** - Adverse events, warnings, risk mitigation

What aspect of the drug would you like me to analyze?"""

    def _get_suggested_questions(self, message: str) -> List[str]:
        """Generate relevant follow-up questions."""
        
        if any(word in message for word in ["clinical", "trial"]):
            return [
                "What are the primary endpoints in Phase 3 trials?",
                "How does efficacy compare to competitors?",
                "What is the safety profile from trials?"
            ]
        elif any(word in message for word in ["market", "revenue"]):
            return [
                "Who are the main competitors?",
                "What is the projected market growth?",
                "What are the key market risks?"
            ]
        elif any(word in message for word in ["patent", "ip"]):
            return [
                "When do key patents expire?",
                "Are there any patent challenges?",
                "What is the biosimilar pipeline?"
            ]
        else:
            return [
                "What is the current market size?",
                "How many clinical trials are active?",
                "What is the FDA approval status?"
            ]
