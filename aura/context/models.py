"""Context models used by AURA cognitive layer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AIContext:
    """Complete context provided to the AI provider."""

    messages: list[dict[str, str]] = field(
        default_factory=list,
    )

    tools: list[dict[str, object]] = field(
        default_factory=list,
    )

    memories: list[tuple[str, str]] = field(
        default_factory=list,
    )

    system_prompt: str = ""

    metadata: dict[str, object] = field(
        default_factory=dict,
    )