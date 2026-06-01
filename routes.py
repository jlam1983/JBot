"""
JLLMBot Routes

Four main routes:
1. Route 1: Prompt Processing - Process user prompt and update agent mindset
2. Route 2: Agent Creation - Simple factory API for creating agents
3. Route 3: Multi-Agent Interaction - Context, Job, Agents, and Interaction
4. Route 4: LLM Integration - Ollama API chat with context windows
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable
from enum import Enum

from src.core.agent import Agent, AgentConfig
from src.core.context import Context, SessionMemory
from src.core.job_types import Job, JobType, Intent, Goal
from src.core.summary_storage import SummaryStorage, Experience, Rule, ImportantFact
from src.interaction.interaction_manager import InteractionManager, InteractionType
from src.interaction.sequential import SequentialInteraction
from src.interaction.group_discuss import GroupDiscuss, ConsensusMethod
from src.interaction.workflow_suggestion import WorkflowSuggestion
from src.display.mindset_modifier import MindsetModifier, ThinkingStyle

from llm import OllamaChat, LLMManager, ContextWindow, Message


# =============================================================================
# Route 1: Prompt Processing with Agent Mindset
# =============================================================================

@dataclass
class PromptResult:
    """Result of prompt processing."""
    original_prompt: str
    transformed_prompt: str
    agent_mindset_snapshot: dict[str, Any]
    suggestions: list[str] = field(default_factory=list)
    feedback: str = ""


@dataclass
class PromptProcessor:
    """
    Route 1: Process user prompt and update agent mindset.

    Takes a raw user prompt, transforms it based on agent mindset,
    and returns the enhanced prompt along with mindset updates.
    """
    agent_id: str
    mindset_modifier: MindsetModifier
    context_window: ContextWindow = field(default_factory=ContextWindow)

    # Processing options
    enhance_prompt: bool = True
    add_context: bool = True
    apply_thinking_style: bool = True

    def process_prompt(
        self,
        user_prompt: str,
        additional_context: str | None = None
    ) -> PromptResult:
        """
        Process a user prompt with agent mindset.

        Args:
            user_prompt: The raw user input
            additional_context: Optional additional context

        Returns:
            PromptResult with transformed prompt and mindset info
        """
        # Get current mindset configuration
        mindset_config = self.mindset_modifier.get_current_configuration()

        # Transform prompt based on mindset
        transformed = user_prompt

        if self.apply_thinking_style:
            transformed = self._apply_thinking_style(transformed, mindset_config)

        if self.enhance_prompt:
            transformed = self._enhance_prompt(transformed, additional_context)

        if self.add_context:
            # Add relevant context from recent conversation
            recent = self.context_window.get_recent_messages(3)
            if recent:
                context_parts = [f"Recent: {m.role}: {m.content[:100]}..." for m in recent]
                transformed = f"Context:\n{chr(10).join(context_parts)}\n\nCurrent: {transformed}"

        # Generate suggestions based on mindset
        suggestions = self._generate_suggestions(mindset_config)

        return PromptResult(
            original_prompt=user_prompt,
            transformed_prompt=transformed,
            agent_mindset_snapshot=mindset_config,
            suggestions=suggestions
        )

    def _apply_thinking_style(self, prompt: str, mindset: dict[str, Any]) -> str:
        """Apply thinking style to prompt."""
        thinking_style = mindset.get("thinking_style", "analytical")
        verbosity = mindset.get("verbosity", 3)
        reasoning_depth = mindset.get("reasoning_depth", 3)

        prefixes = {
            "analytical": "Analyze this thoroughly:\n",
            "creative": "Brainstorm creative solutions for:\n",
            "practical": "Provide a practical solution for:\n"
        }

        depth_instruction = f"\n[Think step-by-step, depth level: {reasoning_depth}/5]"

        prefix = prefixes.get(thinking_style, "")
        enhanced = f"{prefix}{prompt}{depth_instruction}"

        if verbosity >= 4:
            enhanced += "\n[Provide detailed explanations]"
        elif verbosity <= 2:
            enhanced += "\n[Be concise]"

        return enhanced

    def _enhance_prompt(self, prompt: str, additional_context: str | None) -> str:
        """Enhance prompt with structure."""
        enhanced = prompt

        if additional_context:
            enhanced = f"{additional_context}\n\n---\n\n{prompt}"

        return enhanced

    def _generate_suggestions(self, mindset: dict[str, Any]) -> list[str]:
        """Generate suggestions based on mindset."""
        suggestions = []
        thinking_style = mindset.get("thinking_style", "analytical")

        if thinking_style == "analytical":
            suggestions.append("Consider breaking this into smaller problems")
            suggestions.append("Verify assumptions before proceeding")
        elif thinking_style == "creative":
            suggestions.append("Explore alternative perspectives")
            suggestions.append("Consider unconventional approaches")
        elif thinking_style == "practical":
            suggestions.append("Focus on actionable steps")
            suggestions.append("Consider implementation constraints")

        return suggestions

    def update_mindset_from_feedback(self, feedback: str, rating: int) -> None:
        """
        Update agent mindset based on user feedback.

        Args:
            feedback: User's feedback text
            rating: Rating 1-5
        """
        # Adjust parameters based on feedback
        if rating >= 4:
            # Positive feedback - maintain current style
            pass
        elif rating <= 2:
            # Negative feedback - adjust
            if "too verbose" in feedback.lower():
                self.mindset_modifier.adjust_verbosity(-1)
            elif "too shallow" in feedback.lower():
                self.mindset_modifier.adjust_reasoning_depth(1)
            elif "not creative" in feedback.lower():
                self.mindset_modifier.adjust_creativity(1)

    def add_to_context(self, role: str, content: str) -> None:
        """Add message to context window."""
        self.context_window.add_message(role, content)


# =============================================================================
# Route 2: Simple Agent Factory API
# =============================================================================

@dataclass
class AgentFactory:
    """
    Route 2: Simple factory API for creating and managing agents.

    Provides a clean, simple interface for agent creation without
    needing to understand the full configuration schema.
    """
    _agents: dict[str, Agent] = field(default_factory=dict)
    _configs: dict[str, AgentConfig] = field(default_factory=dict)

    def create_agent(
        self,
        name: str,
        agent_type: str = "general",
        thinking_style: str = "analytical",
        capabilities: list[str] | None = None,
        rules: list[str] | None = None,
        **kwargs: Any
    ) -> Agent:
        """
        Create a new agent with simple parameters.

        Args:
            name: Agent name
            agent_type: Type of agent (general, planner, coder, etc.)
            thinking_style: Thinking style (analytical, creative, practical)
            capabilities: List of capabilities
            rules: List of rules the agent must follow
            **kwargs: Additional agent-specific settings

        Returns:
            Created Agent instance
        """
        # Build role configuration based on type
        roles_config = self._build_roles(agent_type, capabilities or [], rules or [])

        # Build working style
        working_style = self._build_working_style(thinking_style)

        # Build principle
        principle = self._build_principle(rules or [])

        # Create config
        config = AgentConfig(
            name=name,
            description=f"{agent_type} agent: {name}",
            working_style=working_style,
            principle=principle
        )

        # Set roles from config dict
        if "role" in kwargs:
            config.roles = self._dict_to_roles(kwargs["role"])

        # Create agent
        agent = Agent(config)
        self._agents[name] = agent
        self._configs[name] = config

        return agent

    def _build_roles(
        self,
        agent_type: str,
        capabilities: list[str],
        rules: list[str]
    ) -> dict[str, Any]:
        """Build role configuration based on agent type."""
        roles = {}

        # Base roles for all agent types
        if agent_type in ["planner", "general"]:
            roles["planner"] = {"list_of_plan": ["analyze", "execute", "review"]}

        if agent_type in ["coder", "developer", "general"]:
            roles["worker"] = {
                "run_python_code": True,
                "use_tools": ["file_editor", "shell"]
            }

        if agent_type in ["researcher", "analyst", "general"]:
            roles["fact_judger"] = {
                "fact": {
                    "compare_knowledge_base": True,
                    "compare_internet": True
                }
            }
            roles["value_judger"] = {
                "value": {
                    "view_angle": "objective",
                    "value_selected_list": ["accuracy", "clarity"]
                }
            }

        if agent_type == "writer":
            roles["knowledge_explainer"] = {
                "explain": {
                    "target_audience": "general",
                    "depth_level": "moderate",
                    "explanation_style": "simple"
                }
            }

        return roles

    def _build_working_style(self, thinking_style: str) -> Any:
        """Build working style based on thinking style."""
        from src.core.agent import WorkingStyle, WorkingMode, InputType, OutputType

        mode = WorkingMode.SEQUENTIAL
        if thinking_style == "creative":
            mode = WorkingMode.PARALLEL

        return WorkingStyle(
            mode=mode,
            input_type=InputType.TEXT,
            output_type=OutputType.TEXT
        )

    def _build_principle(self, rules: list[str]) -> Any:
        """Build principle based on rules."""
        from src.core.agent import Principle, FallbackStrategy

        return Principle(
            core_principles=rules if rules else ["be helpful", "be accurate"],
            priority_order=["safety", "accuracy", "efficiency"],
            fallback_strategy=FallbackStrategy.RETRY
        )

    def _dict_to_roles(self, role_dict: dict[str, Any]) -> Any:
        """Convert role dict to AgentRoles object."""
        from src.core.agent import AgentRoles, PlannerRole, WorkerRole

        roles = AgentRoles()

        if "planner" in role_dict:
            data = role_dict["planner"]
            roles.planner = PlannerRole(list_of_plan=data.get("list_of_plan", []))

        if "worker" in role_dict:
            data = role_dict["worker"]
            roles.worker = WorkerRole(
                run_cmd=data.get("run_cmd", True),
                run_python_code=data.get("run_python_code", True)
            )

        return roles

    def get_agent(self, name: str) -> Agent | None:
        """Get an agent by name."""
        return self._agents.get(name)

    def list_agents(self) -> list[str]:
        """List all created agents."""
        return list(self._agents.keys())

    def delete_agent(self, name: str) -> bool:
        """Delete an agent."""
        if name in self._agents:
            del self._agents[name]
            if name in self._configs:
                del self._configs[name]
            return True
        return False

    def create_from_json(self, json_path: str) -> Agent:
        """Create agent from JSON file."""
        import json
        with open(json_path, 'r') as f:
            data = json.load(f)
        config = AgentConfig.from_dict(data)
        agent = Agent(config)
        self._agents[config.name] = agent
        self._configs[config.name] = config
        return agent


# =============================================================================
# Route 3: Multi-Agent Context, Job, and Interaction
# =============================================================================

@dataclass
class MultiAgentRunner:
    """
    Route 3: Create context, job, multiple agents, and run interactions.

    This route orchestrates the full workflow:
    1. Create shared context
    2. Create job with intent
    3. Create multiple agents
    4. Run interaction between agents
    5. Collect and return results
    """
    context: Context
    job: Job
    agents: list[Agent] = field(default_factory=list)
    interaction_manager: InteractionManager = field(default_factory=InteractionManager)
    storage: SummaryStorage = field(default_factory=SummaryStorage)

    @classmethod
    def setup(
        cls,
        session_id: str,
        job_type: JobType,
        user_intent: str,
        agent_configs: list[dict[str, Any]]
    ) -> MultiAgentRunner:
        """
        Setup a multi-agent run.

        Args:
            session_id: Session identifier
            job_type: Type of job
            user_intent: User's intent/purpose
            agent_configs: List of agent configurations

        Returns:
            Configured MultiAgentRunner
        """
        # Create context
        ctx = Context.create(session_id=session_id)
        ctx.set_job_type(job_type.value)

        # Create job from intent
        job = Job.create(job_type, user_intent)
        job.intent.interpret()

        # Create agents from configs
        agents = []
        for config_dict in agent_configs:
            if isinstance(config_dict, dict):
                agent = Agent(config_dict)
            else:
                agent = config_dict  # Already an Agent
            agents.append(agent)
            ctx.update_agent_list(agent.name)

        # Create interaction manager
        manager = InteractionManager()
        for agent in agents:
            manager.add_agent(agent.name)

        # Create runner
        runner = cls(
            context=ctx,
            job=job,
            agents=agents,
            interaction_manager=manager
        )

        return runner

    def run_sequential(
        self,
        agent_sequence: list[str] | None = None,
        initial_input: str = ""
    ) -> dict[str, Any]:
        """
        Run agents in sequence.

        Args:
            agent_sequence: Order of agents to run (names)
            initial_input: Starting input

        Returns:
            Results from the sequential run
        """
        if agent_sequence is None:
            agent_sequence = [a.name for a in self.agents]

        # Create sequential interaction
        seq = SequentialInteraction(agents=agent_sequence)
        seq.config.agent_sequence = agent_sequence

        # Run
        result = seq.process(initial_input or self.job.intent.raw_input)

        # Store experience
        self.storage.add_experience(Experience(
            source="sequential_run",
            content=f"Ran {len(agent_sequence)} agents sequentially",
            domain="interaction"
        ))

        return {
            "interaction_type": "sequential",
            "agents_run": agent_sequence,
            "final_result": result,
            "context": self.context.session_memory.session_id
        }

    def run_group_discuss(
        self,
        topic: str | None = None,
        consensus_method: str = "voting"
    ) -> dict[str, Any]:
        """
        Run group discussion.

        Args:
            topic: Discussion topic
            consensus_method: How to reach consensus

        Returns:
            Discussion results with consensus
        """
        discuss = GroupDiscuss(agents=[a.name for a in self.agents])

        # Set consensus method
        method_map = {
            "voting": ConsensusMethod.VOTING,
            "negotiation": ConsensusMethod.NEGOTIATION,
            "arbitration": ConsensusMethod.ARBITRATION
        }
        discuss.consensus_method = method_map.get(consensus_method, ConsensusMethod.VOTING)

        # Run discussion
        result = discuss.discuss(topic or self.job.intent.raw_input)

        # Store experience
        self.storage.add_experience(Experience(
            source="group_discuss",
            content=f"Group discussed: {topic or 'main topic'}",
            domain="interaction"
        ))

        return {
            "interaction_type": "group_discuss",
            "topic": topic,
            "consensus": result.get("consensus"),
            "all_contributions": result.get("phases"),
            "context": self.context.session_memory.session_id
        }

    def run_workflow_suggestion(
        self,
        workflow_input: str | None = None,
        enable_suggestions: bool = True
    ) -> dict[str, Any]:
        """
        Run workflow with suggestions.

        Args:
            workflow_input: Input for the workflow
            enable_suggestions: Whether to generate suggestions

        Returns:
            Workflow results with suggestions
        """
        wf = WorkflowSuggestion(agents=[a.name for a in self.agents])
        wf.suggest_process_enhancement = enable_suggestions
        wf.suggest_scope_adjustment = enable_suggestions

        result = wf.suggest_and_execute(workflow_input or self.job.intent.raw_input)

        return {
            "interaction_type": "workflow_suggestion",
            "input": workflow_input,
            "suggestions": result.get("suggestions", []),
            "accepted_count": result.get("accepted_count", 0),
            "result": result.get("result"),
            "context": self.context.session_memory.session_id
        }

    def add_goal(self, goal_description: str, dependencies: list[str] | None = None) -> None:
        """Add a goal to the job."""
        goal_id = f"goal_{len(self.job.goals)}"
        goal = Goal(
            goal_id=goal_id,
            description=goal_description,
            dependencies=dependencies or []
        )
        self.job.add_goal(goal)

    def mark_goal_complete(self, goal_id: str) -> None:
        """Mark a goal as complete."""
        for goal in self.job.goals:
            if goal.goal_id == goal_id:
                goal.completed = True
                self.job.progress.mark_complete(goal_id)
                break

    def get_status(self) -> dict[str, Any]:
        """Get current status of the multi-agent run."""
        return {
            "context_id": self.context.session_memory.session_id,
            "job_type": self.job.job_type.value,
            "intent": self.job.intent.raw_input,
            "goals": {
                "total": len(self.job.goals),
                "completed": len(self.job.progress.completed_goals),
                "pending": len(self.job.progress.pending_goals),
                "blocked": len(self.job.progress.blocked_goals)
            },
            "agents": [a.name for a in self.agents],
            "interaction_type": self.interaction_manager.current_type.value
        }


# =============================================================================
# Route 4: LLM Integration (Combined with Route 1)
# =============================================================================

@dataclass
class LLMIntegrationMixin:
    """
    Route 4: LLM Integration with Ollama API.

    Provides chat interface with context window support,
    memory management, and feedback collection.
    """
    llm_manager: LLMManager

    async def chat(
        self,
        user_input: str,
        system_prompt: str | None = None,
        use_memory: bool = True
    ) -> tuple[str, LLMResponse]:
        """
        Send message to LLM with context.

        Args:
            user_input: User message
            system_prompt: Optional system prompt
            use_memory: Whether to use conversation memory

        Returns:
            Tuple of (response_text, LLMResponse)
        """
        response = await self.llm_manager.send_message(
            user_input=user_input,
            system_prompt=system_prompt,
            use_memory=use_memory
        )
        return response.content, response

    async def chat_stream(
        self,
        user_input: str,
        system_prompt: str | None = None
    ) -> AsyncIterator[str]:
        """Stream chat response."""
        async for chunk in self.llm_manager.send_message_stream(
            user_input=user_input,
            system_prompt=system_prompt
        ):
            yield chunk

    def provide_feedback(
        self,
        prompt: str,
        response: str,
        feedback_type: str,
        rating: int,
        notes: str | None = None
    ) -> None:
        """Provide feedback on a response."""
        self.llm_manager.add_feedback(
            prompt=prompt,
            response=response,
            feedback_type=feedback_type,
            rating=rating,
            notes=notes
        )

    def get_context_summary(self, message_count: int = 10) -> str:
        """Get recent context as string."""
        return self.llm_manager.get_recent_context(message_count)

    def clear_conversation(self) -> None:
        """Clear conversation context."""
        self.llm_manager.clear_context()


# =============================================================================
# Convenience Functions
# =============================================================================

def create_quick_agent(
    name: str,
    agent_type: str = "general",
    thinking_style: str = "analytical"
) -> tuple[Agent, MindsetModifier]:
    """
    Create an agent with mindset modifier in one call.

    Args:
        name: Agent name
        agent_type: Type of agent
        thinking_style: Thinking style

    Returns:
        Tuple of (Agent, MindsetModifier)
    """
    factory = AgentFactory()
    agent = factory.create_agent(name, agent_type, thinking_style)

    modifier = MindsetModifier(agent_id=name)
    modifier.apply_preset(thinking_style)

    return agent, modifier


async def run_quick_chat(
    prompt: str,
    system_prompt: str | None = None,
    ollama_url: str = "http://localhost:11434",
    model: str = "llama3.2"
) -> str:
    """
    Quick chat with Ollama.

    Args:
        prompt: User prompt
        system_prompt: Optional system prompt
        ollama_url: Ollama server URL
        model: Model to use

    Returns:
        LLM response text
    """
    llm = OllamaChat(base_url=ollama_url, model=model)
    manager = LLMManager(llm=llm)
    context_window = ContextWindow(system_prompt=system_prompt or "")

    try:
        response = await manager.send_message(prompt, use_memory=False)
        return response.content
    finally:
        await manager.close()


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    # Route 2: Quick agent creation
    print("=== Route 2: Agent Factory ===")
    factory = AgentFactory()
    agent = factory.create_agent(
        name="assistant",
        agent_type="general",
        thinking_style="analytical",
        rules=["be helpful", "be accurate"]
    )
    print(f"Created agent: {agent.name}")

    # Route 3: Multi-agent setup
    print("\n=== Route 3: Multi-Agent Runner ===")
    runner = MultiAgentRunner.setup(
        session_id="test_session",
        job_type=JobType.CONTENT_GENERATION,
        user_intent="Write a technical blog post about AI agents",
        agent_configs=[
            {"name": "researcher", "description": "Research agent"},
            {"name": "writer", "description": "Writing agent"},
            {"name": "editor", "description": "Editing agent"}
        ]
    )
    print(f"Setup complete: {len(runner.agents)} agents")

    result = runner.run_sequential(
        agent_sequence=["researcher", "writer", "editor"],
        initial_input="AI Agents"
    )
    print(f"Sequential run result: {result['interaction_type']}")

    # Route 4: Quick chat (requires Ollama running)
    print("\n=== Route 4: LLM Chat ===")
    print("(Requires Ollama to be running)")

    async def test_chat():
        try:
            response = await run_quick_chat("What is 2+2?")
            print(f"Chat response: {response}")
        except Exception as e:
            print(f"Chat not available: {e}")

    asyncio.run(test_chat())
