import psycopg2
from psycopg2 import sql, OperationalError, errorcodes, errors
from dotenv import load_dotenv
load_dotenv(override=True)
import os

class PostgreSQLService:
    def __init__(self):
        self.dbname = os.environ.get("POSTGRESQL_DB")
        self.user = os.environ.get("POSTGRESQL_USER")
        self.password = os.environ.get("POSTGRESQL_PASSWORD")
        self.host = os.environ.get("POSTGRESQL_HOST")
        self.port = 5432
        self.connection = None

    def connect_postgresql(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            if e.pgcode == errorcodes.INVALID_PASSWORD:
                print("Invalid password")
            elif e.pgcode == errorcodes.INVALID_CATALOG_NAME:
                print("Database does not exist")
            else:
                print(f"An error occurred: {e}")
    
    def execute_postgresql_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully")
        except Exception as e:
            self.connection.rollback()
            print(f"Failed to execute query: {e}")
        finally:
            cursor.close()
    
    def fetch_postgresql_data(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Failed to fetch results: {e}")
            return None
        finally:
            cursor.close()

    def close_postgresql_connection(self):
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection closed")