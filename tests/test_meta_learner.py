from aura.brain.learning import LearningContext
from aura.brain.meta_learner import MetaLearner


def test_meta_learner_recommends_safe_strategy_for_low_quality():
    learner = MetaLearner()

    context = LearningContext(
        [
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=tool_execution; "
                    "success=False; "
                    "output=error"
                ),
            ),
        ],
    )

    result = learner.analyze(
        context,
    )

    assert result.target_strategy == "safe_tool_execution"

    assert result.risk_adjustment == "medium"

    assert result.confidence_change == -0.1


def test_meta_learner_keeps_strategy_for_medium_quality():
    learner = MetaLearner()

    context = LearningContext(
        [
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=tool_execution; "
                    "success=True; "
                    "output=10"
                ),
            ),
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=False; "
                    "output=error"
                ),
            ),
        ],
    )

    result = learner.analyze(
        context,
    )

    assert result.risk_adjustment == "normal"

    assert result.confidence_change == 0.0


def test_meta_learner_rewards_high_quality_learning():
    learner = MetaLearner()

    context = LearningContext(
        [
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=tool_execution; "
                    "success=True; "
                    "output=10"
                ),
            ),
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=tool_execution; "
                    "success=True; "
                    "output=20"
                ),
            ),
        ],
    )

    result = learner.analyze(
        context,
    )

    assert result.target_strategy == "tool_execution"

    assert result.risk_adjustment == "low"

    assert result.confidence_change == 0.1
