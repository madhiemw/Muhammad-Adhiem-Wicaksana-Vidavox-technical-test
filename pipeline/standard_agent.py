import requests
from typing import Dict
from config import Config
class GroqPipeline:
    def __init__(self, config: Config):
        self.api_url = config.GROQ_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.GROQ_API_KEY}"
        }
    
    def generate_response(self, context: str, question: str) -> str:
        """Generate response using Groq API"""
        try:
            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{
                    "role": "user",
                    "content": (f"embedding result: {context}\n"
                              f"Answer the following user question: {question}, "
                              "the name of the robot is AV-826 "
                              "and answer it as a professional CS."
                              "just use embedding result as a fact for the answer and "
                              "if the question is has relation with effecency just add '#table' tag as a regex at the end of your output the db contain data about" "av-826 testing data and performance such as operation temperature and sensor accuracy"
                              "dont create any fake data, fake table or fake sql code. just summary the embedding result"
                              "if the question doesnt has relation with the robot product give polite feedback")
                }],
                "temperature": 0.1
            }
            
            response = requests.post(self.api_url, json=data, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                raise Exception(f"Groq API error: {response.status_code}")
        except Exception as e:
            raise Exception(f"Groq generation error: {str(e)}")
