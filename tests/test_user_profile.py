from aura.brain.user_profile import UserProfile


def test_user_profile_stores_preferences():

    profile = UserProfile()

    profile.set_preference(
        "language",
        "python",
    )

    assert profile.preferences["language"] == "python"


def test_user_profile_stores_coding_style():

    profile = UserProfile()

    profile.set_coding_style(
        "architecture",
        "clean",
    )

    assert profile.coding_style["architecture"] == "clean"


def test_user_profile_adds_tools():

    profile = UserProfile()

    profile.add_tool(
        "Unity",
    )

    assert "Unity" in profile.favorite_tools
