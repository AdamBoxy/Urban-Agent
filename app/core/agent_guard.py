from dataclasses import dataclass
from typing import Optional
from .response_schema import AgentStatus, AgentResponse, UsageMetrics

@dataclass(frozen=True)
class AgentLimits:
    max_turns: int = 4
    max_tool_calls: int = 6
    max_tokens: int = 2500
    min_confidence: float = 0.65

@dataclass
class AgentState:
    turns: int = 0
    tool_calls: int = 0
    estimated_tokens: int = 0
    current_confidence: float = 1.0

class AgentGuard:
    def __init__(self, limits: Optional[AgentLimits] = None):
        self.limits = limits if limits is not None else AgentLimits()
        self.state = AgentState()
        
    def log_turn(self, tool_calls_in_turn: int = 0, estimated_tokens_in_turn: int = 0, confidence: float = 1.0) -> None:
        self.state.turns += 1
        self.state.tool_calls += tool_calls_in_turn
        self.state.estimated_tokens += estimated_tokens_in_turn
        self.state.current_confidence = confidence

    def should_exit(self) -> Optional[AgentResponse]:
        usage: UsageMetrics = {
            "turns": self.state.turns,
            "tool_calls": self.state.tool_calls,
            "estimated_tokens": self.state.estimated_tokens
        }
        
        if self.state.turns >= self.limits.max_turns:
            return AgentResponse(status=AgentStatus.BUDGET_EXCEEDED, confidence=self.state.current_confidence, summary="Agent terminated due to reaching max turns limit.", next_agent=None, reason="MAX_TURNS_EXCEEDED", usage=usage)
        if self.state.tool_calls >= self.limits.max_tool_calls:
            return AgentResponse(status=AgentStatus.BUDGET_EXCEEDED, confidence=self.state.current_confidence, summary="Agent terminated due to reaching max tool calls limit.", next_agent=None, reason="MAX_TOOL_CALLS_EXCEEDED", usage=usage)
        if self.state.estimated_tokens >= self.limits.max_tokens:
            return AgentResponse(status=AgentStatus.BUDGET_EXCEEDED, confidence=self.state.current_confidence, summary="Agent terminated due to reaching max tokens limit.", next_agent=None, reason="MAX_TOKENS_EXCEEDED", usage=usage)
        if self.state.current_confidence < self.limits.min_confidence:
            return AgentResponse(status=AgentStatus.NEEDS_HUMAN, confidence=self.state.current_confidence, summary="Agent confidence dropped below acceptable threshold. Human intervention required.", next_agent=None, reason="LOW_CONFIDENCE", usage=usage)
        return None
