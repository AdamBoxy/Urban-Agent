# Agent Profiles

This document details the responsibilities, toolsets, and constraints of the agents in the Urban Agent system.

## 1. Orchestrator Agent (`agent.py`)
*   **Model:** `gemini-2.5-flash`
*   **Role:** The central routing hub and security gateway.
*   **Core Instruction:** Never answer domain-specific questions directly. Route requests, log transactions, and request human approval when security flags are tripped.
*   **Tools:**
    *   `route_to_subagent`: Dispatches the payload to the appropriate agency.
    *   `log_audit_trail`: Records the transaction for compliance.
    *   `request_agency_approval`: A `LongRunningFunctionTool` that halts execution to request human authorization.
*   **Middleware:**
    *   `sanitize_and_defend_hook`: Scrubs PII and detects prompt injection.
    *   `emergency_mcp_hook`: Validates payloads before critical tool dispatch.

## 2. Family Services Agent (`family_services_agent.py`)
*   **Model:** `gemini-2.5-flash`
*   **Role:** Domain expert for social services and family welfare.
*   **Core Instruction:** Interact with databases and return ONLY structured data. No routing or auth.
*   **Tools:**
    *   `verify_case_status(case_id)`: Returns a strict JSON payload mapping `case_id`, `status`, `assigned_worker`, `next_visit_scheduled`, and `action_required`.

## 3. Water Utility Agent (`water_utility_agent.py`)
*   **Model:** `gemini-2.5-flash`
*   **Role:** Domain expert handling water infrastructure telemetry.
*   **Core Instruction:** Monitor and report on water metrics. Return ONLY structured data.
*   **Tools:**
    *   `check_main_pressure(zone_id)`: Returns a strict JSON payload mapping `zone_id`, `current_psi`, `optimal_range_psi`, `status`, and `active_alerts`.
