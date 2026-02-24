from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class AgentRequest(BaseModel):
    query: str

class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class AgentResponse(BaseModel):
    intent: str
    plan: List[ToolCall]
    message: str
    notes: Optional[str] = None