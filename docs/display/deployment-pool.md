# Deployment Pool

## Overview

Deployment Pool manages the lifecycle of agents from design to production. It allows deploying agents as online services and generating standalone code.

---

## Deployment Pool Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  Deployment Pool                                                 │
├─────────────────────────────────────────────────────────────────┤
│  [+ Deploy Agent]  [⚙ Settings]  [📊 Monitor]                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │ ● Online        │  │ ○ Offline       │  │ ○ Building      │   │
│  │ Agent A v1.2.3  │  │ Agent B v1.0.0  │  │ Agent C v1.3.0  │   │
│  │ [Stop] [Restart]│  │ [Deploy]       │  │ [Cancel]        │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
│                                                                   │
│  Code Collection                                                 │
│  [agent_a_v1.2.3.py] [View] [Copy Import] [Download]            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Status States

| Status | Description | Actions |
|--------|-------------|---------|
| **Online** | Running and responding | Stop, Restart, View Logs |
| **Offline** | Saved but not running | Deploy, Edit, Delete |
| **Building** | Being packaged/deployed | View Progress, Cancel |
| **Error** | Deployment failed | View Error, Retry |

---

## Deployment Operations

### Deploy
```json
"deploy_operation": {
  "target": {
    "environment": "local | server | cloud",
    "resources": {"cpu": "1-4 cores", "memory": "512MB-4GB"}
  },
  "exposure": {
    "protocol": "http | https | websocket",
    "authentication": "none | api_key | oauth",
    "rate_limit": 100
  }
}
```

### Deployment Flow
```
Build → Package → Deploy to Server → Running
```

---

## Code Collection Generation

Generated standalone Python code:

```python
# agent_a_v1.2.3.py
from jllmbot import Agent, AgentConfig

class AgentA(Agent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self._setup_roles()

    def process(self, input_data, context):
        # Main processing logic
        pass

def create_agent(config: AgentConfig) -> Agent:
    return AgentA(config)
```

### Usage in External Python
```python
from agent_a_v1_2_3 import create_agent
agent = create_agent(my_config)
result = agent.run_sync("input")
```

---

## Server Management

### Server Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent/{name}/run` | Run agent |
| GET | `/agent/{name}/status` | Get status |
| POST | `/agent/{name}/reload` | Reload config |
| GET | `/health` | Health check |

---

## Monitoring

### Agent Metrics
```json
{
  "requests_total": 1234,
  "avg_response_time_ms": 245,
  "uptime_seconds": 172800,
  "memory_usage_mb": 128
}
```

---

## Use Cases

1. **Deploy to Production**: Take designed agents live
2. **Local Testing**: Run agents locally before deployment
3. **Code Integration**: Import generated agents into custom Python projects
4. **Scale Agents**: Run multiple instances
