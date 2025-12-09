# PharmaAssist AI - Design & Architecture (Round 2)

## 📱 User Experience Flow

The following diagram illustrates the core user journey through the PharmaAssist AI platform, from initial molecule search to deep insight generation.

```mermaid
graph TD
    A[Landing Page] -->|Search Molecule| B[Analysis Loading]
    B -->|Streaming Data| C[Molecule Result Dashboard]
    C --> D[Clinical Trials Analysis]
    C --> E[Market Intelligence]
    C --> F[Regulatory Status]
    C --> G[Safety Profile]
    C --> H[AI Chat Assistant]
    
    H -->|Query| I[Contextual Answers]
    D -->|Details| J[Trial Specifics]
```

## 🖥️ Interface Walkthrough

### 1. Global Research Dashboard
The central command center for drug intelligence across all searches.
![Global Dashboard](./docs/images/dashboard-page-ss.png)
> **Design Philosophy**: Information density without clutter. Uses a bento-grid layout for high-level metrics (FDA status, Market Cap) while allowing deep dives via tabs.

### 2. Search & Analysis Initiation
The entry point where users define their research target or browse history.
![Home Page](./docs/images/home-page-ss.png)

#### History View
Quick access to past analyses with status indicators.
![History Page](./docs/images/history-page-ss.png)

### 3. Multi-Agent Orchestration
Visualizing the AI "thinking" process builds user trust.
![Loading Screen](./docs/images/loading-page-ss.png)
> **UX features**: Individual agent cards lighting up as they activate (Brain, Flask, Chart, etc.) providing transparency into the RAG pipeline.

### 4. Molecule Result Page (Deep Dive)
The granular analysis for a specific target molecule.
![Result Page Overview](./docs/images/result-page-ss.png)

#### Market Intelligence
Detailed market size, CAGR, and competitor landscape.
![Market Tab](./docs/images/market-tab-ss.png)

#### Clinical Trials
Comprehensive breakdown of trial phases and status.
![Clinical Tab](./docs/images/clinical-tab-ss.png)

### 5. Evidence Visualization
Graph-based view of connected entities and data sources.
![Evidence Graph](./docs/images/evidence-graph-ss.png)
> **Insight**: Visualizes relationships between molecules, trials, and patents.

### 6. Conversational Intelligence
Turning static data into dynamic answers.
![Chat Interface](./docs/images/chatbot-ss.png)

## 🔮 Future Roadmap (Concept Wireframes)
*Proposed features for the next development phase.*

### Comparative Analysis View
*Side-by-side comparison of multiple drugs.*

### Automated PDF Report Generation
*Preview of the exportable executive summary.*
