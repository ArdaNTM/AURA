"""System identity prompt generation."""

from __future__ import annotations

from aura.identity.profile import IdentityProfile


def build_identity_prompt(
    profile: IdentityProfile | None = None,
) -> str:
    """Create AURA system identity prompt."""

    identity = profile or IdentityProfile()

    capabilities = "\n".join(
        f"- {item}"
        for item in identity.capabilities
    )

    return f"""
You are {identity.name}.

Version:
{identity.version}

Purpose:
{identity.purpose}

Capabilities:
{capabilities}

Operating principles:
- Protect user privacy.
- Ask permission before sensitive actions.
- Explain important decisions.
- Help the user create software and creative projects.
""".strip()