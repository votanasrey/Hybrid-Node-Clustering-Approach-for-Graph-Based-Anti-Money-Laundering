import sys
import os
from dotenv import load_dotenv  # type: ignore
load_dotenv(override=True)
sys.path.append(os.getenv("PROJECT_PATH"))
from typing import Dict, Any, List
from collections import defaultdict
import logging

from services.memgraph import MemgraphClient
mg_client = MemgraphClient()


class GraphFeatureExtractor:
    def __init__(self):
        self.mg_client = MemgraphClient()

    def extract_node_features(self) -> List[Dict[str, Any]]:
        try:
            query = '''
                MATCH (a:Account)-[:FROM]->(t:Transaction)-[:TO]->(r:Account)
                WITH 
                    a.account_id AS account_id,
                    a.bank AS bank,
                    a.betweenness AS betweenness,
                    a.pagerank AS pagerank,

                    COUNT(DISTINCT t.transaction_id) AS total_trxns,
                    COUNT(DISTINCT CASE WHEN t.is_laundering = 1 THEN r.account_id END) AS total_fraud_trxns,
                    COUNT(DISTINCT r.account_id) AS total_receivers,
                    SUM(t.usd_amount) AS total_usd_amount,
                    SUM(CASE WHEN t.is_laundering = 1 THEN t.usd_amount END) AS total_fraud_usd_amount,
                    AVG(t.usd_amount) AS avg_usd_amount,
                    MAX(t.usd_amount) AS max_usd_amount,
                    MIN(t.usd_amount) AS min_usd_amount, 

                    COUNT(CASE WHEN t.usd_amount < 1000 THEN 1 END) AS total_small_txns,
                    COUNT(CASE WHEN t.usd_amount > 12000 THEN 1 END) AS total_high_txns,
                    COUNT(CASE WHEN t.payment_format = "Cash" THEN 1 END) AS total_cash_txns,
                    COUNT(DISTINCT t.payment_format) AS unique_payment_formats,
                    COUNT(DISTINCT date(t.timestamp)) AS total_active_days,
                    MIN(localDatetime(t.timestamp)) AS first_trxns_datetime,
                    MAX(localDatetime(t.timestamp)) AS last_trxns_datetime

                WITH 
                    account_id,
                    bank,
                    betweenness,
                    pagerank,
                    total_trxns,
                    total_fraud_trxns,
                    total_receivers,
                    total_usd_amount,
                    total_fraud_usd_amount,
                    avg_usd_amount,
                    max_usd_amount,
                    min_usd_amount,
                    total_small_txns,
                    total_high_txns,
                    total_cash_txns,
                    unique_payment_formats,
                    total_active_days,

                    CASE WHEN total_active_days = 0 THEN 0 ELSE toFloat(total_trxns) / total_active_days END AS total_trxns_per_day,
                    CASE WHEN total_active_days = 0 THEN 0 ELSE toFloat(total_usd_amount) / total_active_days END AS total_usd_amount_per_day,
                    CASE WHEN total_receivers = 0 THEN 0 ELSE toFloat(total_usd_amount) / total_receivers END AS avg_usd_amount_per_receiver,
                    CASE WHEN total_usd_amount = 0 THEN 0 ELSE toFloat(total_fraud_usd_amount) / total_usd_amount END AS ratio_fraud_usd_amount,
                    CASE WHEN avg_usd_amount = 0 THEN 0 ELSE toFloat(max_usd_amount) / avg_usd_amount END AS ratio_max_to_avg,
                    CASE WHEN total_receivers = 0 THEN 0 ELSE toFloat(total_fraud_trxns) / total_receivers END AS ratio_fraud_receiver,
                    CASE WHEN total_trxns = 0 THEN 0 ELSE toFloat(total_cash_txns) / total_trxns END AS ratio_cash_trxns,
                    CASE WHEN total_trxns = 0 THEN 0 ELSE toFloat(total_small_txns) / total_trxns END AS ratio_small_trxns,
                    CASE WHEN total_trxns = 0 THEN 0 ELSE toFloat(total_high_txns) / total_trxns END AS ratio_high_trxns,

                    (pagerank * betweenness) AS pagerank_betweenness_interaction,
                    ABS(pagerank - betweenness) AS pagerank_betweenness_difference,
                    CASE WHEN betweenness = 0 THEN 0 ELSE pagerank / betweenness END AS ratio_pagerank_betweenness,
                    CASE WHEN total_trxns = 0 THEN 0 ELSE pagerank / total_trxns END AS ratio_pagerank_txn,
                    CASE WHEN avg_usd_amount = 0 THEN 0 ELSE pagerank / avg_usd_amount END AS ratio_pagerank_txn_amount

                RETURN 
                    account_id,
                    bank,
                    betweenness,
                    pagerank,
                    total_trxns,
                    total_fraud_trxns,
                    total_receivers,
                    total_usd_amount,
                    total_fraud_usd_amount,
                    avg_usd_amount,
                    max_usd_amount,
                    min_usd_amount,
                    total_small_txns,
                    total_high_txns,
                    total_cash_txns,
                    unique_payment_formats,
                    total_active_days,
                    total_trxns_per_day,
                    total_usd_amount_per_day,
                    avg_usd_amount_per_receiver,
                    ratio_max_to_avg,
                    ratio_fraud_receiver,
                    ratio_fraud_usd_amount,
                    ratio_cash_trxns,
                    ratio_small_trxns,
                    ratio_high_trxns,
                    pagerank_betweenness_interaction,
                    pagerank_betweenness_difference,
                    ratio_pagerank_betweenness,
                    ratio_pagerank_txn,
                    ratio_pagerank_txn_amount

            '''
            features = self.mg_client.execute_query(query)
            account_feature_list = []
            for f in features:
                # Dynamically map the keys from the query response
                account_features = {key: f[key] for key in f}
                account_feature_list.append(account_features)
            return account_feature_list

        except Exception as e:
            logging.error(f"Error extracting graph features: {e}")


if __name__ == "__main__":
    graph_extractor = GraphFeatureExtractor()
    features_for_ml = graph_extractor.extract_node_features()
    print(features_for_ml)
