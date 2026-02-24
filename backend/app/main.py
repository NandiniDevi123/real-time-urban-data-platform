from fastapi import FastAPI
from backend.app.routes.ingest import router as ingest_router

from backend.app.routes.agent import router as agent_router

from backend.app.routes.health import router as health_router

app = FastAPI(title="Real-Time Urban Data Integration & Analytics Platform")

app.include_router(health_router)

app.include_router(ingest_router)

app.include_router(agent_router)
