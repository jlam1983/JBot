# Agent Building

This section covers how agents are created, configured, and managed.

## Documents

| Document | Description |
|----------|-------------|
| [Agent Builder](./agent-builder.md) | Agent creation overview |
| [Factory Methods](./factory-methods.md) | LLM-based code generation |
| [Config Delegation](./config-delegation.md) | JSON config to class mapping |
| [Tool Builder](./tool-builder.md) | Tool creation and management |

## Building Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Design    │────►│   Build     │────►│  Deploy     │
│   (Config)  │     │   (Factory) │     │  (Pool)     │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Agent Creation Methods

### 1. Build - LLM Source Code

- Factory method creates agent instances using LLM-generated source code
- **Coder**: Generates code based on user prompt
- **Guider**: Generates code based on rules defined in md files
- Code deployment to agent pool

### 2. Config - Use Existing

- Delegate methods to classes via JSON config
- Shared API for existing code grouped by category
- Plugin structure for add/remove functionality
- Manager for functional grouping
