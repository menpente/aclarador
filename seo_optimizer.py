"""
Advanced SEO optimization while maintaining Spanish language clarity
"""

import re
from typing import Dict, List, Any, Tuple
from collections import Counter
import math

class AdvancedSEOOptimizer:
    """Advanced SEO optimization with Spanish language considerations"""
    
    def __init__(self):
        # Spanish stop words for better keyword analysis
        self.spanish_stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'pero', 'sus', 'muy', 'ser', 'ya', 'está', 'todo', 'esta', 'fue', 'han', 'más', 'como', 'si', 'mi', 'me', 'sin', 'sobre', 'este', 'años', 'entre', 'cuando', 'él', 'mismo', 'tanto', 'otros', 'hasta', 'ni', 'contra', 'ese', 'eso', 'durante', 'también', 'cada', 'menos', 'hacer', 'desde', 'nos', 'vez', 'solo', 'otra', 'donde', 'quien', 'uno', 'cual', 'todos', 'antes'
        }
        
        # SEO best practices for Spanish content
        self.seo_guidelines = {
            'title_length': {'min': 30, 'max': 60, 'optimal': 55},
            'meta_description_length': {'min': 120, 'max': 160, 'optimal': 155},
            'keyword_density': {'min': 0.5, 'max': 3.0, 'optimal': 1.5},
            'paragraph_length': {'min': 50, 'max': 300, 'optimal': 150},
            'sentence_length': {'min': 8, 'max': 30, 'optimal': 20}
        }
    
    def analyze_seo_comprehensive(self, text: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """Comprehensive SEO analysis of Spanish text"""
        
        analysis = {
            'text_structure': self._analyze_text_structure(text),
            'keyword_analysis': self._analyze_keywords(text, target_keywords or []),
            'readability_seo': self._analyze_readability_for_seo(text),
            'content_quality': self._analyze_content_quality(text),
            'technical_seo': self._analyze_technical_aspects(text),
            'recommendations': []
        }
        
        # Generate comprehensive recommendations
        analysis['recommendations'] = self._generate_seo_recommendations(analysis)
        analysis['seo_score'] = self._calculate_seo_score(analysis)
        
        return analysis
    
    def _analyze_text_structure(self, text: str) -> Dict[str, Any]:
        """Analyze text structure for SEO"""
        
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        words = text.split()
        
        # Detect potential headings (lines that are shorter and may be titles)
        potential_headings = []
        for para in paragraphs:
            if len(para) < 80 and not para.endswith('.') and len(para.split()) < 15:
                potential_headings.append(para)
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'avg_paragraph_length': len(words) / len(paragraphs) if paragraphs else 0,
            'potential_headings': potential_headings,
            'structure_score': self._score_text_structure(len(words), len(sentences), len(paragraphs))
        }
    
    def _analyze_keywords(self, text: str, target_keywords: List[str]) -> Dict[str, Any]:
        """Advanced keyword analysis for Spanish text"""
        
        # Clean and tokenize text
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = [word for word in clean_text.split() if word not in self.spanish_stop_words and len(word) > 2]
        
        # Word frequency analysis
        word_freq = Counter(words)
        total_words = len(words)
        
        # Analyze target keywords if provided
        target_analysis = {}
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            count = clean_text.count(keyword_lower)
            density = (count / total_words * 100) if total_words > 0 else 0
            
            target_analysis[keyword] = {
                'count': count,
                'density': density,
                'optimal': self.seo_guidelines['keyword_density']['min'] <= density <= self.seo_guidelines['keyword_density']['max']
            }
        
        # Find potential keywords (most frequent meaningful words)
        potential_keywords = [
            {'word': word, 'frequency': freq, 'density': freq/total_words*100}
            for word, freq in word_freq.most_common(10)
            if len(word) > 3
        ]
        
        return {
            'total_words': total_words,
            'unique_words': len(word_freq),
            'target_keywords': target_analysis,
            'potential_keywords': potential_keywords,
            'keyword_diversity': len(word_freq) / total_words if total_words > 0 else 0
        }
    
    def _analyze_readability_for_seo(self, text: str) -> Dict[str, Any]:
        """Analyze readability with SEO considerations"""
        
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        words = text.split()
        
        if not sentences or not words:
            return {'readability_score': 0, 'seo_readability': 'poor'}
        
        # Calculate metrics
        avg_sentence_length = len(words) / len(sentences)
        
        # Spanish readability considerations
        complex_words = self._count_complex_spanish_words(words)
        complex_word_ratio = complex_words / len(words)
        
        # SEO readability score (simplified)
        readability_score = 100
        
        # Penalty for long sentences (SEO prefers shorter sentences)
        if avg_sentence_length > 25:
            readability_score -= (avg_sentence_length - 25) * 2
        
        # Penalty for complex words
        readability_score -= complex_word_ratio * 30
        
        readability_score = max(0, min(100, readability_score))
        
        # Determine SEO readability level
        if readability_score >= 80:
            seo_readability = 'excellent'
        elif readability_score >= 60:
            seo_readability = 'good'
        elif readability_score >= 40:
            seo_readability = 'fair'
        else:
            seo_readability = 'poor'
        
        return {
            'readability_score': readability_score / 100,
            'seo_readability': seo_readability,
            'avg_sentence_length': avg_sentence_length,
            'complex_word_ratio': complex_word_ratio,
            'recommended_sentence_length': self.seo_guidelines['sentence_length']['optimal']
        }
    
    def _analyze_content_quality(self, text: str) -> Dict[str, Any]:
        """Analyze content quality for SEO"""
        
        # Content depth indicators
        questions = len(re.findall(r'\?', text))
        lists = len(re.findall(r'[-•*]\s', text))
        numbers = len(re.findall(r'\d+', text))
        
        # Engagement indicators
        exclamations = len(re.findall(r'!', text))
        action_words = len(re.findall(r'\b(hacer|crear|aprender|descubrir|obtener|lograr|conseguir|mejorar)\b', text.lower()))
        
        # Content structure
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        avg_paragraph_length = len(text.split()) / len(paragraphs) if paragraphs else 0
        
        return {
            'content_depth_score': min(1.0, (questions + lists + numbers) / 10),
            'engagement_score': min(1.0, (exclamations + action_words) / 5),
            'structure_score': 1.0 if 50 <= avg_paragraph_length <= 200 else 0.6,
            'questions': questions,
            'lists': lists,
            'action_words': action_words,
            'avg_paragraph_length': avg_paragraph_length
        }
    
    def _analyze_technical_aspects(self, text: str) -> Dict[str, Any]:
        """Analyze technical SEO aspects"""
        
        # URL/Link detection
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        www_links = re.findall(r'www\.[\w.-]+', text)
        
        # Special characters and formatting
        bold_indicators = text.count('**') // 2  # Markdown bold
        italic_indicators = text.count('*') - (bold_indicators * 2)
        formatting_elements = bold_indicators + italic_indicators
        
        # Content freshness indicators (dates, temporal words)
        temporal_words = len(re.findall(r'\b(hoy|ayer|mañana|ahora|actual|nuevo|reciente|2024|2025)\b', text.lower()))
        
        return {
            'external_links': len(urls),
            'www_references': len(www_links),
            'formatting_elements': formatting_elements,
            'temporal_relevance': temporal_words,
            'technical_score': min(1.0, (len(urls) + formatting_elements + temporal_words) / 10)
        }
    
    def _count_complex_spanish_words(self, words: List[str]) -> int:
        """Count complex words in Spanish text"""
        complex_count = 0
        
        for word in words:
            # Consider words with 4+ syllables or technical terms as complex
            if (len(word) > 12 or 
                word.endswith(('ción', 'sión', 'mente', 'idad', 'ismo')) or
                word.startswith(('pre', 'anti', 'super', 'inter', 'trans'))):
                complex_count += 1
        
        return complex_count
    
    def _score_text_structure(self, words: int, sentences: int, paragraphs: int) -> float:
        """Score text structure for SEO"""
        score = 1.0
        
        # Optimal word count for web content
        if words < 300:
            score *= 0.7  # Too short
        elif words > 2000:
            score *= 0.8  # Might be too long for some content
        
        # Sentence structure
        if sentences > 0:
            avg_sentence = words / sentences
            if avg_sentence > 30:
                score *= 0.6  # Too long sentences
            elif avg_sentence < 8:
                score *= 0.8  # Too short sentences
        
        return min(1.0, score)
    
    def _generate_seo_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate SEO improvement recommendations"""
        recommendations = []
        
        # Structure recommendations
        structure = analysis['text_structure']
        if structure['avg_sentence_length'] > 25:
            recommendations.append({
                'type': 'structure',
                'priority': 'high',
                'issue': 'Oraciones muy largas afectan SEO',
                'recommendation': f'Reducir longitud promedio de oraciones de {structure["avg_sentence_length"]:.1f} a menos de 25 palabras',
                'seo_impact': 'Mejora legibilidad y tiempo de permanencia'
            })
        
        # Keyword recommendations
        keyword_analysis = analysis['keyword_analysis']
        for keyword, data in keyword_analysis['target_keywords'].items():
            if not data['optimal']:
                if data['density'] < 0.5:
                    recommendations.append({
                        'type': 'keywords',
                        'priority': 'medium',
                        'issue': f'Baja densidad de palabra clave "{keyword}"',
                        'recommendation': f'Aumentar uso de "{keyword}" (actual: {data["density"]:.1f}%, objetivo: 1-2%)',
                        'seo_impact': 'Mejor posicionamiento para términos objetivo'
                    })
                elif data['density'] > 3.0:
                    recommendations.append({
                        'type': 'keywords',
                        'priority': 'high',
                        'issue': f'Sobreoptimización de "{keyword}"',
                        'recommendation': f'Reducir uso de "{keyword}" (actual: {data["density"]:.1f}%, máximo: 3%)',
                        'seo_impact': 'Evita penalizaciones por keyword stuffing'
                    })
        
        # Readability recommendations
        readability = analysis['readability_seo']
        if readability['seo_readability'] in ['fair', 'poor']:
            recommendations.append({
                'type': 'readability',
                'priority': 'high',
                'issue': f'Legibilidad SEO {readability["seo_readability"]}',
                'recommendation': 'Simplificar vocabulario y reducir longitud de oraciones',
                'seo_impact': 'Mejor experiencia de usuario y tiempo de permanencia'
            })
        
        # Content quality recommendations
        content = analysis['content_quality']
        if content['engagement_score'] < 0.3:
            recommendations.append({
                'type': 'engagement',
                'priority': 'medium',
                'issue': 'Bajo potencial de engagement',
                'recommendation': 'Añadir palabras de acción, preguntas o elementos interactivos',
                'seo_impact': 'Mejora métricas de engagement'
            })
        
        return recommendations
    
    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate overall SEO score"""
        
        # Weight different aspects
        structure_weight = 0.25
        keyword_weight = 0.30
        readability_weight = 0.25
        content_weight = 0.20
        
        # Get individual scores
        structure_score = analysis['text_structure']['structure_score']
        
        # Keyword score (average of target keyword optimization)
        keyword_scores = [data['density'] / 2.0 for data in analysis['keyword_analysis']['target_keywords'].values()]
        keyword_score = sum(keyword_scores) / len(keyword_scores) if keyword_scores else 0.5
        keyword_score = min(1.0, keyword_score)
        
        readability_score = analysis['readability_seo']['readability_score']
        
        content_score = (
            analysis['content_quality']['content_depth_score'] +
            analysis['content_quality']['engagement_score'] +
            analysis['content_quality']['structure_score']
        ) / 3
        
        # Calculate weighted overall score
        overall_score = (
            structure_score * structure_weight +
            keyword_score * keyword_weight +
            readability_score * readability_weight +
            content_score * content_weight
        )
        
        return {
            'overall': overall_score,
            'structure': structure_score,
            'keywords': keyword_score,
            'readability': readability_score,
            'content': content_score
        }
    
    def optimize_for_seo(self, text: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """Provide specific SEO optimizations"""
        
        analysis = self.analyze_seo_comprehensive(text, target_keywords)
        
        # Generate specific optimization suggestions
        optimizations = {
            'title_suggestions': self._suggest_seo_titles(text, target_keywords or []),
            'meta_description_suggestions': self._suggest_meta_descriptions(text, target_keywords or []),
            'content_improvements': self._suggest_content_improvements(text, analysis),
            'keyword_integration': self._suggest_keyword_integration(text, target_keywords or [])
        }
        
        return {
            'analysis': analysis,
            'optimizations': optimizations,
            'priority_actions': self._get_priority_actions(analysis)
        }
    
    def _suggest_seo_titles(self, text: str, keywords: List[str]) -> List[str]:
        """Suggest SEO-optimized titles"""
        suggestions = []
        
        # Extract main topic (first sentence or paragraph)
        first_sentence = text.split('.')[0] if '.' in text else text[:100]
        
        # Create title variations
        if keywords:
            for keyword in keywords[:2]:  # Use first 2 keywords
                suggestions.append(f"Guía Completa: {keyword.title()}")
                suggestions.append(f"Cómo {keyword.title()} - Guía Práctica")
                suggestions.append(f"Todo sobre {keyword.title()} en 2024")
        
        # Generic title based on content
        if len(first_sentence) < 60:
            suggestions.append(first_sentence.title())
        
        return suggestions[:5]
    
    def _suggest_meta_descriptions(self, text: str, keywords: List[str]) -> List[str]:
        """Suggest SEO-optimized meta descriptions"""
        suggestions = []
        
        # Extract key information from first paragraph
        first_para = text.split('\n\n')[0] if '\n\n' in text else text[:200]
        
        # Create meta description variations
        base_description = first_para[:120] + "..."
        
        if keywords:
            keyword_desc = f"Descubre todo sobre {', '.join(keywords[:2])}. {first_para[:100]}..."
            suggestions.append(keyword_desc)
        
        suggestions.append(base_description)
        suggestions.append(f"Guía completa y actualizada. {first_para[:120]}...")
        
        return [desc for desc in suggestions if len(desc) <= 160][:3]
    
    def _suggest_content_improvements(self, text: str, analysis: Dict[str, Any]) -> List[str]:
        """Suggest content improvements for SEO"""
        improvements = []
        
        readability = analysis['readability_seo']
        if readability['avg_sentence_length'] > 25:
            improvements.append(f"Dividir oraciones largas (promedio: {readability['avg_sentence_length']:.1f} palabras)")
        
        content = analysis['content_quality']
        if content['questions'] == 0:
            improvements.append("Añadir preguntas para mejorar engagement")
        
        if content['lists'] == 0:
            improvements.append("Incluir listas con viñetas para mejor estructura")
        
        structure = analysis['text_structure']
        if len(structure['potential_headings']) == 0:
            improvements.append("Agregar subtítulos (H2, H3) para mejor estructura")
        
        return improvements
    
    def _suggest_keyword_integration(self, text: str, keywords: List[str]) -> Dict[str, List[str]]:
        """Suggest how to better integrate keywords"""
        suggestions = {}
        
        for keyword in keywords:
            keyword_suggestions = []
            
            # Suggest variations
            keyword_suggestions.append(f"Usar variaciones: {keyword}, {keyword}s, {keyword.replace(' ', '-')}")
            
            # Suggest placement
            keyword_suggestions.append("Incluir en el primer párrafo")
            keyword_suggestions.append("Usar en subtítulos cuando sea natural")
            keyword_suggestions.append("Incluir en la conclusión")
            
            suggestions[keyword] = keyword_suggestions
        
        return suggestions
    
    def _get_priority_actions(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get top priority SEO actions"""
        actions = []
        
        scores = analysis['seo_score']
        
        # Prioritize based on lowest scores
        if scores['readability'] < 0.6:
            actions.append({
                'action': 'Mejorar legibilidad',
                'priority': 'Alta',
                'impact': 'Tiempo de permanencia y experiencia de usuario'
            })
        
        if scores['structure'] < 0.6:
            actions.append({
                'action': 'Optimizar estructura del contenido',
                'priority': 'Alta', 
                'impact': 'Mejor indexación y navegabilidad'
            })
        
        if scores['keywords'] < 0.4:
            actions.append({
                'action': 'Optimizar densidad de palabras clave',
                'priority': 'Media',
                'impact': 'Mejor posicionamiento en buscadores'
            })
        
        return actions[:3]  # Top 3 priority actions