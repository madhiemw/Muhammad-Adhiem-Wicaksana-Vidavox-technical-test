from sentence_transformers import SentenceTransformer

model = SentenceTransformer('LazarusNLP/all-indo-e5-small-v4')

def encode_query(query: str):
    """Encodes a query into an embedding vector using SentenceTransformer."""
    try:
        return model.encode([query])[0]  
    except Exception as e:
        raise Exception(f"Error encoding query: {str(e)}")
