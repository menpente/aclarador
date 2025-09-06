from typing import List, Dict, Any, Optional
from .vector_store import VectorStore

class KnowledgeRetrieval:
    """Handles retrieval of relevant guidelines from the PDF knowledge base"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def get_relevant_guidelines(self, 
                              text: str, 
                              agent_type: str, 
                              issues: List[str] = None,
                              n_results: int = 3) -> List[Dict[str, Any]]:
        """Get relevant guidelines based on text and agent type"""
        
        # Create context-aware query
        query_parts = [text[:200]]  # First 200 chars of text
        
        # Add agent-specific keywords
        agent_keywords = {
            "grammar": ["gramática", "concordancia", "sintaxis", "verbo"],
            "style": ["estilo", "claridad", "lenguaje claro", "oraciones"],
            "seo": ["SEO", "internet", "web", "buscadores", "optimización"],
            "validator": ["principios", "lenguaje claro", "validación"]
        }
        
        if agent_type in agent_keywords:
            query_parts.extend(agent_keywords[agent_type])
        
        # Add issue-specific terms
        if issues:
            issue_keywords = {
                "long_sentence": ["oraciones largas", "treinta palabras", "simplificar"],
                "complex_vocabulary": ["vocabulario", "palabras complejas", "jerga"],
                "passive_voice": ["voz pasiva", "voz activa", "sujeto verbo"],
                "grammar_error": ["gramática", "error gramatical", "corrección"]
            }
            
            for issue in issues:
                if issue in issue_keywords:
                    query_parts.extend(issue_keywords[issue])
        
        query = " ".join(query_parts)
        
        # Search by category if possible
        if agent_type in ["grammar", "style", "seo"]:
            results = self.vector_store.search_by_category(query, agent_type, n_results)
        else:
            results = self.vector_store.search(query, n_results)
        
        return self._format_guidelines(results, agent_type)
    
    def get_guidelines_for_text_type(self, 
                                   text_type: str,
                                   specific_query: str = None,
                                   n_results: int = 3) -> List[Dict[str, Any]]:
        """Get guidelines specific to text type"""
        
        type_queries = {
            "web": "escritura internet web online SEO",
            "document": "documentos formales estructura clara",
            "marketing": "marketing comunicación persuasiva",
            "short": "textos cortos mensajes breves"
        }
        
        base_query = type_queries.get(text_type, "lenguaje claro principios")
        
        if specific_query:
            query = f"{base_query} {specific_query}"
        else:
            query = base_query
        
        results = self.vector_store.search(query, n_results)
        return self._format_guidelines(results, f"text_type_{text_type}")
    
    def get_correction_examples(self, 
                              correction_type: str,
                              n_results: int = 2) -> List[Dict[str, Any]]:
        """Get examples of specific types of corrections"""
        
        example_queries = {
            "sentence_length": "ejemplo oración larga corta simplificar",
            "passive_voice": "ejemplo voz pasiva activa antes después",
            "jargon": "ejemplo jerga lenguaje sencillo técnico",
            "structure": "ejemplo estructura clara orden lógico"
        }
        
        query = example_queries.get(correction_type, f"ejemplo {correction_type}")
        results = self.vector_store.search(query, n_results)
        
        return self._format_guidelines(results, f"examples_{correction_type}")
    
    def _format_guidelines(self, 
                          results: List[Dict[str, Any]], 
                          context: str) -> List[Dict[str, Any]]:
        """Format search results as guidelines"""
        
        guidelines = []
        for result in results:
            guideline = {
                "content": result["content"],
                "source": "Manual de estilo de lenguaje claro",
                "page": result["metadata"].get("page", "Unknown"),
                "relevance": 1 - (result.get("distance", 0.5) if result.get("distance") else 0.5),
                "context": context,
                "chunk_id": result["id"],
                "reference": f"Manual de lenguaje claro, página {result['metadata'].get('page', '?')}"
            }
            guidelines.append(guideline)
        
        return guidelines
    
    def get_principle_explanation(self, principle: str) -> Optional[Dict[str, Any]]:
        """Get explanation of a specific lenguaje claro principle"""
        
        principles_map = {
            "one_idea_per_sentence": "una idea por oración principio",
            "max_30_words": "treinta palabras máximo oración",
            "avoid_jargon": "evitar jerga lenguaje técnico",
            "active_voice": "voz activa pasiva sujeto verbo predicado",
            "logical_structure": "estructura lógica organización información"
        }
        
        query = principles_map.get(principle, principle)
        results = self.vector_store.search(query, n_results=1)
        
        if results:
            return self._format_guidelines(results, f"principle_{principle}")[0]
        
        return None
    
    def search_by_keywords(self, keywords: List[str], n_results: int = 5) -> List[Dict[str, Any]]:
        """Search using specific keywords"""
        query = " ".join(keywords)
        results = self.vector_store.search(query, n_results)
        return self._format_guidelines(results, "keyword_search")