from google.adk.tools.tool_context import ToolContext


def get_travel_summary(tool_context: ToolContext) -> dict:
    return {
        "flights": tool_context.state.get("flight_data", "No data"),
        "trains": tool_context.state.get("train_data", "No data"),
        "buses": tool_context.state.get("bus_data", "No data"),
    }