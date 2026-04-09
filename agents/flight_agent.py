import os
import asyncio
# from dotenv import load_dotenv

# load_dotenv()

# os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

# print("Step 1: imports done 2")

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from tools.flight_tools import search_flights

print("Step 1: imports done")

flight_agent = Agent(
    model="gemini-2.5-pro",
    name="flight_agent",
    description="Helps search for flights.",
    instruction="You help users find flights. Use the search_flights tool.",
    tools=[search_flights],
)

print("Step 2: agent created")

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
        agent=flight_agent,
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