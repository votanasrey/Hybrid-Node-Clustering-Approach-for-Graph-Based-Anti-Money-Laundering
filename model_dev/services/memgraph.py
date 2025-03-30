from gqlalchemy import Memgraph #type: ignore
from dotenv import load_dotenv  #type: ignore
import os
load_dotenv(override=True)

class MemgraphClient:
    def __init__(self, 
            host=os.getenv("MEMGRAPH_HOST"), 
            port=int(os.getenv("MEMGRAPH_PORT"))
        ):
        self.host = host
        self.port = port
        self.connection = self.connect()

    def connect(self):
        try:
            memgraph = Memgraph(self.host, self.port)
            if memgraph._get_cached_connection().is_active():
                print(f"✅ Connected to Memgraph at {self.host}:{self.port}")
            return memgraph
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return None

    def execute_query(self, query, params=None):
        if not self.connection:
            print("⚠️ No active Memgraph connection.")
            return []
        try:
            return list(self.connection.execute_and_fetch(query, params or {}))
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            return []