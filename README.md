# 🐳 Docker Agent From Scratch

A **Docker AI agent built from scratch** using Python, the OpenAI-compatible API, and Ollama. Implements raw tool calling, conversation history, and dynamic tool execution **without agent frameworks**.

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **🔧 Raw Tool Calling** - Direct implementation of OpenAI-compatible tool/function calling without relying on agent frameworks
- **💬 Conversation History** - Full conversation context across multiple turns
- **🤖 Dynamic Tool Execution** - Seamlessly execute Docker commands via the LLM agent
- **🏗️ Well-Structured** - Clean separation of concerns with organized module structure
- **🚀 Extensible** - Easy to add new tools and capabilities
- **⚡ Lightweight** - Minimal dependencies, only OpenAI SDK and Ollama

## 🏛️ Architecture

The agent operates through a structured pipeline:

1. **User Input** → Sent to LLM with system prompt and tools
2. **LLM Processing** → Model decides which tool to call (if any)
3. **Tool Execution** → Agent executes the selected tool
4. **Result Integration** → Tool result added to conversation history
5. **Response Generation** → LLM provides final response to user

### Project Structure

```
docker-agent/
├── main.py                         # Entry point (minimal)
├── llm/
│   ├── __init__.py
│   └── client.py                   # OpenAI client configuration
├── src/
│   ├── __init__.py
│   ├── agent.py                    # Main agent loop
│   ├── config.py                   # Tools configuration
│   └── prompts.py                  # System prompts
├── tools/
│   ├── __init__.py
│   ├── implementations.py          # Tool function implementations
│   └── schemas.py                  # OpenAI tool schemas
├── pyproject.toml                  # Project metadata & dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [Ollama](https://ollama.ai/) running locally (default: `http://localhost:11434`)
- Docker (for running containers)
- `uv` (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/PrathmeshAdhav2006/docker-agent-from-scratch.git
cd docker-agent

# Install dependencies
uv sync

# Start Ollama (in another terminal)
ollama serve
```

### Running the Agent

```bash
# Start the agent
uv run main.py

# Example interaction:
# You: List all running Docker containers
# Agent: [Calls list_running_containers tool]
# Agent: Here are the currently running containers...

# Type 'exit' to quit
```

## 🔧 Available Tools

### `list_running_containers`
Lists all currently running Docker containers with details (ID, image, name, status, ports).

**Usage:**
```
You: What Docker containers are currently running?
Agent: [Executes list_running_containers]
Agent: Here are your running containers...
```

## 📝 System Prompt

The agent follows a strict set of rules defined in `src/prompts.py`:

1. **Use available tools** - If a suitable tool exists, use it
2. **Never block user** - Don't ask user to manually run Docker commands
3. **Clear communication** - State when operations are not implemented
4. **No assumptions** - Never invent or assume unavailable tools

## 🛠️ Adding New Tools

Adding a new Docker tool is straightforward:

### 1. Implement the tool function

**File:** `tools/implementations.py`
```python
def your_new_tool():
    """Description of what this tool does."""
    # Implementation here
    return result
```

### 2. Define the OpenAI schema

**File:** `tools/schemas.py`
```python
your_tool_schema = {
    "type": "function",
    "function": {
        "name": "your_new_tool",
        "description": "What this tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "..."}
            },
            "required": ["param1"],
            "additionalProperties": False
        }
    }
}
```

### 3. Register in configuration

**File:** `src/config.py`
```python
from tools.implementations import your_new_tool
from tools.schemas import your_tool_schema

AVAILABLE_TOOLS = {
    "list_running_containers": list_running_containers,
    "your_new_tool": your_new_tool,  # Add here
}

TOOL_SCHEMAS = [
    list_running_containers_tool,
    your_tool_schema,  # Add here
]
```

That's it! The agent will automatically discover and use your new tool.

## 🔌 Configuration

### Ollama Model

The default model is `gpt-oss:20b`. Change it in `src/agent.py`:

```python
response = client.chat.completions.create(
    model="gpt-oss:20b",  # Change this
    messages=messages,
    tools=TOOL_SCHEMAS
)
```

Available Ollama models: [ollama.ai/library](https://ollama.ai/library)

### LLM Endpoint

Configure the Ollama endpoint in `llm/client.py`:

```python
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Change if needed
    api_key="ollama"
)
```

## 💡 How It Works

### Agent Loop

```
┌─────────────────────────────────────────────┐
│ User enters prompt                          │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ Send to LLM with system prompt & tools      │
└──────────────┬──────────────────────────────┘
               │
               ▼
         ┌──────────────┐
         │ LLM Response │
         └──────┬───────┘
                │
        ┌───────┴───────┐
        │               │
   finish_reason   finish_reason
   = "tool_calls"  = "end_turn"
        │               │
        ▼               ▼
    Execute Tool    Print Response
        │               │
        ├───────────────┤
        │               │
        └───────┬───────┘
                │
           Continue Loop
```

### Conversation History

Each message is stored with its role:
- `"system"` - System prompt with rules
- `"user"` - User messages
- `"assistant"` - Agent responses with tool calls
- `"tool"` - Tool execution results

This creates a full conversation context that persists across multiple turns.

## 🧪 Testing

Run the verification script to ensure everything is working:

```bash
uv run verify_structure.py
```

Expected output:
```
✓ All imports working
✓ Available tools: ['list_running_containers']
✓ System prompt loaded: 478 chars
```

## 🔐 Security Considerations

- **Tool validation** - Only registered tools can be executed
- **Error handling** - Tool errors are caught and reported safely
- **System isolation** - Tools run in the same environment; use containers for isolation

## 📦 Dependencies

- `openai` - OpenAI SDK for API compatibility with Ollama

See `pyproject.toml` for full dependency list.

## 🤝 Contributing

Contributions are welcome! To add new tools or features:

1. Fork the repository
2. Create a feature branch
3. Add your tool following the structure above
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🎯 Roadmap

- [ ] Add more Docker tools (create, stop, remove containers)
- [ ] Image management tools
- [ ] Network and volume management
- [ ] Persistent conversation history (file/database)
- [ ] Web UI dashboard
- [ ] Multi-model support
- [ ] Tool parameter validation

## 🤔 FAQ

**Q: Why Ollama instead of OpenAI API?**
A: Ollama is free, open-source, and runs locally. Perfect for development and privacy-conscious applications.

**Q: Can I use this with the real OpenAI API?**
A: Yes! Just change the `base_url` in `llm/client.py` to `https://api.openai.com/v1` and update the API key.

**Q: How do I handle tool parameters?**
A: Parameters are defined in the OpenAI schema under `parameters.properties`. The agent automatically extracts them from the LLM response.

**Q: Can I run multiple tools in one turn?**
A: Currently, the agent processes one tool per turn. Multiple tools can be called across multiple turns via conversation history.

---

**Built with ❤️ using Python, Ollama, and OpenAI-compatible APIs**
