from gqlalchemy import Memgraph
import os
from dotenv import load_dotenv
import pandas as pd
import json
import datetime
load_dotenv()


class memgraph_service:

    def __init__(self):
        """
            A init function to connect to the memgraph database 
        """
        self.mg = Memgraph(os.environ.get("MEMGRAPH_HOST"), 7687)
      
    def create_transaction(self, transaction):
        """
            A function to create a transaction record in the graph database
        """
        
        query = '''
        MERGE (tr:TM_TRANSACTION_RECORD {id: $CUST_NO})
        ON CREATE SET
            tr.CIF_CREATION_DATE = date($CIF_CREATION_DATE),
            tr.RECEIVED_AMOUNT = toFloat($RECEIVED_AMOUNT)
        RETURN tr
        '''
        
        try:
            data = self.mg.execute_and_fetch(query, transaction)
            data = list(data)[0]
            print(data)
            return data
        
        except Exception as e:
            print(f"Error inserting transaction: {e}")
            return None