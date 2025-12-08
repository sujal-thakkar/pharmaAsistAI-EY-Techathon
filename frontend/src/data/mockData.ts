// Mock Data for PharmaAssist AI - Based on real pharmaceutical data patterns
import { 
  MoleculeData, 
  AgentStep, 
  AnalysisResult, 
  Insight, 
  Source, 
  DashboardMetrics,
  ClinicalTrial,
  MarketData,
  PatentInfo,
  RegulatoryStatus,
  EvidenceNode,
  EvidenceEdge
} from '@/types';

// Simple molecule database for search/display
export const MOLECULE_DATABASE: MoleculeData[] = [
  {
    id: 'mol-001',
    name: 'Aspirin',
    category: 'NSAID',
    molecularWeight: 180.16,
    formula: 'C9H8O4',
    mechanism: 'Inhibits cyclooxygenase (COX) enzymes, reducing prostaglandin synthesis',
    indications: ['Pain', 'Fever', 'Inflammation', 'Cardiovascular Protection']
  },
  {
    id: 'mol-002',
    name: 'Metformin',
    category: 'Biguanide',
    molecularWeight: 129.16,
    formula: 'C4H11N5',
    mechanism: 'Decreases hepatic glucose production and increases insulin sensitivity',
    indications: ['Type 2 Diabetes', 'PCOS', 'Pre-diabetes']
  },
  {
    id: 'mol-003',
    name: 'Omeprazole',
    category: 'Proton Pump Inhibitor',
    molecularWeight: 345.42,
    formula: 'C17H19N3O3S',
    mechanism: 'Irreversibly inhibits the H+/K+ ATPase proton pump in gastric parietal cells',
    indications: ['GERD', 'Peptic Ulcer', 'Zollinger-Ellison Syndrome']
  }
];

// Sample Clinical Trials
const SAMPLE_CLINICAL_TRIALS: ClinicalTrial[] = [
  {
    id: 'nct-001',
    title: 'Efficacy Study in Pain Management',
    phase: 'Phase 3',
    status: 'Active',
    startDate: '2023-01-15',
    enrollment: 1500,
    sponsor: 'PharmaCorp Inc.',
    primaryEndpoint: 'Pain reduction from baseline'
  },
  {
    id: 'nct-002',
    title: 'Cardiovascular Outcomes Trial',
    phase: 'Phase 4',
    status: 'Recruiting',
    startDate: '2023-06-01',
    enrollment: 3000,
    sponsor: 'Global Research Labs',
    primaryEndpoint: 'Major adverse cardiovascular events'
  },
  {
    id: 'nct-003',
    title: 'Pediatric Formulation Study',
    phase: 'Phase 2',
    status: 'Completed',
    startDate: '2022-03-10',
    endDate: '2023-09-15',
    enrollment: 250,
    sponsor: 'PharmaCorp Inc.',
    primaryEndpoint: 'Pharmacokinetic profile in pediatric patients'
  },
  {
    id: 'nct-004',
    title: 'Long-term Safety Study',
    phase: 'Phase 4',
    status: 'Active',
    startDate: '2021-09-01',
    enrollment: 5000,
    sponsor: 'MedResearch Alliance',
    primaryEndpoint: 'Incidence of adverse events over 5 years'
  }
];

// Sample Market Data
const SAMPLE_MARKET_DATA: MarketData = {
  marketSize: 12500000000,
  marketShare: 23.5,
  growthRate: 8.2,
  competitors: [
    { name: 'Ibuprofen', company: 'Generic', marketShare: 28 },
    { name: 'Naproxen', company: 'Bayer', marketShare: 15 },
    { name: 'Acetaminophen', company: 'J&J', marketShare: 22 },
    { name: 'Diclofenac', company: 'Novartis', marketShare: 12 }
  ]
};

// Sample Patent Info
const SAMPLE_PATENT_INFO: PatentInfo = {
  id: 'pat-001',
  title: 'Extended Release Formulation',
  filingDate: '2015-03-20',
  expiryDate: '2035-03-20',
  status: 'Active',
  patentNumber: 'US10234567B2',
  holder: 'PharmaCorp Inc.'
};

// Sample Regulatory Status
const SAMPLE_REGULATORY_STATUS: RegulatoryStatus = {
  fda: 'Approved',
  ema: 'Approved',
  approvalDate: '1899-03-06',
  approvedIndications: ['Pain', 'Fever', 'Anti-inflammatory', 'Antiplatelet']
};

// Sample Insights
const SAMPLE_INSIGHTS: Insight[] = [
  {
    id: 'ins-001',
    type: 'positive',
    title: 'Strong Market Growth Expected',
    description: 'Market analysts project 8.2% CAGR over the next 5 years driven by aging population and cardiovascular prevention guidelines.',
    confidence: 87,
    source: 'Market Research Report 2024'
  },
  {
    id: 'ins-002',
    type: 'neutral',
    title: 'Generic Competition Intensifying',
    description: 'Multiple generic manufacturers entering the market may impact pricing strategies.',
    confidence: 92,
    source: 'FDA Orange Book Analysis'
  },
  {
    id: 'ins-003',
    type: 'positive',
    title: 'New Indication Potential',
    description: 'Recent studies suggest potential efficacy in cancer prevention, opening new market opportunities.',
    confidence: 65,
    source: 'Clinical Research Database'
  },
  {
    id: 'ins-004',
    type: 'negative',
    title: 'Regulatory Scrutiny Increasing',
    description: 'FDA has issued new guidance on cardiovascular risk labeling requirements.',
    confidence: 78,
    source: 'FDA Guidance Documents'
  }
];

// Sample Sources
const SAMPLE_SOURCES: Source[] = [
  { id: 'src-001', name: 'ClinicalTrials.gov', type: 'clinical-trial', url: 'https://clinicaltrials.gov' },
  { id: 'src-002', name: 'FDA Drug Database', type: 'fda-document', url: 'https://www.fda.gov' },
  { id: 'src-003', name: 'PubMed Research', type: 'publication', url: 'https://pubmed.ncbi.nlm.nih.gov' },
  { id: 'src-004', name: 'USPTO Patent Search', type: 'patent', url: 'https://www.uspto.gov' },
  { id: 'src-005', name: 'IQVIA Market Report', type: 'market-report', url: 'https://www.iqvia.com' }
];

// Sample Analysis Result
export const SAMPLE_ANALYSIS_RESULT: AnalysisResult = {
  id: 'analysis-001',
  moleculeData: MOLECULE_DATABASE[0],
  marketData: SAMPLE_MARKET_DATA,
  clinicalTrials: SAMPLE_CLINICAL_TRIALS,
  patentInfo: SAMPLE_PATENT_INFO,
  regulatoryStatus: SAMPLE_REGULATORY_STATUS,
  insights: SAMPLE_INSIGHTS,
  sources: SAMPLE_SOURCES,
  generatedAt: new Date().toISOString()
};

// Agent Steps for Analysis Process
export const AGENT_STEPS: AgentStep[] = [
  {
    id: 'step-1',
    name: 'Master Agent',
    description: 'Creating analysis plan and coordinating specialized agents...',
    status: 'pending',
    progress: 0,
    icon: 'brain'
  },
  {
    id: 'step-2',
    name: 'Clinical Trials Agent',
    description: 'Scanning ClinicalTrials.gov and extracting trial data...',
    status: 'pending',
    progress: 0,
    icon: 'flask'
  },
  {
    id: 'step-3',
    name: 'Market Intelligence Agent',
    description: 'Analyzing market trends, competitor landscape, and revenue projections...',
    status: 'pending',
    progress: 0,
    icon: 'chart'
  },
  {
    id: 'step-4',
    name: 'Patent Analysis Agent',
    description: 'Reviewing patent filings, expirations, and IP landscape...',
    status: 'pending',
    progress: 0,
    icon: 'file'
  },
  {
    id: 'step-5',
    name: 'Regulatory Intelligence Agent',
    description: 'Checking FDA/EMA approvals, warnings, and regulatory pathway...',
    status: 'pending',
    progress: 0,
    icon: 'shield'
  },
  {
    id: 'step-6',
    name: 'Safety Profile Agent',
    description: 'Analyzing adverse events, contraindications, and risk factors...',
    status: 'pending',
    progress: 0,
    icon: 'alert'
  },
  {
    id: 'step-7',
    name: 'Synthesis Agent',
    description: 'Compiling insights and generating comprehensive report...',
    status: 'pending',
    progress: 0,
    icon: 'sparkles'
  }
];

// Dashboard Metrics
export const SAMPLE_METRICS: DashboardMetrics = {
  clinicalTrialsActive: 3,
  clinicalTrialsTotal: 47,
  marketPotential: '$35B',
  competitorCount: 8,
  patentExpiry: 'Sep 2026',
  riskScore: 35,
  opportunityScore: 85,
  timeToMarket: 'Marketed'
};

// Analysis Intent Options
export const ANALYSIS_INTENTS = [
  { value: 'comprehensive', label: 'Comprehensive Analysis', description: 'Full analysis covering all aspects' },
  { value: 'competitive-landscape', label: 'Competitive Landscape', description: 'Market position and competitor analysis' },
  { value: 'clinical-development', label: 'Clinical Development', description: 'Trial data and development pipeline' },
  { value: 'market-opportunity', label: 'Market Opportunity', description: 'Revenue potential and market sizing' },
  { value: 'regulatory-pathway', label: 'Regulatory Pathway', description: 'Approval status and regulatory strategy' },
  { value: 'safety-analysis', label: 'Safety Analysis', description: 'Adverse events and risk profile' },
  { value: 'patent-review', label: 'Patent Review', description: 'IP landscape and patent expiry' }
];

// Evidence Graph Data
export const SAMPLE_EVIDENCE_NODES: EvidenceNode[] = [
  { id: 'node-1', type: 'molecule', data: { label: 'Aspirin' }, position: { x: 250, y: 50 } },
  { id: 'node-2', type: 'trial', data: { label: 'Phase 3 Pain Trial' }, position: { x: 100, y: 150 } },
  { id: 'node-3', type: 'patent', data: { label: 'US10234567B2' }, position: { x: 400, y: 150 } },
  { id: 'node-4', type: 'market', data: { label: 'NSAID Market' }, position: { x: 250, y: 250 } },
  { id: 'node-5', type: 'regulatory', data: { label: 'FDA Approved' }, position: { x: 100, y: 350 } },
  { id: 'node-6', type: 'insight', data: { label: 'Market Growth' }, position: { x: 400, y: 350 } }
];

export const SAMPLE_EVIDENCE_EDGES: EvidenceEdge[] = [
  { id: 'edge-1', source: 'node-1', target: 'node-2', label: 'tested in' },
  { id: 'edge-2', source: 'node-1', target: 'node-3', label: 'protected by' },
  { id: 'edge-3', source: 'node-1', target: 'node-4', label: 'competes in' },
  { id: 'edge-4', source: 'node-2', target: 'node-5', label: 'approved by' },
  { id: 'edge-5', source: 'node-4', target: 'node-6', label: 'indicates' }
];
