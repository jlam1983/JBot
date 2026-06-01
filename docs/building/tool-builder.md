# Tool Builder

## Overview

Tool Builder creates functional units that extend agent capabilities. Tools can be generated through LLM or configured through JSON.

---

## Tool Creation Methods

### 1. Build - LLM Source Code

```json
"llm_tool_build": {
  "factory_method": {
    "coder": {
      "input": "user_description",
      "generates": "tool_code"
    },
    "guider": {
      "input": "md_rules",
      "generates": "structured_tool"
    }
  },
  "on_factory": {
    "code_generation": {
      "category_grouping": {
        "enabled": true,
        "group_by": "functionality"
      },
      "shared_interface": {
        "enabled": true,
        "interface_type": "category_based"
      }
    },
    "code_deployment": {
      "target": "tool_pool"
    }
  }
}
```

### 2. Tool Function

```json
"tool_function": {
  "dynamic_generation": {
    "enabled": true,
    "input": "user_description",
    "output": "executable_tool"
  },
  "capabilities": [
    "file_operations",
    "code_execution",
    "web_requests",
    "data_processing"
  ]
}
```

---

## Tool Categories

```json
"tool_categories": {
  "file_tools": {
    "interface": "FileToolInterface",
    "examples": ["read_file", "write_file", "list_directory"]
  },
  "code_tools": {
    "interface": "CodeToolInterface",
    "examples": ["run_python", "run_shell", "compile"]
  },
  "web_tools": {
    "interface": "WebToolInterface",
    "examples": ["fetch_url", "search", "api_call"]
  },
  "data_tools": {
    "interface": "DataToolInterface",
    "examples": ["parse_json", "query_db", "transform"]
  }
}
```

---

## Tool Pool

```json
"tool_pool": {
  "management": {
    "register": true,
    "unregister": true,
    "update": true,
    "list_available": true
  },
  "discovery": {
    "by_category": true,
    "by_capability": true,
    "by_name": true
  },
  "usage": {
    "allocate_to_agent": true,
    "share_between_agents": true,
    "track_usage": true
  }
}
```
