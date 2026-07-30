"""Terminal user interface for AURA."""

from __future__ import annotations

from collections.abc import Callable

from rich.console import Console

from aura.config.settings import Settings
from aura.core.router import CommandRouter


class CLI:
    """Run AURA's interactive terminal loop."""

    def __init__(
        self,
        console: Console | None = None,
        input_reader: Callable[[str], str] = input,
    ) -> None:
        self._console = console or Console()
        self._input_reader = input_reader

    def start(self, settings: Settings, router: CommandRouter) -> None:
        """Show the banner and process messages until the user exits."""
        self._console.print(
            "[bold cyan]==================================================[/bold cyan]"
        )
        self._console.print(
            f"[bold cyan]{settings.aura_name} v0.1.0 - Foundation[/bold cyan]"
        )
        self._console.print(
            "[bold cyan]==================================================[/bold cyan]"
        )
        self._console.print()
        self._console.print("Merhaba Arda!")
        self._console.print(
            "AURA başarıyla başlatıldı. Yardım için 'yardım' yazabilirsin."
        )
        self._console.print()

        while True:
            try:
                user_input = self._input_reader("AURA > ")
            except (EOFError, KeyboardInterrupt):
                self._console.print("\nGörüşmek üzere.")
                return

            result = router.route(user_input)
            self._console.print(result.message)
            self._console.print()
            if result.should_exit:
                return
