import asyncio
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.agents import ParallelAgent
from google.adk.agents import SequentialAgent
from config import model_name

from agents import (
    flight_agent,
    train_agent,
    bus_agent,
    response_formatter,
)

print("Step 1: imports done")

# travel agent

travel_planner = ParallelAgent(
    name="travel_planner_workflow",
    sub_agents=[
        flight_agent,
        train_agent,
        bus_agent
    ]
)


# travel workflow

travel_workflow = SequentialAgent(
    name="travel_workflow",
    sub_agents=[
        travel_planner,      # Step 1: Gather options
        response_formatter,  # Step 2: Format output
    ]
)


# root agent

root_agent = Agent(
    name="travel_assistant",
    model=model_name,
    description="Main entry point for travel planning assistant",
    instruction="""
    You are a helpful travel planning assistant.
    - Greet the user warmly.
    - Ask for travel details if missing: source city, destination city, and travel date.
    - Once you have all three details, transfer control to the travel_workflow.
    """,
    sub_agents=[travel_workflow]
)

# for testing flow

async def main():
    print("Step 3: inside main")
    session_service = InMemorySessionService()
    print("Step 4: session service created")
    session = await session_service.create_session(
        state={}, app_name="travel_app", user_id="user_1"
    )
    print("Step 5: session created")
    runner = Runner(
        app_name="travel_app",
        agent=root_agent,
        session_service=session_service,
    )
    print("Main Agent ready. Type your query (Ctrl+C to exit):\n")
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