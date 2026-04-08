import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

print("Step 1: imports done 2")

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from tools.train_tools import search_trains

train_agent = Agent(
    name="train_agent",
    model="gemini-2.5-pro",
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


async def main():
    print("Step 3: inside main")
    session_service = InMemorySessionService()
    print("Step 4: session service created")
    session = await session_service.create_session(
        state={}, app_name="flight_app", user_id="user_1"
    )
    print("Step 5: session created")
    runner = Runner(
        app_name="flight_app",
        agent=train_agent,
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