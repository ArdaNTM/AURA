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
        self,
        settings: Settings | None = None,
        cli: CLI | None = None,
    ) -> None:
        self.settings = settings or Settings()
        self.logger = configure_logging(
            self.settings.log_level,
            self.settings.log_directory,
        )

        provider = ProviderFactory.create(self.settings)
        ai_manager = AIManager(provider)

        self.router = CommandRouter(ai_manager)
        self.cli = cli or CLI()

    def startup(self) -> None:
        """Initialize application resources."""
        self.logger.info(
            "AURA is starting with provider '%s'.",
            self.settings.model_provider,
        )

    def run(self) -> None:
        """Run the application."""
        self.startup()

        try:
            self.cli.start(self.settings, self.router)

        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user.")

        except Exception:
            self.logger.exception("Unexpected application error.")
            raise

        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """Release application resources."""
        self.logger.info("AURA shutdown complete.")