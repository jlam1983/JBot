"""
Mindset Modifier - Agent thinking visualization.

Based on docs/display/mindset-modifier.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from datetime import datetime


class ThinkingStyle(Enum):
    """Agent thinking styles."""
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    PRACTICAL = "practical"
    HYBRID = "hybrid"


class PhaseStatus(Enum):
    """Status of a thought phase."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ThoughtPhase:
    """A phase in the agent's thinking process."""
    phase_name: str
    status: PhaseStatus = PhaseStatus.PENDING
    duration_ms: int = 0
    output: Any = None
    thinking_steps: list[str] = field(default_factory=list)

    def activate(self) -> None:
        self.status = PhaseStatus.IN_PROGRESS

    def complete(self, output: Any = None) -> None:
        self.status = PhaseStatus.COMPLETED
        self.output = output

    def add_thinking_step(self, step: str) -> None:
        self.thinking_steps.append(step)


@dataclass
class ThoughtProcess:
    """
    Represents the agent's thinking process.
    """
    current_phase: str = ""
    phase_history: list[ThoughtPhase] = field(default_factory=list)
    working_memory_usage: float = 0
    attention_focus: str = ""
    processing_mode: str = "deliberate"

    def add_phase(self, phase: ThoughtPhase) -> None:
        """Add a phase to the process."""
        self.phase_history.append(phase)

    def set_current_phase(self, phase_name: str) -> None:
        """Set the currently active phase."""
        self.current_phase = phase_name

    def get_current_phase(self) -> ThoughtPhase | None:
        """Get the currently active phase."""
        for phase in reversed(self.phase_history):
            if phase.phase_name == self.current_phase:
                return phase
        return None

    def get_completed_phases(self) -> list[ThoughtPhase]:
        """Get all completed phases."""
        return [p for p in self.phase_history if p.status == PhaseStatus.COMPLETED]

    def step_forward(self) -> ThoughtPhase | None:
        """Move to the next phase."""
        found_current = False
        for phase in self.phase_history:
            if found_current:
                phase.activate()
                self.current_phase = phase.phase_name
                return phase
            if phase.phase_name == self.current_phase:
                phase.complete()
                found_current = True
        return None

    def step_back(self) -> ThoughtPhase | None:
        """Move to the previous phase."""
        for i, phase in enumerate(self.phase_history):
            if phase.phase_name == self.current_phase:
                if i > 0:
                    prev_phase = self.phase_history[i - 1]
                    prev_phase.status = PhaseStatus.IN_PROGRESS
                    self.current_phase = prev_phase.phase_name
                    return prev_phase
        return None


@dataclass
class PromptComponent:
    """A component of the final prompt."""
    component_type: str  # role_definition, capability_list, constraint_list, etc.
    content: str = ""


@dataclass
class PromptGenerator:
    """
    Manages prompt generation for the agent.
    """
    system_prompt_components: list[PromptComponent] = field(default_factory=list)
    context_injection_enabled: bool = True
    injected_context: list[dict[str, str]] = field(default_factory=list)

    def build_system_prompt(
        self,
        role_definition: str,
        capabilities: list[str],
        constraints: list[str],
        output_format: str | None = None
    ) -> str:
        """Build the system prompt."""
        prompt_parts = [f"You are {role_definition}."]

        if capabilities:
            prompt_parts.append("\nYour capabilities:")
            for cap in capabilities:
                prompt_parts.append(f"- {cap}")

        if constraints:
            prompt_parts.append("\nAlways consider:")
            for constraint in constraints:
                prompt_parts.append(f"- {constraint}")

        if output_format:
            prompt_parts.append(f"\nRespond in {output_format} format.")

        return "\n".join(prompt_parts)

    def inject_context(
        self,
        context_type: str,
        content: str
    ) -> None:
        """Inject context into the prompt."""
        self.injected_context.append({
            "type": context_type,
            "content": content
        })

    def build_final_prompt(
        self,
        user_input: str,
        transformed_input: str | None = None
    ) -> dict[str, Any]:
        """Build the complete prompt with all components."""
        return {
            "system_prompt": "\n".join(c.content for c in self.system_prompt_components),
            "context": self.injected_context if self.context_injection_enabled else [],
            "user_input": transformed_input or user_input,
            "token_count": len(user_input) // 4  # Rough estimate
        }


@dataclass
class Feedback:
    """Feedback to the client."""
    summary: str = ""
    next_steps: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    confidence: float = 0


@dataclass
class MindsetModifier:
    """
    View and modify how agents generate prompts and process thoughts.
    """
    agent_id: str = ""
    thinking_style: ThinkingStyle = ThinkingStyle.ANALYTICAL
    verbosity: int = 3  # 1-5
    reasoning_depth: int = 3  # 1-5
    creativity: int = 3  # 1-5
    caution: int = 3  # 1-5

    # Presets
    ANALYTICAL_PRESET = {
        "thinking_style": ThinkingStyle.ANALYTICAL,
        "verbosity": 3,
        "reasoning_depth": 5,
        "creativity": 2,
        "caution": 4
    }

    CREATIVE_PRESET = {
        "thinking_style": ThinkingStyle.CREATIVE,
        "verbosity": 3,
        "reasoning_depth": 3,
        "creativity": 5,
        "caution": 2
    }

    EFFICIENT_PRESET = {
        "thinking_style": ThinkingStyle.PRACTICAL,
        "verbosity": 2,
        "reasoning_depth": 2,
        "creativity": 3,
        "caution": 2
    }

    THOROUGH_PRESET = {
        "thinking_style": ThinkingStyle.ANALYTICAL,
        "verbosity": 4,
        "reasoning_depth": 5,
        "creativity": 3,
        "caution": 5
    }

    def apply_preset(self, preset_name: str) -> None:
        """Apply a configuration preset."""
        presets = {
            "analytical": self.ANALYTICAL_PRESET,
            "creative": self.CREATIVE_PRESET,
            "efficient": self.EFFICIENT_PRESET,
            "thorough": self.THOROUGH_PRESET
        }

        if preset_name in presets:
            preset = presets[preset_name]
            self.thinking_style = preset["thinking_style"]
            self.verbosity = preset["verbosity"]
            self.reasoning_depth = preset["reasoning_depth"]
            self.creativity = preset["creativity"]
            self.caution = preset["caution"]

    def adjust_thinking_style(self, value: int) -> None:
        """Set thinking style (1=analytical, 5=creative)."""
        self.thinking_style = ThinkingStyle.HYBRID
        if value <= 2:
            self.thinking_style = ThinkingStyle.ANALYTICAL
        elif value >= 4:
            self.thinking_style = ThinkingStyle.CREATIVE

    def adjust_verbosity(self, value: int) -> None:
        """Set verbosity level (1=concise, 5=verbose)."""
        self.verbosity = max(1, min(5, value))

    def adjust_reasoning_depth(self, value: int) -> None:
        """Set reasoning depth (1=shallow, 5=deep)."""
        self.reasoning_depth = max(1, min(5, value))

    def adjust_creativity(self, value: int) -> None:
        """Set creativity level (1=rigid, 5=flexible)."""
        self.creativity = max(1, min(5, value))

    def get_current_configuration(self) -> dict[str, Any]:
        """Get current mindset configuration."""
        return {
            "thinking_style": self.thinking_style.value,
            "verbosity": self.verbosity,
            "reasoning_depth": self.reasoning_depth,
            "creativity": self.creativity,
            "caution": self.caution
        }

    def generate_feedback(
        self,
        result: Any,
        confidence: float
    ) -> Feedback:
        """Generate feedback to the client based on result."""
        return Feedback(
            summary="Task completed successfully" if confidence > 0.7 else "Task completed with warnings",
            next_steps=["Review output", "Approve or modify"],
            suggestions=["Consider testing edge cases"],
            confidence=confidence
        )
