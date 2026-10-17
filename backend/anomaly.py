import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class CloudAnomalyDetector:
    """
    AI Anomaly Detection Engine powered by Isolation Forest.
    Detects sudden CPU spikes, abnormal RAM consumption, network anomalies, and workload surges.
    Fulfills Section 13 requirements.
    """
    def __init__(self, contamination: float = 0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        features = ["cpu_utilization", "ram_utilization"]
        if "network_throughput_mbps" in df.columns:
            features.append("network_throughput_mbps")
        if "request_rate_per_sec" in df.columns:
            features.append("request_rate_per_sec")

        valid_df = df[features].fillna(df[features].median())
        self.model.fit(valid_df)
        self.is_fitted = True

    def detect_anomalies(self, df: pd.DataFrame) -> list[dict]:
        features = ["cpu_utilization", "ram_utilization"]
        if "network_throughput_mbps" in df.columns:
            features.append("network_throughput_mbps")
        if "request_rate_per_sec" in df.columns:
            features.append("request_rate_per_sec")

        valid_df = df[features].fillna(df[features].median())
        
        if not self.is_fitted:
            self.fit(df)

        scores = self.model.decision_function(valid_df)
        preds = self.model.predict(valid_df)

        anomalies = []
        for idx, (is_anomaly, score) in enumerate(zip(preds, scores)):
            row = df.iloc[idx]
            cpu = float(row.get("cpu_utilization", 0.0))
            ram = float(row.get("ram_utilization", 0.0))
            net = float(row.get("network_throughput_mbps", 0.0))
            ts = str(row.get("timestamp", idx))

            # Threshold & Severity Logic
            severity = "Normal"
            reasons = []

            if is_anomaly == -1 or cpu >= 85.0 or ram >= 85.0:
                if cpu >= 90.0 or ram >= 90.0:
                    severity = "Critical"
                else:
                    severity = "Warning"

                if cpu >= 85.0:
                    reasons.append(f"Sudden CPU Spike: {cpu:.1f}%")
                if ram >= 85.0:
                    reasons.append(f"Unusual RAM Consumption: {ram:.1f}%")
                if net > 500.0:
                    reasons.append(f"Abnormal Network Traffic: {net:.1f} MB/s")
                if not reasons:
                    reasons.append("Unusual Workload Pattern Detected by Isolation Forest")

                anomalies.append({
                    "id": idx + 1,
                    "timestamp": ts,
                    "cpu_utilization": round(cpu, 2),
                    "ram_utilization": round(ram, 2),
                    "network_mbps": round(net, 2),
                    "anomaly_score": round(float(score), 4),
                    "severity": severity,
                    "reasons": ", ".join(reasons)
                })

        return anomalies

    def evaluate_live_metric(self, cpu: float, ram: float, network: float = 0.0) -> dict:
        """
        Instant anomaly check for live stream metrics.
        """
        severity = "Normal"
        description = "System operating within healthy telemetry bounds."

        if cpu >= 90.0 or ram >= 90.0:
            severity = "Critical"
            description = f"Critical Resource Usage! CPU={cpu:.1f}%, RAM={ram:.1f}%"
        elif cpu >= 80.0 or ram >= 80.0:
            severity = "Warning"
            description = f"High Resource Demand Warning: CPU={cpu:.1f}%, RAM={ram:.1f}%"

        return {
            "cpu": cpu,
            "ram": ram,
            "network": network,
            "severity": severity,
            "description": description
        }
