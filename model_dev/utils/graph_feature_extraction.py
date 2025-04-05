import sys
import os
from dotenv import load_dotenv #type: ignore
load_dotenv(override=True)
sys.path.append(os.getenv("PROJECT_PATH"))
from typing import Dict, Any, List

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

    def fetch_account_node_features(self) -> List[Dict[str, Any]]:
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



# if __name__ == "__main__":
#     graph_extractor = GraphFeatureExtractor()
#     graph_extractor.extract_and_update_features()
#     features_for_ml = graph_extractor.fetch_account_node_features()
#     print(features_for_ml)