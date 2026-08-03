from aura.brain.models import Decision
from aura.brain.observation import Observation
from aura.brain.reflection_engine import ReflectionEngine


def test_reflection_includes_skill_context():

    decision = Decision(
        intent="calculation",
        strategy="tool_execution",
        metadata={
            "skill_context": {
                "name": "calculation",
                "confidence": 0.95,
            }
        },
    )

    observation = Observation(
        source="calculator",
        output="10",
        success=True,
        score=1.0,
    )

    reflection = ReflectionEngine().reflect(
        observation,
        decision,
    )

    assert reflection.metadata["decision"]["skill"]["name"] == "calculation"

    assert reflection.metadata["decision"]["skill"]["confidence"] == 0.95
