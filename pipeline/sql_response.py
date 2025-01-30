import requests
from config import Config

class DB_Response_Generator:
    def __init__(self, config: Config):
        self.api_url = config.GROQ_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.GROQ_API_KEY}"
        }

    def generate_response(self, context: str, db_result:str, sqlcode:str) -> str:
        """Generate SQL query using Groq API"""
        try:
            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{
                    "role": "user",
                    "content": (f"question: {context}\n"
                                "heres the table column test_id,test_date,model_name,noise_level_db,cleaning_efficiency_percent, battery_duration_minutes INT,"
                                "area_covered_sqm, dust_collection_grams, operating_temperature_celsius ,maintenance_score, navigation_accuracy_percent ,software_version\n"
                                f"and heres the sql code: {sqlcode} "
                                "below is result of sql query\n"
                                f"{db_result}\n"
                                "make summary and use non technical sentence to explain it into user and use it to answer user question ")
                }],
                "temperature": 0.1
            }

            response = requests.post(self.api_url, json=data, headers=self.headers)

            if response.status_code == 200:
                response_text = response.json()['choices'][0]['message']['content']
                return response_text
            else:
                raise Exception(f"Groq API error: {response.status_code}, {response.text}")

        except Exception as e:
            return str(e)
