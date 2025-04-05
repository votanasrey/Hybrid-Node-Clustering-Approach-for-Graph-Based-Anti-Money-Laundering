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

class GraphFeatureConstructor:
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
        logging.debug("Pagerank Results:", results[0:10]) 
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
        logging.debug("Betweenness Results:", results[0:10])
        return {row["node_id"]: row["betweenness"] for row in results}

    def update_node_properties(self, node_features: Dict[int, Dict[str, Any]]):
        for node_id, features in node_features.items():
            query = f'''
                MATCH (n:Account) WHERE id(n) = {node_id}
                SET {", ".join([f"n.{k} = {repr(v)}" for k, v in features.items() if v is not None])}
            '''
            self.mg_client.execute_query(query)

    def construct_and_update_node_properties(self):
        try:
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
            logging.info("ALL nodes updated the features of pagerank and betweeness")
            return True
        except Exception as e:
            logging.error(f"Error to construct the graph {e}")
            return False 

  

if __name__ == "__main__":
    graph_extractor = GraphFeatureConstructor()
    constructor = graph_extractor.construct_and_update_node_properties()
    print(constructor)