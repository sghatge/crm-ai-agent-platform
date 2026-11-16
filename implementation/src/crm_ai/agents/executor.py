from crm_ai.tools.crm_mock import get_contact

ALLOWED_TOOLS = {"get_contact": get_contact}


def execute_tool(tool_name: str, arguments: dict):
    if tool_name not in ALLOWED_TOOLS:
        raise ValueError(f"Tool is not allow-listed: {tool_name}")
    return ALLOWED_TOOLS[tool_name](**arguments)
