from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class OrchestratorRunState:
    agent_hops: int = 0
    delegation_depth: int = 0
    total_tokens: int = 0
    failed_agents_count: int = 0
    current_agent: str = "orchestrator"
    visited_agents: List[str] = field(default_factory=list)
    history_log: List[Dict[str, Any]] = field(default_factory=list)

    def log_hop(self, next_agent: str, token_cost: int = 0, success: bool = True) -> None:
        self.agent_hops += 1
        self.total_tokens += token_cost
        
        if not success:
            self.failed_agents_count += 1
            
        if self.current_agent != "orchestrator":
            self.visited_agents.append(self.current_agent)
            
        self.current_agent = next_agent
