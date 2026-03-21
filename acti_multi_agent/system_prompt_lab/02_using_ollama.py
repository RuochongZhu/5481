#!/usr/bin/env python3
"""
02_using_ollama.py — System Prompt Role Exploration
SYSEN 6170 Lab: Understanding how system prompts define agent behavior

Demonstrates 3 different system prompt roles using Anthropic API.
"""

import os
import sys
from anthropic import Anthropic

MODEL = "claude-sonnet-4-20250514"
client = Anthropic()

# ---------------------------------------------------------------------------
# Define 3 roles with different system prompts and matching user messages
# ---------------------------------------------------------------------------
roles = [
    {
        "name": "Role 1: Talking Mouse (Original)",
        "system": (
            "You are a talking mouse. Your name is Jerry. "
            "You can only talk about mice and cheese."
        ),
        "user": "What do you think about the weather today?",
    },
    {
        "name": "Role 2: Helpful Data Analyst",
        "system": (
            "You are a helpful data analyst. You specialize in interpreting "
            "datasets, explaining statistical concepts in plain language, and "
            "recommending appropriate visualizations. Keep answers concise."
        ),
        "user": "I have a dataset with 1000 rows of customer purchase history. What's the best way to find purchasing trends?",
    },
    {
        "name": "Role 3: Creative Writing Assistant",
        "system": (
            "You are a creative writing assistant. You help users brainstorm "
            "story ideas, develop characters, and improve prose style. "
            "You write in a vivid, engaging tone."
        ),
        "user": "Help me write the opening paragraph of a mystery novel set in a small college town.",
    },
]

# ---------------------------------------------------------------------------
# Run each role
# ---------------------------------------------------------------------------
for i, role in enumerate(roles):
    print("=" * 60)
    print(f"  {role['name']}")
    print("=" * 60)
    print(f"  System Prompt: {role['system']}")
    print(f"  User Message:  {role['user']}")
    print("-" * 60)

    resp = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=role["system"],
        messages=[{"role": "user", "content": role["user"]}],
    )
    print(f"  Agent Response:\n{resp.content[0].text}")
    print()

print("=" * 60)
print("  Done — 3 roles tested.")
print("=" * 60)
