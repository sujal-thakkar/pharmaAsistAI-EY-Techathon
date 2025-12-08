"""Analysis Service - Manages analysis jobs and results."""
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import asyncio
import uuid
import logging

from app.agents.orchestrator import AgentOrchestrator
from app.models.analysis import AnalysisRequest, AnalysisStatus

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for managing pharmaceutical analysis jobs."""
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.active_analyses: Dict[str, Dict[str, Any]] = {}
        self.completed_analyses: Dict[str, Dict[str, Any]] = {}
    
    async def start_analysis(
        self,
        request: AnalysisRequest,
        progress_callback: Optional[Callable[[str, float, Optional[str]], None]] = None
    ) -> Dict[str, Any]:
        """
        Start a new analysis job.
        
        Args:
            request: Analysis request parameters
            progress_callback: Callback for progress updates (step_id, progress, summary)
            
        Returns:
            Analysis results
        """
        analysis_id = f"analysis-{uuid.uuid4().hex[:8]}"
        
        logger.info(f"🔬 Starting analysis {analysis_id} for {request.molecule_name}")
        
        # Track analysis
        self.active_analyses[analysis_id] = {
            "id": analysis_id,
            "status": AnalysisStatus.PROCESSING,
            "request": request.model_dump(),
            "started_at": datetime.utcnow().isoformat(),
            "progress": 0,
            "current_step": None
        }
        
        try:
            # Run the orchestrator
            results = await self.orchestrator.run(
                molecule_name=request.molecule_name,
                analysis_types=[t.value for t in request.analysis_types],
                additional_context=request.additional_context,
                progress_callback=progress_callback
            )
            
            # Add analysis ID to results
            results["id"] = analysis_id
            
            # Move to completed
            self.completed_analyses[analysis_id] = {
                **self.active_analyses.pop(analysis_id),
                "status": AnalysisStatus.COMPLETED,
                "completed_at": datetime.utcnow().isoformat(),
                "results": results
            }
            
            logger.info(f"✅ Analysis {analysis_id} completed successfully")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Analysis {analysis_id} failed: {str(e)}")
            
            # Mark as failed
            if analysis_id in self.active_analyses:
                self.active_analyses[analysis_id].update({
                    "status": AnalysisStatus.FAILED,
                    "error": str(e),
                    "failed_at": datetime.utcnow().isoformat()
                })
            
            raise
    
    def get_analysis_status(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of an analysis job."""
        if analysis_id in self.active_analyses:
            return self.active_analyses[analysis_id]
        
        if analysis_id in self.completed_analyses:
            return self.completed_analyses[analysis_id]
        
        return None
    
    def get_analysis_result(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get the results of a completed analysis."""
        if analysis_id in self.completed_analyses:
            return self.completed_analyses[analysis_id].get("results")
        return None
    
    def update_progress(
        self,
        analysis_id: str,
        step_id: str,
        progress: float,
        summary: Optional[str] = None
    ):
        """Update progress for an active analysis."""
        if analysis_id in self.active_analyses:
            self.active_analyses[analysis_id].update({
                "current_step": step_id,
                "progress": progress,
                "last_summary": summary
            })
    
    def list_recent_analyses(self, limit: int = 10) -> list:
        """List recent analyses."""
        all_analyses = [
            *self.active_analyses.values(),
            *self.completed_analyses.values()
        ]
        
        # Sort by started_at descending
        all_analyses.sort(
            key=lambda x: x.get("started_at", ""),
            reverse=True
        )
        
        return all_analyses[:limit]


# Singleton instance
analysis_service = AnalysisService()
