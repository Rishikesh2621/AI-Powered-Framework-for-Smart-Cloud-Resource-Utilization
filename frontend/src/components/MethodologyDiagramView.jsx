import React from 'react';
import { Database, Sliders, Cpu, IndianRupee, Rocket, Bell, Activity, Layers, CheckCircle } from 'lucide-react';

export default function MethodologyDiagramView({ setActiveTab }) {
  const stages = [
    {
      step: 1,
      title: 'Data Collection',
      icon: Activity,
      tab: 'monitoring',
      color: '#6366f1',
      bullets: ['Collect real-time data from cloud resources', 'CPU, RAM, Storage, Network, VM, etc.']
    },
    {
      step: 2,
      title: 'Data Preprocessing',
      icon: Database,
      tab: 'preprocessing',
      color: '#10b981',
      bullets: ['Data Cleaning', 'Handling Missing Values', 'Normalization & Outlier Filtering']
    },
    {
      step: 3,
      title: 'Feature Engineering',
      icon: Sliders,
      tab: 'features',
      color: '#f59e0b',
      bullets: ['Extract important features (Lags & Rolling Means)', 'Build meaningful domain representations']
    },
    {
      step: 4,
      title: 'AI Prediction Engine',
      icon: Cpu,
      tab: 'prediction',
      color: '#06b6d4',
      bullets: ['Train ML/DL models (RF, XGBoost, NeuralNet)', 'Predict future resource demand']
    },
    {
      step: 5,
      title: 'Resource Optimization & Cost',
      icon: IndianRupee,
      tab: 'optimization',
      color: '#ec4899',
      bullets: ['Optimize resource allocation', 'Load balancing & right-sizing', 'Cost savings estimation in INR (₹)']
    },
    {
      step: 6,
      title: 'Auto Scaling & Resource Allocation',
      icon: Rocket,
      tab: 'autoscale',
      color: '#8b5cf6',
      bullets: ['Scale Up / Scale Down execution', 'Allocate resources dynamically']
    },
    {
      step: 7,
      title: 'Automation & Notifications (n8n)',
      icon: Bell,
      tab: 'n8n',
      color: '#3b82f6',
      bullets: ['Automated workflows', 'Alerts & Reports', 'Email / Admin notifications']
    },
    {
      step: 8,
      title: 'Monitoring & Dashboard',
      icon: Layers,
      tab: 'monitoring',
      color: '#14b8a6',
      bullets: ['Live Monitoring', 'Performance Analytics', 'Cost & Resource Insights']
    }
  ];

  return (
    <div className="glass-card">
      <div className="card-header" style={{ marginBottom: '2rem' }}>
        <div>
          <h2 className="card-title" style={{ fontSize: '1.4rem' }}>
            <Layers size={26} color="var(--accent-primary)" /> Project Methodology Architecture
          </h2>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            End-to-End Circular Methodology for Smart Cloud Resource Utilization & Auto-Scaling. Click any module to jump to its live implementation.
          </p>
        </div>
        <span className="badge badge-success">8 STAGE PIPELINE COMPLETE</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
        {stages.map((stg) => {
          const IconComp = stg.icon;
          return (
            <div
              key={stg.step}
              onClick={() => setActiveTab(stg.tab)}
              style={{
                background: '#FFFFFF',
                borderRadius: '10px',
                padding: '1.25rem',
                border: '1px solid #E2E8F0',
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.04)',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div style={{
                    width: '38px',
                    height: '38px',
                    borderRadius: '8px',
                    background: `${stg.color}15`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: stg.color
                  }}>
                    <IconComp size={20} />
                  </div>
                  <div>
                    <span style={{ fontSize: '0.72rem', color: stg.color, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                      Stage 0{stg.step}
                    </span>
                    <h4 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#0F172A' }}>{stg.title}</h4>
                  </div>
                </div>
                <CheckCircle size={18} color={stg.color} />
              </div>

              <ul style={{ paddingLeft: '1.2rem', margin: 0, fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                {stg.bullets.map((b, i) => (
                  <li key={i} style={{ marginBottom: '4px' }}>{b}</li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </div>
  );
}
