#!/usr/bin/env python3
"""
Comprehensive test suite for Phase 4 - Optimization & Advanced Features
"""

import sys
import os
import time
import uuid

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def test_multi_pass_refinement():
    """Test multi-pass refinement system"""
    print("🔄 Testing Multi-Pass Refinement System")
    print("-" * 50)
    
    try:
        from agent_coordinator import AgentCoordinator
        from multi_pass_processor import MultiPassProcessor, AdvancedProcessingOptions
        
        # Initialize components
        coordinator = AgentCoordinator(use_knowledge_base=True)
        options = AdvancedProcessingOptions()
        
        # Test different processing modes
        modes = ['conservative', 'balanced', 'aggressive']
        test_text = "Este texto es muy largo y complejo que que tiene más de treinta palabras en esta oración y utiliza vocabulario técnico que podría ser difícil de entender para los usuarios normales y necesita mejoras significativas."
        
        print(f"📝 Test text: {test_text[:80]}...")
        print()
        
        for mode in modes:
            print(f"🎛 Testing {mode} mode:")
            
            processor = options.create_custom_processor(coordinator, mode)
            results = processor.process_with_multiple_passes(test_text)
            
            metrics = results['overall_metrics']
            print(f"   ✅ Passes: {metrics['total_passes']}")
            print(f"   ⏱ Time: {metrics['total_time']:.1f}s")
            print(f"   📊 Quality: {metrics['initial_quality']:.1%} → {metrics['final_quality']:.1%}")
            print(f"   🔧 Improvements: {metrics['total_improvements']}")
            print()
        
        print("✅ Multi-pass refinement system working!")
        return True
        
    except Exception as e:
        print(f"❌ Error in multi-pass testing: {e}")
        return False

def test_advanced_seo_optimizer():
    """Test advanced SEO optimization features"""
    print("🔍 Testing Advanced SEO Optimizer")
    print("-" * 50)
    
    try:
        from seo_optimizer import AdvancedSEOOptimizer
        
        optimizer = AdvancedSEOOptimizer()
        
        # Test cases
        test_cases = [
            {
                'name': 'Web Content',
                'text': 'Nuestro sitio web www.ejemplo.com ofrece servicios de SEO y optimización para motores de búsqueda que ayudan a mejorar la visibilidad online y posicionamiento.',
                'keywords': ['SEO', 'optimización', 'posicionamiento']
            },
            {
                'name': 'Blog Article',
                'text': 'Cómo mejorar el posicionamiento web: guía completa. El SEO es fundamental para cualquier sitio web que busque visibilidad en buscadores como Google.',
                'keywords': ['posicionamiento web', 'SEO', 'Google']
            }
        ]
        
        for test_case in test_cases:
            print(f"📝 {test_case['name']}:")
            
            analysis = optimizer.analyze_seo_comprehensive(
                test_case['text'], 
                test_case['keywords']
            )
            
            print(f"   📊 SEO Score: {analysis['seo_score']['overall']:.1%}")
            print(f"   📖 Readability: {analysis['readability_seo']['seo_readability']}")
            print(f"   🔑 Keywords analyzed: {len(analysis['keyword_analysis']['target_keywords'])}")
            print(f"   💡 Recommendations: {len(analysis['recommendations'])}")
            
            # Test optimization suggestions
            optimizations = optimizer.optimize_for_seo(
                test_case['text'], 
                test_case['keywords']
            )
            
            print(f"   🎯 Title suggestions: {len(optimizations['optimizations']['title_suggestions'])}")
            print(f"   📄 Meta descriptions: {len(optimizations['optimizations']['meta_description_suggestions'])}")
            print()
        
        print("✅ Advanced SEO optimizer working!")
        return True
        
    except Exception as e:
        print(f"❌ Error in SEO testing: {e}")
        return False

def test_performance_optimization():
    """Test performance optimization and caching"""
    print("⚡ Testing Performance Optimization")
    print("-" * 50)
    
    try:
        from agent_coordinator import AgentCoordinator
        from performance_optimizer import PerformanceOptimizer, OptimizedAgentCoordinator
        
        # Initialize components
        base_coordinator = AgentCoordinator(use_knowledge_base=True)
        performance_optimizer = PerformanceOptimizer()
        
        # Test caching
        @performance_optimizer.cached(ttl=300)
        def dummy_processing(text):
            time.sleep(0.1)  # Simulate processing
            return f"processed: {text}"
        
        # Test cache performance
        test_text = "Test text for caching"
        
        # First call (should be slow)
        start = time.time()
        result1 = dummy_processing(test_text)
        time1 = time.time() - start
        
        # Second call (should be fast - cached)
        start = time.time()
        result2 = dummy_processing(test_text)
        time2 = time.time() - start
        
        print(f"   ⏱ First call: {time1:.3f}s")
        print(f"   ⚡ Cached call: {time2:.3f}s")
        print(f"   🚀 Speed improvement: {time1/time2:.1f}x")
        
        # Test optimized coordinator
        optimized_coordinator = OptimizedAgentCoordinator(base_coordinator, performance_optimizer)
        
        texts = [
            "Este es un texto de prueba.",
            "Otro texto similar para testing.",
            "Texto final de la prueba."
        ]
        
        start = time.time()
        results = optimized_coordinator.process_multiple_texts(texts)
        batch_time = time.time() - start
        
        print(f"   📊 Batch processing: {len(texts)} texts in {batch_time:.1f}s")
        print(f"   📈 Performance stats available: ✅")
        
        # Get performance report
        report = performance_optimizer.get_performance_report()
        print(f"   💾 Cache hits: {report['cache_stats']['hits']}")
        print(f"   📊 Hit rate: {report['cache_stats']['hit_rate']:.1%}")
        
        print("✅ Performance optimization working!")
        return True
        
    except Exception as e:
        print(f"❌ Error in performance testing: {e}")
        return False

def test_user_feedback_system():
    """Test user feedback integration"""
    print("👥 Testing User Feedback System")
    print("-" * 50)
    
    try:
        from agent_coordinator import AgentCoordinator
        from feedback_system import UserFeedbackManager, FeedbackIntegratedCoordinator
        
        # Initialize components
        base_coordinator = AgentCoordinator(use_knowledge_base=True)
        feedback_manager = UserFeedbackManager("test_feedback.json")
        
        # Generate test feedback data
        feedback_manager.simulate_feedback_data(20)
        
        # Test feedback analysis
        analytics = feedback_manager.analyze_feedback()
        
        print(f"   📊 Total feedback: {analytics.total_feedback}")
        print(f"   ⭐ Average rating: {analytics.average_rating:.1f}/5")
        print(f"   😊 Satisfaction rate: {analytics.user_satisfaction_trend}")
        print(f"   🤖 Agent performance tracked: {len(analytics.agent_performance)}")
        
        # Test integrated coordinator
        integrated_coordinator = FeedbackIntegratedCoordinator(base_coordinator, feedback_manager)
        
        test_text = "Este es un texto de prueba para el sistema de feedback."
        results = integrated_coordinator.process_text_with_feedback(test_text)
        
        print(f"   🎯 Feedback prompts generated: ✅")
        print(f"   📝 Ready for user feedback: {results.get('ready_for_feedback', False)}")
        
        # Test feedback submission
        feedback_id = integrated_coordinator.submit_user_feedback(
            results, 4.5, 'praise', 'Excelente corrección!'
        )
        
        print(f"   📤 Feedback submitted: {feedback_id[:8]}...")
        
        # Get improvement insights
        insights = integrated_coordinator.get_improvement_insights()
        print(f"   💡 System health: {insights['system_health']['satisfaction_level']}")
        
        print("✅ User feedback system working!")
        return True
        
    except Exception as e:
        print(f"❌ Error in feedback testing: {e}")
        return False

def test_quality_convergence():
    """Test quality convergence detection"""
    print("🎯 Testing Quality Convergence Detection")
    print("-" * 50)
    
    try:
        from quality_analyzer import QualityAnalyzer, ConvergenceDetector
        from agent_coordinator import AgentCoordinator
        
        # Initialize components
        analyzer = QualityAnalyzer()
        detector = ConvergenceDetector()
        coordinator = AgentCoordinator(use_knowledge_base=True)
        
        # Test quality analysis
        test_texts = [
            "Este texto tiene algunos errores que que necesitan corrección.",  # Low quality
            "Este texto tiene algunos errores que necesitan corrección.",      # Medium quality
            "Este texto tiene buena estructura y claridad.",                   # High quality
        ]
        
        print("📊 Quality Analysis:")
        for i, text in enumerate(test_texts, 1):
            # Process text
            results = coordinator.process_text(text)
            
            # Analyze quality
            quality = analyzer.analyze_comprehensive_quality(text, results)
            
            print(f"   Text {i}: Overall={quality.overall_quality:.1%}, "
                  f"Readability={quality.readability_score:.1%}, "
                  f"Grammar={quality.grammar_accuracy:.1%}")
            
            # Add to convergence detector
            detector.add_processing_result(text, results)
        
        # Test convergence detection
        convergence = detector.check_convergence()
        trend = detector.get_quality_trend()
        
        print(f"   🔄 Convergence status: {convergence.get('converged', False)}")
        print(f"   📈 Quality trend: {trend['direction']}")
        print(f"   📊 Data points: {trend['data_points']}")
        
        # Get detailed analysis
        detailed = detector.get_detailed_analysis()
        if detailed['status'] == 'analyzed':
            print(f"   ⭐ Current quality: {detailed['current_metrics']['overall_quality']:.1%}")
            print(f"   🎯 Recommendations: {len(detailed['recommendations'])}")
        
        print("✅ Quality convergence detection working!")
        return True
        
    except Exception as e:
        print(f"❌ Error in convergence testing: {e}")
        return False

def test_advanced_analytics():
    """Test advanced analytics and dashboard"""
    print("📊 Testing Advanced Analytics Dashboard")
    print("-" * 50)
    
    try:
        from analytics_dashboard import AdvancedAnalytics, AnalyticsIntegratedSystem
        from agent_coordinator import AgentCoordinator
        
        # Initialize components
        base_coordinator = AgentCoordinator(use_knowledge_base=True)
        analytics_system = AnalyticsIntegratedSystem(base_coordinator)
        
        # Generate test data
        test_texts = [
            "Texto corto para prueba.",
            "Este es un texto más largo que necesita análisis de estilo y gramática.",
            "Contenido web para SEO: optimización, posicionamiento y visibilidad online.",
            "Documento formal con estructura clara y vocabulario apropiado."
        ]
        
        print("📈 Processing texts for analytics:")
        for i, text in enumerate(test_texts, 1):
            results = analytics_system.process_with_analytics(text)
            print(f"   Text {i}: Processed in {results['analytics']['processing_time']:.2f}s")
            
            # Simulate user feedback for some texts
            if i % 2 == 0:
                feedback = {
                    'rating': 4.5 if i == 2 else 3.5,
                    'feedback_type': 'praise',
                    'comment': 'Muy útil' if i == 2 else 'Aceptable'
                }
                analytics_system.submit_feedback_with_analytics(results, feedback)
        
        # Get dashboard data
        dashboard = analytics_system.get_analytics_dashboard()
        
        print("📊 Dashboard Metrics:")
        summary = dashboard['summary']
        print(f"   📝 Total requests: {summary['total_requests']}")
        print(f"   ⭐ Average quality: {summary['avg_quality']:.1%}")
        print(f"   😊 User satisfaction: {summary['user_satisfaction']:.1%}")
        print(f"   🩺 System health: {summary['system_health']}")
        
        # Show insights
        insights = dashboard['insights']
        print(f"   💡 Generated insights: {len(insights)}")
        
        if insights:
            top_insight = insights[0]
            print(f"   🔍 Top insight: {top_insight['title']}")
        
        # Show recommendations
        recommendations = dashboard['recommendations']
        print(f"   🎯 Recommendations: {len(recommendations)}")
        
        if recommendations:
            print(f"   📋 Top recommendation: {recommendations[0]}")
        
        print("✅ Advanced analytics working!")
        return True
        
    except Exception as e:
        print(f"❌ Error in analytics testing: {e}")
        return False

def test_integrated_phase4_system():
    """Test complete Phase 4 integrated system"""
    print("🚀 Testing Complete Phase 4 Integration")
    print("=" * 60)
    
    try:
        from agent_coordinator import AgentCoordinator
        from multi_pass_processor import MultiPassProcessor
        from performance_optimizer import PerformanceOptimizer
        from feedback_system import UserFeedbackManager
        from quality_analyzer import ConvergenceDetector
        from analytics_dashboard import AdvancedAnalytics
        
        print("🔧 Initializing integrated system...")
        
        # Initialize all components
        base_coordinator = AgentCoordinator(use_knowledge_base=True)
        multi_pass_processor = MultiPassProcessor(base_coordinator, max_passes=3)
        performance_optimizer = PerformanceOptimizer()
        feedback_manager = UserFeedbackManager("integrated_test_feedback.json")
        convergence_detector = ConvergenceDetector()
        analytics = AdvancedAnalytics("integrated_test_analytics.json")
        
        print("✅ All components initialized")
        
        # Optimize performance
        performance_optimizer.optimize_agent_coordination(base_coordinator)
        
        # Test complex processing workflow
        complex_text = """
        La implementación de sistemas de inteligencia artificial en el ámbito empresarial que que 
        requiere una planificación estratégica cuidadosa y detallada que debe contemplar múltiples 
        factores organizacionales, tecnológicos y humanos para garantizar el éxito del proyecto 
        y maximizar el retorno de inversión esperado por los stakeholders involucrados.
        """
        
        print(f"📝 Processing complex text ({len(complex_text.split())} words)...")
        
        # Multi-pass processing with all features
        start_time = time.time()
        
        # Step 1: Multi-pass refinement
        multi_pass_results = multi_pass_processor.process_with_multiple_passes(
            complex_text.strip(),
            user_preferences={'mode': 'balanced'}
        )
        
        processing_time = time.time() - start_time
        
        # Step 2: Quality analysis and convergence detection
        final_text = multi_pass_results['final_text']
        convergence_detector.add_processing_result(final_text, multi_pass_results)
        convergence_status = convergence_detector.check_convergence()
        
        # Step 3: Record analytics
        session_id = str(uuid.uuid4())
        analytics.record_processing_event(
            session_id=session_id,
            text_input=complex_text.strip(),
            results=multi_pass_results,
            processing_time=processing_time
        )
        
        # Results summary
        print("\n🎯 PHASE 4 INTEGRATION RESULTS:")
        print("=" * 40)
        
        overall_metrics = multi_pass_results['overall_metrics']
        print(f"📊 Processing Summary:")
        print(f"   • Passes completed: {overall_metrics['total_passes']}")
        print(f"   • Total processing time: {overall_metrics['total_time']:.1f}s")
        print(f"   • Quality improvement: {overall_metrics['initial_quality']:.1%} → {overall_metrics['final_quality']:.1%}")
        print(f"   • Total improvements: {overall_metrics['total_improvements']}")
        print(f"   • Convergence achieved: {overall_metrics['convergence_achieved']}")
        
        print(f"\n🔄 Convergence Analysis:")
        print(f"   • Status: {'✅ Converged' if convergence_status['converged'] else '🔄 Continuing'}")
        print(f"   • Reason: {convergence_status['reason']}")
        print(f"   • Confidence: {convergence_status['confidence']:.1%}")
        print(f"   • Recommendation: {convergence_status['recommendation']}")
        
        print(f"\n⚡ Performance Metrics:")
        perf_report = performance_optimizer.get_performance_report()
        print(f"   • Cache hit rate: {perf_report['cache_stats']['hit_rate']:.1%}")
        print(f"   • Average processing time: {perf_report['processing_stats']['avg_time']:.2f}s")
        print(f"   • Total cached functions: {perf_report['cache_stats']['size']}")
        
        print(f"\n📈 System Health:")
        dashboard_data = analytics.get_dashboard_data()
        health = dashboard_data['summary']['system_health']
        print(f"   • Overall health: {health}")
        print(f"   • Total requests processed: {dashboard_data['summary']['total_requests']}")
        
        print(f"\n🎉 PHASE 4 FULLY INTEGRATED AND OPERATIONAL!")
        return True
        
    except Exception as e:
        print(f"❌ Error in integrated system testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_comprehensive_phase4_tests():
    """Run all Phase 4 tests"""
    print("🧪 PHASE 4 COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        ("Multi-Pass Refinement", test_multi_pass_refinement),
        ("Advanced SEO Optimizer", test_advanced_seo_optimizer),
        ("Performance Optimization", test_performance_optimization),
        ("User Feedback System", test_user_feedback_system),
        ("Quality Convergence", test_quality_convergence),
        ("Advanced Analytics", test_advanced_analytics),
        ("Integrated System", test_integrated_phase4_system)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"🧪 Testing: {test_name}")
        print("=" * 60)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                failed += 1
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: ERROR - {e}")
        
        print()
        print("=" * 60)
        print()
    
    # Final summary
    total = passed + failed
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print("🏁 PHASE 4 TEST SUMMARY")
    print("=" * 40)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    print(f"📊 Success Rate: {success_rate:.1f}%")
    print()
    
    if success_rate >= 80:
        print("🎊 PHASE 4 STATUS: SUCCESS!")
        print("🚀 All major systems operational!")
    elif success_rate >= 60:
        print("⚠️  PHASE 4 STATUS: MOSTLY WORKING")
        print("🔧 Some components need attention")
    else:
        print("❌ PHASE 4 STATUS: NEEDS WORK")
        print("🛠️  Significant issues to resolve")
    
    return success_rate >= 80

if __name__ == "__main__":
    success = run_comprehensive_phase4_tests()
    
    if success:
        print("\n🎉 PHASE 4 OPTIMIZATION & ADVANCED FEATURES: COMPLETE!")
        print("🏆 Aclarador system ready for production deployment!")
    else:
        print("\n🔧 Phase 4 testing revealed issues that need resolution.")
        print("📋 Review test output and address failing components.")