import pandas as pd #type: ignore
from utils.feature_extractions.graph_feature_extractor import GraphFeatureExtractor
from utils.trainings.isolation_forest_trainer import (
    train_isolation_forest
)
from utils.evaluations.isolation_forest_evaluator import (
    evaluate_isolation_forest
)

graph_extractor = GraphFeatureExtractor()
df = graph_extractor.extract_node_features()

# Step 1: Preprocess the data and engineer features
processed_df, metadata = graph_extractor.apply_feature_engineering(df)
print(processed_df)
print(metadata)

processed_df.to_csv('final_training_data.csv', index=False)