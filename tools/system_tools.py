from google.adk.tools.tool_context import ToolContext

def save_note(tool_context: ToolContext, note: str) -> dict:
    tool_context.state["NOTE"] = note
    return {"status": "saved"}

def create_task(tool_context: ToolContext, task: str) -> dict:
    tool_context.state["TASK"] = task
    return {"status": "created"}

