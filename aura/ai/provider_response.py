"""Standard response object returned by AI providers."""

from __future__ import annotations

from dataclasses import dataclass

from aura.ai.tool_call import ToolCall


@dataclass(frozen=True, slots=True)
class ProviderResponse:
    """Normalized provider output."""

    text: str | None = None
    tool_call: ToolCall | None = None

    @property
    def has_tool_call(self) -> bool:
        """Return True when provider requested a tool."""
        return self.tool_call is not None

    @property
    def has_text(self) -> bool:
        """Return True when provider returned text."""
        return bool(self.text)
