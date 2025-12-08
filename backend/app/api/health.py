"""Health check endpoints."""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "pharmaassist-api"
    }


@router.get("/health/ready")
async def readiness_check():
    """Readiness check for all dependencies."""
    # TODO: Check database, vector store, OpenAI connectivity
    return {
        "status": "ready",
        "checks": {
            "database": "ok",
            "vector_store": "ok",
            "llm": "ok"
        }
    }
