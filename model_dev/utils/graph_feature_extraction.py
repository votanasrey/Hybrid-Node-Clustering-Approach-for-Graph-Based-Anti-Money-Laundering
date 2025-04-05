import sys
import os
from dotenv import load_dotenv #type: ignore
load_dotenv(override=True)
sys.path.append(os.getenv("PROJECT_PATH"))
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict


from services.memgraph import MemgraphClient
mg_client = MemgraphClient()


class GraphFeatureExtractor:
    def __init__(self):
        self.mg_client = MemgraphClient()

    def run_pagerank(self) -> Dict[int, float]:
        query = '''
            CALL nxalg.pagerank() 
            YIELD node, rank
            WITH node, rank
            WHERE node:Account
            RETURN id(node) AS node_id, rank
            ORDER BY rank DESC
        '''
        results = self.mg_client.execute_query(query)
        print("Pagerank results:", results[10]) 
        return {row["node_id"]: row["rank"] for row in results}

    def run_betweenness_centrality(self) -> Dict[int, float]:
        query = '''
            CALL nxalg.betweenness_centrality() 
            YIELD node, betweenness
            WITH node, betweenness
            WHERE node:Account
            RETURN id(node) AS node_id, betweenness
            ORDER BY betweenness DESC
        '''
        results = self.mg_client.execute_query(query)
        print("Betweenness results:", results[10])  # Debugging
        return {row["node_id"]: row["betweenness"] for row in results}



    def update_node_properties(self, node_features: Dict[int, Dict[str, Any]]):
        for node_id, features in node_features.items():
            query = f'''
                MATCH (n:Account) WHERE id(n) = {node_id}
                SET {", ".join([f"n.{k} = {repr(v)}" for k, v in features.items() if v is not None])}
            '''
            self.mg_client.execute_query(query)
        print("ALL nodes updated the features of pagerank and betweeness")

    def extract_and_update_features(self):
        pagerank_scores = self.run_pagerank()
        betweenness_centrality = self.run_betweenness_centrality()
        node_features = {}
        for node_id in set(pagerank_scores.keys()).union(betweenness_centrality.keys()):
            features = {
                "pagerank": pagerank_scores.get(node_id, None),
                "betweenness": betweenness_centrality.get(node_id, None)
            }
            node_features[node_id] = features
        self.update_node_properties(node_features)

    def fetch_node_dynamic_features(self) -> List[Dict[str, Any]]:
        query = '''
            MATCH (n:Account)
            RETURN n.account_id AS node_id, n.pagerank AS pagerank, n.betweenness AS betweenness
        '''
        features = self.mg_client.execute_query(query)

        result_list = []
        for feature in features:
            result_dict = {key: feature[key] for key in feature}
            result_list.append(result_dict)

        return result_list
    
    def fetch_node_static_features(self) -> List[Dict[str, Any]]:
        query = '''
            MATCH (a:Account)-[:FROM]->(t:Transaction)-[:TO]->(receiver:Account)
            RETURN a.account_id AS account_id,
                a.bank AS bank,
                a.rank AS rank,
                a.betweenness AS betweenness,
                a.pagerank AS pagerank,
                t.amount_paid AS amount_paid,
                t.amount_received AS amount_received,
                t.is_laundering AS is_laundering,
                t.payment_currency AS payment_currency,
                t.payment_format AS payment_format,
                t.receiving_currency AS receiving_currency,
                t.timestamp AS timestamp,
                t.transaction_id AS transaction_id,
                t.usd_amount AS usd_amount
        '''
        features = self.mg_client.execute_query(query)
        account_map = defaultdict(list)
        for f in features:
            account_map[f["account_id"]].append(f)

        account_feature_list = []
        for account_id, rows in account_map.items():
            # Basic account-level info
            account_features = {
                "account_id": account_id,
                "bank": rows[0]["bank"],
                "rank": rows[0]["rank"],
                "betweenness": rows[0]["betweenness"],
                "pagerank": rows[0]["pagerank"]
            }

            # Aggregated transaction features
            total_paid = sum(f["amount_paid"] for f in rows)
            total_received = sum(f["amount_received"] for f in rows)
            total_usd_amount = sum(f["usd_amount"] for f in rows)
            num_transactions = len(rows)

            timestamps = [
                f["timestamp"] if isinstance(f["timestamp"], datetime)
                else datetime.strptime(f["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
                for f in rows if f["timestamp"] is not None
            ]
            timestamps.sort()
            if len(timestamps) > 1:
                time_diffs = [(timestamps[i] - timestamps[i - 1]).total_seconds() for i in range(1, len(timestamps))]
                avg_transaction_interval = sum(time_diffs) / len(time_diffs)
            else:
                avg_transaction_interval = None

            usd_transactions = sum(1 for f in rows if f["payment_currency"] == "US Dollar")
            usd_percentage = (usd_transactions / num_transactions) * 100 if num_transactions > 0 else 0

            account_features.update({
                "total_paid": total_paid,
                "total_received": total_received,
                "total_usd_amount": total_usd_amount,
                "num_transactions": num_transactions,
                "avg_transaction_interval": avg_transaction_interval,
                "usd_percentage": usd_percentage
            })

            account_feature_list.append(account_features)

        return account_feature_list


if __name__ == "__main__":
    graph_extractor = GraphFeatureExtractor()
    # graph_extractor.extract_and_update_features()
    features_for_ml = graph_extractor.fetch_node_static_features()
    print(features_for_ml)