from typing import Dict, Any, Optional
from .agent_state import OrchestratorRunState
from .limits import OrchestratorLimits
from .exit_conditions import evaluate_orchestrator_exit

class OrchestratorGuard:
    def __init__(self, limits: Optional[OrchestratorLimits] = None):
        self.limits = limits if limits is not None else OrchestratorLimits()
        self.state = OrchestratorRunState()

    def verify_next_step(self, next_agent_id: str, estimated_cost: int = 0, last_hop_successful: bool = True) -> Optional[Dict[str, Any]]:
        self.state.log_hop(next_agent=next_agent_id, token_cost=estimated_cost, success=last_hop_successful)
        violation = evaluate_orchestrator_exit(self.state, self.limits)
        if violation:
            status = "ERROR" if "SECURITY" in violation or "CIRCUIT" in violation else "BUDGET_EXCEEDED"
            return {
                "status": status,
                "confidence": 0.0,
                "summary": "Execution terminated by Orchestrator Guard Rails.",
                "next_agent": None,
                "reason": violation,
                "usage": {
                    "hops": self.state.agent_hops,
                    "total_tokens": self.state.total_tokens
                }
            }
        return None
