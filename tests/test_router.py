from aura.ai.manager import AIManager
from aura.ai.providers.dummy_provider import DummyProvider
from aura.core.router import CommandRouter


def build_router() -> CommandRouter:
    return CommandRouter(AIManager(DummyProvider()))


def test_help_command_returns_available_commands() -> None:
    result = build_router().route("yardım")

    assert result.message == "Kullanılabilir komutlar:\n- yardım\n- çıkış"
    assert not result.should_exit


def test_exit_command_stops_cli_loop() -> None:
    result = build_router().route("çıkış")

    assert result.message == "Görüşmek üzere."
    assert result.should_exit
