from aura.ai.manager import AIManager
from aura.ai.provider_response import ProviderResponse
from aura.ai.providers.base import AIProvider
from aura.ai.providers.dummy_provider import DummyProvider
from aura.ai.tool_call import ToolCall
from aura.ai.tool_runner import ToolRunner
from aura.context.builder import ContextBuilder
from aura.core.ai_events import (
    AIResponseCompleted,
    AIResponseStarted,
    ToolCompleted,
    ToolFailed,
    ToolStarted,
)
from aura.core.events import EventBus
from aura.core.session import Session
from aura.core.tools import Tool, ToolRegistry
from aura.memory.in_memory import InMemoryMemory


class EchoTool(Tool):
    @property
    def name(self) -> str:
        return "echo"

    def execute(self, value: str) -> str:
        return value


class ToolCallingProvider(AIProvider):
    """Fake provider that requests a tool execution once."""

    def __init__(self) -> None:
        self._called = 0

    @property
    def name(self) -> str:
        return "tool-caller"

    def generate_response(
        self,
        user_message: str,
        history=None,
        tools=None,
        tool_outputs=None,
    ) -> ProviderResponse:
        self._called += 1

        if self._called == 1:
            return ProviderResponse(
                tool_call=ToolCall(
                    name="echo",
                    arguments={
                        "value": "hello",
                    },
                    call_id="call_123",
                )
            )

        return ProviderResponse(
            text="Tool sonucu işlendi: hello",
        )


class MultipleToolCallingProvider(AIProvider):
    """Fake provider that requests multiple tools."""

    def __init__(self) -> None:
        self.called = 0

    @property
    def name(self) -> str:
        return "multiple-tool-caller"

    def generate_response(
        self,
        user_message: str,
        history=None,
        tools=None,
        tool_outputs=None,
    ) -> ProviderResponse:
        self.called += 1

        if self.called <= 2:
            return ProviderResponse(
                tool_call=ToolCall(
                    name="echo",
                    arguments={
                        "value": f"hello-{self.called}",
                    },
                    call_id=f"call_{self.called}",
                )
            )

        return ProviderResponse(
            text="İki araç çalıştı.",
        )


class InfiniteToolCallingProvider(AIProvider):
    """Fake provider that never stops requesting tools."""

    @property
    def name(self) -> str:
        return "infinite-tool-caller"

    def generate_response(
        self,
        user_message: str,
        history=None,
        tools=None,
        tool_outputs=None,
    ) -> ProviderResponse:
        return ProviderResponse(
            tool_call=ToolCall(
                name="echo",
                arguments={
                    "value": "loop",
                },
                call_id="loop_call",
            )
        )


def create_manager() -> AIManager:
    registry = ToolRegistry()

    return AIManager(
        DummyProvider(),
        Session(InMemoryMemory()),
        registry,
        ToolRunner(registry),
    )


def create_manager_with_tools() -> AIManager:
    registry = ToolRegistry()
    registry.register(EchoTool())

    return AIManager(
        DummyProvider(),
        Session(InMemoryMemory()),
        registry,
        ToolRunner(registry),
    )


def create_tool_call_manager() -> AIManager:
    registry = ToolRegistry()
    registry.register(EchoTool())

    return AIManager(
        ToolCallingProvider(),
        Session(InMemoryMemory()),
        registry,
        ToolRunner(registry),
    )


def test_dummy_provider_answers_greeting() -> None:
    manager = create_manager()

    assert manager.provider.name == "dummy"

    assert (
        manager.respond("Merhaba") == "Merhaba! Ben AURA. Şimdilik çekirdek modundayım."
    )


def test_dummy_provider_echoes_other_messages() -> None:
    manager = create_manager()

    assert (
        manager.respond("Bugün ne yapıyoruz?") == "Mesajını aldım: Bugün ne yapıyoruz?"
    )


def test_tools_property() -> None:
    manager = create_manager()

    assert manager.tools.list_tools() == []


def test_run_tool_success() -> None:
    manager = create_manager_with_tools()

    result = manager.run_tool(
        "echo",
        "hello",
    )

    assert result.success
    assert result.name == "echo"
    assert result.output == "hello"


def test_run_tool_failure() -> None:
    manager = create_manager()

    result = manager.run_tool(
        "missing",
    )

    assert not result.success
    assert result.name == "missing"


def test_execute_tool_call() -> None:
    manager = create_manager_with_tools()

    result = manager.execute_tool_call(
        ToolCall(
            name="echo",
            arguments={
                "value": "hello",
            },
        )
    )

    assert result.success
    assert result.name == "echo"
    assert result.output == "hello"


def test_tool_call_is_executed() -> None:
    manager = create_tool_call_manager()

    result = manager.respond(
        "echo çalıştır",
    )

    assert result == "Tool sonucu işlendi: hello"


def test_build_tool_message() -> None:
    manager = create_manager_with_tools()

    result = manager.run_tool(
        "echo",
        "hello",
    )

    message = manager.build_tool_message(
        result,
    )

    assert message == {
        "role": "tool",
        "content": "hello",
    }


def test_build_tool_output() -> None:
    manager = create_manager_with_tools()

    call = ToolCall(
        name="echo",
        arguments={
            "value": "hello",
        },
        call_id="call_123",
    )

    result = manager.execute_tool_call(
        call,
    )

    output = manager.build_tool_output(
        call,
        result,
    )

    assert output == {
        "type": "function_call_output",
        "call_id": "call_123",
        "output": "hello",
    }


def test_multiple_tool_calls_are_supported() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())

    provider = MultipleToolCallingProvider()

    manager = AIManager(
        provider,
        Session(InMemoryMemory()),
        registry,
        ToolRunner(registry),
    )

    result = manager.respond(
        "iki tool çalıştır",
    )

    assert result == "İki araç çalıştı."
    assert provider.called == 3


def test_tool_loop_stops_after_limit() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())

    manager = AIManager(
        InfiniteToolCallingProvider(),
        Session(InMemoryMemory()),
        registry,
        ToolRunner(registry),
        max_tool_calls=3,
    )

    result = manager.respond(
        "sonsuz döngü",
    )

    assert result == "AURA çok fazla araç çağrısı denedi."


def test_ai_response_events() -> None:
    events = []

    bus = EventBus()

    bus.subscribe(
        AIResponseStarted,
        events.append,
    )

    bus.subscribe(
        AIResponseCompleted,
        events.append,
    )

    manager = AIManager(
        DummyProvider(),
        Session(InMemoryMemory()),
        ToolRegistry(),
        ToolRunner(ToolRegistry()),
        event_bus=bus,
    )

    result = manager.respond(
        "Merhaba",
    )

    assert isinstance(events[0], AIResponseStarted)
    assert events[0].message == "Merhaba"

    assert isinstance(events[-1], AIResponseCompleted)
    assert events[-1].response == result


def test_tool_events() -> None:
    events = []

    bus = EventBus()

    bus.subscribe(
        ToolStarted,
        events.append,
    )

    bus.subscribe(
        ToolCompleted,
        events.append,
    )

    registry = ToolRegistry()
    registry.register(EchoTool())

    manager = AIManager(
        ToolCallingProvider(),
        Session(InMemoryMemory()),
        registry,
        ToolRunner(registry),
        event_bus=bus,
    )

    result = manager.respond(
        "echo çalıştır",
    )

    assert result == "Tool sonucu işlendi: hello"

    assert isinstance(events[0], ToolStarted)
    assert events[0].name == "echo"

    assert isinstance(events[1], ToolCompleted)
    assert events[1].name == "echo"
    assert events[1].output == "hello"


def test_tool_failed_event() -> None:
    events = []

    bus = EventBus()

    bus.subscribe(
        ToolFailed,
        events.append,
    )

    registry = ToolRegistry()

    manager = AIManager(
        ToolCallingProvider(),
        Session(InMemoryMemory()),
        registry,
        ToolRunner(registry),
        event_bus=bus,
    )

    result = manager.execute_tool_call(
        ToolCall(
            name="missing",
            arguments={},
            call_id="call_failed",
        )
    )

    assert not result.success

    assert len(events) == 1

    event = events[0]

    assert isinstance(
        event,
        ToolFailed,
    )

    assert event.name == "missing"


def test_ai_manager_injects_memory_context():
    registry = ToolRegistry()

    memory = InMemoryMemory()

    memory.add(
        "user",
        "AURA memory sistemi tamamlandı",
    )

    session = Session(
        memory,
    )

    class ContextCheckingProvider(AIProvider):
        """Provider that verifies memory injection."""

        @property
        def name(self) -> str:
            return "context-checker"

        def generate_response(
            self,
            user_message: str,
            history=None,
            tools=None,
            tool_outputs=None,
        ) -> ProviderResponse:
            assert history is not None

            system_messages = [
                message for message in history if message["role"] == "system"
            ]

            assert len(system_messages) == 1

            assert "AURA memory sistemi tamamlandı" in system_messages[0]["content"]

            return ProviderResponse(
                text="memory bulundu",
            )

    manager = AIManager(
        ContextCheckingProvider(),
        session,
        registry,
        ToolRunner(registry),
        context_builder=ContextBuilder(
            session,
            registry,
            memory,
        ),
    )

    result = manager.respond(
        "AURA memory",
    )

    assert result == "memory bulundu"
