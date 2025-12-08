"""Base Agent class for all specialized pharmaceutical research agents."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all research agents."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
    @abstractmethod
    async def execute(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Execute the agent's task.
        
        Args:
            query: The research query/molecule name
            context: Additional context from previous agents
            progress_callback: Callback function(progress: float, summary: str)
            
        Returns:
            Dictionary containing agent results
        """
        pass
    
    async def run(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """Run the agent with timing and error handling."""
        self.start_time = datetime.utcnow()
        logger.info(f"🚀 Agent '{self.name}' starting for query: {query}")
        
        try:
            if progress_callback:
                progress_callback(0, f"Starting {self.name}...")
            
            result = await self.execute(query, context, progress_callback)
            
            self.end_time = datetime.utcnow()
            duration = (self.end_time - self.start_time).total_seconds()
            
            logger.info(f"✅ Agent '{self.name}' completed in {duration:.2f}s")
            
            if progress_callback:
                progress_callback(100, f"Completed {self.name}")
            
            return {
                "agent": self.name,
                "status": "success",
                "duration_seconds": duration,
                "data": result
            }
            
        except Exception as e:
            self.end_time = datetime.utcnow()
            logger.error(f"❌ Agent '{self.name}' failed: {str(e)}")
            
            if progress_callback:
                progress_callback(100, f"Error in {self.name}: {str(e)}")
            
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e),
                "data": None
            }
