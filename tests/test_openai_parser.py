from types import SimpleNamespace

from aura.ai.openai_parser import OpenAIParser


def test_parse_text_response() -> None:
    response = SimpleNamespace(
        output=[],
        output_text="Hello",
    )

    result = OpenAIParser().parse(response)

    assert result.text == "Hello"
    assert not result.has_tool_call


def test_parse_tool_call_response() -> None:
    response = SimpleNamespace(
        output=[
            SimpleNamespace(
                type="function_call",
                name="calculator",
                arguments='{"expression":"2+2"}',
                call_id="call_123",
            )
        ],
        output_text="",
    )

    result = OpenAIParser().parse(response)

    assert result.has_tool_call
    assert result.tool_call is not None
    assert result.tool_call.name == "calculator"
    assert result.tool_call.call_id == "call_123"
    assert result.tool_call.arguments == {
        "expression": "2+2",
    }
