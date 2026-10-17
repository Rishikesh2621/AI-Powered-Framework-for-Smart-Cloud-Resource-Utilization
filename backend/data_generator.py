import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

class CloudDataGenerator:
    """
    Generates synthetic but realistic cloud resource utilization telemetry data.
    Includes daily seasonality, weekly trends, traffic bursts, missing values, and noise.
    """
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)

    def generate_historical_dataset(self, days: int = 14, interval_minutes: int = 5) -> pd.DataFrame:
        start_time = datetime.now() - timedelta(days=days)
        total_steps = int((days * 24 * 60) / interval_minutes)
        
        timestamps = [start_time + timedelta(minutes=i * interval_minutes) for i in range(total_steps)]
        
        data = []
        
        for i, ts in enumerate(timestamps):
            hour = ts.hour + ts.minute / 60.0
            day_of_week = ts.weekday()
            
            # Base diurnal cycle (peak at 14:00, trough at 04:00)
            daily_pattern = 0.5 + 0.35 * np.sin((hour - 8) * np.pi / 12)
            
            # Weekend reduction factor (30% drop on Sat/Sun)
            weekend_factor = 0.7 if day_of_week >= 5 else 1.0
            
            # Base load calculation
            base_load = daily_pattern * weekend_factor
            
            # Burst traffic spikes (5% chance of sudden high load)
            burst = np.random.uniform(20.0, 45.0) if np.random.rand() < 0.04 else 0.0
            
            # Gaussian noise
            noise = np.random.normal(0, 3.0)
            
            # Compute CPU Utilization (%)
            cpu_pct = np.clip(base_load * 65.0 + burst + noise + 15.0, 5.0, 98.0)
            
            # RAM Utilization (%) - correlated with CPU with some inertia
            ram_pct = np.clip(cpu_pct * 0.75 + 15.0 + np.random.normal(0, 2.0), 10.0, 95.0)
            
            # Network Throughput (Mbps)
            network_mbps = np.clip(cpu_pct * 12.5 + burst * 8.0 + np.random.normal(0, 25.0), 50.0, 1500.0)
            
            # Active Requests / sec
            requests_per_sec = np.clip(cpu_pct * 45.0 + burst * 30.0 + np.random.normal(0, 100.0), 100.0, 5000.0)
            
            # Storage Utilization (GB) - steady slight growth with oscillation
            storage_gb = 250.0 + (i / total_steps) * 80.0 + np.random.normal(0, 1.5)
            
            # Response Latency (ms) - exponentially rises with CPU load over 80%
            base_latency = 25.0 + (cpu_pct / 100.0) * 15.0
            if cpu_pct > 80.0:
                base_latency += (cpu_pct - 80.0) ** 1.8
            latency_ms = float(np.clip(base_latency + np.random.normal(0, 4.0), 10.0, 500.0))
            
            # Active VM Count (reactive baseline: 4 to 20 VMs based on load)
            active_vms = int(np.clip(np.ceil(cpu_pct / 6.0), 4, 24))
            active_pods = active_vms * 8 + int(np.random.uniform(-3, 5))
            
            data.append({
                "timestamp": ts.isoformat(),
                "cpu_utilization": round(float(cpu_pct), 2),
                "ram_utilization": round(float(ram_pct), 2),
                "storage_utilization_gb": round(float(storage_gb), 2),
                "network_throughput_mbps": round(float(network_mbps), 2),
                "request_rate_per_sec": round(float(requests_per_sec), 2),
                "response_latency_ms": round(float(latency_ms), 2),
                "active_vm_count": active_vms,
                "active_pod_count": active_pods
            })
            
        df = pd.DataFrame(data)
        
        # Inject realistic data issues for Preprocessing Demonstration (Objective 1)
        # 1. Missing values (~3% of CPU/RAM entries)
        nan_indices_cpu = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
        nan_indices_ram = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
        df.loc[nan_indices_cpu, "cpu_utilization"] = np.nan
        df.loc[nan_indices_ram, "ram_utilization"] = np.nan
        
        # 2. Outliers (anomalous negative values or sensor glitches)
        outlier_indices = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
        df.loc[outlier_indices, "cpu_utilization"] = 999.9  # sensor error spike
        
        return df

    def generate_live_metric(self, current_vms: int = 8, spike_active: bool = False) -> dict:
        now = datetime.now()
        hour = now.hour + now.minute / 60.0
        
        daily_pattern = 0.5 + 0.35 * np.sin((hour - 8) * np.pi / 12)
        base_cpu = daily_pattern * 60.0 + 15.0
        
        if spike_active:
            base_cpu += random.uniform(30.0, 45.0)
            
        cpu = float(np.clip(base_cpu + random.gauss(0, 4.0), 5.0, 99.0))
        ram = float(np.clip(cpu * 0.75 + 15.0 + random.gauss(0, 2.0), 10.0, 95.0))
        network = float(np.clip(cpu * 14.0 + random.gauss(0, 30.0), 60.0, 1600.0))
        req_rate = float(np.clip(cpu * 40.0 + random.gauss(0, 80.0), 120.0, 4800.0))
        
        base_latency = 20.0 + (cpu / 100.0) * 20.0
        if cpu > 80.0:
            base_latency += (cpu - 80.0) ** 1.6
        latency = float(np.clip(base_latency + random.gauss(0, 3.0), 10.0, 450.0))
        
        return {
            "timestamp": now.isoformat(),
            "cpu_utilization": round(cpu, 2),
            "ram_utilization": round(ram, 2),
            "storage_utilization_gb": round(280.0 + random.uniform(0, 5), 2),
            "network_throughput_mbps": round(network, 2),
            "request_rate_per_sec": round(req_rate, 2),
            "response_latency_ms": round(latency, 2),
            "active_vm_count": current_vms,
            "active_pod_count": current_vms * 8
        }
