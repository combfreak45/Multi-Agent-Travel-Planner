from google.adk.tools.tool_context import ToolContext

def save_note(tool_context: ToolContext, note: str) -> dict:
    tool_context.state["NOTE"] = note
    return {"status": "saved"}

def create_task(tool_context: ToolContext, task: str) -> dict:
    tool_context.state["TASK"] = task
    return {"status": "created"}

def get_travel_summary(tool_context: ToolContext) -> dict:
    return {
        "flights": tool_context.state.get("flight_data", "No data"),
        "trains": tool_context.state.get("train_data", "No data"),
        "buses": tool_context.state.get("bus_data", "No data"),
    }
