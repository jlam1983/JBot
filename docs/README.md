# JLLMBot Documentation

## Overview

JLLMBot is an intelligent agent system that enables dynamic generation, management, and orchestration of AI agents. The system provides a complete framework for building agents with configurable roles, actions, and interaction patterns.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        JLLMBot System                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      Display Layer                       │   │
│  │  Interaction Plan │ Deployment Pool │ Mindset Modifier  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Interaction Layer                     │   │
│  │     Sequential │ Group Discuss │ Workflow Suggestion     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      Core Layer                          │   │
│  │     Agent │ Context │ Job Types │ Summary Storage       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Building Layer                        │   │
│  │     Factory Methods │ Config Delegation │ Tool Builder  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Documentation Structure

### [Core Concepts](./core/README.md)

The fundamental building blocks of the agent system.

| Document | Description |
|----------|-------------|
| [Agent](./core/agent.md) | Agent definition, roles, and actions |
| [Context](./core/context.md) | Session memory and state management |
| [Job Types](./core/job-types.md) | Work types and intent-goal transformation |
| [Summary Storage](./core/summary-storage.md) | Long-term knowledge accumulation |

### [Agent Building](./building/README.md)

How to create and configure agents.

| Document | Description |
|----------|-------------|
| [Agent Builder](./building/agent-builder.md) | Agent creation overview |
| [Factory Methods](./building/factory-methods.md) | LLM-based code generation |
| [Config Delegation](./building/config-delegation.md) | JSON config to class mapping |
| [Tool Builder](./building/tool-builder.md) | Tool creation and management |

### [Interaction Patterns](./interaction/README.md)

How agents collaborate and communicate.

| Document | Description |
|----------|-------------|
| [Interaction Overview](./interaction/interaction-overview.md) | Interaction types and patterns |
| [Sequential](./interaction/sequential-interaction.md) | One-by-one chain processing |
| [Group Discuss](./interaction/group-discuss.md) | Multi-agent collaboration |
| [Workflow Suggestion](./interaction/workflow-suggestion.md) | Dynamic workflow optimization |

### [Display System](./display/README.md)

Visual interfaces for managing agents.

| Document | Description |
|----------|-------------|
| [Display Overview](./display/display-overview.md) | Display system architecture |
| [Interaction Plan](./display/interaction-plan.md) | Node-based visual canvas |
| [Deployment Pool](./display/deployment-pool.md) | Agent deployment management |
| [Mindset Modifier](./display/mindset-modifier.md) | Agent thinking visualization |

---

## Key Concepts

### Intent → Goal → Action

```
User Intent (Abstract Purpose)
         │
         ▼
    Interpretation
         │
         ▼
    Goals (Situational Steps)
         │
         ▼
    Agent Roles & Actions
         │
         ▼
    Execution
```

### Agent Structure

```
Agent
├── Working Style (sequential | parallel | hybrid)
├── Principle (core principles, constraints, fallback)
├── Roles (planner, guider, judger, worker, etc.)
└── Actions (monitor, planning, reflecting, integrating, etc.)
```

### Interaction Patterns

1. **Sequential**: One agent's output feeds the next
2. **Group Discuss**: Multiple agents collaborate with roles (moderator, synthesizer)
3. **Workflow Suggestion**: Dynamic optimization with value-added suggestions

---

## Getting Started

1. **Understand Core Concepts**: Start with [Agent](./core/agent.md) to understand what agents are
2. **Learn Job Types**: Read [Job Types](./core/job-types.md) to understand how work is structured
3. **Explore Interaction**: See [Interaction Overview](./interaction/interaction-overview.md) for collaboration patterns
4. **Use the Display**: Try the [Interaction Plan](./display/interaction-plan.md) canvas to design workflows

---

## Related Documentation

- [Agent JSON Schema](./core/agent-json.md) - Detailed JSON configuration reference
