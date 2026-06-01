"""
Interaction Plan - Node-based visual canvas.

Based on docs/display/interaction-plan.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class NodeType(Enum):
    """Types of nodes on the canvas."""
    AGENT = "agent"
    INTERACTION = "interaction"
    TEMPLATE = "template"
    DATA = "data"
    CONDITION = "condition"


@dataclass
class NodePort:
    """Input or output port on a node."""
    name: str
    port_type: str = "any"


@dataclass
class Node:
    """
    A node on the interaction canvas.
    """
    node_id: str
    node_type: NodeType
    name: str
    config: dict[str, Any] = field(default_factory=dict)
    position_x: float = 0
    position_y: float = 0
    inputs: list[NodePort] = field(default_factory=list)
    outputs: list[NodePort] = field(default_factory=list)

    def add_input(self, port_name: str, port_type: str = "any") -> None:
        """Add an input port."""
        self.inputs.append(NodePort(name=port_name, port_type=port_type))

    def add_output(self, port_name: str, port_type: str = "any") -> None:
        """Add an output port."""
        self.outputs.append(NodePort(name=port_name, port_type=port_type))

    def get_config(self) -> dict[str, Any]:
        """Get node configuration."""
        return self.config

    def set_config(self, config: dict[str, Any]) -> None:
        """Set node configuration."""
        self.config = config


@dataclass
class Connection:
    """A connection between two nodes."""
    connection_id: str
    source_node_id: str
    source_port: str
    target_node_id: str
    target_port: str


@dataclass
class Canvas:
    """
    The canvas for designing agent interactions.
    """
    canvas_id: str = "default"
    nodes: dict[str, Node] = field(default_factory=dict)
    connections: dict[str, Connection] = field(default_factory=dict)
    zoom_level: float = 1.0

    def add_node(self, node: Node) -> None:
        """Add a node to the canvas."""
        self.nodes[node.node_id] = node

    def remove_node(self, node_id: str) -> bool:
        """Remove a node and its connections."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            # Remove related connections
            to_remove = [
                cid for cid, conn in self.connections.items()
                if conn.source_node_id == node_id or conn.target_node_id == node_id
            ]
            for cid in to_remove:
                del self.connections[cid]
            return True
        return False

    def get_node(self, node_id: str) -> Node | None:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def add_connection(
        self,
        connection_id: str,
        source_id: str,
        source_port: str,
        target_id: str,
        target_port: str
    ) -> bool:
        """Add a connection between nodes."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return False

        connection = Connection(
            connection_id=connection_id,
            source_node_id=source_id,
            source_port=source_port,
            target_node_id=target_id,
            target_port=target_port
        )
        self.connections[connection_id] = connection
        return True

    def remove_connection(self, connection_id: str) -> bool:
        """Remove a connection."""
        if connection_id in self.connections:
            del self.connections[connection_id]
            return True
        return False

    def set_zoom(self, zoom: float) -> None:
        """Set zoom level (0.5 to 2.0)."""
        self.zoom_level = max(0.5, min(2.0, zoom))

    def to_dict(self) -> dict[str, Any]:
        """Export canvas to dictionary."""
        return {
            "canvas_id": self.canvas_id,
            "nodes": {nid: n.__dict__ for nid, n in self.nodes.items()},
            "connections": {cid: c.__dict__ for cid, c in self.connections.items()},
            "zoom_level": self.zoom_level
        }


@dataclass
class InteractionPlan:
    """
    Visual canvas for designing agent interactions.
    """
    name: str = "Interaction Plan"
    canvas: Canvas = field(default_factory=Canvas)

    def create_agent_node(
        self,
        node_id: str,
        name: str,
        agent_type: str,
        position: tuple[float, float] = (0, 0)
    ) -> Node:
        """Create an agent node."""
        node = Node(
            node_id=node_id,
            node_type=NodeType.AGENT,
            name=name,
            config={"agent_type": agent_type},
            position_x=position[0],
            position_y=position[1]
        )
        node.add_input("input")
        node.add_output("output")
        self.canvas.add_node(node)
        return node

    def create_interaction_node(
        self,
        node_id: str,
        name: str,
        interaction_type: str,
        position: tuple[float, float] = (0, 0)
    ) -> Node:
        """Create an interaction node."""
        node = Node(
            node_id=node_id,
            node_type=NodeType.INTERACTION,
            name=name,
            config={"interaction_type": interaction_type},
            position_x=position[0],
            position_y=position[1]
        )
        node.add_input("trigger")
        node.add_input("data_in")
        node.add_output("data_out")
        node.add_output("result")
        self.canvas.add_node(node)
        return node

    def create_template_node(
        self,
        node_id: str,
        template_id: str,
        position: tuple[float, float] = (0, 0)
    ) -> Node:
        """Create a template node."""
        node = Node(
            node_id=node_id,
            node_type=NodeType.TEMPLATE,
            name=f"Template: {template_id}",
            config={"template_id": template_id},
            position_x=position[0],
            position_y=position[1]
        )
        self.canvas.add_node(node)
        return node

    def update_node_config(self, node_id: str, config: dict[str, Any]) -> bool:
        """Update node configuration."""
        node = self.canvas.get_node(node_id)
        if node:
            node.set_config(config)
            return True
        return False

    def delete_node(self, node_id: str) -> bool:
        """Delete a node."""
        return self.canvas.remove_node(node_id)

    def connect_nodes(
        self,
        connection_id: str,
        source_id: str,
        source_port: str,
        target_id: str,
        target_port: str
    ) -> bool:
        """Connect two nodes."""
        return self.canvas.add_connection(
            connection_id, source_id, source_port, target_id, target_port
        )


@dataclass
class TemplateLibrary:
    """Library of reusable templates."""
    templates: dict[str, dict[str, Any]] = field(default_factory=dict)

    def save_template(self, name: str, template_data: dict[str, Any]) -> None:
        """Save a template."""
        self.templates[name] = template_data

    def load_template(self, name: str) -> dict[str, Any] | None:
        """Load a template."""
        return self.templates.get(name)

    def list_templates(self) -> list[str]:
        """List all templates."""
        return list(self.templates.keys())

    def delete_template(self, name: str) -> bool:
        """Delete a template."""
        if name in self.templates:
            del self.templates[name]
            return True
        return False
