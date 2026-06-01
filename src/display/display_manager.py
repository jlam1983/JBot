"""
Display Manager - Display system architecture.

Based on docs/display/display-overview.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DisplayArea(Enum):
    """Display areas in the system."""
    INTERACTION_PLAN = "interaction_plan"
    DEPLOYMENT_POOL = "deployment_pool"
    MINDSET_MODIFIER = "mindset_modifier"


@dataclass
class DisplayManager:
    """
    Manages visual interfaces for managing agents, interactions,
    and deployments.
    """
    current_area: DisplayArea = DisplayArea.INTERACTION_PLAN
    areas: dict[DisplayArea, bool] = field(default_factory=lambda: {
        DisplayArea.INTERACTION_PLAN: True,
        DisplayArea.DEPLOYMENT_POOL: True,
        DisplayArea.MINDSET_MODIFIER: True
    })

    def switch_to(self, area: DisplayArea) -> None:
        """Switch to a different display area."""
        if area in self.areas and self.areas[area]:
            self.current_area = area

    def get_current_area(self) -> DisplayArea:
        """Get the currently active display area."""
        return self.current_area

    def list_available_areas(self) -> list[DisplayArea]:
        """List all available display areas."""
        return [area for area, available in self.areas.items() if available]

    def enable_area(self, area: DisplayArea) -> None:
        """Enable a display area."""
        self.areas[area] = True

    def disable_area(self, area: DisplayArea) -> None:
        """Disable a display area."""
        self.areas[area] = False
