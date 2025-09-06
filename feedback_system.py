"""
User feedback integration system for continuous improvement
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
import os

@dataclass
class UserFeedback:
    """Represents user feedback on text processing results"""
    id: str
    session_id: str
    original_text: str
    processed_text: str
    user_rating: float  # 1-5 scale
    feedback_type: str  # 'correction', 'suggestion', 'complaint', 'praise'
    specific_feedback: str
    agent_used: List[str]
    processing_time: float
    timestamp: float
    user_corrections: Optional[Dict[str, str]] = None  # User's manual corrections
    improvement_areas: Optional[List[str]] = None  # Areas user wants improved

@dataclass
class FeedbackAnalytics:
    """Analytics derived from user feedback"""
    total_feedback: int
    average_rating: float
    rating_distribution: Dict[str, int]
    common_complaints: List[Dict[str, Any]]
    improvement_suggestions: List[Dict[str, Any]]
    agent_performance: Dict[str, Dict[str, float]]
    user_satisfaction_trend: List[Dict[str, Any]]

class UserFeedbackManager:
    """Manages collection and analysis of user feedback"""
    
    def __init__(self, feedback_file: str = "feedback_data.json"):
        self.feedback_file = feedback_file
        self.feedback_data: List[UserFeedback] = []
        self.load_feedback_data()
        
        # Feedback categories for analysis
        self.feedback_categories = {
            'grammar_accuracy': ['gramática', 'concordancia', 'ortografía', 'acentos'],
            'style_improvement': ['estilo', 'claridad', 'oraciones', 'legibilidad'],
            'seo_optimization': ['seo', 'keywords', 'títulos', 'meta'],
            'overall_quality': ['calidad', 'resultado', 'general', 'satisfecho'],
            'performance': ['velocidad', 'tiempo', 'lento', 'rápido'],
            'usability': ['interfaz', 'fácil', 'difícil', 'confuso']
        }
    
    def collect_feedback(self, 
                        session_id: str,
                        original_text: str,
                        processed_text: str,
                        user_rating: float,
                        feedback_type: str,
                        specific_feedback: str,
                        agent_used: List[str],
                        processing_time: float,
                        user_corrections: Optional[Dict[str, str]] = None,
                        improvement_areas: Optional[List[str]] = None) -> str:
        """Collect user feedback"""
        
        feedback_id = str(uuid.uuid4())
        
        feedback = UserFeedback(
            id=feedback_id,
            session_id=session_id,
            original_text=original_text,
            processed_text=processed_text,
            user_rating=user_rating,
            feedback_type=feedback_type,
            specific_feedback=specific_feedback,
            agent_used=agent_used,
            processing_time=processing_time,
            timestamp=time.time(),
            user_corrections=user_corrections,
            improvement_areas=improvement_areas
        )
        
        self.feedback_data.append(feedback)
        self.save_feedback_data()
        
        print(f"Feedback collected: {feedback_id}")
        return feedback_id
    
    def get_feedback_prompt(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate interactive feedback prompts based on results"""
        
        prompts = {
            'rating_question': '¿Qué tan satisfecho está con el resultado? (1-5 estrellas)',
            'quality_questions': [],
            'specific_areas': [],
            'improvement_suggestions': []
        }
        
        # Generate specific questions based on what was processed
        improvements = results.get('improvements', [])
        
        if any(imp.get('agent') == 'grammar' for imp in improvements):
            prompts['quality_questions'].append({
                'area': 'grammar',
                'question': '¿Las correcciones gramaticales son apropiadas?',
                'options': ['Todas correctas', 'Mayormente correctas', 'Algunas correctas', 'Pocas correctas', 'Ninguna correcta']
            })
        
        if any(imp.get('agent') == 'style' for imp in improvements):
            prompts['quality_questions'].append({
                'area': 'style',
                'question': '¿Las sugerencias de estilo mejoran la claridad?',
                'options': ['Mucho', 'Bastante', 'Algo', 'Poco', 'Nada']
            })
        
        if any(imp.get('agent') == 'seo' for imp in improvements):
            prompts['quality_questions'].append({
                'area': 'seo',
                'question': '¿Las optimizaciones SEO son útiles?',
                'options': ['Muy útiles', 'Útiles', 'Algo útiles', 'Poco útiles', 'No útiles']
            })
        
        # Suggest specific improvement areas
        prompts['specific_areas'] = [
            'Precisión en correcciones gramaticales',
            'Claridad de las explicaciones',
            'Velocidad de procesamiento',
            'Interfaz de usuario',
            'Calidad de sugerencias de estilo',
            'Utilidad de referencias al manual'
        ]
        
        return prompts
    
    def analyze_feedback(self, days_back: int = 30) -> FeedbackAnalytics:
        """Analyze collected feedback"""
        
        # Filter recent feedback
        cutoff_time = time.time() - (days_back * 24 * 3600)
        recent_feedback = [f for f in self.feedback_data if f.timestamp >= cutoff_time]
        
        if not recent_feedback:
            return FeedbackAnalytics(
                total_feedback=0,
                average_rating=0,
                rating_distribution={},
                common_complaints=[],
                improvement_suggestions=[],
                agent_performance={},
                user_satisfaction_trend=[]
            )
        
        # Calculate basic metrics
        total_feedback = len(recent_feedback)
        average_rating = sum(f.user_rating for f in recent_feedback) / total_feedback
        
        # Rating distribution
        rating_dist = defaultdict(int)
        for feedback in recent_feedback:
            rating_dist[str(int(feedback.user_rating))] += 1
        
        # Analyze common complaints and suggestions
        complaints = self._categorize_feedback(recent_feedback, ['complaint', 'suggestion'])
        
        # Agent performance analysis
        agent_performance = self._analyze_agent_performance(recent_feedback)
        
        # Satisfaction trend (weekly)
        trend = self._calculate_satisfaction_trend(recent_feedback, days_back)
        
        return FeedbackAnalytics(
            total_feedback=total_feedback,
            average_rating=average_rating,
            rating_distribution=dict(rating_dist),
            common_complaints=complaints['complaints'],
            improvement_suggestions=complaints['suggestions'],
            agent_performance=agent_performance,
            user_satisfaction_trend=trend
        )
    
    def _categorize_feedback(self, feedback_list: List[UserFeedback], types: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize feedback by type and content"""
        
        categorized = {'complaints': [], 'suggestions': []}
        
        for feedback in feedback_list:
            if feedback.feedback_type not in types:
                continue
            
            # Categorize by content
            feedback_lower = feedback.specific_feedback.lower()
            categories = []
            
            for category, keywords in self.feedback_categories.items():
                if any(keyword in feedback_lower for keyword in keywords):
                    categories.append(category)
            
            feedback_item = {
                'text': feedback.specific_feedback,
                'rating': feedback.user_rating,
                'categories': categories,
                'timestamp': feedback.timestamp,
                'agents_used': feedback.agent_used
            }
            
            if feedback.feedback_type == 'complaint':
                categorized['complaints'].append(feedback_item)
            elif feedback.feedback_type == 'suggestion':
                categorized['suggestions'].append(feedback_item)
        
        # Sort by frequency and impact
        for category in categorized:
            categorized[category].sort(key=lambda x: x['rating'])  # Low ratings first for complaints
        
        return categorized
    
    def _analyze_agent_performance(self, feedback_list: List[UserFeedback]) -> Dict[str, Dict[str, float]]:
        """Analyze performance of individual agents based on feedback"""
        
        agent_metrics = defaultdict(lambda: {'ratings': [], 'count': 0})
        
        for feedback in feedback_list:
            for agent in feedback.agent_used:
                agent_metrics[agent]['ratings'].append(feedback.user_rating)
                agent_metrics[agent]['count'] += 1
        
        # Calculate metrics for each agent
        performance = {}
        for agent, data in agent_metrics.items():
            if data['count'] > 0:
                performance[agent] = {
                    'average_rating': sum(data['ratings']) / len(data['ratings']),
                    'total_usage': data['count'],
                    'satisfaction_rate': len([r for r in data['ratings'] if r >= 4]) / len(data['ratings']),
                    'complaint_rate': len([r for r in data['ratings'] if r <= 2]) / len(data['ratings'])
                }
        
        return performance
    
    def _calculate_satisfaction_trend(self, feedback_list: List[UserFeedback], days_back: int) -> List[Dict[str, Any]]:
        """Calculate satisfaction trend over time"""
        
        # Group feedback by week
        weekly_data = defaultdict(list)
        
        for feedback in feedback_list:
            # Calculate week number
            feedback_date = datetime.fromtimestamp(feedback.timestamp)
            week_start = feedback_date - timedelta(days=feedback_date.weekday())
            week_key = week_start.strftime('%Y-%W')
            
            weekly_data[week_key].append(feedback.user_rating)
        
        # Calculate weekly averages
        trend = []
        for week, ratings in sorted(weekly_data.items()):
            trend.append({
                'week': week,
                'average_rating': sum(ratings) / len(ratings),
                'feedback_count': len(ratings),
                'satisfaction_rate': len([r for r in ratings if r >= 4]) / len(ratings)
            })
        
        return trend
    
    def get_improvement_recommendations(self) -> List[Dict[str, Any]]:
        """Get recommendations for system improvements based on feedback"""
        
        analytics = self.analyze_feedback()
        recommendations = []
        
        # Low rating analysis
        if analytics.average_rating < 3.5:
            recommendations.append({
                'priority': 'high',
                'area': 'overall_quality',
                'recommendation': f'Puntuación promedio baja ({analytics.average_rating:.1f}). Revisar calidad general del sistema.',
                'suggested_actions': [
                    'Revisar precisión de correcciones automáticas',
                    'Mejorar explicaciones de cambios',
                    'Actualizar base de conocimientos'
                ]
            })
        
        # Agent-specific recommendations
        for agent, metrics in analytics.agent_performance.items():
            if metrics['complaint_rate'] > 0.3:  # More than 30% complaints
                recommendations.append({
                    'priority': 'medium',
                    'area': f'agent_{agent}',
                    'recommendation': f'Alto índice de quejas para agente {agent} ({metrics["complaint_rate"]:.1%})',
                    'suggested_actions': [
                        f'Revisar reglas del agente {agent}',
                        'Analizar casos específicos de error',
                        'Actualizar algoritmos de detección'
                    ]
                })
        
        # Common complaint categories
        common_categories = defaultdict(int)
        for complaint in analytics.common_complaints:
            for category in complaint['categories']:
                common_categories[category] += 1
        
        for category, count in common_categories.items():
            if count >= 3:  # At least 3 complaints in this category
                recommendations.append({
                    'priority': 'medium',
                    'area': category,
                    'recommendation': f'Múltiples quejas en categoría {category} ({count} casos)',
                    'suggested_actions': [
                        f'Revisar funcionalidad de {category}',
                        'Mejorar documentación y explicaciones',
                        'Considerar ajustes en algoritmos'
                    ]
                })
        
        return sorted(recommendations, key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x['priority']], reverse=True)
    
    def export_feedback_report(self, filename: Optional[str] = None) -> str:
        """Export comprehensive feedback report"""
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"feedback_report_{timestamp}.json"
        
        analytics = self.analyze_feedback()
        recommendations = self.get_improvement_recommendations()
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'analytics': asdict(analytics),
            'recommendations': recommendations,
            'raw_feedback_count': len(self.feedback_data),
            'summary': {
                'overall_satisfaction': 'good' if analytics.average_rating >= 4 else 'needs_improvement',
                'top_priority_areas': [r['area'] for r in recommendations[:3]],
                'user_engagement': 'high' if analytics.total_feedback >= 50 else 'low'
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"Feedback report exported to {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting report: {e}")
            return ""
    
    def load_feedback_data(self) -> None:
        """Load feedback data from file"""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.feedback_data = [
                    UserFeedback(**item) for item in data
                ]
                print(f"Loaded {len(self.feedback_data)} feedback entries")
            except Exception as e:
                print(f"Error loading feedback data: {e}")
                self.feedback_data = []
        else:
            self.feedback_data = []
    
    def save_feedback_data(self) -> None:
        """Save feedback data to file"""
        try:
            data = [asdict(feedback) for feedback in self.feedback_data]
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving feedback data: {e}")
    
    def simulate_feedback_data(self, num_entries: int = 50) -> None:
        """Generate simulated feedback data for testing"""
        
        import random
        
        sample_texts = [
            "Este es un texto de ejemplo para probar el sistema.",
            "La empresa fue fundada en 1990 y ha crecido mucho desde entonces.",
            "Nuestro sitio web ofrece servicios de consultoría en marketing digital.",
            "El documento contiene información importante que que debe ser revisada.",
            "Los usuarios pueden acceder a la plataforma desde cualquier dispositivo."
        ]
        
        agents = [['grammar'], ['style'], ['grammar', 'style'], ['seo'], ['grammar', 'style', 'seo']]
        feedback_types = ['correction', 'suggestion', 'praise', 'complaint']
        
        for i in range(num_entries):
            session_id = f"sim_session_{i}"
            original = random.choice(sample_texts)
            processed = original  # Simplified
            rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.2, 0.4, 0.25])[0]
            feedback_type = random.choice(feedback_types)
            
            # Generate feedback text based on rating
            if rating >= 4:
                feedback_text = random.choice([
                    "Excelente corrección, muy útil",
                    "Me ayudó mucho a mejorar mi texto", 
                    "Las sugerencias son muy apropiadas"
                ])
            elif rating == 3:
                feedback_text = random.choice([
                    "Está bien pero podría mejorar",
                    "Algunas sugerencias son útiles",
                    "Regular, cumple su función"
                ])
            else:
                feedback_text = random.choice([
                    "Las correcciones no son precisas",
                    "El sistema es muy lento",
                    "No entiendo las explicaciones"
                ])
            
            # Random timestamp within last 30 days
            timestamp = time.time() - random.randint(0, 30 * 24 * 3600)
            
            feedback = UserFeedback(
                id=str(uuid.uuid4()),
                session_id=session_id,
                original_text=original,
                processed_text=processed,
                user_rating=rating,
                feedback_type=feedback_type,
                specific_feedback=feedback_text,
                agent_used=random.choice(agents),
                processing_time=random.uniform(0.5, 5.0),
                timestamp=timestamp
            )
            
            self.feedback_data.append(feedback)
        
        self.save_feedback_data()
        print(f"Generated {num_entries} simulated feedback entries")

class FeedbackIntegratedCoordinator:
    """Agent coordinator with integrated feedback system"""
    
    def __init__(self, base_coordinator, feedback_manager: UserFeedbackManager):
        self.base_coordinator = base_coordinator
        self.feedback_manager = feedback_manager
        self.session_id = str(uuid.uuid4())
    
    def process_text_with_feedback(self, text: str, selected_agents: List[str] = None) -> Dict[str, Any]:
        """Process text and prepare for feedback collection"""
        
        start_time = time.time()
        results = self.base_coordinator.process_text(text, selected_agents)
        processing_time = time.time() - start_time
        
        # Add feedback prompts to results
        feedback_prompts = self.feedback_manager.get_feedback_prompt(results)
        
        results.update({
            'feedback_prompts': feedback_prompts,
            'session_id': self.session_id,
            'processing_time': processing_time,
            'ready_for_feedback': True
        })
        
        return results
    
    def submit_user_feedback(self, 
                           results: Dict[str, Any],
                           user_rating: float,
                           feedback_type: str,
                           specific_feedback: str,
                           user_corrections: Optional[Dict[str, str]] = None) -> str:
        """Submit user feedback for processed results"""
        
        return self.feedback_manager.collect_feedback(
            session_id=results.get('session_id', self.session_id),
            original_text=results.get('original_text', ''),
            processed_text=results.get('corrected_text', ''),
            user_rating=user_rating,
            feedback_type=feedback_type,
            specific_feedback=specific_feedback,
            agent_used=list(results.get('agent_results', {}).keys()),
            processing_time=results.get('processing_time', 0),
            user_corrections=user_corrections
        )
    
    def get_improvement_insights(self) -> Dict[str, Any]:
        """Get insights for system improvement"""
        
        analytics = self.feedback_manager.analyze_feedback()
        recommendations = self.feedback_manager.get_improvement_recommendations()
        
        return {
            'analytics': analytics,
            'recommendations': recommendations,
            'system_health': {
                'satisfaction_level': 'good' if analytics.average_rating >= 4 else 'needs_improvement',
                'user_engagement': 'active' if analytics.total_feedback >= 20 else 'low',
                'top_issues': [r['area'] for r in recommendations[:3]]
            }
        }