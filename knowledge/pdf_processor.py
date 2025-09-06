import os
from typing import List, Dict, Any
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFProcessor:
    """Handles PDF content extraction and processing"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def extract_text(self) -> List[Dict[str, Any]]:
        """Extract text from PDF and split into chunks"""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        
        # Load PDF
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        
        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Format chunks with metadata
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            processed_chunks.append({
                "id": f"chunk_{i}",
                "content": chunk.page_content,
                "metadata": {
                    "source": self.pdf_path,
                    "page": chunk.metadata.get("page", 0),
                    "chunk_index": i,
                    "length": len(chunk.page_content)
                }
            })
        
        return processed_chunks
    
    def extract_sections(self) -> Dict[str, List[str]]:
        """Extract content organized by sections"""
        chunks = self.extract_text()
        
        sections = {
            "grammar": [],
            "style": [],
            "internet_writing": [],
            "seo": [],
            "punctuation": [],
            "general": []
        }
        
        for chunk in chunks:
            content = chunk["content"].lower()
            
            # Classify chunk by content keywords
            if any(keyword in content for keyword in ["gramática", "concordancia", "verbo", "sustantivo"]):
                sections["grammar"].append(chunk)
            elif any(keyword in content for keyword in ["estilo", "claridad", "lenguaje claro"]):
                sections["style"].append(chunk)
            elif any(keyword in content for keyword in ["internet", "web", "online", "digital"]):
                sections["internet_writing"].append(chunk)
            elif any(keyword in content for keyword in ["seo", "buscador", "optimización"]):
                sections["seo"].append(chunk)
            elif any(keyword in content for keyword in ["puntuación", "coma", "punto", "signo"]):
                sections["punctuation"].append(chunk)
            else:
                sections["general"].append(chunk)
        
        return sections
    
    def get_chunk_by_page(self, page_number: int) -> List[Dict[str, Any]]:
        """Get all chunks from a specific page"""
        chunks = self.extract_text()
        return [chunk for chunk in chunks if chunk["metadata"]["page"] == page_number]
    
    def search_content(self, query: str) -> List[Dict[str, Any]]:
        """Simple text search in PDF content"""
        chunks = self.extract_text()
        query_lower = query.lower()
        
        matching_chunks = []
        for chunk in chunks:
            if query_lower in chunk["content"].lower():
                # Calculate relevance score
                score = chunk["content"].lower().count(query_lower)
                chunk["relevance_score"] = score
                matching_chunks.append(chunk)
        
        # Sort by relevance
        return sorted(matching_chunks, key=lambda x: x["relevance_score"], reverse=True)