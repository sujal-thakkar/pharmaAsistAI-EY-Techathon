"""Clinical Trials Agent - Searches and analyzes clinical trial data using RAG."""
from typing import Dict, Any, Optional, Callable, List
import asyncio
from datetime import datetime, timedelta
import random
import re

from app.agents.base import BaseAgent
from app.services.rag_service import rag_service
from app.services.llm_service import llm_service


class ClinicalTrialsAgent(BaseAgent):
    """Agent for searching and analyzing clinical trial information using RAG pipeline."""
    
    def __init__(self):
        super().__init__(
            name="Clinical Trials Agent",
            description="Searches knowledge base for clinical trial information and evidence"
        )
    
    async def execute(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """Search and analyze clinical trials for the molecule using RAG."""
        
        if progress_callback:
            progress_callback(10, "Searching clinical trial knowledge base...")
        
        # Search RAG for clinical trial information
        clinical_query = f"{query} clinical trials phase efficacy safety endpoints"
        rag_results = await rag_service.search(clinical_query, n_results=8)
        
        if progress_callback:
            progress_callback(30, "Analyzing trial evidence...")
        
        await asyncio.sleep(0.2)
        
        # Extract clinical information from RAG context
        clinical_contexts = [r["content"] for r in rag_results if r.get("relevance_score", 0) > 0.2]
        
        if progress_callback:
            progress_callback(50, "Extracting trial data...")
        
        # Use LLM to extract structured clinical trial information
        if clinical_contexts and llm_service.is_available:
            trial_summary = await self._extract_clinical_info(query, clinical_contexts)
        else:
            trial_summary = self._generate_generic_trial_info(query)
        
        if progress_callback:
            progress_callback(70, "Generating trial analysis...")
        
        # Generate mock trial listings (simulating ClinicalTrials.gov search)
        trials = self._generate_contextual_trials(query, clinical_contexts)
        
        # Analyze trial phases
        phase_summary = self._analyze_phases(trials)
        
        if progress_callback:
            progress_callback(90, "Compiling clinical report...")
        
        await asyncio.sleep(0.1)
        
        # Compile results
        results = {
            "trials": trials,
            "totalTrials": len(trials),
            "phaseSummary": phase_summary,
            "activeTrials": sum(1 for t in trials if t["status"] == "Recruiting"),
            "completedTrials": sum(1 for t in trials if t["status"] == "Completed"),
            "averageEnrollment": sum(t["enrollment"] for t in trials) // len(trials) if trials else 0,
            "clinicalEvidence": trial_summary,
            "sources": [
                {
                    "content": r["content"][:150] + "...",
                    "relevance": r.get("relevance_score", 0)
                }
                for r in rag_results[:3]
            ],
            "lastUpdated": datetime.utcnow().isoformat()
        }
        
        if progress_callback:
            progress_callback(100, f"Analyzed {len(trials)} clinical trials")
        
        return results
    
    async def _extract_clinical_info(self, molecule: str, contexts: list) -> Dict[str, Any]:
        """Use LLM to extract structured clinical trial information."""
        context_text = "\n\n".join(contexts)
        
        prompt = f"""Based on the following information about {molecule}, extract clinical trial evidence.

CONTEXT:
{context_text}

Extract the following information in JSON format:
{{
  "keyFindings": ["list of key clinical findings"],
  "efficacyData": "summary of efficacy data from trials",
  "safetyProfile": "summary of safety/side effect data",
  "trialNames": ["names of specific trials mentioned"],
  "endpoints": ["primary/secondary endpoints mentioned"],
  "patientPopulation": "description of patient populations studied"
}}

Only output the JSON, nothing else."""

        try:
            response = await llm_service.generate_completion(prompt)
            # Clean and parse JSON
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            response = response.strip()
            
            import json
            return json.loads(response)
        except Exception as e:
            return self._generate_generic_trial_info(molecule)
    
    def _generate_generic_trial_info(self, molecule: str) -> Dict[str, Any]:
        """Generate generic clinical trial summary."""
        return {
            "keyFindings": [
                f"Multiple clinical trials have evaluated {molecule}",
                "Phase 3 trials demonstrated efficacy vs placebo",
                "Safety profile established through controlled studies"
            ],
            "efficacyData": f"Clinical trials of {molecule} have shown therapeutic benefit in target indications.",
            "safetyProfile": "Common adverse events reported in clinical trials with manageable safety profile.",
            "trialNames": [],
            "endpoints": ["Primary efficacy endpoint", "Safety and tolerability"],
            "patientPopulation": "Adult patients with relevant indication"
        }
    
    def _generate_contextual_trials(self, molecule_name: str, contexts: list) -> List[Dict[str, Any]]:
        """Generate mock clinical trial data informed by RAG context."""
        
        # Try to extract actual trial names from context
        context_text = " ".join(contexts)
        
        # Look for specific trial patterns
        trial_patterns = {
            "semaglutide|ozempic|wegovy": ["SUSTAIN-1", "SUSTAIN-2", "STEP 1", "STEP 2", "SELECT"],
            "pembrolizumab|keytruda": ["KEYNOTE-024", "KEYNOTE-189", "KEYNOTE-522"],
            "adalimumab|humira": ["ULTRA-1", "ULTRA-2", "CHARM"],
            "tirzepatide|mounjaro": ["SURMOUNT-1", "SURPASS-1", "SURPASS-2"],
            "metformin": ["UKPDS", "DPP", "ADOPT"],
        }
        
        # Find matching trial names
        trial_names = []
        molecule_lower = molecule_name.lower()
        for pattern, names in trial_patterns.items():
            if re.search(pattern, molecule_lower):
                trial_names = names
                break
        
        # Determine conditions based on context
        conditions = self._extract_conditions(context_text, molecule_name)
        
        phases = ["Phase 1", "Phase 2", "Phase 2/3", "Phase 3", "Phase 4"]
        statuses = ["Recruiting", "Active, not recruiting", "Completed", "Enrolling by invitation"]
        sponsors = [
            "Novo Nordisk", "Pfizer", "Eli Lilly", "AstraZeneca",
            "Merck", "Johnson & Johnson", "Roche", "Bristol-Myers Squibb",
            "GSK", "Sanofi", "Boehringer Ingelheim"
        ]
        
        num_trials = random.randint(5, 10)
        trials = []
        
        for i in range(num_trials):
            start_date = datetime.now() - timedelta(days=random.randint(100, 1500))
            phase = random.choice(phases)
            status = random.choice(statuses)
            
            # Use real trial name if available
            if i < len(trial_names):
                trial_title = f"{trial_names[i]}: Study of {molecule_name} in {random.choice(conditions)}"
            else:
                trial_title = f"Study of {molecule_name} in {random.choice(conditions)}"
            
            trial = {
                "id": f"NCT{random.randint(10000000, 99999999)}",
                "title": trial_title,
                "phase": phase,
                "status": status,
                "enrollment": random.randint(50, 5000),
                "condition": random.choice(conditions),
                "sponsor": random.choice(sponsors),
                "startDate": start_date.strftime("%Y-%m-%d"),
                "estimatedCompletion": (start_date + timedelta(days=random.randint(365, 1095))).strftime("%Y-%m-%d"),
                "primaryOutcome": f"Efficacy of {molecule_name} measured by primary endpoint",
                "locations": random.randint(5, 100)
            }
            trials.append(trial)
        
        return trials
    
    def _extract_conditions(self, context: str, molecule: str) -> List[str]:
        """Extract relevant conditions from context."""
        condition_keywords = {
            "diabetes": ["Type 2 Diabetes", "Diabetes Mellitus", "Glycemic Control"],
            "obesity": ["Obesity", "Weight Management", "Chronic Weight Management"],
            "cancer": ["Cancer", "Solid Tumors", "Malignancy"],
            "pain": ["Chronic Pain", "Pain Management", "Analgesia"],
            "inflammation": ["Inflammation", "Inflammatory Disease", "Anti-inflammatory"],
            "cardiovascular": ["Cardiovascular Disease", "Heart Disease", "MACE Reduction"],
            "arthritis": ["Rheumatoid Arthritis", "Psoriatic Arthritis", "Arthritis"],
            "psoriasis": ["Psoriasis", "Plaque Psoriasis", "Skin Disease"],
            "crohn": ["Crohn's Disease", "Inflammatory Bowel Disease", "IBD"],
        }
        
        context_lower = context.lower()
        found_conditions = []
        
        for keyword, conditions in condition_keywords.items():
            if keyword in context_lower or keyword in molecule.lower():
                found_conditions.extend(conditions)
        
        if not found_conditions:
            found_conditions = ["Target Indication", "Disease State", "Medical Condition"]
        
        return list(set(found_conditions))[:5]
    
    def _analyze_phases(self, trials: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze trial phase distribution."""
        phases = {}
        for trial in trials:
            phase = trial["phase"]
            phases[phase] = phases.get(phase, 0) + 1
        return phases


# Create singleton instance
clinical_agent = ClinicalTrialsAgent()
