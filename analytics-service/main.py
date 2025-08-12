from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import datetime
import requests
from zoneinfo import ZoneInfo
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Allow requests from frontend origin
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ClickHouse service endpoint (inside Kubernetes)
CLICKHOUSE_URL = "http://clickhouse-svc.default.svc.cluster.local:8123"

@app.get("/")
def root():
    return {"message": "Welcome to the Analytics Service"}

# POST /track - store event in ClickHouse
@app.post("/track")
async def track_event(request: Request):
    data = await request.json()
    event_type = data.get("event_type", "unknown")
    timestamp = datetime.datetime.now(ZoneInfo("Asia/Colombo")).strftime('%Y-%m-%d %H:%M:%S')

    # Compose the INSERT query in JSONEachRow format
    query = f"""INSERT INTO analytics.events FORMAT JSONEachRow
{{"event_type": "{event_type}", "timestamp": "{timestamp}"}}"""

    try:
        response = requests.post(CLICKHOUSE_URL, data=query)
        return {"status": response.status_code, "event": event_type}
    except Exception as e:
        print("ClickHouse error:", e)
        return {"status": 500, "error": str(e)}

# GET /events - fetch all tracked events
@app.get("/events")
def get_events():
    try:
        query = "SELECT * FROM analytics.events ORDER BY timestamp DESC FORMAT JSON"
        response = requests.post(CLICKHOUSE_URL, data=query)
        return response.json()
    except Exception as e:
        print("ClickHouse fetch error:", e)
        return {"status": 500, "error": str(e)}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Enable Prometheus metrics to /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
