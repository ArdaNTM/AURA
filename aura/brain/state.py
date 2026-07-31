"""Agent execution state models for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field

from aura.brain.decision import Action
from aura.brain.models import Decision
from aura.brain.observation import Observation


@dataclass
class AgentState:
    """Runtime state of an agent execution."""

    goal: str

    decision: Decision | None = None

    action: Action | None = None

    observations: list[Observation] = field(
        default_factory=list,
    )

    completed: bool = False

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    def add_observation(
        self,
        observation: Observation,
    ) -> None:
        """Store a new observation."""

        self.observations.append(
            observation,
        )

    @property
    def latest_observation(
        self,
    ) -> Observation | None:
        """Return latest observation."""

        if not self.observations:
            return None

        return self.observations[-1]

    @property
    def output(
        self,
    ) -> str | None:
        """Return latest execution output."""

        observation = self.latest_observation

        if not observation:
            return None

        return observation.output
