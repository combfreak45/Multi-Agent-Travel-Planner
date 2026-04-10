import os
from google.adk.agents import Agent
from tools.get_travel_summary import get_travel_summary
from config import model_name



response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Formats final travel response",
    tools=[get_travel_summary],
    instruction="""
    You are a travel response formatter.
    Call the get_travel_summary tool to retrieve all collected travel data.
    Then present a clean, user-friendly travel plan.
    Suggest the best transport option based on price and timing.
    """
)