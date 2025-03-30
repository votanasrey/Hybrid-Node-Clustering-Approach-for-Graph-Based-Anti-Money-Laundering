from services.memgraph import MemgraphClient

if __name__ == "__main__":
    mg_client = MemgraphClient()

    query = "MATCH (a:Account) RETURN a.account_id, a.bank LIMIT 10"
    results = mg_client.execute_query(query)

    if results:
        for row in results:
            print(row)