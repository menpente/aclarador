"""
Advanced metrics and analytics dashboard for Aclarador system
"""

import time
import json
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import os

@dataclass
class SystemMetrics:
    """System-wide performance metrics"""
    
    # Usage metrics
    total_requests: int
    unique_sessions: int
    avg_requests_per_session: float
    
    # Performance metrics
    avg_processing_time: float
    min_processing_time: float
    max_processing_time: float
    cache_hit_rate: float
    
    # Quality metrics
    avg_quality_score: float
    quality_distribution: Dict[str, int]
    improvement_success_rate: float
    
    # Agent metrics
    agent_usage: Dict[str, int]
    agent_performance: Dict[str, float]
    
    # User satisfaction
    avg_user_rating: float
    satisfaction_rate: float
    feedback_count: int

@dataclass
class AnalyticsInsight:
    """Represents an analytical insight"""
    
    category: str
    insight_type: str  # 'trend', 'anomaly', 'recommendation'
    title: str
    description: str
    impact_level: str  # 'high', 'medium', 'low'
    confidence: float
    data_points: Dict[str, Any]
    timestamp: float

class AdvancedAnalytics:
    """Advanced analytics and insights system"""
    
    def __init__(self, data_file: str = "analytics_data.json"):
        self.data_file = data_file
        self.metrics_history: List[Dict[str, Any]] = []
        self.insights_cache: List[AnalyticsInsight] = []
        self.load_analytics_data()
    
    def record_processing_event(self, 
                               session_id: str,
                               text_input: str,
                               results: Dict[str, Any],
                               processing_time: float,
                               user_feedback: Optional[Dict[str, Any]] = None) -> None:
        """Record a processing event for analytics"""
        
        event = {
            'timestamp': time.time(),
            'session_id': session_id,
            'text_length': len(text_input.split()),
            'text_type': results.get('analysis', {}).get('text_type', 'unknown'),
            'agents_used': list(results.get('agent_results', {}).keys()),
            'processing_time': processing_time,
            'improvements_count': len(results.get('improvements', [])),
            'quality_score': results.get('final_validation', {}).get('quality_score', 0),
            'knowledge_guidelines_used': len(results.get('knowledge_guidelines', [])),
            'user_feedback': user_feedback
        }
        
        self.metrics_history.append(event)
        self.save_analytics_data()
        
        # Generate insights if enough data
        if len(self.metrics_history) % 10 == 0:  # Every 10 events
            self._generate_insights()
    
    def calculate_system_metrics(self, days_back: int = 30) -> SystemMetrics:
        """Calculate comprehensive system metrics"""
        
        # Filter recent events
        cutoff_time = time.time() - (days_back * 24 * 3600)
        recent_events = [e for e in self.metrics_history if e['timestamp'] >= cutoff_time]
        
        if not recent_events:
            return SystemMetrics(0, 0, 0, 0, 0, 0, 0, 0, {}, 0, {}, {}, 0, 0, 0)
        
        # Usage metrics
        total_requests = len(recent_events)
        unique_sessions = len(set(e['session_id'] for e in recent_events))
        avg_requests_per_session = total_requests / unique_sessions if unique_sessions > 0 else 0
        
        # Performance metrics
        processing_times = [e['processing_time'] for e in recent_events]
        avg_processing_time = statistics.mean(processing_times)
        min_processing_time = min(processing_times)
        max_processing_time = max(processing_times)
        
        # Cache hit rate (simplified - would need actual cache data)
        cache_hit_rate = 0.65  # Placeholder
        
        # Quality metrics
        quality_scores = [e['quality_score'] for e in recent_events if e['quality_score'] > 0]
        avg_quality_score = statistics.mean(quality_scores) if quality_scores else 0
        
        quality_distribution = self._calculate_quality_distribution(quality_scores)
        improvement_success_rate = self._calculate_improvement_success_rate(recent_events)
        
        # Agent metrics
        agent_usage = self._calculate_agent_usage(recent_events)
        agent_performance = self._calculate_agent_performance(recent_events)
        
        # User satisfaction (from feedback)
        feedback_events = [e for e in recent_events if e.get('user_feedback')]
        if feedback_events:
            ratings = [e['user_feedback']['rating'] for e in feedback_events if 'rating' in e['user_feedback']]
            avg_user_rating = statistics.mean(ratings) if ratings else 0
            satisfaction_rate = len([r for r in ratings if r >= 4]) / len(ratings) if ratings else 0
        else:
            avg_user_rating = 0
            satisfaction_rate = 0
        
        return SystemMetrics(
            total_requests=total_requests,
            unique_sessions=unique_sessions,
            avg_requests_per_session=avg_requests_per_session,
            avg_processing_time=avg_processing_time,
            min_processing_time=min_processing_time,
            max_processing_time=max_processing_time,
            cache_hit_rate=cache_hit_rate,
            avg_quality_score=avg_quality_score,
            quality_distribution=quality_distribution,
            improvement_success_rate=improvement_success_rate,
            agent_usage=agent_usage,
            agent_performance=agent_performance,
            avg_user_rating=avg_user_rating,
            satisfaction_rate=satisfaction_rate,
            feedback_count=len(feedback_events)
        )
    
    def _calculate_quality_distribution(self, quality_scores: List[float]) -> Dict[str, int]:
        """Calculate distribution of quality scores"""
        
        distribution = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        
        for score in quality_scores:
            if score >= 0.9:
                distribution['excellent'] += 1
            elif score >= 0.7:
                distribution['good'] += 1
            elif score >= 0.5:
                distribution['fair'] += 1
            else:
                distribution['poor'] += 1
        
        return distribution
    
    def _calculate_improvement_success_rate(self, events: List[Dict[str, Any]]) -> float:
        """Calculate rate of successful improvements"""
        
        events_with_improvements = [e for e in events if e['improvements_count'] > 0]
        return len(events_with_improvements) / len(events) if events else 0
    
    def _calculate_agent_usage(self, events: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate agent usage statistics"""
        
        agent_counter = Counter()
        
        for event in events:
            for agent in event['agents_used']:
                agent_counter[agent] += 1
        
        return dict(agent_counter)
    
    def _calculate_agent_performance(self, events: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate agent performance metrics"""
        
        agent_performance = defaultdict(list)
        
        # Collect quality scores per agent
        for event in events:
            if event['quality_score'] > 0:
                for agent in event['agents_used']:
                    agent_performance[agent].append(event['quality_score'])
        
        # Calculate average performance
        return {
            agent: statistics.mean(scores)
            for agent, scores in agent_performance.items()
        }
    
    def generate_usage_insights(self, days_back: int = 30) -> List[AnalyticsInsight]:
        """Generate insights about system usage patterns"""
        
        insights = []
        recent_events = [e for e in self.metrics_history 
                        if e['timestamp'] >= time.time() - (days_back * 24 * 3600)]
        
        if len(recent_events) < 10:
            return insights
        
        # Usage trend analysis
        daily_usage = self._group_by_day(recent_events)
        usage_trend = self._calculate_trend(daily_usage)
        
        if usage_trend['direction'] == 'increasing':
            insights.append(AnalyticsInsight(
                category='usage',
                insight_type='trend',
                title='Crecimiento en el uso del sistema',
                description=f'El uso ha aumentado {usage_trend["change_percent"]:.1f}% en los últimos {days_back} días',
                impact_level='medium',
                confidence=usage_trend['confidence'],
                data_points={'daily_usage': daily_usage, 'trend': usage_trend},
                timestamp=time.time()
            ))
        
        # Peak usage times
        hourly_usage = self._group_by_hour(recent_events)
        peak_hours = sorted(hourly_usage.items(), key=lambda x: x[1], reverse=True)[:3]
        
        insights.append(AnalyticsInsight(
            category='usage',
            insight_type='trend',
            title='Horas pico de uso',
            description=f'Mayor actividad entre las {peak_hours[0][0]}:00 y {peak_hours[2][0]}:00',
            impact_level='low',
            confidence=0.8,
            data_points={'hourly_distribution': dict(hourly_usage)},
            timestamp=time.time()
        ))
        
        return insights
    
    def generate_performance_insights(self) -> List[AnalyticsInsight]:
        """Generate performance-related insights"""
        
        insights = []
        recent_events = self.metrics_history[-100:]  # Last 100 events
        
        if len(recent_events) < 20:
            return insights
        
        # Processing time analysis
        processing_times = [e['processing_time'] for e in recent_events]
        avg_time = statistics.mean(processing_times)
        
        # Identify slow processing
        if avg_time > 3.0:
            insights.append(AnalyticsInsight(
                category='performance',
                insight_type='anomaly',
                title='Tiempo de procesamiento elevado',
                description=f'Tiempo promedio de {avg_time:.1f}s excede el objetivo de 3s',
                impact_level='high',
                confidence=0.9,
                data_points={'avg_time': avg_time, 'target': 3.0},
                timestamp=time.time()
            ))
        
        # Cache performance (if data available)
        knowledge_usage = [e['knowledge_guidelines_used'] for e in recent_events]
        avg_knowledge_usage = statistics.mean(knowledge_usage)
        
        if avg_knowledge_usage > 3:
            insights.append(AnalyticsInsight(
                category='performance',
                insight_type='trend',
                title='Alto uso de base de conocimientos',
                description=f'Promedio de {avg_knowledge_usage:.1f} directrices por solicitud indica buena integración',
                impact_level='medium',
                confidence=0.8,
                data_points={'avg_knowledge_usage': avg_knowledge_usage},
                timestamp=time.time()
            ))
        
        return insights
    
    def generate_quality_insights(self) -> List[AnalyticsInsight]:
        """Generate quality-related insights"""
        
        insights = []
        recent_events = [e for e in self.metrics_history[-50:] if e['quality_score'] > 0]
        
        if len(recent_events) < 10:
            return insights
        
        # Quality trend
        quality_scores = [e['quality_score'] for e in recent_events]
        avg_quality = statistics.mean(quality_scores)
        
        if avg_quality >= 0.85:
            insights.append(AnalyticsInsight(
                category='quality',
                insight_type='trend',
                title='Alta calidad del sistema',
                description=f'Puntuación promedio de calidad: {avg_quality:.1%}',
                impact_level='medium',
                confidence=0.9,
                data_points={'avg_quality': avg_quality, 'scores': quality_scores},
                timestamp=time.time()
            ))
        elif avg_quality < 0.6:
            insights.append(AnalyticsInsight(
                category='quality',
                insight_type='anomaly',
                title='Calidad por debajo del objetivo',
                description=f'Puntuación promedio de {avg_quality:.1%} requiere atención',
                impact_level='high',
                confidence=0.85,
                data_points={'avg_quality': avg_quality},
                timestamp=time.time()
            ))
        
        # Improvement effectiveness
        improvements_per_request = [e['improvements_count'] for e in recent_events]
        avg_improvements = statistics.mean(improvements_per_request)
        
        if avg_improvements > 5:
            insights.append(AnalyticsInsight(
                category='quality',
                insight_type='recommendation',
                title='Alto número de correcciones',
                description=f'Promedio de {avg_improvements:.1f} mejoras por texto sugiere textos complejos',
                impact_level='medium',
                confidence=0.7,
                data_points={'avg_improvements': avg_improvements},
                timestamp=time.time()
            ))
        
        return insights
    
    def generate_agent_insights(self) -> List[AnalyticsInsight]:
        """Generate agent-specific insights"""
        
        insights = []
        recent_events = self.metrics_history[-100:]
        
        if len(recent_events) < 20:
            return insights
        
        # Agent usage patterns
        agent_usage = self._calculate_agent_usage(recent_events)
        most_used_agent = max(agent_usage.items(), key=lambda x: x[1])
        
        insights.append(AnalyticsInsight(
            category='agents',
            insight_type='trend',
            title=f'Agente más utilizado: {most_used_agent[0]}',
            description=f'Usado en {most_used_agent[1]} de {len(recent_events)} solicitudes',
            impact_level='low',
            confidence=0.9,
            data_points={'agent_usage': agent_usage},
            timestamp=time.time()
        ))
        
        # Agent performance comparison
        agent_performance = self._calculate_agent_performance(recent_events)
        if len(agent_performance) > 1:
            best_agent = max(agent_performance.items(), key=lambda x: x[1])
            worst_agent = min(agent_performance.items(), key=lambda x: x[1])
            
            if best_agent[1] - worst_agent[1] > 0.2:  # Significant difference
                insights.append(AnalyticsInsight(
                    category='agents',
                    insight_type='recommendation',
                    title='Diferencias en rendimiento de agentes',
                    description=f'{best_agent[0]} ({best_agent[1]:.1%}) supera significativamente a {worst_agent[0]} ({worst_agent[1]:.1%})',
                    impact_level='medium',
                    confidence=0.8,
                    data_points={'performance': agent_performance},
                    timestamp=time.time()
                ))
        
        return insights
    
    def _group_by_day(self, events: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group events by day"""
        
        daily_counts = defaultdict(int)
        
        for event in events:
            day = datetime.fromtimestamp(event['timestamp']).strftime('%Y-%m-%d')
            daily_counts[day] += 1
        
        return dict(daily_counts)
    
    def _group_by_hour(self, events: List[Dict[str, Any]]) -> Dict[int, int]:
        """Group events by hour of day"""
        
        hourly_counts = defaultdict(int)
        
        for event in events:
            hour = datetime.fromtimestamp(event['timestamp']).hour
            hourly_counts[hour] += 1
        
        return dict(hourly_counts)
    
    def _calculate_trend(self, time_series_data: Dict[str, int]) -> Dict[str, Any]:
        """Calculate trend from time series data"""
        
        if len(time_series_data) < 3:
            return {'direction': 'unknown', 'change_percent': 0, 'confidence': 0}
        
        sorted_data = sorted(time_series_data.items())
        values = [item[1] for item in sorted_data]
        
        # Simple linear trend
        first_third = statistics.mean(values[:len(values)//3])
        last_third = statistics.mean(values[-len(values)//3:])
        
        change_percent = ((last_third - first_third) / first_third * 100) if first_third > 0 else 0
        
        if abs(change_percent) < 10:
            direction = 'stable'
        elif change_percent > 0:
            direction = 'increasing'
        else:
            direction = 'decreasing'
        
        confidence = min(0.95, abs(change_percent) / 50 + 0.5)
        
        return {
            'direction': direction,
            'change_percent': change_percent,
            'confidence': confidence
        }
    
    def _generate_insights(self) -> None:
        """Generate all insights and cache them"""
        
        all_insights = []
        
        # Generate different types of insights
        all_insights.extend(self.generate_usage_insights())
        all_insights.extend(self.generate_performance_insights())
        all_insights.extend(self.generate_quality_insights())
        all_insights.extend(self.generate_agent_insights())
        
        # Sort by impact and confidence
        all_insights.sort(key=lambda x: (
            {'high': 3, 'medium': 2, 'low': 1}[x.impact_level],
            x.confidence
        ), reverse=True)
        
        # Keep only recent insights
        recent_insights = [i for i in all_insights if time.time() - i.timestamp < 7*24*3600]
        self.insights_cache = recent_insights[:20]  # Keep top 20
    
    def get_dashboard_data(self, days_back: int = 30) -> Dict[str, Any]:
        """Get complete dashboard data"""
        
        metrics = self.calculate_system_metrics(days_back)
        insights = self.insights_cache[-10:]  # Last 10 insights
        
        # Calculate additional dashboard metrics
        recent_events = [e for e in self.metrics_history 
                        if e['timestamp'] >= time.time() - (days_back * 24 * 3600)]
        
        dashboard_data = {
            'summary': {
                'total_requests': metrics.total_requests,
                'avg_quality': metrics.avg_quality_score,
                'user_satisfaction': metrics.satisfaction_rate,
                'system_health': self._calculate_system_health(metrics)
            },
            'metrics': asdict(metrics),
            'insights': [asdict(insight) for insight in insights],
            'charts': {
                'quality_trend': self._generate_quality_chart(recent_events),
                'usage_pattern': self._generate_usage_chart(recent_events),
                'agent_performance': dict(metrics.agent_performance)
            },
            'recommendations': self._generate_system_recommendations(metrics, insights),
            'generated_at': datetime.now().isoformat()
        }
        
        return dashboard_data
    
    def _calculate_system_health(self, metrics: SystemMetrics) -> str:
        """Calculate overall system health status"""
        
        health_score = 0
        
        # Quality factor
        if metrics.avg_quality_score >= 0.8:
            health_score += 30
        elif metrics.avg_quality_score >= 0.6:
            health_score += 20
        else:
            health_score += 10
        
        # Performance factor
        if metrics.avg_processing_time <= 2.0:
            health_score += 25
        elif metrics.avg_processing_time <= 5.0:
            health_score += 15
        else:
            health_score += 5
        
        # User satisfaction factor
        if metrics.satisfaction_rate >= 0.8:
            health_score += 25
        elif metrics.satisfaction_rate >= 0.6:
            health_score += 15
        else:
            health_score += 5
        
        # Usage factor
        if metrics.total_requests > 100:
            health_score += 20
        elif metrics.total_requests > 20:
            health_score += 10
        else:
            health_score += 5
        
        if health_score >= 85:
            return 'excellent'
        elif health_score >= 70:
            return 'good'
        elif health_score >= 50:
            return 'fair'
        else:
            return 'poor'
    
    def _generate_quality_chart(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate quality trend chart data"""
        
        quality_events = [e for e in events if e['quality_score'] > 0]
        
        # Group by day and calculate average quality
        daily_quality = defaultdict(list)
        for event in quality_events:
            day = datetime.fromtimestamp(event['timestamp']).strftime('%Y-%m-%d')
            daily_quality[day].append(event['quality_score'])
        
        chart_data = []
        for day, scores in sorted(daily_quality.items()):
            chart_data.append({
                'date': day,
                'quality': statistics.mean(scores),
                'count': len(scores)
            })
        
        return chart_data
    
    def _generate_usage_chart(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate usage pattern chart data"""
        
        daily_usage = self._group_by_day(events)
        
        chart_data = []
        for day, count in sorted(daily_usage.items()):
            chart_data.append({
                'date': day,
                'requests': count
            })
        
        return chart_data
    
    def _generate_system_recommendations(self, metrics: SystemMetrics, insights: List[AnalyticsInsight]) -> List[str]:
        """Generate system-level recommendations"""
        
        recommendations = []
        
        # Performance recommendations
        if metrics.avg_processing_time > 3.0:
            recommendations.append("Considere optimizar el rendimiento - tiempo promedio elevado")
        
        # Quality recommendations
        if metrics.avg_quality_score < 0.7:
            recommendations.append("Revise la precisión de los agentes - calidad por debajo del objetivo")
        
        # Usage recommendations
        if metrics.total_requests < 50:
            recommendations.append("Bajo uso del sistema - considere estrategias de adopción")
        
        # Insight-based recommendations
        high_impact_insights = [i for i in insights if i.impact_level == 'high']
        for insight in high_impact_insights[:2]:
            recommendations.append(f"Prioridad alta: {insight.title}")
        
        return recommendations[:5]  # Top 5 recommendations
    
    def export_analytics_report(self, filename: Optional[str] = None) -> str:
        """Export comprehensive analytics report"""
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analytics_report_{timestamp}.json"
        
        dashboard_data = self.get_dashboard_data()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
            print(f"Analytics report exported to {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting analytics report: {e}")
            return ""
    
    def load_analytics_data(self) -> None:
        """Load analytics data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.metrics_history = data.get('metrics_history', [])
                print(f"Loaded {len(self.metrics_history)} analytics events")
            except Exception as e:
                print(f"Error loading analytics data: {e}")
                self.metrics_history = []
        else:
            self.metrics_history = []
    
    def save_analytics_data(self) -> None:
        """Save analytics data to file"""
        try:
            data = {
                'metrics_history': self.metrics_history,
                'last_updated': time.time()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving analytics data: {e}")

class AnalyticsIntegratedSystem:
    """Complete system with integrated analytics"""
    
    def __init__(self, base_coordinator):
        self.base_coordinator = base_coordinator
        self.analytics = AdvancedAnalytics()
        self.session_id = f"session_{int(time.time())}"
    
    def process_with_analytics(self, text: str, selected_agents: List[str] = None) -> Dict[str, Any]:
        """Process text and record analytics"""
        
        start_time = time.time()
        results = self.base_coordinator.process_text(text, selected_agents)
        processing_time = time.time() - start_time
        
        # Record analytics
        self.analytics.record_processing_event(
            session_id=self.session_id,
            text_input=text,
            results=results,
            processing_time=processing_time
        )
        
        # Add analytics info to results
        results['analytics'] = {
            'processing_time': processing_time,
            'session_id': self.session_id,
            'recorded': True
        }
        
        return results
    
    def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Get analytics dashboard"""
        return self.analytics.get_dashboard_data()
    
    def submit_feedback_with_analytics(self, results: Dict[str, Any], feedback: Dict[str, Any]) -> None:
        """Submit feedback and update analytics"""
        
        # Update the last recorded event with feedback
        if self.analytics.metrics_history:
            last_event = self.analytics.metrics_history[-1]
            if last_event.get('session_id') == results.get('analytics', {}).get('session_id'):
                last_event['user_feedback'] = feedback
                self.analytics.save_analytics_data()