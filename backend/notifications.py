import requests
from datetime import datetime

class N8nAutomationNotifier:
    """
    Automation & Notification System with n8n Webhook Integration.
    Fulfills Methodology Stage 7 (n8n Automation & Notifications).
    """
    def __init__(self):
        self.notification_history = []
        # Pre-populate sample alert history
        self.notification_history.append({
            "id": "ALT-1001",
            "timestamp": datetime.now().isoformat(),
            "event_type": "Auto-Scaling Executed",
            "severity": "INFO",
            "message": "AI Predictive Scaler proactively allocated +4 c5.2xlarge instances before 14:00 peak surge.",
            "n8n_status": "TRIGGERED_SUCCESS",
            "payload_sent": {"action": "SCALE_OUT", "instances": 4, "target_cpu": 72.5}
        })

    def dispatch_alert(self, event_type: str, severity: str, message: str, metrics: dict, webhook_url: str = None) -> dict:
        alert_id = f"ALT-{len(self.notification_history) + 1001}"
        timestamp = datetime.now().isoformat()
        
        payload = {
            "alert_id": alert_id,
            "timestamp": timestamp,
            "source": "AI-Cloud-Resource-Optimizer",
            "event_type": event_type,
            "severity": severity,
            "message": message,
            "metrics": metrics
        }
        
        status = "SIMULATED_SUCCESS"
        response_code = 200
        
        if webhook_url and webhook_url.startswith("http"):
            try:
                res = requests.post(webhook_url, json=payload, timeout=3)
                status = "N8N_WEBHOOK_DELIVERED"
                response_code = res.status_code
            except Exception as e:
                status = f"N8N_WEBHOOK_FAILED ({str(e)})"
                response_code = 500
                
        record = {
            "id": alert_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "severity": severity,
            "message": message,
            "n8n_status": status,
            "response_code": response_code,
            "payload_sent": payload
        }
        
        self.notification_history.insert(0, record)
        return record

    def get_history(self) -> list[dict]:
        return self.notification_history[:20]
