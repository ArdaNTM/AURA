from __future__ import annotations

from datetime import datetime

from aura.memory.base import Memory
from aura.vision.models import VisionResult


class VisionMemory:
    """Store and recall visual experiences."""

    def __init__(
        self,
        memory: Memory,
    ) -> None:
        self._memory = memory

    def store(
        self,
        vision: VisionResult,
        context: str | None = None,
    ) -> None:
        """Store visual observation."""

        elements = ",".join(element.name for element in vision.elements)

        content = (
            "type=vision;"
            f"timestamp={datetime.now().isoformat()};"
            f"context={context or ''};"
            f"description={vision.description};"
            f"objects={','.join(vision.objects)};"
            f"text={','.join(vision.text)};"
            f"elements={elements};"
            f"confidence={vision.confidence}"
        )

        self._memory.add(
            "vision",
            content,
        )

    def recall(
        self,
        query: str,
    ) -> list[tuple[str, str]]:
        """Recall previous visual states."""

        return [item for item in self._memory.search(query) if "type=vision" in item[1]]
