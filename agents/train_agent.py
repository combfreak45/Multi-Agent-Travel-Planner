from google.adk import Agent
from config import model_name
from tools.train_tools import search_trains

train_agent = Agent(
    name="train_agent",
    model=model_name,
    tools=[search_trains],
    instruction="""
    You are a train schedule specialist.
    Review the conversation history for travel details.
    Fetch train options and return best schedules using the search_trains tool.
    """,
    output_key="train_data"
)
