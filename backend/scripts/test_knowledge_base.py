"""
Quick test script for PDF ingestion and knowledge base.
Run this after adding PDFs to data/pdfs/ folder.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.pdf_service import pdf_service
from app.services.rag_service import rag_service


async def test_knowledge_base():
    print("\n" + "="*60)
    print("🧪 PharmaAssist AI - Knowledge Base Test")
    print("="*60)
    
    # 1. Check PDFs in directory
    print("\n📁 Checking PDF directory...")
    pdfs = pdf_service.list_pdfs()
    if pdfs:
        print(f"   Found {len(pdfs)} PDFs:")
        for pdf in pdfs:
            print(f"   - {pdf['name']} ({pdf['size_mb']} MB)")
    else:
        print("   ⚠️  No PDFs found in data/pdfs/")
        print("   Add PDF files and run this script again.")
    
    # 2. Check vector store status
    print("\n🗄️  Checking vector store...")
    stats = rag_service.get_collection_stats()
    print(f"   Status: {stats.get('status', 'unknown')}")
    print(f"   Documents: {stats.get('count', 0)}")
    
    # 3. Ingest PDFs if any exist
    if pdfs:
        print("\n📥 Ingesting PDFs into vector store...")
        chunks = pdf_service.process_all_pdfs()
        if chunks:
            print(f"   Created {len(chunks)} chunks")
            success = await rag_service.ingest_pdf_chunks(chunks)
            if success:
                print("   ✅ Successfully ingested into vector store!")
            else:
                print("   ❌ Ingestion failed")
        else:
            print("   ⚠️  No chunks extracted from PDFs")
    
    # 4. Test search
    print("\n🔍 Testing search...")
    test_queries = ["ibuprofen", "clinical trial", "mechanism of action"]
    for query in test_queries:
        results = await rag_service.search(query, n_results=2)
        print(f"   Query: '{query}' -> {len(results)} results")
        if results and results[0].get("relevance_score", 0) > 0.3:
            print(f"      Top result: {results[0]['content'][:80]}...")
    
    # 5. Final stats
    print("\n📊 Final Knowledge Base Status:")
    final_stats = rag_service.get_collection_stats()
    print(f"   Total documents: {final_stats.get('count', 0)}")
    print(f"   Status: {final_stats.get('status', 'unknown')}")
    
    print("\n" + "="*60)
    print("✨ Test Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_knowledge_base())
