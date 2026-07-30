"""Route user input to AURA's core capabilities."""

from __future__ import annotations

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

    def route(self, user_input: str) -> RouteResult:
        """Turn one line of user input into a response."""
        normalized = user_input.strip().casefold()
        if not normalized:
            return RouteResult("Lütfen bir mesaj veya komut yaz.")
        if normalized in {"yardım", "yardim", "help", "/help"}:
            return RouteResult(self.HELP_TEXT)
        if normalized in {"çıkış", "cikis", "exit", "quit", "/exit"}:
            return RouteResult("Görüşmek üzere.", should_exit=True)
        return RouteResult(self._ai_manager.respond(user_input))
