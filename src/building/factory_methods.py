"""
Factory Methods - LLM-based and Config-based agent instantiation.

Based on docs/building/factory-methods.md
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class FactoryMethod(ABC):
    """Base class for factory methods."""

    @abstractmethod
    def create(self, config: dict[str, Any]) -> Any:
        """Create an instance."""
        pass


@dataclass
class LLMFactoryInput:
    """Input sources for LLM factory."""
    user_prompt: str = ""
    md_rules: list[str] = field(default_factory=list)


@dataclass
class LLMFactory(FactoryMethod):
    """
    Generates agent/tool code using LLM based on user input and rules.
    """
    coder_enabled: bool = True
    guider_enabled: bool = True

    def set_coder_input(self, prompt: str) -> LLMFactory:
        """Set coder input."""
        return self

    def set_guider_input(self, md_files: list[str]) -> LLMFactory:
        """Set guider input from md files."""
        return self

    def create(self, config: dict[str, Any]) -> Any:
        """
        Generate and return agent code.

        In production, this would:
        1. Take user prompt and md rules
        2. Call LLM to generate code
        3. Validate generated code
        4. Return executable code
        """
        raise NotImplementedError("LLM factory requires LLM integration")

    def deploy_to_pool(self, code: Any, pool_type: str = "agent") -> bool:
        """Deploy generated code to pool."""
        # Placeholder for deployment
        return True


@dataclass
class CodeGenerationResult:
    """Result of code generation."""
    code: str
    validation_passed: bool = False
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ConfigFactory(FactoryMethod):
    """
    Delegates configuration to existing class implementations.
    """
    shared_api_enabled: bool = True

    def create(self, config: dict[str, Any]) -> Any:
        """Create agent from JSON config."""
        from ..core.agent import Agent, AgentConfig

        agent_config = AgentConfig.from_dict(config)
        return Agent(agent_config)

    def map_roles_to_classes(self, role_config: dict[str, Any]) -> dict[str, Any]:
        """Map role configurations to class implementations."""
        mapping = {
            "planner": "PlannerImpl",
            "guider": "GuiderImpl",
            "value_judger": "ValueJudgerImpl",
            "fact_judger": "FactJudgerImpl",
            "knowledge_explainer": "KnowledgeExplainerImpl",
            "logic_checker": "LogicCheckerImpl",
            "recommender": "RecommenderImpl",
            "worker": "WorkerImpl",
            "center_integrator": "CenterIntegratorImpl"
        }
        return mapping


@dataclass
class SharedAPI:
    """Shared API pattern for code organization by category."""

    @dataclass
    class CategoryAPI:
        interface: str
        implementations: list[str]
        shared_methods: list[str]

    categories: dict[str, CategoryAPI] = field(default_factory=dict)

    def register_category(
        self,
        name: str,
        interface: str,
        implementations: list[str],
        shared_methods: list[str]
    ) -> None:
        """Register a category with shared API."""
        self.categories[name] = self.CategoryAPI(
            interface=interface,
            implementations=implementations,
            shared_methods=shared_methods
        )

    def get_category(self, name: str) -> CategoryAPI | None:
        """Get category API."""
        return self.categories.get(name)

    def list_categories(self) -> list[str]:
        """List all registered categories."""
        return list(self.categories.keys())


@dataclass
class CodeDeployment:
    """Code deployment to pool."""
    target_pool: str = "agent_pool"
    validate: bool = True
    package: bool = True
    register: bool = True
    activate: bool = True

    def deploy(self, code: Any) -> bool:
        """Deploy code to target pool."""
        if self.validate and not self._validate_code(code):
            return False
        if self.package:
            code = self._package_code(code)
        if self.register:
            self._register_code(code)
        if self.activate:
            self._activate_code(code)
        return True

    def _validate_code(self, code: Any) -> bool:
        """Validate code integrity."""
        return True

    def _package_code(self, code: Any) -> Any:
        """Package code for deployment."""
        return code

    def _register_code(self, code: Any) -> None:
        """Register code in pool."""
        pass

    def _activate_code(self, code: Any) -> None:
        """Activate code for use."""
        pass
