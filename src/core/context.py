"""
Context - Session memory and state management for agents.

Based on docs/core/context.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from datetime import datetime


@dataclass
class SessionMemory:
    """Memory management for a session."""
    session_id: str = field(default_factory=lambda: str(uuid4()))
    short_term: dict[str, Any] = field(default_factory=dict)
    long_term: dict[str, Any] = field(default_factory=dict)
    ttl_seconds: int = 3600
    created_at: datetime = field(default_factory=datetime.now)

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from short or long term memory."""
        if key in self.short_term:
            return self.short_term[key]
        if key in self.long_term:
            return self.long_term[key]
        return default

    def set(self, key: str, value: Any, long_term: bool = False) -> None:
        """Set value in memory."""
        if long_term:
            self.long_term[key] = value
        else:
            self.short_term[key] = value

    def delete(self, key: str) -> None:
        """Delete value from memory."""
        self.short_term.pop(key, None)
        self.long_term.pop(key, None)

    def clear_short_term(self) -> None:
        """Clear short term memory."""
        self.short_term.clear()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "session_id": self.session_id,
            "short_term": self.short_term,
            "long_term": self.long_term,
            "ttl_seconds": self.ttl_seconds,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class StaticAgentList:
    """Static list of agents organized by threading."""
    threads: dict[str, list[str]] = field(default_factory=dict)
    agent_availability: dict[str, str] = field(default_factory=dict)

    def add_agent(self, agent_id: str, thread_id: str | None = None) -> None:
        """Add agent to list."""
        if thread_id is None:
            thread_id = "default"
        if thread_id not in self.threads:
            self.threads[thread_id] = []
        if agent_id not in self.threads[thread_id]:
            self.threads[thread_id].append(agent_id)
        self.agent_availability[agent_id] = "online"

    def remove_agent(self, agent_id: str) -> None:
        """Remove agent from list."""
        for thread_agents in self.threads.values():
            if agent_id in thread_agents:
                thread_agents.remove(agent_id)
        self.agent_availability.pop(agent_id, None)

    def set_availability(self, agent_id: str, status: str) -> None:
        """Set agent availability status."""
        self.agent_availability[agent_id] = status

    def get_agents_in_thread(self, thread_id: str) -> list[str]:
        """Get all agents in a thread."""
        return self.threads.get(thread_id, [])

    def get_agent_status(self, agent_id: str) -> str | None:
        """Get agent status."""
        return self.agent_availability.get(agent_id)


@dataclass
class SharedContext:
    """Shared context for multi-agent collaboration."""
    enabled: bool = True
    sync_frequency: str = "real_time"
    shared_data: dict[str, bool] = field(default_factory=lambda: {
        "current_job": True,
        "accumulated_results": True,
        "intermediate_states": True
    })

    def sync(self, data: dict[str, Any]) -> None:
        """Synchronize shared data."""
        pass  # Implementation depends on sync_frequency

    def get_shared(self, key: str) -> Any:
        """Get shared value."""
        return None


@dataclass
class Context:
    """
    Context is the environment in which agents operate.
    Provides session-based memory management and state maintenance.
    """
    session_memory: SessionMemory = field(default_factory=SessionMemory)
    static_agent_list: StaticAgentList = field(default_factory=StaticAgentList)
    shared_context: SharedContext = field(default_factory=SharedContext)
    current_job_type: str | None = None

    @classmethod
    def create(cls, session_id: str | None = None) -> Context:
        """Create a new context."""
        memory = SessionMemory(session_id=session_id or str(uuid4()))
        return cls(session_memory=memory)

    def set_job_type(self, job_type: str) -> None:
        """Set the current job type."""
        self.current_job_type = job_type

    def get_job_type(self) -> str | None:
        """Get the current job type."""
        return self.current_job_type

    def update_agent_list(self, agent_id: str, thread_id: str | None = None) -> None:
        """Add agent to context's agent list."""
        self.static_agent_list.add_agent(agent_id, thread_id)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "session_memory": self.session_memory.to_dict(),
            "current_job_type": self.current_job_type
        }


class AgentAwareness:
    """Agents within a context are aware of each other."""

    def __init__(self, context: Context):
        self.context = context
        self.know_other_agents: bool = True
        self.know_other_capabilities: bool = True
        self.know_current_role: bool = True
        self.can_communicate: bool = True

    def get_agents_in_context(self) -> list[str]:
        """Get all agents in the context."""
        all_agents = []
        for agents in self.context.static_agent_list.threads.values():
            all_agents.extend(agents)
        return all_agents

    def get_agent_info(self, agent_id: str) -> dict[str, Any] | None:
        """Get information about an agent."""
        if not self.know_other_agents:
            return None
        status = self.context.static_agent_list.get_agent_status(agent_id)
        return {
            "agent_id": agent_id,
            "status": status,
            "can_communicate": self.can_communicate
        }
