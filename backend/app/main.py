"""FastAPI Application Entry Point for PharmaAssist AI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
from pathlib import Path

from app.config import settings
from app.api import analysis, chat, molecules, health, knowledge_base

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown events."""
    # Startup
    logger.info("🚀 Starting PharmaAssist AI Backend...")
    logger.info(f"📊 Debug mode: {settings.debug}")
    logger.info(f"🔗 CORS origins: {settings.cors_origins_list}")
    
    # Initialize services here (database, vector store, etc.)
    yield
    
    # Shutdown
    logger.info("👋 Shutting down PharmaAssist AI Backend...")


# Create FastAPI application
app = FastAPI(
    title="PharmaAssist AI API",
    description="Multi-Agent Pharmaceutical Intelligence Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(molecules.router, prefix="/api/v1", tags=["Molecules"])
app.include_router(knowledge_base.router, prefix="/api/v1/knowledge-base", tags=["Knowledge Base"])

# Mount static files for PDF access
pdf_directory = Path(settings.pdf_directory)
if pdf_directory.exists():
    app.mount("/static/pdfs", StaticFiles(directory=str(pdf_directory)), name="pdfs")
    logger.info(f"📁 Mounted PDF directory at /static/pdfs")
else:
    logger.warning(f"⚠️ PDF directory not found: {pdf_directory}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "PharmaAssist AI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
