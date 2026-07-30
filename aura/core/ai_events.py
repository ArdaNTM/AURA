"""AI lifecycle events."""

from __future__ import annotations

from dataclasses import dataclass

from aura.core.events import Event


@dataclass(frozen=True, slots=True)
class AIResponseStarted(Event):
    """Emitted when AI response generation starts."""

    message: str


@dataclass(frozen=True, slots=True)
class ToolStarted(Event):
    """Emitted before tool execution."""

    name: str


@dataclass(frozen=True, slots=True)
class ToolCompleted(Event):
    """Emitted after successful tool execution."""

    name: str
    output: str


@dataclass(frozen=True, slots=True)
class ToolFailed(Event):
    """Emitted after failed tool execution."""

    name: str
    error: str


@dataclass(frozen=True, slots=True)
class AIResponseCompleted(Event):
    """Emitted after AI response is completed."""

    response: str