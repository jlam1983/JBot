# Factory Methods

## Overview

Factory methods define how agents and tools are instantiated from configurations or generated through LLM code generation.

---

## LLM Factory Method

Generates agent/tool code using LLM based on user input and rules.

### Flow

```
User Prompt + MD Rules → LLM Factory → Generated Code → Agent Pool
```

### Components

```json
"llm_factory": {
  "inputs": {
    "coder_input": {
      "source": "user_prompt",
      "description": "Natural language description of desired agent"
    },
    "guider_input": {
      "source": "md_rule_files",
      "description": "Structured rules for code generation"
    }
  },
  "generation_process": {
    "coder": {
      "task": "generate_source_code",
      "depends_on": "user_prompt",
      "outputs": "python_code"
    },
    "guider": {
      "task": "structure_code_with_rules",
      "depends_on": "md_files",
      "outputs": "structured_implementation"
    }
  },
  "on_factory": {
    "code_generation": true,
    "code_validation": true,
    "code_deployment": {
      "target": "pool",
      "pool_type": "agent | tool"
    }
  }
}
```

---

## Config Factory Method

Delegates configuration to existing class implementations.

### Flow

```
JSON Config → Config Parser → Class Delegation → Agent Instance
```

### Components

```json
"config_factory": {
  "input": {
    "source": "json_file",
    "schema": "agent_json_schema"
  },
  "processing": {
    "parse_config": true,
    "validate_schema": true,
    "map_to_classes": {
      "role_to_class": true,
      "action_to_handler": true,
      "principle_to_constraints": true
    }
  },
  "output": {
    "instantiated_agent": true,
    "ready_to_initialize": true
  }
}
```

---

## Shared API Pattern

```json
"shared_api": {
  "by_category": {
    "judger": {
      "interface": "JudgeInterface",
      "implementations": ["FactJudger", "ValueJudger", "LogicChecker"],
      "shared_methods": ["evaluate", "compare", "validate"]
    },
    "generator": {
      "interface": "GeneratorInterface",
      "implementations": ["ContentGenerator", "PlanGenerator"],
      "shared_methods": ["generate", "refine", "validate"]
    }
  }
}
```

---

## Code Deployment to Pool

```json
"code_deployment": {
  "target_pool": "agent_pool | tool_pool",
  "deployment_steps": {
    "1_validate": "check_code_integrity",
    "2_package": "create_deployable_unit",
    "3_register": "add_to_pool_registry",
    "4_activate": "make_available_for_use"
  },
  "pool_management": {
    "add": true,
    "remove": true,
    "update": true,
    "version": true
  }
}
```
