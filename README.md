# Urban Agent: Multi-Agent Municipal Orchestrator

Urban Agent is a modern, security-first multi-agent system designed to act as the central intelligence layer for municipal infrastructure. Built on the [Google Agent Development Kit (ADK)](https://adk.dev/) and powered by `gemini-2.5-flash`, Urban Agent securely routes civic inquiries to isolated domain experts (sub-agents) while enforcing strict privacy and security guardrails.

## 🚀 Key Features

*   **Intelligent Orchestration:** A central Root Agent that refuses to answer domain-specific queries directly, instead acting as an intelligent router and security gateway.
*   **Isolated Domain Sub-Agents:**
    *   **Family Services Agent:** Securely checks case statuses and handles sensitive social service data.
    *   **Water Utility Agent:** Interfaces with municipal telemetry to report on infrastructure metrics (like water pressure).
*   **Security-First Middleware:**
    *   **Prompt Injection Defense:** Intercepts LLM calls before execution to detect and neutralize malicious instructions.
    *   **Data Privacy (PII Scrubbing):** Automatically strips SSNs, phone numbers, and other sensitive PII from user inputs.
    *   **Emergency Hooks:** Pre-call hooks on critical tool executions for secondary logging and authentication checks.
    *   **Stateful Guardrails:** A dynamic state tracker (`OrchestratorGuard`) monitors execution metrics (agent hops, token budget, failed loops) and triggers circuit breakers if limits are breached.
    *   **Per-Agent Limits:** Isolated Sub-Agents are wrapped with `AgentGuard` trackers, instantly terminating runaways if they breach token budgets, tool call limits, or confidence thresholds.
    *   **Tool Execution Constraints:** The `ToolGuard` middleware wraps tool execution, enforcing strict timeouts (5s), retry-limit circuit breakers, and agency-specific tool allowlists.
*   **JIT UI Hydration:** Sub-agents return strict JSON payloads, allowing modern frontends to seamlessly hydrate cached UI templates without parsing raw conversational text.

*   **PLEASE NOTE: THE A2UI/JIT FEATURES ARE STILL IN PROGRESS: WILL BE INCLUDED LATER AS I DEBUG**

## 📁 Repository Structure

*   `app/agent.py`: The core orchestrator, security hooks, and routing logic.
*   `app/family_services_agent.py`: The Family Services domain sub-agent.
*   `app/water_utility_agent.py`: The Water Utility domain sub-agent.
*   `SETUP_GUIDE.md`: Step-by-step instructions for getting the system running locally.
*   `AGENT.md`: A deep dive into the specific agent architectures, instructions, and schemas.
*   `SYSTEM_ARCHITECTURE.md`: A detailed architectural write-up of the IPC bridging and security flows.

## 🛠️ Quick Start

Check out the [Setup Guide](SETUP_GUIDE.md) to get started with local authentication, or jump right into the playground:

```bash
# If not already setup
uvx google-agents-cli setup

# Install dependencies and run
cd orchestrator-agent
agents-cli install
agents-cli playground
```
