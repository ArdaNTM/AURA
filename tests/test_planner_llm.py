import json

from aura.ai.llm_provider import LLMProvider
from aura.brain.llm_reasoner import LLMReasoner
from aura.brain.planner import Planner


class FakeLLMProvider(LLMProvider):
    """Fake LLM provider."""

    def complete(
        self,
        prompt: str,
    ) -> str:

        return json.dumps(
            {
                "intent": "calculation",
                "goal": "calculate expression",
                "capability": "calculation",
                "confidence": 0.95,
                "risk_level": "low",
                "entities": {
                    "expression": "10+5",
                },
            }
        )


def test_planner_uses_llm_reasoner():

    reasoner = LLMReasoner(
        FakeLLMProvider(),
    )

    planner = Planner(
        llm_reasoner=reasoner,
    )

    decision = planner.decide(
        "hesapla",
    )

    assert decision.intent == "calculation"

    assert decision.metadata["intent_confidence"] == 0.95


def test_planner_keeps_fallback_without_llm():

    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.intent == "calculation"
