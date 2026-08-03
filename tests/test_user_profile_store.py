from aura.brain.user_profile import UserProfile
from aura.brain.user_profile_store import UserProfileStore


def test_user_profile_store_save_load(
    tmp_path,
):

    store = UserProfileStore(
        tmp_path / "user.json",
    )

    profile = UserProfile()

    profile.set_preference(
        "language",
        "Python",
    )

    profile.add_tool(
        "Unity",
    )

    store.save(
        profile,
    )

    loaded = store.load()

    assert loaded.preferences["language"] == "Python"

    assert "Unity" in loaded.favorite_tools
