# Agent

## Overview

An Agent is an autonomous entity configured through JSON that can perceive, reason, plan, and act to fulfill user intent. Agents combine **roles** (what they are) with **actions** (what they do) and operate within a **context** (where they store state).

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Agent                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐        │
│  │ Working Style │  │   Principle  │  │   Metadata    │        │
│  │  (How to run) │  │(Constraints)  │  │  (Identity)   │        │
│  └───────────────┘  └───────────────┘  └───────────────┘        │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                         Roles                              │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │   │
│  │  │Planner│ │Guider│ │Judger│ │Worker│ │Expl.│ │Center│       │   │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘       │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                        Actions                              │   │
│  │  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐       │   │
│  │  │Monitor│ │Planning│ │Integr.│ │Absorb.│ │Working│       │   │
│  │  └───────┘ └───────┘ └───────┘ └───────┘ └───────┘       │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent JSON Schema

```json
{
  "name": "string",
  "description": "string",

  "working_style": {
    "mode": "sequential | parallel | hybrid",
    "input_type": "text | code | file | multi-modal",
    "output_type": "text | code | file | structured",
    "execution_order": ["role1", "role2"],
    "termination_condition": "string"
  },

  "principle": {
    "core_principles": ["principle1", "principle2"],
    "priority_order": ["safety", "accuracy", "efficiency"],
    "constraint": {
      "max_iterations": 10,
      "max_time_seconds": 300,
      "resource_limit": "string"
    },
    "fallback_strategy": "abort | retry | skip | escalate"
  },

  "action": {
    "monitor": { ... },
    "planning": { ... },
    "reflecting": { ... },
    "integrating": { ... },
    "absorbing": { ... },
    "abstracting": { ... },
    "working": { ... },
    "correcting": { ... }
  },

  "role": {
    "planner": { ... },
    "guider": { ... },
    "value_judger": { ... },
    "fact_judger": { ... },
    "knowledge_explainer": { ... },
    "logic_checker": { ... },
    "recommender": { ... },
    "worker": { ... },
    "center_integrator": { ... }
  }
}
```

---

## Metadata

### name
- **Type:** string
- **Description:** Unique identifier for the agent

### description
- **Type:** string
- **Description:** Brief description of the agent's purpose

---

## Working Style

Defines how the agent processes tasks.

| Property | Type | Description |
|----------|------|-------------|
| `mode` | enum | `sequential` (one-by-one), `parallel` (simultaneous), `hybrid` (mixed) |
| `input_type` | enum | Accepted input types: text, code, file, multi-modal |
| `output_type` | enum | Expected output format |
| `execution_order` | array | Specific order of role execution |
| `termination_condition` | string | When to stop processing |

---

## Principle

Core operational constraints and fallback behavior.

| Property | Type | Description |
|----------|------|-------------|
| `core_principles` | array | Fundamental rules governing behavior |
| `priority_order` | array | Hierarchy when principles conflict |
| `constraint.max_iterations` | number | Maximum loop iterations |
| `constraint.max_time_seconds` | number | Maximum execution time |
| `fallback_strategy` | enum | `abort`, `retry`, `skip`, or `escalate` |

---

## Roles

Roles define the agent's functional identity and capabilities.

### Role Summary

| Role | Purpose |
|------|---------|
| **Planner** | Determines plans and strategies |
| **Guider** | Defines rules and behavioral guidelines |
| **Value Judger** | Evaluates values and perspectives |
| **Fact Judger** | Verifies factual accuracy |
| **Knowledge Explainer** | Explains complex concepts |
| **Logic Checker** | Validates logical consistency |
| **Recommender** | Provides suggestions and solutions |
| **Worker** | Executes tasks using tools |
| **Center Integrator** | Central hub for data/messaging |

### 1. Planner

```json
"planner": {
  "list_of_plan": ["step1", "step2", "step3"]
}
```

### 2. Guider

```json
"guider": {
  "rule_set": {
    "must": ["rule1", "rule2"],
    "must_not": ["forbidden1", "forbidden2"],
    "concept_to_concern": {
      "concept_a": "concern_a"
    }
  }
}
```

### 3. Value Judger

```json
"value_judger": {
  "value": {
    "view_angle": "perspective",
    "value_selected_list": ["value1", "value2"],
    "value_list_arrangement": "priority/ranking"
  }
}
```

### 4. Fact Judger

```json
"fact_judger": {
  "fact": {
    "related_fact_search": "search query",
    "compare_user_text": {
      "knowledge_base": true,
      "internet": true
    },
    "compare_with_theory": {
      "society_proved": true
    }
  }
}
```

### 5. Knowledge Explainer

```json
"knowledge_explainer": {
  "explain": {
    "target_audience": "beginner | intermediate | expert",
    "depth_level": "surface | moderate | deep",
    "explanation_style": "simple | technical | illustrative",
    "include_examples": true,
    "include_analogies": true
  }
}
```

### 6. Logic Checker

```json
"logic_checker": {
  "logic": {
    "check_types": {
      "circular_reasoning": true,
      "contradiction": true,
      "missing_premise": true,
      "invalid_inference": true,
      "fallacy_detection": true
    },
    "reasoning_framework": "deductive | inductive | abductive"
  }
}
```

### 7. Recommender

```json
"recommender": {
  "suggestion": {
    "problem_points": ["issue1", "issue2"],
    "solutions": {
      "problem1": {
        "solution": "description",
        "suggestion": "actionable advice"
      }
    }
  }
}
```

### 8. Worker

```json
"worker": {
  "do_the_work": {
    "run_cmd": true,
    "run_shell": true,
    "run_python_code": true,
    "use_tools": ["tool1", "tool2"]
  }
}
```

### 9. Center Integrator

```json
"center_integrator": {
  "data_holder": true,
  "message_holder": true,
  "generated_text_holder": true,
  "communicate_between_holders": true
}
```

---

## Actions

Actions define the agent's operational behaviors during task execution.

### Action Summary

| Action | Purpose |
|--------|---------|
| **Monitor** | Observes and tracks progress |
| **Planning** | Develops strategies |
| **Reflecting** | Reviews and evaluates |
| **Integrating** | Synthesizes concepts |
| **Absorbing** | Updates thought storage |
| **Abstracting** | Extracts from data |
| **Working** | Executes tasks |
| **Correcting** | Fixes errors |

### 1. Monitor

```json
"monitor": {
  "observe": {
    "track_progress": true,
    "track_resources": true,
    "track_environment": true
  },
  "triggers": {
    "on_change": "notify | log | action",
    "on_threshold": "alert | stop | adjust"
  }
}
```

### 2. Planning

```json
"planning": {
  "plan": {
    "strategy": "sequential | parallel | hierarchical",
    "goal_decomposition": true,
    "subtask_generation": true,
    "dependency_mapping": true
  },
  "replanning": {
    "on_failure": true,
    "on_new_information": true
  }
}
```

### 3. Reflecting

```json
"reflecting": {
  "self_evaluation": true,
  "outcome_analysis": true,
  "error_analysis": true,
  "learn_from_experience": true,
  "reflection_triggers": {
    "on_completion": true,
    "on_failure": true,
    "periodic_reflection": true
  }
}
```

### 4. Integrating

```json
"integrating": {
  "solve_concept": {
    "methods": ["decomposition", "analogy", "first_principles"]
  },
  "group_concept": {
    "grouping_criteria": ["semantic", "functional", "causal"]
  },
  "find_first_principle": {
    "methods": ["abstraction", "reduction", "socratic_questioning"]
  }
}
```

### 5. Absorbing

```json
"absorbing": {
  "thought_storage": {
    "storage_type": "episodic | semantic | procedural",
    "update_strategy": "append | merge | replace"
  },
  "thinking_experience": {
    "capture_reasoning_chain": true,
    "capture_decision_points": true,
    "capture_heuristics": true
  },
  "knowledge_updates": {
    "merge_strategy": "last_write_wins | importance_weighted",
    "incremental_learning": true
  }
}
```

### 6. Abstracting

```json
"abstracting": {
  "extraction": {
    "info_piece": {
      "granularity": "sentence | paragraph | section"
    },
    "table_attribute": {
      "extract_headers": true,
      "infer_relationships": true
    },
    "article_fragment": {
      "fragment_types": ["finding", "method", "result"]
    }
  },
  "summarization": {
    "summary_length": "brief | moderate | comprehensive"
  }
}
```

### 7. Working

```json
"working": {
  "execution": {
    "run_cmd": true,
    "run_shell": true,
    "run_python_code": true,
    "use_tools": ["tool1", "tool2"]
  },
  "sandbox": {
    "enabled": true,
    "isolation_level": "full | partial | none"
  }
}
```

### 8. Correcting

```json
"correcting": {
  "error_detection": {
    "detect_syntax_error": true,
    "detect_logic_error": true,
    "detect_runtime_error": true
  },
  "auto_correction": {
    "enabled": true,
    "fix_syntax": true,
    "fix_runtime": true
  },
  "feedback_loop": {
    "feedback_source": ["user", "system", "self"]
  }
}
```

---

## Usage Notes

- All roles are optional and can be mixed based on agent requirements
- **Center Integrator** connects all other components
- Actions operate alongside roles - roles define identity, actions define behavior
- **Absorbing** and **Abstracting** handle knowledge management
- **Monitor** and **Reflecting** enable self-improvement
