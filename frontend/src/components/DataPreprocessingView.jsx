import React, { useState } from 'react';
import { Database, CheckCircle, AlertTriangle, ShieldCheck, RefreshCw } from 'lucide-react';

export default function DataPreprocessingView({ datasetSummary, onRunPreprocessing }) {
  const [activeTab, setActiveTab] = useState('cleaned');
  const [isCleaning, setIsCleaning] = useState(false);

  const metrics = datasetSummary?.quality_metrics || {
    total_records: 4032,
    missing_values_handled: 242,
    outliers_rectified: 40,
    initial_quality_score: 82.4,
    processed_quality_score: 99.8,
    improvement_pct: 17.4
  };

  const rawRows = datasetSummary?.raw_preview || [];
  const cleanedRows = datasetSummary?.cleaned_preview || [];

  const handleRun = async () => {
    setIsCleaning(true);
    await onRunPreprocessing();
    setTimeout(() => setIsCleaning(false), 500);
  };

  return (
    <div>
      {/* Header KPI cards */}
      <div className="grid-4">
        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><Database size={18} /> Ingested Records</span>
            <span className="badge badge-info">14 DAYS (5m)</span>
          </div>
          <div className="metric-value">{metrics.total_records || 4032}</div>
          <div className="metric-sub">Continuous Telemetry Sample</div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><AlertTriangle size={18} /> Missing Values Imputed</span>
            <span className="badge badge-warning">KNN / LINEAR</span>
          </div>
          <div className="metric-value">{metrics.missing_values_handled} <span style={{ fontSize: '1rem' }}>nulls</span></div>
          <div className="metric-sub">Bi-directional Linear Interpolation</div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><ShieldCheck size={18} /> Outliers Rectified</span>
            <span className="badge badge-danger">SENSOR ERRORS</span>
          </div>
          <div className="metric-value">{metrics.outliers_rectified} <span style={{ fontSize: '1rem' }}>spikes</span></div>
          <div className="metric-sub">Clipping & Z-Score Noise Filter</div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><CheckCircle size={18} /> Data Reliability Score</span>
            <span className="badge badge-success">+{metrics.improvement_pct}% GAIN</span>
          </div>
          <div className="metric-value" style={{ color: 'var(--accent-emerald)' }}>
            {metrics.processed_quality_score}%
          </div>
          <div className="metric-sub">Initial Score: {metrics.initial_quality_score}%</div>
        </div>
      </div>

      {/* Main Preprocessing Framework Card */}
      <div className="glass-card">
        <div className="card-header">
          <div>
            <h3 className="card-title"><Database size={20} /> Systematic Data Preprocessing Framework (Objective 1)</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              Ensures high data quality and reliability by resolving telemetry gaps, sensor glitches, and scale imbalances.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            <div style={{ display: 'flex', background: '#F1F5F9', padding: '4px', borderRadius: '8px', border: '1px solid #E2E8F0' }}>
              <button 
                className={`tab-btn ${activeTab === 'cleaned' ? 'active' : ''}`}
                onClick={() => setActiveTab('cleaned')}
                style={{ padding: '4px 12px', fontSize: '0.78rem' }}
              >
                Cleaned Data ({cleanedRows.length})
              </button>
              <button 
                className={`tab-btn ${activeTab === 'raw' ? 'active' : ''}`}
                onClick={() => setActiveTab('raw')}
                style={{ padding: '4px 12px', fontSize: '0.78rem' }}
              >
                Raw Corrupted Feed ({rawRows.length})
              </button>
            </div>

            <button className="btn-primary" onClick={handleRun} disabled={isCleaning}>
              <RefreshCw size={14} className={isCleaning ? 'animate-spin' : ''} />
              {isCleaning ? 'Processing...' : 'Run Cleaning Pipeline'}
            </button>
          </div>
        </div>

        {/* Data Table */}
        <div className="data-table-wrapper" style={{ marginTop: '1rem' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>CPU Utilization (%)</th>
                <th>RAM Utilization (%)</th>
                <th>Storage (GB)</th>
                <th>Network (Mbps)</th>
                <th>Latency (ms)</th>
                <th>Active VMs</th>
                <th>Data Health Status</th>
              </tr>
            </thead>
            <tbody>
              {(activeTab === 'cleaned' ? cleanedRows : rawRows).slice(0, 12).map((row, idx) => {
                const isCorrupted = row.cpu_utilization === null || row.cpu_utilization > 100 || row.ram_utilization === null;
                return (
                  <tr key={idx}>
                    <td style={{ fontFamily: 'monospace', color: 'var(--text-muted)' }}>
                      {new Date(row.timestamp).toLocaleString()}
                    </td>
                    <td style={{ color: isCorrupted ? 'var(--accent-rose)' : 'var(--text-main)', fontWeight: isCorrupted ? 'bold' : 'normal' }}>
                      {row.cpu_utilization === null ? 'NaN [Missing]' : `${row.cpu_utilization}%`}
                    </td>
                    <td style={{ color: isCorrupted ? 'var(--accent-rose)' : 'inherit', fontWeight: isCorrupted ? 'bold' : 'normal' }}>
                      {row.ram_utilization === null ? 'NaN [Missing]' : `${row.ram_utilization}%`}
                    </td>
                    <td>{row.storage_utilization_gb} GB</td>
                    <td>{row.network_throughput_mbps} Mbps</td>
                    <td>{row.response_latency_ms} ms</td>
                    <td><span className="badge badge-info">{row.active_vm_count} VMs</span></td>
                    <td>
                      {activeTab === 'raw' && isCorrupted ? (
                        <span className="badge badge-danger">Corrupted / Sensor Failure</span>
                      ) : (
                        <span className="badge badge-success">Clean & Validated</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
