"""
Agent - Core agent definition with roles, actions, working style, and principles.

Based on docs/core/agent.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class WorkingMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"


class InputType(Enum):
    TEXT = "text"
    CODE = "code"
    FILE = "file"
    MULTI_MODAL = "multi-modal"


class OutputType(Enum):
    TEXT = "text"
    CODE = "code"
    FILE = "file"
    STRUCTURED = "structured"


class FallbackStrategy(Enum):
    ABORT = "abort"
    RETRY = "retry"
    SKIP = "skip"
    ESCALATE = "escalate"


@dataclass
class WorkingStyle:
    """Defines how the agent processes tasks."""
    mode: WorkingMode = WorkingMode.SEQUENTIAL
    input_type: InputType = InputType.TEXT
    output_type: OutputType = OutputType.TEXT
    execution_order: list[str] = field(default_factory=list)
    termination_condition: str | None = None


@dataclass
class Principle:
    """Core operational principles and constraints."""
    core_principles: list[str] = field(default_factory=list)
    priority_order: list[str] = field(default_factory=list)
    max_iterations: int = 10
    max_time_seconds: int = 300
    resource_limit: str | None = None
    fallback_strategy: FallbackStrategy = FallbackStrategy.ABORT


@dataclass
class WorkingAction:
    """Working action configuration."""
    run_cmd: bool = False
    run_shell: bool = False
    run_python_code: bool = False
    run_api_calls: bool = False
    use_tools: list[str] = field(default_factory=list)


@dataclass
class MonitorAction:
    """Monitor action configuration."""
    track_progress: bool = True
    track_resources: bool = True
    track_environment: bool = True
    observe_interval_seconds: int = 5
    on_change: str = "notify"
    on_threshold: str = "alert"


@dataclass
class PlanningAction:
    """Planning action configuration."""
    strategy: str = "sequential"
    goal_decomposition: bool = True
    subtask_generation: bool = True
    dependency_mapping: bool = True
    contingency_planning: bool = True
    replan_on_failure: bool = True
    replan_on_new_info: bool = True


@dataclass
class ReflectingAction:
    """Reflecting action configuration."""
    self_evaluation: bool = True
    outcome_analysis: bool = True
    error_analysis: bool = True
    learn_from_experience: bool = True
    reflect_on_completion: bool = True
    reflect_on_failure: bool = True
    periodic_reflection: bool = False


@dataclass
class IntegratingAction:
    """Integrating action configuration."""
    solve_concept_enabled: bool = True
    solve_methods: list[str] = field(default_factory=lambda: ["decomposition", "analogy"])
    group_concept_enabled: bool = True
    grouping_criteria: list[str] = field(default_factory=lambda: ["semantic"])
    find_first_principle_enabled: bool = True
    find_principle_methods: list[str] = field(default_factory=lambda: ["abstraction"])
    guide_concept_enabled: bool = True


@dataclass
class AbsorbingAction:
    """Absorbing action configuration."""
    thought_storage_enabled: bool = True
    storage_type: str = "semantic"
    update_strategy: str = "merge"
    max_items: int = 1000
    capture_reasoning_chain: bool = True
    capture_decision_points: bool = True
    capture_heuristics: bool = True
    incremental_learning: bool = True


@dataclass
class AbstractingAction:
    """Abstracting action configuration."""
    extract_info_piece: bool = True
    info_granularity: str = "paragraph"
    extract_table_attribute: bool = True
    extract_article_fragment: bool = True
    fragment_types: list[str] = field(default_factory=lambda: ["finding", "method"])
    enable_summary: bool = True
    summary_length: str = "moderate"


@dataclass
class CorrectingAction:
    """Correcting action configuration."""
    detect_syntax_error: bool = True
    detect_logic_error: bool = True
    detect_runtime_error: bool = True
    detect_semantic_error: bool = True
    auto_correct_enabled: bool = True
    fix_syntax: bool = True
    fix_runtime: bool = True
    require_approval: bool = True
    feedback_sources: list[str] = field(default_factory=lambda: ["user", "system"])


@dataclass
class AgentActions:
    """All agent actions."""
    monitor: MonitorAction = field(default_factory=MonitorAction)
    planning: PlanningAction = field(default_factory=PlanningAction)
    reflecting: ReflectingAction = field(default_factory=ReflectingAction)
    integrating: IntegratingAction = field(default_factory=IntegratingAction)
    absorbing: AbsorbingAction = field(default_factory=AbsorbingAction)
    abstracting: AbstractingAction = field(default_factory=AbstractingAction)
    working: WorkingAction = field(default_factory=WorkingAction)
    correcting: CorrectingAction = field(default_factory=CorrectingAction)


# Role configurations

@dataclass
class PlannerRole:
    """Planner role configuration."""
    list_of_plan: list[str] = field(default_factory=list)


@dataclass
class GuiderRole:
    """Guider role configuration."""
    must: list[str] = field(default_factory=list)
    must_not: list[str] = field(default_factory=list)
    concept_to_concern: dict[str, str] = field(default_factory=dict)


@dataclass
class ValueJudgerRole:
    """Value judger role configuration."""
    view_angle: str = "default"
    value_selected_list: list[str] = field(default_factory=list)
    value_list_arrangement: str = "default"


@dataclass
class FactJudgerRole:
    """Fact judger role configuration."""
    related_fact_search: str = ""
    compare_knowledge_base: bool = True
    compare_internet: bool = False
    compare_society_proved: bool = True


@dataclass
class KnowledgeExplainerRole:
    """Knowledge explainer role configuration."""
    target_audience: str = "intermediate"
    depth_level: str = "moderate"
    explanation_style: str = "technical"
    include_examples: bool = True
    include_analogies: bool = True


@dataclass
class LogicCheckerRole:
    """Logic checker role configuration."""
    check_circular_reasoning: bool = True
    check_contradiction: bool = True
    check_missing_premise: bool = True
    check_invalid_inference: bool = True
    check_fallacy: bool = True
    reasoning_framework: str = "deductive"


@dataclass
class RecommenderRole:
    """Recommender role configuration."""
    problem_points: list[str] = field(default_factory=list)
    solutions: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class WorkerRole:
    """Worker role configuration."""
    run_cmd: bool = True
    run_shell: bool = True
    run_python_code: bool = True
    use_tools: list[str] = field(default_factory=list)


@dataclass
class CenterIntegratorRole:
    """Center integrator role configuration."""
    data_holder: bool = True
    message_holder: bool = True
    generated_text_holder: bool = True
    communicate_between_holders: bool = True


@dataclass
class AgentRoles:
    """All agent roles."""
    planner: PlannerRole | None = None
    guider: GuiderRole | None = None
    value_judger: ValueJudgerRole | None = None
    fact_judger: FactJudgerRole | None = None
    knowledge_explainer: KnowledgeExplainerRole | None = None
    logic_checker: LogicCheckerRole | None = None
    recommender: RecommenderRole | None = None
    worker: WorkerRole | None = None
    center_integrator: CenterIntegratorRole | None = None


@dataclass
class AgentConfig:
    """Complete agent configuration."""
    name: str
    description: str = ""
    working_style: WorkingStyle = field(default_factory=WorkingStyle)
    principle: Principle = field(default_factory=Principle)
    actions: AgentActions = field(default_factory=AgentActions)
    roles: AgentRoles = field(default_factory=AgentRoles)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentConfig:
        """Create AgentConfig from dictionary."""
        def _parse_working_style(ws: dict) -> WorkingStyle:
            return WorkingStyle(
                mode=WorkingMode(ws.get("mode", "sequential")),
                input_type=InputType(ws.get("input_type", "text")),
                output_type=OutputType(ws.get("output_type", "text")),
                execution_order=ws.get("execution_order", []),
                termination_condition=ws.get("termination_condition")
            )

        def _parse_principle(p: dict) -> Principle:
            return Principle(
                core_principles=p.get("core_principles", []),
                priority_order=p.get("priority_order", []),
                max_iterations=p.get("constraint", {}).get("max_iterations", 10),
                max_time_seconds=p.get("constraint", {}).get("max_time_seconds", 300),
                resource_limit=p.get("constraint", {}).get("resource_limit"),
                fallback_strategy=FallbackStrategy(p.get("fallback_strategy", "abort"))
            )

        def _parse_roles(r: dict) -> AgentRoles:
            roles = AgentRoles()
            if "planner" in r:
                data = r["planner"]
                roles.planner = PlannerRole(list_of_plan=data.get("list_of_plan", []))
            if "guider" in r:
                data = r["guider"]["rule_set"]
                roles.guider = GuiderRole(
                    must=data.get("must", []),
                    must_not=data.get("must_not", []),
                    concept_to_concern=data.get("concept_to_concern", {})
                )
            if "value_judger" in r:
                data = r["value_judger"]["value"]
                roles.value_judger = ValueJudgerRole(
                    view_angle=data.get("view_angle", "default"),
                    value_selected_list=data.get("value_selected_list", []),
                    value_list_arrangement=data.get("value_list_arrangement", "default")
                )
            if "fact_judger" in r:
                data = r["fact_judger"]["fact"]
                roles.fact_judger = FactJudgerRole(
                    related_fact_search=data.get("related_fact_search", ""),
                    compare_knowledge_base=data.get("compare_user_text", {}).get("knowledge_base", True),
                    compare_internet=data.get("compare_user_text", {}).get("internet", False),
                    compare_society_proved=data.get("compare_with_theory", {}).get("society_proved", True)
                )
            return roles

        return cls(
            name=data["name"],
            description=data.get("description", ""),
            working_style=_parse_working_style(data.get("working_style", {})),
            principle=_parse_principle(data.get("principle", {})),
            roles=_parse_roles(data.get("role", {}))
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "working_style": {
                "mode": self.working_style.mode.value,
                "input_type": self.working_style.input_type.value,
                "output_type": self.working_style.output_type.value,
                "execution_order": self.working_style.execution_order,
                "termination_condition": self.working_style.termination_condition
            },
            "principle": {
                "core_principles": self.principle.core_principles,
                "priority_order": self.principle.priority_order,
                "constraint": {
                    "max_iterations": self.principle.max_iterations,
                    "max_time_seconds": self.principle.max_time_seconds,
                    "resource_limit": self.principle.resource_limit
                },
                "fallback_strategy": self.principle.fallback_strategy.value
            }
        }


class Agent:
    """
    Agent is an autonomous entity configured through JSON that can perceive,
    reason, plan, and act to fulfill user intent.
    """

    def __init__(self, config: AgentConfig | dict[str, Any]):
        if isinstance(config, dict):
            self.config = AgentConfig.from_dict(config)
        else:
            self.config = config

        self.name = self.config.name
        self._initialize_roles()
        self._initialize_actions()

    def _initialize_roles(self) -> None:
        """Initialize role implementations."""
        pass

    def _initialize_actions(self) -> None:
        """Initialize action handlers."""
        pass

    def process(self, input_data: Any, context: dict | None = None) -> Any:
        """
        Process input data and return result.

        Args:
            input_data: The input to process
            context: Optional context dictionary

        Returns:
            Processed result
        """
        raise NotImplementedError("Subclasses must implement process()")

    def run_sync(self, user_input: str) -> str:
        """
        Run agent synchronously with string input.

        Args:
            user_input: String input

        Returns:
            String output
        """
        result = self.process(user_input)
        return str(result) if result is not None else ""

    async def process_async(self, input_data: Any, context: dict | None = None) -> Any:
        """Async version of process."""
        return self.process(input_data, context)

    def __repr__(self) -> str:
        return f"Agent(name={self.name!r})"
