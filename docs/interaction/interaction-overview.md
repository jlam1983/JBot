# Interaction Overview

## Overview

Interaction defines how agents communicate, collaborate, and coordinate within a shared context to accomplish user intent collectively.

---

## What is Agent Interaction?

Agent interaction is the **communication and collaboration patterns** between agents operating within the same context:

- How agents pass information between each other
- How agents coordinate to achieve shared goals
- How agents contribute to a unified outcome
- How group decisions are formed

```
┌─────────────────────────────────────────────────────────────┐
│                       Context                                │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ Agent A │◄──►│ Agent B │◄──►│ Agent C │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
│       │              │              │                        │
│       └──────────────┴──────────────┘                        │
│                      │                                        │
│              ┌───────▼───────┐                               │
│              │   Interaction │                               │
│              │    Patterns   │                               │
│              └───────────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Interaction Types

### 1. One-by-One (Sequential)

Agents interact in a linear, sequential pattern where output from one agent becomes input for the next.

```json
"one_by_one": {
  "pattern": {
    "direction": "linear",
    "agent_order": ["agent1", "agent2", "agent3"],
    "data_flow": "sequential_pass"
  },
  "characteristics": {
    "input_source": "previous_agent_output",
    "output_destination": "next_agent_input",
    "latency": "low",
    "simplicity": "high"
  },
  "use_cases": ["Pipeline processing", "Step-by-step refinement"]
}
```

### 2. Group Discuss

Multiple agents discuss, debate, and collaborate simultaneously to reach a shared understanding or decision.

```json
"group_discuss": {
  "pattern": {
    "structure": "mesh | hub_spoke | hierarchical",
    "communication": "broadcast | direct | moderated",
    "consensus_formation": "voting | negotiation | arbitration"
  },
  "roles": {
    "contributor": "Agents that provide input",
    "moderator": "Manages discussion flow",
    "synthesizer": "Combines contributions"
  },
  "use_cases": ["Multi-perspective analysis", "Brainstorming", "Consensus building"]
}
```

### 3. Workflow Suggestion

Agents propose and refine workflows dynamically, adding value at each step.

```json
"workflow_suggestion": {
  "pattern": {
    "chain_type": "linear | branched | parallel | adaptive",
    "value_addition": "at_each_step | on_trigger | continuous"
  },
  "suggestion_types": {
    "process_enhancement": "Suggest improved steps",
    "scope_adjustment": "Suggest expanding/narrowing scope",
    "sequence_modification": "Suggest reordering",
    "parallelization": "Suggest concurrent execution"
  },
  "use_cases": ["Data pipeline optimization", "Prompt chain refinement"]
}
```

---

## Data Flow Patterns

### Prompt Chain

```
User Intent → Prompt A → Prompt B → Prompt C → Final Output
                │           │           │
                ▼           ▼           ▼
             Value+      Value+      Value+
```

### Data Chain

```
Raw Data → Agent A → Intermediate → Agent B → Processed → Agent C → Result
              │                                │                                │
              ▼                                ▼                                ▼
           Insight 1                       Insight 2                       Insight 3
```

---

## Interaction Configuration

```json
"interaction_config": {
  "context_setup": {
    "shared_context": true,
    "agent_awareness": {
      "know_other_agents": true,
      "know_other_capabilities": true
    }
  },
  "communication": {
    "message_types": ["request", "response", "notification", "broadcast"],
    "protocols": ["request_response", "fire_and_forget", "subscription"]
  },
  "coordination": {
    "task_distribution": "centralized | decentralized",
    "conflict_resolution": "priority | consensus | arbitration"
  }
}
```
