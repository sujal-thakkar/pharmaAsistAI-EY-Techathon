# PDF Knowledge Base Directory

Place your pharmaceutical research PDFs here for the RAG (Retrieval-Augmented Generation) pipeline.

## How to Add PDFs

1. **Copy PDFs to this folder** (`backend/data/pdfs/`)
2. **Ingest them into the vector database** by calling:
   ```bash
   curl -X POST http://localhost:8000/api/v1/knowledge-base/ingest-all-pdfs
   ```
   Or via Python:
   ```python
   import requests
   requests.post("http://localhost:8000/api/v1/knowledge-base/ingest-all-pdfs")
   ```

## Recommended PDFs

For the PharmaAssist AI demo, consider adding:
- Drug monographs (FDA labels)
- Clinical trial summaries
- Market analysis reports
- Patent documents
- Scientific papers on drug mechanisms

## Supported Formats

- `.pdf` files only
- Text-based PDFs work best (scanned images require OCR)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/knowledge-base/status` | GET | Check KB status |
| `/api/v1/knowledge-base/upload-pdf` | POST | Upload single PDF |
| `/api/v1/knowledge-base/ingest-all-pdfs` | POST | Process all PDFs in this folder |
| `/api/v1/knowledge-base/search` | POST | Search the knowledge base |
