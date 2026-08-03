"""Memory optimization layer for AURA."""

from __future__ import annotations

from datetime import datetime, timedelta

from aura.memory.base import Memory


class MemoryOptimizer:
    """Optimize long term memory quality."""

    def __init__(
        self,
        max_age_days: int = 90,
    ) -> None:
        self._max_age_days = max_age_days

    def find_expired(
        self,
        memory: Memory,
    ) -> list[tuple[str, str]]:
        """Find old low value memories."""

        expired = []

        threshold = datetime.now() - timedelta(
            days=self._max_age_days,
        )

        for item in memory.history():

            content = item[1]

            if "timestamp=" not in content:
                continue

            try:
                timestamp = content.split(
                    "timestamp=",
                )[1].split(
                    ";",
                )[0]

                created = datetime.fromisoformat(
                    timestamp,
                )

                if created < threshold:
                    if self._is_low_value(
                        content,
                    ):
                        expired.append(
                            item,
                        )

            except (
                ValueError,
                IndexError,
            ):
                continue

        return expired

    def compress(
        self,
        memory: Memory,
    ) -> int:
        """Compress duplicate experiences."""

        history = memory.history()

        groups: dict[str, list[str]] = {}

        for _, content in history:

            key = self._extract_key(
                content,
            )

            groups.setdefault(
                key,
                [],
            ).append(
                content,
            )

        compressed = 0

        for key, items in groups.items():

            if len(items) > 3:

                compressed += len(items) - 1

                summary = (
                    f"memory_summary={key}; "
                    f"experiences={len(items)}; "
                    "compressed=True"
                )

                memory.clear()

                memory.add(
                    "assistant",
                    summary,
                )

                break

        return compressed

    def _extract_key(
        self,
        content: str,
    ) -> str:
        """Extract memory identity."""

        for prefix in (
            "intent=",
            "task=",
        ):
            if prefix in content:
                return content.split(prefix)[1].split(";")[0]

        return "general"

    def _is_low_value(
        self,
        content: str,
    ) -> bool:
        """Determine memory value."""

        if "success=True" in content:
            return False

        if "confidence=" in content:
            return False

        return True
