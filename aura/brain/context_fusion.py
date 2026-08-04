from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContextScore:
    source: str
    weight: float
    available: bool


class ContextFusion:
    """
    Combine multimodal information sources
    into unified reasoning context.
    """

    def fuse(
        self,
        *,
        memory: list[tuple[str, str]] | None = None,
        vision: dict[str, object] | None = None,
        user_profile: dict[str, object] | None = None,
        learning: dict[str, object] | None = None,
    ) -> dict[str, object]:

        context: dict[str, object] = {}

        scores: list[ContextScore] = []

        if memory:
            context["memory_context"] = memory

            scores.append(
                ContextScore(
                    source="memory",
                    weight=0.30,
                    available=True,
                )
            )

        if vision:
            context["vision_context"] = vision

            scores.append(
                ContextScore(
                    source="vision",
                    weight=0.25,
                    available=True,
                )
            )

        if user_profile:
            context["user_context"] = user_profile

            scores.append(
                ContextScore(
                    source="user_profile",
                    weight=0.20,
                    available=True,
                )
            )

        if learning:
            context["learning_context"] = learning

            scores.append(
                ContextScore(
                    source="learning",
                    weight=0.25,
                    available=True,
                )
            )

        context["fusion"] = {
            "sources": [
                {
                    "name": item.source,
                    "weight": item.weight,
                    "available": item.available,
                }
                for item in scores
            ],
            "confidence": sum(item.weight for item in scores),
        }

        return context
