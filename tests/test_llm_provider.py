from aura.ai.llm_provider import LLMProvider


class FakeLLMProvider(LLMProvider):
    """Test provider."""

    def complete(
        self,
        prompt: str,
    ) -> str:
        return "test response"


def test_llm_provider_generates_response():
    provider = FakeLLMProvider()

    response = provider.complete(
        "hello",
    )

    assert response == "test response"
