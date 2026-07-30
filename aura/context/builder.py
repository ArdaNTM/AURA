"""Context builder for AURA cognitive layer."""

from __future__ import annotations

from aura.context.models import AIContext
from aura.context.system_prompt import build_system_prompt
from aura.core.session import Session
from aura.core.tools import ToolRegistry
from aura.memory.base import Memory


class ContextBuilder:
    """Build AI context from AURA runtime state."""

    def __init__(
        self,
        session: Session,
        tools: ToolRegistry,
        memory: Memory,
    ) -> None:
        self._session = session
        self._tools = tools
        self._memory = memory

    def build(
        self,
        query: str | None = None,
    ) -> AIContext:
        """Create current AI context."""

        memories: list[tuple[str, str]] = []

        if query:
            memories = self._memory.search(
                query,
            )

        system_prompt = build_system_prompt(
            memories,
        )

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.extend(
            self._session.messages(),
        )

        return AIContext(
            messages=messages,
            tools=self._tools.openai_schemas(),
            memories=memories,
            system_prompt=system_prompt,
        )
