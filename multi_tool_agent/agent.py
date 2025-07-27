import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.greeting_agent import greeting_agent
from multi_tool_agent.video_analysis_agent import video_analysis_agent
from multi_tool_agent.forecast_agent import predict_crowd  # 👈 NEW
from dotenv import load_dotenv
from multi_tool_agent.summary_agent import fetch_logs
load_dotenv()

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

weather_time_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)

root_agent = Agent(
    name="coordinator_agent",
    model="gemini-2.0-flash",
    description="Coordinates requests between greeting and log summary agents.",
    instruction="""
        Use `greeting_agent` to handle any kind of greeting, welcome messages, or general interaction with the user.
        
         Use `fetch_logs` when the user asks about:
        - The current status of one or more zones
        - A summary of recent events
        - What happened recently or is happening now
        - Incident summaries or zone-level updates
        These are based on logs from the past 1 hour.

        Use `predict_crowd` only when the user explicitly asks about:
        - Future predictions
        - What will happen next in a zone
        - Forecasts of crowd levels
        - Expected trends in upcoming minutes
        Respond with only crowd level labels (LOW, MEDIUM, HIGH) and do not return raw numbers.

        Ensure you interpret the user's intent carefully. If the query is about what's currently happening or just happened, prefer `fetch_logs`. If it's about what will happen soon or future crowd conditions, use `predict_crowd`.

        Route tasks only to the appropriate sub-agent and avoid answering directly unless none of them apply.
    """,
    sub_agents=[
        greeting_agent,
        # video_analysis_agent,
        # weather_time_agent,
        fetch_logs,
        predict_crowd
    ],
    # tools=[AgentTool(agent=fetch_logs)]
)
