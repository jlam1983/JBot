"""Interaction module - agent collaboration patterns."""

from .interaction_manager import InteractionManager, InteractionType
from .sequential import SequentialInteraction, ChainType
from .group_discuss import GroupDiscuss, DiscussionStructure, ConsensusMethod
from .workflow_suggestion import WorkflowSuggestion, SuggestionType, ValueAdditionPoint

__all__ = [
    "InteractionManager",
    "InteractionType",
    "SequentialInteraction",
    "ChainType",
    "GroupDiscuss",
    "DiscussionStructure",
    "ConsensusMethod",
    "WorkflowSuggestion",
    "SuggestionType",
    "ValueAdditionPoint",
]
