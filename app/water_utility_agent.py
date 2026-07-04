from google.adk.agents import Agent
from google.adk.models import Gemini
import json

def check_main_pressure(zone_id: str) -> str:
    """Checks the water main pressure for a given zone ID. Returns a strict JSON string."""
    response = {
        "zone_id": zone_id,
        "pressure_psi": 65.5,
        "status": "NORMAL",
        "last_reading": "2026-06-25T14:30:00Z"
    }
    return json.dumps(response)

water_utility_agent = Agent(
    name="water_utility_agent",
    model=Gemini(model="gemini-2.5-flash"),
    description="Domain expert for water utility telemetry.",
    instruction="You handle water utility inquiries. Use the check_main_pressure tool.",
    tools=[check_main_pressure]
)
