import requests
from config import Config
from utils.regex import extract_sql_query

class MYSQL_Generator:
    def __init__(self, config: Config):
        self.api_url = config.GROQ_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.GROQ_API_KEY}"
        }

    def generate_response(self, context: str) -> str:
        """Generate SQL query using Groq API"""
        try:
            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{
                    "role": "user",
                    "content": (f"question: {context}\n"
                                "the table name is vidavox"
                                "the table is about av826 testing data"
                                "---below is the column table of MySQL db---"
                                "test_id VARCHAR(10) PRIMARY KEY,test_date DATE,model_name VARCHAR(50),noise_level_db DECIMAL(5, 2),cleaning_efficiency_percent DECIMAL(5, 2), battery_duration_minutes INT, area_covered_sqm DECIMAL(10, 2), dust_collection_grams DECIMAL(10, 2), operating_temperature_celsius DECIMAL(5, 2),maintenance_score DECIMAL(5, 2), navigation_accuracy_percent DECIMAL(5, 2),software_version VARCHAR(50)"
                                "---and below is the data example from the DB---"
                                "('TST0000020', '2024-01-07', 'AV826', 56.9, 95.8, 112, 42.41, 87.0, 26.6, 9, 96.9, 'v2.1.0')"
                                "your task is to generate just 1 MySQL code relateed above column and dont create any description to answer user question just use MySQL code "
                                "always limit the data only 10 line "
                                "dont create any fake mysql code"
                                "return none if the question doesn't has relation with the column and example data above"
                                )
                }],
                "temperature": 0.1
            }

            response = requests.post(self.api_url, json=data, headers=self.headers)

            if response.status_code == 200:
                response_text = response.json()['choices'][0]['message']['content']
                return extract_sql_query(response_text)
            else:
                raise Exception(f"Groq API error: {response.status_code}, {response.text}")

        except Exception as e:
            return str(e)
