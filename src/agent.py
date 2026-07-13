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

        print(f"\n🔧 Executing Tool: {tool_name}")

        tool = AVAILABLE_TOOLS.get(tool_name)

        if tool is None:

            tool_result = (
                f"Error: Tool '{tool_name}' is not available."
            )

            print(f"❌ {tool_name} failed")

        else:

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

                tool_result = tool(**arguments)

                print(f"✅ {tool_name} completed")

            except Exception as e:

                tool_result = (
                    f"Error while executing '{tool_name}': {e}"
                )

                print(f"❌ {tool_name} failed")

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
            print("\n👋 Goodbye!")
            break

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        round_number = 1

        while True:

            print(f"\n🤖 Processing (Round {round_number})...")

            response = ask_llm(
                messages,
                use_tools=True,
            )

            assistant_message = response.choices[0].message
            finish_reason = response.choices[0].finish_reason

            # Final response
            if finish_reason != "tool_calls":
                break

            print("🧠 Tool(s) requested.\n")

            messages.append(assistant_message)

            tool_messages = execute_tool_calls(
                assistant_message.tool_calls
            )

            messages.extend(tool_messages)

            round_number += 1

        print("\n💬 Generating response...\n")

        print("🐳 Docker Assistant:\n")

        print(assistant_message.content)

        messages.append(assistant_message)