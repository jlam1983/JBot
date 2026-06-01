"""
LLM Integration Module - Ollama API Chat Interface

Handles LLM interactions with context, memory, and context windows support.
"""

from __future__ import annotations

import json
import httpx
from dataclasses import dataclass, field
from typing import Any, AsyncIterator
from datetime import datetime
from enum import Enum


class LLMProvider(Enum):
    """LLM provider types."""
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


@dataclass
class Message:
    """A message in the conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content
        }


@dataclass
class ContextWindow:
    """
    Context window management for LLM interactions.
    Handles up/down content flow and memory management.
    """
    max_tokens: int = 4096
    current_tokens: int = 0
    messages: list[Message] = field(default_factory=list)
    system_prompt: str = ""

    # Memory settings
    enable_memory: bool = True
    memory_priority: str = "recent"  # recent, important, hybrid
    max_stored_messages: int = 100

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the context."""
        msg = Message(role=role, content=content)
        self.messages.append(msg)
        self._trim()

    def _trim(self) -> None:
        """Trim messages to fit within context window."""
        if len(self.messages) > self.max_stored_messages:
            # Keep recent messages based on memory_priority
            if self.memory_priority == "recent":
                self.messages = self.messages[-self.max_stored_messages:]
            elif self.memory_priority == "important":
                # Keep messages marked as important
                important = [m for m in self.messages if hasattr(m, 'important') and m.important]
                self.messages = important[-self.max_stored_messages:]
            else:
                # Hybrid: keep some recent, some important
                keep = self.max_stored_messages // 2
                recent = self.messages[-keep:]
                important = [m for m in self.messages if hasattr(m, 'important') and m.important]
                self.messages = (important + recent)[:self.max_stored_messages]

    def get_recent_messages(self, count: int = 10) -> list[Message]:
        """Get recent messages."""
        return self.messages[-count:]

    def get_context_messages(self) -> list[dict[str, Any]]:
        """Get all messages formatted for LLM."""
        result = []
        if self.system_prompt:
            result.append({"role": "system", "content": self.system_prompt})
        result.extend([m.to_dict() for m in self.messages])
        return result

    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 chars)."""
        return len(text) // 4


@dataclass
class LLMResponse:
    """Response from LLM."""
    content: str
    model: str
    done: bool = True
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw_response: dict[str, Any] | None = None


class OllamaChat:
    """
    Ollama API Chat Interface.

    Supports context windows, memory management, and streaming.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2",
        timeout: float = 120.0
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.provider = LLMProvider.OLLAMA
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def chat(
        self,
        messages: list[dict[str, str]],
        context_window: ContextWindow | None = None,
        stream: bool = False,
        **kwargs: Any
    ) -> LLMResponse:
        """
        Send chat request to Ollama.

        Args:
            messages: List of message dicts with "role" and "content"
            context_window: Optional context window for memory
            stream: Whether to stream response
            **kwargs: Additional Ollama parameters (temperature, top_p, etc.)

        Returns:
            LLMResponse with generated content
        """
        client = await self._get_client()

        # Build request payload
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": kwargs
        }

        try:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                content=data.get("message", {}).get("content", ""),
                model=self.model,
                done=data.get("done", True),
                prompt_tokens=data.get("prompt_eval_count", 0),
                completion_tokens=data.get("eval_count", 0),
                total_tokens=data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
                raw_response=data
            )
        except httpx.HTTPError as e:
            return LLMResponse(
                content=f"Error: {str(e)}",
                model=self.model,
                done=True
            )

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        context_window: ContextWindow | None = None,
        **kwargs: Any
    ) -> LLMResponse:
        """
        Generate completion using /api/generate endpoint.

        Args:
            prompt: User prompt
            system: Optional system prompt
            context_window: Optional context window
            **kwargs: Additional Ollama parameters

        Returns:
            LLMResponse with generated content
        """
        client = await self._get_client()

        full_prompt = prompt
        if system:
            full_prompt = f"{system}\n\n{prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": kwargs
        }

        try:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                content=data.get("response", ""),
                model=self.model,
                done=data.get("done", True),
                raw_response=data
            )
        except httpx.HTTPError as e:
            return LLMResponse(
                content=f"Error: {str(e)}",
                model=self.model,
                done=True
            )

    async def stream_chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """
        Stream chat response.

        Yields:
            Text chunks as they arrive
        """
        client = await self._get_client()

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": kwargs
        }

        try:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json=payload
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
        except httpx.HTTPError as e:
            yield f"Error: {str(e)}"

    async def list_models(self) -> list[dict[str, Any]]:
        """List available models."""
        client = await self._get_client()
        try:
            response = await client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return data.get("models", [])
        except httpx.HTTPError:
            return []


@dataclass
class LLMManager:
    """
    Manager for LLM interactions with context and memory support.
    """
    llm: OllamaChat
    context_window: ContextWindow = field(default_factory=ContextWindow)

    # Feedback settings
    collect_feedback: bool = True
    feedback_history: list[dict[str, Any]] = field(default_factory=list)

    async def send_message(
        self,
        user_input: str,
        system_prompt: str | None = None,
        use_memory: bool = True
    ) -> LLMResponse:
        """
        Send message with context window support.

        Args:
            user_input: User's message
            system_prompt: Optional system prompt
            use_memory: Whether to include context window memory

        Returns:
            LLMResponse
        """
        # Add user message to context
        self.context_window.add_message("user", user_input)

        # Update system prompt if provided
        if system_prompt:
            self.context_window.system_prompt = system_prompt

        # Get messages for LLM
        if use_memory:
            messages = self.context_window.get_context_messages()
        else:
            messages = [{"role": "user", "content": user_input}]
            if system_prompt:
                messages.insert(0, {"role": "system", "content": system_prompt})

        # Send to LLM
        response = await self.llm.chat(messages)

        # Add assistant response to context
        if response.done and not response.content.startswith("Error"):
            self.context_window.add_message("assistant", response.content)

        return response

    async def send_message_stream(
        self,
        user_input: str,
        system_prompt: str | None = None
    ) -> AsyncIterator[str]:
        """Stream response to user message."""
        self.context_window.add_message("user", user_input)

        messages = self.context_window.get_context_messages()
        if system_prompt:
            self.context_window.system_prompt = system_prompt
            messages = self.context_window.get_context_messages()

        full_response = ""
        async for chunk in self.llm.stream_chat(messages):
            full_response += chunk
            yield chunk

        # Add final response to context
        if full_response:
            self.context_window.add_message("assistant", full_response)

    def add_feedback(
        self,
        prompt: str,
        response: str,
        feedback_type: str,
        rating: int | None = None,
        notes: str | None = None
    ) -> None:
        """Record feedback for learning."""
        if not self.collect_feedback:
            return

        self.feedback_history.append({
            "prompt": prompt,
            "response": response,
            "feedback_type": feedback_type,
            "rating": rating,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        })

    def get_recent_context(self, message_count: int = 10) -> str:
        """Get recent conversation context as string."""
        messages = self.context_window.get_recent_messages(message_count)
        return "\n".join(f"{m.role}: {m.content}" for m in messages)

    def clear_context(self) -> None:
        """Clear conversation context."""
        self.context_window.clear()

    async def close(self) -> None:
        """Close LLM connections."""
        await self.llm.close()
