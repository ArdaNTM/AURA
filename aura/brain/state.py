"""Agent execution state models for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field

from aura.brain.decision import Action
from aura.brain.improvement import ImprovementPlan
from aura.brain.models import Decision
from aura.brain.observation import Observation
from aura.brain.reflection import Reflection


@dataclass
class AgentState:
    """Runtime state of an agent execution."""

    goal: str

    decision: Decision | None = None

    action: Action | None = None

    observations: list[Observation] = field(
        default_factory=list,
    )

    reflection: Reflection | None = None

    improvement_plan: ImprovementPlan | None = None

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

    def set_reflection(
        self,
        reflection: Reflection,
    ) -> None:
        """Store reflection result."""

        self.reflection = reflection

    def set_improvement_plan(
        self,
        plan: ImprovementPlan,
    ) -> None:
        """Store improvement recommendation."""

        self.improvement_plan = plan

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
