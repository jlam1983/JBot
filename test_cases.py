"""
Test Cases for JLLMBot

Run with: python -m pytest test_cases.py -v
"""

import pytest
from src.core.agent import (
    Agent, AgentConfig, WorkingStyle, Principle,
    WorkingMode, FallbackStrategy, AgentRoles,
    AgentActions, PlannerRole, GuiderRole, WorkerRole
)
from src.core.context import Context, SessionMemory, StaticAgentList
from src.core.job_types import Job, JobType, Intent, Goal, IntentToGoalTransformer
from src.core.summary_storage import SummaryStorage, Experience, Rule, ImportantFact, Notice
from src.building.agent_builder import AgentBuilder, BuildMethod
from src.building.factory_methods import ConfigFactory, SharedAPI
from src.interaction.interaction_manager import InteractionManager, InteractionType
from src.interaction.sequential import SequentialInteraction, ChainType
from src.interaction.group_discuss import GroupDiscuss, DiscussionStructure, ConsensusMethod
from src.interaction.workflow_suggestion import WorkflowSuggestion, SuggestionType
from src.display.deployment_pool import DeploymentPool, AgentStatus, DeploymentConfig
from src.display.mindset_modifier import MindsetModifier, ThinkingStyle


# =============================================================================
# Core - Agent Tests
# =============================================================================

class TestAgentConfig:
    """Tests for AgentConfig."""

    def test_create_basic_config(self):
        """Test creating a basic agent configuration."""
        config = AgentConfig(name="test_agent", description="A test agent")
        assert config.name == "test_agent"
        assert config.description == "A test agent"

    def test_create_from_dict(self):
        """Test creating config from dictionary."""
        data = {
            "name": "planner_agent",
            "description": "Plans tasks",
            "working_style": {
                "mode": "sequential",
                "input_type": "text",
                "output_type": "structured"
            },
            "principle": {
                "core_principles": ["be accurate", "be helpful"],
                "priority_order": ["safety", "accuracy"],
                "constraint": {"max_iterations": 5}
            },
            "role": {
                "planner": {"list_of_plan": ["step1", "step2"]}
            }
        }
        config = AgentConfig.from_dict(data)
        assert config.name == "planner_agent"
        assert config.working_style.mode.value == "sequential"
        assert config.principle.core_principles == ["be accurate", "be helpful"]

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = AgentConfig(name="test")
        result = config.to_dict()
        assert result["name"] == "test"
        assert "working_style" in result
        assert "principle" in result


class TestAgent:
    """Tests for Agent class."""

    def test_create_agent_from_config(self):
        """Test creating an agent with config."""
        config = AgentConfig(name="my_agent")
        agent = Agent(config)
        assert agent.name == "my_agent"

    def test_create_agent_from_dict(self):
        """Test creating an agent with dictionary."""
        data = {"name": "dict_agent", "description": "Created from dict"}
        agent = Agent(data)
        assert agent.name == "dict_agent"

    def test_agent_repr(self):
        """Test agent string representation."""
        config = AgentConfig(name="repr_test")
        agent = Agent(config)
        assert "repr_test" in repr(agent)


# =============================================================================
# Core - Context Tests
# =============================================================================

class TestSessionMemory:
    """Tests for SessionMemory."""

    def test_create_session(self):
        """Test creating a session."""
        session = SessionMemory()
        assert session.session_id is not None
        assert session.short_term == {}
        assert session.long_term == {}

    def test_set_and_get(self):
        """Test setting and getting values."""
        session = SessionMemory()
        session.set("key1", "value1")
        assert session.get("key1") == "value1"

    def test_long_term_storage(self):
        """Test long-term memory storage."""
        session = SessionMemory()
        session.set("persistent", "data", long_term=True)
        assert session.get("persistent") == "data"
        assert "persistent" in session.long_term

    def test_delete(self):
        """Test deleting values."""
        session = SessionMemory()
        session.set("to_delete", "value")
        session.delete("to_delete")
        assert session.get("to_delete") is None

    def test_clear_short_term(self):
        """Test clearing short-term memory."""
        session = SessionMemory()
        session.set("temp", "data")
        session.clear_short_term()
        assert session.get("temp") is None


class TestContext:
    """Tests for Context."""

    def test_create_context(self):
        """Test creating a context."""
        ctx = Context.create(session_id="test_session")
        assert ctx.session_memory.session_id == "test_session"

    def test_set_job_type(self):
        """Test setting job type."""
        ctx = Context.create()
        ctx.set_job_type("content_generation")
        assert ctx.get_job_type() == "content_generation"


class TestStaticAgentList:
    """Tests for StaticAgentList."""

    def test_add_agent(self):
        """Test adding agents."""
        agent_list = StaticAgentList()
        agent_list.add_agent("agent1", "thread1")
        assert "agent1" in agent_list.threads["thread1"]
        assert agent_list.get_agent_status("agent1") == "online"

    def test_remove_agent(self):
        """Test removing agents."""
        agent_list = StaticAgentList()
        agent_list.add_agent("agent1")
        agent_list.remove_agent("agent1")
        assert agent_list.get_agent_status("agent1") is None


# =============================================================================
# Core - Job Types Tests
# =============================================================================

class TestIntent:
    """Tests for Intent."""

    def test_create_intent(self):
        """Test creating an intent."""
        intent = Intent(raw_input="Build a web app")
        assert intent.raw_input == "Build a web app"

    def test_interpret_intent(self):
        """Test interpreting intent."""
        intent = Intent(raw_input="Create API")
        intent.interpret()
        assert intent.interpreted_purpose == "Create API"

    def test_add_constraint(self):
        """Test adding constraints."""
        intent = Intent(raw_input="Test")
        intent.add_constraint("must be fast")
        assert "must be fast" in intent.constraints


class TestGoal:
    """Tests for Goal."""

    def test_create_goal(self):
        """Test creating a goal."""
        goal = Goal(goal_id="g1", description="Test goal")
        assert goal.goal_id == "g1"
        assert not goal.completed

    def test_goal_blocked(self):
        """Test goal blocking logic."""
        goal = Goal(goal_id="g1", description="Test", dependencies=["g0"])
        assert goal.is_blocked(set())  # Blocked when g0 not completed
        assert not goal.is_blocked({"g0"})  # Not blocked when g0 completed


class TestJob:
    """Tests for Job."""

    def test_create_job(self):
        """Test creating a job."""
        job = Job.create(JobType.CONTENT_GENERATION, "Write an article")
        assert job.job_type == JobType.CONTENT_GENERATION
        assert job.intent.raw_input == "Write an article"

    def test_add_goals(self):
        """Test adding goals to job."""
        job = Job.create(JobType.WORKFLOW_RUNNER, "Process data")
        job.add_goal(Goal(goal_id="g1", description="Step 1"))
        job.add_goal(Goal(goal_id="g2", description="Step 2"))
        assert len(job.goals) == 2

    def test_job_completion(self):
        """Test job completion check."""
        job = Job.create(JobType.PLANNING, "Plan project")
        job.add_goal(Goal(goal_id="g1", description="Step 1"))
        assert not job.is_complete()
        job.goals[0].completed = True
        assert job.is_complete()


class TestIntentToGoalTransformer:
    """Tests for IntentToGoalTransformer."""

    def test_transform_intent(self):
        """Test transforming intent to goals."""
        transformer = IntentToGoalTransformer()
        intent = Intent(raw_input="Build API")
        intent.add_constraint("RESTful")
        goals = transformer.transform(intent)
        assert len(goals) > 0
        assert any("RESTful" in g.description for g in goals)


# =============================================================================
# Core - Summary Storage Tests
# =============================================================================

class TestSummaryStorage:
    """Tests for SummaryStorage."""

    def test_create_storage(self):
        """Test creating storage."""
        storage = SummaryStorage()
        assert len(storage.experience_list) == 0

    def test_add_experience(self):
        """Test adding experience."""
        storage = SummaryStorage()
        exp = Experience(source="reasoning_chain", content="Test reasoning")
        storage.add_experience(exp)
        assert len(storage.experience_list) == 1

    def test_add_rule(self):
        """Test adding rules."""
        storage = SummaryStorage()
        rule = Rule(rule_id="r1", content="Be helpful", priority=1)
        storage.add_rule(rule)
        assert len(storage.rules_list) == 1

    def test_add_fact(self):
        """Test adding important facts."""
        storage = SummaryStorage()
        fact = ImportantFact(fact_id="f1", content="Key fact")
        storage.add_fact(fact)
        assert len(storage.facts_list) == 1

    def test_get_rules_by_type(self):
        """Test filtering rules by type."""
        storage = SummaryStorage()
        storage.add_rule(Rule(rule_id="r1", content="Safety rule", rule_type="safety", priority=1))
        storage.add_rule(Rule(rule_id="r2", content="Behavior rule", rule_type="behavioral", priority=2))
        safety_rules = storage.get_rules(rule_type="safety")
        assert len(safety_rules) == 1

    def test_deduplication(self):
        """Test experience deduplication."""
        storage = SummaryStorage()
        exp1 = Experience(source="test", content="Same content", confidence=0.8)
        exp2 = Experience(source="test", content="Same content", confidence=0.9)
        storage.add_experience(exp1)
        storage.add_experience(exp2)
        # Should be deduplicated (1 instead of 2)
        assert len(storage.experience_list) == 1

    def test_storage_refinement(self):
        """Test storage refinement."""
        storage = SummaryStorage()
        storage.add_experience(Experience(source="test", content="Content 1"))
        storage.add_experience(Experience(source="test", content="Content 1"))  # Duplicate
        storage.refine()
        # Should consolidate duplicates
        assert len(storage.experience_list) <= 2


# =============================================================================
# Building - Agent Builder Tests
# =============================================================================

class TestAgentBuilder:
    """Tests for AgentBuilder."""

    def test_create_builder(self):
        """Test creating agent builder."""
        builder = AgentBuilder()
        assert builder.build_method == BuildMethod.CONFIG_EXISTING

    def test_build_from_existing(self):
        """Test building from existing config."""
        builder = AgentBuilder(build_method=BuildMethod.CONFIG_EXISTING)
        data = {"name": "built_agent"}
        agent = builder.build_from_config(data)
        assert agent.name == "built_agent"

    def test_plugin_management(self):
        """Test plugin add/remove."""
        builder = AgentBuilder()
        assert builder.add_plugin("test_plugin") is True
        assert builder.remove_plugin("test_plugin") is True


# =============================================================================
# Building - Factory Tests
# =============================================================================

class TestConfigFactory:
    """Tests for ConfigFactory."""

    def test_create_from_config(self):
        """Test creating agent from config."""
        factory = ConfigFactory()
        data = {"name": "factory_agent", "description": "Via factory"}
        agent = factory.create(data)
        assert agent.name == "factory_agent"


class TestSharedAPI:
    """Tests for SharedAPI."""

    def test_register_category(self):
        """Test registering a category."""
        api = SharedAPI()
        api.register_category("judger", "JudgeInterface", ["FactJudger", "ValueJudger"], ["evaluate"])
        assert api.get_category("judger") is not None

    def test_list_categories(self):
        """Test listing categories."""
        api = SharedAPI()
        api.register_category("judger", "Interface", [], [])
        api.register_category("generator", "Interface", [], [])
        cats = api.list_categories()
        assert len(cats) == 2


# =============================================================================
# Interaction - Sequential Tests
# =============================================================================

class TestSequentialInteraction:
    """Tests for SequentialInteraction."""

    def test_create_sequential(self):
        """Test creating sequential interaction."""
        seq = SequentialInteraction(agents=["a", "b", "c"])
        assert len(seq.agents) == 3

    def test_process_sequential(self):
        """Test processing through chain."""
        seq = SequentialInteraction(agents=["a", "b"])
        seq.config.agent_sequence = ["a", "b"]
        result = seq.process("input")
        assert "a:" in result
        assert "b:" in result


# =============================================================================
# Interaction - Group Discuss Tests
# =============================================================================

class TestGroupDiscuss:
    """Tests for GroupDiscuss."""

    def test_create_group_discuss(self):
        """Test creating group discuss."""
        discuss = GroupDiscuss(agents=["a", "b", "c"])
        assert len(discuss.agents) == 3
        assert discuss.structure == DiscussionStructure.MESH

    def test_discuss_phases(self):
        """Test discussion phases initialization."""
        discuss = GroupDiscuss(agents=["a"])
        assert len(discuss.phases) == 4  # opening, sharing, debate, synthesis

    def test_run_discussion(self):
        """Test running a discussion."""
        discuss = GroupDiscuss(agents=["a", "b"])
        discuss.consensus_method = ConsensusMethod.VOTING
        result = discuss.discuss("What is the best approach?")
        assert "topic" in result
        assert result["consensus"] is not None


# =============================================================================
# Interaction - Workflow Suggestion Tests
# =============================================================================

class TestWorkflowSuggestion:
    """Tests for WorkflowSuggestion."""

    def test_create_workflow_suggestion(self):
        """Test creating workflow suggestion."""
        wf = WorkflowSuggestion(agents=["a", "b"])
        assert len(wf.agents) == 2

    def test_generate_suggestions(self):
        """Test generating suggestions."""
        wf = WorkflowSuggestion()
        suggestions = wf.generate_suggestions("context")
        assert len(suggestions) > 0

    def test_suggestion_accept(self):
        """Test accepting a suggestion."""
        from src.interaction.workflow_suggestion import Suggestion, SuggestionType
        suggestion = Suggestion(
            suggestion_type=SuggestionType.PROCESS_ENHANCEMENT,
            description="Test"
        )
        suggestion.accept()
        assert suggestion.accepted is True


# =============================================================================
# Interaction - Interaction Manager Tests
# =============================================================================

class TestInteractionManager:
    """Tests for InteractionManager."""

    def test_create_manager(self):
        """Test creating interaction manager."""
        manager = InteractionManager()
        assert manager.current_type == InteractionType.SEQUENTIAL

    def test_add_remove_agents(self):
        """Test adding and removing agents."""
        manager = InteractionManager()
        manager.add_agent("agent1")
        manager.remove_agent("agent1")
        assert "agent1" not in manager.agents_in_context


# =============================================================================
# Display - Deployment Pool Tests
# =============================================================================

class TestDeploymentPool:
    """Tests for DeploymentPool."""

    def test_create_pool(self):
        """Test creating deployment pool."""
        pool = DeploymentPool()
        assert len(pool.deployed_agents) == 0

    def test_deploy_agent(self):
        """Test deploying an agent."""
        pool = DeploymentPool()
        config = DeploymentConfig(environment="local")
        op = pool.deploy("agent1", "Test Agent", "v1.0", "/path/to/code", config)
        assert op.agent_id == "agent1"
        assert pool.get_agent("agent1") is not None

    def test_stop_agent(self):
        """Test stopping an agent."""
        pool = DeploymentPool()
        pool.deploy("agent1", "Test", "v1", "/code")
        assert pool.stop("agent1") is True
        assert pool.get_agent("agent1").status == AgentStatus.OFFLINE

    def test_list_agents_by_status(self):
        """Test listing agents by status."""
        pool = DeploymentPool()
        pool.deploy("agent1", "A", "v1", "/code")
        pool.deploy("agent2", "B", "v1", "/code")
        pool.stop("agent1")
        online = pool.list_agents(status=AgentStatus.ONLINE)
        offline = pool.list_agents(status=AgentStatus.OFFLINE)
        assert len(online) >= 1
        assert len(offline) >= 1


# =============================================================================
# Display - Mindset Modifier Tests
# =============================================================================

class TestMindsetModifier:
    """Tests for MindsetModifier."""

    def test_create_modifier(self):
        """Test creating mindset modifier."""
        modifier = MindsetModifier(agent_id="test_agent")
        assert modifier.agent_id == "test_agent"
        assert modifier.thinking_style == ThinkingStyle.ANALYTICAL

    def test_apply_preset(self):
        """Test applying configuration preset."""
        modifier = MindsetModifier()
        modifier.apply_preset("creative")
        assert modifier.thinking_style == ThinkingStyle.CREATIVE
        assert modifier.creativity == 5

    def test_adjust_verbosity(self):
        """Test adjusting verbosity."""
        modifier = MindsetModifier()
        modifier.adjust_verbosity(5)
        assert modifier.verbosity == 5

    def test_get_configuration(self):
        """Test getting current configuration."""
        modifier = MindsetModifier()
        config = modifier.get_current_configuration()
        assert "thinking_style" in config
        assert "verbosity" in config


# =============================================================================
# Integration Tests
# =============================================================================

class TestEndToEndAgent:
    """End-to-end tests for agent creation and execution."""

    def test_full_agent_lifecycle(self):
        """Test complete agent lifecycle."""
        # 1. Create context
        ctx = Context.create(session_id="test")

        # 2. Create agent
        data = {
            "name": "lifecycle_test",
            "working_style": {"mode": "sequential"},
            "role": {
                "planner": {"list_of_plan": ["think", "act", "review"]}
            }
        }
        agent = Agent(data)
        assert agent.name == "lifecycle_test"

        # 3. Create job
        job = Job.create(JobType.CONTENT_GENERATION, "Write documentation")
        job.add_goal(Goal(goal_id="g1", description="Research"))
        job.add_goal(Goal(goal_id="g2", description="Draft", dependencies=["g1"]))
        assert not job.is_complete()

    def test_agent_with_storage(self):
        """Test agent with summary storage."""
        storage = SummaryStorage()
        storage.add_experience(Experience(source="test", content="Learned something"))
        storage.add_rule(Rule(rule_id="r1", content="Be accurate", priority=1))

        # Retrieve
        experiences = storage.get_experiences()
        rules = storage.get_rules(enabled_only=True)
        assert len(experiences) == 1
        assert len(rules) == 1


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
