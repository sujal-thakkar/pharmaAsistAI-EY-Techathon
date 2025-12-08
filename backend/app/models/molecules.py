"""Pydantic models for Molecules endpoints."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MoleculeCategory(BaseModel):
    """Molecule category with count."""
    name: str
    count: int
    description: Optional[str] = None


class MoleculeBase(BaseModel):
    """Base molecule model."""
    name: str = Field(..., min_length=1, max_length=200)
    formula: Optional[str] = None
    molecular_weight: Optional[float] = Field(None, alias="molecularWeight")
    category: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        populate_by_name = True


class MoleculeCreate(MoleculeBase):
    """Model for creating a molecule."""
    cas_number: Optional[str] = Field(None, alias="casNumber")
    smiles: Optional[str] = None
    iupac_name: Optional[str] = Field(None, alias="iupacName")
    mechanism_of_action: Optional[str] = Field(None, alias="mechanismOfAction")
    
    class Config:
        populate_by_name = True


class MoleculeUpdate(BaseModel):
    """Model for updating a molecule."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
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


class Molecule(MoleculeBase):
    """Complete molecule model with all fields."""
    id: str
    cas_number: Optional[str] = Field(None, alias="casNumber")
    smiles: Optional[str] = None
    iupac_name: Optional[str] = Field(None, alias="iupacName")
    mechanism_of_action: Optional[str] = Field(None, alias="mechanismOfAction")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    analysis_count: int = Field(0, alias="analysisCount")
    
    class Config:
        populate_by_name = True
        from_attributes = True


class MoleculeList(BaseModel):
    """Paginated list of molecules."""
    items: List[Molecule]
    total: int
    page: int
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    
    class Config:
        populate_by_name = True


class MoleculeSearchResult(BaseModel):
    """Search result for molecules."""
    id: str
    name: str
    category: Optional[str] = None
    formula: Optional[str] = None
    relevance_score: float = Field(alias="relevanceScore")
    
    class Config:
        populate_by_name = True
