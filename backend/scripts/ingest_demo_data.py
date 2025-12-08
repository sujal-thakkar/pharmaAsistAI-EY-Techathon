"""
Demo data ingestion script - Loads sample pharmaceutical data into the knowledge base.
This provides realistic search results even without actual PDFs.
Run this to populate the knowledge base for demo purposes.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rag_service import rag_service


# Sample pharmaceutical knowledge for common drugs
DEMO_KNOWLEDGE = [
    # Ibuprofen
    {
        "content": """Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) with analgesic and antipyretic properties. 
        Chemical Formula: C13H18O2. Molecular Weight: 206.29 g/mol. CAS Number: 15687-27-1.
        Mechanism of Action: Ibuprofen works by inhibiting cyclooxygenase (COX-1 and COX-2) enzymes, which reduces prostaglandin 
        synthesis and thereby decreases inflammation, pain, and fever. FDA approved in 1974.
        Therapeutic Class: NSAID, Analgesic, Antipyretic.
        Common Brand Names: Advil, Motrin, Nurofen.
        Indications: Mild to moderate pain, fever reduction, rheumatoid arthritis, osteoarthritis, dysmenorrhea.""",
        "metadata": {"source": "drug_monograph", "category": "nsaid", "drug": "ibuprofen"}
    },
    {
        "content": """Ibuprofen Clinical Trials Summary: Over 400 clinical trials have been conducted on ibuprofen globally.
        Key findings include effectiveness in post-operative pain management, dental pain, and headache relief.
        Cardiovascular Safety: Long-term high-dose use may increase cardiovascular risk. FDA black box warning applies.
        GI Safety: Risk of gastrointestinal bleeding, especially in elderly patients or with concurrent corticosteroid use.
        Drug Interactions: NSAIDs may reduce the antihypertensive effect of ACE inhibitors and increase lithium levels.""",
        "metadata": {"source": "clinical_data", "category": "clinical_trials", "drug": "ibuprofen"}
    },
    
    # Aspirin
    {
        "content": """Aspirin (Acetylsalicylic Acid) is one of the most widely used medications globally.
        Chemical Formula: C9H8O4. Molecular Weight: 180.16 g/mol. CAS Number: 50-78-2.
        Mechanism: Irreversibly inhibits COX-1 and COX-2, blocking prostaglandin and thromboxane synthesis.
        Unique Property: Antiplatelet effect lasts for the lifetime of the platelet (7-10 days).
        FDA approved since 1899 (one of the oldest synthetic drugs).
        Indications: Pain relief, fever reduction, anti-inflammatory, cardiovascular prevention, stroke prevention.""",
        "metadata": {"source": "drug_monograph", "category": "nsaid", "drug": "aspirin"}
    },
    
    # Semaglutide
    {
        "content": """Semaglutide is a glucagon-like peptide-1 (GLP-1) receptor agonist.
        Chemical Formula: C187H291N45O59. Molecular Weight: 4113.58 g/mol.
        Brand Names: Ozempic (diabetes), Wegovy (obesity), Rybelsus (oral form).
        Mechanism: Activates GLP-1 receptors, enhancing glucose-dependent insulin secretion, suppressing glucagon,
        slowing gastric emptying, and reducing appetite through central nervous system effects.
        FDA Approvals: Ozempic (2017), Rybelsus (2019), Wegovy (2021).
        Clinical Impact: SUSTAIN and STEP trial programs showed significant HbA1c reduction and weight loss.""",
        "metadata": {"source": "drug_monograph", "category": "glp1_agonist", "drug": "semaglutide"}
    },
    {
        "content": """Semaglutide Market Analysis 2024:
        Global GLP-1 market size: $25 billion (2024), projected $50 billion by 2030.
        Novo Nordisk market share: 65% of GLP-1 market.
        Key competitors: Eli Lilly (Tirzepatide/Mounjaro), Pfizer (danuglipron in development).
        Supply constraints have limited market penetration. Manufacturing expansion underway.
        Obesity indication driving majority of new prescriptions. Insurance coverage varies.""",
        "metadata": {"source": "market_analysis", "category": "market_data", "drug": "semaglutide"}
    },
    
    # Pembrolizumab
    {
        "content": """Pembrolizumab (Keytruda) is a humanized monoclonal antibody targeting PD-1.
        Mechanism: Blocks PD-1/PD-L1 interaction, releasing T-cell inhibition and enabling immune-mediated tumor destruction.
        Chemical Class: IgG4 kappa immunoglobulin.
        FDA Approvals: Melanoma (2014), NSCLC (2015), Head and Neck Cancer (2016), and 20+ additional indications.
        Merck's blockbuster drug with annual sales exceeding $25 billion.
        Clinical Trials: KEYNOTE program encompasses over 1,500 clinical trials worldwide.""",
        "metadata": {"source": "drug_monograph", "category": "immunotherapy", "drug": "pembrolizumab"}
    },
    
    # Metformin
    {
        "content": """Metformin is the first-line treatment for Type 2 Diabetes Mellitus.
        Chemical Formula: C4H11N5. Molecular Weight: 129.16 g/mol. CAS Number: 657-24-9.
        Mechanism: Decreases hepatic glucose production, increases insulin sensitivity, reduces intestinal glucose absorption.
        FDA approved in 1994 (used in Europe since 1957).
        Brand Names: Glucophage, Fortamet, Glumetza.
        Off-label uses: PCOS, weight management, anti-aging research (TAME trial).
        Safety: Low risk of hypoglycemia, lactic acidosis rare but serious risk.""",
        "metadata": {"source": "drug_monograph", "category": "antidiabetic", "drug": "metformin"}
    },
    
    # Adalimumab
    {
        "content": """Adalimumab (Humira) is a fully human monoclonal antibody targeting TNF-alpha.
        Mechanism: Binds to TNF-alpha, preventing its interaction with p55 and p75 cell surface TNF receptors.
        FDA approved in 2002 for rheumatoid arthritis.
        Indications: RA, Psoriatic Arthritis, Ankylosing Spondylitis, Crohn's Disease, Ulcerative Colitis, Plaque Psoriasis.
        Was the world's best-selling drug (2012-2022) with peak sales of $21 billion annually.
        Biosimilars now available: Hadlima, Hyrimoz, Cyltezo, Amjevita.""",
        "metadata": {"source": "drug_monograph", "category": "tnf_inhibitor", "drug": "adalimumab"}
    },
    
    # Paracetamol/Acetaminophen
    {
        "content": """Paracetamol (Acetaminophen) is a widely used analgesic and antipyretic.
        Chemical Formula: C8H9NO2. Molecular Weight: 151.16 g/mol. CAS Number: 103-90-2.
        Brand Names: Tylenol, Panadol, Calpol.
        Mechanism: Central inhibition of COX enzymes and activation of descending serotonergic pathways.
        Unlike NSAIDs, has minimal anti-inflammatory effect and does not affect platelet function.
        Hepatotoxicity: Overdose causes severe liver damage; N-acetylcysteine is the antidote.
        Maximum daily dose: 4g in healthy adults, lower in hepatic impairment.""",
        "metadata": {"source": "drug_monograph", "category": "analgesic", "drug": "paracetamol"}
    },
    
    # Atorvastatin
    {
        "content": """Atorvastatin (Lipitor) is an HMG-CoA reductase inhibitor (statin).
        Chemical Formula: C33H35FN2O5. Molecular Weight: 558.64 g/mol.
        Mechanism: Inhibits HMG-CoA reductase, reducing hepatic cholesterol synthesis and increasing LDL receptor expression.
        FDA approved in 1996. Was the best-selling drug globally for many years.
        Indications: Hypercholesterolemia, mixed dyslipidemia, cardiovascular risk reduction.
        Clinical Evidence: ASCOT-LLA, CARDS, TNT trials demonstrated cardiovascular benefits.
        Patent expired 2011; multiple generics available.""",
        "metadata": {"source": "drug_monograph", "category": "statin", "drug": "atorvastatin"}
    },
    
    # Tirzepatide
    {
        "content": """Tirzepatide (Mounjaro, Zepbound) is a dual GIP/GLP-1 receptor agonist.
        First-in-class dual incretin agonist developed by Eli Lilly.
        Mechanism: Activates both GIP and GLP-1 receptors, providing synergistic effects on glucose control and weight loss.
        Clinical Results: SURPASS trials showed superior HbA1c reduction vs semaglutide.
        Weight Loss: SURMOUNT trials showed up to 22.5% body weight reduction.
        FDA Approvals: Mounjaro (diabetes, 2022), Zepbound (obesity, 2023).
        Market Competition: Direct competitor to Novo Nordisk's Wegovy.""",
        "metadata": {"source": "drug_monograph", "category": "dual_incretin", "drug": "tirzepatide"}
    },
]


async def ingest_demo_data():
    print("\n" + "="*60)
    print("🧪 PharmaAssist AI - Demo Data Ingestion")
    print("="*60)
    
    # Check current status
    stats = rag_service.get_collection_stats()
    print(f"\n📊 Current knowledge base: {stats.get('count', 0)} documents")
    
    # Prepare documents and metadata
    documents = [item["content"] for item in DEMO_KNOWLEDGE]
    metadatas = [item["metadata"] for item in DEMO_KNOWLEDGE]
    
    print(f"\n📥 Ingesting {len(documents)} demo documents...")
    
    # Add to knowledge base
    success = await rag_service.add_documents(documents, metadatas)
    
    if success:
        print("✅ Demo data ingested successfully!")
        
        # Verify
        new_stats = rag_service.get_collection_stats()
        print(f"\n📊 Updated knowledge base: {new_stats.get('count', 0)} documents")
        
        # Test search
        print("\n🔍 Testing search queries...")
        test_queries = [
            ("ibuprofen mechanism", "ibuprofen"),
            ("semaglutide market size", "semaglutide"),
            ("pembrolizumab indication", "pembrolizumab"),
        ]
        
        for query, expected_drug in test_queries:
            results = await rag_service.search(query, n_results=1)
            if results:
                found_drug = results[0].get("metadata", {}).get("drug", "unknown")
                score = results[0].get("relevance_score", 0)
                status = "✅" if found_drug == expected_drug else "⚠️"
                print(f"   {status} '{query}' -> {found_drug} (score: {score:.2f})")
            else:
                print(f"   ❌ '{query}' -> No results")
    else:
        print("❌ Failed to ingest demo data")
    
    print("\n" + "="*60)
    print("✨ Demo data ready! Your app is now populated for demo.")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(ingest_demo_data())
