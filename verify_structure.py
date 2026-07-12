#!/usr/bin/env python3
"""Quick import verification."""

from src.agent import run_agent
from src.config import AVAILABLE_TOOLS
from src.prompts import DOCKER_ASSISTANT_PROMPT

print("✓ All imports working")
print(f"✓ Available tools: {list(AVAILABLE_TOOLS.keys())}")
print(f"✓ System prompt loaded: {len(DOCKER_ASSISTANT_PROMPT)} chars")
