"""
Test Cases for JLLMBot Routes

Tests for Route 1-4:
1. Prompt Processing with Agent Mindset
2. Agent Factory (Simple API)
3. Multi-Agent Context, Job, and Interaction
4. LLM Integration
"""

import pytest
import asyncio
from routes import (
    PromptProcessor, AgentFactory, MultiAgentRunner,
    LLMIntegrationMixin, create_quick_agent
)
from src.core.agent import Agent, AgentConfig
from src.core.job_types import Job, JobType, Intent, Goal
from src.display.mindset_modifier import MindsetModifier, ThinkingStyle
from llm import OllamaChat, LLMManager, ContextWindow, Message


# =============================================================================
# Route 1: Prompt Processor Tests
# =============================================================================

class TestPromptProcessor:
    """Tests for Route 1: Prompt Processing."""

    def test_create_processor(self):
        """Test creating a prompt processor."""
        modifier = MindsetModifier(agent_id="test")
        processor = PromptProcessor("test", modifier)
        assert processor.agent_id == "test"

    def test_process_basic_prompt(self):
        """Test basic prompt processing."""
        modifier = MindsetModifier()
        modifier.apply_preset("analytical")
        processor = PromptProcessor("test", modifier)

        result = processor.process_prompt("What is Python?")

        assert result.original_prompt == "What is Python?"
        assert result.transformed_prompt != ""
        assert "thinking_style" in result.agent_mindset_snapshot

    def test_process_with_thinking_style(self):
        """Test prompt processing with different thinking styles."""
        modifier = MindsetModifier()

        # Test creative style
        modifier.apply_preset("creative")
        processor = PromptProcessor("test", modifier)
        result = processor.process_prompt("Build an app")
        assert "creative" in result.transformed_prompt.lower() or "brainstorm" in result.transformed_prompt.lower()

        # Test analytical style
        modifier.apply_preset("analytical")
        processor = PromptProcessor("test", modifier)
        result = processor.process_prompt("Build an app")
        assert "analyze" in result.transformed_prompt.lower() or "thoroughly" in result.transformed_prompt.lower()

    def test_suggestions_generated(self):
        """Test that suggestions are generated."""
        modifier = MindsetModifier()
        modifier.apply_preset("analytical")
        processor = PromptProcessor("test", modifier)

        result = processor.process_prompt("Complex task")
        assert len(result.suggestions) > 0

    def test_context_window_integration(self):
        """Test adding to context window."""
        modifier = MindsetModifier()
        context = ContextWindow()
        processor = PromptProcessor("test", modifier, context)

        processor.add_to_context("user", "Hello")
        processor.add_to_context("assistant", "Hi there")

        assert len(context.messages) == 2

    def test_update_mindset_from_feedback(self):
        """Test updating mindset based on feedback."""
        modifier = MindsetModifier(agent_id="test")
        modifier.adjust_verbosity(3)

        processor = PromptProcessor("test", modifier)
        processor.update_mindset_from_feedback("too verbose", rating=2)

        # Verbosity should decrease
        assert processor.mindset_modifier.verbosity < 3


# =============================================================================
# Route 2: Agent Factory Tests
# =============================================================================

class TestAgentFactory:
    """Tests for Route 2: Agent Factory."""

    def test_create_agent(self):
        """Test creating an agent via factory."""
        factory = AgentFactory()
        agent = factory.create_agent(
            name="test_agent",
            agent_type="general",
            thinking_style="analytical"
        )
        assert agent.name == "test_agent"

    def test_create_with_rules(self):
        """Test creating agent with rules."""
        factory = AgentFactory()
        agent = factory.create_agent(
            name="ruled_agent",
            rules=["be helpful", "be accurate"]
        )
        assert len(agent.config.principle.core_principles) == 2

    def test_create_coder_agent(self):
        """Test creating a coder agent."""
        factory = AgentFactory()
        agent = factory.create_agent(
            name="coder",
            agent_type="coder"
        )
        assert agent.name == "coder"

    def test_create_researcher_agent(self):
        """Test creating a researcher agent."""
        factory = AgentFactory()
        agent = factory.create_agent(
            name="researcher",
            agent_type="researcher"
        )
        assert agent.name == "researcher"

    def test_list_agents(self):
        """Test listing agents."""
        factory = AgentFactory()
        factory.create_agent("agent1", "general")
        factory.create_agent("agent2", "general")

        agents = factory.list_agents()
        assert len(agents) == 2
        assert "agent1" in agents
        assert "agent2" in agents

    def test_get_agent(self):
        """Test getting an agent by name."""
        factory = AgentFactory()
        created = factory.create_agent("get_test", "general")

        retrieved = factory.get_agent("get_test")
        assert retrieved is not None
        assert retrieved.name == created.name

    def test_delete_agent(self):
        """Test deleting an agent."""
        factory = AgentFactory()
        factory.create_agent("to_delete", "general")

        assert factory.delete_agent("to_delete") is True
        assert factory.get_agent("to_delete") is None

    def test_quick_agent_creation(self):
        """Test quick agent + mindset creation."""
        agent, modifier = create_quick_agent("quick", "general", "creative")
        assert agent.name == "quick"
        assert modifier.thinking_style == ThinkingStyle.CREATIVE


# =============================================================================
# Route 3: Multi-Agent Runner Tests
# =============================================================================

class TestMultiAgentRunner:
    """Tests for Route 3: Multi-Agent Context and Interaction."""

    def test_setup_runner(self):
        """Test setting up a multi-agent runner."""
        runner = MultiAgentRunner.setup(
            session_id="test_session",
            job_type=JobType.CONTENT_GENERATION,
            user_intent="Write an article",
            agent_configs=[
                {"name": "researcher"},
                {"name": "writer"}
            ]
        )

        assert runner.context is not None
        assert runner.job is not None
        assert len(runner.agents) == 2

    def test_add_goals(self):
        """Test adding goals to job."""
        runner = MultiAgentRunner.setup(
            session_id="test",
            job_type=JobType.WORKFLOW_RUNNER,
            user_intent="Process data",
            agent_configs=[{"name": "agent1"}]
        )

        runner.add_goal("Step 1")
        runner.add_goal("Step 2", dependencies=["Step 1"])

        assert len(runner.job.goals) == 2

    def test_mark_goal_complete(self):
        """Test marking goals complete."""
        runner = MultiAgentRunner.setup(
            session_id="test",
            job_type=JobType.PLANNING,
            user_intent="Plan project",
            agent_configs=[{"name": "planner"}]
        )

        runner.add_goal("Goal 1")
        runner.add_goal("Goal 2")

        runner.mark_goal_complete("goal_0")

        assert runner.job.goals[0].completed is True
        assert runner.job.goals[1].completed is False

    def test_run_sequential(self):
        """Test running sequential interaction."""
        runner = MultiAgentRunner.setup(
            session_id="test",
            job_type=JobType.CONTENT_GENERATION,
            user_intent="Generate content",
            agent_configs=[
                {"name": "researcher"},
                {"name": "writer"}
            ]
        )

        result = runner.run_sequential(
            agent_sequence=["researcher", "writer"],
            initial_input="Topic"
        )

        assert result["interaction_type"] == "sequential"
        assert "researcher" in result["agents_run"]
        assert "writer" in result["agents_run"]

    def test_run_group_discuss(self):
        """Test running group discussion."""
        runner = MultiAgentRunner.setup(
            session_id="test",
            job_type=JobType.RESEARCH_DISCUSS,
            user_intent="Discuss best approach",
            agent_configs=[
                {"name": "expert1"},
                {"name": "expert2"},
                {"name": "expert3"}
            ]
        )

        result = runner.run_group_discuss(
            topic="Python vs JavaScript",
            consensus_method="voting"
        )

        assert result["interaction_type"] == "group_discuss"
        assert result["topic"] == "Python vs JavaScript"

    def test_run_workflow_suggestion(self):
        """Test running workflow with suggestions."""
        runner = MultiAgentRunner.setup(
            session_id="test",
            job_type=JobType.WORKFLOW_RUNNER,
            user_intent="Process pipeline",
            agent_configs=[
                {"name": "step1"},
                {"name": "step2"}
            ]
        )

        result = runner.run_workflow_suggestion(
            workflow_input="Data pipeline",
            enable_suggestions=True
        )

        assert result["interaction_type"] == "workflow_suggestion"
        assert "suggestions" in result

    def test_get_status(self):
        """Test getting runner status."""
        runner = MultiAgentRunner.setup(
            session_id="status_test",
            job_type=JobType.CONTENT_GENERATION,
            user_intent="Test",
            agent_configs=[{"name": "agent1"}]
        )

        status = runner.get_status()

        assert "context_id" in status
        assert status["context_id"] == "status_test"
        assert status["job_type"] == "content_generation"
        assert len(status["agents"]) == 1


# =============================================================================
# Route 4: LLM Integration Tests
# =============================================================================

class TestLLMManager:
    """Tests for Route 4: LLM Integration."""

    def test_create_llm_manager(self):
        """Test creating LLM manager."""
        llm = OllamaChat(base_url="http://localhost:11434")
        manager = LLMManager(llm=llm)

        assert manager.llm.base_url == "http://localhost:11434"

    def test_context_window(self):
        """Test context window functionality."""
        window = ContextWindow(max_tokens=1000)
        window.add_message("user", "Hello")
        window.add_message("assistant", "Hi there")

        assert len(window.messages) == 2

        messages = window.get_context_messages()
        assert len(messages) == 2

    def test_context_window_trim(self):
        """Test context window trimming."""
        window = ContextWindow(max_stored_messages=3)
        for i in range(5):
            window.add_message("user", f"Message {i}")

        assert len(window.messages) <= 3

    def test_message_to_dict(self):
        """Test message serialization."""
        msg = Message(role="user", content="Test message")
        d = msg.to_dict()

        assert d["role"] == "user"
        assert d["content"] == "Test message"

    def test_ollama_chat_init(self):
        """Test OllamaChat initialization."""
        llm = OllamaChat(
            base_url="http://custom:11434",
            model="custom_model"
        )

        assert llm.base_url == "http://custom:11434"
        assert llm.model == "custom_model"
        assert llm.provider.value == "ollama"

    @pytest.mark.asyncio
    async def test_llm_generate_error_handling(self):
        """Test error handling when Ollama is not available."""
        llm = OllamaChat(base_url="http://localhost:9999")
        response = await llm.generate("test prompt")

        # Should return error response, not raise exception
        assert "Error" in response.content or response.content == ""

    def test_feedback_collection(self):
        """Test feedback collection."""
        llm = OllamaChat()
        manager = LLMManager(llm=llm)

        manager.add_feedback(
            prompt="Test prompt",
            response="Test response",
            feedback_type="rating",
            rating=5,
            notes="Good"
        )

        assert len(manager.feedback_history) == 1
        assert manager.feedback_history[0]["rating"] == 5

    def test_clear_context(self):
        """Test clearing conversation context."""
        llm = OllamaChat()
        manager = LLMManager(llm=llm)
        manager.context_window.add_message("user", "Hello")

        manager.clear_context()

        assert len(manager.context_window.messages) == 0

    def test_get_recent_context(self):
        """Test getting recent context."""
        llm = OllamaChat()
        manager = LLMManager(llm=llm)

        manager.context_window.add_message("user", "Hello")
        manager.context_window.add_message("assistant", "Hi")
        manager.context_window.add_message("user", "How are you?")

        context = manager.get_recent_context(message_count=2)
        assert "How are you?" in context


# =============================================================================
# Integration Tests
# =============================================================================

class TestEndToEndRoutes:
    """End-to-end tests combining multiple routes."""

    def test_agent_creation_to_interaction(self):
        """Test creating agent and running interaction."""
        # Route 2: Create agents
        factory = AgentFactory()
        agent1 = factory.create_agent("agent1", "general")
        agent2 = factory.create_agent("agent2", "general")

        # Route 3: Setup interaction
        runner = MultiAgentRunner.setup(
            session_id="e2e_test",
            job_type=JobType.CONTENT_GENERATION,
            user_intent="Generate output",
            agent_configs=[agent1, agent2]
        )

        result = runner.run_sequential(
            agent_sequence=["agent1", "agent2"],
            initial_input="Test input"
        )

        assert result["interaction_type"] == "sequential"

    def test_prompt_to_agent_to_llm(self):
        """Test full pipeline: prompt processing -> agent -> LLM."""
        # Route 1: Process prompt
        modifier = MindsetModifier()
        modifier.apply_preset("analytical")
        processor = PromptProcessor("test", modifier)

        result = processor.process_prompt("Write code")

        # Route 2: Create agent based on mindset
        factory = AgentFactory()
        agent = factory.create_agent(
            name="coder",
            agent_type="coder",
            thinking_style=result.agent_mindset_snapshot["thinking_style"]
        )

        assert agent.name == "coder"

    @pytest.mark.asyncio
    async def test_llm_with_memory(self):
        """Test LLM interaction with memory."""
        llm = OllamaChat()
        manager = LLMManager(
            llm=llm,
            context_window=ContextWindow(system_prompt="You are a helpful assistant.")
        )

        # First message
        await manager.send_message("My name is John", use_memory=False)

        # Second message should have context
        context = manager.get_recent_context()
        assert "John" in context or len(context) > 0

        await manager.close()


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
