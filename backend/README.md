# PharmaAssist AI Backend

FastAPI backend for the PharmaAssist AI pharmaceutical intelligence platform.

## Quick Start

1. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key (optional for mock mode)
   ```

4. **Run the server:**
   ```bash
   python run.py
   
   # Or using uvicorn directly:
   uvicorn app.main:app --reload --port 8000
   ```

5. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## API Endpoints

### Health
- `GET /health` - Health check

### Analysis
- `POST /api/v1/analysis/start` - Start new analysis
- `GET /api/v1/analysis/{id}/stream` - Stream analysis progress (SSE)
- `GET /api/v1/analysis/{id}` - Get analysis status
- `GET /api/v1/analysis/{id}/results` - Get complete results
- `GET /api/v1/analyses` - List all analyses

### Chat
- `POST /api/v1/chat` - Send chat message
- `GET /api/v1/chat/stream` - Stream chat response (SSE)
- `GET /api/v1/chat/history/{conversation_id}` - Get chat history
- `POST /api/v1/chat/feedback` - Submit feedback

### Molecules
- `GET /api/v1/molecules` - List molecules
- `GET /api/v1/molecules/{id}` - Get molecule details
- `GET /api/v1/molecules/categories` - Get molecule categories

## Architecture

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration settings
│   ├── api/                  # API route handlers
│   │   ├── health.py
│   │   ├── analysis.py
│   │   ├── chat.py
│   │   └── molecules.py
│   ├── agents/              # AI research agents
│   │   ├── base.py          # Base agent class
│   │   ├── orchestrator.py  # Agent coordinator
│   │   ├── molecule_agent.py
│   │   ├── clinical_agent.py
│   │   ├── market_agent.py
│   │   ├── regulatory_agent.py
│   │   ├── synthesizer_agent.py
│   │   └── chat_agent.py
│   ├── models/              # Pydantic models
│   │   ├── analysis.py
│   │   ├── chat.py
│   │   └── molecules.py
│   └── services/            # Business logic services
│       ├── openai_service.py
│       ├── rag_service.py
│       ├── analysis_service.py
│       └── chat_service.py
├── requirements.txt
├── .env.example
├── run.py
└── README.md
```

## Features

- **Multi-Agent Pipeline**: Orchestrated agents for comprehensive drug research
- **Real-time Streaming**: SSE-based progress updates
- **RAG System**: ChromaDB-powered knowledge retrieval
- **OpenAI Integration**: GPT-4 powered insights (with mock fallback)
- **Mock Mode**: Full functionality without API keys for testing

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | None (uses mock) |
| `DATABASE_URL` | SQLite database path | `sqlite:///./pharma_assist.db` |
| `CHROMADB_PATH` | ChromaDB storage path | `./chromadb_data` |
| `DEBUG` | Enable debug mode | `true` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `EMBEDDING_MODEL` | Embedding model | `text-embedding-3-small` |
