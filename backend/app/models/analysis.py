"""Pydantic models for Analysis endpoints."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AnalysisType(str, Enum):
    """Available analysis types."""
    CLINICAL = "clinical"
    MARKET = "market"
    REGULATORY = "regulatory"
    COMPETITIVE = "competitive"
    SAFETY = "safety"


class AnalysisStatus(str, Enum):
    """Analysis status states."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisRequest(BaseModel):
    """Request model for starting analysis."""
    molecule_name: str = Field(..., min_length=1, max_length=200, description="Name of the drug/molecule")
    analysis_types: List[AnalysisType] = Field(
        default=[AnalysisType.CLINICAL, AnalysisType.MARKET, AnalysisType.REGULATORY],
        description="Types of analysis to perform"
    )
    additional_context: Optional[str] = Field(None, max_length=1000, description="Additional context for analysis")


class AgentStep(BaseModel):
    """Model for agent step progress."""
    step_id: str
    name: str
    status: str = "pending"  # pending, running, completed, error
    progress: float = 0
    summary: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class AnalysisProgressEvent(BaseModel):
    """Server-sent event for analysis progress."""
    event_type: str  # step_update, completed, error
    step_id: Optional[str] = None
    progress: Optional[float] = None
    summary: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class ClinicalTrial(BaseModel):
    """Clinical trial information."""
    id: str
    title: str
    phase: str
    status: str
    enrollment: int
    condition: str
    sponsor: str
    start_date: str = Field(alias="startDate")
    estimated_completion: str = Field(alias="estimatedCompletion")
    primary_outcome: str = Field(alias="primaryOutcome")
    locations: int
    
    class Config:
        populate_by_name = True


class Competitor(BaseModel):
    """Competitor information."""
    name: str
    company: str
    category: str
    market_share: float = Field(alias="marketShare")
    revenue: int
    
    class Config:
        populate_by_name = True


class PatentInfo(BaseModel):
    """Patent information."""
    patent_number: str = Field(alias="patentNumber")
    title: str
    filing_date: str = Field(alias="filingDate")
    expiry_date: str = Field(alias="expiryDate")
    status: str
    holder: str
    extension_applied: bool = Field(alias="extensionApplied")
    challenges_filed: int = Field(alias="challengesFiled")
    
    class Config:
        populate_by_name = True


class RegulatoryStatus(BaseModel):
    """Regulatory approval status."""
    fda: str
    ema: str
    approval_date: Optional[str] = Field(None, alias="approvalDate")
    approved_indications: List[str] = Field(default=[], alias="approvedIndications")
    label_warnings: List[str] = Field(default=[], alias="labelWarnings")
    
    class Config:
        populate_by_name = True


class Insight(BaseModel):
    """Analysis insight."""
    id: str
    type: str
    category: str
    title: str
    content: str
    impact: str  # high, medium, low
    confidence: float


class Source(BaseModel):
    """Source citation."""
    id: str
    title: str
    type: str
    publisher: str
    date: str
    url: str
    reliability: float


class MoleculeData(BaseModel):
    """Molecule/drug data."""
    name: str
    formula: Optional[str] = None
    molecular_weight: Optional[float] = Field(None, alias="molecularWeight")
    category: Optional[str] = None
    description: Optional[str] = None
    cas_number: Optional[str] = Field(None, alias="casNumber")
    smiles: Optional[str] = None
    iupac_name: Optional[str] = Field(None, alias="iupacName")
    mechanism_of_action: Optional[str] = Field(None, alias="mechanismOfAction")
    
    class Config:
        populate_by_name = True


class MarketData(BaseModel):
    """Market intelligence data."""
    market_size: int = Field(alias="marketSize")
    growth_rate: float = Field(alias="growthRate")
    market_share: float = Field(alias="marketShare")
    year_over_year_growth: float = Field(alias="yearOverYearGrowth")
    projected_market_2028: int = Field(alias="projectedMarket2028")
    competitors: List[Competitor] = []
    revenue_history: List[Dict[str, Any]] = Field(default=[], alias="revenueHistory")
    
    class Config:
        populate_by_name = True


class AnalysisResult(BaseModel):
    """Complete analysis result."""
    id: str
    molecule_name: str = Field(alias="moleculeName")
    generated_at: str = Field(alias="generatedAt")
    molecule_data: Optional[MoleculeData] = Field(None, alias="moleculeData")
    clinical_trials: List[ClinicalTrial] = Field(default=[], alias="clinicalTrials")
    market_data: Optional[MarketData] = Field(None, alias="marketData")
    regulatory_status: Optional[RegulatoryStatus] = Field(None, alias="regulatoryStatus")
    patent_info: Optional[PatentInfo] = Field(None, alias="patentInfo")
    insights: List[Insight] = []
    summary: str = ""
    sources: List[Source] = []
    
    class Config:
        populate_by_name = True


class AnalysisStatusResponse(BaseModel):
    """Response for analysis status check."""
    id: str
    status: AnalysisStatus
    progress: float = 0
    current_step: Optional[str] = Field(None, alias="currentStep")
    steps: List[AgentStep] = []
    error: Optional[str] = None
    result: Optional[AnalysisResult] = None
    
    class Config:
        populate_by_name = True
