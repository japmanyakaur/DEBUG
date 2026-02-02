import requests

LOG_BACKEND_URL = "http://127.0.0.1:8000/logs"

def send_log(log: dict):
    try:
        requests.post(
            LOG_BACKEND_URL,
            json=log,
            timeout=1
        )
    except Exception:
        print("Failed to send log")
