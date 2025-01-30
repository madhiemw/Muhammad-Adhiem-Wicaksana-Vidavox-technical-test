from typing import List

class DocumentProcessor:
    @staticmethod
    def process(results: dict) -> str:
        """Process and combine ChromaDB results"""
        if not results or 'documents' not in results:
            return ""
        
        relevant_documents = results['documents']
        if isinstance(relevant_documents, list):
            if relevant_documents and isinstance(relevant_documents[0], list):
                relevant_documents = [item for sublist in relevant_documents for item in sublist]
            relevant_documents = [str(doc) for doc in relevant_documents]
        
        return " ".join(relevant_documents)
