"""
Tool Builder - Tool creation and management.

Based on docs/building/tool-builder.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ToolCategory(Enum):
    """Tool categories."""
    FILE_TOOLS = "file_tools"
    CODE_TOOLS = "code_tools"
    WEB_TOOLS = "web_tools"
    DATA_TOOLS = "data_tools"


@dataclass
class ToolInterface:
    """Interface that all tools must implement."""
    name: str
    category: ToolCategory
    execute_method: str = "execute"
    validate_method: str = "validate"


@dataclass
class Tool:
    """
    A functional unit that extends agent capabilities.
    """
    name: str
    description: str = ""
    category: ToolCategory = ToolCategory.DATA_TOOLS
    enabled: bool = True
    config: dict[str, Any] = field(default_factory=dict)

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the tool."""
        raise NotImplementedError(f"Tool {self.name} must implement execute()")

    def validate(self, *args: Any, **kwargs: Any) -> bool:
        """Validate tool input."""
        return True


@dataclass
class FileTool(Tool):
    """Tool for file operations."""

    def __init__(self, name: str = "file_tool"):
        super().__init__(
            name=name,
            category=ToolCategory.FILE_TOOLS,
            description="Tool for file operations"
        )


@dataclass
class CodeTool(Tool):
    """Tool for code execution."""

    def __init__(self, name: str = "code_tool"):
        super().__init__(
            name=name,
            category=ToolCategory.CODE_TOOLS,
            description="Tool for code execution"
        )


@dataclass
class WebTool(Tool):
    """Tool for web requests."""

    def __init__(self, name: str = "web_tool"):
        super().__init__(
            name=name,
            category=ToolCategory.WEB_TOOLS,
            description="Tool for web requests"
        )


@dataclass
class ToolBuilder:
    """
    Tool Builder creates functional units that extend agent capabilities.
    """
    category_grouping_enabled: bool = True
    shared_interface_enabled: bool = True
    tool_pool_enabled: bool = True

    def build_from_llm(
        self,
        user_description: str,
        md_rules: list[str] | None = None
    ) -> Tool:
        """
        Build tool using LLM from user description.

        Args:
            user_description: Natural language description of desired tool
            md_rules: Optional rules from md files

        Returns:
            Generated Tool instance
        """
        # In production, would use LLM to generate tool code
        raise NotImplementedError("LLM tool building requires LLM integration")

    def build_from_config(self, config: dict[str, Any]) -> Tool:
        """Build tool from configuration."""
        return Tool(
            name=config.get("name", "unnamed_tool"),
            description=config.get("description", ""),
            category=ToolCategory(config.get("category", "data_tools")),
            enabled=config.get("enabled", True),
            config=config.get("config", {})
        )

    def register_tool(self, tool: Tool) -> bool:
        """Register tool in the system."""
        if not self.tool_pool_enabled:
            return False
        return True

    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister tool from the system."""
        return True

    def list_tools(
        self,
        category: ToolCategory | None = None,
        enabled_only: bool = True
    ) -> list[str]:
        """List available tools."""
        return []


@dataclass
class ToolPool:
    """
    Pool for managing registered tools.
    """
    tools: dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        """Register a tool."""
        self.tools[tool.name] = tool

    def unregister(self, tool_name: str) -> bool:
        """Unregister a tool."""
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False

    def get(self, tool_name: str) -> Tool | None:
        """Get a tool by name."""
        return self.tools.get(tool_name)

    def list_by_category(self, category: ToolCategory) -> list[Tool]:
        """List tools by category."""
        return [t for t in self.tools.values() if t.category == category]

    def list_all(self, enabled_only: bool = True) -> list[str]:
        """List all tool names."""
        if enabled_only:
            return [t.name for t in self.tools.values() if t.enabled]
        return list(self.tools.keys())
