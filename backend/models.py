from sqlalchemy import Column, Integer, String, Float
from database import Base

class LogDB(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String)
    level = Column(String)
    message = Column(String)
    timestamp = Column(Float)
    request_id = Column(String)
    endpoint = Column(String)
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String)
    start_time = Column(Float)
    status = Column(String)  # ACTIVE / RESOLVED
