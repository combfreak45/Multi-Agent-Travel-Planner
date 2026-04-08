from google.adk import Agent
from config import model_name
from tools.train_tools import search_trains

train_agent = Agent(
    name="train_agent",
    model=model_name,
    tools=[search_trains],
    instruction="""
    You are a train schedule specialist for Indian Railways.
    Review the conversation history for travel details (source city, destination city, travel date).
    
    CRITICAL INSTRUCTIONS BEFORE APPLYING TOOLS:
    1. Determine the Indian Railway primary station codes for the source and destination cities. For example, New Delhi is 'NDLS', Mumbai Central is 'MMCT', Bangalore is 'SBC', etc.
    2. Format the travel date into exactly 'DD-MM-YYYY' format.
    
    Use the search_trains tool with these station codes and formatted date to fetch the train options.
    If no trains are found or the list is empty, advise the user accordingly.
    """,
    output_key="train_data"
)
