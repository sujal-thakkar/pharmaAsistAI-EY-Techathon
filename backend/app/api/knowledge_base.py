"""Knowledge Base API - Manage RAG knowledge base and PDF ingestion."""
from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel
import logging

from app.services.rag_service import rag_service
from app.services.pdf_service import pdf_service

logger = logging.getLogger(__name__)
router = APIRouter()


class SearchQuery(BaseModel):
    """Search query model."""
    query: str
    n_results: int = 5
    category_filter: Optional[str] = None


class DocumentInput(BaseModel):
    """Input for adding documents to knowledge base."""
    documents: List[str]
    category: str = "custom"


class SearchResult(BaseModel):
    """Search result model."""
    content: str
    relevance_score: float
    category: str
    source: str


@router.get("/status")
async def get_knowledge_base_status():
    """Get the current status of the knowledge base."""
    stats = rag_service.get_collection_stats()
    pdfs = pdf_service.list_pdfs()
    
    return {
        "status": "operational" if stats.get("status") == "available" else "unavailable",
        "vectorStore": stats,
        "pdfDirectory": {
            "count": len(pdfs),
            "files": pdfs[:10]  # Show first 10
        }
    }


@router.post("/search")
async def search_knowledge_base(query: SearchQuery):
    """Search the knowledge base for relevant documents."""
    results = await rag_service.search(
        query=query.query,
        n_results=query.n_results,
        category_filter=query.category_filter
    )
    
    return {
        "query": query.query,
        "results": results,
        "count": len(results)
    }


@router.post("/search/molecule")
async def search_molecule_info(molecule_name: str):
    """Search for comprehensive information about a specific molecule."""
    info = await rag_service.search_for_molecule(molecule_name)
    return info


@router.post("/documents")
async def add_documents(input: DocumentInput):
    """Add documents directly to the knowledge base."""
    if not input.documents:
        raise HTTPException(status_code=400, detail="No documents provided")
    
    metadatas = [
        {"source": "api_upload", "category": input.category, "type": "custom"}
        for _ in input.documents
    ]
    
    success = await rag_service.add_documents(input.documents, metadatas)
    
    if success:
        return {
            "status": "success",
            "message": f"Added {len(input.documents)} documents to knowledge base",
            "newCount": rag_service.get_collection_stats().get("count", 0)
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to add documents")


@router.post("/upload-pdf")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload and process a PDF file into the knowledge base."""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Save the file
    content = await file.read()
    file_path = pdf_service.save_uploaded_pdf(content, file.filename)
    
    # Process in background
    async def process_pdf():
        try:
            documents = pdf_service.load_pdf(file_path)
            chunks = pdf_service.chunk_documents(documents)
            await rag_service.ingest_pdf_chunks(chunks)
            logger.info(f"✅ Processed PDF: {file.filename} -> {len(chunks)} chunks")
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
    
    background_tasks.add_task(process_pdf)
    
    return {
        "status": "processing",
        "message": f"PDF '{file.filename}' uploaded and queued for processing",
        "filePath": file_path
    }


@router.post("/ingest-all-pdfs")
async def ingest_all_pdfs(background_tasks: BackgroundTasks):
    """Process all PDFs in the data directory."""
    pdf_list = pdf_service.list_pdfs()
    
    if not pdf_list:
        return {
            "status": "no_files",
            "message": "No PDF files found in the data directory"
        }
    
    async def process_all():
        try:
            chunks = pdf_service.process_all_pdfs()
            if chunks:
                await rag_service.ingest_pdf_chunks(chunks)
                logger.info(f"✅ Ingested {len(chunks)} chunks from {len(pdf_list)} PDFs")
        except Exception as e:
            logger.error(f"Error ingesting PDFs: {e}")
    
    background_tasks.add_task(process_all)
    
    return {
        "status": "processing",
        "message": f"Ingesting {len(pdf_list)} PDF files in background",
        "files": [p["name"] for p in pdf_list]
    }


@router.get("/pdfs")
async def list_pdfs():
    """List all PDFs in the data directory."""
    pdfs = pdf_service.list_pdfs()
    return {
        "count": len(pdfs),
        "files": pdfs
    }


@router.post("/rebuild")
async def rebuild_knowledge_base():
    """Clear and rebuild the knowledge base from scratch."""
    success = await rag_service.clear_and_rebuild()
    
    if success:
        return {
            "status": "success",
            "message": "Knowledge base rebuilt successfully",
            "newCount": rag_service.get_collection_stats().get("count", 0)
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to rebuild knowledge base")


@router.get("/context")
async def get_context_for_query(query: str, n_results: int = 5):
    """Get formatted context for a query (useful for debugging RAG)."""
    context = await rag_service.get_context_for_query(query, n_results)
    
    return {
        "query": query,
        "context": context,
        "contextLength": len(context)
    }
