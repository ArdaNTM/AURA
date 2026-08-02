"""Tool discovery service for AURA."""

from __future__ import annotations

from aura.core.tools import ToolRegistry


class ToolDiscovery:
    """Discover available tools and capabilities."""

    def __init__(
        self,
        registry: ToolRegistry | None = None,
    ) -> None:
        self._registry = registry

    @property
    def registry(
        self,
    ) -> ToolRegistry | None:
        """Return registry."""

        return self._registry

    def available_tools(
        self,
    ) -> list[str]:
        """Return available tool names."""

        if not self._registry:
            return []

        return self._registry.list_tools()

    def available_schemas(
        self,
    ) -> list[dict[str, object]]:
        """Return available tool schemas."""

        if not self._registry:
            return []

        return self._registry.schemas()

    def is_available(
        self,
        capability: str,
    ) -> bool:
        """Check whether a capability has an available tool."""

        for schema in self.available_schemas():
            if (
                schema.get(
                    "capability",
                )
                == capability
            ):
                return True

        return False

    def find_tool(
        self,
        capability: str,
    ) -> str | None:
        """Find a tool name for a capability."""

        for schema in self.available_schemas():
            if (
                schema.get(
                    "capability",
                )
                == capability
            ):
                return str(
                    schema.get(
                        "name",
                    )
                )

        return None
