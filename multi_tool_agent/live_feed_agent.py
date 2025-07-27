from google.adk.agents import Agent
from google.adk.tools import LongRunningFunctionTool
import requests
def fetch_recent_logs() -> dict:
    try:
        response = requests.get("https://backend-1013135954620.us-central1.run.app/")
        response.raise_for_status()
        summary_text = response.text.strip()
        return summary_text

    except Exception as e:
        return f"Error fetching or refining summary: {e}"

fetch_logs = Agent(
    name="fetch_logs",
    model="gemini-2.0-flash",
    description="This agent is used to generate summary of events captured in different zones at the public event",
     instruction="""
        Use the provided tool to retrieve recent event logs from the past hour.
        If the user requests a summary of all zones, generate a human-readable summary of event logs in paragraph along with meaningful insights like shifts in crowd density over a time period,etc
        If the user asks for information about a specific zone, provide only the summary or status for that zone.
        If the user asks for the latest status at a particular zone, extract the most recent relevant log from that zone and describe the current situation.
        Always rely on the tool output for accurate and up-to-date information.
    """,
    tools=[fetch_recent_logs]
)