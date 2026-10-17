import os
import io
import pandas as pd
import numpy as np
from fastapi import FastAPI, Query, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

from backend.database import init_db, get_db
from backend.models_db import ResourceMetricsDB, PredictionDB, AnomalyDB, OptimizationLogDB, CostLogDB
from backend.data_generator import CloudDataGenerator
from backend.preprocessing import CloudDataPreprocessor
from backend.models import CloudPredictiveEngine
from backend.optimization import CloudResourceOptimizer
from backend.autoscaler import CloudAutoScalerSimulator
from backend.notifications import N8nAutomationNotifier
from backend.anomaly import CloudAnomalyDetector
from backend.cost import CloudCostEstimator

app = FastAPI(
    title="AI-Powered Framework for Smart Cloud Resource Utilization API",
    description="ML-driven Cloud Resource Demand Forecasting, Optimization, Anomaly Detection, Auto-Scaling & n8n Automation Engine",
    version="2.0.0"
)

# Enable CORS for Frontend Applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database Schema
init_db()

# Global Controllers
data_gen = CloudDataGenerator(seed=42)
preprocessor = CloudDataPreprocessor()
predictor_engine = CloudPredictiveEngine()
optimizer = CloudResourceOptimizer()
autoscaler = CloudAutoScalerSimulator()
notifier = N8nAutomationNotifier()
anomaly_detector = CloudAnomalyDetector()
cost_estimator = CloudCostEstimator()

# System State Cache
STATE = {
    "raw_df": None,
    "cleaned_df": None,
    "featured_df": None,
    "split_data": None,
    "quality_metrics": {},
    "evaluation_results": {},
    "live_vms": 8,
    "spike_active": False
}

def initialize_system(days: int = 3):
    if STATE["raw_df"] is None:
        print(f"[INIT] Generating {days}-day cloud telemetry dataset...")
        STATE["raw_df"] = data_gen.generate_historical_dataset(days=days, interval_minutes=5)
        
        # Preprocessing & Feature Engineering
        cleaned_df, q_metrics = preprocessor.preprocess_raw_data(STATE["raw_df"])
        featured_df = preprocessor.create_features(cleaned_df)
        split_data = preprocessor.prepare_train_test_split(featured_df)
        
        STATE["cleaned_df"] = cleaned_df
        STATE["featured_df"] = featured_df
        STATE["split_data"] = split_data
        STATE["quality_metrics"] = q_metrics
        
        # Anomaly Detection Initialization
        anomaly_detector.fit(cleaned_df)
        
        # Train ML Models on startup (Random Forest, XGBoost, LSTM)
        print("[INIT] Training Predictive Models (Random Forest, XGBoost, LSTM)...")
        STATE["evaluation_results"] = predictor_engine.train_and_evaluate_all(split_data, target_name="cpu_utilization")
def ensure_system_initialized():
    if STATE["raw_df"] is None:
        initialize_system()

@app.on_event("startup")
def on_startup():
    ensure_system_initialized()

# Request Schemas
class TriggerAlertRequest(BaseModel):
    event_type: str
    severity: str
    message: str
    webhook_url: Optional[str] = None
    metrics: Optional[dict] = None

class OptimizeRequest(BaseModel):
    current_cpu: float
    predicted_cpu: float
    current_ram: Optional[float] = 50.0
    predicted_ram: Optional[float] = 50.0
    active_vms: Optional[int] = 8

class CostEstimateRequest(BaseModel):
    active_vms: int = 8
    recommended_vms: int = 5
    duration_hours: float = 720.0

@app.get("/health")
@app.get("/")
def health_check():
    return {
        "status": "ONLINE",
        "project": "AI-Powered Framework for Smart Cloud Resource Utilization",
        "aim": "Predict cloud demand, detect anomalies, optimize allocation, reduce cloud cost, and automate scaling using AI/ML",
        "objectives_fulfilled": 3,
        "database": "CONNECTED",
        "docs_url": "http://127.0.0.1:8000/docs"
    }

@app.get("/api/metrics/live")
def get_live_metrics(spike: Optional[bool] = False):
    if spike:
        STATE["spike_active"] = True
    metric = data_gen.generate_live_metric(current_vms=STATE["live_vms"], spike_active=STATE["spike_active"])
    if STATE["spike_active"]:
        STATE["spike_active"] = False

    # Check live anomaly
    anomaly_status = anomaly_detector.evaluate_live_metric(metric["cpu_utilization"], metric["ram_utilization"], metric["network_throughput_mbps"])
    metric["anomaly_status"] = anomaly_status
    return metric

@app.get("/api/dataset/summary")
def get_dataset_summary():
    ensure_system_initialized()
    raw_df = STATE["raw_df"]
    cleaned_df = STATE["cleaned_df"]
    
    return {
        "total_records": len(raw_df) if raw_df is not None else 0,
        "raw_preview": raw_df.head(15).replace({np.nan: None}).to_dict(orient="records") if raw_df is not None else [],
        "cleaned_preview": cleaned_df.head(15).replace({np.nan: None}).to_dict(orient="records") if cleaned_df is not None else [],
        "quality_metrics": STATE["quality_metrics"],
        "columns": list(cleaned_df.columns) if cleaned_df is not None else []
    }

@app.post("/api/upload-csv")
async def upload_custom_csv(
    file: UploadFile = File(...),
    imputation_method: str = Form("ffill"),
    outlier_method: str = Form("iqr")
):
    """
    Accepts arbitrary cloud workload CSV uploads (Google Trace, Alibaba, AWS CloudWatch, custom CSVs).
    Performs column auto-mapping and runs preprocessing pipeline.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    contents = await file.read()
    df_uploaded = pd.read_csv(io.BytesIO(contents))

    cleaned_df, q_metrics = preprocessor.preprocess_raw_data(
        df_uploaded,
        imputation_method=imputation_method,
        outlier_method=outlier_method
    )
    featured_df = preprocessor.create_features(cleaned_df)
    split_data = preprocessor.prepare_train_test_split(featured_df)

    STATE["raw_df"] = df_uploaded
    STATE["cleaned_df"] = cleaned_df
    STATE["featured_df"] = featured_df
    STATE["split_data"] = split_data
    STATE["quality_metrics"] = q_metrics

    # Train models on newly uploaded dataset
    STATE["evaluation_results"] = predictor_engine.train_and_evaluate_all(split_data, target_name="cpu_utilization")
    anomaly_detector.fit(cleaned_df)

    return {
        "message": f"Dataset '{file.filename}' uploaded and processed successfully.",
        "row_count": len(cleaned_df),
        "column_count": len(cleaned_df.columns),
        "validation_report": q_metrics,
        "columns": list(cleaned_df.columns)
    }

@app.post("/api/preprocess/run")
def run_preprocessing(imputation_method: str = Query("ffill"), outlier_method: str = Query("iqr")):
    cleaned_df, q_metrics = preprocessor.preprocess_raw_data(
        STATE["raw_df"],
        imputation_method=imputation_method,
        outlier_method=outlier_method
    )
    featured_df = preprocessor.create_features(cleaned_df)
    split_data = preprocessor.prepare_train_test_split(featured_df)
    
    STATE["cleaned_df"] = cleaned_df
    STATE["featured_df"] = featured_df
    STATE["split_data"] = split_data
    STATE["quality_metrics"] = q_metrics
    
    return {
        "message": "Data preprocessing and feature engineering executed successfully.",
        "quality_metrics": q_metrics,
        "engineered_feature_count": len(split_data["feature_names"]),
        "feature_names": split_data["feature_names"]
    }

@app.post("/api/models/train")
def train_models(target: str = Query("cpu_utilization")):
    if STATE["split_data"] is None:
        run_preprocessing()
        
    results = predictor_engine.train_and_evaluate_all(STATE["split_data"], target_name=target)
    STATE["evaluation_results"] = results
    return {
        "message": f"ML predictive models (Random Forest, XGBoost, LSTM) trained and evaluated for target: '{target}'",
        "leaderboard": results,
        "best_model": predictor_engine.best_model_name
    }

@app.get("/api/models/evaluation")
def get_model_evaluation():
    ensure_system_initialized()
    return {
        "leaderboard": STATE["evaluation_results"],
        "best_model": predictor_engine.best_model_name,
        "tested_models": ["Random Forest", "XGBoost", "LSTM Neural Net"]
    }

@app.post("/api/models/predict")
def predict_demand(model_name: str = Query("XGBoost"), horizon_steps: int = Query(12)):
    ensure_system_initialized()
    if STATE["featured_df"] is None:
        raise HTTPException(status_code=400, detail="Data pipeline not initialized.")
        
    predictions = predictor_engine.predict_future_demand(
        latest_features=STATE["split_data"]["X_test"],
        model_name=model_name,
        horizon_steps=horizon_steps
    )
    return {
        "model_used": model_name,
        "horizon_steps": horizon_steps,
        "predictions": predictions
    }

@app.get("/api/anomalies")
def get_anomalies():
    ensure_system_initialized()
    if STATE["cleaned_df"] is None:
        raise HTTPException(status_code=400, detail="Cleaned dataset not available.")
    
    anomalies = anomaly_detector.detect_anomalies(STATE["cleaned_df"])
    return {
        "total_anomalies_detected": len(anomalies),
        "anomalies": anomalies[:50]  # top 50
    }

@app.get("/api/recommendation")
@app.post("/api/optimize")
def optimize_resource_allocation(req: Optional[OptimizeRequest] = None):
    curr_cpu = req.current_cpu if req else 68.0
    pred_cpu = req.predicted_cpu if req else 84.0
    curr_ram = req.current_ram if req else 60.0
    pred_ram = req.predicted_ram if req else 78.0
    vms = req.active_vms if req else STATE["live_vms"]

    decision = optimizer.evaluate_scaling_decision(
        current_cpu=curr_cpu,
        predicted_cpu=pred_cpu,
        current_ram=curr_ram,
        predicted_ram=pred_ram,
        active_vms=vms
    )
    return decision

@app.get("/api/cost-estimate")
def get_cost_estimate(active_vms: int = 8, recommended_vms: int = 5, duration_hours: float = 720.0):
    return cost_estimator.calculate_cost(active_vms, recommended_vms, duration_hours)

@app.get("/api/optimization/insights")
def get_optimization_insights():
    if STATE["cleaned_df"] is None:
        raise HTTPException(status_code=400, detail="Data not available.")
    return optimizer.evaluate_optimization(STATE["cleaned_df"])

@app.post("/api/autoscale/simulate")
def simulate_autoscale():
    if STATE["cleaned_df"] is None:
        raise HTTPException(status_code=400, detail="Data not available.")
    sim_result = autoscaler.simulate_scaling_policies(STATE["cleaned_df"])
    return sim_result

@app.post("/api/notifications/n8n-trigger")
def trigger_n8n_alert(req: TriggerAlertRequest):
    metrics = req.metrics or {"cpu_utilization": 88.5, "active_vms": STATE["live_vms"]}
    res = notifier.dispatch_alert(
        event_type=req.event_type,
        severity=req.severity,
        message=req.message,
        metrics=metrics,
        webhook_url=req.webhook_url
    )
    return res

@app.get("/api/notifications/history")
def get_notification_history():
    return {"history": notifier.get_history()}
