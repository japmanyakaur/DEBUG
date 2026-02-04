import requests
from datetime import datetime

BACKEND_URL = "http://localhost:8000/logs"

def send_log(service, level, message, request_id, endpoint):
    payload = {
        "service_name": service,
        "level": level,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "endpoint": endpoint
    }

    requests.post(BACKEND_URL, json=payload)
