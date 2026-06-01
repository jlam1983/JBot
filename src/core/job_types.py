"""
Job Types - Work types and intent-goal transformation.

Based on docs/core/job-types.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class JobType(Enum):
    """Job types for agent work."""
    CONTENT_GENERATION = "content_generation"
    RESEARCH_DISCUSS = "research_discuss"
    WORKFLOW_RUNNER = "workflow_runner"
    PROBLEM_SOLVING = "problem_solving"
    PLANNING = "planning"


@dataclass
class Intent:
    """User intent - abstract high-level purpose."""
    raw_input: str
    interpreted_purpose: str = ""
    implied_needs: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)

    def interpret(self) -> Intent:
        """Interpret the raw input to extract purpose."""
        self.interpreted_purpose = self.raw_input
        return self

    def add_constraint(self, constraint: str) -> None:
        """Add a constraint."""
        if constraint not in self.constraints:
            self.constraints.append(constraint)

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_input": self.raw_input,
            "interpreted_purpose": self.interpreted_purpose,
            "implied_needs": self.implied_needs,
            "constraints": self.constraints
        }


@dataclass
class Goal:
    """Goal - concrete situational implementation step."""
    goal_id: str
    description: str
    dependencies: list[str] = field(default_factory=list)
    priority: int = 0
    completed: bool = False

    def is_blocked(self, completed_goals: set[str]) -> bool:
        """Check if goal is blocked by incomplete dependencies."""
        return any(dep not in completed_goals for dep in self.dependencies)

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal_id": self.goal_id,
            "description": self.description,
            "dependencies": self.dependencies,
            "priority": self.priority,
            "completed": self.completed
        }


@dataclass
class ProgressTracking:
    """Track progress of job execution."""
    current_phase: str = ""
    completed_goals: list[str] = field(default_factory=list)
    pending_goals: list[str] = field(default_factory=list)
    blocked_goals: list[str] = field(default_factory=list)

    def mark_complete(self, goal_id: str) -> None:
        """Mark a goal as complete."""
        if goal_id in self.pending_goals:
            self.pending_goals.remove(goal_id)
        if goal_id not in self.completed_goals:
            self.completed_goals.append(goal_id)

    def mark_blocked(self, goal_id: str) -> None:
        """Mark a goal as blocked."""
        if goal_id in self.pending_goals:
            self.pending_goals.remove(goal_id)
        if goal_id not in self.blocked_goals:
            self.blocked_goals.append(goal_id)

    def get_completion_percentage(self) -> float:
        """Get completion percentage."""
        total = len(self.completed_goals) + len(self.pending_goals) + len(self.blocked_goals)
        if total == 0:
            return 0.0
        return len(self.completed_goals) / total


@dataclass
class Requirement:
    """Requirement for action."""
    name: str
    satisfied: bool = False

    def satisfy(self) -> None:
        self.satisfied = True

    def unsatisfy(self) -> None:
        self.satisfied = False


@dataclass
class Job:
    """
    Job is a fundamental unit of work that agents execute
    to fulfill user intent.
    """
    job_type: JobType
    intent: Intent
    goals: list[Goal] = field(default_factory=list)
    progress: ProgressTracking = field(default_factory=ProgressTracking)
    requirements: list[Requirement] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        job_type: JobType,
        raw_input: str,
        interpret: bool = True
    ) -> Job:
        """Create a new job."""
        intent = Intent(raw_input=raw_input)
        if interpret:
            intent.interpret()
        return cls(job_type=job_type, intent=intent)

    def add_goal(self, goal: Goal) -> None:
        """Add a goal to the job."""
        self.goals.append(goal)
        self.progress.pending_goals.append(goal.goal_id)

    def decompose_goals(self, sub_goals: list[str]) -> None:
        """Break down goals into sub-goals."""
        for i, sub in enumerate(sub_goals):
            goal = Goal(
                goal_id=f"{self.progress.current_phase}_sub_{i}",
                description=sub,
                priority=i
            )
            self.add_goal(goal)

    def prioritize_goals(self) -> list[Goal]:
        """Sort goals by priority."""
        return sorted(self.goals, key=lambda g: g.priority)

    def get_next_ready_goal(self) -> Goal | None:
        """Get the next goal that is ready to execute."""
        completed = set(self.progress.completed_goals)
        for goal in self.prioritize_goals():
            if not goal.completed and not goal.is_blocked(completed):
                return goal
        return None

    def is_complete(self) -> bool:
        """Check if all goals are complete."""
        return all(goal.completed for goal in self.goals)

    def validate_intent(self) -> bool:
        """Validate that intent has been fulfilled."""
        return self.is_complete()


# Intent to Goal Transformation

@dataclass
class IntentToGoalTransformer:
    """Transforms user intent into goals."""
    clarify_ambiguity: bool = True
    identify_constraints: bool = True
    extract_implicit_needs: bool = True
    break_into_sub_goals: bool = True
    identify_dependencies: bool = True
    prioritize_by_importance: bool = True

    def transform(self, intent: Intent) -> list[Goal]:
        """Transform intent into goals."""
        goals = []

        # Extract implicit needs
        if self.extract_implicit_needs:
            for need in intent.implied_needs:
                goals.append(Goal(
                    goal_id=f"address_{len(goals)}",
                    description=f"Address need: {need}",
                    priority=len(goals)
                ))

        # Add main purpose as a goal
        goals.append(Goal(
            goal_id="main_purpose",
            description=intent.interpreted_purpose or intent.raw_input,
            priority=0
        ))

        # Add constraint handling goals
        if self.identify_constraints:
            for i, constraint in enumerate(intent.constraints):
                goals.append(Goal(
                    goal_id=f"constraint_{i}",
                    description=f"Handle constraint: {constraint}",
                    priority=len(goals)
                ))

        return goals


# Advanced Suggestions

@dataclass
class Suggestion:
    """Suggestion for workflow improvement."""
    suggestion_type: str
    description: str
    reasoning: str = ""
    accepted: bool | None = None

    def accept(self) -> None:
        self.accepted = True

    def reject(self) -> None:
        self.accepted = False


@dataclass
class AdvancedSuggestions:
    """Advanced suggestions based on abstract intent."""
    enabled: bool = True
    suggest_process_improvement: bool = True
    suggest_scope_expansion: bool = True
    suggest_risk_alerts: bool = True
    suggest_alternatives: bool = True

    def generate(
        self,
        intent: Intent,
        current_goals: list[Goal]
    ) -> list[Suggestion]:
        """Generate suggestions based on intent and current goals."""
        suggestions = []
        if not self.enabled:
            return suggestions

        if self.suggest_process_improvement:
            suggestions.append(Suggestion(
                suggestion_type="process_improvement",
                description="Consider parallel execution where possible",
                reasoning="Parallel execution can reduce overall time"
            ))

        if self.suggest_scope_expansion:
            suggestions.append(Suggestion(
                suggestion_type="scope_expansion",
                description="You might also want to consider error handling",
                reasoning="Adding error handling improves robustness"
            ))

        return suggestions
