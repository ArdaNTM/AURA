from __future__ import annotations

import json
from pathlib import Path

from aura.brain.user_profile import UserProfile


class UserProfileStore:
    """Persistent user profile storage."""

    def __init__(
        self,
        path: str | Path = "user_profile.json",
    ) -> None:
        self._path = Path(
            path,
        )

    def save(
        self,
        profile: UserProfile,
    ) -> None:
        """Save user profile."""

        data = {
            "preferences": profile.preferences,
            "coding_style": profile.coding_style,
            "workflow": profile.workflow,
            "favorite_tools": profile.favorite_tools,
            "communication_style": profile.communication_style,
        }

        self._path.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def load(
        self,
    ) -> UserProfile:
        """Load user profile."""

        if not self._path.exists():
            return UserProfile()

        data = json.loads(
            self._path.read_text(
                encoding="utf-8",
            ),
        )

        return UserProfile(
            preferences=data.get(
                "preferences",
                {},
            ),
            coding_style=data.get(
                "coding_style",
                {},
            ),
            workflow=data.get(
                "workflow",
                {},
            ),
            favorite_tools=data.get(
                "favorite_tools",
                [],
            ),
            communication_style=data.get(
                "communication_style",
                {},
            ),
        )
