from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Incident, Log

ERROR_THRESHOLD = 3
TIME_WINDOW_SECONDS = 30

def process_log(db: Session, log: Log):
    if log.level != "ERROR":
        return

    now = datetime.utcnow()
    window_start = now - timedelta(seconds=TIME_WINDOW_SECONDS)

    recent_errors = db.query(Log).filter(
        Log.service_name == log.service_name,
        Log.level == "ERROR",
        Log.timestamp >= window_start
    ).count()

    if recent_errors < ERROR_THRESHOLD:
        return

    active_incident = db.query(Incident).filter(
        Incident.service_name == log.service_name,
        Incident.status == "ACTIVE"
    ).first()

    if active_incident:
        return

    incident = Incident(
        service_name=log.service_name,
        incident_type="DOWN",
        start_time=now
    )

    db.add(incident)
    db.commit()
