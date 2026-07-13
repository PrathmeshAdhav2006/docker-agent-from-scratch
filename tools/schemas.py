list_running_containers_tool = {
    "type": "function",
    "function": {
        "name": "list_running_containers",
        "description": "Lists all currently running Docker containers.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
}

list_images_tool = {
    "type": "function",
    "function": {
        "name": "list_images",
        "description": "Lists all Docker images available on the system.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
}