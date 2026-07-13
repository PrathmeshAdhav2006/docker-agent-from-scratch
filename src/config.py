"""Configuration for available tools and schemas."""

from tools.implementations import container_logs, list_images, list_running_containers, stop_container, remove_container, list_all_containers
from tools.schemas import list_running_containers_tool , list_images_tool , container_logs_tool, stop_container_tool, remove_container_tool, list_all_containers_tool  


AVAILABLE_TOOLS = {
    "list_running_containers": list_running_containers, 
    "list_images": list_images,
    "container_logs": container_logs,
    "stop_container": stop_container,
    "remove_container": remove_container,
    "list_all_containers": list_all_containers,
}

TOOL_SCHEMAS = [
    list_running_containers_tool,
    list_images_tool,
    container_logs_tool,
    stop_container_tool,
    remove_container_tool,
    list_all_containers_tool
]   

