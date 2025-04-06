import numpy as np #type: ignore
from sklearn.preprocessing import StandardScaler #type: ignore
from sklearn.decomposition import PCA #type: ignore
from sklearn.ensemble import IsolationForest #type: ignore

def train_isolation_forest(
        df, 
        metadata, 
        contamination='auto', 
        n_estimators=200,                   
        apply_pca=True, 
        pca_components=0.95, 
        return_model=False
    ):
    """
    Apply standardization, optional PCA, and Isolation Forest for anomaly detection.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Preprocessed DataFrame from preprocess_transaction_data function
    metadata : dict
        Preprocessing metadata from preprocess_transaction_data function
    contamination : float or 'auto'
        Expected proportion of outliers in the data or 'auto'
    n_estimators : int
        Number of trees in the Isolation Forest
    apply_pca : bool
        Whether to apply PCA for dimensionality reduction
    pca_components : float or int
        Number of components to keep (if float, fraction of variance to retain)
    return_model : bool
        Whether to return the trained models along with results
    
    Returns:
    --------
    pandas.DataFrame
        Original DataFrame with anomaly scores and flags
    dict
        Summary information about the anomaly detection process
    dict (optional)
        Trained models if return_model=True
    """
    print("**"*50)
    print("✅ Training Isolation Forest")
    print("**"*50)

    result_df = df.copy()
    features_for_model = metadata['features_for_model']
    
    print("✅ Step 1: Standardize the features")
    scaler = StandardScaler()
    X = scaler.fit_transform(result_df[features_for_model])
    
    print("✅ Step 2: Apply PCA if requested")
    pca_model = None
    if apply_pca:
        pca_model = PCA(n_components=pca_components)
        X = pca_model.fit_transform(X)
        # Store variance explained for reporting
        if isinstance(pca_components, float):
            pca_explained_variance = sum(pca_model.explained_variance_ratio_)
        else:
            pca_explained_variance = sum(pca_model.explained_variance_ratio_)

    print("✅ Step 3: Apply Isolation Forest")
    iso_forest = IsolationForest(
        n_estimators=n_estimators,
        max_samples='auto',
        contamination=contamination,
        max_features=0.8,
        bootstrap=True,
        n_jobs=-1,
        random_state=42
    )
    
    iso_forest.fit(X)
    
    # Get anomaly scores (-1 = anomaly, 1 = normal)
    raw_predictions = iso_forest.predict(X)
    # Get decision function scores (lower = more anomalous)
    decision_scores = iso_forest.decision_function(X)
    
    print("✅ Step 4: Add results to DataFrame")
    result_df['anomaly_flag'] = raw_predictions == -1
    result_df['anomaly_score'] = decision_scores
    
    # Convert to probability (0-1 where 1 = most anomalous)
    min_score = min(decision_scores)
    max_score = max(decision_scores)
    result_df['anomaly_probability'] = 1 - (decision_scores - min_score) / (max_score - min_score)
    # Add percentile rank
    result_df['anomaly_percentile'] = result_df['anomaly_probability'].rank(pct=True) * 100
    
    print("✅ Step 5: Generate summary information")
    summary = {
        'total_accounts': len(result_df),
        'accounts_flagged_as_anomalies': sum(result_df['anomaly_flag']),
        'anomaly_rate': sum(result_df['anomaly_flag']) / len(result_df),
        'features_used': len(features_for_model),
        'features_list': features_for_model,
    }
    
    if apply_pca:
        summary['pca_explained_variance'] = pca_explained_variance
        summary['pca_components_used'] = pca_model.n_components_
    
    if return_model:
        models = {
            'scaler': scaler,
            'isolation_forest': iso_forest
        }
        if apply_pca:
            models['pca'] = pca_model
        return result_df, summary, models

    return result_df, summary