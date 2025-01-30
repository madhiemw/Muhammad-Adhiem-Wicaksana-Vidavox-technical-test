from utils.sentence_transformer_util import encode_query

class EmbeddingPipeline:
    @staticmethod
    def process(text: str):
        """Convert input text to embedding"""
        chat = ("pertanyaan", text)
        return encode_query(chat)
