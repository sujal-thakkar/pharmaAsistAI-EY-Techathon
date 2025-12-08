"""Analysis API endpoints - Core pharmaceutical research functionality."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import asyncio
import json
import uuid

router = APIRouter()


# === Request/Response Models ===

class AnalysisRequest(BaseModel):
    """Request model for starting a new analysis."""
    molecule_name: str
    analysis_types: List[str]  # market, clinical, regulatory, competitive
    additional_context: Optional[str] = None


class AgentStep(BaseModel):
    """Model for agent progress steps."""
    id: str
    name: str
    description: str
    status: str  # pending, in-progress, completed, error
    progress: float
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    result_summary: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Response model for analysis results."""
    id: str
    molecule_name: str
    status: str
    created_at: str
    completed_at: Optional[str] = None
    insights: Optional[List[dict]] = None
    market_data: Optional[dict] = None
    clinical_trials: Optional[List[dict]] = None
    regulatory_status: Optional[dict] = None
    patent_info: Optional[dict] = None
    sources: Optional[List[dict]] = None


# === In-memory storage (replace with database in production) ===
analyses_store: dict = {}


# === Endpoints ===

@router.post("/analysis/start", response_model=dict)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Start a new pharmaceutical analysis.
    Returns analysis ID immediately, processing happens in background.
    """
    analysis_id = str(uuid.uuid4())
    
    # Initialize analysis record
    analyses_store[analysis_id] = {
        "id": analysis_id,
        "molecule_name": request.molecule_name,
        "analysis_types": request.analysis_types,
        "status": "processing",
        "created_at": datetime.utcnow().isoformat(),
        "steps": [],
        "current_step": 0,
        "progress": 0
    }
    
    # Start background processing
    background_tasks.add_task(run_analysis_pipeline, analysis_id, request)
    
    return {
        "analysis_id": analysis_id,
        "status": "started",
        "message": f"Analysis started for {request.molecule_name}"
    }


@router.get("/analysis/{analysis_id}/stream")
async def stream_analysis_progress(analysis_id: str):
    """
    Stream analysis progress using Server-Sent Events (SSE).
    Frontend can subscribe to this for real-time updates.
    """
    if analysis_id not in analyses_store:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    async def event_generator():
        while True:
            analysis = analyses_store.get(analysis_id)
            if not analysis:
                break
            
            # Send current state
            yield f"data: {json.dumps(analysis)}\n\n"
            
            # Check if completed
            if analysis["status"] in ["completed", "error"]:
                break
            
            await asyncio.sleep(0.5)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


@router.get("/analysis/{analysis_id}", response_model=dict)
async def get_analysis(analysis_id: str):
    """Get analysis status and results."""
    if analysis_id not in analyses_store:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analyses_store[analysis_id]


@router.get("/analysis/{analysis_id}/results", response_model=dict)
async def get_analysis_results(analysis_id: str):
    """Get complete analysis results."""
    if analysis_id not in analyses_store:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis = analyses_store[analysis_id]
    
    if analysis["status"] != "completed":
        raise HTTPException(
            status_code=400, 
            detail=f"Analysis not completed. Current status: {analysis['status']}"
        )
    
    return analysis.get("results", {})


@router.get("/analyses", response_model=List[dict])
async def list_analyses(limit: int = 20, offset: int = 0):
    """List all analyses with pagination."""
    all_analyses = list(analyses_store.values())
    # Sort by created_at descending
    all_analyses.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return all_analyses[offset:offset + limit]


# === Background Processing ===

async def run_analysis_pipeline(analysis_id: str, request: AnalysisRequest):
    """
    Main analysis pipeline that orchestrates multi-agent research.
    This runs in the background while streaming updates to the client.
    """
    from app.agents.orchestrator import AgentOrchestrator
    
    try:
        orchestrator = AgentOrchestrator()
        
        # Define agent steps
        steps = [
            {"id": "parse", "name": "Query Parser", "description": "Understanding your research query..."},
            {"id": "molecule", "name": "Molecule Analyzer", "description": "Fetching molecular structure and properties..."},
            {"id": "clinical", "name": "Clinical Trials Agent", "description": "Searching clinical trial databases..."},
            {"id": "market", "name": "Market Intelligence", "description": "Analyzing market data and trends..."},
            {"id": "regulatory", "name": "Regulatory Scanner", "description": "Checking FDA/EMA approval status..."},
            {"id": "patent", "name": "Patent Analyzer", "description": "Reviewing intellectual property..."},
            {"id": "synthesizer", "name": "Insight Synthesizer", "description": "Generating comprehensive insights..."},
        ]
        
        analyses_store[analysis_id]["steps"] = steps
        
        # Run orchestrator
        results = await orchestrator.run(
            molecule_name=request.molecule_name,
            analysis_types=request.analysis_types,
            additional_context=request.additional_context,
            progress_callback=lambda step_id, progress, summary: update_step_progress(
                analysis_id, step_id, progress, summary
            )
        )
        
        # Update final state
        analyses_store[analysis_id].update({
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "progress": 100,
            "results": results
        })
        
    except Exception as e:
        analyses_store[analysis_id].update({
            "status": "error",
            "error": str(e),
            "completed_at": datetime.utcnow().isoformat()
        })


def update_step_progress(analysis_id: str, step_id: str, progress: float, summary: Optional[str] = None):
    """Update progress for a specific agent step."""
    if analysis_id not in analyses_store:
        return
    
    analysis = analyses_store[analysis_id]
    steps = analysis.get("steps", [])
    
    for i, step in enumerate(steps):
        if step["id"] == step_id:
            step["status"] = "completed" if progress >= 100 else "in-progress"
            step["progress"] = progress
            if summary:
                step["result_summary"] = summary
            if progress >= 100:
                step["end_time"] = datetime.utcnow().isoformat()
            elif step.get("start_time") is None:
                step["start_time"] = datetime.utcnow().isoformat()
            
            # Update overall progress
            completed_steps = sum(1 for s in steps if s.get("status") == "completed")
            analysis["progress"] = (completed_steps / len(steps)) * 100
            analysis["current_step"] = i
            break
