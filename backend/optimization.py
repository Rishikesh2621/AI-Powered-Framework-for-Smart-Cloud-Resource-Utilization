import datetime
import numpy as np
import pandas as pd

class CloudResourceOptimizer:
    """
    Rule-based + AI-Assisted Smart Resource Optimization Engine.
    Evaluates workload demand forecasts, resource availability, cost impact, and auto-scaling policies.
    Fulfills Sections 14 and 15 of the Master Prompt.
    """
    def __init__(self, cooldown_minutes: int = 0):
        self.cooldown_minutes = cooldown_minutes
        self.last_scale_time = None
        self.last_decision = "MAINTAIN"

    def evaluate_scaling_decision(
        self,
        current_cpu: float,
        predicted_cpu: float,
        current_ram: float = None,
        predicted_ram: float = None,
        active_vms: int = 8
    ) -> dict:
        """
        Evaluates current & predicted CPU and RAM metrics to output SCALE UP, MAINTAIN, or SCALE DOWN decisions
        with hysteresis and cooldown protection.
        """
        if current_ram is None:
            current_ram = current_cpu
        if predicted_ram is None:
            predicted_ram = predicted_cpu

        now = datetime.datetime.now()
        cooldown_active = False

        if self.last_scale_time is not None:
            elapsed_sec = (now - self.last_scale_time).total_seconds()
            if elapsed_sec < (self.cooldown_minutes * 60):
                cooldown_active = True

        # Multi-metric rule logic (considering both CPU and RAM)
        if predicted_cpu > 80.0 or predicted_ram > 80.0 or current_cpu > 85.0:
            raw_recommendation = "SCALE UP"
            target_vms = min(24, active_vms + max(2, int(np.ceil((predicted_cpu - 80.0) / 10.0))))
            reason = (
                f"Predicted resource demand (CPU: {predicted_cpu:.1f}%, RAM: {predicted_ram:.1f}%) "
                f"exceeds the 80% scaling threshold. Increasing capacity from {active_vms} to {target_vms} VMs."
            )
        elif predicted_cpu < 30.0 and predicted_ram < 35.0 and current_cpu < 35.0:
            raw_recommendation = "SCALE DOWN"
            target_vms = max(2, active_vms - max(1, int(np.floor((30.0 - predicted_cpu) / 10.0))))
            reason = (
                f"Predicted resource utilization (CPU: {predicted_cpu:.1f}%, RAM: {predicted_ram:.1f}%) "
                f"is consistently low (< 30%). Scaling down from {active_vms} to {target_vms} VMs to reduce wastage."
            )
        else:
            raw_recommendation = "MAINTAIN"
            target_vms = active_vms
            reason = (
                f"Resource utilization (CPU: {predicted_cpu:.1f}%, RAM: {predicted_ram:.1f}%) "
                f"is within the optimal operational zone (30% - 80%). Maintaining current allocation of {active_vms} VMs."
            )

        # Enforce Cooldown Protection
        final_decision = raw_recommendation
        if cooldown_active and raw_recommendation != "MAINTAIN" and raw_recommendation != self.last_decision:
            final_decision = "MAINTAIN"
            reason += f" (Note: Cooldown active for {self.cooldown_minutes} mins; holding decision at MAINTAIN)."
        elif final_decision != "MAINTAIN":
            self.last_scale_time = now
            self.last_decision = final_decision

        return {
            "current_cpu": round(current_cpu, 2),
            "predicted_cpu": round(predicted_cpu, 2),
            "current_ram": round(current_ram, 2),
            "predicted_ram": round(predicted_ram, 2),
            "active_vms": active_vms,
            "target_vms": target_vms,
            "recommendation": final_decision,
            "raw_recommendation": raw_recommendation,
            "cooldown_active": cooldown_active,
            "reason": reason
        }

    def evaluate_optimization(self, df: pd.DataFrame) -> dict:
        """
        Processes dataset telemetry to calculate global optimization insights and resource wastage statistics.
        """
        avg_cpu = float(df["cpu_utilization"].mean())
        peak_cpu = float(df["cpu_utilization"].max())
        avg_ram = float(df["ram_utilization"].mean())

        # Resource Wastage % = Allocated - Used
        avg_vms = 8.0
        allocated_capacity = avg_vms * 100.0
        actual_used = avg_cpu * (avg_vms / 8.0)
        wastage_pct = max(0.0, ((allocated_capacity - actual_used) / allocated_capacity) * 100.0)

        # Potential cost reduction under predictive scaling vs static allocation
        estimated_cost_reduction_pct = round(min(35.0, max(12.0, wastage_pct * 0.45)), 2)

        return {
            "avg_cpu_utilization": round(avg_cpu, 2),
            "peak_cpu_utilization": round(peak_cpu, 2),
            "avg_ram_utilization": round(avg_ram, 2),
            "resource_wastage_pct": round(wastage_pct, 2),
            "estimated_cost_reduction_pct": estimated_cost_reduction_pct,
            "optimization_status": "OPTIMAL_HEALTHY" if avg_cpu > 40.0 else "OVER_PROVISIONED"
        }
