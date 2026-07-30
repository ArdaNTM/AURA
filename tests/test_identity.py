from aura.identity import (
    IdentityProfile,
    build_identity_prompt,
)


def test_identity_profile_defaults():
    profile = IdentityProfile()

    assert profile.name == "AURA"
    assert profile.version == "0.5"


def test_identity_prompt_contains_identity():
    prompt = build_identity_prompt()

    assert "AURA" in prompt
    assert "Personal AI assistant" in prompt


def test_custom_identity():
    profile = IdentityProfile(
        name="JARVIS",
        version="1.0",
    )

    prompt = build_identity_prompt(
        profile,
    )

    assert "JARVIS" in prompt
    assert "1.0" in prompt
