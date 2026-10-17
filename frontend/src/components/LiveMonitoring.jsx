import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Cpu, HardDrive, Wifi, Server, Zap, AlertTriangle, Clock } from 'lucide-react';

export default function LiveMonitoring({ liveMetric, historyMetrics, triggerSpike }) {
  const [metricHistory, setMetricHistory] = useState([]);

  useEffect(() => {
    if (liveMetric && liveMetric.timestamp) {
      const timeLabel = new Date(liveMetric.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      setMetricHistory((prev) => {
        const updated = [...prev, { ...liveMetric, timeLabel }];
        return updated.slice(-30); // Keep last 30 readings
      });
    }
  }, [liveMetric]);

  const currentCpu = liveMetric?.cpu_utilization ?? 48.5;
  const currentRam = liveMetric?.ram_utilization ?? 52.1;
  const currentNet = liveMetric?.network_throughput_mbps ?? 620.0;
  const currentVms = liveMetric?.active_vm_count ?? 8;
  const currentLatency = liveMetric?.response_latency_ms ?? 24.5;

  return (
    <div>
      {/* Top Stat Cards Grid */}
      <div className="grid-4">
        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><Cpu size={18} /> CPU Utilization</span>
            <span className={`badge ${currentCpu > 80 ? 'badge-danger' : currentCpu > 60 ? 'badge-warning' : 'badge-success'}`}>
              {currentCpu > 80 ? 'HIGH LOAD' : 'NORMAL'}
            </span>
          </div>
          <div className="metric-value">{currentCpu.toFixed(1)}%</div>
          <div className="metric-sub">
            <Zap size={14} color="#6366f1" /> Allocated: {currentVms * 8} vCPUs ({currentVms} Nodes)
          </div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><HardDrive size={18} /> Memory (RAM)</span>
            <span className="badge badge-info">DYNAMIC</span>
          </div>
          <div className="metric-value">{currentRam.toFixed(1)}%</div>
          <div className="metric-sub">
            Allocated: {currentVms * 16} GB RAM
          </div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><Wifi size={18} /> Network Bandwidth</span>
            <span className="badge badge-info">IN / OUT</span>
          </div>
          <div className="metric-value">{currentNet.toFixed(0)} <span style={{ fontSize: '1rem' }}>Mbps</span></div>
          <div className="metric-sub">
            Active Requests: {(currentCpu * 38).toFixed(0)} req/sec
          </div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title"><Server size={18} /> Compute Instances</span>
            <span className="badge badge-success">ACTIVE FLEET</span>
          </div>
          <div className="metric-value">{currentVms} <span style={{ fontSize: '1rem' }}>c5.2xlarge</span></div>
          <div className="metric-sub">
            <Clock size={14} /> Latency: {currentLatency.toFixed(1)} ms
          </div>
        </div>
      </div>

      {/* Main Real-Time Telemetry Chart */}
      <div className="glass-card" style={{ marginBottom: '1.5rem' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title"><Zap size={20} /> Live Telemetry Metric Stream (Data Collection Module)</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              Real-time ingestion of cloud resource utilization signals (CPU, Memory, Network Throughput).
            </p>
          </div>
          <button className="btn-danger" onClick={triggerSpike}>
            <AlertTriangle size={16} /> Simulate Sudden Load Spike (+40%)
          </button>
        </div>

        <div style={{ width: '100%', height: 340, marginTop: '1rem' }}>
          <ResponsiveContainer>
            <AreaChart data={metricHistory}>
              <defs>
                <linearGradient id="cpuGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#2563eb" stopOpacity={0.0}/>
                </linearGradient>
                <linearGradient id="ramGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0284c7" stopOpacity={0.25}/>
                  <stop offset="95%" stopColor="#0284c7" stopOpacity={0.0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="timeLabel" stroke="#64748b" tick={{ fontSize: 12, fill: '#475569' }} />
              <YAxis domain={[0, 100]} stroke="#64748b" tick={{ fontSize: 12, fill: '#475569' }} unit="%" />
              <Tooltip 
                contentStyle={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', color: '#0f172a', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
                labelStyle={{ color: '#0f172a', fontWeight: 600 }}
              />
              <Area type="monotone" dataKey="cpu_utilization" name="CPU Utilization %" stroke="#2563eb" strokeWidth={2.5} fillOpacity={1} fill="url(#cpuGrad)" />
              <Area type="monotone" dataKey="ram_utilization" name="RAM Utilization %" stroke="#0284c7" strokeWidth={2} fillOpacity={1} fill="url(#ramGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
