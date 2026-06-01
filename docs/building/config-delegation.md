# Config Delegation

## Overview

Config Delegation maps JSON configuration to class implementations, enabling declarative agent configuration.

---

## Delegation Pattern

```json
"delegation": {
  "json_config": {
    "role": {
      "planner": {...},
      "guider": {...}
    },
    "action": {
      "working": {...},
      "monitoring": {...}
    }
  },
  "class_mapping": {
    "planner": "PlannerClass",
    "guider": "GuiderClass",
    "working": "WorkingClass",
    "monitoring": "MonitoringClass"
  },
  "delegation_process": {
    "parse": "read_json_config",
    "map": "match_keys_to_classes",
    "instantiate": "create_class_instances",
    "wire": "connect_components"
  }
}
```

---

## Role to Class Delegation

```json
"role_delegation": {
  "planner": {
    "class": "PlannerImpl",
    "init_from_config": ["list_of_plan", "strategy"]
  },
  "guider": {
    "class": "GuiderImpl",
    "init_from_config": ["rule_set"]
  },
  "value_judger": {
    "class": "ValueJudgerImpl",
    "init_from_config": ["value", "view_angle"]
  },
  "fact_judger": {
    "class": "FactJudgerImpl",
    "init_from_config": ["fact"]
  },
  "worker": {
    "class": "WorkerImpl",
    "init_from_config": ["do_the_work"]
  },
  "center_integrator": {
    "class": "CenterIntegratorImpl",
    "init_from_config": ["data_holder", "message_holder"]
  }
}
```

---

## Action to Handler Delegation

```json
"action_delegation": {
  "monitor": {
    "handler": "MonitorHandler",
    "config_keys": ["observe", "triggers"]
  },
  "planning": {
    "handler": "PlanningHandler",
    "config_keys": ["plan", "replanning"]
  },
  "reflecting": {
    "handler": "ReflectingHandler",
    "config_keys": ["self_evaluation", "outcome_analysis"]
  },
  "integrating": {
    "handler": "IntegratingHandler",
    "config_keys": ["solve_concept", "group_concept"]
  },
  "absorbing": {
    "handler": "AbsorbingHandler",
    "config_keys": ["thought_storage", "thinking_experience"]
  },
  "abstracting": {
    "handler": "AbstractingHandler",
    "config_keys": ["extraction", "summarization"]
  },
  "working": {
    "handler": "WorkingHandler",
    "config_keys": ["execution", "sandbox", "error_handling"]
  },
  "correcting": {
    "handler": "CorrectingHandler",
    "config_keys": ["error_detection", "auto_correction"]
  }
}
```

---

## Plugin Integration

```json
"plugin_delegation": {
  "interface_required": "AgentInterface",
  "discovery": {
    "scan_folders": ["./plugins/agents"],
    "auto_discover": true
  },
  "registration": {
    "name": "from_config",
    "class": "from_implementation",
    "config_schema": "validated_against"
  },
  "lifecycle": {
    "load": "on_demand",
    "unload": "when_idle",
    "reload": "on_config_change"
  }
}
```
