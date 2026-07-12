"""Configuration for available tools and schemas."""

from tools.implementations import list_running_containers
from tools.schemas import list_running_containers_tool


AVAILABLE_TOOLS = {
    "list_running_containers": list_running_containers,
}

TOOL_SCHEMAS = [
    list_running_containers_tool
]
