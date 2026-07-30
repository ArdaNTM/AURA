"""Route user input to AURA's core capabilities."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from aura.ai.manager import AIManager


@dataclass(frozen=True, slots=True)
class RouteResult:
    """The response and lifecycle instruction produced by a command."""

    message: str
    should_exit: bool = False


class CommandRouter:
    """Handle built-in commands before delegating ordinary messages to AI."""

    HELP_TEXT = "Kullanılabilir komutlar:\n- yardım\n- çıkış"

    def __init__(self, ai_manager: AIManager) -> None:
        self._ai_manager = ai_manager
        self._commands: dict[str, Callable[[], RouteResult]] = {
            "yardım": self._help,
            "yardim": self._help,
            "help": self._help,
            "/help": self._help,
            "çıkış": self._exit,
            "cikis": self._exit,
            "exit": self._exit,
            "quit": self._exit,
            "/exit": self._exit,
        }

    def route(self, user_input: str) -> RouteResult:
        """Turn one line of user input into a response."""
        normalized = user_input.strip().casefold()

        if not normalized:
            return RouteResult("Lütfen bir mesaj veya komut yaz.")

        command = self._commands.get(normalized)
        if command is not None:
            return command()

        return RouteResult(self._ai_manager.respond(user_input))

    def _help(self) -> RouteResult:
        """Return the help message."""
        return RouteResult(self.HELP_TEXT)

    def _exit(self) -> RouteResult:
        """Exit the application."""
        return RouteResult("Görüşmek üzere.", should_exit=True)