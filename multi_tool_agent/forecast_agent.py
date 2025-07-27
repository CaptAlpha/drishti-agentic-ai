from google.adk.agents import Agent
import requests
def predict_crowd_density() -> dict:
    try:
        response = requests.get("https://backend-1013135954620.us-central1.run.app/forecast/predict")
        print(response)
        return response.json()

    except Exception as e:
        return f"Error fetching or refining summary: {e}"

predict_crowd = Agent(
    name="predict_crowd",
    model="gemini-2.0-flash",
    description="Forecasts future crowd density in various event zones using trained models based on historical video analysis.",
    instruction="""
        Use the tool to forecast crowd density levels in one or more zones for the next 15 minutes.
        
        The model returns numeric values (e.g., 100, 300, 600, 900), but do NOT display these numbers to the user.
        Instead, convert them into qualitative levels:
          - LOW for ~100
          - MEDIUM for ~300–600
          - HIGH for ~700–900
          - VERY HIGH if close to or above 1000 (if applicable)

        When a specific zone is requested, return its upcoming trend in levels only.
        If all zones are requested, give a zone-wise summary using these labels.

        Focus on clear, readable summaries like:
          - "Zone A is expected to stay HIGH for the next 15 minutes."
          - "Zone C will shift from MEDIUM to HIGH gradually."

        Never display the raw numeric predictions directly to the user.
    """,
    tools=[predict_crowd_density]
)