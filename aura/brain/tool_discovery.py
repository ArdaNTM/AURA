"""Tool discovery service for AURA."""

from __future__ import annotations

from aura.core.tools import ToolRegistry


class ToolDiscovery:
    """Discover available tools and capabilities."""

    def __init__(
        self,
        registry: ToolRegistry,
    ) -> None:
        self._registry = registry

    @property
    def registry(
        self,
    ) -> ToolRegistry:
        """Return registry."""

        return self._registry

    def available_tools(
        self,
    ) -> list[str]:
        """Return available tool names."""

        return self._registry.list_tools()

    def available_schemas(
        self,
    ) -> list[dict[str, object]]:
        """Return available tool schemas."""

        return self._registry.schemas()
