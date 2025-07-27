from google.adk.agents import Agent

def greet(name: str) -> dict:
    """Greets the user by name."""
    return {"status": "success", "report": f"Hello, {name}!"}

greeting_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description="Agent to greet users.",
    instruction="Greet the user if they say hellog or provide their name. ",
    tools=[greet]
)