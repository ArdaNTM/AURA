import json

from aura.ai.llm_provider import LLMProvider
from aura.brain.llm_reasoner import LLMReasoner
from aura.brain.planner import Planner


class LowConfidenceProvider(LLMProvider):
    """Return low confidence reasoning."""

    def complete(
        self,
        prompt: str,
    ) -> str:
        return json.dumps(
            {
                "intent": "filesystem",
                "goal": "open file",
                "capability": "filesystem",
                "confidence": 0.3,
                "risk_level": "medium",
                "entities": {},
            }
        )


def test_planner_falls_back_when_llm_confidence_low():

    planner = Planner(
        llm_reasoner=LLMReasoner(
            LowConfidenceProvider(),
        ),
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.intent == "calculation"
