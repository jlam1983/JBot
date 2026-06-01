"""
Summary Storage - Long-term knowledge accumulation and refinement.

Based on docs/core/summary-storage.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Experience:
    """Learned knowledge from agent interactions."""
    source: str = ""  # reasoning_chain, decision_point, task_outcome
    content: str = ""
    domain: str = ""
    importance: float = 0.5
    frequency: int = 1
    confidence: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)

    def increment_frequency(self) -> None:
        self.frequency += 1

    def update_confidence(self, new_confidence: float) -> None:
        self.confidence = (self.confidence + new_confidence) / 2


@dataclass
class Rule:
    """A rule that agents should follow."""
    rule_id: str
    content: str
    rule_type: str = "behavioral"  # safety, behavioral, domain_specific
    priority: int = 1  # 1=high, 2=medium, 3=low
    enforcement: str = "advisory"  # strict, advisory
    source: str = "built_in"  # built_in, learned, user_defined
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "content": self.content,
            "rule_type": self.rule_type,
            "priority": self.priority,
            "enforcement": self.enforcement,
            "source": self.source,
            "enabled": self.enabled
        }


@dataclass
class ImportantFact:
    """Brief, important fact for easy retrieval."""
    fact_id: str
    content: str
    source: str = ""
    confidence: float = 1.0
    importance_score: float = 0.7
    domain: str = ""
    topic: str = ""
    last_verified: datetime = field(default_factory=datetime.now)

    def decay_importance(self, factor: float = 0.9) -> None:
        """Decay importance over time if not reinforced."""
        self.importance_score *= factor

    def reinforce(self, factor: float = 1.1) -> None:
        """Reinforce importance."""
        self.importance_score = min(1.0, self.importance_score * factor)


@dataclass
class Notice:
    """Brief observation or noteworthy item."""
    notice_id: str
    content: str
    agent_id: str = ""
    notice_type: str = "observation"  # observation, anomaly, pattern, suggestion
    alert_level: str | None = None  # info, warning, critical
    context: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "notice_id": self.notice_id,
            "content": self.content,
            "agent_id": self.agent_id,
            "notice_type": self.notice_type,
            "alert_level": self.alert_level,
            "timestamp": self.timestamp.isoformat()
        }


class StorageOperation:
    """Storage operation types."""

    ACCUMULATE = "accumulate"
    REFINEMENT = "refinement"
    RETRIEVE = "retrieve"


@dataclass
class SummaryStorage:
    """
    Summary Storage is a persistent knowledge management system
    that accumulates, refines, and organizes information across sessions.
    """
    experience_list: list[Experience] = field(default_factory=list)
    rules_list: list[Rule] = field(default_factory=list)
    facts_list: list[ImportantFact] = field(default_factory=list)
    notices_list: list[Notice] = field(default_factory=list)

    # Configuration
    max_experiences: int = 1000
    max_facts: int = 500
    importance_threshold: float = 0.3
    deduplication_threshold: float = 0.85

    # Storage backend (for future use)
    storage_backend: str = "memory"  # memory, vector_db, graph_db

    def add_experience(self, experience: Experience) -> None:
        """Add experience to storage."""
        # Check for duplicates
        for existing in self.experience_list:
            if self._is_similar(existing.content, experience.content):
                existing.increment_frequency()
                existing.update_confidence(experience.confidence)
                return

        # Apply retention policy
        if len(self.experience_list) >= self.max_experiences:
            self._prune_low_importance_experiences()

        self.experience_list.append(experience)

    def add_rule(self, rule: Rule) -> None:
        """Add rule to storage."""
        if rule.importance_score < self.importance_threshold:
            return
        self.rules_list.append(rule)

    def add_fact(self, fact: ImportantFact) -> None:
        """Add important fact to storage."""
        if len(self.facts_list) >= self.max_facts:
            self._prune_low_importance_facts()
        self.facts_list.append(fact)

    def add_notice(self, notice: Notice) -> None:
        """Add notice to storage."""
        self.notices_list.append(notice)

    def get_experiences(
        self,
        domain: str | None = None,
        min_importance: float = 0.0
    ) -> list[Experience]:
        """Retrieve experiences."""
        results = self.experience_list
        if domain:
            results = [e for e in results if e.domain == domain]
        if min_importance > 0:
            results = [e for e in results if e.importance >= min_importance]
        return results

    def get_rules(
        self,
        rule_type: str | None = None,
        enabled_only: bool = True
    ) -> list[Rule]:
        """Retrieve rules."""
        results = self.rules_list
        if rule_type:
            results = [r for r in results if r.rule_type == rule_type]
        if enabled_only:
            results = [r for r in results if r.enabled]
        return sorted(results, key=lambda r: r.priority)

    def get_facts(
        self,
        domain: str | None = None,
        min_importance: float = 0.0
    ) -> list[ImportantFact]:
        """Retrieve important facts."""
        results = self.facts_list
        if domain:
            results = [f for f in results if f.domain == domain]
        if min_importance > 0:
            results = [f for f in results if f.importance_score >= min_importance]
        return sorted(results, key=lambda f: f.importance_score, reverse=True)

    def get_notices(
        self,
        agent_id: str | None = None,
        notice_type: str | None = None
    ) -> list[Notice]:
        """Retrieve notices."""
        results = self.notices_list
        if agent_id:
            results = [n for n in results if n.agent_id == agent_id]
        if notice_type:
            results = [n for n in results if n.notice_type == notice_type]
        return results

    def refine(self) -> None:
        """Refine storage - consolidate, remove duplicates, prune."""
        self._consolidate_experiences()
        self._remove_duplicate_facts()
        self._prune_old_notices()

    def _is_similar(self, text1: str, text2: str, threshold: float = 0.85) -> bool:
        """Check if two texts are similar (simple implementation)."""
        # In production, use embeddings or more sophisticated comparison
        if not text1 or not text2:
            return False
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return False
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union >= threshold if union > 0 else False

    def _prune_low_importance_experiences(self) -> None:
        """Remove low importance experiences."""
        self.experience_list.sort(key=lambda e: e.importance)
        self.experience_list = self.experience_list[int(len(self.experience_list) * 0.2):]

    def _prune_low_importance_facts(self) -> None:
        """Remove low importance facts."""
        self.facts_list.sort(key=lambda f: f.importance_score)
        self.facts_list = self.facts_list[int(len(self.facts_list) * 0.2):]

    def _consolidate_experiences(self) -> None:
        """Consolidate similar experiences."""
        consolidated = []
        for exp in self.experience_list:
            found = False
            for existing in consolidated:
                if self._is_similar(exp.content, existing.content):
                    existing.increment_frequency()
                    existing.update_confidence(exp.confidence)
                    found = True
                    break
            if not found:
                consolidated.append(exp)
        self.experience_list = consolidated

    def _remove_duplicate_facts(self) -> None:
        """Remove duplicate facts."""
        seen = set()
        unique = []
        for fact in self.facts_list:
            if fact.content not in seen:
                seen.add(fact.content)
                unique.append(fact)
        self.facts_list = unique

    def _prune_old_notices(self) -> None:
        """Remove old ephemeral notices."""
        self.notices_list = [
            n for n in self.notices_list
            if n.notice_type != "observation" or
            (datetime.now() - n.timestamp).days < 7
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_count": len(self.experience_list),
            "rules_count": len(self.rules_list),
            "facts_count": len(self.facts_list),
            "notices_count": len(self.notices_list)
        }


class CrossAgentSummary:
    """Cross-agent knowledge sharing."""

    def __init__(self, storage: SummaryStorage):
        self.storage = storage
        self.enabled = True
        self.sync_strategy = "real_time"

    def share_to_storage(
        self,
        agent_id: str,
        experience: Experience | None = None,
        rule: Rule | None = None,
        fact: ImportantFact | None = None
    ) -> None:
        """Share knowledge to storage."""
        if experience:
            if experience.source == "":
                experience.source = agent_id
            self.storage.add_experience(experience)
        if rule:
            self.storage.add_rule(rule)
        if fact:
            self.storage.add_fact(fact)

    def aggregate_perspectives(
        self,
        agent_perspectives: dict[str, list[str]]
    ) -> list[Experience]:
        """Aggregate experiences from different agent perspectives."""
        aggregated = []
        for agent_id, sources in agent_perspectives.items():
            for source in sources:
                exp = Experience(source=source, content=f"Perspective of {agent_id}")
                aggregated.append(exp)
        return aggregated
