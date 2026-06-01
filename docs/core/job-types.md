# Job Types

## Overview

Jobs are fundamental units of work that agents execute to fulfill user intent. Each job type serves a distinct purpose but shares a common goal: translating abstract user intent into actionable outcomes.

---

## Core Concept: Intent vs Goal

```
┌─────────────────────────────────────────────────────────────┐
│                      User Intent                             │
│                   (Abstract Purpose)                         │
│                  "What the user wants"                       │
│                  "Why they want it"                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │    Interpretation   │
                    │   & Decomposition   │
                    └─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Goals                                 │
│                  (Situational Implementation)                │
│                 "How to achieve intent"                      │
│                "What steps to take"                          │
└─────────────────────────────────────────────────────────────┘
```

### User Intent

- **Type:** Abstract, high-level purpose
- **Description:** The underlying need or goal the user wants to accomplish
- **Characteristics:**
  - Often stated as "I want to...", "I need to...", "I should..."
  - May be implicit or explicitly stated
  - Can be multi-faceted (primary intent + secondary intents)
  - Serves as the anchor for all downstream decisions

### Goals

- **Type:** Concrete, situational implementation steps
- **Description:** Specific actions or milestones to achieve the intent
- **Characteristics:**
  - Derived from interpreting the user intent
  - Adaptable to current situation/context
  - Can be dynamically adjusted based on progress
  - Measurable and verifiable

### Intent → Goal Transformation

```json
"intent_to_goal": {
  "interpretation": {
    "clarify_ambiguity": true,
    "identify_constraints": true,
    "extract_implicit_needs": true
  },
  "decomposition": {
    "break_into_sub_goals": true,
    "identify_dependencies": true,
    "prioritize_by_importance": true
  },
  "advanced_suggestion": {
    "enabled": true,
    "suggest_alternatives": true,
    "propose_improvements": true,
    "anticipate_follow_up": true
  }
}
```

---

## Job Types Summary

| Job Type | Purpose | Phases |
|----------|---------|--------|
| **Content Generation** | Produce text, code, media | Requirement → Planning → Drafting → Refinement |
| **Research/Discuss** | Investigate & discuss topics | Gathering → Analysis → Discussion |
| **Workflow Runner** | Execute multi-step processes | Planning → Setup → Execution → Completion |
| **Problem Solving** | Identify & resolve issues | Analysis → Root Cause → Solution |
| **Planning** | Create strategic plans | Clarification → Strategy → Plan → Contingency |

---

## 1. Content Generation

```json
"content_generation": {
  "purpose": "Produce text, code, or media that fulfills user intent",
  "goal_breakdown": {
    "requirement_analysis": {
      "goals": ["understand_topic", "identify_audience", "determine_format"]
    },
    "content_planning": {
      "goals": ["outline_structure", "determine_key_points", "plan_transitions"]
    },
    "drafting": {
      "goals": ["write_content", "incorporate_examples", "ensure_clarity"]
    },
    "refinement": {
      "goals": ["review_accuracy", "polish_language", "format_output"]
    }
  }
}
```

---

## 2. Research/Discuss

```json
"research_discuss": {
  "purpose": "Investigate, analyze, and discuss topics to provide insights",
  "goal_breakdown": {
    "information_gathering": {
      "goals": ["collect_relevant_data", "identify_sources", "verify_credibility"]
    },
    "analysis": {
      "goals": ["identify_patterns", "evaluate_evidence", "synthesize_findings"]
    },
    "discussion": {
      "goals": ["present_findings", "address_questions", "explore_perspectives"]
    }
  }
}
```

---

## 3. Workflow Runner

```json
"workflow_runner": {
  "purpose": "Coordinate and execute sequential or parallel tasks",
  "goal_breakdown": {
    "workflow_planning": {
      "goals": ["define_steps", "identify_resources", "map_dependencies"]
    },
    "execution_setup": {
      "goals": ["initialize_resources", "validate_prerequisites", "prepare_environment"]
    },
    "step_execution": {
      "goals": ["execute_current_step", "handle_errors", "update_progress"]
    },
    "completion": {
      "goals": ["verify_outcomes", "cleanup_resources", "report_results"]
    }
  }
}
```

---

## 4. Problem Solving

```json
"problem_solving": {
  "purpose": "Identify root causes and implement solutions",
  "goal_breakdown": {
    "problem_analysis": {
      "goals": ["define_problem", "gather_symptoms", "identify_constraints"]
    },
    "root_cause_analysis": {
      "goals": ["investigate_causes", "test_hypotheses", "identify_fixes"]
    },
    "solution_implementation": {
      "goals": ["plan_fix", "implement_solution", "verify_resolution"]
    }
  }
}
```

---

## 5. Planning

```json
"planning": {
  "purpose": "Develop actionable plans from abstract intent",
  "goal_breakdown": {
    "goal_clarification": {
      "goals": ["clarify_intent", "set_objectives", "define_success_metrics"]
    },
    "strategy_development": {
      "goals": ["identify_approaches", "evaluate_options", "select_strategy"]
    },
    "plan_creation": {
      "goals": ["break_into_tasks", "sequence_tasks", "assign_resources"]
    },
    "contingency_planning": {
      "goals": ["identify_risks", "plan_alternatives", "define_milestones"]
    }
  }
}
```

---

## Universal Job Structure

```json
"job_structure": {
  "user_intent": {
    "raw_input": "string",
    "interpreted_purpose": "string",
    "implied_needs": ["string"],
    "constraints": ["string"]
  },
  "goals": {
    "primary_goal": "string",
    "sub_goals": ["string"],
    "dependencies": {"goal_id": ["prerequisite_ids"]},
    "priority_order": ["goal_id"]
  },
  "progress_tracking": {
    "current_phase": "string",
    "completed_goals": ["goal_id"],
    "pending_goals": ["goal_id"]
  },
  "requirements_for_action": {
    "prerequisites": ["string"],
    "inputs_needed": ["string"],
    "outputs_expected": ["string"]
  }
}
```

---

## Goal Breakdown Process

```
User Intent → Interpret → Decompose → Prioritize → Plan → Execute → Validate
```

1. **Interpret**: Extract purpose, identify constraints
2. **Decompose**: Break into sub-goals, identify dependencies
3. **Prioritize**: Order by importance, urgency, dependencies
4. **Plan**: Convert goals to actionable tasks
5. **Execute**: Perform tasks, track progress
6. **Validate**: Check if intent has been fulfilled

---

## Advanced Suggestions

```json
"advanced_suggestions": {
  "enabled": true,
  "types": {
    "process_improvement": "Suggest improved workflows",
    "scope_expansion": "Suggest related additions",
    "risk_alert": "Warn about potential issues",
    "alternative_intent": "Propose simpler paths"
  }
}
```

---

## Usage Notes

- User intent anchors all goals and actions
- Advanced suggestions leverage abstract purpose to propose improvements
- Each job type has distinct phases but shares the universal structure
- Progress tracking enables visibility and course correction
