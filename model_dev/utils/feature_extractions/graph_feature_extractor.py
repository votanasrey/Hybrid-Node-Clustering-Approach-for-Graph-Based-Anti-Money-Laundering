import sys
import os
from dotenv import load_dotenv #type: ignore
load_dotenv(override=True)
sys.path.append(os.getenv("PROJECT_PATH"))
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict
import logging

from services.memgraph import MemgraphClient
mg_client = MemgraphClient()


class GraphFeatureExtractor:
    def __init__(self):
        self.mg_client = MemgraphClient()
    
    def extract_node_static_features(self) -> List[Dict[str, Any]]:
        try: 
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
                    t.usd_amount AS usd_amount,
                    COUNT(DISTINCT receiver.account_id) AS num_receivers
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
        except Exception as e:
            logging.error(f"Eror to extract the graph features: {e}")

    def extract_node_aggregrate_features(self) -> List[Dict[str, Any]]:
        try: 
            query = '''
                MATCH (a:Account)-[:FROM]->(t:Transaction)-[:TO]->(receiver:Account)
                RETURN DISTINCT 
                    a.account_id AS account_id,
                    COUNT(DISTINCT t.transaction_id) AS num_transactions,
                    COUNT(DISTINCT CASE WHEN t.is_laundering = 1 THEN receiver.account_id END) AS num_fraud_transactions,
                    COUNT(DISTINCT receiver.account_id) AS num_receivers
            '''
            features = self.mg_client.execute_query(query)
            account_map = defaultdict(list)
            for f in features:
                account_map[f["account_id"]].append(f)

            account_feature_list = []
            for account_id, rows in account_map.items():
                account_features = {
                    "account_id": account_id,
                    "num_transactions": rows[0]["num_transactions"],
                    "num_fraud_transactions": rows[0]["num_fraud_transactions"],
                    "num_receivers": rows[0]["num_receivers"]
                }

                account_feature_list.append(account_features)
            return account_feature_list
        except Exception as e:
            logging.error(f"Eror to extract the graph features: {e}")


if __name__ == "__main__":
    graph_extractor = GraphFeatureExtractor()
    features_for_ml = graph_extractor.extract_node_aggregrate_features()
    print(features_for_ml)