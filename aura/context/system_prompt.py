"""System prompt generation for AURA context."""

from __future__ import annotations


def build_memory_context(
    memories: list[tuple[str, str]],
) -> str:
    """Create system context from memories."""

    if not memories:
        return ""

    lines = [
        "Relevant memories from previous conversations:"
    ]

    for role, content in memories:
        lines.append(
            f"- {role}: {content}"
        )

    return "\n".join(lines)