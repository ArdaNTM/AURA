"""Conversation session."""

from __future__ import annotations

from aura.memory.base import Memory


class Session:
    """Represents a conversation session."""

    def __init__(
        self,
        memory: Memory,
    ) -> None:
        self._memory = memory

    @property
    def memory(self) -> Memory:
        return self._memory

    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        """Add a generic conversation message."""

        self._memory.add(
            role,
            content,
        )

    def add_user_message(
        self,
        content: str,
    ) -> None:
        """Add a user message."""

        self.add_message(
            "user",
            content,
        )

    def add_assistant_message(
        self,
        content: str,
    ) -> None:
        """Add an assistant message."""

        self.add_message(
            "assistant",
            content,
        )

    def add_tool_message(
        self,
        content: str,
    ) -> None:
        """Add a tool result message."""

        self.add_message(
            "tool",
            content,
        )

    def history(self) -> list[tuple[str, str]]:
        return self._memory.history()

    def messages(self) -> list[dict[str, str]]:
        return [
            {
                "role": role,
                "content": content,
            }
            for role, content in self._memory.history()
        ]

    def clear(self) -> None:
        self._memory.clear()

    def close(self) -> None:
        """Close memory resources if supported."""

        close_method = getattr(
            self._memory,
            "close",
            None,
        )

        if callable(close_method):
            close_method()
