# PharmaAssist AI
<img width="2816" height="509" alt="pharmaAssist-logo" src="https://github.com/user-attachments/assets/05ef2477-0cd4-4cf3-a05a-f434758ce532" />

> **EY Techathon 6.0 Submission** - B2B Pharmaceutical Insights Platform

## 🧬 Overview

PharmaAssist AI is an enterprise-grade pharmaceutical intelligence platform that leverages a multi-agent AI system to provide comprehensive drug analysis. The platform combines advanced RAG (Retrieval-Augmented Generation) capabilities with specialized AI agents to deliver insights across clinical trials, market dynamics, regulatory landscapes, and competitive intelligence.

## ✨ Key Features

### Multi-Agent Analysis Pipeline
- **Molecule Agent** - Compound structure and mechanism analysis
- **Clinical Agent** - Clinical trial data aggregation and insights
- **Market Agent** - Market size, share, and competitive landscape
- **Regulatory Agent** - FDA/EMA approval status and compliance
- **Safety Agent** - Adverse events and safety profile analysis
- **Synthesizer Agent** - Cross-domain insight synthesis

### Real-time Streaming
- Server-Sent Events (SSE) for live analysis progress
- Agent step-by-step visibility
- Streaming chat responses

### Interactive Results Dashboard
- Multi-tab visualization (Overview, Clinical, Market, Safety, Patents)
- Evidence graph with source mapping
- Exportable reports (PDF, JSON, Excel)

### AI-Powered Chat
- Context-aware Q&A about analysis results
- Source citations and references
- Suggested follow-up questions

## 🛠️ Tech Stack

### Frontend
- **Next.js 16** with App Router
- **React 19** with TypeScript
- **Tailwind CSS v4** for styling
- **Zustand** for state management
- **React Flow** for evidence visualization
- **Lucide React** for icons

### Backend
- **FastAPI** with async support
- **LangChain** for AI orchestration
- **OpenAI GPT-4** for analysis
- **ChromaDB** for vector storage
- **SQLite/PostgreSQL** for data persistence
- **SSE** for real-time streaming

## 📁 Project Structure

```
pharmaAsistAI EY Techathon/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   ├── data/            # Mock data for development
│   │   ├── services/        # API client services
│   │   ├── store/           # Zustand state management
│   │   └── types/           # TypeScript definitions
│   ├── .env.local           # Frontend environment variables
│   └── package.json
│
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── agents/          # AI agent implementations
│   │   ├── api/             # API route handlers
│   │   ├── models/          # Pydantic data models
│   │   ├── services/        # Business logic services
│   │   ├── config.py        # Application configuration
│   │   └── main.py          # FastAPI app entry point
│   ├── .env                 # Backend environment variables
│   ├── requirements.txt     # Python dependencies
│   └── run.py               # Development server script
│
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites
- **Node.js 18+** for frontend
- **Python 3.10+** for backend
- **OpenAI API Key** for AI functionality

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/pharmaassist-ai.git
cd pharmaassist-ai
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the server
python run.py
```

The backend will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit if needed (defaults work for local development)

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Enable Backend Integration

By default, the frontend uses mock data for development. To enable real backend integration:

1. Ensure your OpenAI API key is configured in `backend/.env`
2. Edit `frontend/.env.local`:
   ```
   NEXT_PUBLIC_USE_BACKEND=true
   ```
3. Restart the frontend server

## 📊 Usage Guide

### Running an Analysis

1. Navigate to the **Analyze** page
2. Enter a molecule name (e.g., "Atorvastatin", "Pembrolizumab")
3. Select analysis types (Clinical, Market, Regulatory, Competitive)
4. Click **Start Analysis**
5. Watch the multi-agent pipeline process in real-time
6. Explore results in the interactive dashboard

### Using the Chat Interface

1. After an analysis completes, open the **Chat** panel
2. Ask questions about the analysis results
3. View source citations for answers
4. Use suggested questions for deeper exploration

### Exporting Results

1. Navigate to the **Results** tab
2. Click the **Export** button
3. Choose format: PDF, JSON, or Excel
4. Download the comprehensive report

## 🔌 API Endpoints

### Analysis
- `POST /api/v1/analysis/start` - Start a new analysis
- `GET /api/v1/analysis/{id}` - Get analysis status
- `GET /api/v1/analysis/{id}/stream` - Stream analysis progress (SSE)
- `GET /api/v1/analysis/{id}/results` - Get final results

### Chat
- `POST /api/v1/chat` - Send a chat message
- `GET /api/v1/chat/history` - Get chat history

### Molecules
- `GET /api/v1/molecules` - List molecules
- `GET /api/v1/molecules/{id}` - Get molecule details
- `GET /api/v1/molecules/categories` - Get categories

### Health
- `GET /health` - Health check

## 🧪 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
cd backend
ruff check .

# Frontend linting
cd frontend
npm run lint
```

## 📝 Environment Variables

### Backend (`backend/.env`)
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `CHROMA_PERSIST_DIRECTORY` | Vector DB storage path | No |
| `LLM_MODEL` | OpenAI model to use | No (defaults to gpt-4-turbo) |
| `EMBEDDING_MODEL` | Embedding model | No |

### Frontend (`frontend/.env.local`)
| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | No (defaults to localhost:8000) |
| `NEXT_PUBLIC_USE_BACKEND` | Enable real backend | No (defaults to false) |

## 🏆 EY Techathon 6.0

This project was developed for EY Techathon 6.0, addressing the challenge of providing AI-powered pharmaceutical insights for B2B enterprise clients.

### Problem Statement
Pharmaceutical companies need rapid, comprehensive insights across clinical trials, market dynamics, regulatory requirements, and competitive landscapes to make informed decisions about drug development and commercialization.

### Our Solution
PharmaAssist AI provides a unified platform that:
- Aggregates data from multiple pharmaceutical databases
- Uses specialized AI agents for domain-specific analysis
- Delivers real-time insights through an intuitive interface
- Enables natural language exploration of complex data

## 👥 Team

- **Team Name**: ChaturVeda
- **Members**: [Sreejita Deb](https://github.com/Sreejita67), [Rounak Saha](https://github.com/Rounak36), [Sujal Thakkar](https://github.com/sujal-thakkar), [Rohit Singh](https://github.com/codeboy16)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ for EY Techathon 6.0
