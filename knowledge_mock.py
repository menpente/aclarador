"""
Mock knowledge base system for Phase 3 demonstration
Uses pre-extracted content instead of PDF processing
"""

class MockKnowledgeBase:
    """Mock knowledge base with pre-defined Spanish language guidelines"""
    
    def __init__(self):
        self.guidelines = {
            "grammar": [
                {
                    "content": "La concordancia entre sujeto y verbo es fundamental en español. El verbo debe concordar en número y persona con el sujeto. Ejemplo: 'Los estudiantes estudian' (no 'Los estudiantes estudia').",
                    "page": 45,
                    "relevance": 0.95,
                    "reference": "Manual de lenguaje claro, página 45",
                    "context": "grammar"
                },
                {
                    "content": "Los signos de puntuación deben usarse correctamente. La coma separa elementos de una enumeración, excepto antes de 'y', 'e', 'o', 'u'. Ejemplo: 'Juan, Pedro, María y Ana'.",
                    "page": 52,
                    "relevance": 0.88,
                    "reference": "Manual de lenguaje claro, página 52", 
                    "context": "grammar"
                }
            ],
            "style": [
                {
                    "content": "Una oración debe expresar una sola idea principal. Las oraciones largas dificultan la comprensión. Recomendación: máximo 30 palabras por oración para mantener la claridad.",
                    "page": 23,
                    "relevance": 0.92,
                    "reference": "Manual de lenguaje claro, página 23",
                    "context": "style"
                },
                {
                    "content": "Evite el uso de voz pasiva cuando sea posible. Prefiera la voz activa: 'El equipo realizó el proyecto' en lugar de 'El proyecto fue realizado por el equipo'.",
                    "page": 27,
                    "relevance": 0.85,
                    "reference": "Manual de lenguaje claro, página 27",
                    "context": "style"
                },
                {
                    "content": "Utilice palabras conocidas por su audiencia. Evite la jerga técnica o explíquela cuando sea necesaria. Ejemplo: use 'comenzar' en lugar de 'inicializar'.",
                    "page": 31,
                    "relevance": 0.90,
                    "reference": "Manual de lenguaje claro, página 31",
                    "context": "style"
                }
            ],
            "seo": [
                {
                    "content": "Para contenido web, mantenga los títulos entre 50-60 caracteres para SEO óptimo. Los títulos largos se truncan en resultados de búsqueda, perdiendo impacto.",
                    "page": 78,
                    "relevance": 0.87,
                    "reference": "Manual de lenguaje claro, página 78",
                    "context": "seo"
                },
                {
                    "content": "Balance la densidad de palabras clave (1-2%) con la legibilidad. No sacrifique la claridad por el SEO. Los buscadores valoran el contenido útil y bien escrito.",
                    "page": 82,
                    "relevance": 0.83,
                    "reference": "Manual de lenguaje claro, página 82",
                    "context": "seo"
                }
            ],
            "general": [
                {
                    "content": "Los principios del lenguaje claro buscan que la comunicación sea efectiva, accesible y comprensible para la audiencia objetivo. Esto incluye estructura lógica, vocabulario apropiado y formato adecuado.",
                    "page": 12,
                    "relevance": 0.94,
                    "reference": "Manual de lenguaje claro, página 12",
                    "context": "general"
                },
                {
                    "content": "La estructura lógica organiza la información del general al particular, o en orden cronológico. Use encabezados, listas y párrafos cortos para mejorar la lectura.",
                    "page": 18,
                    "relevance": 0.89,
                    "reference": "Manual de lenguaje claro, página 18",
                    "context": "general"
                }
            ]
        }
    
    def get_relevant_guidelines(self, text, agent_type, issues=None, n_results=3):
        """Get relevant guidelines based on agent type and issues"""
        
        # Get guidelines for the specific agent type
        agent_guidelines = self.guidelines.get(agent_type, self.guidelines.get("general", []))
        
        # If we have issues, try to find more specific guidelines
        if issues:
            enhanced_guidelines = []
            for issue in issues:
                if issue == "long_sentence" and agent_type == "style":
                    enhanced_guidelines.extend([g for g in self.guidelines["style"] if "30 palabras" in g["content"]])
                elif issue == "complex_vocabulary" and agent_type == "style":
                    enhanced_guidelines.extend([g for g in self.guidelines["style"] if "jerga" in g["content"]])
                elif issue == "grammar_error" and agent_type == "grammar":
                    enhanced_guidelines.extend(self.guidelines["grammar"])
            
            if enhanced_guidelines:
                agent_guidelines = enhanced_guidelines
        
        # Return top results
        return agent_guidelines[:n_results]
    
    def get_guidelines_for_text_type(self, text_type, specific_query=None, n_results=3):
        """Get guidelines for specific text types"""
        
        if text_type == "web":
            return self.guidelines["seo"][:n_results]
        elif text_type in ["document", "formal"]:
            return self.guidelines["general"][:n_results]
        else:
            return self.guidelines["style"][:n_results]
    
    def search_by_keywords(self, keywords, n_results=3):
        """Search guidelines by keywords"""
        results = []
        
        for category, guidelines in self.guidelines.items():
            for guideline in guidelines:
                # Simple keyword matching
                content_lower = guideline["content"].lower()
                if any(keyword.lower() in content_lower for keyword in keywords):
                    results.append(guideline)
        
        return results[:n_results]

class MockVectorStore:
    """Mock vector store for compatibility"""
    
    def __init__(self):
        self.knowledge_base = MockKnowledgeBase()
    
    def get_collection_info(self):
        """Return mock collection info"""
        return {
            "name": "mock_lenguaje_claro",
            "count": 8,  # Total number of guidelines
            "metadata": {"description": "Mock Spanish plain language guidelines"}
        }
    
    def search(self, query, n_results=5):
        """Mock search functionality"""
        # Simple keyword extraction from query
        keywords = query.split()
        return self.knowledge_base.search_by_keywords(keywords, n_results)

class MockKnowledgeRetrieval:
    """Mock knowledge retrieval system"""
    
    def __init__(self):
        self.knowledge_base = MockKnowledgeBase()
    
    def get_relevant_guidelines(self, text, agent_type, issues=None, n_results=3):
        """Get relevant guidelines"""
        return self.knowledge_base.get_relevant_guidelines(text, agent_type, issues, n_results)
    
    def get_guidelines_for_text_type(self, text_type, specific_query=None, n_results=3):
        """Get guidelines for text type"""
        return self.knowledge_base.get_guidelines_for_text_type(text_type, specific_query, n_results)
    
    def search_by_keywords(self, keywords, n_results=5):
        """Search by keywords"""
        return self.knowledge_base.search_by_keywords(keywords, n_results)
    
    def get_principle_explanation(self, principle):
        """Get explanation of specific principle"""
        principle_map = {
            "one_idea_per_sentence": self.knowledge_base.guidelines["style"][0],
            "max_30_words": self.knowledge_base.guidelines["style"][0], 
            "avoid_jargon": self.knowledge_base.guidelines["style"][2],
            "active_voice": self.knowledge_base.guidelines["style"][1]
        }
        
        return principle_map.get(principle)

# For compatibility with existing code
def get_mock_knowledge_system():
    """Get mock knowledge system components"""
    vector_store = MockVectorStore()
    retrieval = MockKnowledgeRetrieval()
    return vector_store, retrieval