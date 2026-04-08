from google.adk import Agent
from config import model_name
from tools.flight_tools import search_flights

flight_agent = Agent(
    name="flight_agent",
    model=model_name,
    instruction="""
    You are a flight search specialist.
    Review the conversation history to find the user's desired source, destination, and travel date.
    Use the search_flights tool to find flight options.
    """,
    tools=[search_flights],
    output_key="flight_data"
)
