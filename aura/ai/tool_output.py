"""Tool execution output sent back to providers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToolOutput:
    """Normalized tool execution output."""

    call_id: str
    output: str