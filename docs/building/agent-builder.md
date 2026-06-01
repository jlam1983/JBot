# Agent Builder

## Overview

Agent Builder provides the infrastructure for creating and configuring agents through factory methods and JSON configuration delegation.

---

## Agent Creation Methods

### 1. Build - LLM Source Code

Generate agent code using LLM.

```json
"llm_build": {
  "factory_method": {
    "coder": {
      "input": "user_prompt",
      "generates": "source_code"
    },
    "guider": {
      "input": "md_rules",
      "generates": "structured_code"
    }
  },
  "on_factory": {
    "code_generation": {
      "coder": "based on user prompt input",
      "guider": "based on rule of md file"
    },
    "code_deployment": {
      "target": "agent_pool"
    }
  }
}
```

### 2. Config - Use Existing

Configure agents using existing code through JSON config.

```json
"config_build": {
  "factory_method": {
    "delegate_to_class": true,
    "shared_api": true,
    "plugin_structure": true,
    "functional_manager": true
  },
  "on_factory": {
    "delegate_method": "json_config_to_class_mapping",
    "shared_api_per_category": true,
    "plugin_folder_structure": {
      "add_allowed": true,
      "remove_allowed": true,
      "interface_required": true
    },
    "manager": {
      "group_functions": true,
      "group_by_category": true
    }
  }
}
```

---

## Factory Methods

### LLM Factory Method

```json
"llm_factory": {
  "input_sources": {
    "user_prompt": "natural_language_description",
    "md_rules": "rule_definitions"
  },
  "generation": {
    "coder": {
      "depends_on": "user_prompt",
      "outputs": "source_code"
    },
    "guider": {
      "depends_on": "md_file_rules",
      "outputs": "structured_implementation"
    }
  },
  "output": {
    "deployed_to": "agent_pool"
  }
}
```

### Config Factory Method

```json
"config_factory": {
  "input": "json_configuration",
  "processing": {
    "delegate_to_classes": true,
    "map_roles_to_implementations": true,
    "map_actions_to_handlers": true
  },
  "output": {
    "instantiated_agent": true,
    "ready_for_deployment": true
  }
}
```

---

## Plugin Structure

Agents and tools can be structured as plugins:

```json
"plugin_structure": {
  "folder_layout": {
    "base_path": "./plugins/",
    "agent_plugins": "./plugins/agents/",
    "tool_plugins": "./plugins/tools/"
  },
  "interface_required": {
    "agent": "AgentInterface",
    "tool": "ToolInterface"
  },
  "lifecycle": {
    "discovery": "auto_scan",
    "registration": "automatic",
    "activation": "on_demand"
  },
  "user_actions": {
    "add_plugin": true,
    "remove_plugin": true,
    "update_plugin": true
  }
}
```

---

## Functional Manager

```json
"functional_manager": {
  "grouping": {
    "by_category": true,
    "by_capability": true,
    "by_purpose": true
  },
  "management": {
    "list_available": true,
    "enable_disable": true,
    "configure": true,
    "monitor": true
  }
}
```

---

## Agent Function

### Content Windows

```json
"content_windows": {
  "up_content": {
    "direction": "input_to_agent",
    "window_size": "configurable"
  },
  "down_content": {
    "direction": "agent_to_output",
    "window_size": "configurable"
  }
}
```
