import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import TabsHeader from './components/TabsHeader';

import LiveMonitoring from './components/LiveMonitoring';
import DataPreprocessingView from './components/DataPreprocessingView';
import FeatureEngineeringView from './components/FeatureEngineeringView';
import PredictionEngineView from './components/PredictionEngineView';
import OptimizationView from './components/OptimizationView';
import AutoScalerSimView from './components/AutoScalerSimView';
import AutomationN8nView from './components/AutomationN8nView';
import MethodologyDiagramView from './components/MethodologyDiagramView';

const API_BASE = 'http://127.0.0.1:8000';

export default function App() {
  const [activeTab, setActiveTab] = useState('monitoring');
  const [isLiveStreaming, setIsLiveStreaming] = useState(true);

  // API States
  const [liveMetric, setLiveMetric] = useState(null);
  const [datasetSummary, setDatasetSummary] = useState(null);
  const [leaderboard, setLeaderboard] = useState({});
  const [predictions, setPredictions] = useState([]);
  const [optimizationInsights, setOptimizationInsights] = useState(null);
  const [autoScaleData, setAutoScaleData] = useState(null);
  const [notificationHistory, setNotificationHistory] = useState([]);

  // 1. Live Telemetry Poller
  useEffect(() => {
    let interval = null;
    if (isLiveStreaming) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/api/metrics/live`);
          if (res.ok) {
            const data = await res.json();
            setLiveMetric(data);
          }
        } catch (e) {
          console.log('Live stream fetch error:', e);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isLiveStreaming]);

  // 2. Initial Data Sync
  const fetchAllState = async () => {
    try {
      // Fetch Dataset Summary
      const dsRes = await fetch(`${API_BASE}/api/dataset/summary`);
      if (dsRes.ok) setDatasetSummary(await dsRes.json());

      // Fetch Model Evaluation Leaderboard
      const evRes = await fetch(`${API_BASE}/api/models/evaluation`);
      if (evRes.ok) {
        const evData = await evRes.json();
        setLeaderboard(evData.leaderboard || {});
      }

      // Fetch Initial Forecast Predictions
      const prRes = await fetch(`${API_BASE}/api/models/predict?model_name=XGBoost&horizon_steps=12`, { method: 'POST' });
      if (prRes.ok) {
        const prData = await prRes.json();
        setPredictions(prData.predictions || []);
      }

      // Fetch Optimization Insights
      const optRes = await fetch(`${API_BASE}/api/optimization/insights`);
      if (optRes.ok) setOptimizationInsights(await optRes.json());

      // Fetch Auto-Scaler Simulation Data
      const simRes = await fetch(`${API_BASE}/api/autoscale/simulate`, { method: 'POST' });
      if (simRes.ok) setAutoScaleData(await simRes.json());

      // Fetch Notification History
      const n8nRes = await fetch(`${API_BASE}/api/notifications/history`);
      if (n8nRes.ok) {
        const n8nData = await n8nRes.json();
        setNotificationHistory(n8nData.history || []);
      }
    } catch (err) {
      console.error('API Sync Error:', err);
    }
  };

  useEffect(() => {
    fetchAllState();
  }, []);

  // Action Handlers
  const handleTriggerSpike = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/metrics/live?spike=true`);
      if (res.ok) setLiveMetric(await res.json());
    } catch (e) {
      console.error(e);
    }
  };

  const handleRunPreprocessing = async () => {
    try {
      await fetch(`${API_BASE}/api/preprocess/run`, { method: 'POST' });
      await fetchAllState();
    } catch (e) {
      console.error(e);
    }
  };

  const handleTrainModels = async (target) => {
    try {
      const res = await fetch(`${API_BASE}/api/models/train?target=${target}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setLeaderboard(data.leaderboard || {});
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleFetchPredictions = async (modelName, horizonSteps) => {
    try {
      const res = await fetch(`${API_BASE}/api/models/predict?model_name=${modelName}&horizon_steps=${horizonSteps}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setPredictions(data.predictions || []);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSimulateAutoScaler = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/autoscale/simulate`, { method: 'POST' });
      if (res.ok) setAutoScaleData(await res.json());
    } catch (e) {
      console.error(e);
    }
  };

  const handleTriggerN8n = async (payload) => {
    try {
      const res = await fetch(`${API_BASE}/api/notifications/n8n-trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        const historyRes = await fetch(`${API_BASE}/api/notifications/history`);
        if (historyRes.ok) {
          const hData = await historyRes.json();
          setNotificationHistory(hData.history || []);
        }
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="app-container">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onRefresh={fetchAllState}
        isLiveStreaming={isLiveStreaming}
        setIsLiveStreaming={setIsLiveStreaming}
      />

      <TabsHeader activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="main-content">
        {activeTab === 'monitoring' && (
          <LiveMonitoring
            liveMetric={liveMetric}
            triggerSpike={handleTriggerSpike}
          />
        )}

        {activeTab === 'preprocessing' && (
          <DataPreprocessingView
            datasetSummary={datasetSummary}
            onRunPreprocessing={handleRunPreprocessing}
          />
        )}

        {activeTab === 'features' && (
          <FeatureEngineeringView />
        )}

        {activeTab === 'prediction' && (
          <PredictionEngineView
            leaderboard={leaderboard}
            predictions={predictions}
            onTrainModels={handleTrainModels}
            onFetchPredictions={handleFetchPredictions}
          />
        )}

        {activeTab === 'optimization' && (
          <OptimizationView insights={optimizationInsights} />
        )}

        {activeTab === 'autoscale' && (
          <AutoScalerSimView
            autoScaleData={autoScaleData}
            onSimulate={handleSimulateAutoScaler}
          />
        )}

        {activeTab === 'n8n' && (
          <AutomationN8nView
            notificationHistory={notificationHistory}
            onTriggerN8n={handleTriggerN8n}
          />
        )}

        {activeTab === 'methodology' && (
          <MethodologyDiagramView setActiveTab={setActiveTab} />
        )}
      </main>
    </div>
  );
}
