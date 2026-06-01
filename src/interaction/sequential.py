"""
Sequential Interaction - One-by-one chain processing.

Based on docs/interaction/sequential-interaction.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ChainType(Enum):
    """Types of sequential chains."""
    LINEAR_FORWARD = "linear_forward"
    LINEAR_WITH_SELECTION = "linear_with_selection"
    BIDIRECTIONAL = "bidirectional"
    CYCLIC = "cyclic"


@dataclass
class SequentialConfig:
    """Configuration for sequential interaction."""
    chain_type: ChainType = ChainType.LINEAR_FORWARD
    agent_sequence: list[str] = field(default_factory=list)
    direction: str = "forward"
    loop_allowed: bool = False
    max_iterations: int = 10
    full_output_pass: bool = True
    stop_on_error: bool = True
    retry_count: int = 3


@dataclass
class SequentialInteraction:
    """
    Sequential interaction - agents process in a linear chain,
    each agent's output serving as the next agent's input.
    """
    agents: list[str] = field(default_factory=list)
    config: SequentialConfig = field(default_factory=SequentialConfig)

    def __init__(self, agents: list[str] | None = None, **kwargs: Any):
        self.agents = agents or []
        self.config = SequentialConfig(**kwargs)

    def process(self, input_data: Any) -> Any:
        """
        Process input through the sequential chain.

        Args:
            input_data: Initial input to the chain

        Returns:
            Final output after all agents have processed
        """
        if not self.agents:
            return input_data

        current_data = input_data
        iteration = 0

        while iteration < self.config.max_iterations:
            processed_any = False

            for agent_id in self.config.agent_sequence:
                if agent_id not in self.agents:
                    continue

                # In production, would actually call the agent
                result = self._call_agent(agent_id, current_data)
                if result is not None:
                    current_data = result
                    processed_any = True

                # Check for early termination
                if self._should_terminate(current_data):
                    return current_data

            if not processed_any:
                break

            iteration += 1

            # Handle direction
            if self.config.direction == "backward":
                self.config.agent_sequence = list(reversed(self.config.agent_sequence))

            # Handle cyclic
            if self.config.chain_type == ChainType.CYCLIC and iteration >= self.config.max_iterations:
                if not self._should_terminate(current_data):
                    iteration = 0  # Reset for another cycle

        return current_data

    def _call_agent(self, agent_id: str, input_data: Any) -> Any:
        """
        Call an agent with input data.

        Placeholder - in production would call actual agent.
        """
        # Simulate agent processing
        return f"{agent_id}: {input_data}"

    def _should_terminate(self, data: Any) -> bool:
        """Check if processing should terminate."""
        if isinstance(data, dict):
            return data.get("terminate", False)
        if isinstance(data, str):
            return "terminate" in data.lower()
        return False

    def add_value_at_step(
        self,
        agent_id: str,
        original_data: Any,
        value_additions: list[str]
    ) -> Any:
        """
        Add value at a processing step.

        Args:
            agent_id: Agent adding value
            original_data: Data before adding value
            value_additions: List of values to add

        Returns:
            Data with value additions
        """
        return {
            "original": original_data,
            "agent": agent_id,
            "additions": value_additions
        }


@dataclass
class ValueAddition:
    """Value addition at a chain step."""
    agent_id: str
    role: str
    additions: list[str] = field(default_factory=list)


def suggest_skip_remaining_steps(current_output: Any) -> bool:
    """Suggest skipping remaining steps if output is optimal."""
    if isinstance(current_output, dict):
        return current_output.get("is_optimal", False)
    return False


def suggest_add_refinement_step(current_output: Any, quality_threshold: float = 0.8) -> bool:
    """Suggest adding a refinement step if quality is below threshold."""
    if isinstance(current_output, dict):
        quality = current_output.get("quality", 1.0)
        return quality < quality_threshold
    return False


def suggest_reorder_steps(
    current_sequence: list[str],
    dependency_analysis: dict[str, list[str]]
) -> list[str] | None:
    """Suggest reordering steps based on dependency analysis."""
    # Simple topological sort suggestion
    return current_sequence  # Return unchanged in base implementation


def suggest_parallelize_subtasks(
    current_sequence: list[str],
    independent_tasks: list[list[str]]
) -> list[list[str]]:
    """Suggest parallelizing independent sub-tasks."""
    return independent_tasks
