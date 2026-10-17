import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

from backend.main import app, STATE
from backend.data_generator import CloudDataGenerator
from backend.preprocessing import CloudDataPreprocessor
from backend.models import CloudPredictiveEngine
from backend.optimization import CloudResourceOptimizer
from backend.anomaly import CloudAnomalyDetector
from backend.cost import CloudCostEstimator

client = TestClient(app)

def test_data_generator():
    gen = CloudDataGenerator(seed=42)
    df = gen.generate_historical_dataset(days=1, interval_minutes=5)
    assert len(df) > 0
    assert "cpu_utilization" in df.columns
    assert "ram_utilization" in df.columns

def test_preprocessing_and_features():
    gen = CloudDataGenerator(seed=42)
    raw_df = gen.generate_historical_dataset(days=1, interval_minutes=5)
    
    preprocessor = CloudDataPreprocessor()
    cleaned_df, report = preprocessor.preprocess_raw_data(raw_df)
    assert report["status"] == "COMPLETED_SUCCESSFULLY"
    assert cleaned_df["cpu_utilization"].isna().sum() == 0

    featured_df = preprocessor.create_features(cleaned_df)
    assert "cpu_lag_1" in featured_df.columns
    assert "cpu_rolling_mean_3" in featured_df.columns

    split_data = preprocessor.prepare_train_test_split(featured_df)
    assert "X_train" in split_data
    assert "X_test" in split_data

def test_ml_model_training_and_prediction():
    gen = CloudDataGenerator(seed=42)
    raw_df = gen.generate_historical_dataset(days=1, interval_minutes=5)
    preprocessor = CloudDataPreprocessor()
    cleaned_df, _ = preprocessor.preprocess_raw_data(raw_df)
    featured_df = preprocessor.create_features(cleaned_df)
    split_data = preprocessor.prepare_train_test_split(featured_df)

    predictor = CloudPredictiveEngine()
    eval_results = predictor.train_and_evaluate_all(split_data, target_name="cpu_utilization")

    assert "XGBoost" in eval_results
    assert "Random Forest" in eval_results
    assert eval_results["XGBoost"]["rmse"] >= 0.0

    preds = predictor.predict_future_demand(split_data["X_test"], model_name="XGBoost", horizon_steps=6)
    assert len(preds) == 6
    assert "predicted_cpu" in preds[0]

def test_anomaly_detector():
    gen = CloudDataGenerator(seed=42)
    df = gen.generate_historical_dataset(days=1, interval_minutes=5)
    preprocessor = CloudDataPreprocessor()
    cleaned_df, _ = preprocessor.preprocess_raw_data(df)

    anomaly_det = CloudAnomalyDetector()
    anomalies = anomaly_det.detect_anomalies(cleaned_df)
    assert isinstance(anomalies, list)

    live_check = anomaly_det.evaluate_live_metric(cpu=95.0, ram=92.0)
    assert live_check["severity"] == "Critical"

def test_optimization_engine():
    optimizer = CloudResourceOptimizer()
    decision_up = optimizer.evaluate_scaling_decision(current_cpu=85.0, predicted_cpu=88.0, active_vms=8)
    assert decision_up["recommendation"] == "SCALE UP"
    assert decision_up["target_vms"] > 8

    decision_down = optimizer.evaluate_scaling_decision(current_cpu=20.0, predicted_cpu=22.0, active_vms=8)
    assert decision_down["recommendation"] == "SCALE DOWN"
    assert decision_down["target_vms"] < 8

def test_cost_estimator():
    estimator = CloudCostEstimator()
    res = estimator.calculate_cost(active_vms=8, recommended_vms=5, duration_hours=720)
    assert res["estimated_savings_monthly"] > 0.0
    assert res["estimated_savings_pct"] > 0.0

def test_api_endpoints():
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "ONLINE"

    r_summary = client.get("/api/dataset/summary")
    assert r_summary.status_code == 200
    assert "quality_metrics" in r_summary.json()

    r_predict = client.post("/api/models/predict?model_name=XGBoost&horizon_steps=6")
    assert r_predict.status_code == 200
    assert len(r_predict.json()["predictions"]) == 6

    r_opt = client.get("/api/recommendation")
    assert r_opt.status_code == 200
    assert "recommendation" in r_opt.json()
