import time
from fastapi import FastAPI
from pydantic import BaseModel
from database import engine, SessionLocal
from models import Log, Incident
from database import Base

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# -----------------------------
# Pydantic model for input
# -----------------------------
class LogInput(BaseModel):
    service_name: str
    level: str
    message: str
    timestamp: float
    request_id: str
    endpoint: str


# -----------------------------
# Receive logs
# -----------------------------
@app.post("/logs")
def receive_log(log: LogInput):
    db = SessionLocal()

    db_log = Log(**log.dict())
    db.add(db_log)
    db.commit()

    print(f"📥 Log received: {log.level} - {log.message}")

    # -----------------------------
    # INCIDENT DETECTION LOGIC
    # -----------------------------
    if log.level == "ERROR":
        recent_errors = db.query(Log).filter(
            Log.service_name == log.service_name,
            Log.level == "ERROR",
            Log.timestamp >= log.timestamp - 60
        ).count()

        if recent_errors >= 3:
            existing_incident = db.query(Incident).filter(
                Incident.service_name == log.service_name,
                Incident.status == "ACTIVE"
            ).first()

            if not existing_incident:
                incident = Incident(
                    service_name=log.service_name,
                    start_time=log.timestamp,
                    status="ACTIVE"
                )
                db.add(incident)
                db.commit()
                print("🚨 INCIDENT CREATED")

    db.close()
    return {"status": "ok"}


# -----------------------------
# Get incidents
# -----------------------------
@app.get("/incidents")
def get_incidents():
    db = SessionLocal()
    incidents = db.query(Incident).all()
    db.close()
    return incidents


# -----------------------------
# Get logs (optionally filtered)
# -----------------------------
@app.get("/logs")
def get_logs(service_name: str = None):
    db = SessionLocal()
    query = db.query(Log)

    if service_name:
        query = query.filter(Log.service_name == service_name)

    logs = query.all()
    db.close()
    return logs
