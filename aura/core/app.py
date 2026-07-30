"""AURA application composition root."""

from __future__ import annotations

from aura.ai.factory import ProviderFactory
from aura.ai.manager import AIManager
from aura.config.settings import Settings
from aura.core.logger import configure_logging
from aura.core.router import CommandRouter
from aura.ui.cli import CLI


class AuraApplication:
    """Create and run the AURA core application."""

    def __init__(
        self, settings: Settings | None = None, cli: CLI | None = None
    ) -> None:
        self.settings = settings or Settings()
        self.logger = configure_logging(self.settings.log_level)
        provider = ProviderFactory.create(self.settings)
        self.router = CommandRouter(AIManager(provider))
        self.cli = cli or CLI()

    def run(self) -> None:
        """Start the chosen user interface."""
        self.logger.info(
            "AURA is starting with provider '%s'.", self.settings.model_provider
        )
        self.cli.start(self.settings, self.router)
