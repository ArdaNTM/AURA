from types import SimpleNamespace
from unittest.mock import MagicMock

from aura.ai.providers.openai_provider import OpenAIProvider


def create_provider() -> OpenAIProvider:
    return OpenAIProvider(
        api_key="test-key",
        model="test-model",
    )


def test_openai_provider_name() -> None:
    provider = create_provider()

    assert provider.name == "openai"


def test_openai_provider_model() -> None:
    provider = create_provider()

    assert provider.model == "test-model"


def test_openai_provider_returns_text_response() -> None:
    provider = create_provider()

    provider._client.responses.create = MagicMock(
        return_value=SimpleNamespace(
            output=[],
            output_text="Hello AURA",
        )
    )

    result = provider.generate_response(
        "Merhaba",
    )

    assert result.text == "Hello AURA"
    assert not result.has_tool_call


def test_openai_provider_sends_tools() -> None:
    provider = create_provider()

    provider._client.responses.create = MagicMock(
        return_value=SimpleNamespace(
            output=[],
            output_text="ok",
        )
    )

    provider.generate_response(
        "hesapla",
        tools=[
            {
                "name": "calculator",
                "description": "Calculate values.",
                "parameters": {
                    "type": "object",
                },
            }
        ],
    )

    provider._client.responses.create.assert_called_once()

    request = (
        provider._client.responses.create.call_args.kwargs
    )

    assert request["tools"] == [
        {
            "type": "function",
            "name": "calculator",
            "description": "Calculate values.",
            "parameters": {
                "type": "object",
            },
        }
    ]


def test_openai_provider_sends_tool_outputs() -> None:
    provider = create_provider()

    provider._client.responses.create = MagicMock(
        return_value=SimpleNamespace(
            output=[],
            output_text="ok",
        )
    )

    provider.generate_response(
        "devam et",
        tool_outputs=[
            {
                "call_id": "call_123",
                "output": "hello",
            }
        ],
    )

    provider._client.responses.create.assert_called_once()

    request = (
        provider._client.responses.create.call_args.kwargs
    )

    assert {
        "type": "function_call_output",
        "call_id": "call_123",
        "output": "hello",
    } in request["input"]