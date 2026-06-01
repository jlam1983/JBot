# Interaction Plan

## Overview

A visual canvas interface for designing agent interactions using a node-based GUI.

---

## Canvas Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  Toolbar                                                          │
│  [+ Node] [+ Template] [Connect] [Zoom] [Fit] [Export]           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│         ┌─────────┐                    ┌─────────┐             │
│         │ Planner │─────────────────────│ Guider  │             │
│         │  Node   │                     │  Node   │             │
│         └────┬────┘                     └────┬────┘             │
│              │                               │                    │
│              │         ┌─────────┐           │                    │
│              └─────────│ Worker  │───────────┘                    │
│                        │  Node   │                               │
│                        └────┬────┘                               │
│                             ▼                                      │
│                       ┌─────────┐                                │
│                       │ Output  │                                │
│                       └─────────┘                                │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│  Properties Panel (shown when node selected)                     │
│  [Name] [Type ▼] [Config {...}] [Apply] [Delete] [Duplicate]    │
└─────────────────────────────────────────────────────────────────┘
```

### Canvas Controls

| Action | Control |
|--------|---------|
| **Pan** | Click + drag on empty area |
| **Zoom** | Mouse wheel (50%-200%) |
| **Select** | Click on node |
| **Multi-select** | Ctrl+Click or drag box |
| **Connect** | Drag output port to input port |
| **Delete** | Select + Delete key |

---

## Node Types

### 1. Agent Node
```json
"agent_node": {
  "visual": {"shape": "rounded_rectangle", "color": "#4A90D9"},
  "properties": {
    "name": "string",
    "agent_type": "planner | guider | worker | judger | ...",
    "agent_config": "json_config"
  }
}
```

### 2. Interaction Node
```json
"interaction_node": {
  "visual": {"shape": "diamond", "color": "#7B68EE"},
  "properties": {
    "interaction_type": "sequential | group_discuss | workflow_suggestion"
  }
}
```

### 3. Template Node
```json
"template_node": {
  "visual": {"shape": "rectangle", "color": "#50C878"},
  "properties": {
    "template_id": "string",
    "parameters": {...}
  }
}
```

### 4. Data Node
```json
"data_node": {
  "visual": {"shape": "parallelogram", "color": "#FF6B6B"},
  "properties": {
    "data_type": "input | output | storage"
  }
}
```

### 5. Condition Node
```json
"condition_node": {
  "visual": {"shape": "hexagon", "color": "#FFB347"},
  "properties": {
    "condition": "expression",
    "true_branch": "node_id",
    "false_branch": "node_id"
  }
}
```

---

## CRUD Operations

### Create
1. Click `[+ Node]` in toolbar
2. Select node type
3. Node appears at canvas center
4. Popup editor opens for configuration

### Read
- Click node to select → Properties panel shows details
- Double-click to open full popup editor

### Update
1. Select node
2. Edit properties in popup
3. Click `Apply` to save

### Delete
1. Select node(s)
2. Press `Delete` key
3. Node and connections are removed

---

## Template Library

- **Save as Template**: Right-click → "Save as Template"
- **Load Template**: Click `[+ Template]` → Browse library
- **Includes**: Sequential Pipeline, Group Discuss, Research Agent patterns

---

## Interaction Patterns on Canvas

| Pattern | Diagram |
|---------|---------|
| **Sequential** | `[A] ──► [B] ──► [C]` |
| **Parallel** | `[A] ──┼──► [B]` <br> `└──► [C]` |
| **Group Discuss** | `[Moderator]` <br> `/  │  \` <br> `[A] [B] [C]` |
| **Conditional** | `[A] ──► [B] ──► [D]` <br> ` └──► [C]` |
