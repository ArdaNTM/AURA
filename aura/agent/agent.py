from __future__ import annotations

from aura.agent.agent_loop import AgentLoop
from aura.brain.runtime import AgentRuntime


class Agent:
    """
    Unified AURA autonomous agent interface.

    High level entry point.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
    ) -> None:

        self._loop = AgentLoop(
            runtime,
        )

    @property
    def state(
        self,
    ):
        return self._loop.state

    def execute(
        self,
        message: str,
    ):
        """
        Execute autonomous agent cycle.
        """

        return self._loop.run(
            message,
        )
