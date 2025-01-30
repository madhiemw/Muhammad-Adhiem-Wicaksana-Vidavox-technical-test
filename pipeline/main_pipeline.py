from config import Config
from pipeline.embeddings import EmbeddingPipeline
from pipeline.chromadb_search import ChromaDBPipeline
from pipeline.document_processor import DocumentProcessor
from pipeline.standard_agent import GroqPipeline
from pipeline.sql_query import MYSQL_Generator
from pipeline.sql_response import DB_Response_Generator
from utils.regex import remove_table_and_text, detect_none_in_text, remove_unnecesery_table
from utils.mysql_util import MySQLDatabase_execute

class QAPipeline:
    def __init__(self, config: Config):
        self.config = config
        self.embedding_pipeline = EmbeddingPipeline()
        self.chromadb_pipeline = ChromaDBPipeline(config)
        self.document_processor = DocumentProcessor()
        self.groq_pipeline = GroqPipeline(config)
        self.sql_generator = MYSQL_Generator(config)
        self.sql_execute = MySQLDatabase_execute(config)  
        self.sql_response = DB_Response_Generator(config)

    def process(self, question: str, collection_name: str):
        """Run the complete QA pipeline and return retrieved documents + AI response"""
        try:
            if collection_name == "QnA data":
                    collection_name = "test11"
            elif collection_name == "Semantic Data":
                    collection_name = "test12"
             
            embedding = self.embedding_pipeline.process(question)

            search_results = self.chromadb_pipeline.query(
                embedding, 
                collection_name  
            )

            retrieved_text = self.document_processor.process(search_results)
            
            if not retrieved_text:
                return "No relevant documents found.", "No relevant information found."

            response = self.groq_pipeline.generate_response(retrieved_text, question)
            tabledetect = remove_table_and_text(response)
            if tabledetect == False:
                cleaned_response = remove_unnecesery_table(response)
                return retrieved_text, cleaned_response
            else: 
                cleaned_response = remove_unnecesery_table(response )
                generateqsl = self.sql_generator.generate_response(question)
                if generateqsl is not None:
                    sql_execute = self.sql_execute.execute_query(generateqsl)
                    if sql_execute == "None":
                         return retrieved_text, cleaned_response
                    else: 
                        sql_response = self.sql_response.generate_response(context=question, db_result=sql_execute, sqlcode=generateqsl)
                        final_response = cleaned_response + "\n\n --------connected with SQL Agent--------\n\n--------Database analyzing result--------\n\n" + sql_response
                    return retrieved_text, final_response
                else :
                    return retrieved_text, cleaned_response
                
        except Exception as e:
            return f"Error retrieving documents: {str(e)}", f"Pipeline error: {str(e)}"
