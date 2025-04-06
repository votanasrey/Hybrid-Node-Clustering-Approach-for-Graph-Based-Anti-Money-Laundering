import pandas as pd #type: ignore
from utils.feature_extractions.graph_feature_extractor import GraphFeatureExtractor
from utils.training.isolation_forest_training import (
    train_isolation_forest
)

graph_extractor = GraphFeatureExtractor()
df = graph_extractor.extract_node_features()

# Step 1: Preprocess the data and engineer features
processed_df, metadata = graph_extractor.apply_feature_engineering(df)
print(processed_df)
print(metadata)

# Option 2: Get results and trained models (for later prediction on new data)
result_df, summary, isolation_forst_model = train_isolation_forest(
    processed_df, 
    metadata,
    contamination=0.05,
    n_estimators=200,
    apply_pca=True,
    pca_components=0.9,
    return_model=True        # Return trained models
)

# View the summary
print(summary)

# Get top 20 most anomalous accounts
top_anomalies = result_df.sort_values('anomaly_probability', ascending=False).head(20)
print(top_anomalies[['account_id', 'anomaly_probability', 'anomaly_percentile']])

# Feature importance by correlation with anomaly score
try:
    # Get only numeric columns
    numeric_cols = result_df.select_dtypes(include=['float64', 'int64']).columns
    
    # Calculate correlation on numeric columns only
    feature_importance_alt = result_df[numeric_cols].corr()['anomaly_probability'].sort_values(ascending=False).head(10)
    print("\nAlternative calculation:")
    print(feature_importance_alt)
except Exception as e:
    print(f"Error in alternative approach: {e}")
    print("Top features correlated with anomalies:")
print(feature_importance_alt)

def predict_anomalies(new_df, metadata, models):
    processed_new_df, _ = graph_extractor.apply_feature_engineering(new_df)
    features = metadata['features_for_model']
    X = models['scaler'].transform(processed_new_df[features])
    
    if 'pca' in models:
        X = models['pca'].transform(X)
    
    raw_predictions = models['isolation_forest'].predict(X)
    decision_scores = models['isolation_forest'].decision_function(X)
    processed_new_df['anomaly_flag'] = raw_predictions == -1
    processed_new_df['anomaly_score'] = decision_scores
    
    return processed_new_df

new_result = predict_anomalies(
    df,
    metadata,
    isolation_forst_model
)

print("New Results")
print(new_result)
print("Detected Anomaly Dist: ", new_result["anomaly_flag"].value_counts()) 