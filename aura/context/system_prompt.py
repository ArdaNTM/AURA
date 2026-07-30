"""System prompt generation for AURA context."""

from __future__ import annotations

from aura.identity import IdentityProfile, build_identity_prompt


def build_memory_context(
    memories: list[tuple[str, str]],
) -> str:
    """Create system context from memories."""

    if not memories:
        return ""

    lines = ["Relevant memories from previous conversations:"]

    for role, content in memories:
        lines.append(f"- {role}: {content}")

    return "\n".join(lines)


def build_system_prompt(
    memories: list[tuple[str, str]],
    profile: IdentityProfile | None = None,
) -> str:
    """Create complete AURA system prompt."""

    sections = [
        build_identity_prompt(
            profile,
        ),
        build_memory_context(
            memories,
        ),
    ]

    return "\n\n".join(section for section in sections if section)
