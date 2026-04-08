from google.adk import Agent
from google.adk.agents import SequentialAgent
from config import model_name
from agents import (
    flight_agent,
    train_agent,
    bus_agent,
    notes_agent,
    task_agent,
    response_formatter,
    calendar_agent
)

# =========================================================
# 🔹 TRAVEL PLANNER (MULTI-AGENT COORDINATOR)
# =========================================================

travel_planner = SequentialAgent(
    name="travel_planner_workflow",
    sub_agents=[
        flight_agent,
        train_agent,
        bus_agent
    ]
)

# =========================================================
# 🔹 MAIN WORKFLOW (CHAIN)
# =========================================================

travel_workflow = SequentialAgent(
    name="travel_workflow",
    sub_agents=[
        travel_planner,     # Step 1: Gather options
        response_formatter,  # Step 2: Format output
        calendar_agent
    ]
)

# =========================================================
# 🔹 ROOT AGENT (ENTRY POINT)
# =========================================================

root_agent = Agent(
    name="travel_assistant",
    model=model_name,
    description="Main entry point for travel planning assistant",
    instruction="""
    You are a helpful travel planning assistant.
    - Greet the user warmly.
    - Ask for travel details if missing: source city, destination city, and travel date.
    - Once you have all three details, transfer control to the travel_workflow.
    - After options are shown, wait for the user to confirm their preferred transport.
    - Once confirmed, the calendar_agent will book it on Google Calendar automatically.
    """,
    sub_agents=[travel_workflow, notes_agent, task_agent]
)

if __name__ == "__main__":
    pass  # Replace with run loop if testing natively