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

    def evaluate_quality(
        self,
        observation: Observation,
    ) -> dict[str, object]:
        """Evaluate observation quality metrics."""

        quality = {
            "success": observation.success,
            "score": observation.score,
            "retry_needed": observation.retry_needed,
            "output_length": len(
                observation.output,
            ),
        }

        if observation.score >= 0.9:
            quality["quality_level"] = "high"

        elif observation.score >= 0.5:
            quality["quality_level"] = "medium"

        else:
            quality["quality_level"] = "low"

        return quality
