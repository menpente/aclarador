from typing import Dict, List, Any
from .base_agent import BaseAgent

class GrammarAgent(BaseAgent):
    """Agent for grammar and syntax corrections"""
    
    def __init__(self):
        super().__init__("Grammar")
    
    def analyze(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze grammar and suggest corrections"""
        return {
            "corrections": self._find_grammar_issues(text),
            "confidence": 0.85,
            "agent": self.name
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "grammar_correction",
            "punctuation_fixing",
            "sentence_structure",
            "agreement_checking"
        ]
    
    def _find_grammar_issues(self, text: str) -> List[Dict[str, str]]:
        """Find grammar issues (placeholder implementation)"""
        corrections = []
        
        # Basic checks for demonstration
        if "que que" in text.lower():
            corrections.append({
                "type": "grammar",
                "original": "que que",
                "corrected": "que",
                "reason": "Repetición innecesaria de 'que'",
                "pdf_reference": "Sección de conectores"
            })
        
        # Check for missing accents (basic example)
        accent_pairs = [
            ("mas", "más"),
            ("si", "sí"),
            ("tu", "tú"),
            ("el", "él")
        ]
        
        for original, corrected in accent_pairs:
            if f" {original} " in text.lower():
                corrections.append({
                    "type": "grammar",
                    "original": original,
                    "corrected": corrected,
                    "reason": f"Posible falta de acento en '{original}'",
                    "pdf_reference": "Sección de acentuación"
                })
        
        return corrections