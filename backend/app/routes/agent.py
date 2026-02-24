from fastapi import APIRouter
from backend.app.agent.reasoning_agent import ReasoningAgent
from backend.app.schemas.agent_models import AgentRequest, AgentResponse

router = APIRouter(prefix="/agent", tags=["Agent"])
agent = ReasoningAgent()

@router.post("/query", response_model=AgentResponse)
def agent_query(payload: AgentRequest):
    intent, plan, msg = agent.respond(payload.query)
    return AgentResponse(
        intent=intent,
        plan=plan,
        message=msg,
        notes="Tool execution is not connected yet. This endpoint validates intent + tool planning."
    )