from .limits import OrchestratorLimits
from .agent_state import OrchestratorRunState

def evaluate_orchestrator_exit(state: OrchestratorRunState, limits: OrchestratorLimits) -> str | None:
    if state.agent_hops >= limits.max_agent_hops:
        return "ORCHESTRATOR_ERROR: Max agent hops reached across infrastructure grid."
    if state.total_tokens >= limits.max_global_tokens:
        return "ORCHESTRATOR_ERROR: Global token budget exceeded."
    if state.failed_agents_count >= limits.max_allowed_failures:
        return "ORCHESTRATOR_ERROR: Max allowed sub-agent failures exceeded."
    if state.current_agent in state.visited_agents and not limits.allow_recursive_handoff:
        return "ORCHESTRATOR_ERROR: Recursive routing loop detected. Circuit breaker triggered."
    return None
