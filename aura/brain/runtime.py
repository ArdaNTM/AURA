"""AURA agent runtime orchestration."""

from __future__ import annotations

from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.state import AgentState
from aura.memory.base import Memory


class AgentRuntime:
    """Coordinate brain decisions and execution state."""

    def __init__(
        self,
        brain: Brain,
        executor: PlanExecutor,
        memory: Memory | None = None,
    ) -> None:
        self._brain = brain
        self._executor = executor
        self._memory = memory

    @property
    def brain(self) -> Brain:
        """Return brain instance."""

        return self._brain

    @property
    def executor(self) -> PlanExecutor:
        """Return executor instance."""

        return self._executor

    @property
    def memory(self) -> Memory | None:
        """Return memory instance."""

        return self._memory

    def run(
        self,
        user_message: str,
    ) -> AgentState:
        """Run one agent cycle."""

        state = AgentState(
            goal=user_message,
        )

        memories = []

        if self._memory:
            memories = self._memory.search(
                user_message,
            )

        decision, action = self._brain.think(
            user_message,
            memories=memories,
        )

        state.decision = decision
        state.action = action

        observations = self._executor.execute_with_observation(
            decision,
        )

        for observation in observations:
            state.add_observation(
                observation,
            )

        state.completed = True

        return state
