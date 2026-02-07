from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    level = Column(String)                     # INFO / ERROR
    message = Column(Text)
    timestamp = Column(DateTime)
    request_id = Column(String, index=True)
    endpoint = Column(String)


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    status = Column(String, default="ACTIVE")  # ACTIVE | RESOLVED
    incident_type = Column(String)             # DOWN (SLOW later)
    start_time = Column(DateTime, default=datetime.utcnow)
