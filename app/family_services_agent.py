from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
import json

def verify_case_status(case_id: str) -> str:
    """Verifies the case status for a given family services case ID. Returns a strict JSON string."""
    response = {
        "case_id": case_id,
        "status": "ACTIVE",
        "last_update": "2026-06-25",
        "assigned_worker": "Jane Doe"
    }
    return json.dumps(response)

family_services_agent = Agent(
    name="family_services_agent",
    model=Gemini(model="gemini-2.5-flash"),
    description="Domain expert for family services data.",
    instruction="You handle family services inquiries. Use the verify_case_status tool.",
    tools=[verify_case_status]
)
