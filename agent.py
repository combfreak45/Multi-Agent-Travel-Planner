import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent

from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def book_travel_calendar(
    summary: str,
    source: str,
    destination: str,
    travel_date: str,       # Format: YYYY-MM-DD
    departure_time: str,    # Format: HH:MM (24hr), e.g. "07:00"
    transport_mode: str,    # e.g. "flight", "train", "bus"
    attendee_email: str = ""
) -> dict:
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
        

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        tz = "Asia/Kolkata"
        start_str = f"{travel_date}T{departure_time}:00+05:30"
        start_dt = datetime.datetime.strptime(f"{travel_date} {departure_time}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + datetime.timedelta(hours=2)
        end_str = f"{travel_date}T{end_dt.strftime('%H:%M')}:00+05:30"
       
        description = (
            f"Travel Plan booked by AI Travel Assistant\n"
            f"Mode: {transport_mode.upper()}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Date: {travel_date}\n"
            f"Departure: {departure_time}")
        event = {
            "summary": summary or f"{transport_mode.capitalize()} from {source} to {destination}",
            "location": f"{source} to {destination}",
            "description": description,
            "colorId": 6,
            "start": {"dateTime": start_str, "timeZone": tz},
            "end": {"dateTime": end_str, "timeZone": tz}
       }
        event = service.events().insert(calendarId="primary", body=event).execute()
        return {
        "status": "success",
        "message": "Calendar event created successfully!",
        "event_link": link,
        "event_summary": summary or f"{transport_mode.capitalize()} from {source} to {destination}"
        }
    #    now = dt.datetime.now().isoformat() + "Z"
    #    events_result = service.events().list(calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime").execute()
    #    events = events_result.get("items", [])
    #    if not events:
    #        print("No upcoming events found.")
    #        return
    #    for event in events:
    #         start = event["start"].get("dateTime", event["start"].get("date"))
    #         print(start, event['summary'] )
    except HttpError as error:
        print(f"An error occurred: {error}")












# --- Setup Logging and Environment ---

load_dotenv()
cloud_logging_client = google.cloud.logging.Client()

model_name = os.getenv("MODEL")

# =========================================================
# 🔹 MOCK / MCP TOOLS (Replace with MCP calls later)
# =========================================================

def search_flights(source: str, destination: str, date: str) -> dict:
    return {
        "flights": [
            {"time": "7:00 AM", "price": 4500},
            {"time": "3:00 PM", "price": 5200}
        ]
    }

def search_trains(source: str, destination: str, date: str) -> dict:
    return {
        "trains": [
            {"name": "Express", "time": "6:00 AM"},
            {"name": "Superfast", "time": "9:00 PM"}
        ]
    }

def search_buses(source: str, destination: str, date: str) -> dict:
    return {
        "buses": [
            {"type": "AC Sleeper", "time": "10:00 PM"},
            {"type": "Seater", "time": "6:00 AM"}
        ]
    }

def save_note(tool_context: ToolContext, note: str) -> dict:
    tool_context.state["NOTE"] = note
    return {"status": "saved"}

def create_task(tool_context: ToolContext, task: str) -> dict:
    tool_context.state["TASK"] = task
    return {"status": "created"}

def get_weather(city: str) -> dict:
    return {"weather": "Sunny", "temp": "28C"}


def book_calendar_tool(
    tool_context: ToolContext,
    summary: str,
    source: str,
    destination: str,
    travel_date: str,
    departure_time: str,
    transport_mode: str,
    attendee_email: str = ""
) -> dict:
    """Wrapper that calls my_calendar.py and saves result to agent state."""
    result = book_travel_calendar(
        summary=summary,
        source=source,
        destination=destination,
        travel_date=travel_date,
        departure_time=departure_time,
        transport_mode=transport_mode,
        attendee_email=attendee_email
    )
 
    # Save booking result to state so other agents can reference it
    if result["status"] == "success":
        tool_context.state["CALENDAR_EVENT"] = {
            "status": "booked",
            "link": result["event_link"],
            "summary": result["event_summary"],
            "date": travel_date,
            "departure": departure_time
        }
 
    return result


# =========================================================
# 🔹 TRANSPORT AGENTS
# =========================================================

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

# =========================================================
# 🔹 INFO AGENT
# =========================================================

info_agent = Agent(
    name="info_agent",
    model=model_name,
    tools=[get_weather],
    instruction="""
    You are a local information specialist.
    Review the conversation history to find the destination city.
    Fetch weather or general travel info using the get_weather tool.
    """,
    output_key="info_data"
)

# =========================================================
# 🔹 NOTES + TASK AGENTS
# =========================================================

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

# =========================================================
# 🔹 TRAVEL PLANNER (MULTI-AGENT COORDINATOR)
# =========================================================

travel_planner = SequentialAgent(
    name="travel_planner_workflow",
    sub_agents=[
        flight_agent,
        train_agent,
        bus_agent,
        info_agent
    ]
)

# =========================================================
# 🔹 RESPONSE FORMATTER
# =========================================================

def get_travel_summary(tool_context: ToolContext) -> dict:
    return {
        "flights": tool_context.state.get("flight_data", "No data"),
        "trains": tool_context.state.get("train_data", "No data"),
        "buses": tool_context.state.get("bus_data", "No data"),
        "info": tool_context.state.get("info_data", "No data"),
    }

response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Formats final travel response",
    tools=[get_travel_summary],  # ✅ use tool instead of {} placeholders
    instruction="""
    You are a travel response formatter.
    Call the get_travel_summary tool to retrieve all collected travel data.
    Then present a clean, user-friendly travel plan.
    Suggest the best transport option based on price and timing.
    """
)

calendar_agent = Agent(
    name="calendar_agent",
    model=model_name,
    description="Books confirmed travel on Google Calendar",
    tools=[book_calendar_tool],
    instruction="""
    You are a calendar booking specialist.
    
    Only act when the user has CONFIRMED their transport choice (e.g. "book the train", 
    "I'll take the 7AM flight", "go with the bus", etc.).
    
    Extract from the conversation:
    - source (departure city)
    - destination (arrival city)  
    - travel_date (YYYY-MM-DD format)
    - departure_time (HH:MM in 24hr format based on chosen option)
    - transport_mode (flight / train / bus)
    - summary (short event title like "Train: Mumbai to Pune")
    
    Then call book_travel_calendar with these details.
    
    After booking, confirm to the user:
    "✅ Your [transport] from [source] to [destination] on [date] at [time] has been added to your Google Calendar!"
    And share the event link.
    
    If the user hasn't confirmed a choice yet, do NOT book anything. 
    Just say "Please confirm your preferred transport option and I'll book it right away!"
    """
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
    sub_agents=[travel_workflow,notes_agent,task_agent]
)