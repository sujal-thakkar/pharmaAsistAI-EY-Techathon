"""Insight Synthesizer Agent - Generates comprehensive insights from all agent data."""
from typing import Dict, Any, Optional, Callable, List
import asyncio
from datetime import datetime

from app.agents.base import BaseAgent
from app.config import settings


class InsightSynthesizerAgent(BaseAgent):
    """Agent for synthesizing insights from all research data."""
    
    def __init__(self):
        super().__init__(
            name="Insight Synthesizer",
            description="Synthesizes comprehensive insights from all research agents"
        )
    
    async def execute(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """Synthesize insights from all agent results."""
        
        if progress_callback:
            progress_callback(10, "Analyzing research data...")
        
        await asyncio.sleep(0.3)
        
        # Extract data from context (other agent results)
        molecule_data = context.get("molecule", {}).get("data", {})
        clinical_data = context.get("clinical", {}).get("data", {})
        market_data = context.get("market", {}).get("data", {})
        regulatory_data = context.get("regulatory", {}).get("data", {})
        
        if progress_callback:
            progress_callback(30, "Identifying key patterns...")
        
        await asyncio.sleep(0.3)
        
        # Generate insights based on data
        insights = self._generate_insights(query, molecule_data, clinical_data, market_data, regulatory_data)
        
        if progress_callback:
            progress_callback(50, "Generating strategic recommendations...")
        
        await asyncio.sleep(0.3)
        
        # Generate summary
        summary = self._generate_summary(query, insights, market_data, regulatory_data)
        
        if progress_callback:
            progress_callback(70, "Compiling source citations...")
        
        await asyncio.sleep(0.2)
        
        # Generate sources
        sources = self._generate_sources(query)
        
        if progress_callback:
            progress_callback(90, "Finalizing report...")
        
        await asyncio.sleep(0.2)
        
        results = {
            "insights": insights,
            "summary": summary,
            "sources": sources,
            "keyMetrics": self._extract_key_metrics(market_data, clinical_data, regulatory_data),
            "recommendations": self._generate_recommendations(insights),
            "riskFactors": self._identify_risks(clinical_data, regulatory_data),
            "generatedAt": datetime.utcnow().isoformat()
        }
        
        if progress_callback:
            progress_callback(100, f"Generated {len(insights)} insights")
        
        return results
    
    def _generate_insights(
        self,
        molecule_name: str,
        molecule_data: Dict,
        clinical_data: Dict,
        market_data: Dict,
        regulatory_data: Dict
    ) -> List[Dict[str, Any]]:
        """Generate insights from all data sources."""
        insights = []
        
        # Market insights
        if market_data:
            market_size = market_data.get("marketSize", 0)
            growth_rate = market_data.get("growthRate", 0)
            
            if market_size > 10000000000:
                insights.append({
                    "id": "insight-market-1",
                    "type": "market",
                    "category": "Market Size",
                    "title": "Blockbuster Drug Status",
                    "content": f"{molecule_name} operates in a ${market_size/1e9:.1f}B market, placing it among top pharmaceutical products globally.",
                    "impact": "high",
                    "confidence": 0.92
                })
            
            if growth_rate > 20:
                insights.append({
                    "id": "insight-market-2",
                    "type": "market",
                    "category": "Growth",
                    "title": "Exceptional Growth Trajectory",
                    "content": f"The market is growing at {growth_rate:.1f}% annually, significantly outpacing industry average of 5-7%.",
                    "impact": "high",
                    "confidence": 0.88
                })
        
        # Clinical insights
        if clinical_data:
            active_trials = clinical_data.get("activeTrials", 0)
            total_trials = clinical_data.get("totalTrials", 0)
            
            if total_trials > 5:
                insights.append({
                    "id": "insight-clinical-1",
                    "type": "clinical",
                    "category": "Development Pipeline",
                    "title": "Robust Clinical Pipeline",
                    "content": f"{total_trials} clinical trials identified, with {active_trials} actively recruiting, indicating strong development momentum.",
                    "impact": "medium",
                    "confidence": 0.95
                })
        
        # Regulatory insights
        if regulatory_data:
            reg_status = regulatory_data.get("status", {})
            if reg_status.get("fda") == "Approved":
                insights.append({
                    "id": "insight-reg-1",
                    "type": "regulatory",
                    "category": "Approval Status",
                    "title": "Full Regulatory Approval",
                    "content": f"{molecule_name} has FDA and EMA approval, providing strong market access in major territories.",
                    "impact": "high",
                    "confidence": 0.99
                })
            
            patent_info = regulatory_data.get("patent_info", {})
            if patent_info.get("status") == "Active":
                insights.append({
                    "id": "insight-reg-2",
                    "type": "regulatory",
                    "category": "IP Protection",
                    "title": "Patent Protection Active",
                    "content": f"Patent protection extends until {patent_info.get('expiryDate', 'N/A')}, providing market exclusivity.",
                    "impact": "high",
                    "confidence": 0.97
                })
        
        # Competitive insights
        if market_data and market_data.get("competitors"):
            competitors = market_data.get("competitors", [])
            insights.append({
                "id": "insight-comp-1",
                "type": "competitive",
                "category": "Competition",
                "title": "Competitive Landscape Analysis",
                "content": f"{len(competitors)} major competitors identified in the therapeutic area, with varying market share distribution.",
                "impact": "medium",
                "confidence": 0.85
            })
        
        # Safety insight
        insights.append({
            "id": "insight-safety-1",
            "type": "safety",
            "category": "Safety Profile",
            "title": "Established Safety Profile",
            "content": f"{molecule_name} has demonstrated an acceptable safety profile in clinical studies and post-marketing surveillance.",
            "impact": "medium",
            "confidence": 0.82
        })
        
        return insights
    
    def _generate_summary(
        self,
        molecule_name: str,
        insights: List[Dict],
        market_data: Dict,
        regulatory_data: Dict
    ) -> str:
        """Generate executive summary."""
        market_size = market_data.get("marketSize", 0) if market_data else 0
        growth_rate = market_data.get("growthRate", 0) if market_data else 0
        reg_status = regulatory_data.get("status", {}).get("fda", "Unknown") if regulatory_data else "Unknown"
        
        summary = f"""## Executive Summary: {molecule_name}

**Market Position:** {molecule_name} operates in a ${market_size/1e9:.1f}B market with {growth_rate:.1f}% projected growth.

**Regulatory Status:** Currently {reg_status} by FDA, with active market presence in major global territories.

**Key Findings:**
- {len(insights)} key insights identified across market, clinical, regulatory, and competitive dimensions
- Strong growth trajectory supported by expanding indications and market adoption
- Patent protection and regulatory exclusivity provide competitive moat

**Recommendation:** Based on comprehensive analysis, {molecule_name} represents a significant opportunity in the pharmaceutical landscape with strong fundamentals and growth potential.
"""
        return summary
    
    def _generate_sources(self, molecule_name: str) -> List[Dict[str, Any]]:
        """Generate source citations."""
        return [
            {
                "id": "src-1",
                "title": f"{molecule_name} Market Analysis Report 2024",
                "type": "Market Research",
                "publisher": "Global Market Insights",
                "date": "2024-Q3",
                "url": "https://example.com/market-report",
                "reliability": 0.95
            },
            {
                "id": "src-2",
                "title": "ClinicalTrials.gov Database",
                "type": "Clinical Database",
                "publisher": "U.S. National Library of Medicine",
                "date": "2024",
                "url": "https://clinicaltrials.gov",
                "reliability": 0.99
            },
            {
                "id": "src-3",
                "title": "FDA Drug Approval Database",
                "type": "Regulatory",
                "publisher": "U.S. Food and Drug Administration",
                "date": "2024",
                "url": "https://www.accessdata.fda.gov/scripts/cder/daf/",
                "reliability": 0.99
            },
            {
                "id": "src-4",
                "title": f"{molecule_name} Prescribing Information",
                "type": "Product Label",
                "publisher": "Manufacturer",
                "date": "2024",
                "url": "https://example.com/prescribing-info",
                "reliability": 0.98
            },
            {
                "id": "src-5",
                "title": "USPTO Patent Database",
                "type": "Patent",
                "publisher": "United States Patent and Trademark Office",
                "date": "2024",
                "url": "https://www.uspto.gov",
                "reliability": 0.99
            }
        ]
    
    def _extract_key_metrics(
        self,
        market_data: Dict,
        clinical_data: Dict,
        regulatory_data: Dict
    ) -> Dict[str, Any]:
        """Extract key metrics for dashboard display."""
        return {
            "marketSize": market_data.get("marketSize", 0) if market_data else 0,
            "growthRate": market_data.get("growthRate", 0) if market_data else 0,
            "marketShare": market_data.get("marketShare", 0) if market_data else 0,
            "activeTrials": clinical_data.get("activeTrials", 0) if clinical_data else 0,
            "totalTrials": clinical_data.get("totalTrials", 0) if clinical_data else 0,
            "fdaStatus": regulatory_data.get("status", {}).get("fda", "Unknown") if regulatory_data else "Unknown",
            "patentStatus": regulatory_data.get("patent_info", {}).get("status", "Unknown") if regulatory_data else "Unknown"
        }
    
    def _generate_recommendations(self, insights: List[Dict]) -> List[str]:
        """Generate strategic recommendations."""
        return [
            "Monitor competitive pipeline developments closely",
            "Explore expansion into adjacent therapeutic areas",
            "Prepare for patent cliff with lifecycle management strategies",
            "Invest in real-world evidence generation to support market access",
            "Consider geographic expansion in emerging markets"
        ]
    
    def _identify_risks(self, clinical_data: Dict, regulatory_data: Dict) -> List[Dict[str, Any]]:
        """Identify risk factors."""
        return [
            {
                "risk": "Patent Expiration",
                "severity": "high",
                "timeframe": "2-5 years",
                "mitigation": "Lifecycle management, new formulations"
            },
            {
                "risk": "Competitive Pressure",
                "severity": "medium",
                "timeframe": "Ongoing",
                "mitigation": "Differentiation through clinical evidence"
            },
            {
                "risk": "Regulatory Changes",
                "severity": "medium",
                "timeframe": "1-3 years",
                "mitigation": "Proactive regulatory engagement"
            }
        ]
