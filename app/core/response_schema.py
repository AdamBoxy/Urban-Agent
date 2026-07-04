from enum import Enum
from typing import TypedDict, Optional

class AgentStatus(str, Enum):
    DONE = "DONE"
    HANDOFF = "HANDOFF"
    NEEDS_HUMAN = "NEEDS_HUMAN"
    ERROR = "ERROR"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"

class UsageMetrics(TypedDict):
    turns: int
    tool_calls: int
    estimated_tokens: int

class AgentResponse(TypedDict):
    status: AgentStatus
    confidence: float
    summary: str
    next_agent: Optional[str]
    reason: str
    usage: UsageMetrics
