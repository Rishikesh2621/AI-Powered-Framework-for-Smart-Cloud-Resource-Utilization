import React from 'react';
import { Activity, Database, Sliders, Cpu, IndianRupee, Rocket, Bell, Layers } from 'lucide-react';

export default function TabsHeader({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'monitoring', label: '1. Data Collection & Live Telemetry', icon: Activity },
    { id: 'preprocessing', label: '2. Data Preprocessing Framework', icon: Database },
    { id: 'features', label: '3. Feature Engineering', icon: Sliders },
    { id: 'prediction', label: '4. AI Prediction Engine', icon: Cpu },
    { id: 'optimization', label: '5. Resource Optimization & Cost (₹)', icon: IndianRupee },
    { id: 'autoscale', label: '6. Auto Scaling & Allocation', icon: Rocket },
    { id: 'n8n', label: '7. Automation & Notifications (n8n)', icon: Bell },
    { id: 'methodology', label: '8. Methodology Architecture', icon: Layers },
  ];

  return (
    <div className="tabs-bar">
      {tabs.map((tab) => {
        const IconComponent = tab.icon;
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            className={`tab-btn ${isActive ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <IconComponent size={16} />
            <span>{tab.label}</span>
          </button>
        );
      })}
    </div>
  );
}
