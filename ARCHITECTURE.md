# JLLMBot Architecture Guide

## Overview

JLLMBot is an intelligent agent system with a modular architecture. This guide explains the data flow, key concepts, and how components interact.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         JLLMBot                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                      Display Layer                          │  │
│  │   Interaction Plan │ Deployment Pool │ Mindset Modifier     │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    Interaction Layer                         │  │
│  │     Sequential │ Group Discuss │ Workflow Suggestion        │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                       Core Layer                             │  │
│  │     Agent │ Context │ Job Types │ Summary Storage           │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                     Building Layer                            │  │
│  │     Factory Methods │ Config Delegation │ Tool Builder      │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. User Input → Agent Processing

```
User Input (String/JSON)
        │
        ▼
┌───────────────────┐
│   Context         │ ← Session memory, agent list
│   (SessionMemory) │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│   Job             │ ← Intent → Goals transformation
│   (Job, Intent)   │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│   Agent           │ ← Process with roles & actions
│   (Agent.process)│
└───────────────────┘
        │
        ▼
    Output (Result)
```

### 2. Agent Internal Processing

```python
# Input flow inside Agent.process()
input_data
    │
    ▼
┌─────────────────────────────────────────────┐
│ 1. Role Processing                          │
│    - Planner: Generate plan                 │
│    - Guider: Apply rules                   │
│    - Judgers: Evaluate values/facts         │
│    - Worker: Execute tasks                  │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ 2. Action Processing                        │
│    - Monitor: Track progress               │
│    - Planning: Strategize                  │
│    - Reflecting: Self-evaluate             │
│    - Integrating: Synthesize concepts       │
│    - Absorbing: Update memory              │
│    - Abstracting: Extract info              │
│    - Correcting: Fix errors                │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ 3. Center Integrator                        │
│    - Data holder: Store results            │
│    - Message holder: Manage messages       │
│    - Generated text holder: Keep outputs    │
└─────────────────────────────────────────────┘
    │
    ▼
   Output
```

### 3. Multi-Agent Interaction Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Interaction Manager                            │
│                                                                  │
│   User Intent                                                    │
│       │                                                           │
│       ▼                                                           │
│   ┌────────────────────────────────────────────────────────────┐ │
│   │  Sequential: A → B → C → Result                            │ │
│   │  Group Discuss: All agents contribute → Consensus           │ │
│   │  Workflow Suggestion: A → [Suggest] → B → [Suggest] → C   │ │
│   └────────────────────────────────────────────────────────────┘ │
│       │                                                           │
│       ▼                                                           │
│   Result + Suggestions                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. Agent (src/core/agent.py)

The core autonomous entity.

```python
# Creation
config = AgentConfig(name="my_agent", description="...")
agent = Agent(config)

# Or from dict
agent = Agent({"name": "my_agent", ...})

# Execution
result = agent.process(input_data, context)
# or
result = agent.run_sync("string input")
```

**Agent Structure:**
```
Agent
├── WorkingStyle (how to run: sequential/parallel/hybrid)
├── Principle (constraints, fallback strategy)
├── Actions (8 types: monitor, planning, reflecting, etc.)
└── Roles (9 types: planner, guider, judgers, worker, etc.)
```

### 2. Context (src/core/context.py)

Environment for agent operation.

```python
# Create
ctx = Context.create(session_id="my_session")

# Set job type
ctx.set_job_type("content_generation")

# Memory
ctx.session_memory.set("key", "value")
value = ctx.session_memory.get("key")

# Agent list
ctx.update_agent_list("agent1", "thread1")
```

### 3. Job & Intent (src/core/job_types.py)

Work units that translate intent into goals.

```python
# Create job from user intent
job = Job.create(JobType.CONTENT_GENERATION, "Write an article")

# Add goals
job.add_goal(Goal(goal_id="g1", description="Research"))
job.add_goal(Goal(goal_id="g2", description="Draft", dependencies=["g1"]))

# Process goals
next_goal = job.get_next_ready_goal()  # Returns g1 (no dependencies)
job.progress.mark_complete("g1")
next_goal = job.get_next_ready_goal()  # Returns g2 (g1 completed)

# Check completion
job.is_complete()
```

### 4. Summary Storage (src/core/summary_storage.py)

Persistent knowledge across sessions.

```python
storage = SummaryStorage()

# Add experiences
storage.add_experience(Experience(source="reasoning", content="..."))

# Add rules
storage.add_rule(Rule(rule_id="r1", content="Be accurate", priority=1))

# Add important facts
storage.add_fact(ImportantFact(fact_id="f1", content="Key info"))

# Retrieve
storage.get_experiences(domain="coding")
storage.get_rules(rule_type="safety")
storage.get_facts(min_importance=0.7)

# Refine (consolidate, deduplicate)
storage.refine()
```

### 5. Interactions (src/interaction/)

Multi-agent collaboration patterns.

```python
# Sequential Interaction
seq = SequentialInteraction(agents=["agent_a", "agent_b"])
seq.config.agent_sequence = ["agent_a", "agent_b"]
result = seq.process("input data")

# Group Discuss
discuss = GroupDiscuss(agents=["a", "b", "c"])
discuss.consensus_method = ConsensusMethod.VOTING
result = discuss.discuss("Topic to discuss")

# Workflow Suggestion
wf = WorkflowSuggestion(agents=["a", "b"])
suggestions = wf.generate_suggestions("context")
result = wf.suggest_and_execute("workflow input")
```

### 6. Deployment Pool (src/display/deployment_pool.py)

Deploy and manage agents as services.

```python
pool = DeploymentPool()

# Deploy
op = pool.deploy(
    agent_id="my_agent",
    name="My Agent",
    version="v1.0",
    code_path="/path/to/code",
    config=DeploymentConfig(environment="local")
)

# Monitor
agent = pool.get_agent("my_agent")
print(agent.status)  # ONLINE, OFFLINE, BUILDING, ERROR

# Control
pool.stop("my_agent")
pool.restart("my_agent")
```

### 7. Mindset Modifier (src/display/mindset_modifier.py)

Configure agent thinking style.

```python
modifier = MindsetModifier(agent_id="my_agent")

# Apply preset
modifier.apply_preset("analytical")   # Deep reasoning
modifier.apply_preset("creative")     # High creativity
modifier.apply_preset("efficient")    # Fast, concise
modifier.apply_preset("thorough")       # Detailed, comprehensive

# Or adjust individually
modifier.adjust_verbosity(3)      # 1=concise, 5=verbose
modifier.adjust_reasoning_depth(5)  # 1=shallow, 5=deep
modifier.adjust_creativity(2)     # 1=rigid, 5=flexible

# Get configuration
config = modifier.get_current_configuration()
```

---

## JSON Configuration Example

```json
{
  "name": "content_writer",
  "description": "Writes high-quality content",

  "working_style": {
    "mode": "sequential",
    "input_type": "text",
    "output_type": "text"
  },

  "principle": {
    "core_principles": ["be accurate", "be helpful", "be clear"],
    "priority_order": ["accuracy", "helpfulness", "efficiency"],
    "constraint": {
      "max_iterations": 10,
      "max_time_seconds": 300
    },
    "fallback_strategy": "retry"
  },

  "action": {
    "monitor": {
      "track_progress": true,
      "track_resources": true
    },
    "planning": {
      "goal_decomposition": true,
      "subtask_generation": true
    },
    "reflecting": {
      "self_evaluation": true,
      "learn_from_experience": true
    }
  },

  "role": {
    "planner": {
      "list_of_plan": ["research", "outline", "draft", "revise"]
    },
    "guider": {
      "rule_set": {
        "must": ["cite sources", "check facts"],
        "must_not": ["plagiarize", "speculate without evidence"]
      }
    },
    "fact_judger": {
      "fact": {
        "compare_knowledge_base": true,
        "compare_internet": true
      }
    }
  }
}
```

---

## Input/Output Summary

| Component | Input | Output |
|-----------|-------|--------|
| `Agent.process()` | Any (data + context) | Any (result) |
| `Job.create()` | JobType + raw_input | Job with Intent |
| `IntentToGoalTransformer.transform()` | Intent | list[Goal] |
| `SequentialInteraction.process()` | Any | Processed result |
| `GroupDiscuss.discuss()` | Topic | dict with consensus |
| `WorkflowSuggestion.suggest_and_execute()` | Workflow input | dict with result + suggestions |
| `DeploymentPool.deploy()` | Agent config | DeploymentOperation |
| `MindsetModifier.get_configuration()` | - | dict with settings |

---

## Running Tests

```bash
# Run all tests
python -m pytest test_cases.py -v

# Run specific test class
python -m pytest test_cases.py::TestAgent -v

# Run with coverage
python -m pytest test_cases.py --cov=src --cov-report=html
```

---

## Module Dependencies

```
src/
├── __init__.py              # Package entry
├── core/
│   ├── agent.py             # ← Depends on nothing else in src
│   ├── context.py           # ← Depends on nothing
│   ├── job_types.py         # ← Depends on nothing
│   └── summary_storage.py   # ← Depends on nothing
├── building/
│   ├── agent_builder.py      # ← Uses core.agent
│   ├── factory_methods.py   # ← Uses core.agent
│   ├── config_delegation.py # ← Uses core.agent
│   └── tool_builder.py       # ← Uses core
├── interaction/
│   ├── interaction_manager.py # ← Uses other interaction modules
│   ├── sequential.py         # ← Uses nothing
│   ├── group_discuss.py      # ← Uses nothing
│   └── workflow_suggestion.py # ← Uses nothing
└── display/
    ├── display_manager.py     # ← Uses nothing
    ├── interaction_plan.py    # ← Uses nothing
    ├── deployment_pool.py     # ← Uses nothing
    └── mindset_modifier.py   # ← Uses nothing
```

---

## Important Notes

1. **Core is Independent**: The `core/` module has no internal dependencies - all classes can be used standalone.

2. **Building Builds on Core**: `building/` modules use `core/` classes to create and configure agents.

3. **Interaction is Independent**: `interaction/` modules work without core/building dependencies for flexibility.

4. **Display is Independent**: `display/` modules provide visualization and don't depend on other src modules.

5. **LLM Integration Needed**: Factory methods that generate code (`LLMFactory`) require actual LLM integration - currently raise `NotImplementedError`.

6. **Placeholder Implementations**: Some methods are placeholders for full implementation (e.g., actual agent execution).
