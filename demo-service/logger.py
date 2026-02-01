"""

Sends structured logs from this service to the
central LogLite backend.

Logging failures must never affect service uptime.
"""

import requests

LOG_BACKEND_URL = "http://localhost:8000/logs"

def send_log(log: dict):
    """
    Sends log data to central logging backend 
     simulates real microservice log shipping.
    """
    try:
        requests.post(
            LOG_BACKEND_URL,
            json=log,
            timeout=1
        )
    except Exception:
        # Log failure should NEVER crash the service
        print(" Failed to send log")