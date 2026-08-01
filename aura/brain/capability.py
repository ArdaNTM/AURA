"""Capability registry for AURA."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class Capability:
    """Represents a system capability."""

    name: str

    description: str

    requires_tool: bool = False

    default_tool: str | None = None

    requires_permission: bool = False

    risk_level: str = "low"


class CapabilityRegistry:
    """Registry of AURA capabilities."""

    def __init__(
        self,
    ) -> None:
        self._capabilities: dict[str, Capability] = {
            "conversation": Capability(
                name="conversation",
                description="General conversation",
            ),
            "calculation": Capability(
                name="calculation",
                description="Mathematical calculations",
                requires_tool=True,
                default_tool="calculator",
                risk_level="low",
            ),
            "search": Capability(
                name="search",
                description="Search the web",
                requires_tool=True,
                risk_level="low",
            ),
            "coding": Capability(
                name="coding",
                description="Generate or edit code",
                risk_level="low",
            ),
            "filesystem": Capability(
                name="filesystem",
                description="Read and write files",
                requires_tool=True,
                requires_permission=True,
                risk_level="medium",
            ),
            "computer": Capability(
                name="computer",
                description="Control the computer",
                requires_tool=True,
                requires_permission=True,
                risk_level="high",
            ),
            "memory": Capability(
                name="memory",
                description="Store and retrieve memories",
                requires_tool=True,
                risk_level="medium",
            ),
        }

    def get(
        self,
        name: str,
    ) -> Capability:
        """Return a capability."""

        return self._capabilities[name]

    def has(
        self,
        name: str,
    ) -> bool:
        """Return whether capability exists."""

        return name in self._capabilities

    def all(
        self,
    ) -> list[Capability]:
        """Return all capabilities."""

        return list(
            self._capabilities.values(),
        )
