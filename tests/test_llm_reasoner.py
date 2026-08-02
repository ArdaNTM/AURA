import json

from aura.ai.llm_provider import LLMProvider
from aura.brain.llm_reasoner import LLMReasoner


class FakeLLMProvider(LLMProvider):
    """Fake provider for tests."""

    def __init__(
        self,
        response: str,
    ) -> None:
        self.response = response
        self.last_prompt = None

    def complete(
        self,
        prompt: str,
    ) -> str:
        self.last_prompt = prompt

        return self.response


def test_llm_reasoner_creates_reasoning_result():
    provider = FakeLLMProvider(
        json.dumps(
            {
                "intent": "calculation",
                "goal": "calculate expression",
                "capability": "calculation",
                "confidence": 0.9,
                "risk_level": "low",
            }
        )
    )

    reasoner = LLMReasoner(
        provider,
    )

    result = reasoner.analyze(
        "5+5 hesapla",
    )

    assert result.intent == "calculation"

    assert result.goal == "calculate expression"

    assert result.capability == "calculation"

    assert result.confidence == 0.9

    assert result.risk_level == "low"


def test_llm_reasoner_sends_user_message_to_provider():
    provider = FakeLLMProvider(
        "{}",
    )

    reasoner = LLMReasoner(
        provider,
    )

    reasoner.analyze(
        "merhaba",
    )

    assert provider.last_prompt is not None

    assert "merhaba" in provider.last_prompt


def test_llm_reasoner_handles_invalid_json():
    provider = FakeLLMProvider(
        "invalid response",
    )

    reasoner = LLMReasoner(
        provider,
    )

    result = reasoner.analyze(
        "test",
    )

    assert result.intent == "unknown"

    assert result.confidence == 0.0
