"""AURA application composition root."""

from __future__ import annotations

from aura.ai.factory import ProviderFactory
from aura.ai.manager import AIManager
from aura.ai.tool_runner import ToolRunner
from aura.config.settings import Settings
from aura.context.builder import ContextBuilder
from aura.core.container import Container
from aura.core.event_logger import EventLogger
from aura.core.events import EventBus
from aura.core.logger import configure_logging
from aura.core.router import CommandRouter
from aura.core.session import Session
from aura.core.tools import ToolRegistry
from aura.memory.base import Memory
from aura.memory.factory import MemoryFactory
from aura.tools import CalculatorTool
from aura.ui.cli import CLI


class AuraApplication:
    """Create and run the AURA core application."""

    def __init__(
        self,
        settings: Settings | None = None,
        cli: CLI | None = None,
        container: Container | None = None,
    ) -> None:
        self.container = container or Container()

        self.container.register_instance(
            Settings,
            settings or Settings(),
        )

        self.container.register_factory(
            EventBus,
            lambda _: EventBus(),
        )

        self.container.register_factory(
            Memory,
            lambda c: MemoryFactory.create(
                c.resolve(Settings),
            ),
        )

        self.container.register_factory(
            Session,
            lambda c: Session(
                c.resolve(Memory),
            ),
        )

        self.container.register_factory(
            ToolRegistry,
            lambda _: ToolRegistry(),
        )

        self.container.register_factory(
            ToolRunner,
            lambda c: ToolRunner(
                c.resolve(ToolRegistry),
            ),
        )

        self.container.register_factory(
            ContextBuilder,
            lambda c: ContextBuilder(
                c.resolve(Session),
                c.resolve(ToolRegistry),
                c.resolve(Memory),
            ),
        )

        self.container.register_factory(
            AIManager,
            lambda c: AIManager(
                ProviderFactory.create(
                    c.resolve(Settings),
                ),
                c.resolve(Session),
                c.resolve(ToolRegistry),
                c.resolve(ToolRunner),
                event_bus=c.resolve(EventBus),
                context_builder=c.resolve(ContextBuilder),
            ),
        )

        self.container.register_factory(
            CommandRouter,
            lambda c: CommandRouter(
                c.resolve(AIManager),
            ),
        )

        self.settings = self.container.resolve(
            Settings,
        )

        self.session = self.container.resolve(
            Session,
        )

        self.tools = self.container.resolve(
            ToolRegistry,
        )

        self.tool_runner = self.container.resolve(
            ToolRunner,
        )

        self.tools.register(
            CalculatorTool(),
        )

        self.logger = configure_logging(
            self.settings.log_level,
            self.settings.log_directory,
        )

        self.event_bus = self.container.resolve(
            EventBus,
        )

        self.event_logger = EventLogger(
            self.event_bus,
            self.logger,
        )

        self.router = self.container.resolve(
            CommandRouter,
        )

        self.cli = cli or CLI()

    def startup(self) -> None:
        """Initialize application resources."""

        self.logger.info(
            "AURA is starting with provider '%s'.",
            self.settings.model_provider,
        )

        self.logger.info(
            "Loaded tools: %s",
            self.tools.list_tools(),
        )

    def run(self) -> None:
        """Run the application."""

        self.startup()

        try:
            self.cli.start(
                self.settings,
                self.router,
            )

        except KeyboardInterrupt:
            self.logger.info(
                "Application interrupted by user.",
            )

        except Exception:
            self.logger.exception(
                "Unexpected application error.",
            )
            raise

        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """Release application resources."""

        self.session.close()

        self.logger.info(
            "AURA shutdown complete.",
        )
