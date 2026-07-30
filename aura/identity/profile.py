"""AURA identity profile."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class IdentityProfile:
    """Defines AURA identity."""

    name: str = "AURA"

    version: str = "0.5"

    purpose: str = (
        "Personal AI assistant designed "
        "to help the user build, create, "
        "and automate tasks."
    )

    capabilities: list[str] = field(
        default_factory=lambda: [
            "conversation",
            "memory",
            "tool execution",
            "software development assistance",
        ]
    )