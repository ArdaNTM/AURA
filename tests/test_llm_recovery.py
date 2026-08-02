import json

from aura.ai.llm_provider import LLMProvider
from aura.brain.llm_reasoner import LLMReasoner
from aura.brain.llm_validator import LLMValidator
from aura.brain.planner import Planner


class InvalidLLMProvider(LLMProvider):
    """Returns invalid reasoning."""

    def complete(
        self,
        prompt: str,
    ) -> str:
        return json.dumps(
            {
                "intent": "unknown_action",
                "confidence": 0.9,
                "risk_level": "low",
            }
        )


def test_planner_recovers_from_invalid_llm_reasoning():

    reasoner = LLMReasoner(
        InvalidLLMProvider(),
    )

    validator = LLMValidator(
        Planner().capabilities,
    )

    planner = Planner(
        llm_reasoner=reasoner,
        llm_validator=validator,
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.intent == "calculation"
