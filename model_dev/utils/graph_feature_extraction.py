import sys
import os
from dotenv import load_dotenv #type: ignore
load_dotenv(override=True)
sys.path.append(os.getenv("PROJECT_PATH"))

from services.memgraph import MemgraphClient
mg_client = MemgraphClient()

query = "MATCH (a:Account) RETURN a.account_id, a.bank LIMIT 10"
results = mg_client.execute_query(query)

if results:
    for row in results:
        print(row)