// PharmaAssist AI - Type Definitions

// Analysis Type for search selection
export type AnalysisType = 'market' | 'clinical' | 'regulatory' | 'competitive';

export interface MoleculeData {
  id: string;
  name: string;
  genericName?: string;
  category: string;
  phase?: string;
  status?: 'active' | 'discontinued' | 'in-development';
  molecularWeight: number;
  formula: string;
  mechanism: string;
  indications: string[];
}

export interface ClinicalTrial {
  id: string;
  title: string;
  phase: 'Phase 1' | 'Phase 2' | 'Phase 3' | 'Phase 4';
  status: 'Active' | 'Recruiting' | 'Completed' | 'Terminated' | 'Suspended';
  startDate: string;
  endDate?: string;
  enrollment: number;
  sponsor: string;
  primaryEndpoint?: string;
  results?: string;
  nctNumber?: string;
  locations?: string[];
}

export interface MarketData {
  marketSize: number;
  marketShare: number;
  growthRate: number;
  competitors: Competitor[];
  pricePerUnit?: number;
  targetMarket?: string;
  launchDate?: string;
  peakSalesEstimate?: number;
}

export interface Competitor {
  name: string;
  company: string;
  marketShare: number;
  revenue?: number;
}

export interface PatentInfo {
  id: string;
  title: string;
  filingDate: string;
  expiryDate: string;
  status: 'Active' | 'Expired' | 'Pending';
  patentNumber: string;
  holder: string;
}

export interface RegulatoryStatus {
  fda: 'Approved' | 'Pending' | 'Rejected' | 'Under Review';
  ema: 'Approved' | 'Pending' | 'Rejected' | 'Under Review';
  approvalDate?: string;
  approvedIndications: string[];
  warnings?: string[];
  blackBoxWarning?: boolean;
}

// Agent System Types
export interface AgentStep {
  id: string;
  name: string;
  description: string;
  status: 'pending' | 'in-progress' | 'completed' | 'error';
  progress: number;
  startTime?: Date;
  endTime?: Date;
  result?: string;
  icon: string;
}

export interface AnalysisRequest {
  moleculeName: string;
  analysisTypes: AnalysisType[];
  additionalContext?: string;
}

export interface AnalysisResult {
  id: string;
  moleculeData: MoleculeData;
  marketData: MarketData;
  clinicalTrials: ClinicalTrial[];
  patentInfo: PatentInfo;
  regulatoryStatus: RegulatoryStatus;
  insights: Insight[];
  sources: Source[];
  generatedAt: string;
}

export interface Insight {
  id: string;
  type: 'positive' | 'negative' | 'neutral' | 'opportunity';
  title: string;
  description: string;
  confidence: number;
  source: string;
}

export interface Source {
  id: string;
  name: string;
  type: 'clinical-trial' | 'publication' | 'fda-document' | 'patent' | 'market-report' | 'news';
  url: string;
  relevanceScore?: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  sources?: Source[];
}

// Graph/Flow Types for Evidence Visualization
export interface EvidenceNode {
  id: string;
  type: string;
  data: { label: string; description?: string; confidence?: number };
  position: { x: number; y: number };
}

export interface EvidenceEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  animated?: boolean;
  type?: 'supports' | 'contradicts' | 'related';
}

// Dashboard Metrics
export interface DashboardMetrics {
  clinicalTrialsActive: number;
  clinicalTrialsTotal: number;
  marketPotential: string;
  competitorCount: number;
  patentExpiry: string;
  riskScore: number;
  opportunityScore: number;
  timeToMarket: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
