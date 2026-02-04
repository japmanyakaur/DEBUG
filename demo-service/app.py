import time
import random
import uuid
import os
from fastapi import FastAPI, Request
from logger import send_log

app = FastAPI()
SERVICE_NAME = "demo-service"


# -----------------------------
# Middleware: add request_id
# -----------------------------
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """
    Every incoming request gets a unique request_id.
    This helps us correlate logs later.
    """
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    return response


# -----------------------------
# Health endpoint (PingWatch)
# -----------------------------
@app.get("/health")
async def health(request: Request):
    """
    Randomly becomes slow to simulate performance issues.
    """
    delay = 3 if random.random() < 0.3 else 0.05
    time.sleep(delay)

    send_log({
        "service_name": SERVICE_NAME,
        "level": "INFO",
        "message": "Health check successful",
        "timestamp": time.time(),
        "request_id": request.state.request_id,
        "endpoint": "/health"
    })

    return {"status": "ok"}


# -----------------------------
# Payment endpoint
# -----------------------------
@app.post("/pay")
async def pay(request: Request):
    """
    Randomly fails to simulate backend issues.
    """
    if random.random() < 0.4:
        send_log({
            "service_name": SERVICE_NAME,
            "level": "ERROR",
            "message": "Payment failed: database timeout",
            "timestamp": time.time(),
            "request_id": request.state.request_id,
            "endpoint": "/pay"
        })
        return {"error": "payment failed"}

    send_log({
        "service_name": SERVICE_NAME,
        "level": "INFO",
        "message": "Payment successful",
        "timestamp": time.time(),
        "request_id": request.state.request_id,
        "endpoint": "/pay"
    })

    return {"status": "payment success"}


# -----------------------------
# Crash endpoint (demo only)
# -----------------------------
@app.post("/crash")
async def crash(request: Request):
    """
    Immediately crashes the service.
    Used to demo incidents.
    """
    send_log({
        "service_name": SERVICE_NAME,
        "level": "ERROR",
        "message": "Service crashed intentionally",
        "timestamp": time.time(),
        "request_id": request.state.request_id,
        "endpoint": "/crash"
    })

    os._exit(1)
