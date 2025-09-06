#!/usr/bin/env python3
"""
Script to initialize the knowledge base from PDF content
"""

import os
from knowledge.pdf_processor import PDFProcessor
from knowledge.vector_store import VectorStore

def setup_knowledge_base(pdf_path: str, force_reload: bool = False):
    """Initialize the knowledge base with PDF content"""
    
    print("Setting up knowledge base...")
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return False
    
    try:
        # Initialize vector store
        print("Initializing vector store...")
        vector_store = VectorStore(
            collection_name="lenguaje_claro",
            persist_directory="./chroma_db"
        )
        
        # Add PDF content
        print(f"Processing PDF: {pdf_path}")
        vector_store.add_pdf_content(pdf_path, force_reload=force_reload)
        
        # Get collection info
        info = vector_store.get_collection_info()
        print(f"Knowledge base setup complete!")
        print(f"Collection: {info['name']}")
        print(f"Documents: {info['count']}")
        
        # Test search
        print("\nTesting search functionality...")
        results = vector_store.search("lenguaje claro oraciones", n_results=2)
        for i, result in enumerate(results, 1):
            print(f"  {i}. Found content from page {result['metadata']['page']}")
            print(f"     Preview: {result['content'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"Error setting up knowledge base: {e}")
        return False

if __name__ == "__main__":
    # Path to the PDF manual
    pdf_path = "ref/Manual de estilo de lenguaje claro.pdf"
    
    # Setup with option to force reload
    import sys
    force_reload = "--force" in sys.argv
    
    success = setup_knowledge_base(pdf_path, force_reload=force_reload)
    
    if success:
        print("\nKnowledge base is ready for use!")
        print("You can now run the enhanced application.")
    else:
        print("\nFailed to setup knowledge base.")
        print("Please check the error messages above.")