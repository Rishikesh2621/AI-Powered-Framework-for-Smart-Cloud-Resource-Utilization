import React from 'react';
import { Cpu, Activity, ShieldCheck, Zap, RefreshCw } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onRefresh, isLiveStreaming, setIsLiveStreaming }) {
  return (
    <header className="navbar">
      <div className="brand-container">
        <div className="brand-icon">
          <Cpu size={24} />
        </div>
        <div>
          <h1 className="brand-title">Smart Cloud AI Framework</h1>
          <div className="brand-subtitle">Resource Utilization & Auto-Scaling System</div>
        </div>
      </div>

      <div className="nav-actions">
        <button 
          className={`btn-secondary ${isLiveStreaming ? 'active' : ''}`}
          onClick={() => setIsLiveStreaming(!isLiveStreaming)}
          style={{ padding: '6px 14px', fontSize: '0.8rem' }}
        >
          <Zap size={14} color={isLiveStreaming ? '#10b981' : '#94a3b8'} />
          {isLiveStreaming ? 'Live Stream Active' : 'Paused'}
        </button>

        <button 
          className="btn-secondary"
          onClick={onRefresh}
          style={{ padding: '6px 14px', fontSize: '0.8rem' }}
        >
          <RefreshCw size={14} />
          Sync State
        </button>
      </div>
    </header>
  );
}
