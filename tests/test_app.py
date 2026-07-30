from unittest.mock import MagicMock

from aura.core.app import AuraApplication


def test_application_runs_cli() -> None:
    cli = MagicMock()

    app = AuraApplication(cli=cli)

    app.run()

    cli.start.assert_called_once()


def test_shutdown_is_called() -> None:
    cli = MagicMock()

    app = AuraApplication(cli=cli)

    app.shutdown = MagicMock()

    app.run()

    app.shutdown.assert_called_once()