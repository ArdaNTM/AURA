from __future__ import annotations

from aura.vision.similarity import VisionSimilarity


class VisionRecovery:
    """Recover failed visual actions."""

    def __init__(
        self,
        similarity: VisionSimilarity | None = None,
    ) -> None:

        self._similarity = similarity or VisionSimilarity()

    def recover(
        self,
        target: str,
        available_elements: list[str],
    ) -> dict[str, object]:
        """Find recovery strategy."""

        alternative = self._similarity.compare(
            target,
            available_elements,
        )

        if alternative:

            return {
                "retry": True,
                "new_target": alternative,
                "confidence": 0.8,
            }

        return {
            "retry": False,
            "new_target": None,
            "confidence": 0.0,
        }
