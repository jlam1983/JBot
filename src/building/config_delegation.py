"""
Config Delegation - JSON config to class mapping.

Based on docs/building/config-delegation.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Type


@dataclass
class ClassMapping:
    """Maps configuration keys to class implementations."""
    config_key: str
    class_name: str
    init_from_config: list[str] = field(default_factory=list)


@dataclass
class RoleDelegation:
    """Role to class delegation mapping."""

    @dataclass
    class RoleMapping:
        class_path: str
        config_keys: list[str]

    planner: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.PlannerRole",
            config_keys=["list_of_plan"]
        )
    )
    guider: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.GuiderRole",
            config_keys=["rule_set"]
        )
    )
    value_judger: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.ValueJudgerRole",
            config_keys=["value"]
        )
    )
    fact_judger: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.FactJudgerRole",
            config_keys=["fact"]
        )
    )
    knowledge_explainer: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.KnowledgeExplainerRole",
            config_keys=["explain"]
        )
    )
    logic_checker: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.LogicCheckerRole",
            config_keys=["logic"]
        )
    )
    recommender: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.RecommenderRole",
            config_keys=["suggestion"]
        )
    )
    worker: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.WorkerRole",
            config_keys=["do_the_work"]
        )
    )
    center_integrator: RoleMapping = field(
        default_factory=lambda: RoleMapping(
            class_path="core.agent.CenterIntegratorRole",
            config_keys=["data_holder", "message_holder"]
        )
    )

    def get_mapping(self, role_name: str) -> RoleMapping | None:
        """Get mapping for a role."""
        return getattr(self, role_name, None)


@dataclass
class ActionDelegation:
    """Action to handler delegation mapping."""

    @dataclass
    class ActionMapping:
        handler_path: str
        config_keys: list[str]

    monitor: ActionMapping = field(
        default_factory=lambda: ActionMapping(
            handler_path="core.agent.MonitorAction",
            config_keys=["observe", "triggers"]
        )
    )
    planning: ActionMapping = field(
        default_factory=lambda: ActionMapping(
            handler_path="core.agent.PlanningAction",
            config_keys=["plan", "replanning"]
        )
    )
    reflecting: ActionMapping = field(
        default_factory=lambda: ActionMapping(
            handler_path="core.agent.ReflectingAction",
            config_keys=["self_evaluation", "outcome_analysis"]
        )
    )
    integrating: ActionMapping = field(
        default_factory=lambda: ActionMapping(
            handler_path="core.agent.IntegratingAction",
            config_keys=["solve_concept", "group_concept"]
        )
    )
    absorbing: ActionMapping = field(
        default_factory=lambda: ActionMapping(
            handler_path="core.agent.AbsorbingAction",
            config_keys=["thought_storage", "thinking_experience"]
        )
    )
    abstracting: ActionMapping = field(
        default_factory=lambda: ActionMapping(
            handler_path="core.agent.AbstractingAction",
            config_keys=["extraction", "summarization"]
        )
    )
    working: ActionMapping = field(
        default_factory=lambda: ActionMapping(
            handler_path="core.agent.WorkingAction",
            config_keys=["execution", "sandbox", "error_handling"]
        )
    )
    correcting: ActionMapping = field(
        default_factory=lambda: ActionMapping(
            handler_path="core.agent.CorrectingAction",
            config_keys=["error_detection", "auto_correction"]
        )
    )

    def get_mapping(self, action_name: str) -> ActionMapping | None:
        """Get mapping for an action."""
        return getattr(self, action_name, None)


@dataclass
class ConfigDelegator:
    """
    Maps JSON configuration to class implementations.
    Enables declarative agent configuration.
    """
    role_delegation: RoleDelegation = field(default_factory=RoleDelegation)
    action_delegation: ActionDelegation = field(default_factory=ActionDelegation)

    def parse_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Parse and validate configuration."""
        parsed = {
            "name": config.get("name", ""),
            "description": config.get("description", ""),
            "roles": {},
            "actions": {}
        }

        # Parse roles
        if "role" in config:
            for role_name, role_config in config["role"].items():
                mapping = self.role_delegation.get_mapping(role_name)
                if mapping:
                    parsed["roles"][role_name] = self._extract_role_data(
                        role_name, role_config, mapping
                    )

        # Parse actions
        if "action" in config:
            for action_name, action_config in config["action"].items():
                mapping = self.action_delegation.get_mapping(action_name)
                if mapping:
                    parsed["actions"][action_name] = self._extract_action_data(
                        action_name, action_config, mapping
                    )

        return parsed

    def _extract_role_data(
        self,
        role_name: str,
        role_config: dict[str, Any],
        mapping: RoleDelegation.RoleMapping
    ) -> dict[str, Any]:
        """Extract role configuration data."""
        extracted = {}
        for key in mapping.config_keys:
            if key in role_config:
                extracted[key] = role_config[key]
        return extracted

    def _extract_action_data(
        self,
        action_name: str,
        action_config: dict[str, Any],
        mapping: ActionDelegation.ActionMapping
    ) -> dict[str, Any]:
        """Extract action configuration data."""
        extracted = {}
        for key in mapping.config_keys:
            if key in action_config:
                extracted[key] = action_config[key]
        return extracted

    def instantiate_role(
        self,
        role_name: str,
        role_data: dict[str, Any]
    ) -> Any:
        """Instantiate a role class from configuration."""
        mapping = self.role_delegation.get_mapping(role_name)
        if not mapping:
            return None

        # In production, would dynamically instantiate the class
        return role_data

    def instantiate_action(
        self,
        action_name: str,
        action_data: dict[str, Any]
    ) -> Any:
        """Instantiate an action handler from configuration."""
        mapping = self.action_delegation.get_mapping(action_name)
        if not mapping:
            return None

        # In production, would dynamically instantiate the class
        return action_data


@dataclass
class PluginDelegation:
    """Plugin integration for dynamic loading."""
    interface_required: str = "AgentInterface"
    scan_folders: list[str] = field(default_factory=lambda: ["./plugins/agents"])
    auto_discover: bool = True
    on_demand_load: bool = True

    def discover_plugins(self) -> list[str]:
        """Discover available plugins."""
        return []

    def load_plugin(self, plugin_name: str) -> Any:
        """Load a plugin by name."""
        raise NotImplementedError("Plugin loading requires implementation")

    def register_plugin(
        self,
        name: str,
        plugin_class: Type,
        config_schema: dict[str, Any] | None = None
    ) -> None:
        """Register a plugin manually."""
        pass

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin."""
        return True
