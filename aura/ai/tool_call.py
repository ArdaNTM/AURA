"""Representation of an AI requested tool call."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ToolCall:
    """A tool execution request produced by an AI provider."""

    name: str
    arguments: dict[str, Any]
    call_id: str | None = None