"""
Agent Builder - Agent creation overview.

Based on docs/building/agent-builder.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class BuildMethod(Enum):
    """Method for building agents."""
    LLM_SOURCE = "llm_source"  # Generate code using LLM
    CONFIG_EXISTING = "config_existing"  # Use existing configuration


@dataclass
class PluginStructure:
    """Plugin folder structure for agents."""
    base_path: str = "./plugins/"
    agent_plugins_path: str = "./plugins/agents/"
    tool_plugins_path: str = "./plugins/tools/"
    interface_required: str = "AgentInterface"
    auto_discover: bool = True
    add_allowed: bool = True
    remove_allowed: bool = True
    update_allowed: bool = True


@dataclass
class FunctionalManager:
    """Manager for functional grouping."""
    group_by_category: bool = True
    group_by_capability: bool = True
    group_by_purpose: bool = True
    list_available: bool = True
    enable_disable: bool = True
    configure: bool = True
    monitor: bool = True


@dataclass
class AgentBuilder:
    """
    Agent Builder provides infrastructure for creating and
    configuring agents through factory methods and JSON configuration.
    """
    build_method: BuildMethod = BuildMethod.CONFIG_EXISTING
    plugin_structure: PluginStructure = field(default_factory=PluginStructure)
    functional_manager: FunctionalManager = field(default_factory=FunctionalManager)

    # LLM Build configuration
    coder_input_from_prompt: bool = True
    guider_input_from_md: bool = True

    # Config Build configuration
    delegate_to_classes: bool = True
    shared_api_per_category: bool = True

    def build_from_config(self, config: dict[str, Any]) -> Any:
        """Build agent from configuration."""
        if self.build_method == BuildMethod.LLM_SOURCE:
            return self._build_from_llm(config)
        return self._build_from_existing(config)

    def _build_from_llm(self, config: dict[str, Any]) -> Any:
        """Build agent using LLM code generation."""
        # Placeholder - actual implementation would use LLM
        raise NotImplementedError("LLM-based building not yet implemented")

    def _build_from_existing(self, config: dict[str, Any]) -> Any:
        """Build agent using existing configuration."""
        from ..core.agent import Agent, AgentConfig
        agent_config = AgentConfig.from_dict(config)
        return Agent(agent_config)

    def add_plugin(self, plugin_path: str) -> bool:
        """Add a plugin to the system."""
        if not self.plugin_structure.add_allowed:
            return False
        # Implementation would discover and load plugin
        return True

    def remove_plugin(self, plugin_name: str) -> bool:
        """Remove a plugin from the system."""
        if not self.plugin_structure.remove_allowed:
            return False
        return True

    def list_plugins(self) -> list[str]:
        """List available plugins."""
        return []  # Implementation would scan plugin directory


@dataclass
class ContentWindows:
    """Content window management for agents."""
    up_content_direction: str = "input_to_agent"
    up_content_window_size: int = 4096
    down_content_direction: str = "agent_to_output"
    down_content_window_size: int = 4096

    def configure(
        self,
        up_size: int | None = None,
        down_size: int | None = None
    ) -> None:
        """Configure window sizes."""
        if up_size is not None:
            self.up_content_window_size = up_size
        if down_size is not None:
            self.down_content_window_size = down_size
