from aura.brain.learning_profile import LearningProfile


def test_learning_profile_registers_successful_task():
    profile = LearningProfile()

    profile.register_task(
        success=True,
        strategy="tool_execution",
    )

    assert profile.total_tasks == 1

    assert profile.successful_tasks == 1

    assert profile.failed_tasks == 0

    assert profile.strategy_usage["tool_execution"] == 1

    assert profile.strategy_success["tool_execution"] == 1


def test_learning_profile_registers_failed_task():
    profile = LearningProfile()

    profile.register_task(
        success=False,
        strategy="tool_execution",
    )

    assert profile.total_tasks == 1

    assert profile.successful_tasks == 0

    assert profile.failed_tasks == 1

    assert profile.strategy_usage["tool_execution"] == 1

    assert "tool_execution" not in profile.strategy_success


def test_learning_profile_calculates_success_rate():
    profile = LearningProfile()

    profile.register_task(
        success=True,
    )

    profile.register_task(
        success=True,
    )

    profile.register_task(
        success=False,
    )

    assert profile.success_rate == 2 / 3


def test_learning_profile_calculates_strategy_success_rate():
    profile = LearningProfile()

    profile.register_task(
        success=True,
        strategy="safe_tool_execution",
    )

    profile.register_task(
        success=True,
        strategy="safe_tool_execution",
    )

    profile.register_task(
        success=False,
        strategy="safe_tool_execution",
    )

    assert (
        profile.strategy_success_rate(
            "safe_tool_execution",
        )
        == 2 / 3
    )


def test_learning_profile_updates_skill_score():
    profile = LearningProfile()

    profile.update_skill(
        "coding",
        0.85,
    )

    assert profile.skill_scores["coding"] == 0.85
