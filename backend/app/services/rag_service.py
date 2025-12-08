"""RAG Service - Retrieval Augmented Generation for pharmaceutical data."""
from typing import List, Dict, Any, Optional
import logging
import os
import uuid
import asyncio

from app.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """Service for Retrieval Augmented Generation using ChromaDB with Gemini embeddings."""
    
    def __init__(self):
        self.collection = None
        self.embedding_function = None
        self._initialize_chromadb()
    
    def _get_embedding_function(self):
        """Get the appropriate embedding function. Uses local sentence-transformers for reliability."""
        try:
            # Use local sentence-transformers embeddings (no API quota issues)
            # This is more reliable than Gemini/OpenAI embeddings for hackathon demo
            from chromadb.utils import embedding_functions
            
            # sentence-transformers will use the default all-MiniLM-L6-v2 model
            # which is fast and doesn't require API calls
            logger.info("✅ Using local sentence-transformers embeddings (all-MiniLM-L6-v2)")
            return embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
                
        except Exception as e:
            logger.warning(f"Sentence-transformers not available: {e}")
            logger.info("⚠️ Using ChromaDB default embeddings")
            return None
    
    def _initialize_chromadb(self):
        """Initialize ChromaDB for vector storage."""
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings
            
            # Create persist directory if it doesn't exist
            os.makedirs(settings.chroma_persist_directory, exist_ok=True)
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_directory,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
            
            # Get embedding function
            self.embedding_function = self._get_embedding_function()
            
            # Get or create collection for pharmaceutical data
            if self.embedding_function:
                self.collection = self.client.get_or_create_collection(
                    name="pharma_knowledge",
                    embedding_function=self.embedding_function,
                    metadata={"description": "Pharmaceutical research knowledge base"}
                )
            else:
                self.collection = self.client.get_or_create_collection(
                    name="pharma_knowledge",
                    metadata={"description": "Pharmaceutical research knowledge base"}
                )
            
            logger.info(f"✅ ChromaDB initialized at {settings.chroma_persist_directory}")
            logger.info(f"📚 Collection contains {self.collection.count()} documents")
            
            # Seed with initial data if empty
            if self.collection.count() == 0:
                self._seed_initial_data()
                
        except Exception as e:
            logger.error(f"❌ ChromaDB initialization error: {str(e)}")
            self.collection = None
    
    def _seed_initial_data(self):
        """Seed the vector database with comprehensive pharmaceutical knowledge."""
        logger.info("🌱 Seeding ChromaDB with pharmaceutical knowledge base...")
        
        # Comprehensive pharmaceutical knowledge organized by drug/category
        documents = [
            # ===== IBUPROFEN =====
            "Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) used to treat pain, fever, and inflammation. Chemical formula: C13H18O2, molecular weight: 206.29 g/mol. CAS Number: 15687-27-1. IUPAC name: 2-(4-isobutylphenyl)propionic acid.",
            "Ibuprofen mechanism of action: It works by inhibiting cyclooxygenase (COX-1 and COX-2) enzymes, which reduces prostaglandin synthesis and thereby decreases inflammation, pain, and fever.",
            "Ibuprofen clinical uses: Treatment of mild to moderate pain, osteoarthritis, rheumatoid arthritis, dysmenorrhea, headache, dental pain, and fever reduction. Also used for patent ductus arteriosus in premature infants.",
            "Ibuprofen side effects: Common adverse effects include gastrointestinal disturbances (nausea, dyspepsia, GI bleeding, peptic ulcers), cardiovascular risks (increased MI and stroke risk), renal impairment, and hypersensitivity reactions.",
            "Ibuprofen market data: Global ibuprofen market valued at approximately $1.2 billion, with major manufacturers including GSK, Pfizer, and Johnson & Johnson. Available OTC in most countries under brands Advil, Motrin, Nurofen.",
            "Ibuprofen dosing: Adults typically 200-400mg every 4-6 hours, maximum 1200mg/day for OTC use. Prescription doses may go up to 3200mg/day for inflammatory conditions. Pediatric: 5-10mg/kg every 6-8 hours.",
            
            # ===== ASPIRIN =====
            "Aspirin (acetylsalicylic acid) is an NSAID used for pain, fever, inflammation, and cardiovascular protection. Chemical formula: C9H8O4, molecular weight: 180.16 g/mol. CAS Number: 50-78-2.",
            "Aspirin mechanism of action: Irreversibly inhibits COX-1 and COX-2 enzymes. Its antiplatelet effect comes from permanent acetylation of platelet COX-1, inhibiting thromboxane A2 synthesis for the platelet's lifetime (7-10 days).",
            "Aspirin clinical uses: Pain relief, fever reduction, anti-inflammatory therapy, and low-dose aspirin (75-100mg) for cardiovascular disease prevention and secondary prevention of heart attack and stroke.",
            "Aspirin side effects: GI bleeding, peptic ulcer, tinnitus at high doses, Reye syndrome in children with viral infections, hypersensitivity reactions, and increased bleeding risk. Contraindicated in children under 16 with viral illness.",
            
            # ===== SEMAGLUTIDE (OZEMPIC/WEGOVY) =====
            "Semaglutide (brand names: Ozempic, Wegovy, Rybelsus) is a GLP-1 receptor agonist. Formula: C187H291N45O59, molecular weight: 4113.58 g/mol. CAS Number: 910463-68-2. Developed by Novo Nordisk.",
            "Semaglutide mechanism of action: Activates GLP-1 receptors to enhance glucose-dependent insulin secretion, suppress glucagon release, slow gastric emptying, and reduce appetite through central nervous system effects on hypothalamus.",
            "Semaglutide clinical trials: SUSTAIN trials (type 2 diabetes) showed HbA1c reduction of 1.5-1.8%. STEP trials (obesity) demonstrated weight loss of 15-17% of body weight. SELECT trial showed 20% MACE reduction.",
            "Semaglutide market data: Novo Nordisk's blockbuster drug with sales exceeding $18 billion in 2023. Ozempic approved for type 2 diabetes, Wegovy for chronic weight management. Supply shortages due to unprecedented demand.",
            "Semaglutide side effects: Nausea, vomiting, diarrhea, constipation, abdominal pain (typically decrease over time). Rare risks include pancreatitis, medullary thyroid carcinoma (contraindicated in MEN2), gallbladder disease, gastroparesis.",
            "Semaglutide dosing: Ozempic starts at 0.25mg weekly, titrated to 0.5mg then 1mg or 2mg. Wegovy starts at 0.25mg weekly, titrated over 16-20 weeks to 2.4mg maintenance dose.",
            
            # ===== METFORMIN =====
            "Metformin is a biguanide antidiabetic medication and first-line treatment for type 2 diabetes. Formula: C4H11N5, molecular weight: 129.16 g/mol. CAS Number: 657-24-9. Generic drug, off-patent.",
            "Metformin mechanism of action: Primarily reduces hepatic glucose production by inhibiting gluconeogenesis via AMPK activation. Also improves insulin sensitivity in peripheral tissues and may modulate gut microbiome.",
            "Metformin clinical uses: Type 2 diabetes mellitus, polycystic ovary syndrome (PCOS), prediabetes prevention. Being studied for anti-aging (TAME trial), cancer prevention, and cognitive protection properties.",
            "Metformin side effects: GI symptoms (diarrhea, nausea, metallic taste) affect 20-30% of patients. Vitamin B12 deficiency with long-term use. Rare but serious: lactic acidosis (contraindicated in eGFR <30).",
            "Metformin market data: One of the most prescribed drugs worldwide, available as generic. Annual prescriptions exceed 80 million in the US alone. Cost-effective at under $10/month.",
            
            # ===== PEMBROLIZUMAB (KEYTRUDA) =====
            "Pembrolizumab (Keytruda) is a humanized monoclonal antibody PD-1 checkpoint inhibitor. Formula: C6504H10004N1716O2036S46, molecular weight: ~149 kDa. CAS Number: 1374853-91-4. Manufactured by Merck.",
            "Pembrolizumab mechanism of action: Blocks PD-1 receptor on T cells, preventing interaction with PD-L1/PD-L2 on tumor cells. This releases the 'brakes' on T-cell-mediated anti-tumor immune response.",
            "Pembrolizumab clinical uses: Melanoma, non-small cell lung cancer (NSCLC), head and neck squamous cell carcinoma, classical Hodgkin lymphoma, urothelial carcinoma, MSI-H/dMMR solid tumors, and 40+ other indications.",
            "Pembrolizumab clinical trials: KEYNOTE trials showed breakthrough survival benefits. KEYNOTE-024 (NSCLC) showed 10-month OS improvement. Used as first-line monotherapy or combination with chemotherapy.",
            "Pembrolizumab market data: Merck's blockbuster drug with sales exceeding $25 billion in 2023, making it the world's top-selling drug. Protected by patents until mid-2030s.",
            "Pembrolizumab side effects: Immune-related adverse events (irAEs) including pneumonitis (2-5%), colitis (1-2%), hepatitis, endocrinopathies (hypothyroidism most common), nephritis, and dermatologic reactions.",
            
            # ===== ADALIMUMAB (HUMIRA) =====
            "Adalimumab (Humira) is a fully human recombinant monoclonal antibody TNF-alpha inhibitor. Formula: C6428H9912N1694O1987S46, molecular weight: ~148 kDa. CAS Number: 331731-18-1. Originally by AbbVie.",
            "Adalimumab mechanism of action: Binds specifically to soluble and transmembrane TNF-alpha, blocking its interaction with p55 and p75 cell surface TNF receptors, thereby reducing inflammatory cascades.",
            "Adalimumab clinical uses: Rheumatoid arthritis, psoriatic arthritis, ankylosing spondylitis, Crohn's disease, ulcerative colitis, plaque psoriasis, hidradenitis suppurativa, uveitis, juvenile idiopathic arthritis.",
            "Adalimumab market data: Previously world's best-selling drug (peak sales $21 billion/year). Now facing biosimilar competition: Hadlima, Hyrimoz, Cyltezo, Amjevita (launched 2023) with 80%+ price discounts.",
            "Adalimumab side effects: Injection site reactions (20%), increased serious infection risk, reactivation of latent tuberculosis (must screen before starting), hepatotoxicity, heart failure exacerbation, lupus-like syndrome.",
            
            # ===== ATORVASTATIN (LIPITOR) =====
            "Atorvastatin (Lipitor) is an HMG-CoA reductase inhibitor (statin) for cholesterol management. Formula: C33H35FN2O5, molecular weight: 558.64 g/mol. CAS Number: 134523-00-5. Now generic.",
            "Atorvastatin mechanism of action: Competitively inhibits HMG-CoA reductase, the rate-limiting enzyme in hepatic cholesterol biosynthesis, leading to upregulation of LDL receptors and increased LDL clearance from blood.",
            "Atorvastatin clinical uses: Primary and secondary prevention of atherosclerotic cardiovascular disease, hypercholesterolemia, mixed dyslipidemia, familial hypercholesterolemia. Reduces LDL-C by 30-55%.",
            "Atorvastatin side effects: Myalgia (5-10%), elevated liver enzymes, rhabdomyolysis (rare but serious), new-onset diabetes (slight risk), cognitive effects. Avoid grapefruit juice (CYP3A4 interaction).",
            
            # ===== PARACETAMOL/ACETAMINOPHEN =====
            "Paracetamol (Acetaminophen/Tylenol) is an analgesic and antipyretic medication. Formula: C8H9NO2, molecular weight: 151.16 g/mol. CAS Number: 103-90-2. One of the most widely used OTC medications.",
            "Paracetamol mechanism of action: Not fully understood. Believed to inhibit COX enzymes centrally, activate descending serotonergic pain pathways, and interact with endocannabinoid system. Minimal anti-inflammatory effect.",
            "Paracetamol clinical uses: First-line treatment for mild-moderate pain and fever. Preferred analgesic in pregnancy, patients with renal disease, and those who cannot take NSAIDs. Component of many combination products.",
            "Paracetamol safety: Hepatotoxicity is main concern. Maximum 4g/day for adults (3g for elderly/liver disease). Overdose can cause acute liver failure. N-acetylcysteine is antidote if given within 8-10 hours.",
            
            # ===== TIRZEPATIDE (MOUNJARO/ZEPBOUND) =====
            "Tirzepatide (Mounjaro, Zepbound) is a dual GIP/GLP-1 receptor agonist developed by Eli Lilly. First-in-class mechanism targeting both incretin pathways for enhanced glycemic control and weight loss.",
            "Tirzepatide clinical trials: SURMOUNT trials showed up to 22.5% weight loss (superior to semaglutide). SURPASS trials showed HbA1c reductions up to 2.5%. Potential for obesity-related comorbidity improvement.",
            "Tirzepatide market data: Eli Lilly's competitor to Novo Nordisk's semaglutide. Approved 2022 for diabetes (Mounjaro), 2023 for obesity (Zepbound). Rapidly capturing market share.",
            
            # ===== CLINICAL TRIAL PHASES =====
            "Clinical trial Phase 1: First-in-human studies testing safety, tolerability, pharmacokinetics (absorption, distribution, metabolism, excretion), and pharmacodynamics. Typically 20-100 healthy volunteers. Duration: several months.",
            "Clinical trial Phase 2: Proof-of-concept and dose-finding studies in patients with target condition. Establishes efficacy signals and optimal dosing. Typically 100-300 patients. Duration: several months to 2 years.",
            "Clinical trial Phase 3: Large-scale pivotal/confirmatory trials comparing to standard of care or placebo. Required for regulatory approval. Typically 300-3000+ patients across multiple sites. Duration: 1-4 years.",
            "Clinical trial Phase 4: Post-marketing surveillance studying long-term safety, real-world effectiveness, new indications, and detecting rare adverse events. Required by regulators, ongoing after approval.",
            
            # ===== REGULATORY PATHWAYS =====
            "FDA Breakthrough Therapy Designation: Expedited development for drugs treating serious conditions with preliminary clinical evidence of substantial improvement over existing therapies. Intensive FDA guidance included.",
            "FDA Priority Review: 6-month review (vs. standard 10-month) for drugs that offer major advances in treatment or provide treatment where no adequate therapy exists. Does not change approval standards.",
            "FDA Accelerated Approval: Based on surrogate endpoints reasonably likely to predict clinical benefit (e.g., tumor shrinkage instead of survival). Requires post-marketing confirmatory trials.",
            "FDA Fast Track Designation: For drugs treating serious conditions and filling unmet medical need. Allows rolling review (submit sections of NDA as completed) and more frequent FDA meetings.",
            "Patent exclusivity in pharmaceuticals: 20 years from filing date. Data exclusivity: 5 years for NCEs in US, 10 years in EU. Biologics: 12 years in US (BPCIA), 10 years in EU.",
            
            # ===== MARKET TRENDS =====
            "Global pharmaceutical market size: Valued at approximately $1.5 trillion in 2023, projected to reach $2.3 trillion by 2028. Growth driven by innovation in biologics, specialty drugs, and emerging markets.",
            "Obesity drug market: Fastest growing pharmaceutical category with 50%+ annual growth. GLP-1 agonists (semaglutide, tirzepatide) driving market. Expected to exceed $100 billion by 2030.",
            "Oncology market: Largest therapeutic category at ~$200 billion annually. Dominated by checkpoint inhibitors (Keytruda, Opdivo), targeted therapies, and emerging cell/gene therapies.",
            "Biosimilars market growth: Biosimilars expected to save $100+ billion in healthcare costs by 2025. Key categories: anti-TNF (Humira biosimilars), oncology supportive care, insulin analogs.",
            "Pharmaceutical R&D spending: Global pharma R&D exceeded $250 billion in 2023. Average cost to develop a new drug: $2.6 billion including failures. Success rate from Phase 1: ~10%.",
        ]
        
        # Generate IDs and metadata
        ids = [f"kb_doc_{i}" for i in range(len(documents))]
        
        metadatas = []
        for doc in documents:
            doc_lower = doc.lower()
            # Auto-categorize based on content
            if "ibuprofen" in doc_lower:
                category = "ibuprofen"
            elif any(word in doc_lower for word in ["aspirin", "acetylsalicylic"]):
                category = "aspirin"
            elif any(word in doc_lower for word in ["semaglutide", "ozempic", "wegovy"]):
                category = "glp1"
            elif any(word in doc_lower for word in ["tirzepatide", "mounjaro", "zepbound"]):
                category = "glp1"
            elif "metformin" in doc_lower:
                category = "diabetes"
            elif any(word in doc_lower for word in ["pembrolizumab", "keytruda", "pd-1", "checkpoint"]):
                category = "immunotherapy"
            elif any(word in doc_lower for word in ["adalimumab", "humira", "tnf"]):
                category = "tnf"
            elif any(word in doc_lower for word in ["atorvastatin", "lipitor", "statin"]):
                category = "cardiovascular"
            elif any(word in doc_lower for word in ["paracetamol", "acetaminophen"]):
                category = "analgesic"
            elif any(word in doc_lower for word in ["clinical trial", "phase"]):
                category = "clinical_trials"
            elif any(word in doc_lower for word in ["fda", "regulatory", "patent", "approval"]):
                category = "regulatory"
            elif any(word in doc_lower for word in ["market", "billion", "sales"]):
                category = "market"
            else:
                category = "general"
            
            metadatas.append({
                "source": "pharma_knowledge_base",
                "category": category,
                "type": "reference"
            })
        
        try:
            # Add in batches to avoid issues
            batch_size = 20
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i+batch_size]
                batch_ids = ids[i:i+batch_size]
                batch_meta = metadatas[i:i+batch_size]
                
                self.collection.add(
                    documents=batch_docs,
                    ids=batch_ids,
                    metadatas=batch_meta
                )
            
            logger.info(f"✅ Seeded {len(documents)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Error seeding data: {str(e)}")
    
    @property
    def is_available(self) -> bool:
        """Check if RAG service is available."""
        return self.collection is not None
    
    async def search(
        self,
        query: str,
        n_results: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents based on query.
        
        Args:
            query: Search query
            n_results: Number of results to return
            category_filter: Optional category to filter by
            
        Returns:
            List of relevant documents with metadata
        """
        if not self.is_available:
            logger.warning("RAG service not available, returning mock results")
            return self._mock_search(query, n_results)
        
        try:
            where_filter = None
            if category_filter:
                where_filter = {"category": category_filter}
            
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
            
            documents = []
            if results and results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    distance = results["distances"][0][i] if results["distances"] else 1.0
                    documents.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": distance,
                        "relevance_score": max(0, 1 - distance)  # Convert distance to similarity
                    })
            
            logger.info(f"🔍 Found {len(documents)} relevant documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"RAG search error: {str(e)}")
            return self._mock_search(query, n_results)
    
    async def search_for_molecule(self, molecule_name: str) -> Dict[str, Any]:
        """
        Search for information about a specific molecule.
        
        Args:
            molecule_name: Name of the molecule/drug
            
        Returns:
            Aggregated information about the molecule
        """
        # Search for various aspects of the molecule
        results = await self.search(molecule_name, n_results=10)
        
        # Aggregate results
        info = {
            "molecule": molecule_name,
            "found_documents": len(results),
            "contexts": [r["content"] for r in results],
            "categories": list(set(r["metadata"].get("category", "unknown") for r in results)),
            "relevance_scores": [r.get("relevance_score", 0) for r in results]
        }
        
        return info
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> bool:
        """
        Add documents to the knowledge base.
        
        Args:
            documents: List of document texts
            metadatas: Optional list of metadata dicts
            ids: Optional list of document IDs
            
        Returns:
            Success status
        """
        if not self.is_available:
            logger.warning("RAG service not available - documents not added")
            return False
        
        try:
            if not ids:
                ids = [str(uuid.uuid4()) for _ in documents]
            
            if not metadatas:
                metadatas = [{"source": "user_upload", "type": "custom"} for _ in documents]
            
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            
            logger.info(f"✅ Added {len(documents)} documents to knowledge base")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False
    
    async def ingest_pdf_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Ingest chunked PDF documents into the knowledge base.
        
        Args:
            chunks: List of chunks with content and metadata
            
        Returns:
            Success status
        """
        if not chunks:
            logger.warning("No chunks to ingest")
            return False
        
        documents = [c["content"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [f"pdf_{uuid.uuid4()}" for _ in chunks]
        
        return await self.add_documents(documents, metadatas, ids)
    
    def _mock_search(self, query: str, n_results: int) -> List[Dict[str, Any]]:
        """Return mock search results for testing."""
        query_lower = query.lower()
        
        # Simple keyword matching for common drugs
        mock_results = []
        
        if "ibuprofen" in query_lower:
            mock_results.append({
                "content": "Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) used to treat pain, fever, and inflammation. Formula: C13H18O2, molecular weight: 206.29 g/mol.",
                "metadata": {"source": "mock", "category": "ibuprofen"},
                "distance": 0.1,
                "relevance_score": 0.9
            })
        elif "aspirin" in query_lower:
            mock_results.append({
                "content": "Aspirin (acetylsalicylic acid) is an NSAID used for pain, fever, inflammation, and cardiovascular protection. Formula: C9H8O4, molecular weight: 180.16 g/mol.",
                "metadata": {"source": "mock", "category": "aspirin"},
                "distance": 0.1,
                "relevance_score": 0.9
            })
        else:
            mock_results.append({
                "content": f"Information about {query} from pharmaceutical knowledge base.",
                "metadata": {"source": "mock", "category": "general"},
                "distance": 0.5,
                "relevance_score": 0.5
            })
        
        return mock_results[:n_results]
    
    async def get_context_for_query(self, query: str, n_results: int = 5) -> str:
        """
        Get relevant context for a query to use in LLM prompts.
        
        Args:
            query: User query
            n_results: Number of results to retrieve
            
        Returns:
            Concatenated relevant context
        """
        results = await self.search(query, n_results=n_results)
        
        if not results:
            return ""
        
        context_parts = []
        for i, result in enumerate(results):
            score = result.get('relevance_score', 0)
            context_parts.append(f"[Source {i+1}] (Relevance: {score:.2f})\n{result['content']}")
        
        return "\n\n".join(context_parts)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        if not self.is_available:
            return {"status": "unavailable", "count": 0}
        
        try:
            count = self.collection.count()
            return {
                "status": "available",
                "count": count,
                "name": "pharma_knowledge",
                "persist_directory": settings.chroma_persist_directory
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def clear_and_rebuild(self) -> bool:
        """Clear the collection and rebuild from scratch."""
        if not self.is_available:
            return False
        
        try:
            # Delete the collection
            self.client.delete_collection("pharma_knowledge")
            
            # Reinitialize
            self._initialize_chromadb()
            
            logger.info("✅ Collection cleared and rebuilt")
            return True
            
        except Exception as e:
            logger.error(f"Error rebuilding collection: {e}")
            return False


# Singleton instance
rag_service = RAGService()
