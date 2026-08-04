from __future__ import annotations

from dataclasses import dataclass, field

from aura.agent.experience import AgentExperience
from aura.brain.state import AgentState


@dataclass
class AgentExecutionState:
    """High level autonomous agent state."""

    cycles: int = 0

    last_state: AgentState | None = None

    history: list[AgentState] = field(
        default_factory=list,
    )

    experiences: list[AgentExperience] = field(
        default_factory=list,
    )

    def update(
        self,
        state: AgentState,
    ) -> None:
        self.cycles += 1

        self.last_state = state

        self.history.append(
            state,
        )
