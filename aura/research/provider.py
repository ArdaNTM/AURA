"""Research provider interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from aura.research.models import ResearchResult


class ResearchProvider(ABC):
    """Base research provider."""

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> list[ResearchResult]:
        """Search information sources."""
