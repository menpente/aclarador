import os
import chromadb
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from .pdf_processor import PDFProcessor

class VectorStore:
    """Manages vector database for PDF content retrieval"""
    
    def __init__(self, collection_name: str = "lenguaje_claro", persist_directory: str = "./chroma_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Spanish plain language style guide content"}
            )
    
    def add_pdf_content(self, pdf_path: str, force_reload: bool = False):
        """Add PDF content to vector store"""
        if not force_reload and self.collection.count() > 0:
            print(f"Collection already has {self.collection.count()} documents. Use force_reload=True to reload.")
            return
        
        # Extract PDF content
        processor = PDFProcessor(pdf_path)
        chunks = processor.extract_text()
        
        if not chunks:
            raise ValueError("No content extracted from PDF")
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for chunk in chunks:
            documents.append(chunk["content"])
            metadatas.append(chunk["metadata"])
            ids.append(chunk["id"])
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Add to collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Added {len(chunks)} chunks to vector store")
    
    def search(self, query: str, n_results: int = 5, filter_metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Search for relevant content"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None,
                    "id": results['ids'][0][i]
                })
        
        return formatted_results
    
    def search_by_category(self, query: str, category: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search within specific category"""
        category_keywords = {
            "grammar": ["gramática", "concordancia", "verbo", "sustantivo"],
            "style": ["estilo", "claridad", "lenguaje claro"],
            "internet": ["internet", "web", "online", "digital"],
            "seo": ["seo", "buscador", "optimización"],
            "punctuation": ["puntuación", "coma", "punto", "signo"]
        }
        
        # Enhanced query with category keywords
        if category in category_keywords:
            enhanced_query = f"{query} {' '.join(category_keywords[category])}"
        else:
            enhanced_query = query
        
        return self.search(enhanced_query, n_results)
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        return {
            "name": self.collection_name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata
        }
    
    def clear_collection(self):
        """Clear all documents from collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Spanish plain language style guide content"}
            )
            print("Collection cleared successfully")
        except Exception as e:
            print(f"Error clearing collection: {e}")
    
    def get_similar_chunks(self, reference_chunk_id: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Find chunks similar to a reference chunk"""
        # Get the reference chunk
        reference_result = self.collection.get(ids=[reference_chunk_id])
        
        if not reference_result['documents']:
            return []
        
        reference_text = reference_result['documents'][0]
        
        # Search for similar content
        return self.search(reference_text, n_results + 1)[1:]  # Exclude the reference chunk itself