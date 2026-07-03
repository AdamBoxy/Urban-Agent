# System Architecture

The Urban Agent platform is designed around the **Agent-to-Agent (A2A)** interaction pattern, prioritizing security, isolation, and strict payload definitions.

## The Routing Flow
1.  **Ingestion:** The user submits a prompt to the Orchestrator.
2.  **Security Middleware (`before_model_callback`):**
    *   The prompt is intercepted.
    *   Regex patterns scrub sensitive PII (SSNs, Phone Numbers).
    *   Prompt injection signatures are checked. If malicious intent is detected, the request is hard-routed to a human supervisor via `request_agency_approval`, completely bypassing the LLM processing phase.
3.  **LLM Processing:** The Orchestrator determines which agency is best suited to handle the request based on the scrubbed payload.
4.  **Pre-Call Hook (`before_tool_callback`):**
    *   Before `route_to_subagent` executes, the system validates the payload. This acts as an emergency breakpoint for injecting secondary multi-factor auth (MFA) tokens if the target agency is highly classified.
5.  **IPC Simulation / Dispatch:**
    *   The orchestrator invokes the sub-agent.
6.  **Sub-Agent Processing:**
    *   The isolated sub-agent executes its specialized tool (e.g., `check_main_pressure`).
    *   It strictly formats its response as a JSON string (bypassing conversational text).
7.  **Response:** The raw JSON is bubbled back through the Orchestrator to the frontend, where it is used to hydrate Just-In-Time (JIT) UI components.

## Future Enhancements
*   **Socket Bridge:** Replace the direct Python imports in `route_to_subagent` with a true IPC or Model Context Protocol (MCP) bridge, allowing sub-agents to live in entirely separate docker containers or cloud instances.
*   **Authentication Service:** Integrate Google Cloud Secret Manager for dynamic API key injection at the `emergency_mcp_hook` layer.
