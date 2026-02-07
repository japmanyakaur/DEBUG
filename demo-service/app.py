from fastapi import FastAPI, Request
import time
import random
import uuid
from logger import send_log

app = FastAPI()
SERVICE_NAME = "demo-service"


# -----------------------------
# Add request_id to every request
# -----------------------------
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    return await call_next(request)


# -----------------------------
# Health endpoint
# -----------------------------
@app.get("/health")
def health(request: Request):
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)

    send_log(
        SERVICE_NAME,
        "INFO",
        f"Health check took {delay:.2f}s",
        request.state.request_id,
        "/health"
    )

    return {"status": "ok", "latency": delay}


# -----------------------------
# Payment endpoint
# -----------------------------
@app.post("/pay")
def pay(request: Request):
    if random.random() < 0.5:
        send_log(
            SERVICE_NAME,
            "ERROR",
            "Payment service timeout",
            request.state.request_id,
            "/pay"
        )
        return {"status": "failed"}

    send_log(
        SERVICE_NAME,
        "INFO",
        "Payment successful",
        request.state.request_id,
        "/pay"
    )
    return {"status": "success"}


# -----------------------------
# Crash endpoint (controlled crash)
# -----------------------------
@app.get("/crash")
def crash(request: Request):
    send_log(
        SERVICE_NAME,
        "ERROR",
        "Service crashed intentionally",
        request.state.request_id,
        "/crash"
    )
    raise Exception("Crash simulated")
