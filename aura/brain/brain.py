"""AURA cognitive brain facade."""

from __future__ import annotations

from aura.brain.decision import Action, DecisionEngine
from aura.brain.models import Decision
from aura.brain.planner import Planner


class Brain:
    """High level interface for AURA reasoning."""

    def __init__(
        self,
        planner: Planner | None = None,
        decision_engine: DecisionEngine | None = None,
    ) -> None:
        self._planner = planner or Planner()

        self._decision_engine = (
            decision_engine
            or DecisionEngine()
        )

    @property
    def planner(self) -> Planner:
        return self._planner

    @property
    def decision_engine(self) -> DecisionEngine:
        return self._decision_engine

    def think(
        self,
        user_message: str,
    ) -> tuple[Decision, Action]:
        """Analyze a request and select an action."""

        decision = self._planner.decide(
            user_message,
        )

        action = self._decision_engine.decide(
            decision,
        )

        return decision, action