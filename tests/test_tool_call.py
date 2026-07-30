from aura.ai.tool_call import ToolCall


def test_tool_call_without_call_id() -> None:
    call = ToolCall(
        name="echo",
        arguments={
            "value": "hello",
        },
    )

    assert call.name == "echo"
    assert call.arguments["value"] == "hello"
    assert call.call_id is None


def test_tool_call_with_call_id() -> None:
    call = ToolCall(
        name="echo",
        arguments={
            "value": "hello",
        },
        call_id="call_123",
    )

    assert call.call_id == "call_123"