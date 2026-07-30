from types import SimpleNamespace
from unittest.mock import MagicMock

from aura.ai.manager import AIManager
from aura.ai.providers.openai_provider import OpenAIProvider
from aura.ai.tool_runner import ToolRunner
from aura.core.session import Session
from aura.core.tools import ToolRegistry
from aura.memory.in_memory import InMemoryMemory
from aura.tools import CalculatorTool


def test_openai_tool_agent_flow() -> None:
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    provider = OpenAIProvider(
        api_key="test-key",
        model="test-model",
    )

    provider._client.responses.create = MagicMock(
        side_effect=[
            SimpleNamespace(
                output=[
                    SimpleNamespace(
                        type="function_call",
                        name="calculator",
                        arguments='{"expression":"2+2"}',
                        call_id="call_123",
                    )
                ],
                output_text="",
            ),
            SimpleNamespace(
                output=[],
                output_text="Sonuç 4.",
            ),
        ]
    )

    manager = AIManager(
        provider,
        Session(
            InMemoryMemory(),
        ),
        registry,
        ToolRunner(registry),
    )

    result = manager.respond(
        "2+2 hesapla",
    )

    assert result == "Sonuç 4."

    assert provider._client.responses.create.call_count == 2

    first_request = provider._client.responses.create.call_args_list[0].kwargs

    assert first_request["tools"][0]["type"] == "function"

    assert first_request["tools"][0]["name"] == ("calculator")

    assert first_request["tools"][0]["description"] == (
        "Evaluate basic mathematical expressions."
    )

    assert (
        first_request["tools"][0]["parameters"]
        == registry.openai_schemas()[0]["parameters"]
    )

    second_request = provider._client.responses.create.call_args_list[1].kwargs

    assert {
        "type": "function_call_output",
        "call_id": "call_123",
        "output": "4",
    } in second_request["input"]


def test_calculator_tool_is_registered() -> None:
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    manager = AIManager(
        OpenAIProvider(
            api_key="test-key",
            model="test-model",
        ),
        Session(
            InMemoryMemory(),
        ),
        registry,
        ToolRunner(registry),
    )

    assert manager.tools.list_tools() == [
        "calculator",
    ]
