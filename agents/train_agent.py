import os
import asyncio
# from dotenv import load_dotenv

# load_dotenv()

# os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"


from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from tools.train_tools import search_trains

# print("Step 1: imports done")

train_agent = Agent(
    name="train_agent",
    model="gemini-2.5-pro",
    tools=[search_trains],
    output_key="train_data",
    instruction="""
    You are a train schedule specialist for Indian Railways.
    Review the conversation history for travel details (source city, destination city, travel date).

    CRITICAL INSTRUCTIONS BEFORE USING TOOLS:
    1. Determine the Indian Railway primary station codes for the source and destination cities.
       Examples: New Delhi='NDLS', Mumbai Central='MMCT', Bangalore='SBC', Chennai='MAS', Pune='PUNE'

    2. Format the travel date into exactly 'DD-MM-YYYY' format.

    3. Use the search_trains tool with these station codes and formatted date.

    4. If no trains are found or the API returns empty results:
       - Try alternative major stations in the same city (e.g., for Delhi: try NDLS, DLI, NZM)
       - Try nearby cities with major railway stations (within 100km)
       - Clearly mention: "Showing trains from [Station Name] ([CODE]) as an alternative"

    5. If still no results, return: "No trains available between these cities on this date."

    Do NOT ask the user for clarification. Make the best decision and explain it clearly.
    """
)


# async def main():
#     print("Step 3: inside main")
#     session_service = InMemorySessionService()
#     print("Step 4: session service created")
#     session = await session_service.create_session(
#         state={}, app_name="flight_app", user_id="user_1"
#     )
#     print("Step 5: session created")
#     runner = Runner(
#         app_name="flight_app",
#         agent=train_agent,
#         session_service=session_service,
#     )
#     print("Flight Agent ready. Type your query (Ctrl+C to exit):\n")
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