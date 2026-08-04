from __future__ import annotations

from aura.agent.autonomous_task import AutonomousTask
from aura.agent.experience import AgentExperience
from aura.agent.memory_loop import AgentMemoryLoop
from aura.agent.scheduler import Scheduler
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

        self.memory = AgentMemoryLoop()

        self.scheduler = Scheduler()

    @property
    def memory_context(
        self,
    ) -> dict[str, object]:
        return self.memory.context()

    def run(
        self,
        message: str,
    ):

        result = self._runtime.run(
            message,
            agent_context=self.memory_context,
        )

        self.state.update(
            result,
        )
        initiative = result.metadata.get(
            "initiative",
        )

        if isinstance(
            initiative,
            dict,
        ):

            task = AutonomousTask(
                description=initiative["task"],
                interval=3600,
            )

            self.scheduler.add(
                task,
            )
        experience = AgentExperience(
            task=message,
            success=result.completed,
            strategy=(result.decision.strategy if result.decision else None),
            score=(result.reflection.quality_score if result.reflection else 0.0),
            output=result.output,
            reflection=(result.reflection.summary if result.reflection else None),
        )

        self.memory.remember(
            experience,
        )

        self.state.experiences.append(
            experience,
        )

        return result
