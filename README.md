# DEBUG : _Automated Incident Detection & Log Correlation_


## Overview

Debug Platform automatically detects when a service becomes slow or goes down and instantly surfaces the most relevant logs responsible for the issue.

Instead of engineers manually searching through logs during failures, the system **detects incidents and brings the right logs automatically**.

---

## Core Idea 

 When a service fails or slows down, the system detects the incident and automatically shows the logs that likely caused it.

---

## Why This Exists

In real systems:
- Services fail or slow down
- Engineers manually search logs to find the cause
- Time is wasted during incidents

Debug Platform removes manual log searching by **linking monitoring and logging together**.

---

##  Architecture

The system consists of three parts:

1. **Demo Service** – A deliberately unstable backend used for testing  
2. **Backend** – Log collection, health monitoring, and incident analysis  
3. **Frontend** – Dashboard showing services, incidents, and relevant logs  

---


## Components

### Demo Service
- Simulates latency, errors, and crashes
- Emits structured logs with `request_id`
- Used only for demonstration and testing

### Logs
- Centralized log ingestion
- Stores structured logs from services
- Used during incidents to find relevant errors

### Monitoring
- Periodically checks service health
- Detects SLOW or DOWN services
- Automatically creates incidents

### Incident Brain
- Triggered when an incident occurs
- Auto-filters logs by:
  - service
  - time window
  - ERROR / WARN level
- Groups logs by `request_id`
- Highlights probable root cause

### Frontend Dashboard
- Shows service status (UP / SLOW / DOWN)
- Lists incidents
- Displays auto-filtered logs per incident

---

## Demo Flow

1. Service is healthy  
2. Trigger failures or crash  
3. Incident is detected automatically  
4. Relevant logs appear instantly  


---

## Tech Stack

- **Backend:** FastAPI  
- **Frontend:** React  
- **Database:** PostgreSQL (Supabase)  
- **Monitoring:** Poll-based health checks  
- **Logging:** Structured JSON logs  

---





