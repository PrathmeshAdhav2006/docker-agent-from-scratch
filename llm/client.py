from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # Ollama ignores this, but the SDK requires it
)
