"""
Workflow Suggestion - Dynamic workflow optimization.

Based on docs/interaction/workflow-suggestion.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SuggestionType(Enum):
    """Types of workflow suggestions."""
    PROCESS_ENHANCEMENT = "process_enhancement"
    SCOPE_ADJUSTMENT = "scope_adjustment"
    SEQUENCE_MODIFICATION = "sequence_modification"
    PARALLELIZATION = "parallelization"


class ValueAdditionPoint(Enum):
    """Points where value can be added."""
    INPUT_STAGE = "input_stage"
    PROCESSING_STAGE = "processing_stage"
    OUTPUT_STAGE = "output_stage"


@dataclass
class Suggestion:
    """A suggestion for workflow improvement."""
    suggestion_type: SuggestionType
    description: str
    reasoning: str = ""
    impact: str = "medium"  # high, medium, low
    confidence: float = 0.5
    risk: str = "low"  # high, medium, low
    accepted: bool | None = None

    def accept(self) -> None:
        self.accepted = True

    def reject(self) -> None:
        self.accepted = False

    def should_auto_accept(self) -> bool:
        """Check if suggestion should be auto-accepted."""
        return (
            self.impact == "high" and
            self.confidence > 0.9 and
            self.risk == "low"
        )


@dataclass
class WorkflowChainType:
    """Type of workflow chain."""
    LINEAR = "linear"
    BRANCHED = "branched"
    PARALLEL = "parallel"
    ADAPTIVE = "adaptive"


@dataclass
class WorkflowSuggestion:
    """
    Workflow Suggestion - enables agents to dynamically propose,
    refine, and optimize workflows during execution.
    """
    agents: list[str] = field(default_factory=list)
    chain_type: str = WorkflowChainType.LINEAR
    value_addition_enabled: bool = True

    # Suggestion settings
    suggest_process_enhancement: bool = True
    suggest_scope_adjustment: bool = True
    suggest_sequence_modification: bool = True
    suggest_parallelization: bool = True

    # Value addition points
    input_suggestions: list[str] = field(default_factory=lambda: [
        "input_enrichment", "format_conversion", "constraint_identification"
    ])
    processing_suggestions: list[str] = field(default_factory=lambda: [
        "method_optimization", "alternative_approaches", "risk_identification"
    ])
    output_suggestions: list[str] = field(default_factory=lambda: [
        "result_validation", "format_optimization", "follow_up_suggestions"
    ])

    def __init__(self, agents: list[str] | None = None, **kwargs: Any):
        self.agents = agents or []
        for key, value in kwargs.items():
            setattr(self, key, value)

    def suggest_and_execute(self, workflow_input: Any) -> dict[str, Any]:
        """
        Suggest improvements and execute workflow.

        Returns:
            Results with suggestions and final output
        """
        suggestions = self.generate_suggestions(workflow_input)
        accepted = [s for s in suggestions if s.accepted or s.should_auto_accept()]

        # Execute with accepted suggestions
        result = self._execute_with_suggestions(workflow_input, accepted)

        return {
            "suggestions": [s.__dict__ for s in suggestions],
            "accepted_count": len(accepted),
            "result": result
        }

    def generate_suggestions(self, context: Any) -> list[Suggestion]:
        """Generate workflow suggestions based on context."""
        suggestions = []

        if self.suggest_process_enhancement:
            suggestions.extend(self._suggest_process_enhancements(context))

        if self.suggest_scope_adjustment:
            suggestions.extend(self._suggest_scope_adjustments(context))

        if self.suggest_sequence_modification:
            suggestions.extend(self._suggest_sequence_modifications(context))

        if self.suggest_parallelization:
            suggestions.extend(self._suggest_parallelizations(context))

        return suggestions

    def _suggest_process_enhancements(self, context: Any) -> list[Suggestion]:
        """Suggest process enhancements."""
        return [
            Suggestion(
                suggestion_type=SuggestionType.PROCESS_ENHANCEMENT,
                description="Consider parallel execution where possible",
                reasoning="Parallel execution can reduce overall time",
                impact="high",
                confidence=0.7,
                risk="low"
            )
        ]

    def _suggest_scope_adjustments(self, context: Any) -> list[Suggestion]:
        """Suggest scope adjustments."""
        suggestions = []

        suggestions.append(Suggestion(
            suggestion_type=SuggestionType.SCOPE_ADJUSTMENT,
            description="You might also want to include error handling",
            reasoning="Adding error handling improves robustness",
            impact="medium",
            confidence=0.6,
            risk="low"
        ))

        return suggestions

    def _suggest_sequence_modifications(self, context: Any) -> list[Suggestion]:
        """Suggest sequence modifications."""
        return [
            Suggestion(
                suggestion_type=SuggestionType.SEQUENCE_MODIFICATION,
                description="Moving validation earlier would catch errors sooner",
                reasoning="Early validation prevents downstream errors",
                impact="medium",
                confidence=0.75,
                risk="low"
            )
        ]

    def _suggest_parallelizations(self, context: Any) -> list[Suggestion]:
        """Suggest parallelization opportunities."""
        return [
            Suggestion(
                suggestion_type=SuggestionType.PARALLELIZATION,
                description="Data collection and validation can run concurrently",
                reasoning="Independent tasks can run in parallel",
                impact="high",
                confidence=0.8,
                risk="low"
            )
        ]

    def _execute_with_suggestions(
        self,
        workflow_input: Any,
        accepted_suggestions: list[Suggestion]
    ) -> Any:
        """Execute workflow with accepted suggestions."""
        # Placeholder - would execute workflow with modifications
        return {
            "executed": True,
            "modifications": [s.description for s in accepted_suggestions]
        }

    def evaluate_suggestion(self, suggestion: Suggestion) -> dict[str, Any]:
        """Evaluate a suggestion against criteria."""
        return {
            "impact": suggestion.impact,
            "confidence": suggestion.confidence,
            "risk": suggestion.risk,
            "auto_accept": suggestion.should_auto_accept()
        }


@dataclass
class ValueAddition:
    """Value added at a workflow step."""
    point: ValueAdditionPoint
    additions: list[str] = field(default_factory=list)
    agent_id: str = ""


@dataclass
class AdaptiveWorkflow:
    """Adaptive workflow that can modify based on results."""
    current_step: int = 0
    steps: list[Any] = field(default_factory=list)
    suggestions: list[Suggestion] = field(default_factory=list)

    def adapt(self, intermediate_result: Any) -> bool:
        """Adapt workflow based on intermediate result."""
        # Check if adaptation is needed
        if isinstance(intermediate_result, dict):
            if intermediate_result.get("needs_adaptation"):
                return True
        return False

    def add_step(self, step: Any) -> None:
        """Add a step to the workflow."""
        self.steps.append(step)

    def insert_step(self, index: int, step: Any) -> None:
        """Insert a step at a specific position."""
        self.steps.insert(index, step)

    def remove_step(self, index: int) -> None:
        """Remove a step at a specific position."""
        if 0 <= index < len(self.steps):
            self.steps.pop(index)

    def reorder_steps(self, new_order: list[int]) -> None:
        """Reorder steps according to new order."""
        if len(new_order) == len(self.steps):
            self.steps = [self.steps[i] for i in new_order]
