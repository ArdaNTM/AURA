"""AURA agent runtime orchestration."""

from __future__ import annotations

from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.memory_policy import MemoryPolicy
from aura.brain.state import AgentState
from aura.memory.base import Memory


class AgentRuntime:
    """Coordinate brain decisions and execution state."""

    def __init__(
        self,
        brain: Brain,
        executor: PlanExecutor,
        memory: Memory | None = None,
        memory_policy: MemoryPolicy | None = None,
    ) -> None:
        self._brain = brain
        self._executor = executor
        self._memory = memory
        self._memory_policy = memory_policy or MemoryPolicy()

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

    @property
    def memory_policy(self) -> MemoryPolicy:
        """Return memory policy."""

        return self._memory_policy

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

        state.metadata["memory_count"] = len(
            memories,
        )

        decision, action = self._brain.think(
            user_message,
            memories=memories,
        )

        state.decision = decision
        state.action = action

        if decision:
            state.metadata["intent"] = decision.intent
            state.metadata["confidence"] = decision.confidence

        observations = self._executor.execute_with_observation(
            decision,
        )

        for observation in observations:
            state.add_observation(
                observation,
            )

            self._store_observation(
                observation,
            )

        state.metadata["observation_count"] = len(
            observations,
        )

        state.completed = True

        return state

    def _store_observation(
        self,
        observation,
    ) -> None:
        """Store approved observations in memory."""

        if not self._memory:
            return

        if not self._memory_policy.should_store(
            observation,
        ):
            return

        self._memory.add(
            "assistant",
            observation.output,
        )
