from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal, engine
from models import Base, Log
from incident_brain import process_log
from models import Incident

from datetime import timedelta




Base.metadata.create_all(bind=engine)

app = FastAPI(title="LogLite Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.start_time.desc()).all()
@app.post("/logs")
def ingest_logs(log: dict, db: Session = Depends(get_db)):
    log_entry = Log(
        service_name=log["service_name"],
        level=log["level"],
        message=log["message"],
        timestamp=datetime.fromisoformat(log["timestamp"]),
        request_id=log["request_id"],
        endpoint=log["endpoint"]
    )

    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    process_log(db, log_entry)

    return {"status": "log stored"}
@app.get("/incidents/{incident_id}/logs")
def incident_logs(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        return []

    start = incident.start_time - timedelta(seconds=30)
    end = incident.start_time + timedelta(seconds=60)

    logs = db.query(Log).filter(
        Log.service_name == incident.service_name,
        Log.timestamp >= start,
        Log.timestamp <= end,
        Log.level.in_(["ERROR", "WARN"])
    ).order_by(Log.timestamp.asc()).all()

    return logs