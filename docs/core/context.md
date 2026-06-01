# Context

## Overview

Context is the environment in which agents operate. It provides session-based memory management, maintains state across interactions, and enables agents to be organized by threading.

---

## Context Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         Context                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Agent List    │  │  Session Memory │  │   Job State     │  │
│  │  (by Thread)    │  │   (Per Session) │  │   (Active)      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Shared Context                           │  │
│  │         (Synchronized across agents in session)            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Context Types

### 1. Static Agent List

A predefined list of agents organized by threading.

```json
"static_agent_list": {
  "threading": {
    "thread_1": ["agent_a", "agent_b"],
    "thread_2": ["agent_c", "agent_d", "agent_e"]
  },
  "agent_availability": {
    "agent_a": "online",
    "agent_b": "offline"
  }
}
```

### 2. Session Memory

Memory management for each individual session.

```json
"session_memory": {
  "session_id": "uuid",
  "short_term": {
    "current_input": "...",
    "current_output": "...",
    "pending_tasks": []
  },
  "long_term": {
    "accumulated_knowledge": "reference to summary_storage",
    "learned_preferences": {}
  },
  "ttl_seconds": 3600
}
```

### 3. Context Types for Jobs

| Context Type | Purpose |
|-------------|---------|
| **Content Generation** | Generate text, code, or media |
| **Research/Discuss** | Investigate topics, facilitate discussion |
| **Workflow Runner** | Execute multi-step processes |

---

## Context Function

### Memory

Core functionality for maintaining state and history.

```json
"context_function": {
  "memory": {
    "working_memory": {
      "capacity": "items count",
      "eviction_policy": "lru | fifo | importance"
    },
    "episodic_memory": {
      "store_interactions": true,
      "max_episodes": 1000
    },
    "semantic_memory": {
      "store_facts": true,
      "update_on_interaction": true
    }
  },
  "state_management": {
    "persist_state": true,
    "state_sync_frequency": "real_time | periodic",
    "conflict_resolution": "last_write | user_override"
  }
}
```

---

## Agent Awareness

Agents within a context are aware of each other.

```json
"agent_awareness": {
  "know_other_agents": true,
  "know_other_capabilities": true,
  "know_current_role": true,
  "can_communicate": true
}
```

---

## Shared Context

When multiple agents work together, they share context.

```json
"shared_context": {
  "enabled": true,
  "sync_frequency": "real_time | periodic | on_demand",
  "shared_data": {
    "current_job": true,
    "accumulated_results": true,
    "intermediate_states": true
  },
  "synchronization": {
    "on_input_receive": true,
    "on_role_complete": true,
    "on_job_complete": true
  }
}
```

---

## Usage Notes

- Context persists state across agent interactions within a session
- Agents can be statically predefined or dynamically added
- Session memory has configurable TTL for cleanup
- Shared context enables multi-agent collaboration
- Context types should match the job type being performed
