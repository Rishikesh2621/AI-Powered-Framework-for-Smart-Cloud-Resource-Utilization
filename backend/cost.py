class CloudCostEstimator:
    """
    Cloud Cost Estimation & Optimization Module.
    Calculates current vs optimized cloud infrastructure costs in Indian Rupees (INR / ₹) based on configurable pricing models.
    Fulfills Section 16 requirements.
    """
    def __init__(
        self,
        cpu_hourly_rate: float = 3.30,      # ₹3.30 per vCPU/hr
        ram_hourly_rate: float = 0.80,      # ₹0.80 per GB RAM/hr
        vm_base_hourly_rate: float = 10.00, # ₹10.00 per base VM instance/hr
        currency: str = "INR",
        currency_symbol: str = "₹"
    ):
        self.cpu_hourly_rate = cpu_hourly_rate
        self.ram_hourly_rate = ram_hourly_rate
        self.vm_base_hourly_rate = vm_base_hourly_rate
        self.currency = currency
        self.currency_symbol = currency_symbol

    def calculate_cost(
        self,
        active_vms: int,
        recommended_vms: int,
        duration_hours: float = 720.0  # 30 days default
    ) -> dict:
        """
        Calculates current vs optimized estimated cost over the specified duration in Indian Rupees (₹).
        """
        # Baseline Cost under Static Over-provisioned Allocation
        current_hourly = active_vms * (self.vm_base_hourly_rate + 4 * self.cpu_hourly_rate + 16 * self.ram_hourly_rate)
        current_total = current_hourly * duration_hours

        # Optimized Cost under AI Predictive Dynamic Scaling
        optimized_hourly = recommended_vms * (self.vm_base_hourly_rate + 4 * self.cpu_hourly_rate + 16 * self.ram_hourly_rate)
        optimized_total = optimized_hourly * duration_hours

        # Net Savings
        savings_total = max(0.0, current_total - optimized_total)
        savings_pct = (savings_total / current_total * 100.0) if current_total > 0 else 0.0

        return {
            "disclaimer": "Simulated Cloud Cost Calculations in Indian Rupees (INR — ₹)",
            "currency": self.currency,
            "currency_symbol": self.currency_symbol,
            "duration_hours": duration_hours,
            "active_vms": active_vms,
            "recommended_vms": recommended_vms,
            "hourly_rates": {
                "cpu_per_hour_inr": self.cpu_hourly_rate,
                "ram_per_hour_inr": self.ram_hourly_rate,
                "vm_base_per_hour_inr": self.vm_base_hourly_rate,
                "cpu_per_hour": self.cpu_hourly_rate,
                "ram_per_hour": self.ram_hourly_rate,
                "vm_per_hour": self.vm_base_hourly_rate
            },
            "current_estimated_cost_monthly": round(current_total, 2),
            "optimized_estimated_cost_monthly": round(optimized_total, 2),
            "estimated_savings_monthly": round(savings_total, 2),
            "estimated_savings_pct": round(savings_pct, 2)
        }
