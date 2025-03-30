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
            RETURN node, rank
            ORDER BY rank DESC
        '''
        results = self.mg_client.execute_query(query)
        return {row[0]: row[1] for row in results}

    def run_betweenness_centrality(self) -> Dict[int, float]:
        query = '''
            CALL nxalg.betweenness_centrality() 
            YIELD node, betweenness
            WITH node, betweenness
            WHERE node:Account
            RETURN node, betweenness
            ORDER BY betweenness DESC;
        '''
        results = self.mg_client.execute_query(query)
        return {row[0]: row[1] for row in results}

    def run_community_detection(self) -> Dict[int, int]:
        query = '''
            
        '''
        results = self.mg_client.execute_query(query)
        return {row[0]: row[1] for row in results}

    def update_node_properties(self, node_features: Dict[int, Dict[str, Any]]):
        for node_id, features in node_features.items():
            set_clause = ", ".join([f"{key} = {value}" for key, value in features.items()])
            query = f"SET NODE {node_id} SET {set_clause}"
            self.mg_client.execute_query(query)

    def extract_and_update_features(self):
        pagerank_scores = self.run_pagerank()
        betweenness_centrality = self.run_betweenness_centrality()
        community_detection = self.run_community_detection()
        node_features = {}
        for node_id in set(pagerank_scores.keys()).union(betweenness_centrality.keys(), community_detection.keys()):
            features = {
                "pagerank": pagerank_scores.get(node_id, None),
                "betweenness": betweenness_centrality.get(node_id, None),
                "community": community_detection.get(node_id, None)
            }
            node_features[node_id] = features
        self.update_node_properties(node_features)

    def fetch_features_for_ml(self) -> List[List[Any]]:
        query = '''
            MATCH (n:Node)
            RETURN n.nodeId AS node_id, n.pagerank AS pagerank, n.betweenness AS betweenness, n.community AS community
        '''
        features = self.mg_client.execute_query(query)
        return [[f[1], f[2], f[3]] for f in features]  


if __name__ == "__main__":
    graph_extractor = GraphFeatureExtractor()
    graph_extractor.extract_and_update_features()
    features_for_ml = graph_extractor.fetch_features_for_ml()

    for feature_set in features_for_ml:
        print(f"Node features: {feature_set}")
