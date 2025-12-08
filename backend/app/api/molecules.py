"""Molecules API endpoints - Drug/molecule database operations."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


# === Models ===

class MoleculeData(BaseModel):
    """Molecule information model."""
    id: str
    name: str
    formula: str
    molecular_weight: float
    category: str
    description: Optional[str] = None
    cas_number: Optional[str] = None
    smiles: Optional[str] = None
    iupac_name: Optional[str] = None


class MoleculeSearchResult(BaseModel):
    """Search result model."""
    molecules: List[MoleculeData]
    total: int
    page: int
    per_page: int


# === Mock Database ===
MOLECULE_DATABASE = [
    {
        "id": "mol-001",
        "name": "Aspirin",
        "formula": "C9H8O4",
        "molecular_weight": 180.16,
        "category": "NSAID",
        "description": "Acetylsalicylic acid - pain reliever and anti-inflammatory",
        "cas_number": "50-78-2",
        "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "iupac_name": "2-Acetoxybenzoic acid"
    },
    {
        "id": "mol-002",
        "name": "Metformin",
        "formula": "C4H11N5",
        "molecular_weight": 129.16,
        "category": "Antidiabetic",
        "description": "First-line medication for type 2 diabetes",
        "cas_number": "657-24-9",
        "smiles": "CN(C)C(=N)NC(=N)N",
        "iupac_name": "3-(diaminomethylidene)-1,1-dimethylguanidine"
    },
    {
        "id": "mol-003",
        "name": "Semaglutide",
        "formula": "C187H291N45O59",
        "molecular_weight": 4113.58,
        "category": "GLP-1 Agonist",
        "description": "Used for diabetes and weight management (Ozempic, Wegovy)",
        "cas_number": "910463-68-2",
        "smiles": None,
        "iupac_name": None
    },
    {
        "id": "mol-004",
        "name": "Pembrolizumab",
        "formula": "C6504H10004N1716O2036S46",
        "molecular_weight": 146300.0,
        "category": "Immunotherapy",
        "description": "Checkpoint inhibitor for cancer treatment (Keytruda)",
        "cas_number": "1374853-91-4",
        "smiles": None,
        "iupac_name": None
    },
    {
        "id": "mol-005",
        "name": "Adalimumab",
        "formula": "C6428H9912N1694O1987S46",
        "molecular_weight": 144190.0,
        "category": "TNF Inhibitor",
        "description": "Monoclonal antibody for autoimmune diseases (Humira)",
        "cas_number": "331731-18-1",
        "smiles": None,
        "iupac_name": None
    },
    {
        "id": "mol-006",
        "name": "Atorvastatin",
        "formula": "C33H35FN2O5",
        "molecular_weight": 558.64,
        "category": "Statin",
        "description": "Cholesterol-lowering medication (Lipitor)",
        "cas_number": "134523-00-5",
        "smiles": "CC(C)C1=C(C(=C(N1CCC(CC(CC(=O)O)O)O)C2=CC=C(C=C2)F)C3=CC=CC=C3)C(=O)NC4=CC=CC=C4",
        "iupac_name": None
    },
    {
        "id": "mol-007",
        "name": "Omeprazole",
        "formula": "C17H19N3O3S",
        "molecular_weight": 345.42,
        "category": "Proton Pump Inhibitor",
        "description": "Treats gastroesophageal reflux disease (GERD)",
        "cas_number": "73590-58-6",
        "smiles": "CC1=CN=C(C(=C1OC)C)CS(=O)C2=NC3=C(N2)C=CC(=C3)OC",
        "iupac_name": None
    },
    {
        "id": "mol-008",
        "name": "Lisinopril",
        "formula": "C21H31N3O5",
        "molecular_weight": 405.49,
        "category": "ACE Inhibitor",
        "description": "Treats high blood pressure and heart failure",
        "cas_number": "83915-83-7",
        "smiles": None,
        "iupac_name": None
    }
]


# === Endpoints ===

@router.get("/molecules", response_model=MoleculeSearchResult)
async def list_molecules(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None
):
    """List molecules with optional filtering."""
    molecules = MOLECULE_DATABASE.copy()
    
    # Filter by category
    if category:
        molecules = [m for m in molecules if m["category"].lower() == category.lower()]
    
    # Search by name
    if search:
        search_lower = search.lower()
        molecules = [
            m for m in molecules 
            if search_lower in m["name"].lower() or 
               (m.get("description") and search_lower in m["description"].lower())
        ]
    
    # Pagination
    total = len(molecules)
    start = (page - 1) * per_page
    end = start + per_page
    
    return MoleculeSearchResult(
        molecules=[MoleculeData(**m) for m in molecules[start:end]],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/molecules/{molecule_id}", response_model=MoleculeData)
async def get_molecule(molecule_id: str):
    """Get molecule by ID."""
    for molecule in MOLECULE_DATABASE:
        if molecule["id"] == molecule_id:
            return MoleculeData(**molecule)
    
    raise HTTPException(status_code=404, detail="Molecule not found")


@router.get("/molecules/search/{query}", response_model=List[MoleculeData])
async def search_molecules(query: str, limit: int = Query(10, ge=1, le=50)):
    """Search molecules by name or description."""
    query_lower = query.lower()
    
    results = [
        MoleculeData(**m) for m in MOLECULE_DATABASE
        if query_lower in m["name"].lower() or
           (m.get("description") and query_lower in m["description"].lower()) or
           (m.get("formula") and query_lower in m["formula"].lower())
    ]
    
    return results[:limit]


@router.get("/molecules/categories", response_model=List[str])
async def get_categories():
    """Get all molecule categories."""
    categories = list(set(m["category"] for m in MOLECULE_DATABASE))
    return sorted(categories)
