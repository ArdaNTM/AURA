"""Keyboard control abstraction."""

from __future__ import annotations


class KeyboardController:
    """Control keyboard actions."""

    def type_text(
        self,
        text: str,
    ) -> str:
        """Type text."""

        return f"Typed: {text}"

    def press(
        self,
        key: str,
    ) -> str:
        """Press key."""

        return f"Pressed: {key}"
