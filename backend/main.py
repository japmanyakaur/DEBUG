from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from database import Base, engine, SessionLocal
from models import LogDB

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Incident table


class Incident(Base):
    __tablename__ = "incidents"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String)
    start_time = Column(Float)
    status = Column(String)

class Log(BaseModel):
    service_name: str
    level: str
    message: str
    timestamp: float
    request_id: str
    endpoint: str


@app.post("/logs")
async def receive_log(log: Log):
    db = SessionLocal()

    db_log = LogDB(**log.dict())
    db.add(db_log)
    db.commit()

    print("LOG SAVED TO DB")

    # 🚨 Incident detection
    if log.level == "ERROR":
        recent_errors = db.query(LogDB).filter(
            LogDB.service_name == log.service_name,
            LogDB.level == "ERROR",
            LogDB.timestamp >= log.timestamp - 60
        ).count()

        if recent_errors >= 3:
            incident = Incident(
                service_name=log.service_name,
                start_time=log.timestamp,
                status="ACTIVE"
            )
            db.add(incident)
            db.commit()
            print("🚨 INCIDENT CREATED")

    return {"status": "ok"}


@app.get("/logs")
def get_logs():
    db = SessionLocal()
    logs = db.query(LogDB).all()
    return logs
