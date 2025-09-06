"""
Advanced quality analysis and convergence detection system
"""

import re
import math
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from collections import Counter
import statistics

@dataclass
class QualityMetrics:
    """Comprehensive quality metrics for text analysis"""
    
    # Readability metrics
    readability_score: float
    sentence_complexity: float
    vocabulary_complexity: float
    structure_score: float
    
    # Language clarity metrics
    clarity_score: float
    coherence_score: float
    precision_score: float
    
    # Technical metrics
    grammar_accuracy: float
    style_consistency: float
    seo_optimization: float
    
    # Overall metrics
    overall_quality: float
    confidence_level: float
    improvement_potential: float

class QualityAnalyzer:
    """Advanced quality analyzer with convergence detection"""
    
    def __init__(self):
        # Spanish language specific parameters
        self.spanish_complexity_indicators = {
            'complex_structures': [
                r'\b(no obstante|sin embargo|por consiguiente|a pesar de que|dado que)\b',
                r'\b(cuyo|cuya|cuyos|cuyas)\b',
                r'\b(mediante|respecto a|con respecto a|en relación con)\b'
            ],
            'passive_voice': [
                r'\b(fue|fueron|ha sido|han sido|será|serán)\s+\w+ado\b',
                r'\b(fue|fueron|ha sido|han sido|será|serán)\s+\w+ido\b'
            ],
            'complex_vocabulary': [
                r'\w{15,}',  # Very long words
                r'\b\w*(ción|sión|idad|mente|ismo|ística)\b'  # Complex suffixes
            ]
        }
        
        # Quality thresholds for convergence detection
        self.convergence_thresholds = {
            'minimal_improvement': 0.02,  # 2% improvement threshold
            'high_quality': 0.85,  # 85% quality threshold
            'excellent_quality': 0.95,  # 95% quality threshold
            'stability_threshold': 0.01  # 1% stability threshold
        }
    
    def analyze_comprehensive_quality(self, text: str, context: Dict[str, Any] = None) -> QualityMetrics:
        """Perform comprehensive quality analysis"""
        
        # Basic text analysis
        sentences = self._extract_sentences(text)
        words = text.split()
        
        if not sentences or not words:
            return QualityMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        # Calculate individual metrics
        readability = self._calculate_readability(text, sentences, words)
        sentence_complexity = self._analyze_sentence_complexity(sentences)
        vocabulary_complexity = self._analyze_vocabulary_complexity(words)
        structure_score = self._analyze_text_structure(text, sentences)
        
        clarity_score = self._calculate_clarity_score(text, sentences)
        coherence_score = self._calculate_coherence_score(sentences)
        precision_score = self._calculate_precision_score(text, words)
        
        grammar_accuracy = self._estimate_grammar_accuracy(text, context)
        style_consistency = self._analyze_style_consistency(sentences)
        seo_optimization = self._analyze_seo_quality(text, context)
        
        # Calculate overall quality with weights
        overall_quality = self._calculate_overall_quality({
            'readability': readability,
            'clarity': clarity_score,
            'grammar': grammar_accuracy,
            'structure': structure_score,
            'coherence': coherence_score
        })
        
        # Calculate confidence and improvement potential
        confidence_level = self._calculate_confidence_level(text, context)
        improvement_potential = self._calculate_improvement_potential(overall_quality, context)
        
        return QualityMetrics(
            readability_score=readability,
            sentence_complexity=sentence_complexity,
            vocabulary_complexity=vocabulary_complexity,
            structure_score=structure_score,
            clarity_score=clarity_score,
            coherence_score=coherence_score,
            precision_score=precision_score,
            grammar_accuracy=grammar_accuracy,
            style_consistency=style_consistency,
            seo_optimization=seo_optimization,
            overall_quality=overall_quality,
            confidence_level=confidence_level,
            improvement_potential=improvement_potential
        )
    
    def detect_convergence(self, 
                          quality_history: List[QualityMetrics], 
                          improvement_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect if quality improvements have converged"""
        
        if len(quality_history) < 2:
            return {
                'converged': False,
                'reason': 'Insufficient history',
                'confidence': 0.0,
                'recommendation': 'continue'
            }
        
        current = quality_history[-1]
        previous = quality_history[-2]
        
        # Calculate improvement rate
        improvement = current.overall_quality - previous.overall_quality
        
        # Check convergence conditions
        convergence_analysis = {
            'quality_plateau': self._detect_quality_plateau(quality_history),
            'minimal_improvement': improvement < self.convergence_thresholds['minimal_improvement'],
            'high_quality_reached': current.overall_quality >= self.convergence_thresholds['high_quality'],
            'stability_achieved': self._detect_stability(quality_history),
            'improvement_saturation': self._detect_improvement_saturation(improvement_history)
        }
        
        # Determine convergence
        converged, reason, confidence = self._determine_convergence_status(convergence_analysis, current)
        
        # Generate recommendations
        recommendation = self._generate_convergence_recommendation(convergence_analysis, current, improvement_history)
        
        return {
            'converged': converged,
            'reason': reason,
            'confidence': confidence,
            'recommendation': recommendation,
            'current_quality': current.overall_quality,
            'improvement_rate': improvement,
            'analysis_details': convergence_analysis
        }
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _calculate_readability(self, text: str, sentences: List[str], words: List[str]) -> float:
        """Calculate readability score for Spanish text"""
        
        if not sentences or not words:
            return 0.0
        
        # Basic metrics
        avg_sentence_length = len(words) / len(sentences)
        
        # Count syllables (simplified for Spanish)
        syllable_count = 0
        for word in words:
            syllable_count += self._count_spanish_syllables(word)
        
        avg_syllables_per_word = syllable_count / len(words) if words else 0
        
        # Spanish Flesch Reading Ease (adapted formula)
        if sentences and words:
            flesch_score = 206.84 - (1.02 * avg_sentence_length) - (0.60 * avg_syllables_per_word)
            readability = max(0, min(100, flesch_score)) / 100
        else:
            readability = 0
        
        return readability
    
    def _count_spanish_syllables(self, word: str) -> int:
        """Count syllables in Spanish word (simplified)"""
        word = word.lower()
        vowels = 'aeiouáéíóúü'
        syllables = 0
        prev_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False
        
        return max(1, syllables)
    
    def _analyze_sentence_complexity(self, sentences: List[str]) -> float:
        """Analyze sentence complexity"""
        
        if not sentences:
            return 1.0
        
        complexity_scores = []
        
        for sentence in sentences:
            words = sentence.split()
            complexity = 1.0
            
            # Length-based complexity
            if len(words) > 30:
                complexity *= 0.5  # Very complex
            elif len(words) > 20:
                complexity *= 0.7  # Moderately complex
            elif len(words) < 5:
                complexity *= 0.8  # Too short might be unclear
            
            # Structure-based complexity
            for pattern in self.spanish_complexity_indicators['complex_structures']:
                if re.search(pattern, sentence, re.IGNORECASE):
                    complexity *= 0.8
            
            complexity_scores.append(complexity)
        
        return statistics.mean(complexity_scores)
    
    def _analyze_vocabulary_complexity(self, words: List[str]) -> float:
        """Analyze vocabulary complexity"""
        
        if not words:
            return 1.0
        
        complex_word_count = 0
        
        for word in words:
            for pattern in self.spanish_complexity_indicators['complex_vocabulary']:
                if re.search(pattern, word, re.IGNORECASE):
                    complex_word_count += 1
                    break
        
        complexity_ratio = complex_word_count / len(words)
        
        # Convert to score (lower complexity ratio = higher score)
        return max(0.2, 1.0 - (complexity_ratio * 2))
    
    def _analyze_text_structure(self, text: str, sentences: List[str]) -> float:
        """Analyze text structure quality"""
        
        structure_score = 1.0
        
        # Paragraph structure
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if len(paragraphs) > 1:
            avg_para_length = len(sentences) / len(paragraphs)
            if 2 <= avg_para_length <= 8:  # Optimal paragraph length
                structure_score *= 1.0
            else:
                structure_score *= 0.8
        
        # Sentence variety
        sentence_lengths = [len(s.split()) for s in sentences]
        if len(set(sentence_lengths)) > len(sentence_lengths) * 0.3:  # Good variety
            structure_score *= 1.0
        else:
            structure_score *= 0.9
        
        return min(1.0, structure_score)
    
    def _calculate_clarity_score(self, text: str, sentences: List[str]) -> float:
        """Calculate text clarity score"""
        
        clarity_factors = []
        
        # Active vs passive voice
        passive_count = 0
        for pattern in self.spanish_complexity_indicators['passive_voice']:
            passive_count += len(re.findall(pattern, text, re.IGNORECASE))
        
        passive_ratio = passive_count / len(sentences) if sentences else 0
        active_voice_score = max(0.5, 1.0 - passive_ratio)
        clarity_factors.append(active_voice_score)
        
        # Sentence length consistency
        lengths = [len(s.split()) for s in sentences]
        if lengths:
            avg_length = statistics.mean(lengths)
            length_score = 1.0 if 10 <= avg_length <= 25 else 0.7
            clarity_factors.append(length_score)
        
        # Logical flow indicators
        flow_indicators = ['primero', 'segundo', 'además', 'por tanto', 'finalmente', 'en conclusión']
        flow_count = sum(1 for indicator in flow_indicators if indicator in text.lower())
        flow_score = min(1.0, flow_count / max(1, len(sentences) / 5))
        clarity_factors.append(flow_score)
        
        return statistics.mean(clarity_factors) if clarity_factors else 0.5
    
    def _calculate_coherence_score(self, sentences: List[str]) -> float:
        """Calculate text coherence score"""
        
        if len(sentences) < 2:
            return 1.0
        
        coherence_score = 0.8  # Base score
        
        # Word repetition analysis (semantic coherence indicator)
        all_words = []
        for sentence in sentences:
            words = [w.lower() for w in sentence.split() if len(w) > 3]
            all_words.extend(words)
        
        if all_words:
            word_freq = Counter(all_words)
            repeated_words = sum(1 for count in word_freq.values() if count > 1)
            repetition_score = min(1.0, repeated_words / len(set(all_words)))
            coherence_score += repetition_score * 0.2
        
        return min(1.0, coherence_score)
    
    def _calculate_precision_score(self, text: str, words: List[str]) -> float:
        """Calculate precision/conciseness score"""
        
        # Redundancy detection
        redundant_phrases = [
            'muy muy', 'que que', 'el el', 'la la', 'de de',
            'completamente total', 'absolutamente completo',
            'totalmente absoluto'
        ]
        
        redundancy_count = 0
        text_lower = text.lower()
        for phrase in redundant_phrases:
            redundancy_count += text_lower.count(phrase)
        
        # Filler words
        filler_words = ['realmente', 'básicamente', 'obviamente', 'claramente', 'simplemente']
        filler_count = sum(1 for word in words if word.lower() in filler_words)
        
        # Calculate precision
        total_issues = redundancy_count + filler_count
        precision_score = max(0.5, 1.0 - (total_issues / len(words) * 10))
        
        return precision_score
    
    def _estimate_grammar_accuracy(self, text: str, context: Dict[str, Any] = None) -> float:
        """Estimate grammar accuracy based on available information"""
        
        base_score = 0.8  # Assume decent grammar by default
        
        # If we have agent results, use them
        if context and 'agent_results' in context:
            grammar_results = context['agent_results'].get('grammar', {})
            corrections = grammar_results.get('corrections', [])
            
            # More corrections = lower initial accuracy
            if corrections:
                error_density = len(corrections) / max(1, len(text.split()) / 10)
                grammar_score = max(0.3, 0.9 - error_density * 0.1)
            else:
                grammar_score = 0.95
            
            return grammar_score
        
        return base_score
    
    def _analyze_style_consistency(self, sentences: List[str]) -> float:
        """Analyze style consistency"""
        
        if len(sentences) < 2:
            return 1.0
        
        # Sentence length consistency
        lengths = [len(s.split()) for s in sentences]
        length_std = statistics.stdev(lengths) if len(lengths) > 1 else 0
        length_consistency = max(0.5, 1.0 - (length_std / statistics.mean(lengths) if statistics.mean(lengths) > 0 else 1))
        
        # Tense consistency (simplified)
        present_tense = sum(1 for s in sentences if re.search(r'\b(es|está|tiene|hace)\b', s))
        past_tense = sum(1 for s in sentences if re.search(r'\b(fue|estuvo|tuvo|hizo)\b', s))
        future_tense = sum(1 for s in sentences if re.search(r'\b(será|estará|tendrá|hará)\b', s))
        
        total_tense = present_tense + past_tense + future_tense
        if total_tense > 0:
            dominant_tense = max(present_tense, past_tense, future_tense)
            tense_consistency = dominant_tense / total_tense
        else:
            tense_consistency = 1.0
        
        return (length_consistency + tense_consistency) / 2
    
    def _analyze_seo_quality(self, text: str, context: Dict[str, Any] = None) -> float:
        """Analyze SEO quality if relevant"""
        
        # Check if SEO agent was used
        if context and 'agent_results' in context:
            seo_results = context['agent_results'].get('seo', {})
            if seo_results:
                # Use SEO agent's assessment
                balance_score = seo_results.get('clarity_balance', {}).get('balance_score', 0.7)
                return balance_score
        
        # Basic SEO quality assessment
        word_count = len(text.split())
        if 300 <= word_count <= 2000:  # Good length for web content
            return 0.8
        elif word_count < 100:
            return 0.4  # Too short
        else:
            return 0.6  # Might be too long
    
    def _calculate_overall_quality(self, metrics: Dict[str, float]) -> float:
        """Calculate weighted overall quality score"""
        
        weights = {
            'readability': 0.25,
            'clarity': 0.25,
            'grammar': 0.20,
            'structure': 0.15,
            'coherence': 0.15
        }
        
        weighted_score = 0
        total_weight = 0
        
        for metric, value in metrics.items():
            if metric in weights:
                weighted_score += value * weights[metric]
                total_weight += weights[metric]
        
        return weighted_score / total_weight if total_weight > 0 else 0.5
    
    def _calculate_confidence_level(self, text: str, context: Dict[str, Any] = None) -> float:
        """Calculate confidence level of quality assessment"""
        
        confidence = 0.7  # Base confidence
        
        # More text = higher confidence
        word_count = len(text.split())
        if word_count > 100:
            confidence += 0.2
        elif word_count < 20:
            confidence -= 0.2
        
        # Having agent context increases confidence
        if context and 'agent_results' in context:
            agent_count = len(context['agent_results'])
            confidence += min(0.2, agent_count * 0.05)
        
        return min(1.0, max(0.3, confidence))
    
    def _calculate_improvement_potential(self, current_quality: float, context: Dict[str, Any] = None) -> float:
        """Calculate potential for further improvement"""
        
        # Higher current quality = lower improvement potential
        base_potential = 1.0 - current_quality
        
        # If we have improvement history, adjust based on recent improvements
        if context and 'improvements' in context:
            recent_improvements = len(context['improvements'])
            if recent_improvements > 5:
                base_potential *= 0.7  # Less potential if many improvements already made
        
        return min(1.0, base_potential)
    
    def _detect_quality_plateau(self, quality_history: List[QualityMetrics]) -> bool:
        """Detect if quality has plateaued"""
        
        if len(quality_history) < 3:
            return False
        
        recent_scores = [q.overall_quality for q in quality_history[-3:]]
        score_range = max(recent_scores) - min(recent_scores)
        
        return score_range < self.convergence_thresholds['stability_threshold']
    
    def _detect_stability(self, quality_history: List[QualityMetrics]) -> bool:
        """Detect if quality is stable"""
        
        if len(quality_history) < 2:
            return False
        
        last_two = [q.overall_quality for q in quality_history[-2:]]
        return abs(last_two[1] - last_two[0]) < self.convergence_thresholds['stability_threshold']
    
    def _detect_improvement_saturation(self, improvement_history: List[Dict[str, Any]]) -> bool:
        """Detect if improvements are saturated"""
        
        if len(improvement_history) < 2:
            return False
        
        # Check if recent improvements are minimal
        recent_improvement_counts = [len(imp.get('improvements', [])) for imp in improvement_history[-2:]]
        
        return all(count <= 1 for count in recent_improvement_counts)
    
    def _determine_convergence_status(self, 
                                    analysis: Dict[str, bool], 
                                    current: QualityMetrics) -> Tuple[bool, str, float]:
        """Determine if convergence has been achieved"""
        
        # High quality reached
        if current.overall_quality >= self.convergence_thresholds['excellent_quality']:
            return True, "Excellent quality achieved", 0.95
        
        # Multiple convergence indicators
        convergence_indicators = sum(analysis.values())
        
        if convergence_indicators >= 3:
            return True, "Multiple convergence indicators detected", 0.8
        elif current.overall_quality >= self.convergence_thresholds['high_quality'] and convergence_indicators >= 2:
            return True, "High quality with convergence indicators", 0.85
        elif analysis['quality_plateau'] and analysis['stability_achieved']:
            return True, "Quality plateau with stability", 0.75
        else:
            return False, "Convergence not detected", 0.6
    
    def _generate_convergence_recommendation(self, 
                                           analysis: Dict[str, bool], 
                                           current: QualityMetrics,
                                           improvement_history: List[Dict[str, Any]]) -> str:
        """Generate recommendation based on convergence analysis"""
        
        if current.overall_quality >= self.convergence_thresholds['excellent_quality']:
            return "stop_excellent"
        elif current.overall_quality >= self.convergence_thresholds['high_quality']:
            if analysis['stability_achieved']:
                return "stop_good"
            else:
                return "continue_cautiously"
        elif analysis['improvement_saturation'] and current.overall_quality > 0.6:
            return "manual_review"
        elif sum(analysis.values()) >= 2:
            return "stop_convergence"
        else:
            return "continue"

class ConvergenceDetector:
    """Main convergence detection system"""
    
    def __init__(self):
        self.quality_analyzer = QualityAnalyzer()
        self.quality_history: List[QualityMetrics] = []
        self.improvement_history: List[Dict[str, Any]] = []
    
    def add_processing_result(self, text: str, results: Dict[str, Any]) -> None:
        """Add processing result to history"""
        
        # Analyze quality
        quality_metrics = self.quality_analyzer.analyze_comprehensive_quality(text, results)
        self.quality_history.append(quality_metrics)
        
        # Store improvement information
        self.improvement_history.append({
            'improvements': results.get('improvements', []),
            'agent_results': results.get('agent_results', {}),
            'timestamp': results.get('timestamp', 0)
        })
        
        # Keep only recent history (last 10 entries)
        if len(self.quality_history) > 10:
            self.quality_history.pop(0)
            self.improvement_history.pop(0)
    
    def check_convergence(self) -> Dict[str, Any]:
        """Check if processing has converged"""
        
        return self.quality_analyzer.detect_convergence(
            self.quality_history,
            self.improvement_history
        )
    
    def get_quality_trend(self) -> Dict[str, Any]:
        """Get quality improvement trend"""
        
        if len(self.quality_history) < 2:
            return {'trend': 'insufficient_data', 'direction': 'unknown'}
        
        recent_qualities = [q.overall_quality for q in self.quality_history[-3:]]
        
        if len(recent_qualities) >= 2:
            if recent_qualities[-1] > recent_qualities[-2]:
                direction = 'improving'
            elif recent_qualities[-1] < recent_qualities[-2]:
                direction = 'declining'
            else:
                direction = 'stable'
        else:
            direction = 'unknown'
        
        return {
            'trend': 'tracked',
            'direction': direction,
            'current_quality': recent_qualities[-1] if recent_qualities else 0,
            'quality_range': (min(recent_qualities), max(recent_qualities)) if recent_qualities else (0, 0),
            'data_points': len(self.quality_history)
        }
    
    def reset_history(self) -> None:
        """Reset convergence history"""
        self.quality_history.clear()
        self.improvement_history.clear()
    
    def get_detailed_analysis(self) -> Dict[str, Any]:
        """Get detailed quality and convergence analysis"""
        
        if not self.quality_history:
            return {'status': 'no_data'}
        
        current = self.quality_history[-1]
        convergence = self.check_convergence()
        trend = self.get_quality_trend()
        
        return {
            'status': 'analyzed',
            'current_metrics': {
                'overall_quality': current.overall_quality,
                'readability': current.readability_score,
                'clarity': current.clarity_score,
                'grammar_accuracy': current.grammar_accuracy,
                'confidence': current.confidence_level
            },
            'convergence_analysis': convergence,
            'quality_trend': trend,
            'recommendations': self._get_quality_recommendations(current, convergence)
        }
    
    def _get_quality_recommendations(self, current: QualityMetrics, convergence: Dict[str, Any]) -> List[str]:
        """Get recommendations based on quality analysis"""
        
        recommendations = []
        
        if convergence['converged']:
            recommendations.append(f"Processing converged: {convergence['reason']}")
        
        if current.overall_quality < 0.6:
            recommendations.append("Quality below 60% - consider manual review")
        
        if current.readability_score < 0.6:
            recommendations.append("Low readability - simplify vocabulary and sentence structure")
        
        if current.grammar_accuracy < 0.7:
            recommendations.append("Grammar accuracy concerns - review corrections")
        
        if current.improvement_potential > 0.5:
            recommendations.append("High improvement potential - continue processing")
        
        return recommendations