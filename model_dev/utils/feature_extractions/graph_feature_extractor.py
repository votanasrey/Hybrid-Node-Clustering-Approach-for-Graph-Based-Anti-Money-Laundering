import sys
import os
from dotenv import load_dotenv  # type: ignore
load_dotenv(override=True)
sys.path.append(os.getenv("PROJECT_PATH"))
from typing import Dict, Any, List
from collections import defaultdict
import logging
import pandas as pd #type: ignore 
import numpy as np #type: ignore 
from sklearn.preprocessing import StandardScaler #type: ignore 
from sklearn.decomposition import PCA #type: ignore 
from services.memgraph import MemgraphClient

class GraphFeatureExtractor:
    def __init__(self):
        self.mg_client = MemgraphClient()

    def extract_node_features(self):
        try:
            print("✅ Querying Data from Memgraph")
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
                    pagerank_betweenness_difference,
                    ratio_pagerank_betweenness,
                    ratio_pagerank_txn,
                    ratio_pagerank_txn_amount

            '''
            features = self.mg_client.execute_query(query)
            account_feature_list = []
            print("✅ Transform the query results to Dataframe")
            for f in features:
                # Dynamically map the keys from the query response
                account_features = {key: f[key] for key in f}
                account_feature_list.append(account_features)
            try: 
                df = pd.DataFrame(account_feature_list)
            except Exception as e:
                print(f"❌ Cannot convert to dataframe {e}", flush=True)
            return df

        except Exception as e:
            print(f"❌ Error extracting graph features: {e}", flush=True)
            return None

    def apply_feature_engineering(self, df):
        """
        Preprocess transaction data and engineer new features for anomaly detection.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing the transaction features
        
        Returns:
        --------
        pandas.DataFrame
            Processed DataFrame with additional engineered features
        dict
            Dictionary of preprocessing metadata (feature lists, correlation info)
        """
        print("✅ Applying the Feature Engineering")
        processed_df = df.copy()
        
        # Step 1: Handle non-numeric columns
        numeric_cols = processed_df.select_dtypes(include=['float64', 'int64']).columns
        non_numeric_cols = [col for col in processed_df.columns if col not in numeric_cols]
        
        # Step 2: Apply log transformation to amount-based features
        amount_cols = [col for col in numeric_cols if 'amount' in col.lower() or 'usd' in col.lower()]
        for col in amount_cols:
            processed_df[f'{col}_log'] = np.log1p(processed_df[col])
        
        # Step 3: Add new engineered features
        
        # Transaction pattern features
        processed_df['txn_size_variability'] = processed_df['max_usd_amount'] / (processed_df['min_usd_amount'] + 1)
        processed_df['amount_count_ratio'] = processed_df['total_usd_amount'] / (processed_df['total_trxns'] + 1)
        processed_df['small_high_ratio'] = (processed_df['total_small_txns'] + 1) / (processed_df['total_high_txns'] + 1)
        
        # Network pattern features
        processed_df['network_anomaly_score'] = processed_df['pagerank'] * processed_df['ratio_fraud_receiver']
        processed_df['position_activity_disparity'] = abs(processed_df['pagerank'] - (processed_df['total_trxns'] / processed_df['total_trxns'].max()))
        
        # Temporal pattern features
        processed_df['variance_txns_per_day'] = processed_df['total_trxns'] / (processed_df['total_active_days'] ** 2)
        processed_df['temporal_density'] = processed_df['total_trxns'] / (processed_df['total_active_days'] + 1)
        
        # Fraud-specific ratios
        processed_df['fraud_to_normal_ratio'] = processed_df['total_fraud_trxns'] / (processed_df['total_trxns'] - processed_df['total_fraud_trxns'] + 1)
        
        # Combined metric features
        processed_df['combined_network_centrality'] = processed_df['pagerank'] * processed_df['betweenness']
        processed_df['risk_score'] = (
            processed_df['ratio_fraud_usd_amount'] * 
            processed_df['ratio_cash_trxns'] * 
            processed_df['combined_network_centrality']
        )
        
        # Step 4: Identify highly correlated features
        # Get updated numeric columns after adding new features
        numeric_cols = processed_df.select_dtypes(include=['float64', 'int64']).columns
        
        corr_matrix = processed_df[numeric_cols].corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]
        
        # Step 5: Create feature lists for model training
        id_cols = [col for col in non_numeric_cols if 'id' in col.lower() or col == 'account_id' or col == 'bank']
        features_for_model = [col for col in numeric_cols if col not in id_cols and col not in to_drop]
        
        # Create metadata dictionary
        preprocessing_metadata = {
            'original_features': df.columns.tolist(),
            'added_features': [col for col in processed_df.columns if col not in df.columns],
            'highly_correlated_features': to_drop,
            'features_for_model': features_for_model,
            'id_columns': id_cols,
            'numeric_columns': numeric_cols.tolist(),
            'non_numeric_columns': non_numeric_cols
        }
        
        return processed_df, preprocessing_metadata

if __name__ == "__main__":
    graph_extractor = GraphFeatureExtractor()
    df = graph_extractor.extract_node_features()
    training_data, traning_metadata = graph_extractor.apply_feature_engineering(df)
    print(training_data)
    print(traning_metadata)
