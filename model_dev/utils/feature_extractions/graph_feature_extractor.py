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
                    unique_payment_formats,
                    total_trxns,
                    total_fraud_trxns,
                    total_receivers,
                    total_usd_amount,
                    total_fraud_usd_amount,
                    toFloat(total_fraud_usd_amount / total_usd_amount) AS ratio_fraud_usd_amount,
                    avg_usd_amount,
                    max_usd_amount,
                    min_usd_amount,
                    total_small_txns,
                    total_high_txns,
                    total_cash_txns,
                    total_active_days,
                    (max_usd_amount / avg_usd_amount) AS ratio_max_to_avg,
                    (toFloat(total_fraud_trxns) / total_receivers) AS ratio_fraud_receiver,
                    (pagerank * betweenness) AS pagerank_betweenness_interaction,
                    ABS(pagerank - betweenness) AS pagerank_betweenness_difference,
                    CASE 
                        WHEN betweenness = 0 THEN 0
                        ELSE pagerank / betweenness
                    END AS ratio_pagerank_betweenness,
                    (pagerank / total_trxns) AS ratio_pagerank_txn,
                    (pagerank / avg_usd_amount) AS ratio_pagerank_txn_amount,
                    (toFloat(total_cash_txns) / total_trxns) AS ratio_cash_trxns

                RETURN 
                    account_id,
                    bank,
                    betweenness,
                    pagerank,
                    unique_payment_formats,
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
                    total_active_days,
                    ratio_max_to_avg,
                    ratio_fraud_receiver,
                    pagerank_betweenness_interaction,
                    pagerank_betweenness_difference,
                    ratio_pagerank_betweenness,
                    ratio_pagerank_txn,
                    ratio_pagerank_txn_amount,
                    ratio_fraud_usd_amount,
                    ratio_cash_trxns
            '''
            features = self.mg_client.execute_query(query)

            account_feature_list = []
            for f in features:
                account_features = {
                    "account_id": f["account_id"],
                    "bank": f["bank"],
                    "betweenness": f["betweenness"],
                    "pagerank": f["pagerank"],
                    "unique_payment_formats": f["unique_payment_formats"],
                    "total_trxns": f["total_trxns"],
                    "total_fraud_trxns": f["total_fraud_trxns"],
                    "total_receivers": f["total_receivers"],
                    "total_usd_amount": f["total_usd_amount"],
                    "total_fraud_usd_amount": f["total_fraud_usd_amount"],
                    "avg_usd_amount": f["avg_usd_amount"],
                    "max_usd_amount": f["max_usd_amount"],
                    "min_usd_amount": f["min_usd_amount"],
                    "total_small_txns": f["total_small_txns"],
                    "total_high_txns": f["total_high_txns"],
                    "total_cash_txns": f["total_cash_txns"],
                    "total_active_days": f["total_active_days"],
                    "ratio_max_to_avg": f["ratio_max_to_avg"],
                    "ratio_fraud_receiver": f["ratio_fraud_receiver"],
                    "pagerank_betweenness_interaction": f["pagerank_betweenness_interaction"],
                    "pagerank_betweenness_difference": f["pagerank_betweenness_difference"],
                    "ratio_pagerank_betweenness": f["ratio_pagerank_betweenness"],
                    "ratio_pagerank_txn": f["ratio_pagerank_txn"],
                    "ratio_pagerank_txn_amount": f["ratio_pagerank_txn_amount"],
                    "ratio_fraud_usd_amount": f["ratio_fraud_usd_amount"],
                    "ratio_cash_trxns": f["ratio_cash_trxns"]
                }
                account_feature_list.append(account_features)

            return account_feature_list

        except Exception as e:
            logging.error(f"Error extracting graph features: {e}")


if __name__ == "__main__":
    graph_extractor = GraphFeatureExtractor()
    features_for_ml = graph_extractor.extract_node_features()
    print(features_for_ml)
