"""Configuration for available tools and schemas."""

from tools.implementations import container_logs, list_images, list_running_containers
from tools.schemas import list_running_containers_tool , list_images_tool , container_logs_tool


AVAILABLE_TOOLS = {
    "list_running_containers": list_running_containers, 
    "list_images": list_images,
    "container_logs": container_logs
}

TOOL_SCHEMAS = [
    list_running_containers_tool,
    list_images_tool,
    container_logs_tool
]   

