"""Configuration for available tools and schemas."""

from tools.implementations import list_images, list_running_containers
from tools.schemas import list_running_containers_tool , list_images_tool


AVAILABLE_TOOLS = {
    "list_running_containers": list_running_containers, 
    "list_images": list_images
}

TOOL_SCHEMAS = [
    list_running_containers_tool,
    list_images_tool
]
