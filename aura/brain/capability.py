"""Capability registry for AURA."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aura.core.tools import ToolRegistry


@dataclass(
    frozen=True,
)
class Capability:
    """Represents a system capability."""

    name: str

    description: str

    requires_tool: bool = False

    default_tool: str | None = None

    allowed_tools: tuple[str, ...] = ()

    requires_permission: bool = False

    risk_level: str = "low"


class CapabilityRegistry:
    """Registry of AURA capabilities."""

    def __init__(
        self,
        tools: ToolRegistry | None = None,
    ) -> None:
        self._tools = tools
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
                allowed_tools=("calculator",),
                risk_level="low",
            ),
            "search": Capability(
                name="search",
                description="Search the web",
                requires_tool=True,
                allowed_tools=("search",),
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
                default_tool="filesystem",
                requires_permission=True,
                allowed_tools=("filesystem",),
                risk_level="medium",
            ),
            "terminal": Capability(
                name="terminal",
                description="Execute terminal commands",
                requires_tool=True,
                default_tool="terminal",
                allowed_tools=("terminal",),
                requires_permission=True,
                risk_level="high",
            ),
            "computer": Capability(
                name="computer",
                description="Control the computer",
                requires_tool=True,
                default_tool="computer",
                allowed_tools=("computer",),
                requires_permission=True,
                risk_level="high",
            ),
            "memory": Capability(
                name="memory",
                description="Store and retrieve memories",
                requires_tool=True,
                risk_level="medium",
            ),
            "screen": Capability(
                name="screen",
                description="Capture and inspect computer screen",
                requires_tool=True,
                default_tool="screen_capture",
                allowed_tools=("screen_capture",),
                requires_permission=True,
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

    def is_available(
        self,
        name: str,
    ) -> bool:
        """Check whether capability can currently execute."""

        capability = self.get(
            name,
        )

        if not capability.requires_tool:
            return True

        if not capability.default_tool:
            return False

        if not self._tools:
            return False

        return self._tools.has(
            capability.default_tool,
        )

    def validate_tool(
        self,
        capability_name: str,
        tool_name: str,
    ) -> bool:
        """Check whether tool is allowed for capability."""

        capability = self.get(
            capability_name,
        )

        if not capability.requires_tool:
            return False

        if not capability.allowed_tools:
            return False

        return tool_name in capability.allowed_tools
