from google.adk import Agent
from config import model_name
from tools.system_tools import save_note, create_task

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
