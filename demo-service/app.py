import time
import random
import uuid
import os
from fastapi import FastAPI, Request
from logger import send_log

app = FastAPI()

SERVICE_NAME = "demo-service"

# Middleware to attach request_id
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    return response


@app.get("/health")
async def health(request: Request):
    delay = 3 if random.random() < 0.3 else 0.05
    time.sleep(delay)

    send_log({
        "service_name": SERVICE_NAME,
        "level": "INFO",
        "message": "Health check ping",
        "timestamp": time.time(),
        "request_id": request.state.request_id,
        "endpoint": "/health"
    })

    return {"status": "ok"}


@app.post("/pay")
async def pay(request: Request):
    fail = random.random() < 0.4

    if fail:
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


@app.post("/crash")
async def crash(request: Request):
    send_log({
        "service_name": SERVICE_NAME,
        "level": "ERROR",
        "message": "Service crashed intentionally",
        "timestamp": time.time(),
        "request_id": request.state.request_id,
        "endpoint": "/crash"
    })

    os._exit(1)
