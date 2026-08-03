"""Search tool implementation."""

from __future__ import annotations

from typing import Any

from aura.core.tools import Tool
from aura.memory.base import Memory
from aura.research.provider import ResearchProvider


class SearchTool(Tool):
    """Search information sources."""

    def __init__(
        self,
        provider: ResearchProvider | None = None,
        memory: Memory | None = None,
    ) -> None:
        self._provider = provider
        self._memory = memory

    @property
    def name(
        self,
    ) -> str:
        return "search"

    @property
    def capability(
        self,
    ) -> str:
        return "search"

    @property
    def description(
        self,
    ) -> str:
        return "Search information from available sources."

    @property
    def risk_level(
        self,
    ) -> str:
        return "low"

    @property
    def parameters(
        self,
    ) -> dict[str, Any]:
        return {
            "query": {
                "type": "string",
                "description": "Search query.",
            }
        }

    def execute(
        self,
        query: str,
    ) -> str:

        if self._provider is None:
            result = f"Research requested: {query}. " "No provider configured."

            self._store_memory(
                query,
                result,
            )

            return result

        results = self._provider.search(
            query,
        )

        output = "\n".join(result.content for result in results)

        self._store_memory(
            query,
            output,
        )

        return output

    def _store_memory(
        self,
        query: str,
        content: str,
    ) -> None:
        """Store research knowledge."""

        if self._memory is None:
            return

        self._memory.add(
            "research",
            (f"query={query}\n" f"{content}"),
        )
