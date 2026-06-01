"""
Interaction Manager - Orchestrates agent collaboration.

Based on docs/interaction/interaction-overview.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class InteractionType(Enum):
    """Types of agent interaction."""
    SEQUENTIAL = "sequential"
    GROUP_DISCUSS = "group_discuss"
    WORKFLOW_SUGGESTION = "workflow_suggestion"


@dataclass
class InteractionConfig:
    """Configuration for an interaction."""
    interaction_type: InteractionType
    agents: list[str] = field(default_factory=list)
    shared_context: bool = True


@dataclass
class InteractionManager:
    """
    Manages how agents communicate, collaborate, and coordinate
    within a shared context.
    """
    current_type: InteractionType = InteractionType.SEQUENTIAL
    agents_in_context: list[str] = field(default_factory=list)

    def set_interaction_type(self, interaction_type: InteractionType) -> None:
        """Set the current interaction type."""
        self.current_type = interaction_type

    def add_agent(self, agent_id: str) -> None:
        """Add agent to the interaction context."""
        if agent_id not in self.agents_in_context:
            self.agents_in_context.append(agent_id)

    def remove_agent(self, agent_id: str) -> None:
        """Remove agent from the interaction context."""
        if agent_id in self.agents_in_context:
            self.agents_in_context.remove(agent_id)

    def execute_interaction(
        self,
        input_data: Any,
        agents: list[str] | None = None
    ) -> Any:
        """
        Execute interaction with given input.

        Args:
            input_data: Input to process
            agents: Optional list of agents to use (overrides default)

        Returns:
            Interaction result
        """
        if agents:
            self.agents_in_context = agents

        if self.current_type == InteractionType.SEQUENTIAL:
            return self._execute_sequential(input_data)
        elif self.current_type == InteractionType.GROUP_DISCUSS:
            return self._execute_group_discuss(input_data)
        elif self.current_type == InteractionType.WORKFLOW_SUGGESTION:
            return self._execute_workflow_suggestion(input_data)

        raise ValueError(f"Unknown interaction type: {self.current_type}")

    def _execute_sequential(self, input_data: Any) -> Any:
        """Execute sequential interaction."""
        from .sequential import SequentialInteraction
        interaction = SequentialInteraction(agents=self.agents_in_context)
        return interaction.process(input_data)

    def _execute_group_discuss(self, input_data: Any) -> Any:
        """Execute group discuss interaction."""
        from .group_discuss import GroupDiscuss
        discuss = GroupDiscuss(agents=self.agents_in_context)
        return discuss.discuss(input_data)

    def _execute_workflow_suggestion(self, input_data: Any) -> Any:
        """Execute workflow suggestion interaction."""
        from .workflow_suggestion import WorkflowSuggestion
        suggestion = WorkflowSuggestion(agents=self.agents_in_context)
        return suggestion.suggest_and_execute(input_data)


@dataclass
class AgentAwareness:
    """Agents within a context are aware of each other."""
    know_other_agents: bool = True
    know_other_capabilities: bool = True
    know_current_role: bool = True

    def get_other_agents(self, agent_id: str) -> list[str]:
        """Get list of other agents."""
        return []  # Would return agents from context

    def get_agent_capabilities(self, agent_id: str) -> dict[str, Any]:
        """Get capabilities of an agent."""
        return {}
