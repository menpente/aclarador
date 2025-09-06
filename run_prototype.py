#!/usr/bin/env python3
"""
Simple test script to verify the prototype works without full dependencies
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def test_agents():
    """Test agents without external dependencies"""
    print("🤖 Testing agent system...")
    
    try:
        from agent_coordinator import AgentCoordinator
        
        # Initialize coordinator without knowledge base
        coordinator = AgentCoordinator(use_knowledge_base=False)
        
        # Test text
        test_text = "Este texto es muy largo y complejo, tiene más de treinta palabras en esta oración y utiliza vocabulario técnico que que podría ser difícil de entender."
        
        print(f"📝 Texto de prueba: {test_text}")
        print("\n" + "="*50)
        
        # Process text
        results = coordinator.process_text(test_text)
        
        # Display results
        print("📊 RESULTADOS:")
        print(f"✨ Texto corregido: {results['corrected_text']}")
        
        print(f"\n🔍 Análisis:")
        analysis = results.get('analysis', {})
        print(f"   - Tipo: {analysis.get('text_type')}")
        print(f"   - Severidad: {analysis.get('severity_level')}")
        print(f"   - Problemas: {analysis.get('issues_detected')}")
        
        print(f"\n🛠 Mejoras aplicadas ({len(results.get('improvements', []))}):")
        for i, improvement in enumerate(results.get('improvements', []), 1):
            print(f"   {i}. {improvement.get('agent', '').upper()}: {improvement.get('reason', '')}")
            if 'change' in improvement:
                print(f"      Cambio: {improvement['change']}")
        
        print(f"\n✅ Validación:")
        validation = results.get('final_validation', {})
        quality = validation.get('quality_score', 0)
        print(f"   - Puntuación de calidad: {quality:.1%}")
        
        print("\n🎉 ¡Sistema de agentes funcionando correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing agents: {e}")
        return False

def test_basic_imports():
    """Test if basic modules can be imported"""
    print("📦 Testing basic imports...")
    
    try:
        from agents.base_agent import BaseAgent
        from agents.analyzer_agent import AnalyzerAgent
        from agents.grammar_agent import GrammarAgent
        print("✅ Agent modules imported successfully")
        
        from agent_coordinator import AgentCoordinator
        print("✅ Agent coordinator imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Aclarador Prototype")
    print("="*50)
    
    # Test 1: Basic imports
    imports_ok = test_basic_imports()
    
    if imports_ok:
        print("\n" + "="*50)
        # Test 2: Agent functionality
        agents_ok = test_agents()
        
        if agents_ok:
            print("\n" + "="*50)
            print("🎊 PROTOTYPE STATUS: WORKING!")
            print("\n📋 Next steps:")
            print("1. Install dependencies: source venv/bin/activate && pip install -r requirements.txt")
            print("2. Set up knowledge base: python setup_knowledge_base.py")
            print("3. Run enhanced app: streamlit run app_enhanced.py")
        else:
            print("\n❌ Agents not working properly")
    else:
        print("\n❌ Basic imports failed - check file structure")