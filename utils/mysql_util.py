import mysql.connector
from config import Config

class MySQLDatabase_execute:
    def __init__(self, config: Config):
        self.config = config
        self.connection = None

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config.MYSQL_HOST,
                user=self.config.MYSQL_USER,
                password=self.config.MYSQL_PASSWORD,
                database=self.config.MYSQL_DATABASE,
                port=self.config.MYSQL_PORT
            )
            print("Connected to MySQL database successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def execute_query(self, query):
        """Execute the SQL query and return the results"""
        try:
            if self.connection is None:
                self.connect()

            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as err:
            print(f"Query Error: {err}")
            return None

    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
