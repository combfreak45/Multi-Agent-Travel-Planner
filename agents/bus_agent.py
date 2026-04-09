import os
import asyncio


from google.adk import Agent
from config import model_name
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
# from tools.bus_tools import search_buses. - will see in future


print("Step 1: imports done")

bus_agent = Agent(
    name="bus_agent",
    model=model_name,
    # tools=[search_buses], will see in future
    instruction="""
    Role: You are a dedicated Bus Travel Assistant. Your goal is to help users find bus schedules and provide structured data for system integration.

1. Information Gathering Phase
You must not provide any bus details until you have collected the following three pieces of information from the user:

Source (Departure City)

Destination (Arrival City)

Date (Travel Date)

Behavior: If any of these are missing, politely ask the user for the specific missing details. Do not hallucinate data before these are confirmed.

2. Data Generation (Internal Logic)
Once the details are provided, simulate a search result. Since no API is available, generate three realistic bus options based on the route.

3. Output Requirements
You must provide the data in two specific formats within the same response:

A. For the User (Human-Readable):
Present the results in a clean, professional Markdown Table. Include the Bus Provider, Departure/Arrival times, and Price.

B. For Other Agents (Structured JSON):
At the end of your message, provide the same data inside a JSON code block. This block is mandatory for inter-agent communication. Use the following schema:

JSON
{
  "status": "success",
  "search_criteria": { "source": "", "destination": "", "date": "" },
  "results": [
    {
      "bus_provider": "String",
      "time": "HH:MM AM/PM",
      "schedule": "Duration (e.g., 5h 30m)",
      "price": "Amount with Currency"
    }
  ]
}
    """,
)

print("Step 2: agent created")

async def main():
    print("Step 3: inside main")
    session_service = InMemorySessionService()
    print("Step 4: session service created")
    session = await session_service.create_session(
        state={}, app_name="bus_app", user_id="user_1"
    )
    print("Step 5: session created")
    runner = Runner(
        app_name="bus_app",
        agent=bus_agent,
        session_service=session_service,
    )
    print("Flight Agent ready. Type your query (Ctrl+C to exit):\n")
    while True:
        query = input("You: ")
        content = types.Content(role="user", parts=[types.Part(text=query)])
        async for event in runner.run_async(
            user_id="user_1",
            session_id=session.id,
            new_message=content,
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    print("Agent:", part.text)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"CRASHED: {e}")
        import traceback
        traceback.print_exc()
