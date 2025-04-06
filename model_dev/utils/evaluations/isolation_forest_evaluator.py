import pandas as pd #type: ignore
import numpy as np #type: ignore
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score #type: ignore
import matplotlib.pyplot as plt #type: ignore
import seaborn as sns #type: ignore

def evaluate_isolation_forest(
    result_df, 
    true_labels=None, 
    threshold=None,
    label_column='anomaly_flag',
    score_column='anomaly_score',
    account_id_column='account_id',
    visualize=True,
    top_n_anomalies=20,
    feature_importance=True
):
    """
    Comprehensive evaluation of anomaly detection results.
    
    Parameters:
    -----------
    result_df : pandas.DataFrame
        DataFrame containing the results of anomaly detection.
    true_labels : pandas.Series or numpy.array, optional
        True labels for the data if available (1 for normal, -1 for anomalies).
    threshold : float, optional
        Custom threshold for anomaly detection. If not provided, uses the model's default.
    label_column : str, default='anomaly_flag'
        Column name in result_df containing the anomaly flags.
    score_column : str, default='anomaly_score'
        Column name in result_df containing the anomaly scores.
    account_id_column : str, default='account_id'
        Column name in result_df containing the account identifiers.
    visualize : bool, default=True
        Whether to visualize the results.
    top_n_anomalies : int, default=20
        Number of top anomalies to display.
    feature_importance : bool, default=True
        Whether to calculate and display feature importance.
        
    Returns:
    --------
    dict
        Dictionary containing evaluation metrics and other information.
    """
    
    results = {}
    
    # Convert boolean flags to -1/1 format if needed
    if result_df[label_column].dtype == bool:
        y_pred = result_df[label_column].map({True: -1, False: 1}).values
    else:
        y_pred = result_df[label_column].values
    
    y_scores = result_df[score_column].values
    
    # 1. Basic Statistics
    results['anomaly_count'] = sum(y_pred == -1)
    results['normal_count'] = sum(y_pred == 1)
    results['anomaly_ratio'] = results['anomaly_count'] / len(result_df)
    
    print(f"Total instances: {len(result_df)}")
    print(f"Detected anomalies: {results['anomaly_count']} ({results['anomaly_ratio']:.2%})")
    print(f"Normal instances: {results['normal_count']} ({1-results['anomaly_ratio']:.2%})")
    
    # 2. Top anomalies
    if 'anomaly_probability' in result_df.columns:
        sort_col = 'anomaly_probability'
        ascending = False
    else:
        # For Isolation Forest, more negative score = more anomalous
        sort_col = score_column
        ascending = True
    
    top_anomalies = result_df.sort_values(sort_col, ascending=ascending).head(top_n_anomalies)
    results['top_anomalies'] = top_anomalies
    
    print(f"\nTop {top_n_anomalies} most anomalous accounts:")
    display_cols = [account_id_column, score_column]
    if 'anomaly_probability' in result_df.columns:
        display_cols.append('anomaly_probability')
    if 'anomaly_percentile' in result_df.columns:
        display_cols.append('anomaly_percentile')
    
    print(top_anomalies[display_cols])
    
    # 3. Feature importance (if requested)
    if feature_importance:
        try:
            # Get only numeric columns (excluding the anomaly-related columns)
            exclude_cols = [account_id_column, label_column, score_column, 
                           'anomaly_probability', 'anomaly_percentile']
            feature_cols = [col for col in result_df.select_dtypes(include=['float64', 'int64']).columns 
                           if col not in exclude_cols]
            
            # Calculate correlation with anomaly score
            correlations = result_df[feature_cols + [score_column]].corr()[score_column].drop(score_column)
            
            # For Isolation Forest, more negative score = more anomalous
            # So we take absolute correlation for feature importance
            feature_importance = correlations.abs().sort_values(ascending=False).head(10)
            results['feature_importance'] = feature_importance
            
            print("\nTop features correlated with anomalies:")
            print(feature_importance)
            
            if visualize:
                plt.figure(figsize=(10, 6))
                sns.barplot(x=feature_importance.values, y=feature_importance.index)
                plt.title('Feature Importance (Correlation with Anomaly Score)')
                plt.xlabel('Absolute Correlation')
                plt.tight_layout()
                plt.show()
                
        except Exception as e:
            print(f"Error in feature importance calculation: {e}")
    
    # 4. Score distribution
    if visualize:
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        sns.histplot(result_df[result_df[label_column] == True][score_column], 
                    color='red', label='Anomalies', alpha=0.7)
        sns.histplot(result_df[result_df[label_column] == False][score_column], 
                    color='blue', label='Normal', alpha=0.7)
        plt.title('Anomaly Score Distribution')
        plt.xlabel('Anomaly Score')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        sns.boxplot(x=label_column, y=score_column, data=result_df)
        plt.title('Anomaly Score by Class')
        plt.tight_layout()
        plt.show()
    
    # 5. Model evaluation with true labels (if available)
    if true_labels is not None:
        print("\n--- Model Evaluation with True Labels ---")
        
        # Convert true labels to -1/1 format if needed
        if isinstance(true_labels, pd.Series) and true_labels.dtype == bool:
            y_true = true_labels.map({True: -1, False: 1}).values
        else:
            y_true = true_labels
            
        # 5.1 Confusion Matrix
        cm = confusion_matrix(y_true, y_pred)
        results['confusion_matrix'] = cm
        
        print("Confusion Matrix:")
        print(cm)
        
        if visualize:
            plt.figure(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                       xticklabels=['Normal', 'Anomaly'], 
                       yticklabels=['Normal', 'Anomaly'])
            plt.title('Confusion Matrix')
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            plt.tight_layout()
            plt.show()
        
        # 5.2 Classification Report
        cr = classification_report(y_true, y_pred, output_dict=True)
        results['classification_report'] = cr
        
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred))
        
        # 5.3 ROC Curve and AUC
        # We need to adjust the scores for ROC curve if they're from Isolation Forest
        # For Isolation Forest, more negative = more anomalous, but ROC expects higher values for positive class
        adjusted_scores = -y_scores if ascending else y_scores
        
        fpr, tpr, _ = roc_curve(y_true == -1, adjusted_scores)
        roc_auc = auc(fpr, tpr)
        results['roc_auc'] = roc_auc
        
        print(f"\nAUC-ROC: {roc_auc:.4f}")
        
        if visualize:
            plt.figure(figsize=(6, 5))
            plt.plot(fpr, tpr, color='darkorange', lw=2, 
                    label=f'ROC curve (area = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Receiver Operating Characteristic (ROC)')
            plt.legend(loc="lower right")
            plt.tight_layout()
            plt.show()
        
        # 5.4 Precision-Recall Curve
        precision, recall, _ = precision_recall_curve(y_true == -1, adjusted_scores)
        avg_precision = average_precision_score(y_true == -1, adjusted_scores)
        results['average_precision'] = avg_precision
        
        print(f"Average Precision Score: {avg_precision:.4f}")
        
        if visualize:
            plt.figure(figsize=(6, 5))
            plt.plot(recall, precision, color='blue', lw=2, 
                    label=f'Precision-Recall curve (AP = {avg_precision:.2f})')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Precision-Recall Curve')
            plt.legend(loc="upper right")
            plt.tight_layout()
            plt.show()
    
    return results
