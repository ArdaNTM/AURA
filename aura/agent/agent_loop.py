from __future__ import annotations

from aura.agent.state import AgentExecutionState
from aura.brain.runtime import AgentRuntime


class AgentLoop:
    """Autonomous observe-think-act-learn loop."""

    def __init__(
        self,
        runtime: AgentRuntime,
    ) -> None:
        self._runtime = runtime
        self.state = AgentExecutionState()

    def run(
        self,
        message: str,
    ):
        """Execute one autonomous cycle."""

        result = self._runtime.run(
            message,
        )

        self.state.update(
            result,
        )

        return result
