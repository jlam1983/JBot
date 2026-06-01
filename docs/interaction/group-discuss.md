# Group Discuss

## Overview

Group Discuss is a collaborative interaction pattern where multiple agents engage in discussion, debate, and synthesis to reach shared understanding or decisions.

---

## Characteristics

| Attribute | Description |
|-----------|-------------|
| **Structure** | Mesh, hub-spoke, or hierarchical |
| **Communication** | Broadcast, direct, or moderated |
| **Consensus** | Voting, negotiation, or arbitration |
| **Parallelism** | High (multiple agents simultaneously) |
| **Complexity** | Medium to High |

---

## Discussion Structures

### 1. Mesh Structure
```
     ┌───────┐
     │Agent A│◄──────►┌───────┐
     └───┬───┘        │Agent B│
         │◄──────►┌───┴───┬───┘◄─────►┌───────┐
         │        │Agent C│─────────►│Agent D│
         │◄──────►└───────┘◄──────►└───────┘
```
All agents communicate with all others. Best for complex, multi-perspective discussions.

### 2. Hub-Spoke Structure
```
           ┌───────┐
           │Moderator│
           └───┬───┘
         ┌─────┼─────┐
         ▼     ▼     ▼
    ┌───────┬───────┬───────┐
    │Agent A│Agent B│Agent C│
    └───────┴───────┴───────┘
```
Central moderator coordinates. Agents communicate through hub.

### 3. Hierarchical Structure
```
         ┌───────┐
         │Lead A │
      ┌──┴───┐   └──┐
      ▼      ▼      ▼
  ┌─────┐ ┌─────┐ ┌─────┐
  │Sub A│ │Sub B│ │Sub C│
  └─────┘ └─────┘ └─────┘
```
Lead agent coordinates subgroups. Efficient for large discussions.

---

## Discussion Roles

```json
"group_discuss_roles": {
  "moderator": {
    "responsibilities": ["manage_discussion_flow", "enforce_rules", "summarize_progress"]
  },
  "contributor": {
    "responsibilities": ["provide_perspectives", "respond_to_others", "build_on_ideas"]
  },
  "synthesizer": {
    "responsibilities": ["combine_ideas", "identify_common_threads", "resolve_conflicts"]
  },
  "critic": {
    "responsibilities": ["identify_weaknesses", "challenge_assumptions", "highlight_risks"]
  }
}
```

---

## Consensus Formation

```json
"consensus_formation": {
  "method": "voting | negotiation | arbitration | organic",
  "voting": {
    "type": "majority | unanimous | weighted",
    "abstention_allowed": true
  },
  "negotiation": {
    "enabled": true,
    "agents_trade_concessions": true
  },
  "arbitration": {
    "enabled": true,
    "arbitrator": "agent_id"
  }
}
```

---

## Discussion Flow

```
Opening → Sharing → Debate → Synthesis
```

1. **Opening**: Moderator introduces topic, establishes rules
2. **Sharing**: Each agent presents perspective
3. **Debate**: Agents respond and challenge
4. **Synthesis**: Common points identified, final position formed

---

## Use Cases

- **Multi-perspective Analysis**: Different angles on a topic
- **Brainstorming**: Generate diverse ideas
- **Decision Making**: Evaluate options, reach consensus
- **Code Review**: Multiple reviewers provide feedback
