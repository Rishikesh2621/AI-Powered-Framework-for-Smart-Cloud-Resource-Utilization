import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import datetime
import os

from backend.data_generator import CloudDataGenerator
from backend.preprocessing import CloudDataPreprocessor
from backend.models import CloudPredictiveEngine
from backend.optimization import CloudResourceOptimizer
from backend.anomaly import CloudAnomalyDetector
from backend.cost import CloudCostEstimator
from backend.notifications import N8nAutomationNotifier

# Page Setup
st.set_page_config(
    page_title="Smart Cloud Resource Utilization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Clean Professional White Light Theme)
st.markdown("""
<style>
    /* Global App Background and Contrast */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] * {
        color: #1E293B !important;
    }
    p, span, label, h1, h2, h3, h4, h5, h6, div {
        color: #0F172A;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569 !important;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #2563EB;
    }
    .metric-label {
        font-size: 0.88rem;
        color: #475569;
        font-weight: 500;
    }
    .badge-normal {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #BBF7D0;
    }
    .badge-warning {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #FDE68A;
    }
    .badge-critical {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #FECACA;
    }
    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Caching
@st.cache_resource
def load_system_pipeline():
    data_gen = CloudDataGenerator(seed=42)
    preprocessor = CloudDataPreprocessor()
    predictor = CloudPredictiveEngine()
    optimizer = CloudResourceOptimizer()
    anomaly_det = CloudAnomalyDetector()
    cost_est = CloudCostEstimator()
    notifier = N8nAutomationNotifier()

    raw_df = data_gen.generate_historical_dataset(days=14, interval_minutes=5)
    cleaned_df, q_metrics = preprocessor.preprocess_raw_data(raw_df)
    featured_df = preprocessor.create_features(cleaned_df)
    split_data = preprocessor.prepare_train_test_split(featured_df)

    anomaly_det.fit(cleaned_df)
    eval_results = predictor.train_and_evaluate_all(split_data, target_name="cpu_utilization")

    return {
        "raw_df": raw_df,
        "cleaned_df": cleaned_df,
        "featured_df": featured_df,
        "split_data": split_data,
        "q_metrics": q_metrics,
        "eval_results": eval_results,
        "preprocessor": preprocessor,
        "predictor": predictor,
        "optimizer": optimizer,
        "anomaly_det": anomaly_det,
        "cost_est": cost_est,
        "notifier": notifier
    }

pipeline = load_system_pipeline()

# Sidebar Navigation (Section 17: 11 Pages)
st.sidebar.title("Cloud Intelligence")
st.sidebar.caption("Resource Optimization & Forecasting")

navigation_page = st.sidebar.radio(
    "Navigation Menu",
    [
        "1. Overview",
        "2. Data Upload",
        "3. Data Preprocessing",
        "4. EDA",
        "5. Model Training",
        "6. Prediction",
        "7. Anomaly Detection",
        "8. Resource Optimization",
        "9. Cost Analysis",
        "10. System Logs",
        "11. About Project"
    ]
)

st.sidebar.divider()
st.sidebar.info("**System Status**: Models Trained and Active")

# ----------------------------------------------------
# PAGE 1: OVERVIEW
# ----------------------------------------------------
if navigation_page == "1. Overview":
    st.markdown('<div class="main-title">Cloud Resource Intelligence Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Real-time Telemetry, Predictive Scaling, Cost Optimization & Health Monitoring</div>', unsafe_allow_html=True)

    # Fetch latest sample telemetry
    latest_row = pipeline["cleaned_df"].iloc[-1]
    curr_cpu = float(latest_row["cpu_utilization"])
    curr_ram = float(latest_row["ram_utilization"])

    # Sample Forecast
    preds = pipeline["predictor"].predict_future_demand(pipeline["split_data"]["X_test"], model_name="XGBoost", horizon_steps=12)
    pred_cpu = preds[0]["predicted_cpu"]
    pred_ram = preds[0]["predicted_ram"]

    # Scaling & Cost
    opt_decision = pipeline["optimizer"].evaluate_scaling_decision(curr_cpu, pred_cpu, curr_ram, pred_ram)
    cost_info = pipeline["cost_est"].calculate_cost(active_vms=8, recommended_vms=opt_decision["target_vms"])
    anomalies = pipeline["anomaly_det"].detect_anomalies(pipeline["cleaned_df"].tail(100))

    # Top KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Current CPU", f"{curr_cpu:.1f}%")
    with col2:
        st.metric("Current RAM", f"{curr_ram:.1f}%")
    with col3:
        st.metric("Predicted CPU (1h)", f"{pred_cpu:.1f}%")
    with col4:
        st.metric("Resource Status", opt_decision["recommendation"])
    with col5:
        st.metric("Est. Monthly Savings", f"₹{cost_info['estimated_savings_monthly']:,.2f}")

    st.divider()

    # Visual Charts Row
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Historical CPU and RAM Utilization")
        df_plot = pipeline["cleaned_df"].tail(200).copy()
        fig = px.line(df_plot, x="timestamp", y=["cpu_utilization", "ram_utilization"], labels={"value": "Utilization (%)", "timestamp": "Timestamp"}, template="plotly_white")
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Predicted Demand Forecast (1-Hour Horizon)")
        pred_df = pd.DataFrame(preds)
        fig_pred = px.bar(pred_df, x="minutes_ahead", y="predicted_cpu", text_auto=True, color="predicted_cpu", color_continuous_scale="Blues", labels={"minutes_ahead": "Minutes Ahead", "predicted_cpu": "Predicted CPU %"}, template="plotly_white")
        fig_pred.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig_pred, use_container_width=True)

    # Active Recommendation Summary
    st.subheader("Recommended Scaling Action")
    st.success(f"**Decision**: `{opt_decision['recommendation']}` — {opt_decision['reason']}")

# ----------------------------------------------------
# PAGE 2: DATA UPLOAD
# ----------------------------------------------------
elif navigation_page == "2. Data Upload":
    st.markdown('<div class="main-title">Cloud Dataset Upload & Column Mapping</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Support for Google Cluster Trace, Alibaba Trace, AWS CloudWatch, and Custom CSVs</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Cloud Utilization Dataset (CSV format)", type=["csv"])

    if uploaded_file is not None:
        try:
            df_up = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded file: {uploaded_file.name} ({len(df_up)} rows, {len(df_up.columns)} columns)")

            st.subheader("Dataset Preview")
            st.dataframe(df_up.head(10), use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Column Information")
                st.write(pd.DataFrame({"Column": df_up.columns, "Type": df_up.dtypes.astype(str), "Null Count": df_up.isna().sum().values}))

            with col2:
                st.subheader("Run Automatic Column Mapping & Preprocessing")
                impute_m = st.selectbox("Missing Value Method", ["ffill", "mean", "median", "bfill"])
                outlier_m = st.selectbox("Outlier Method", ["iqr", "zscore", "isolation_forest"])

                if st.button("Process & Save Dataset"):
                    cleaned_df, report = pipeline["preprocessor"].preprocess_raw_data(df_up, imputation_method=impute_m, outlier_method=outlier_m)
                    st.json(report)
                    st.success("Dataset successfully ingested into pipeline!")
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")
    else:
        st.info("Using default 14-Day Synthetic Cloud Workload Dataset.")
        st.dataframe(pipeline["raw_df"].head(10), use_container_width=True)

# ----------------------------------------------------
# PAGE 3: DATA PREPROCESSING
# ----------------------------------------------------
elif navigation_page == "3. Data Preprocessing":
    st.markdown('<div class="main-title">Data Preprocessing & Validation Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Objective 1: Cleaning, Imputation, Outlier Handling & Feature Scaling</div>', unsafe_allow_html=True)

    q = pipeline["q_metrics"]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Records", q.get("total_records_initial", len(pipeline["raw_df"])))
    with c2:
        st.metric("Missing Values Handled", q.get("missing_values_before", 0))
    with c3:
        st.metric("Duplicates Removed", q.get("duplicate_records_removed", 0))
    with c4:
        st.metric("Outliers Detected", q.get("outliers_detected", 0))

    st.subheader("Data Validation Report")
    st.json(q)

    st.subheader("Cleaned Dataset Sample")
    st.dataframe(pipeline["cleaned_df"].head(15), use_container_width=True)

# ----------------------------------------------------
# PAGE 4: EDA
# ----------------------------------------------------
elif navigation_page == "4. EDA":
    st.markdown('<div class="main-title">Exploratory Data Analysis (EDA)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Visualizing Resource Distribution, Trends, Peaks, and Correlations</div>', unsafe_allow_html=True)

    df = pipeline["cleaned_df"]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("CPU Utilization Distribution")
        fig_cpu = px.histogram(df, x="cpu_utilization", nbins=40, color_discrete_sequence=["#2563EB"], title="CPU Usage Histogram", template="plotly_white")
        fig_cpu.update_layout(paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig_cpu, use_container_width=True)

    with col2:
        st.subheader("RAM Utilization Distribution")
        fig_ram = px.histogram(df, x="ram_utilization", nbins=40, color_discrete_sequence=["#10B981"], title="RAM Usage Histogram", template="plotly_white")
        fig_ram.update_layout(paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig_ram, use_container_width=True)

    st.subheader("Feature Correlation Matrix")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[numeric_cols].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="Blues", aspect="auto", template="plotly_white")
    fig_corr.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig_corr, use_container_width=True)

# ----------------------------------------------------
# PAGE 5: MODEL TRAINING
# ----------------------------------------------------
elif navigation_page == "5. Model Training":
    st.markdown('<div class="main-title">Machine Learning Model Benchmarking</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Objective 2: Training & Validating Random Forest, XGBoost, and LSTM Models</div>', unsafe_allow_html=True)

    evals = pipeline["eval_results"]

    # Model Leaderboard Table
    st.subheader("Model Benchmark Comparison")
    rows = []
    for model_name, metrics in evals.items():
        rows.append({
            "Model Name": model_name,
            "MAE": metrics["mae"],
            "RMSE": metrics["rmse"],
            "R² Score": metrics["r2"],
            "MAPE (%)": f"{metrics['mape']:.2f}%",
            "Accuracy (%)": f"{metrics['accuracy_pct']:.2f}%"
        })
    st.table(pd.DataFrame(rows))

    best_m = pipeline["predictor"].best_model_name
    st.success(f"**Top Performing Model**: `{best_m}` (Selected based on lowest RMSE)")

# ----------------------------------------------------
# PAGE 6: PREDICTION
# ----------------------------------------------------
elif navigation_page == "6. Prediction":
    st.markdown('<div class="main-title">Resource Demand Prediction Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Forecast Future CPU, RAM & VM Capacity Demands</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sel_model = st.selectbox("Select Predictive Model", ["XGBoost", "Random Forest", "LSTM Neural Net"])
    with c2:
        horizon = st.slider("Prediction Horizon (Steps of 5 mins)", min_value=1, max_value=24, value=12)

    preds = pipeline["predictor"].predict_future_demand(pipeline["split_data"]["X_test"], model_name=sel_model, horizon_steps=horizon)
    pred_df = pd.DataFrame(preds)

    st.dataframe(pred_df, use_container_width=True)

    fig_f = px.line(pred_df, x="minutes_ahead", y=["predicted_cpu", "predicted_ram"], markers=True, title=f"Forecast Horizon via {sel_model}", template="plotly_white")
    fig_f.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig_f, use_container_width=True)

# ----------------------------------------------------
# PAGE 7: ANOMALY DETECTION
# ----------------------------------------------------
elif navigation_page == "7. Anomaly Detection":
    st.markdown('<div class="main-title">AI Anomaly Detection Module</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Isolation Forest Detection of CPU Spikes & Abnormal Consumption</div>', unsafe_allow_html=True)

    anomalies = pipeline["anomaly_det"].detect_anomalies(pipeline["cleaned_df"])
    st.info(f"Total Anomalous Records Identified: {len(anomalies)}")

    if anomalies:
        anom_df = pd.DataFrame(anomalies)
        st.dataframe(anom_df[["timestamp", "cpu_utilization", "ram_utilization", "severity", "reasons"]], use_container_width=True)

        fig_a = px.scatter(anom_df, x="cpu_utilization", y="ram_utilization", color="severity", hover_data=["reasons"], title="Anomaly Cluster Map", template="plotly_white")
        fig_a.update_layout(paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig_a, use_container_width=True)

# ----------------------------------------------------
# PAGE 8: RESOURCE OPTIMIZATION
# ----------------------------------------------------
elif navigation_page == "8. Resource Optimization":
    st.markdown('<div class="main-title">Smart Resource Optimization & Auto-Scaling</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Objective 3: Intelligent Resource Allocation & Cooldown Protection</div>', unsafe_allow_html=True)

    curr_cpu = st.slider("Current CPU Utilization (%)", 0.0, 100.0, 75.0)
    pred_cpu = st.slider("Predicted CPU Utilization (%)", 0.0, 100.0, 86.0)

    dec = pipeline["optimizer"].evaluate_scaling_decision(curr_cpu, pred_cpu)

    st.subheader(f"Scaling Decision: {dec['recommendation']}")
    st.write(f"**Target VM Count**: {dec['target_vms']} VMs (Current: {dec['active_vms']})")
    st.caption(dec["reason"])

    # Immediate INR Financial Impact
    scaled_cost = pipeline["cost_est"].calculate_cost(active_vms=dec["active_vms"], recommended_vms=dec["target_vms"])
    if dec["target_vms"] < dec["active_vms"]:
        st.info(f"**Resource Optimization Benefit**: Scaling down saves approximately **₹{scaled_cost['estimated_savings_monthly']:,.2f} / month** ({scaled_cost['estimated_savings_pct']:.1f}% reduction in infrastructure bill).")
    elif dec["target_vms"] > dec["active_vms"]:
        st.warning(f"**Proactive Scaled Fleet**: Target allocation adjusts compute cost to **₹{scaled_cost['optimized_estimated_cost_monthly']:,.2f} / month** to maintain strict SLA latency limits.")
    else:
        st.success(f"**Optimal Operating Zone**: Running efficiently at current baseline **₹{scaled_cost['current_estimated_cost_monthly']:,.2f} / month**.")

# ----------------------------------------------------
# PAGE 9: COST ANALYSIS
# ----------------------------------------------------
elif navigation_page == "9. Cost Analysis":
    st.markdown('<div class="main-title">Cloud Cost Optimization & Estimation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Calculate Operational Savings in Indian Rupees under AI Predictive Resource Allocation</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        active_vms = st.number_input("Active VMs (Static Baseline)", min_value=1, max_value=64, value=8)
    with c2:
        recommended_vms = st.number_input("Recommended VMs (AI Optimized)", min_value=1, max_value=64, value=5)

    res = pipeline["cost_est"].calculate_cost(active_vms, recommended_vms)

    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Current Est. Monthly Cost", f"₹{res['current_estimated_cost_monthly']:,.2f}")
    with k2:
        st.metric("Optimized Est. Monthly Cost", f"₹{res['optimized_estimated_cost_monthly']:,.2f}")
    with k3:
        st.metric("Estimated Monthly Savings", f"₹{res['estimated_savings_monthly']:,.2f}", f"{res['estimated_savings_pct']:.1f}% savings")

    st.caption(f"Pricing Model (INR Rates): Base VM ₹10.00/hr | vCPU ₹3.30/hr | RAM ₹0.80/GB/hr — {res['disclaimer']}")

# ----------------------------------------------------
# PAGE 10: SYSTEM LOGS
# ----------------------------------------------------
elif navigation_page == "10. System Logs":
    st.markdown('<div class="main-title">System Logs & n8n Automation History</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Track Webhook Dispatches, Model Training Logs & Execution Events</div>', unsafe_allow_html=True)

    st.subheader("n8n Alert Trigger Simulation")
    ev_type = st.text_input("Event Type", "CPU_UTILIZATION_CRITICAL")
    sev = st.selectbox("Severity", ["CRITICAL", "WARNING", "INFO"])
    msg = st.text_area("Alert Message", "Predicted CPU demand exceeds 88% threshold.")

    if st.button("Dispatch n8n Webhook Alert"):
        res = pipeline["notifier"].dispatch_alert(event_type=ev_type, severity=sev, message=msg, metrics={"cpu": 88.5})
        st.json(res)

    st.subheader("Notification Dispatch History")
    st.dataframe(pd.DataFrame(pipeline["notifier"].get_history()), use_container_width=True)

# ----------------------------------------------------
# PAGE 11: ABOUT PROJECT
# ----------------------------------------------------
elif navigation_page == "11. About Project":
    st.markdown('<div class="main-title">About the Project</div>', unsafe_allow_html=True)
    st.markdown("""
    ### AI-Powered Framework for Smart Cloud Resource Utilization
    **B.Tech Major Project II**
    
    #### Project Aim
    Develop an AI-powered framework that analyzes historical cloud resource utilization data, predicts future resource demand, detects abnormal utilization patterns, recommends optimal resource allocation, and supports automated scaling decisions to improve resource utilization, reduce resource wastage and cloud operational costs, and maintain system performance.
    
    #### Objectives
    1. **Data Preprocessing Framework**: Ingest and clean cloud telemetry with automated validation reports.
    2. **Predictive ML Models**: Forecast cloud demand using Random Forest, XGBoost, and LSTM models.
    3. **Resource Optimization Engine**: Deliver intelligent scaling decisions, anomaly detection, and cost estimation.
    
    #### Tech Stack
    * **Backend**: FastAPI, Uvicorn, SQLAlchemy
    * **ML / Data**: Pandas, NumPy, Scikit-learn, XGBoost, PyTorch/LSTM, Joblib
    * **Frontend**: Streamlit, Plotly, Vite + React
    * **Database**: MySQL / SQLite
    * **Automation & Containerization**: n8n Webhooks, Docker, Docker Compose
    """)
