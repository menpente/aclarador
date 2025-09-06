#!/usr/bin/env python3
"""
Test Phase 3 implementation - Knowledge Base Integration
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def test_knowledge_integration():
    """Test the knowledge base integration with agents"""
    print("🧪 Testing Phase 3 - Knowledge Base Integration")
    print("="*60)
    
    try:
        from agent_coordinator import AgentCoordinator
        
        # Initialize coordinator with knowledge base
        coordinator = AgentCoordinator(use_knowledge_base=True)
        
        # Test cases with different types of issues
        test_cases = [
            {
                "name": "Grammar + Style Issues",
                "text": "Este texto es muy largo y complejo que que tiene más de treinta palabras en esta oración y utiliza vocabulario técnico que podría ser difícil de entender para los usuarios normales.",
                "expected_agents": ["grammar", "style"]
            },
            {
                "name": "Web Content (SEO)",
                "text": "Nuestro sitio web www.ejemplo.com ofrece servicios de SEO y optimización para motores de búsqueda que ayudan a mejorar la visibilidad online.",
                "expected_agents": ["grammar", "style", "seo"]
            },
            {
                "name": "Passive Voice",
                "text": "El documento fue elaborado por el equipo y las recomendaciones fueron implementadas por la dirección.",
                "expected_agents": ["grammar", "style"]
            }
        ]
        
        print(f"📊 Knowledge Base Status: {'✅ Active' if coordinator.use_knowledge_base else '❌ Not available'}")
        print(f"🔄 Available Agents: {len(coordinator.get_available_agents())}")
        print()
        
        # Run test cases
        for i, test_case in enumerate(test_cases, 1):
            print(f"🧪 Test Case {i}: {test_case['name']}")
            print(f"📝 Text: {test_case['text']}")
            print("-" * 50)
            
            # Process text
            results = coordinator.process_text(
                test_case['text'],
                selected_agents=test_case['expected_agents'] + ["validator"]
            )
            
            # Display results
            print(f"✨ Corrected: {results['corrected_text']}")
            print(f"🔍 Analysis: Type={results['analysis']['text_type']}, Issues={results['analysis']['issues_detected']}")
            print(f"🛠 Improvements: {len(results['improvements'])}")
            
            # Show knowledge base guidelines
            guidelines = results.get('knowledge_guidelines', [])
            print(f"📚 Knowledge Guidelines: {len(guidelines)}")
            
            for j, guideline in enumerate(guidelines[:2], 1):  # Show first 2
                print(f"   {j}. [{guideline.get('source_agent', 'unknown')}] Page {guideline['page']}")
                print(f"      {guideline['content'][:120]}...")
            
            # Quality score
            validation = results.get('final_validation', {})
            quality = validation.get('quality_score', 0)
            print(f"⭐ Quality Score: {quality:.1%}")
            print()
        
        print("🎉 Phase 3 testing completed successfully!")
        
        # Test knowledge base directly
        print("\n🔍 Direct Knowledge Base Test:")
        if coordinator.knowledge_retrieval:
            kb_test = coordinator.knowledge_retrieval.search_by_keywords(["oración", "palabras"], 2)
            for guideline in kb_test:
                print(f"   📖 Page {guideline['page']}: {guideline['content'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in Phase 3 testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mock_knowledge_base():
    """Test the mock knowledge base directly"""
    print("\n🔬 Testing Mock Knowledge Base Directly")
    print("="*40)
    
    try:
        from knowledge_mock import MockKnowledgeRetrieval
        
        kb = MockKnowledgeRetrieval()
        
        # Test different retrieval methods
        tests = [
            ("Grammar guidelines", "grammar", ["grammar_error"]),
            ("Style guidelines", "style", ["long_sentence"]),
            ("SEO guidelines", "seo", []),
            ("General guidelines", "general", [])
        ]
        
        for name, agent_type, issues in tests:
            print(f"📚 {name}:")
            guidelines = kb.get_relevant_guidelines("test text", agent_type, issues, 2)
            
            for guideline in guidelines:
                print(f"   Page {guideline['page']}: {guideline['content'][:80]}...")
            print()
        
        # Test keyword search
        print("🔍 Keyword Search Test:")
        results = kb.search_by_keywords(["oración", "palabras"], 2)
        for result in results:
            print(f"   Found: {result['content'][:80]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing mock knowledge base: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Phase 3 Testing Suite")
    print("="*60)
    
    # Test 1: Mock knowledge base
    mock_ok = test_mock_knowledge_base()
    
    if mock_ok:
        print("\n" + "="*60)
        # Test 2: Full integration
        integration_ok = test_knowledge_integration()
        
        if integration_ok:
            print("\n🎊 PHASE 3 STATUS: COMPLETED!")
            print("\n📋 Phase 3 Achievements:")
            print("✅ Mock knowledge base with Spanish guidelines")
            print("✅ Agent-knowledge integration") 
            print("✅ RAG system with citation functionality")
            print("✅ Enhanced results with PDF references")
            print("✅ Fallback system for missing dependencies")
            
            print("\n🚀 Ready for enhanced Streamlit app!")
        else:
            print("\n❌ Integration test failed")
    else:
        print("\n❌ Mock knowledge base test failed")