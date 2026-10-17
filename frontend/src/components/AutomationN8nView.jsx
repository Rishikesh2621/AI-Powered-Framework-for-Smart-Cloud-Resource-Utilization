import React, { useState } from 'react';
import { Bell, Send, CheckCircle, AlertTriangle, Code, Play } from 'lucide-react';

export default function AutomationN8nView({ notificationHistory, onTriggerN8n }) {
  const [webhookUrl, setWebhookUrl] = useState('');
  const [eventType, setEventType] = useState('Auto-Scaling Executed');
  const [severity, setSeverity] = useState('INFO');
  const [customMsg, setCustomMsg] = useState('AI Predictive Scaler pre-allocated 4 compute nodes ahead of peak demand surge.');
  const [isSending, setIsSending] = useState(false);

  const handleSend = async () => {
    setIsSending(true);
    await onTriggerN8n({
      event_type: eventType,
      severity: severity,
      message: customMsg,
      webhook_url: webhookUrl
    });
    setTimeout(() => setIsSending(false), 500);
  };

  return (
    <div>
      <div className="grid-2">
        {/* Left Card: Trigger Webhook Bench */}
        <div className="glass-card">
          <div className="card-header">
            <h3 className="card-title"><Bell size={20} /> n8n Webhook & Notification Dispatcher</h3>
            <span className="badge badge-info">AUTOMATION STAGE 7</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginTop: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                n8n Webhook Endpoint URL (Optional Live Webhook)
              </label>
              <input 
                type="text" 
                className="text-input" 
                placeholder="https://n8n.your-domain.com/webhook/cloud-alert"
                value={webhookUrl}
                onChange={(e) => setWebhookUrl(e.target.value)}
                style={{ width: '100%' }}
              />
            </div>

            <div style={{ display: 'flex', gap: '12px' }}>
              <div style={{ flex: 1 }}>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                  Event Type
                </label>
                <select className="select-input" value={eventType} onChange={(e) => setEventType(e.target.value)} style={{ width: '100%' }}>
                  <option value="Auto-Scaling Executed">Auto-Scaling Executed</option>
                  <option value="High Utilization Warning">High Utilization Warning</option>
                  <option value="Anomalous Traffic Spike">Anomalous Traffic Spike</option>
                  <option value="Cost Anomaly Detected">Cost Anomaly Detected</option>
                </select>
              </div>

              <div style={{ flex: 1 }}>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                  Severity Level
                </label>
                <select className="select-input" value={severity} onChange={(e) => setSeverity(e.target.value)} style={{ width: '100%' }}>
                  <option value="INFO">INFO</option>
                  <option value="WARNING">WARNING</option>
                  <option value="CRITICAL">CRITICAL</option>
                </select>
              </div>
            </div>

            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                Alert Message
              </label>
              <input 
                type="text" 
                className="text-input" 
                value={customMsg}
                onChange={(e) => setCustomMsg(e.target.value)}
                style={{ width: '100%' }}
              />
            </div>

            <button className="btn-primary" onClick={handleSend} disabled={isSending}>
              <Send size={16} />
              {isSending ? 'Dispatching Payload...' : 'Dispatch n8n Webhook Alert'}
            </button>
          </div>
        </div>

        {/* Right Card: n8n Workflow Process Map */}
        <div className="glass-card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>
            <Code size={20} /> n8n Automated Workflow Pipeline
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ padding: '12px', background: '#EFF6FF', borderRadius: '8px', border: '1px solid #BFDBFE' }}>
              <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#1E40AF' }}>Node 1: Webhook Trigger Listener</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>Receives POST payload from FastAPI AI Engine</div>
            </div>

            <div style={{ padding: '12px', background: '#F0FDF4', borderRadius: '8px', border: '1px solid #BBF7D0' }}>
              <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#166534' }}>Node 2: Severity Switch & Filter</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>Routes CRITICAL alerts to Slack/SMS, INFO to Admin Feed</div>
            </div>

            <div style={{ padding: '12px', background: '#FAF5FF', borderRadius: '8px', border: '1px solid #E9D5FF' }}>
              <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#6D28D9' }}>Node 3: Cloud Provider API Executor</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>Executes AWS EC2 / GCP Compute instance scaling API calls</div>
            </div>
          </div>
        </div>
      </div>

      {/* Notification Log Table */}
      <div className="glass-card" style={{ marginTop: '1.5rem' }}>
        <div className="card-header">
          <h3 className="card-title"><Bell size={20} /> Dispatch Log Feed</h3>
          <span className="badge badge-success">{notificationHistory.length} EVENTS LOGGED</span>
        </div>

        <div className="data-table-wrapper" style={{ marginTop: '1rem' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Alert ID</th>
                <th>Timestamp</th>
                <th>Event Type</th>
                <th>Severity</th>
                <th>Message</th>
                <th>n8n Status</th>
              </tr>
            </thead>
            <tbody>
              {notificationHistory.map((item) => (
                <tr key={item.id}>
                  <td style={{ fontFamily: 'monospace', fontWeight: 'bold' }}>{item.id}</td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{new Date(item.timestamp).toLocaleTimeString()}</td>
                  <td>{item.event_type}</td>
                  <td>
                    <span className={`badge ${item.severity === 'CRITICAL' ? 'badge-danger' : item.severity === 'WARNING' ? 'badge-warning' : 'badge-info'}`}>
                      {item.severity}
                    </span>
                  </td>
                  <td style={{ fontSize: '0.82rem' }}>{item.message}</td>
                  <td>
                    <span className="badge badge-success">{item.n8n_status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
