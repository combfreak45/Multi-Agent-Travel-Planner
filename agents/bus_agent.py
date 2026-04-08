from google.adk import Agent
from config import model_name
from tools.bus_tools import search_buses

bus_agent = Agent(
    name="bus_agent",
    model=model_name,
    tools=[search_buses],
    instruction="""
    You are a bus route specialist.
    Review the conversation history for travel details.
    Fetch bus routes and return best options using the search_buses tool.
    """,
    output_key="bus_data"
)
