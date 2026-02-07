import requests
from datetime import datetime

BACKEND_LOG_URL = "http://127.0.0.1:8000/logs"

def send_log(service_name, level, message, request_id, endpoint):
    """
    Sends a log to the backend.
    Logging must NEVER crash the service.
    """
    payload = {
        "service_name": service_name,
        "level": level,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "endpoint": endpoint
    }

    try:
        requests.post(BACKEND_LOG_URL, json=payload, timeout=1)
    except Exception:
        # Logging failures should never break the service
        pass
