"""PDF Ingestion Service - Process pharmaceutical PDFs for RAG pipeline."""
import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import uuid
import hashlib

from app.config import settings

logger = logging.getLogger(__name__)


class PDFService:
    """Service for processing PDF documents for the knowledge base."""
    
    def __init__(self):
        self.pdf_directory = Path(settings.pdf_directory)
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Ensure PDF directory exists."""
        self.pdf_directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 PDF directory: {self.pdf_directory}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Generate hash for file to track processed files."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            buf = f.read(65536)  # Read in chunks
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    
    def list_pdfs(self) -> List[Dict[str, Any]]:
        """List all PDFs in the directory."""
        pdfs = []
        for file_path in self.pdf_directory.glob("*.pdf"):
            try:
                stat = file_path.stat()
                pdfs.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size_bytes": stat.st_size,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "modified": stat.st_mtime
                })
            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")
        return pdfs
    
    def load_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load a PDF file and extract text content.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            List of page documents with text and metadata
        """
        try:
            from langchain_community.document_loaders import PyPDFLoader
            
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            documents = []
            for i, page in enumerate(pages):
                documents.append({
                    "content": page.page_content,
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "page": i + 1,
                        "total_pages": len(pages),
                        **page.metadata
                    }
                })
            
            logger.info(f"📄 Loaded {len(pages)} pages from {file_path}")
            return documents
            
        except ImportError:
            logger.error("PyPDFLoader not available. Install with: pip install pypdf")
            return self._fallback_pdf_load(file_path)
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
            return []
    
    def _fallback_pdf_load(self, file_path: str) -> List[Dict[str, Any]]:
        """Fallback PDF loading using PyPDF2 or pypdf directly."""
        try:
            import pypdf
            
            documents = []
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        documents.append({
                            "content": text,
                            "metadata": {
                                "source": os.path.basename(file_path),
                                "page": i + 1,
                                "total_pages": len(reader.pages)
                            }
                        })
            
            logger.info(f"📄 [Fallback] Loaded {len(documents)} pages from {file_path}")
            return documents
            
        except ImportError:
            logger.error("pypdf not available. Install with: pip install pypdf")
            return []
        except Exception as e:
            logger.error(f"Fallback PDF load failed: {e}")
            return []
    
    def chunk_documents(
        self,
        documents: List[Dict[str, Any]],
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Split documents into smaller chunks for better retrieval.
        
        Args:
            documents: List of documents to chunk
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of chunked documents
        """
        chunk_size = chunk_size or self.chunk_size
        chunk_overlap = chunk_overlap or self.chunk_overlap
        
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
            
            chunked_docs = []
            for doc in documents:
                chunks = splitter.split_text(doc["content"])
                for i, chunk in enumerate(chunks):
                    if chunk.strip():
                        chunked_docs.append({
                            "content": chunk,
                            "metadata": {
                                **doc["metadata"],
                                "chunk_index": i,
                                "total_chunks": len(chunks)
                            }
                        })
            
            logger.info(f"✂️ Created {len(chunked_docs)} chunks from {len(documents)} documents")
            return chunked_docs
            
        except ImportError:
            logger.warning("LangChain not available, using simple chunking")
            return self._simple_chunk(documents, chunk_size, chunk_overlap)
    
    def _simple_chunk(
        self,
        documents: List[Dict[str, Any]],
        chunk_size: int,
        chunk_overlap: int
    ) -> List[Dict[str, Any]]:
        """Simple chunking fallback without LangChain."""
        chunked_docs = []
        
        for doc in documents:
            text = doc["content"]
            start = 0
            chunk_index = 0
            
            while start < len(text):
                end = start + chunk_size
                chunk = text[start:end]
                
                if chunk.strip():
                    chunked_docs.append({
                        "content": chunk,
                        "metadata": {
                            **doc["metadata"],
                            "chunk_index": chunk_index
                        }
                    })
                
                start = end - chunk_overlap
                chunk_index += 1
        
        return chunked_docs
    
    def process_all_pdfs(self) -> List[Dict[str, Any]]:
        """
        Process all PDFs in the directory.
        
        Returns:
            List of all chunked documents
        """
        all_chunks = []
        pdf_files = self.list_pdfs()
        
        logger.info(f"📚 Processing {len(pdf_files)} PDF files...")
        
        for pdf_info in pdf_files:
            try:
                documents = self.load_pdf(pdf_info["path"])
                chunks = self.chunk_documents(documents)
                all_chunks.extend(chunks)
                logger.info(f"✅ Processed: {pdf_info['name']} -> {len(chunks)} chunks")
            except Exception as e:
                logger.error(f"❌ Error processing {pdf_info['name']}: {e}")
        
        logger.info(f"📊 Total chunks created: {len(all_chunks)}")
        return all_chunks
    
    def save_uploaded_pdf(self, file_content: bytes, filename: str) -> str:
        """
        Save an uploaded PDF file.
        
        Args:
            file_content: PDF file bytes
            filename: Original filename
            
        Returns:
            Path to saved file
        """
        # Sanitize filename
        safe_filename = "".join(c for c in filename if c.isalnum() or c in "._-")
        if not safe_filename.endswith(".pdf"):
            safe_filename += ".pdf"
        
        file_path = self.pdf_directory / safe_filename
        
        # Handle duplicates
        counter = 1
        while file_path.exists():
            name = safe_filename.rsplit(".", 1)[0]
            file_path = self.pdf_directory / f"{name}_{counter}.pdf"
            counter += 1
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        logger.info(f"💾 Saved uploaded PDF: {file_path}")
        return str(file_path)


# Singleton instance
pdf_service = PDFService()
