import json

from aura.ai.llm_provider import LLMProvider
from aura.brain.llm_reasoner import LLMReasoner
from aura.brain.planner import Planner


class LowConfidenceComputerProvider(LLMProvider):

    def complete(
        self,
        prompt: str,
    ) -> str:
        return json.dumps(
            {
                "intent": "computer",
                "goal": "control computer",
                "capability": "computer",
                "confidence": 0.3,
                "risk_level": "high",
                "entities": {},
            }
        )


def test_low_confidence_high_risk_requires_review():

    planner = Planner(
        llm_reasoner=LLMReasoner(
            LowConfidenceComputerProvider(),
        ),
        llm_confidence_threshold=0.75,
    )

    decision = planner.decide(
        "bilgisayarı kontrol et",
    )

    assert decision.strategy == "risk_review"

    assert decision.metadata["risk_review"]

    assert decision.requires_permission
