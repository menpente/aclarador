#!/usr/bin/env python3
"""
Script to test the knowledge base functionality
"""

from knowledge.vector_store import VectorStore
from knowledge.retrieval import KnowledgeRetrieval

def test_knowledge_base():
    """Test the knowledge base setup and functionality"""
    
    print("Testing knowledge base functionality...")
    
    try:
        # Initialize vector store
        vector_store = VectorStore()
        
        # Check if collection exists and has content
        info = vector_store.get_collection_info()
        print(f"Collection info: {info}")
        
        if info['count'] == 0:
            print("Warning: Knowledge base is empty. Run setup_knowledge_base.py first.")
            return False
        
        # Initialize retrieval system
        retrieval = KnowledgeRetrieval(vector_store)
        
        # Test cases
        test_cases = [
            {
                "name": "Grammar guidelines",
                "query": "gramática concordancia verbo",
                "agent_type": "grammar"
            },
            {
                "name": "Style guidelines", 
                "query": "oraciones largas treinta palabras",
                "agent_type": "style"
            },
            {
                "name": "SEO guidelines",
                "query": "internet SEO buscadores",
                "agent_type": "seo"
            }
        ]
        
        print("\nRunning test cases...")
        for test_case in test_cases:
            print(f"\n--- {test_case['name']} ---")
            
            guidelines = retrieval.get_relevant_guidelines(
                text=test_case['query'],
                agent_type=test_case['agent_type'],
                n_results=2
            )
            
            if guidelines:
                for i, guideline in enumerate(guidelines, 1):
                    print(f"  {i}. Page {guideline['page']}, Relevance: {guideline['relevance']:.2f}")
                    print(f"     Preview: {guideline['content'][:150]}...")
            else:
                print("  No guidelines found")
        
        # Test specific principle lookup
        print("\n--- Principle Lookup ---")
        principle = retrieval.get_principle_explanation("one_idea_per_sentence")
        if principle:
            print(f"Found principle explanation from page {principle['page']}")
            print(f"Preview: {principle['content'][:200]}...")
        else:
            print("Principle explanation not found")
        
        print("\nKnowledge base test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing knowledge base: {e}")
        return False

if __name__ == "__main__":
    success = test_knowledge_base()
    
    if success:
        print("\nKnowledge base is working correctly!")
    else:
        print("\nKnowledge base test failed.")
        print("Make sure you've run setup_knowledge_base.py first.")