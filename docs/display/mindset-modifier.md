# Mindset Modifier

## Overview

Mindset Modifier provides visibility into and control over how agents generate prompts and process thoughts.

---

## Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  Agent Mindset: [Planner Agent ▼]                    [🔄 Sync]  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  ┌─────────────────────────────┐   │
│  │   Thought Process       │  │   Prompt Generation         │   │
│  ├─────────────────────────┤  ├─────────────────────────────┤   │
│  │  1. Intent Parsing      │  │  System Prompt:            │   │
│  │     ↓                   │  │  [You are a planner...]   │   │
│  │  2. Context Load        │  │                             │   │
│  │     ↓                   │  │  User Input:               │   │
│  │  3. Plan Generation ●   │  │  [Plan the following...]   │   │
│  │     ↓                   │  │                             │   │
│  │  4. Strategy Select     │  │  Final Prompt:             │   │
│  │                         │  │  [Full assembled prompt]   │   │
│  │  Confidence: 87%        │  │                             │   │
│  └─────────────────────────┘  └─────────────────────────────┘   │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │  Thinking Style: [Analytical ▼]                           │   │
│  │  Verbosity:      [●●●○○ Medium]                          │   │
│  │  Reasoning Depth: [●●●●○ Deep]                           │   │
│  │  [Apply Changes]  [Reset to Default]  [Save Preset]     │   │
│  └───────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Thought Process Viewer

### Current Phase Detail
```json
"thought_process": {
  "current_phase": "plan_generation",
  "phase_history": [
    {"phase": "intent_parsing", "status": "completed", "output": {...}},
    {"phase": "context_loading", "status": "completed", "output": {...}},
    {"phase": "plan_generation", "status": "in_progress", "output": {...}}
  ]
}
```

### Step Controls
| Action | Description |
|--------|-------------|
| **Step Back** | View previous phase |
| **Step Forward** | Advance to next phase |
| **View All** | See complete history |

---

## Prompt Generation Viewer

### Prompt Components
```json
"prompt_generation": {
  "system_prompt": {
    "components": [
      {"type": "role_definition", "content": "You are a planner agent"},
      {"type": "capability_list", "content": "You can: analyze, plan..."},
      {"type": "constraint_list", "content": "Always consider..."}
    ]
  },
  "context_injection": {
    "enabled": true,
    "injected_content": [
      {"type": "memory", "content": "Previous project..."},
      {"type": "preference", "content": "User prefers..."}
    ]
  }
}
```

---

## Feedback to Client

```json
"response_generation": {
  "raw_output": {
    "content": "Based on your requirements...",
    "confidence": 0.85
  },
  "feedback_to_user": {
    "summary": "Plan created successfully",
    "next_steps": ["Review plan", "Approve milestones"],
    "suggestion": "Consider breaking phase 2 into smaller tasks"
  }
}
```

---

## Mindset Configuration

### Configuration Sliders

| Setting | Range | Description |
|---------|-------|-------------|
| **Thinking Style** | Analytical ← → Creative | How agent approaches problems |
| **Verbosity** | Concise ← → Verbose | Detail in responses |
| **Reasoning Depth** | Shallow ← → Deep | Analysis depth |
| **Creativity** | Rigid ← → Flexible | Alternative exploration |

### Presets
```json
"presets": {
  "analytical": {"thinking_style": "analytical", "reasoning_depth": 5},
  "creative": {"thinking_style": "creative", "creativity": 5},
  "efficient": {"thinking_style": "practical", "verbosity": 2},
  "thorough": {"thinking_style": "analytical", "reasoning_depth": 5, "verbosity": 4}
}
```

---

## Feedback Loop

```
Observe Mindset → Modify Config → Agent Adjusts → Feedback Loop
```

### Adjustment Actions

| Action | Effect |
|--------|--------|
| **Increase Depth** | More reasoning steps |
| **Decrease Depth** | Faster, surface-level |
| **Increase Creativity** | More alternatives |
| **Decrease Verbosity** | Shorter responses |

---

## Use Cases

1. **Debug Thinking**: See exactly how agent processes input
2. **Tune Style**: Adjust verbosity, depth, creativity
3. **Optimize Prompts**: View real-time prompt generation
4. **Quality Assurance**: Verify agent reasoning is sound
