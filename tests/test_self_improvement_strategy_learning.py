from aura.brain.learning_profile import LearningProfile


def test_improvement_changes_strategy_preference():

    class Report:

        success = True
        strategy_change = "safe_tool_execution"
        suggestions = []

    profile = LearningProfile()

    profile.register_improvement_feedback(
        Report(),
    )

    assert profile.improvement_history

    assert profile.strategy_usage["safe_tool_execution"] == 1

    assert profile.strategy_success["safe_tool_execution"] == 1
