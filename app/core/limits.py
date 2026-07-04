from dataclasses import dataclass

@dataclass(frozen=True)
class OrchestratorLimits:
    max_agent_hops: int = 5
    max_delegation_depth: int = 3
    max_global_tokens: int = 25000
    max_allowed_failures: int = 2
    allow_recursive_handoff: bool = False
