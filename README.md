# 🐳 Docker Agent

Docker Agent is a Python assistant that connects to an OpenAI-compatible chat API and executes Docker actions through explicitly registered tools. The codebase is intentionally small and direct: a single entry point launches the agent loop, the model is configured through a local client wrapper, and Docker operations are implemented as plain Python functions.

> ✨ Fast, local, tool-driven Docker control with a model that follows the rules you define.

This project currently uses Ollama by default, but the client is compatible with any backend that speaks the OpenAI chat completion API.

## 🌈 Overview

The agent keeps conversation history in memory, sends the full message thread to the model on each turn, and executes any tool calls the model requests. Tool execution is limited to the functions defined in `tools/implementations.py` and exposed through `src/config.py`.

At a high level, the flow is:

1. 👤 The user enters a prompt in the terminal.
2. 🧠 `src/agent.py` sends the message history to the model.
3. 🛠️ The model may return a normal response or one or more tool calls.
4. ⚙️ If tools are requested, the agent executes them and appends the results to the conversation.
5. 💬 The model is called again until it returns a final response.

## 🎯 What This Project Does

The current tool set supports common Docker read and control operations:

- 📋 Listing running containers
- 🧾 Listing all containers, including stopped ones
- 🖼️ Listing local images
- 📜 Reading container logs
- ⏹️ Stopping a container
- 🗑️ Removing a container

The agent does not invent tools or fall back to manual commands when an operation is not implemented. If a needed capability is missing, that limitation is surfaced directly through the prompt and tool layer.

## 🗂️ Project Layout

```
docker_agent/
├── main.py
├── llm/
│   └── client.py
├── src/
│   ├── agent.py
│   ├── config.py
│   └── prompts.py
├── tools/
│   ├── implementations.py
│   └── schemas.py
├── verify_structure.py
└── pyproject.toml
```

## ✨ Features

- 💬 Chat loop with conversation history
- 🔌 OpenAI-compatible tool calling
- 🐋 Docker command execution through a controlled tool registry
- 🧭 A prompt that tells the model to use registered tools instead of guessing
- 🧰 Support for listing containers, listing images, showing container logs, stopping containers, removing containers, and listing all containers
- 🪄 A simple code path that is easy to inspect and extend

## 🧱 Requirements

- 🐍 Python 3.12+
- 🐳 Docker installed locally
- 🌐 Ollama or another OpenAI-compatible endpoint running at `http://localhost:11434/v1`
- ⚡ `uv` for dependency management

The code also assumes the Docker CLI is available at `/usr/bin/docker`, because the tool implementations call that path directly.

## 🚀 Setup

<details>
<summary>Show setup steps</summary>

```bash
uv sync
```

If you are using Ollama, make sure it is running before starting the agent:

```bash
ollama serve
```

</details>

## ▶️ Run

```bash
uv run main.py
```

Type `exit` to quit the conversation.

<details>
<summary>Try these quick prompts</summary>

- Show running containers
- Show all containers
- Show logs for nginx
- Stop a container by name

</details>

## 💡 Example Session

```text
You: list running containers
Assistant: Here are the running containers...

You: show logs for nginx
Assistant: Here are the logs for nginx...
```

The exact output depends on the containers and images available on your machine.

## 🧰 Available Tools

The agent currently exposes these tools:

- `list_running_containers` - runs `docker ps`
- `list_all_containers` - runs `docker ps -a`
- `list_images` - runs `docker images`
- `container_logs` - runs `docker logs <container>`
- `stop_container` - runs `docker stop <container>`
- `remove_container` - runs `docker rm <container>`

Tool names, arguments, and schemas are defined in `tools/schemas.py`, and the runtime registry lives in `src/config.py`.

### ⚙️ Tool Behavior

The tool layer is intentionally thin:

- Each function shells out to Docker and returns plain text output.
- Errors are returned as strings rather than raising through the agent loop.
- Tool arguments are passed from the model to Python using the schema definitions in `tools/schemas.py`.
- The agent can handle multiple tool calls in one assistant turn if the model returns them.

## ⚙️ Configuration

The model and endpoint are configured in the code rather than through a separate config file:

- `llm/client.py` sets the OpenAI client base URL and API key placeholder
- `src/agent.py` sets the default model name
- `src/prompts.py` defines the system prompt and behavior rules

If you want to point the agent at a different OpenAI-compatible backend, update `llm/client.py`. If you want to use a different model name, update `src/agent.py`.

### 🔧 Current Defaults

- Base URL: `http://localhost:11434/v1`
- API key placeholder: `ollama`
- Model: `gpt-oss:20b`

These defaults are designed for local Ollama usage.

## ✅ Verification

```bash
uv run verify_structure.py
```

That script checks the imports, available tools, and prompt loading.

You can also use it as a quick smoke test after changing tool registrations or prompt content.

## 🛠️ Extending the Agent

To add a new tool, implement the Docker action in `tools/implementations.py`, define the schema in `tools/schemas.py`, and register both in `src/config.py`.

Suggested workflow:

1. ✍️ Add a Python function that performs the Docker action.
2. 🧩 Add a matching schema so the model knows the tool name and arguments.
3. 🔗 Register the function and schema in the config module.
4. 📝 Update the prompt if the new tool changes the agent’s behavior rules.
5. 🧪 Run the verification script and test the new interaction end to end.

## 🧠 Prompt Behavior

The system prompt in `src/prompts.py` is responsible for keeping the agent disciplined.

It instructs the model to:

- 🛠️ Use tools whenever live Docker information is required
- 🚫 Avoid guessing or fabricating Docker state
- 📣 Report when a requested feature is not implemented
- 📦 Preserve tool output accurately
- 🎯 Stay concise and professional

This prompt is an important part of the project because the tool layer is intentionally minimal and the model must rely on the registered commands.

## 🧯 Troubleshooting

If the agent does not start, check the following first:

- 🌐 Ollama or your OpenAI-compatible endpoint is running
- 🐳 Docker is installed and available at `/usr/bin/docker`
- 🔐 You have permission to run Docker commands on the machine
- 🧠 The model name in `src/agent.py` exists in your backend

If a tool returns an error, the error text is passed back into the conversation. That usually means the Docker command failed, the container name is wrong, or Docker is not available in the current environment.

If you change the tool registry and the verification script fails, inspect `src/config.py` and `tools/schemas.py` for mismatched names or missing imports.

## 📝 Notes

- The agent only executes tools that are already registered.
- Docker commands are run on the local machine, so the agent should be used in a trusted environment.
