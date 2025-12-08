"""Molecule Analyzer Agent - Fetches molecular structure and properties using RAG."""
from typing import Dict, Any, Optional, Callable
import asyncio
import re

from app.agents.base import BaseAgent
from app.services.rag_service import rag_service
from app.services.llm_service import llm_service


class MoleculeAnalyzerAgent(BaseAgent):
    """Agent for analyzing molecular structure and properties using RAG pipeline."""
    
    def __init__(self):
        super().__init__(
            name="Molecule Analyzer",
            description="Fetches molecular structure, formula, and chemical properties from knowledge base"
        )
        
        # Reference database for common drugs (fallback when RAG doesn't have data)
        self.molecule_reference = {
            "tirzepatide": {
                "name": "Tirzepatide",
                "formula": "C225H348N48O68",
                "molecularWeight": 4813.45,
                "category": "Dual GIP/GLP-1 Agonist",
                "mechanism": "Dual agonist of glucose-dependent insulinotropic polypeptide (GIP) and glucagon-like peptide-1 (GLP-1) receptors, enhancing insulin secretion, reducing glucagon, and promoting satiety.",
                "casNumber": "2023788-19-2"
            },
            "semaglutide": {
                "name": "Semaglutide",
                "formula": "C187H291N45O59",
                "molecularWeight": 4113.58,
                "category": "GLP-1 Receptor Agonist",
                "mechanism": "Activates GLP-1 receptors, enhancing glucose-dependent insulin secretion, suppressing glucagon release, and slowing gastric emptying.",
                "casNumber": "910463-68-2"
            },
            "ibuprofen": {
                "name": "Ibuprofen",
                "formula": "C13H18O2",
                "molecularWeight": 206.29,
                "category": "NSAID",
                "mechanism": "Inhibits cyclooxygenase (COX-1 and COX-2) enzymes, reducing prostaglandin synthesis and thereby decreasing inflammation, pain, and fever.",
                "casNumber": "15687-27-1"
            },
            "aspirin": {
                "name": "Aspirin",
                "formula": "C9H8O4",
                "molecularWeight": 180.16,
                "category": "NSAID / Antiplatelet",
                "mechanism": "Irreversibly inhibits COX-1 and COX-2, blocking prostaglandin and thromboxane synthesis. Antiplatelet effect lasts for platelet lifetime.",
                "casNumber": "50-78-2"
            },
            "metformin": {
                "name": "Metformin",
                "formula": "C4H11N5",
                "molecularWeight": 129.16,
                "category": "Biguanide Antidiabetic",
                "mechanism": "Decreases hepatic glucose production, increases insulin sensitivity, and reduces intestinal glucose absorption.",
                "casNumber": "657-24-9"
            },
            "pembrolizumab": {
                "name": "Pembrolizumab",
                "formula": "C6504H10004N1716O2036S46",
                "molecularWeight": 146500,
                "category": "PD-1 Inhibitor (Immunotherapy)",
                "mechanism": "Humanized monoclonal antibody that blocks PD-1/PD-L1 interaction, releasing T-cell inhibition and enabling immune-mediated tumor destruction.",
                "casNumber": "1374853-91-4"
            },
            "adalimumab": {
                "name": "Adalimumab",
                "formula": "C6428H9912N1694O1987S46",
                "molecularWeight": 144190,
                "category": "TNF-alpha Inhibitor",
                "mechanism": "Fully human monoclonal antibody that binds TNF-alpha, preventing its interaction with cell surface TNF receptors and reducing inflammation.",
                "casNumber": "331731-18-1"
            },
            "paracetamol": {
                "name": "Paracetamol",
                "formula": "C8H9NO2",
                "molecularWeight": 151.16,
                "category": "Analgesic / Antipyretic",
                "mechanism": "Central inhibition of COX enzymes and activation of descending serotonergic pathways. Minimal anti-inflammatory effect.",
                "casNumber": "103-90-2"
            },
            "atorvastatin": {
                "name": "Atorvastatin",
                "formula": "C33H35FN2O5",
                "molecularWeight": 558.64,
                "category": "Statin (HMG-CoA Reductase Inhibitor)",
                "mechanism": "Inhibits HMG-CoA reductase, reducing hepatic cholesterol synthesis and increasing LDL receptor expression.",
                "casNumber": "134523-00-5"
            },
        }
        
        # Common molecule synonyms for better matching
        self.molecule_synonyms = {
            "advil": "ibuprofen",
            "motrin": "ibuprofen",
            "nurofen": "ibuprofen",
            "tylenol": "paracetamol",
            "acetaminophen": "paracetamol",
            "ozempic": "semaglutide",
            "wegovy": "semaglutide",
            "rybelsus": "semaglutide",
            "mounjaro": "tirzepatide",
            "zepbound": "tirzepatide",
            "keytruda": "pembrolizumab",
            "humira": "adalimumab",
            "lipitor": "atorvastatin",
        }
        
        # Default indications for common drugs
        self.drug_indications = {
            "ibuprofen": ["Pain Relief", "Anti-Inflammatory", "Fever Reduction", "Arthritis"],
            "aspirin": ["Pain Relief", "Fever Reduction", "Anti-Platelet Therapy", "Cardiovascular Prevention"],
            "semaglutide": ["Type 2 Diabetes Mellitus", "Chronic Weight Management"],
            "tirzepatide": ["Type 2 Diabetes Mellitus", "Chronic Weight Management"],
            "pembrolizumab": ["Melanoma", "Non-Small Cell Lung Cancer", "Head and Neck Cancer"],
            "adalimumab": ["Rheumatoid Arthritis", "Plaque Psoriasis", "Crohn's Disease"],
            "metformin": ["Type 2 Diabetes Mellitus", "Prediabetes"],
            "paracetamol": ["Pain Relief", "Fever Reduction"],
            "acetaminophen": ["Pain Relief", "Fever Reduction"],
            "atorvastatin": ["High Cholesterol", "Cardiovascular Disease Prevention"],
        }
    
    def _get_default_indications(self, molecule_name: str) -> list:
        """Get default indications for a molecule."""
        molecule_lower = molecule_name.lower()
        for drug, indications in self.drug_indications.items():
            if drug in molecule_lower or molecule_lower in drug:
                return indications
        return []
    
    def _normalize_molecule_name(self, query: str) -> str:
        """Normalize molecule name, handling brand names and synonyms."""
        query_lower = query.lower().strip()
        
        # Check for synonyms
        for brand, generic in self.molecule_synonyms.items():
            if brand in query_lower:
                return generic
        
        # Extract molecule name from query phrases
        patterns = [
            r"analyze\s+(\w+)",
            r"about\s+(\w+)",
            r"information\s+on\s+(\w+)",
            r"properties\s+of\s+(\w+)",
            r"what\s+is\s+(\w+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                extracted = match.group(1)
                # Check if extracted word is a known synonym
                return self.molecule_synonyms.get(extracted, extracted)
        
        # Return the first word as molecule name if no pattern matches
        first_word = query_lower.split()[0] if query_lower.split() else query_lower
        return self.molecule_synonyms.get(first_word, first_word)
    
    async def _extract_molecule_info_from_context(
        self, 
        molecule_name: str, 
        contexts: list
    ) -> Dict[str, Any]:
        """Use LLM to extract structured molecule information from RAG context."""
        
        context_text = "\n\n".join(contexts)
        
        prompt = f"""Based on the following pharmaceutical knowledge about {molecule_name}, extract the molecular information in a structured format.

CONTEXT:
{context_text}

Extract the following information (use "Unknown" or null if not found):
1. Name: Official/generic name of the molecule
2. Formula: Chemical formula (e.g., C13H18O2)
3. Molecular Weight: In g/mol
4. Category: Drug class (e.g., NSAID, GLP-1 Agonist)
5. Description: Brief 1-2 sentence description
6. CAS Number: Chemical Abstracts Service registry number
7. Mechanism of Action: How the drug works
8. IUPAC Name: Systematic chemical name (if available)

Respond in this exact JSON format:
{{
  "name": "...",
  "formula": "...",
  "molecularWeight": ...,
  "category": "...",
  "description": "...",
  "casNumber": "...",
  "mechanismOfAction": "...",
  "iupacName": "...",
  "indications": ["indication1", "indication2"]
}}

Only output the JSON, nothing else."""

        if llm_service.is_available:
            try:
                response = await llm_service.generate_completion(prompt)
                # Parse the JSON from response
                import json
                # Clean the response - remove markdown code blocks if present
                response = response.strip()
                if response.startswith("```"):
                    response = response.split("```")[1]
                    if response.startswith("json"):
                        response = response[4:]
                response = response.strip()
                
                data = json.loads(response)
                return data
            except Exception as e:
                # Log error and fall back to regex extraction
                import logging
                logging.error(f"LLM extraction failed: {e}")
        
        # Fallback: regex-based extraction from context
        return self._regex_extract_info(molecule_name, context_text)
    
    def _regex_extract_info(self, molecule_name: str, context: str) -> Dict[str, Any]:
        """Fallback regex-based information extraction."""
        info = {
            "name": molecule_name.title(),
            "formula": "Unknown",
            "molecularWeight": 0,
            "category": "Unknown",
            "description": f"Pharmaceutical compound: {molecule_name}",
            "casNumber": None,
            "mechanismOfAction": "Information not available",
            "iupacName": None,
            "smiles": None,
            "indications": self._get_default_indications(molecule_name)
        }
        
        context_lower = context.lower()
        
        # Extract formula
        formula_match = re.search(r'formula[:\s]+([A-Z][A-Za-z0-9]+)', context)
        if formula_match:
            info["formula"] = formula_match.group(1)
        
        # Extract molecular weight
        mw_match = re.search(r'molecular\s+weight[:\s]+(\d+\.?\d*)', context_lower)
        if mw_match:
            info["molecularWeight"] = float(mw_match.group(1))
        
        # Extract CAS number
        cas_match = re.search(r'cas\s*(?:number)?[:\s]+(\d+-\d+-\d+)', context_lower)
        if cas_match:
            info["casNumber"] = cas_match.group(1)
        
        # Extract category from common patterns
        categories = [
            ("nsaid", "NSAID"),
            ("glp-1", "GLP-1 Receptor Agonist"),
            ("gip/glp-1", "Dual GIP/GLP-1 Agonist"),
            ("checkpoint inhibitor", "Checkpoint Inhibitor"),
            ("pd-1", "PD-1 Inhibitor"),
            ("tnf", "TNF Inhibitor"),
            ("statin", "Statin"),
            ("biguanide", "Biguanide"),
            ("analgesic", "Analgesic"),
            ("antipyretic", "Antipyretic"),
            ("antidiabetic", "Antidiabetic"),
        ]
        
        for keyword, category in categories:
            if keyword in context_lower:
                info["category"] = category
                break
        
        # Extract first meaningful sentence as description
        sentences = context.split('. ')
        for sentence in sentences:
            if molecule_name.lower() in sentence.lower() and len(sentence) > 30:
                info["description"] = sentence.strip()[:300]
                break
        
        # Extract mechanism of action
        moa_match = re.search(r'mechanism\s+of\s+action[:\s]+([^.]+\.)', context_lower)
        if moa_match:
            info["mechanismOfAction"] = moa_match.group(1).strip().capitalize()
        
        return info
    
    async def execute(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """Analyze molecule and return properties from RAG knowledge base."""
        
        if progress_callback:
            progress_callback(10, "Parsing molecule query...")
        
        # Normalize the molecule name
        molecule_name = self._normalize_molecule_name(query)
        
        if progress_callback:
            progress_callback(20, f"Searching knowledge base for {molecule_name}...")
        
        # Search RAG for molecule information
        rag_results = await rag_service.search(molecule_name, n_results=8)
        
        if progress_callback:
            progress_callback(40, "Processing search results...")
        
        await asyncio.sleep(0.1)  # Small delay for UI feedback
        
        if rag_results and rag_results[0].get("relevance_score", 0) > 0.3:
            # Found relevant information in RAG
            contexts = [r["content"] for r in rag_results]
            
            if progress_callback:
                progress_callback(60, "Extracting molecular information...")
            
            # Extract structured information
            molecule_data = await self._extract_molecule_info_from_context(
                molecule_name, 
                contexts
            )
            
            if progress_callback:
                progress_callback(80, "Formatting results...")
            
            # Add source information
            molecule_data["sources"] = [
                {
                    "content": r["content"][:200] + "...",
                    "category": r["metadata"].get("category", "unknown"),
                    "relevance": r.get("relevance_score", 0)
                }
                for r in rag_results[:3]
            ]
            molecule_data["found_in_knowledge_base"] = True
            
        else:
            # No relevant information found in RAG - check reference database
            if progress_callback:
                progress_callback(60, f"Checking reference database for {molecule_name}...")
            
            # Look up in reference database
            ref_data = self.molecule_reference.get(molecule_name.lower())
            
            if ref_data:
                # Found in reference database
                molecule_data = {
                    "name": ref_data.get("name", molecule_name.title()),
                    "formula": ref_data.get("formula", "Unknown"),
                    "molecularWeight": ref_data.get("molecularWeight", 0),
                    "category": ref_data.get("category", "Unknown"),
                    "description": f"{ref_data.get('name', molecule_name)} is a {ref_data.get('category', 'pharmaceutical compound')}.",
                    "casNumber": ref_data.get("casNumber"),
                    "mechanismOfAction": ref_data.get("mechanism", "Not available"),
                    "iupacName": None,
                    "smiles": None,
                    "indications": self._get_default_indications(molecule_name),
                    "found_in_knowledge_base": False,
                    "sources": [{"content": "Reference Database", "category": "reference", "relevance": 1.0}]
                }
            else:
                # Not in reference database either
                molecule_data = {
                    "name": molecule_name.title(),
                    "formula": "Unknown",
                    "molecularWeight": 0,
                    "category": "Unknown",
                    "description": f"Limited information available for {molecule_name}. Consider adding relevant research papers to the knowledge base.",
                    "casNumber": None,
                    "mechanismOfAction": "Data not available in knowledge base",
                    "iupacName": None,
                    "smiles": None,
                    "indications": [],
                    "found_in_knowledge_base": False,
                    "sources": []
                }
        
        if progress_callback:
            progress_callback(100, "Molecule analysis complete")
        
        return {
            "agent": self.name,
            "status": "success",
            "data": molecule_data
        }


# Create singleton instance
molecule_agent = MoleculeAnalyzerAgent()
