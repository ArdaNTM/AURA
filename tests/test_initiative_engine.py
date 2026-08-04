from aura.brain.initiative_engine import InitiativeEngine
from aura.brain.self_evaluation import SelfEvaluation


def test_creates_initiative_from_weak_skill():

    evaluation = SelfEvaluation(
        overall_score=0.8,
        weakest_skill="coding",
        best_strategy="tool_execution",
    )

    result = InitiativeEngine().create(
        evaluation,
    )

    assert result is not None

    assert result.task == ("Improve skill: coding")

    assert result.priority == "medium"


def test_creates_reliability_initiative():

    evaluation = SelfEvaluation(
        overall_score=0.2,
    )

    result = InitiativeEngine().create(
        evaluation,
    )

    assert result is not None

    assert result.strategy == "safe_tool_execution"


def test_no_initiative_for_good_state():

    evaluation = SelfEvaluation(
        overall_score=1.0,
    )

    result = InitiativeEngine().create(
        evaluation,
    )

    assert result is None
