# Summary Storage

## Overview

Summary Storage is a persistent knowledge management system that accumulates, refines, and organizes information across agent sessions. It serves as a centralized repository for learned experiences, rules, facts, and observations.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Summary Storage                            │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │ Experience│  │   Rules   │  │   Facts   │  │  Notices  │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────┘
                    Accumulation │ Refinement │ Retrieval
```

---

## Storage Categories

### 1. Experience

Learned knowledge from agent interactions and problem-solving.

```json
"experience": {
  "captured_from": ["reasoning_chain", "decision_point", "task_outcome"],
  "storage": {
    "type": "episodic | semantic | procedural",
    "indexing": ["timestamp", "domain", "importance"]
  },
  "accumulation": {
    "merge_similar": true,
    "update_on_repeat": true,
    "confidence_tracking": true
  },
  "refinement": {
    "periodic_review": true,
    "consolidation": true,
    "forgetting_low_importance": true
  }
}
```

### 2. Rules (Should Concern)

Guidelines and rules that agents should be aware of and follow.

```json
"rules": {
  "rule_types": {
    "safety": {"priority": "high", "enforcement": "strict | advisory"},
    "behavioral": {"priority": "medium", "enforcement": "strict | advisory"},
    "domain_specific": {"priority": "low", "enforcement": "strict | advisory"}
  },
  "rule_management": {
    "addition": "manual | automatic | semi_automatic",
    "conflict_resolution": "priority_based | recency_based | user_override"
  },
  "concern_mapping": {
    "concept_to_rule": true,
    "situation_to_rule": true,
    "trigger_detection": true
  }
}
```

### 3. Brief Importance Fact

Concise, high-value facts that are important and easily retrievable.

```json
"important_facts": {
  "fact_criteria": {
    "importance_score_min": 0.7,
    "verifiable": true,
    "actionable": true,
    "persistence_value": true
  },
  "brief_format": {
    "max_length": 100,
    "include_source": true,
    "include_confidence": true
  },
  "storage": {
    "priority_index": "importance",
    "embedding_enabled": true
  },
  "update_policy": {
    "on_new_evidence": true,
    "on_conflict": "replace | merge | flag",
    "decay_low_importance": true
  }
}
```

### 4. Brief Notice Thing

Short observations and noteworthy items from different agents.

```json
"notices": {
  "by_agent": {
    "enabled": true,
    "per_agent_storage": true,
    "aggregation": "individual | collective | both"
  },
  "notice_types": {
    "observation": {"enabled": true, "persistence": "ephemeral | temporary | permanent"},
    "anomaly": {"enabled": true, "alert_level": "info | warning | critical"},
    "pattern": {"enabled": true, "min_occurrences": 3},
    "suggestion": {"enabled": true, "requires_review": true}
  },
  "brief_format": {
    "max_length": 50,
    "include_context": true,
    "include_timestamp": true,
    "include_agent_id": true
  }
}
```

---

## Storage Operations

### Accumulation

```json
"accumulation": {
  "strategy": "all | selective | importance_weighted",
  "deduplication": {
    "enabled": true,
    "similarity_threshold": 0.85,
    "merge_strategy": "keep_both | keep_newer | keep_important"
  },
  "overflow_handling": {
    "strategy": "drop_oldest | drop_lowest_importance | archive"
  }
}
```

### Refinement

```json
"refinement": {
  "scheduled": {
    "enabled": true,
    "interval_hours": 24,
    "scope": "incremental | full"
  },
  "operations": {
    "consolidate_fragments": true,
    "remove_duplicates": true,
    "update_confidence": true,
    "prune_low_value": true,
    "cross_reference": true
  },
  "quality_metrics": {
    "completeness": true,
    "consistency": true,
    "freshness": true
  }
}
```

### Retrieval

```json
"retrieval": {
  "methods": {
    "exact_match": true,
    "semantic_search": true,
    "keyword_search": true,
    "graph_traversal": true
  },
  "ranking": {
    "by_relevance": true,
    "by_recency": true,
    "by_confidence": true,
    "by_importance": true
  }
}
```

---

## Cross-Agent Summary

```json
"cross_agent": {
  "shared_storage": {
    "enabled": true,
    "sync_strategy": "real_time | periodic | on_demand"
  },
  "agent_perspectives": {
    "planner": "strategic_summary",
    "guider": "rule_applications",
    "worker": "execution_experience",
    "fact_judger": "verified_facts",
    "value_judger": "value_observations"
  },
  "consensus_building": {
    "enabled": true,
    "aggregation_method": "voting | confidence_weighted | priority_based"
  }
}
```

---

## Usage Notes

- Designed for long-term knowledge retention across sessions
- Each category operates independently or integrated with others
- Importance scoring drives storage decisions and retrieval ranking
- Refinement operations maintain storage quality
- Cross-agent summaries enable knowledge sharing
