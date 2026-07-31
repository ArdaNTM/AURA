from aura.brain.brain import Brain
from aura.brain.learning import LearningContext
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


def test_brain_uses_learning_context():
    learning = LearningContext(
        [
            (
                "assistant",
                "Previous tool execution succeeded.",
            ),
        ],
    )

    brain = Brain(
        learning_context=learning,
    )

    decision, _ = brain.think(
        "Merhaba",
    )

    assert "learning" in decision.metadata

    assert decision.metadata["learning"]["memory_count"] == 1


def test_brain_uses_successful_strategy_memory():
    brain = Brain()

    decision, _ = brain.think(
        "5+5 hesapla",
        memories=[
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True; "
                    "output=10"
                ),
            ),
        ],
    )

    assert "learning" in decision.metadata

    learning = decision.metadata["learning"]

    assert (
        len(
            learning["successful_strategies"],
        )
        == 1
    )

    assert "safe_tool_execution" in learning["successful_strategies"][0]


def test_brain_calculates_strategy_scores_from_memory():
    brain = Brain()

    decision, _ = brain.think(
        "5+5 hesapla",
        memories=[
            (
                "assistant",
                ("intent=calculation; " "strategy=tool_execution; " "success=True"),
            ),
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True"
                ),
            ),
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True"
                ),
            ),
        ],
    )

    learning = decision.metadata["learning"]

    assert learning["strategy_scores"] == {
        "tool_execution": 1,
        "safe_tool_execution": 2,
    }


def test_brain_sets_preferred_strategy_confidence():
    brain = Brain()

    decision, _ = brain.think(
        "5+5 hesapla",
        memories=[
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True"
                ),
            ),
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True"
                ),
            ),
            (
                "assistant",
                ("intent=calculation; " "strategy=tool_execution; " "success=True"),
            ),
        ],
    )

    learning = decision.metadata["learning"]

    assert learning["preferred_strategy"] == "safe_tool_execution"

    assert learning["strategy_confidence"] == 2 / 3
