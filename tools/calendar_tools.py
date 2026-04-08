import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.adk.tools.tool_context import ToolContext

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
            "event_link": event.get('htmlLink', ''),
            "event_summary": summary or f"{transport_mode.capitalize()} from {source} to {destination}"
        }
    except HttpError as error:
        print(f"An error occurred: {error}")
        return {"status": "error", "message": str(error)}

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
    """Wrapper that calls book_travel_calendar and saves result to agent state."""
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
            "link": result.get("event_link", ""),
            "summary": result.get("event_summary", ""),
            "date": travel_date,
            "departure": departure_time
        }
 
    return result
