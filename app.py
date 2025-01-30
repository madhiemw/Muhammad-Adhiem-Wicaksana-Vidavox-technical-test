import gradio as gr
from config import Config
from pipeline.main_pipeline import QAPipeline
from typing import List

def create_app():
    config = Config()
    pipeline = QAPipeline(config)

    def process_message(message: str, collection_name: str, history: List[List[str]]):
        retrieved_docs, response = pipeline.process(message, collection_name)
        return response, retrieved_docs  

    interface = gr.Interface(
        fn=process_message,
        inputs=[
            gr.Textbox(label="Your Question"),  
            gr.Dropdown(choices=["QnA data", "Semantic Data"], label="Select Collection", value="Semantic Data") 
        ],
        outputs=[
            gr.Textbox(label="AI Response"),  
            gr.Textbox(label="Retrieved Documents from ChromaDB"),  
        ],
        title="Muhammad Adhiem Wicaksana Vidavox Technical Test",
        description="Ask questions and choose a crhoma db collection, read my documentation for the purpose of the collection :)",
    )

    return interface

if __name__ == "__main__":
    app = create_app()
    app.launch()
