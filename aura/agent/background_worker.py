"""Background autonomous task worker."""

from __future__ import annotations

from aura.agent.agent_loop import AgentLoop
from aura.agent.scheduler import Scheduler


class BackgroundWorker:
    """Execute scheduled autonomous tasks."""

    def __init__(
        self,
        scheduler: Scheduler,
        agent_loop: AgentLoop,
    ) -> None:
        self._scheduler = scheduler
        self._agent_loop = agent_loop

        self._results: list[object] = []

    @property
    def results(
        self,
    ) -> list[object]:
        """Return execution results."""

        return self._results

    def run_pending(
        self,
    ) -> int:
        """Execute pending tasks."""

        executed = 0

        for task in self._scheduler.pending():

            result = self._agent_loop.run(
                task.description,
            )

            self._results.append(
                result,
            )

            task.mark_completed()

            executed += 1

        return executed
