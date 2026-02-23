from fastapi import APIRouter
from backend.app.schemas.urban_event import UrbanEvent
from datetime import datetime

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

# Temporary in-memory store (next step will be Postgres)
EVENTS = []

@router.post("/")
def ingest_event(event: UrbanEvent):
    data = event.model_dump()
    if data["timestamp"] is None:
        data["timestamp"] = datetime.utcnow()
    EVENTS.append(data)
    return {"message": "Event received", "total_events": len(EVENTS)}

@router.get("/latest")
def latest_events(limit: int = 5):
    return {"latest": EVENTS[-limit:]}