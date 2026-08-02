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
                "intent": "calculation",
                "goal": "calculate",
                "capability": "calculation",
                "confidence": 0.3,
                "risk_level": "low",
                "entities": {
                    "expression": "5+5",
                },
            }
        )


def test_planner_blocks_low_confidence_execution():

    planner = Planner(
        llm_confidence_threshold=0.75,
        llm_reasoner=LLMReasoner(
            LowConfidenceProvider(),
        ),
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.strategy == "confidence_review"

    assert decision.metadata["confidence_guard"]
