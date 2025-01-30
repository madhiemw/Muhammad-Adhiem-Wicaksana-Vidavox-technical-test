import chromadb
from typing import List, Dict, Any
from config import Config

class ChromaDBPipeline:
    def __init__(self, config: Config):
        self.client = chromadb.HttpClient(
            host=config.CHROMADB_HOST,
            headers={"Authorization": f"Bearer {config.CHROMADB_TOKEN}"}
        )
        self.n_results = config.N_RESULTS
    
    def query(self, embedding: List[float], collection_name: str) -> Dict[str, Any]:
        """Search ChromaDB with embedding"""
        try:
            collection = self.client.get_collection(
                name=collection_name,
                embedding_function=None
            )
            return collection.query(
                query_embeddings=[embedding],
                n_results=self.n_results
            )
        except Exception as e:
            raise Exception(f"ChromaDB search error: {str(e)}")