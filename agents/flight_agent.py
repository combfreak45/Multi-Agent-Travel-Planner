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
    If source or destination doesn't have airport search for nearby airport and find flights. No need to ask the user.    """,
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