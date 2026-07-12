"""Main agent loop for Docker assistant."""

import json
from llm.client import client
from src.prompts import DOCKER_ASSISTANT_PROMPT
from src.config import AVAILABLE_TOOLS, TOOL_SCHEMAS


def run_agent():
    """Run the Docker assistant agent loop."""
    messages = [
        {
            "role": "system",
            "content": DOCKER_ASSISTANT_PROMPT
        }
    ]

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = client.chat.completions.create(
            model="gpt-oss:20b",
            messages=messages,
            tools=TOOL_SCHEMAS
        )

        assistant_message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            # Save assistant message containing tool calls
            messages.append(assistant_message)

            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool = AVAILABLE_TOOLS.get(tool_name)

                if tool is None:
                    tool_result = f"Error: Tool '{tool_name}' is not available."
                else:
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                        tool_result = tool(**arguments)
                    except Exception as e:
                        tool_result = f"Error while executing '{tool_name}': {e}"

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    }
                )

            response = client.chat.completions.create(
                model="gpt-oss:20b",
                messages=messages
            )

            final_message = response.choices[0].message
            print(f"\nAgent: {final_message.content}")
            messages.append(final_message)

        else:
            print(f"\nAgent: {assistant_message.content}")
            messages.append(assistant_message)
