"""
JLLMBot - Intelligent Agent System

A framework for building, deploying, and managing AI agents with
configurable roles, actions, and interaction patterns.
"""

__version__ = "0.1.0"

from .core.agent import Agent, AgentConfig
from .core.context import Context, SessionMemory

__all__ = [
    "Agent",
    "AgentConfig",
    "Context",
    "SessionMemory",
]
