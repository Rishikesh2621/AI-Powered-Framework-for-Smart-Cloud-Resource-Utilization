import React from 'react';
import { IndianRupee, TrendingDown, ShieldCheck, CheckCircle2, Server, ArrowRight } from 'lucide-react';

export default function OptimizationView({ insights }) {
  const financial = {
    baseline_monthly_cost: insights?.financial_impact?.baseline_monthly_cost_inr || insights?.financial_impact?.baseline_monthly_cost_usd || 207360.00,
    optimized_monthly_cost: insights?.financial_impact?.optimized_monthly_cost_inr || insights?.financial_impact?.optimized_monthly_cost_usd || 129600.00,
    monthly_savings: insights?.financial_impact?.monthly_savings_inr || insights?.financial_impact?.monthly_savings_usd || 77760.00,
    cost_reduction_pct: insights?.financial_impact?.cost_reduction_pct || 37.5,
    co2_emissions_saved_kg: insights?.financial_impact?.co2_emissions_saved_kg || 1144.4
  };

  const health = insights?.cluster_health || {
    avg_cpu_utilization: 48.5,
    avg_ram_utilization: 52.1,
    avg_active_vms: 8.2,
    underutilized_time_pct: 28.4,
    optimal_time_pct: 64.2,
    overutilized_time_pct: 7.4,
    bin_packing_efficiency_score: 88.5
  };

  const recommendations = insights?.recommendations || [
    { type: 'Right-Size Compute Nodes', action: 'Downgrade 3 underutilized c5.2xlarge nodes to c5.xlarge during off-peak hours', vm_tier: 'c5.xlarge', estimated_monthly_savings_inr: 28800, risk_level: 'Low' },
    { type: 'Scheduled Auto-Shutdown', action: 'Spin down 2 staging worker nodes during non-working hours (10 PM - 6 AM IST)', vm_tier: 'c5.large', estimated_monthly_savings_inr: 19200, risk_level: 'Low' },
    { type: 'Dynamic Memory Reclamation', action: 'Reclaim 32GB unused RAM cache across idle worker pools', vm_tier: 'Optimized RAM', estimated_monthly_savings_inr: 12500, risk_level: 'None' }
  ];

  return (
    <div>
      {/* Top Cost KPI Summary Grid in INR */}
      <div className="grid-4">
        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><IndianRupee size={18} /> Baseline Monthly Spend</span>
            <span className="badge badge-warning">UNOPTIMIZED</span>
          </div>
          <div className="metric-value">₹{Number(financial.baseline_monthly_cost).toLocaleString('en-IN')}</div>
          <div className="metric-sub">Static Overprovisioning Model</div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><IndianRupee size={18} /> AI-Optimized Monthly Spend</span>
            <span className="badge badge-success">DYNAMIC AI</span>
          </div>
          <div className="metric-value" style={{ color: 'var(--accent-emerald)' }}>
            ₹{Number(financial.optimized_monthly_cost).toLocaleString('en-IN')}
          </div>
          <div className="metric-sub">Smart Capacity Allocation</div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><TrendingDown size={18} /> Monthly Cost Savings</span>
            <span className="badge badge-success">-{financial.cost_reduction_pct}% REDUCTION</span>
          </div>
          <div className="metric-value" style={{ color: 'var(--accent-cyan)' }}>
            ₹{Number(financial.monthly_savings).toLocaleString('en-IN')} <span style={{ fontSize: '0.9rem' }}>/ mo</span>
          </div>
          <div className="metric-sub">Annualized: ₹{(Number(financial.monthly_savings) * 12).toLocaleString('en-IN')}</div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><ShieldCheck size={18} /> Resource Efficiency Score</span>
            <span className="badge badge-info">OPTIMIZED</span>
          </div>
          <div className="metric-value">{health.bin_packing_efficiency_score}%</div>
          <div className="metric-sub">CO₂ Saved: {financial.co2_emissions_saved_kg} kg/mo</div>
        </div>
      </div>

      {/* Cluster Load Distribution Breakdown */}
      <div className="grid-2">
        <div className="glass-card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>
            <Server size={20} /> Cluster Workload Time Distribution
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span>Optimal Load Zone (25% - 75% CPU)</span>
                <span style={{ fontWeight: 'bold', color: 'var(--accent-emerald)' }}>{health.optimal_time_pct}%</span>
              </div>
              <div style={{ height: '10px', width: '100%', background: '#E2E8F0', borderRadius: '5px' }}>
                <div style={{ height: '100%', width: `${health.optimal_time_pct}%`, background: 'var(--accent-emerald)', borderRadius: '5px' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span>Underutilized Waste Zone (&lt; 25% CPU)</span>
                <span style={{ fontWeight: 'bold', color: 'var(--accent-amber)' }}>{health.underutilized_time_pct}%</span>
              </div>
              <div style={{ height: '10px', width: '100%', background: '#E2E8F0', borderRadius: '5px' }}>
                <div style={{ height: '100%', width: `${health.underutilized_time_pct}%`, background: 'var(--accent-amber)', borderRadius: '5px' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span>High Hotspot Load Zone (&gt; 75% CPU)</span>
                <span style={{ fontWeight: 'bold', color: 'var(--accent-rose)' }}>{health.overutilized_time_pct}%</span>
              </div>
              <div style={{ height: '10px', width: '100%', background: '#E2E8F0', borderRadius: '5px' }}>
                <div style={{ height: '100%', width: `${health.overutilized_time_pct}%`, background: 'var(--accent-rose)', borderRadius: '5px' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Action Recommendations */}
        <div className="glass-card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>
            <CheckCircle2 size={20} /> AI Instance Right-Sizing Recommendations
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {recommendations.map((rec, idx) => (
              <div key={idx} style={{ padding: '14px', background: '#F8FAFC', borderRadius: '10px', border: '1px solid #E2E8F0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--accent-primary)' }}>{rec.type}</span>
                  <span style={{ fontSize: '0.82rem', color: 'var(--accent-emerald)', fontWeight: 700 }}>
                    +₹{Number(rec.estimated_monthly_savings_inr || rec.estimated_monthly_savings_usd || 18400).toLocaleString('en-IN')} / mo
                  </span>
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-main)', marginTop: '6px' }}>
                  {rec.action}
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                  Target Tier: {rec.vm_tier} | Risk Level: {rec.risk_level}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
