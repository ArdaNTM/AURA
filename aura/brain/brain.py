"""AURA cognitive brain facade."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aura.brain.decision import Action, DecisionEngine
from aura.brain.models import Decision
from aura.brain.planner import Planner

if TYPE_CHECKING:
    from aura.core.tools import ToolRegistry
    from aura.memory.base import Memory


class Brain:
    """High level interface for AURA reasoning."""

    def __init__(
        self,
        planner: Planner | None = None,
        decision_engine: DecisionEngine | None = None,
        tools: ToolRegistry | None = None,
        memory: Memory | None = None,
    ) -> None:
        self._tools = tools
        self._memory = memory

        self._planner = planner or Planner(
            tools=tools,
        )

        self._decision_engine = decision_engine or DecisionEngine()

    @property
    def planner(self) -> Planner:
        return self._planner

    @property
    def decision_engine(self) -> DecisionEngine:
        return self._decision_engine

    @property
    def tools(self) -> ToolRegistry | None:
        return self._tools

    @property
    def memory(self) -> Memory | None:
        return self._memory

    def think(
        self,
        user_message: str,
        memories: list[tuple[str, str]] | None = None,
    ) -> tuple[Decision, Action]:
        """Analyze a request and select an action."""

        decision = self._planner.decide(
            user_message,
        )

        if memories:
            decision.metadata["memory"] = memories

        action = self._decision_engine.decide(
            decision,
        )

        return decision, action
