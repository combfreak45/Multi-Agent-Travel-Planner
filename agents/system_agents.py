from google.adk import Agent
from config import model_name
from tools.system_tools import save_note, create_task, get_travel_summary

notes_agent = Agent(
    name="notes_agent",
    model=model_name,
    tools=[save_note],
    instruction="""
    Save the user's final travel itinerary as a note.
    Review the conversation history to capture the final plan.
    Use the save_note tool.
    """
)

task_agent = Agent(
    name="task_agent",
    model=model_name,
    tools=[create_task],
    instruction="""
    Create travel-related tasks based on the conversation history.
    Use the create_task tool.
    """
)

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
