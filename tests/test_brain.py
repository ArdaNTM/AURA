from aura.brain.models import Decision, PlanStep


def test_decision_model_creation():
    decision = Decision(
        intent="calculator",
        confidence=0.9,
        requires_tool=True,
        plan=[
            PlanStep(
                "Calculate value",
            )
        ],
    )

    assert decision.intent == "calculator"

    assert decision.confidence == 0.9

    assert decision.requires_tool

    assert len(decision.plan) == 1

    assert decision.plan[0].description == "Calculate value"