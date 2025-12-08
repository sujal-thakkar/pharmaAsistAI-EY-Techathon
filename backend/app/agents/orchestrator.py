"""Agent Orchestrator - Coordinates multi-agent pharmaceutical research pipeline."""
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import asyncio
import logging

from app.agents.base import BaseAgent
from app.agents.molecule_agent import MoleculeAnalyzerAgent
from app.agents.clinical_agent import ClinicalTrialsAgent
from app.agents.market_agent import MarketIntelligenceAgent
from app.agents.regulatory_agent import RegulatoryAgent
from app.agents.synthesizer_agent import InsightSynthesizerAgent
from app.config import settings

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrates multiple specialized agents to conduct comprehensive
    pharmaceutical research on a molecule/drug.
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all research agents."""
        self.agents = {
            "molecule": MoleculeAnalyzerAgent(),
            "clinical": ClinicalTrialsAgent(),
            "market": MarketIntelligenceAgent(),
            "regulatory": RegulatoryAgent(),
            "synthesizer": InsightSynthesizerAgent()
        }
        
    async def run(
        self,
        molecule_name: str,
        analysis_types: List[str],
        additional_context: Optional[str] = None,
        progress_callback: Optional[Callable[[str, float, Optional[str]], None]] = None
    ) -> Dict[str, Any]:
        """
        Run the full research pipeline.
        
        Args:
            molecule_name: Name of the drug/molecule to research
            analysis_types: List of analysis types to perform
            additional_context: Additional context from user
            progress_callback: Callback(step_id, progress, summary)
            
        Returns:
            Complete analysis results
        """
        logger.info(f"🔬 Starting analysis pipeline for: {molecule_name}")
        logger.info(f"📋 Analysis types: {analysis_types}")
        
        results = {
            "molecule_name": molecule_name,
            "analysis_started": datetime.utcnow().isoformat(),
            "agent_results": {}
        }
        
        context = {
            "molecule_name": molecule_name,
            "additional_context": additional_context
        }
        
        # Step 1: Parse query (simulated)
        if progress_callback:
            progress_callback("parse", 0, None)
        await asyncio.sleep(0.5)
        if progress_callback:
            progress_callback("parse", 100, f"Query parsed: {molecule_name}")
        
        # Step 2: Molecule Analysis
        if progress_callback:
            progress_callback("molecule", 0, None)
        
        molecule_result = await self.agents["molecule"].run(
            query=molecule_name,
            context=context,
            progress_callback=lambda p, s: progress_callback("molecule", p, s) if progress_callback else None
        )
        results["agent_results"]["molecule"] = molecule_result
        context["molecule_data"] = molecule_result.get("data", {})
        
        # Step 3-6: Run analysis agents based on selected types
        analysis_agents = []
        
        if "clinical" in analysis_types:
            analysis_agents.append(("clinical", self.agents["clinical"]))
        if "market" in analysis_types or "competitive" in analysis_types:
            analysis_agents.append(("market", self.agents["market"]))
        if "regulatory" in analysis_types:
            analysis_agents.append(("regulatory", self.agents["regulatory"]))
        
        # Run agents concurrently
        async def run_agent_with_callback(step_id: str, agent: BaseAgent):
            return await agent.run(
                query=molecule_name,
                context=context,
                progress_callback=lambda p, s: progress_callback(step_id, p, s) if progress_callback else None
            )
        
        if analysis_agents:
            agent_tasks = [
                run_agent_with_callback(step_id, agent) 
                for step_id, agent in analysis_agents
            ]
            agent_results = await asyncio.gather(*agent_tasks, return_exceptions=True)
            
            for (step_id, _), result in zip(analysis_agents, agent_results):
                if isinstance(result, Exception):
                    results["agent_results"][step_id] = {
                        "status": "error",
                        "error": str(result)
                    }
                else:
                    results["agent_results"][step_id] = result
                    context[f"{step_id}_data"] = result.get("data", {})
        
        # Step: Patent analysis (part of regulatory but separate step)
        if progress_callback:
            progress_callback("patent", 0, None)
        await asyncio.sleep(0.3)
        results["agent_results"]["patent"] = {
            "status": "success",
            "data": context.get("regulatory_data", {}).get("patent_info", {})
        }
        if progress_callback:
            progress_callback("patent", 100, "Patent analysis complete")
        
        # Step 7: Synthesize insights
        if progress_callback:
            progress_callback("synthesizer", 0, None)
        
        synthesizer_result = await self.agents["synthesizer"].run(
            query=molecule_name,
            context=results["agent_results"],
            progress_callback=lambda p, s: progress_callback("synthesizer", p, s) if progress_callback else None
        )
        results["agent_results"]["synthesizer"] = synthesizer_result
        
        # Compile final results
        results["analysis_completed"] = datetime.utcnow().isoformat()
        results["status"] = "completed"
        
        # Format results for frontend
        formatted_results = self._format_results(results)
        
        logger.info(f"✨ Analysis pipeline completed for: {molecule_name}")
        
        return formatted_results
    
    def _format_results(self, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """Format raw agent results into frontend-compatible structure."""
        agent_data = raw_results.get("agent_results", {})
        
        molecule_data = agent_data.get("molecule", {}).get("data", {})
        clinical_data = agent_data.get("clinical", {}).get("data", {})
        market_data = agent_data.get("market", {}).get("data", {})
        regulatory_data = agent_data.get("regulatory", {}).get("data", {})
        synthesizer_data = agent_data.get("synthesizer", {}).get("data", {})
        
        # Build patentInfo from regulatory data
        patent_expiry = regulatory_data.get("patentExpiry", "Unknown")
        patent_analysis = regulatory_data.get("patentAnalysis", {})
        patent_info = {
            "status": "Expired" if patent_expiry == "Expired" else ("Active" if patent_expiry else "Unknown"),
            "expiryDate": patent_expiry if patent_expiry not in ["Expired", "Unknown", ""] else "",
            "patentNumber": patent_analysis.get("patentNumber", "N/A"),
            "title": patent_analysis.get("title", "N/A"),
            "holder": patent_analysis.get("holder", "N/A"),
        }
        
        # Build regulatoryStatus from regulatory data
        regulatory_status = {
            "fda": regulatory_data.get("fda", "Unknown"),
            "ema": regulatory_data.get("ema", "Unknown"),
            "approvalDate": regulatory_data.get("approvalDate"),
            "approvedIndications": regulatory_data.get("approvedIndications", []),
            "labelWarnings": regulatory_data.get("labelWarnings", []),
        }
        
        return {
            "id": f"analysis-{datetime.utcnow().timestamp():.0f}",
            "moleculeName": raw_results.get("molecule_name"),
            "generatedAt": raw_results.get("analysis_completed"),
            "moleculeData": molecule_data,
            "clinicalTrials": clinical_data.get("trials", []),
            "marketData": market_data,
            "regulatoryStatus": regulatory_status,
            "patentInfo": patent_info,
            "insights": synthesizer_data.get("insights", []),
            "summary": synthesizer_data.get("summary", ""),
            "sources": synthesizer_data.get("sources", [])
        }
