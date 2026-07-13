"""Main agent loop for Docker assistant."""

import json

from llm.client import client
from src.prompts import DOCKER_ASSISTANT_PROMPT
from src.config import AVAILABLE_TOOLS, TOOL_SCHEMAS


MODEL = "gpt-oss:20b"


def ask_llm(messages, use_tools=True):
    """Send messages to the LLM."""

    kwargs = {
        "model": MODEL,
        "messages": messages,
    }

    if use_tools:
        kwargs["tools"] = TOOL_SCHEMAS

    return client.chat.completions.create(**kwargs)


def execute_tool_calls(tool_calls):
    """Execute all requested tools and return tool messages."""

    tool_messages = []

    for tool_call in tool_calls:

        tool_name = tool_call.function.name

        tool = AVAILABLE_TOOLS.get(tool_name)

        if tool is None:

            tool_result = (
                f"Error: Tool '{tool_name}' is not available."
            )

        else:

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

                tool_result = tool(**arguments)

            except Exception as e:

                tool_result = (
                    f"Error while executing "
                    f"'{tool_name}': {e}"
                )

        tool_messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            }
        )

    return tool_messages


def run_agent():
    """Run the Docker assistant."""

    messages = [
        {
            "role": "system",
            "content": DOCKER_ASSISTANT_PROMPT,
        }
    ]

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        response = ask_llm(
            messages,
            use_tools=True,
        )

        assistant_message = response.choices[0].message

        if response.choices[0].finish_reason == "tool_calls":

            messages.append(assistant_message)

            tool_messages = execute_tool_calls(
                assistant_message.tool_calls
            )

            messages.extend(tool_messages)

            response = ask_llm(
                messages,
                use_tools=False,
            )

            assistant_message = response.choices[0].message

        print(f"\n🐳 Docker Assistant:\n")

        print(assistant_message.content)

        messages.append(assistant_message)