import os
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from tools.flight_tools import search_flights


flight_agent = Agent(
    model="gemini-2.5-pro",
    name="flight_agent",
    description="Helps search for flights.",
    output_key="flight_data",
    instruction="""
    You help users find flights. Use the search_flights tool.

    CRITICAL: If the source or destination city doesn't have a commercial airport:
    1. Identify the nearest major city with an airport (within 200km if possible)
    2. Use that airport code to search for flights
    3. In your response, clearly mention: "Showing flights from [Nearby City] ([CODE]) as [Original City] doesn't have an airport"

    Examples:
    - Shimla → Use Chandigarh (IXC)
    - Manali → Use Kullu (KUU) or Chandigarh (IXC)
    - Mysore → Use Bangalore (BLR)

    Do NOT ask the user for clarification. Make the best decision and explain it.
    If no nearby airport exists within reasonable distance, return: "No flights available - [City] and nearby areas don't have commercial airports."
    """,
    tools=[search_flights],
)


# async def main():
#     session_service = InMemorySessionService()
#     session = await session_service.create_session(
#         state={}, app_name="flight_app", user_id="user_1"
#     )
#     runner = Runner(
#         app_name="flight_app",
#         agent=flight_agent,
#         session_service=session_service,
#     )
#     while True:
#         query = input("You: ")
#         content = types.Content(role="user", parts=[types.Part(text=query)])
#         async for event in runner.run_async(
#             user_id="user_1",
#             session_id=session.id,
#             new_message=content,
#         ):
#             if event.is_final_response() and event.content:
#                 for part in event.content.parts:
#                     print("Agent:", part.text)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except Exception as e:
#         print(f"CRASHED: {e}")
#         import traceback
#         traceback.print_exc()