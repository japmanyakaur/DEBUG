from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Log(BaseModel):
    service_name: str
    level: str
    message: str
    timestamp: float
    request_id: str
    endpoint: str

@app.post("/logs")
async def receive_log(log: Log):
    print("LOG RECEIVED:", log)
    return {"status": "ok"}
