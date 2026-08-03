from aura.brain.brain import Brain
from aura.brain.user_profile import UserProfile


def test_brain_uses_user_profile():

    profile = UserProfile()

    profile.set_coding_style(
        "language",
        "Python",
    )

    profile.set_preference(
        "architecture",
        "clean",
    )

    brain = Brain(
        user_profile=profile,
    )

    decision, _ = brain.think(
        "backend yaz",
    )

    learning = decision.metadata["learning"]

    assert "user_profile" in learning

    assert learning["user_profile"]["coding_style"]["language"] == "Python"

    assert learning["user_profile"]["preferences"]["architecture"] == "clean"
