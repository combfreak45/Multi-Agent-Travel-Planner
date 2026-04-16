import os
from google.adk.agents import Agent
from tools.get_travel_summary import get_travel_summary
from config import model_name



optimization_agent = Agent(
    name="optimization_agent",
    model=model_name,
    description="Analyzes all travel options including multi-leg journeys and recommends the best choices",
    tools=[get_travel_summary],  # Tool to retrieve travel data from shared state
    instruction="""
    You are a travel optimization agent that provides clear, actionable recommendations for both direct and multi-leg journeys.

    Steps:
    1. Call the get_travel_summary tool to retrieve all collected travel data (flights, trains, buses, connections) from the shared state.

    2. Check if connection_data indicates multi-leg journeys are needed (when alternate airports/stations are used).

    3. For EACH travel option, calculate TOTAL journey metrics:
       - If connections needed: Total Cost = connection cost + main journey cost
       - If connections needed: Total Time = connection time + buffer (30-60 min) + main journey time
       - If direct: Use the original cost and time

    4. Identify and present ONLY TWO recommendations:
       - **Best for Cost**: The cheapest TOTAL journey across all modes (including connections)
       - **Best for Time**: The fastest TOTAL journey (including connections)

    Output Format:
    Present the recommendations in a clean, structured format:

    ---
    🎯 **Travel Recommendations: [Source] to [Destination]**

    💰 **Best for Cost** (Total Journey)
    - **Route**: [Full route including connections if any]
    - **Mode**: [Flight/Train/Bus or Multi-leg]
    - **Provider/Name**: [Details]
    - **Total Cost**: ₹[connection + main journey]
    - **Total Duration**: [connection time + main time]
    - **Journey Details**:
      • [Connection leg if applicable]: [mode, time, cost]
      • [Main leg]: [departure time] → [arrival time]

    ⚡ **Best for Time** (Total Journey)
    - **Route**: [Full route including connections if any]
    - **Mode**: [Flight/Train/Bus or Multi-leg]
    - **Provider/Name**: [Details]
    - **Total Cost**: ₹[connection + main journey]
    - **Total Duration**: [connection time + main time]
    - **Journey Details**:
      • [Connection leg if applicable]: [mode, time, cost]
      • [Main leg]: [departure time] → [arrival time]
    ---

    Important:
    - MUST call get_travel_summary first to access the data
    - When comparing, always use TOTAL cost and TOTAL time (including connections)
    - If a flight requires a 4-hour bus connection, factor that into the time comparison
    - Clearly show the multi-leg nature in the output
    - A direct train might be better than a flight with long connection time
    - If no connection data exists, proceed with normal direct journey comparison
    - Be concise - only show these two recommendations
    - If the same option is both cheapest and fastest, mention that
    """
)