from aura.ai.llm_provider import LLMProvider
from aura.brain.llm_reasoner import LLMReasoner
from aura.brain.planner import Planner


class FusionLLMProvider(LLMProvider):
    """Return LLM confidence."""

    def complete(
        self,
        prompt: str,
    ) -> str:
        return """
        {
            "intent": "calculation",
            "goal": "calculate",
            "capability": "calculation",
            "confidence": 0.8,
            "risk_level": "low",
            "entities": {
                "expression": "5+5"
            }
        }
        """


def test_planner_fuses_llm_and_intent_confidence():

    planner = Planner(
        llm_reasoner=LLMReasoner(
            FusionLLMProvider(),
        ),
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.intent == "calculation"

    # LLM: 0.80
    # IntentEngine: 0.95
    # Fusion: 0.875 -> 0.88

    assert decision.confidence == 0.88


def test_planner_stores_confidence_metadata():

    planner = Planner(
        llm_reasoner=LLMReasoner(
            FusionLLMProvider(),
        ),
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.metadata["llm_confidence"] == 0.8

    assert decision.metadata["final_confidence"] == 0.88
