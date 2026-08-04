from __future__ import annotations


class VisionSimilarity:
    """Compare visual targets."""

    def compare(
        self,
        expected: str,
        candidates: list[str],
    ) -> str | None:
        """Find closest candidate."""

        expected_lower = expected.casefold()

        for candidate in candidates:
            if expected_lower in candidate.casefold():
                return candidate

        return None
