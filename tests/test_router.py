from aura.ai.manager import AIManager
from aura.ai.providers.dummy_provider import DummyProvider
from aura.ai.tool_runner import ToolRunner
from aura.core.router import CommandRouter
from aura.core.session import Session
from aura.core.tools import ToolRegistry
from aura.memory.in_memory import InMemoryMemory


def build_router() -> CommandRouter:
    registry = ToolRegistry()

    return CommandRouter(
        AIManager(
            DummyProvider(),
            Session(InMemoryMemory()),
            registry,
            ToolRunner(registry),
        )
    )


def test_help_command_returns_available_commands() -> None:
    result = build_router().route("yardım")

    assert result.message == "Kullanılabilir komutlar:\n- yardım\n- çıkış"
    assert not result.should_exit


def test_exit_command_stops_cli_loop() -> None:
    result = build_router().route("çıkış")

    assert result.message == "Görüşmek üzere."
    assert result.should_exit


def test_empty_input_returns_warning() -> None:
    result = build_router().route("   ")

    assert result.message == "Lütfen bir mesaj veya komut yaz."
    assert not result.should_exit


def test_unknown_command_is_forwarded_to_ai() -> None:
    result = build_router().route("Bugün nasılsın?")

    assert result.message == "Mesajını aldım: Bugün nasılsın?"
    assert not result.should_exit


def test_help_aliases() -> None:
    router = build_router()

    for command in ("help", "/help", "yardim"):
        result = router.route(command)

        assert result.message == "Kullanılabilir komutlar:\n- yardım\n- çıkış"
        assert not result.should_exit


def test_exit_aliases() -> None:
    router = build_router()

    for command in ("exit", "quit", "/exit", "cikis"):
        result = router.route(command)

        assert result.should_exit
        assert result.message == "Görüşmek üzere."
