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

container_logs_tool = {
    "type": "function",
    "function": {
        "name": "container_logs",
        "description": "Displays the logs of a specified Docker container.",
        "parameters": {
            "type": "object",
            "properties": {
                "container": {
                    "type": "string",
                    "description": "The name or ID of the Docker container."
                }
            },
            "required": ["container"],
            "additionalProperties": False
        }
    }
}

stop_container_tool = {
    "type": "function",
    "function": {
        "name": "stop_container",
        "description": "Stops a specified Docker container.",
        "parameters": {
            "type": "object",
            "properties": {
                "container": {
                    "type": "string",
                    "description": "The name or ID of the Docker container."
                }
            },
            "required": ["container"],
            "additionalProperties": False
        }
    }
}

remove_container_tool = {
    "type": "function",
    "function": {
        "name": "remove_container",
        "description": "Removes a specified Docker container.",
        "parameters": {
            "type": "object",
            "properties": {
                "container": {
                    "type": "string",
                    "description": "The name or ID of the Docker container."
                }
            },
            "required": ["container"],
            "additionalProperties": False
        }
    }
}

list_all_containers_tool = {
    "type": "function",
    "function": {
        "name": "list_all_containers",
        "description": "Lists all Docker containers, including stopped ones.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
}