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
            gr.Textbox(label="Your Question", placeholder="Enter your question here...", lines=2),  
            gr.Dropdown(
                choices=["QnA data", "Semantic Data"], 
                label="Select Collection", 
                value="Semantic Data"
            ) 
        ],
        outputs=[
            gr.Textbox(label="AI Response", interactive=False),  
            gr.Textbox(label="Retrieved Documents from ChromaDB", interactive=False, lines=5),  
        ],
        title="Vidavox AI Q&A System",
        description=(
            "Ask a question about the AV-826 Smart Robot and retrieve relevant information from ChromaDB. "
            "Select a data collection and explore the system's capabilities.\n\n"
            "**Example Questions:**\n"
            "- Apa saja nilai jual utama pada robot ini?\n"
            "- Apa saja yang robot ini dapat lakukan?\n"
            "- Apa saja kelebihan robot ini dibandingkan dengan kompetitor?\n"
            "- Apakah robot ini lebih baik dari kompetitor?\n"
            "- Jelaskan bagaimana kemampuan robot ini dalam memasak dan membersihkan rumah.\n"
            "- Apakah ada hal khusus yang harus diperhatikan untuk perawatan robot?\n"
            "- Bagaimana menghubungkan aplikasi dengan robot?\n"
            "- Apakah robot ini membutuhkan perawatan khusus?\n"
            "- Seberapa efisien robot ini dapat bekerja?\n"
            "- Bagaimana dengan daya tahan baterai yang dimiliki robot ini?\n"
            "- Bagaimana efisiensi robot ini dalam melakukan pembersihan rumah?"
        ),
        theme="compact",
    )

    return interface

if __name__ == "__main__":
    app = create_app()
    app.launch()
