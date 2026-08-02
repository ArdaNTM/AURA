"""Confidence fusion for AURA."""

from __future__ import annotations


class ConfidenceFusion:
    """Combine confidence signals."""

    def combine(
        self,
        llm_confidence: float,
        intent_confidence: float,
        learning_confidence: float | None = None,
    ) -> float:
        """Calculate final confidence."""

        values = [
            llm_confidence,
            intent_confidence,
        ]

        if learning_confidence is not None:
            values.append(
                learning_confidence,
            )

        return round(
            sum(values) / len(values),
            2,
        )
