"""
InsightLogger v1.5 - Data Science & Analytics Pipeline Example

This example demonstrates how to use InsightLogger for monitoring
data science workflows, machine learning pipelines, and analytics operations.
"""

import numpy as np
import pandas as pd
import time
import random
from insightlog import InsightLogger

def create_sample_data(size=10000):
    """Create sample dataset for analysis"""
    np.random.seed(42)
    return pd.DataFrame({
        'user_id': range(1, size + 1),
        'age': np.random.randint(18, 80, size),
        'income': np.random.normal(50000, 15000, size),
        'spending': np.random.gamma(2, 1000, size),
        'category': np.random.choice(['A', 'B', 'C', 'D'], size),
        'timestamp': pd.date_range('2024-01-01', periods=size, freq='H')
    })

def data_science_pipeline():
    """Complete data science pipeline with comprehensive monitoring"""
    
    print("🔬 Data Science Pipeline with InsightLogger v1.5")
    print("=" * 60)
    
    # Initialize logger with enhanced features for data science
    with InsightLogger(
        name="DataSciencePipeline",
        enable_database=True,
        enable_monitoring=True,
        log_level=20  # INFO level
    ) as logger:
        
        # Pipeline Stage 1: Data Loading and Preparation
        print("📊 Stage 1: Data Loading and Preparation")
        
        @logger.log_function_time
        def load_and_prepare_data():
            """Load and prepare data with monitoring"""
            
            with logger.performance_profile("data_loading"):
                logger.log_types("INFO", "Loading sample dataset...", emoji=True)
                df = create_sample_data(50000)
                
                # Log data characteristics
                logger.log_with_context(
                    "SUCCESS",
                    "Dataset loaded successfully",
                    context={
                        "rows": len(df),
                        "columns": len(df.columns),
                        "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
                        "date_range": f"{df['timestamp'].min()} to {df['timestamp'].max()}"
                    },
                    tags=["data_loading", "dataset_info"]
                )
                
                # Add data quality metrics
                logger.add_custom_metric("dataset_rows", len(df))
                logger.add_custom_metric("dataset_columns", len(df.columns))
                logger.add_custom_metric("missing_values", df.isnull().sum().sum())
                
            with logger.performance_profile("data_cleaning"):
                logger.log_types("INFO", "Cleaning and preprocessing data...", emoji=True)
                
                # Simulate data cleaning operations
                original_size = len(df)
                df = df.dropna()  # Remove missing values
                df = df[df['income'] > 0]  # Remove invalid incomes
                df = df[df['age'] >= 18]  # Remove invalid ages
                
                cleaned_size = len(df)
                removed_rows = original_size - cleaned_size
                
                logger.log_with_context(
                    "SUCCESS",
                    "Data cleaning completed",
                    context={
                        "original_rows": original_size,
                        "cleaned_rows": cleaned_size,
                        "removed_rows": removed_rows,
                        "removal_rate": f"{(removed_rows/original_size)*100:.2f}%"
                    },
                    tags=["data_cleaning", "quality_control"]
                )
                
                # Add cleaning metrics
                logger.add_custom_metric("data_quality_score", (cleaned_size/original_size)*100)
                logger.add_custom_metric("rows_removed", removed_rows)
                
            return df
        
        # Execute data loading
        dataset = load_and_prepare_data()
        
        # Pipeline Stage 2: Exploratory Data Analysis
        print("\n🔍 Stage 2: Exploratory Data Analysis")
        
        @logger.log_function_time
        def exploratory_analysis(df):
            """Perform exploratory data analysis with monitoring"""
            
            with logger.performance_profile("statistical_analysis"):
                logger.log_types("INFO", "Computing statistical summaries...", emoji=True)
                
                # Basic statistics
                numeric_columns = df.select_dtypes(include=[np.number]).columns
                stats = df[numeric_columns].describe()
                
                # Log statistical insights
                for column in numeric_columns:
                    mean_val = df[column].mean()
                    std_val = df[column].std()
                    
                    logger.add_custom_metric(f"{column}_mean", mean_val)
                    logger.add_custom_metric(f"{column}_std", std_val)
                    
                    logger.log_with_context(
                        "DEBUG",
                        f"Statistics for {column}",
                        context={
                            "mean": mean_val,
                            "std": std_val,
                            "min": df[column].min(),
                            "max": df[column].max()
                        },
                        tags=["statistics", "eda"]
                    )
            
            with logger.performance_profile("correlation_analysis"):
                logger.log_types("INFO", "Computing correlation matrix...", emoji=True)
                
                # Correlation analysis
                corr_matrix = df[numeric_columns].corr()
                
                # Find strong correlations
                strong_correlations = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_val = corr_matrix.iloc[i, j]
                        if abs(corr_val) > 0.5:  # Strong correlation threshold
                            strong_correlations.append({
                                'var1': corr_matrix.columns[i],
                                'var2': corr_matrix.columns[j],
                                'correlation': corr_val
                            })
                
                logger.log_with_context(
                    "INFO",
                    f"Found {len(strong_correlations)} strong correlations",
                    context={"correlations": strong_correlations},
                    tags=["correlation", "feature_analysis"]
                )
                
                logger.add_custom_metric("strong_correlations_found", len(strong_correlations))
            
            with logger.performance_profile("outlier_detection"):
                logger.log_types("INFO", "Detecting outliers...", emoji=True)
                
                # Simple outlier detection using IQR
                outliers_count = 0
                for column in numeric_columns:
                    Q1 = df[column].quantile(0.25)
                    Q3 = df[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    column_outliers = len(df[(df[column] < lower_bound) | (df[column] > upper_bound)])
                    outliers_count += column_outliers
                    
                    logger.add_custom_metric(f"{column}_outliers", column_outliers)
                
                logger.log_types("SUCCESS", f"Outlier detection completed: {outliers_count} outliers found")
                logger.add_custom_metric("total_outliers", outliers_count)
            
            return stats
        
        # Execute EDA
        statistics = exploratory_analysis(dataset)
        
        # Pipeline Stage 3: Feature Engineering
        print("\n🔧 Stage 3: Feature Engineering")
        
        @logger.log_function_time
        def feature_engineering(df):
            """Create new features with monitoring"""
            
            with logger.performance_profile("feature_creation"):
                logger.log_types("INFO", "Creating new features...", emoji=True)
                
                # Create derived features
                df['spending_ratio'] = df['spending'] / df['income']
                df['age_group'] = pd.cut(df['age'], bins=[0, 30, 50, 70, 100], 
                                       labels=['Young', 'Middle', 'Senior', 'Elder'])
                df['income_percentile'] = pd.qcut(df['income'], 100, labels=False)
                df['high_spender'] = (df['spending'] > df['spending'].quantile(0.8)).astype(int)
                
                # Time-based features
                df['hour'] = df['timestamp'].dt.hour
                df['day_of_week'] = df['timestamp'].dt.dayofweek
                df['month'] = df['timestamp'].dt.month
                
                new_features = ['spending_ratio', 'age_group', 'income_percentile', 
                              'high_spender', 'hour', 'day_of_week', 'month']
                
                logger.log_with_context(
                    "SUCCESS",
                    "Feature engineering completed",
                    context={
                        "new_features": new_features,
                        "total_features": len(df.columns),
                        "feature_types": df.dtypes.value_counts().to_dict()
                    },
                    tags=["feature_engineering", "data_transformation"]
                )
                
                logger.add_custom_metric("features_created", len(new_features))
                logger.add_custom_metric("total_features", len(df.columns))
            
            with logger.performance_profile("feature_validation"):
                logger.log_types("INFO", "Validating new features...", emoji=True)
                
                # Validate feature quality
                validation_results = {}
                for feature in new_features:
                    if feature in df.columns:
                        missing_pct = (df[feature].isnull().sum() / len(df)) * 100
                        unique_values = df[feature].nunique()
                        
                        validation_results[feature] = {
                            "missing_percentage": missing_pct,
                            "unique_values": unique_values,
                            "data_type": str(df[feature].dtype)
                        }
                        
                        logger.add_custom_metric(f"{feature}_unique_values", unique_values)
                        logger.add_custom_metric(f"{feature}_missing_pct", missing_pct)
                
                logger.log_with_context(
                    "SUCCESS",
                    "Feature validation completed",
                    context=validation_results,
                    tags=["feature_validation", "quality_control"]
                )
            
            return df
        
        # Execute feature engineering
        enhanced_dataset = feature_engineering(dataset)
        
        # Pipeline Stage 4: Model Training Simulation
        print("\n🤖 Stage 4: Model Training Simulation")
        
        @logger.log_function_time
        def simulate_model_training(df):
            """Simulate machine learning model training with monitoring"""
            
            models = ['RandomForest', 'XGBoost', 'LinearRegression', 'SVM', 'NeuralNetwork']
            model_results = {}
            
            for model_name in models:
                logger.log_types("INFO", f"Training {model_name} model...", emoji=True)
                
                with logger.performance_profile(f"model_training_{model_name}"):
                    # Simulate training time based on model complexity
                    training_time = {
                        'RandomForest': random.uniform(2.0, 4.0),
                        'XGBoost': random.uniform(3.0, 6.0),
                        'LinearRegression': random.uniform(0.5, 1.0),
                        'SVM': random.uniform(4.0, 8.0),
                        'NeuralNetwork': random.uniform(5.0, 10.0)
                    }
                    
                    time.sleep(training_time[model_name])
                    
                    # Simulate model performance metrics
                    accuracy = random.uniform(0.7, 0.95)
                    precision = random.uniform(0.65, 0.9)
                    recall = random.uniform(0.6, 0.88)
                    f1_score = 2 * (precision * recall) / (precision + recall)
                    
                    model_results[model_name] = {
                        'accuracy': accuracy,
                        'precision': precision,
                        'recall': recall,
                        'f1_score': f1_score,
                        'training_time': training_time[model_name]
                    }
                    
                    # Log model performance
                    logger.log_with_context(
                        "SUCCESS",
                        f"{model_name} training completed",
                        context={
                            "accuracy": f"{accuracy:.4f}",
                            "precision": f"{precision:.4f}",
                            "recall": f"{recall:.4f}",
                            "f1_score": f"{f1_score:.4f}",
                            "training_time_seconds": training_time[model_name]
                        },
                        tags=["model_training", "performance_metrics", model_name.lower()]
                    )
                    
                    # Add model metrics
                    logger.add_custom_metric(f"{model_name}_accuracy", accuracy)
                    logger.add_custom_metric(f"{model_name}_training_time", training_time[model_name])
                    logger.add_custom_metric("models_trained", 1)
            
            # Find best model
            best_model = max(model_results.items(), key=lambda x: x[1]['f1_score'])
            
            logger.log_types("SUCCESS", 
                           f"Best model: {best_model[0]} (F1: {best_model[1]['f1_score']:.4f})",
                           emoji=True, bold=True)
            
            logger.add_custom_metric("best_model_f1_score", best_model[1]['f1_score'])
            
            return model_results
        
        # Execute model training
        model_results = simulate_model_training(enhanced_dataset)
        
        # Pipeline Stage 5: Model Evaluation and Deployment Simulation
        print("\n📈 Stage 5: Model Evaluation and Deployment")
        
        @logger.log_function_time
        def model_evaluation_and_deployment():
            """Simulate model evaluation and deployment monitoring"""
            
            with logger.performance_profile("model_evaluation"):
                logger.log_types("INFO", "Evaluating model performance...", emoji=True)
                
                # Simulate cross-validation
                cv_scores = [random.uniform(0.75, 0.9) for _ in range(5)]
                cv_mean = np.mean(cv_scores)
                cv_std = np.std(cv_scores)
                
                logger.log_with_context(
                    "SUCCESS",
                    "Cross-validation completed",
                    context={
                        "cv_scores": cv_scores,
                        "cv_mean": cv_mean,
                        "cv_std": cv_std,
                        "cv_folds": 5
                    },
                    tags=["model_evaluation", "cross_validation"]
                )
                
                logger.add_custom_metric("cv_score_mean", cv_mean)
                logger.add_custom_metric("cv_score_std", cv_std)
            
            with logger.performance_profile("model_deployment"):
                logger.log_types("INFO", "Simulating model deployment...", emoji=True)
                
                # Simulate deployment checks
                deployment_checks = {
                    "model_serialization": random.choice([True, True, True, False]),  # 75% success
                    "api_endpoint_test": random.choice([True, True, False]),  # 67% success
                    "load_test": random.choice([True, True, True, True, False]),  # 80% success
                    "security_scan": random.choice([True, True, True, False])  # 75% success
                }
                
                deployment_success = all(deployment_checks.values())
                
                for check, result in deployment_checks.items():
                    logger.log_types(
                        "SUCCESS" if result else "ERROR",
                        f"Deployment check {check}: {'PASSED' if result else 'FAILED'}",
                        emoji=True
                    )
                    logger.add_custom_metric(f"deployment_{check}", 1 if result else 0)
                
                if deployment_success:
                    logger.log_types("SUCCESS", "Model deployment successful!", 
                                   emoji=True, bold=True, border=True)
                    logger.log_security_event("MODEL_DEPLOYMENT", "LOW", "Model deployed successfully")
                else:
                    logger.log_types("ERROR", "Model deployment failed!", 
                                   emoji=True, bold=True)
                    logger.log_security_event("DEPLOYMENT_FAILURE", "HIGH", "Model deployment failed")
                
                logger.add_custom_metric("deployment_success", 1 if deployment_success else 0)
            
            return deployment_success
        
        # Execute evaluation and deployment
        deployment_result = model_evaluation_and_deployment()
        
        # Pipeline Stage 6: Monitoring and Alerting Setup
        print("\n🔔 Stage 6: Production Monitoring Setup")
        
        @logger.log_function_time
        def setup_production_monitoring():
            """Setup production monitoring and alerting"""
            
            logger.log_types("INFO", "Setting up production monitoring...", emoji=True)
            
            # Simulate setting up various monitoring components
            monitoring_components = [
                "model_performance_tracking",
                "data_drift_detection", 
                "prediction_latency_monitoring",
                "error_rate_alerting",
                "resource_usage_monitoring"
            ]
            
            for component in monitoring_components:
                with logger.performance_profile(f"setup_{component}"):
                    time.sleep(random.uniform(0.2, 0.5))  # Simulate setup time
                    
                    setup_success = random.choice([True, True, True, False])  # 75% success rate
                    
                    logger.log_types(
                        "SUCCESS" if setup_success else "WARNING",
                        f"Monitoring component {component}: {'CONFIGURED' if setup_success else 'FAILED'}",
                        emoji=True
                    )
                    
                    logger.add_custom_metric(f"monitoring_{component}_setup", 1 if setup_success else 0)
            
            # Set up alerting thresholds
            alerting_config = {
                "prediction_latency_threshold_ms": 500,
                "accuracy_degradation_threshold": 0.05,
                "error_rate_threshold": 0.02,
                "data_drift_threshold": 0.1
            }
            
            logger.log_with_context(
                "SUCCESS",
                "Production monitoring configured",
                context=alerting_config,
                tags=["production_monitoring", "alerting_setup"]
            )
            
            for metric, threshold in alerting_config.items():
                logger.add_custom_metric(metric, threshold)
        
        # Setup monitoring
        setup_production_monitoring()
        
        # Generate pipeline summary
        print("\n📋 Pipeline Execution Summary")
        
        # Wait for metrics to accumulate
        time.sleep(3)
        
        # Generate comprehensive insights
        logger.view_insights(detailed=True, create_dashboard=True, export_format="json")
        
        # Generate advanced analytics report
        advanced_report = logger.generate_advanced_report()
        
        print(f"\n🏥 Pipeline Health Score: {advanced_report['executive_summary']['health_score']:.1f}/100")
        print(f"⏱️ Total Pipeline Runtime: {advanced_report['executive_summary']['total_runtime']}")
        print(f"📊 Data Points Processed: {len(enhanced_dataset):,}")
        print(f"🔧 Features Created: {len(enhanced_dataset.columns)}")
        print(f"🤖 Models Trained: {len(model_results)}")
        print(f"🚀 Deployment Status: {'SUCCESS' if deployment_result else 'FAILED'}")
        
        # Show anomalies if any
        anomalies = logger.detect_anomalies()
        if anomalies:
            print(f"\n🚨 Anomalies Detected:")
            for anomaly in anomalies:
                print(f"  • {anomaly}")
        
        # Show recommendations
        recommendations = logger._generate_recommendations()
        if recommendations:
            print(f"\n💡 Optimization Recommendations:")
            for rec in recommendations[:3]:  # Show top 3
                print(f"  • {rec['category']}: {rec['message']}")

def ml_model_monitoring_example():
    """Example of monitoring ML models in production"""
    
    print("\n🔬 ML Model Production Monitoring Example")
    print("=" * 50)
    
    with InsightLogger(
        name="MLModelMonitoring",
        enable_database=True,
        enable_monitoring=True,
        enable_alerts=False
    ) as logger:
        
        @logger.log_function_time
        def simulate_model_predictions(batch_size=100):
            """Simulate model predictions with monitoring"""
            
            predictions = []
            prediction_times = []
            
            for i in range(batch_size):
                with logger.performance_profile("single_prediction"):
                    # Simulate prediction time
                    pred_time = random.uniform(0.01, 0.1)
                    time.sleep(pred_time / 100)  # Speed up for demo
                    
                    # Simulate prediction result
                    prediction = random.choice([0, 1])
                    confidence = random.uniform(0.6, 0.99)
                    
                    predictions.append(prediction)
                    prediction_times.append(pred_time * 1000)  # Convert to ms
                    
                    # Log prediction metrics
                    logger.add_custom_metric("prediction_latency_ms", pred_time * 1000)
                    logger.add_custom_metric("prediction_confidence", confidence)
                    logger.add_custom_metric("predictions_made", 1)
                    
                    # Check for anomalies
                    if pred_time > 0.08:  # High latency
                        logger.log_types("WARNING", f"High prediction latency: {pred_time*1000:.1f}ms")
                        logger.log_security_event("HIGH_LATENCY", "MEDIUM", 
                                                f"Prediction latency exceeded threshold: {pred_time*1000:.1f}ms")
                    
                    if confidence < 0.7:  # Low confidence
                        logger.log_types("WARNING", f"Low prediction confidence: {confidence:.3f}")
            
            # Batch summary
            avg_latency = np.mean(prediction_times)
            avg_confidence = np.mean([random.uniform(0.6, 0.99) for _ in range(batch_size)])
            
            logger.log_with_context(
                "SUCCESS",
                f"Batch prediction completed",
                context={
                    "batch_size": batch_size,
                    "avg_latency_ms": avg_latency,
                    "avg_confidence": avg_confidence,
                    "positive_predictions": sum(predictions),
                    "negative_predictions": batch_size - sum(predictions)
                },
                tags=["batch_prediction", "model_performance"]
            )
            
            return predictions, prediction_times
        
        # Simulate multiple prediction batches
        print("🔮 Simulating model predictions...")
        for batch_num in range(5):
            logger.log_types("INFO", f"Processing prediction batch {batch_num + 1}")
            predictions, times = simulate_model_predictions(50)
            time.sleep(1)  # Brief pause between batches
        
        # Model drift simulation
        @logger.log_function_time
        def detect_model_drift():
            """Simulate model drift detection"""
            
            with logger.performance_profile("drift_detection"):
                # Simulate drift detection computation
                time.sleep(0.5)
                
                # Simulate drift metrics
                data_drift_score = random.uniform(0.02, 0.15)
                concept_drift_score = random.uniform(0.01, 0.08)
                
                logger.add_custom_metric("data_drift_score", data_drift_score)
                logger.add_custom_metric("concept_drift_score", concept_drift_score)
                
                # Check drift thresholds
                if data_drift_score > 0.1:
                    logger.log_types("ALERT", f"Data drift detected: {data_drift_score:.3f}")
                    logger.log_security_event("DATA_DRIFT", "HIGH", 
                                            f"Significant data drift detected: {data_drift_score:.3f}")
                
                if concept_drift_score > 0.05:
                    logger.log_types("ALERT", f"Concept drift detected: {concept_drift_score:.3f}")
                    logger.log_security_event("CONCEPT_DRIFT", "HIGH", 
                                            f"Concept drift detected: {concept_drift_score:.3f}")
                
                logger.log_with_context(
                    "SUCCESS",
                    "Drift detection completed",
                    context={
                        "data_drift_score": data_drift_score,
                        "concept_drift_score": concept_drift_score,
                        "drift_status": "DETECTED" if (data_drift_score > 0.1 or concept_drift_score > 0.05) else "NONE"
                    },
                    tags=["drift_detection", "model_monitoring"]
                )
        
        print("📊 Running drift detection...")
        detect_model_drift()
        
        # Generate monitoring insights
        print("\n🔍 Generating ML monitoring insights...")
        logger.view_insights(detailed=True)

if __name__ == "__main__":
    print("🔬 InsightLogger v1.5 - Data Science & ML Pipeline Examples")
    print("=" * 70)
    
    try:
        # Run data science pipeline
        data_science_pipeline()
        
        # Run ML monitoring example
        ml_model_monitoring_example()
        
        print("\n🎉 Data Science and ML examples completed successfully!")
        print("\nGenerated outputs:")
        print("  • Comprehensive performance analysis")
        print("  • Model training metrics and comparisons") 
        print("  • Data quality and feature engineering reports")
        print("  • Production monitoring simulation results")
        print("  • HTML dashboards for all pipelines")
        print("  • SQLite databases with detailed metrics")
        
    except KeyboardInterrupt:
        print("\n⏹️ Examples interrupted by user")
    except Exception as e:
        print(f"\n💥 Error in examples: {e}")
        import traceback
        traceback.print_exc()
