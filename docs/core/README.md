# Core Concepts

This section contains the fundamental building blocks of the JLLMBot agent system.

## Documents

| Document | Description |
|----------|-------------|
| [Agent](./agent.md) | Agent definition with roles, actions, working style, and principles |
| [Agent JSON](./agent-json.md) | Complete JSON configuration schema |
| [Context](./context.md) | Session memory, state management, and agent threading |
| [Job Types](./job-types.md) | Work types and intent-goal transformation |
| [Summary Storage](./summary-storage.md) | Long-term knowledge accumulation and refinement |

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Agent                                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │Working Style │  │  Principle  │  │   Context   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────────────────────────────────────────┐       │
│  │                     Roles                        │       │
│  │  Planner │ Guider │ Judgers │ Worker │ etc.      │       │
│  └─────────────────────────────────────────────────┘       │
│  ┌─────────────────────────────────────────────────┐       │
│  │                    Actions                        │       │
│  │  Monitor │ Planning │ Integrating │ Working     │       │
│  └─────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## Concepts Map

- **Agent** defines WHAT the entity is and WHAT it can do
- **Context** defines WHERE the agent operates (session state)
- **Job Types** defines WHY the agent works (user intent fulfillment)
- **Summary Storage** defines HOW knowledge persists across sessions
