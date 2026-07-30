from aura.ai.provider_response import ProviderResponse
from aura.ai.tool_call import ToolCall


def test_provider_response_with_text() -> None:
    response = ProviderResponse(
        text="Merhaba",
    )

    assert response.text == "Merhaba"
    assert not response.has_tool_call
    assert response.has_text


def test_provider_response_with_tool_call() -> None:
    response = ProviderResponse(
        tool_call=ToolCall(
            name="calculator",
            arguments={
                "expression": "2+2",
            },
        ),
    )

    assert response.tool_call is not None
    assert response.tool_call.name == "calculator"
    assert response.has_tool_call
    assert not response.has_text
