"""Observation evaluator for AURA agent loop."""

from __future__ import annotations

from aura.brain.observation import Observation


class Evaluator:
    """Evaluate agent observations."""

    def evaluate(
        self,
        observation: Observation,
    ) -> Observation:
        """Score and enrich an observation."""

        if not observation.success:
            observation.score = 0.0
            observation.feedback = "Observation failed during execution."
            observation.retry_needed = True

            return observation

        if not observation.output.strip():
            observation.score = 0.5
            observation.feedback = "Execution succeeded but produced no output."

            return observation

        observation.score = 1.0
        observation.feedback = "Observation completed successfully."

        return observation
