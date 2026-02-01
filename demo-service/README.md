# Demo Service

This is a deliberately unstable backend service used to
demonstrate the Debug Platform.

It simulates real production behavior such as:
- health checks
- latency spikes
- business logic failures
- complete service crashes
- structured log emission with request_id

This service is NOT part of the core platform.
It exists only to be monitored, broken, and debugged.
## Endpoints

GET /health
- Used by PingWatch
- Sometimes responds slowly
- Always returns 200 OK

POST /pay
- Simulates a payment operation
- Fails randomly (~40%)
- Emits ERROR logs on failure

POST /crash
- Immediately terminates the process
- Used to simulate service outages
## Run

pip install -r requirements.txt <br>
uvicorn app:app --port 4000 --reload

## Demo Flow

1. Call /health → service is healthy
2. Call /pay multiple times → errors appear
3. Call /crash → service goes DOWN
4. Debug Platform auto-detects incident and shows logs
