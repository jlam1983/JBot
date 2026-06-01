# Sequential Interaction (One-by-One)

## Overview

Sequential interaction is a linear interaction pattern where agents process information in a chain, with each agent's output serving as the next agent's input.

---

## Characteristics

| Attribute | Description |
|-----------|-------------|
| **Pattern** | Linear, ordered chain |
| **Direction** | Forward-only or bidirectional |
| **Complexity** | Low |
| **Latency** | Sum of all agent processing times |
| **Failure Mode** | Chain breaks at failure point |
| **Scalability** | Limited by chain length |

---

## Configuration

```json
"sequential_interaction": {
  "chain_config": {
    "agent_sequence": ["agent_id_1", "agent_id_2", "agent_id_3"],
    "direction": "forward | backward | bidirectional",
    "loop_allowed": false,
    "max_iterations": 10
  },
  "data_passing": {
    "full_output": true,
    "partial_output": {
      "enabled": false,
      "selection_criteria": "relevant | filtered | summarized"
    },
    "transformation": {
      "enabled": true,
      "rules": ["normalize", "enrich", "validate"]
    }
  },
  "error_handling": {
    "stop_on_error": true,
    "retry_failed_agent": true,
    "retry_count": 3,
    "fallback_agent": "agent_id | null"
  }
}
```

---

## Chain Types

### 1. Linear Forward Chain
```
Input → Agent A → Agent B → Agent C → Output
```
Each agent receives the full output of the previous agent.

### 2. Linear Forward with Selection
```
Input → Agent A → Select → Agent B → Select → Agent C → Output
```
A selector filters what gets passed forward.

### 3. Bidirectional Chain
```
Input → Agent A → Agent B → Agent C → Output
                              ▲
                              │
                        Agent C can
                        send back
```
Agents can communicate backwards in the chain.

### 4. Cyclic Chain
```
Agent A → Agent B → Agent C → Agent A (loop)
```
Output cycles back to the start until a condition is met.

---

## Value Addition at Each Step

```json
"value_addition": {
  "agent_a": {"role": "input_processing", "adds": ["validation", "normalization"]},
  "agent_b": {"role": "core_processing", "adds": ["analysis", "extraction"]},
  "agent_c": {"role": "output_refinement", "adds": ["validation", "summarization"]}
}
```

## Workflow Suggestion in Sequential

During sequential processing, agents can suggest:
- **Skip remaining steps** - If output is already optimal
- **Add refinement step** - If quality needs improvement
- **Reorder steps** - If dependency analysis shows inefficiency
- **Parallelize sub-tasks** - If independent portions exist
- **Early termination** - If success criteria are met

---

## Use Cases

- **Document Pipeline**: Parse → Analyze → Summarize → Format
- **Code Generation**: Design → Implement → Test → Document
- **Data Analysis**: Collect → Clean → Analyze → Visualize
