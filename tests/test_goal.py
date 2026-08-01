from aura.brain.goal import Goal


def test_goal_defaults():
    goal = Goal(
        description="Build calculator",
    )

    assert goal.description == "Build calculator"

    assert goal.priority == "normal"

    assert not goal.completed

    assert goal.progress == 0.0


def test_goal_mark_completed():
    goal = Goal(
        description="Complete task",
    )

    goal.mark_completed()

    assert goal.completed

    assert goal.progress == 1.0


def test_goal_updates_progress():
    goal = Goal(
        description="Write documentation",
    )

    goal.update_progress(
        0.4,
    )

    assert goal.progress == 0.4

    assert not goal.completed


def test_goal_completes_at_full_progress():
    goal = Goal(
        description="Run tests",
    )

    goal.update_progress(
        1.0,
    )

    assert goal.completed

    assert goal.progress == 1.0


def test_goal_clamps_progress():
    goal = Goal(
        description="Clamp values",
    )

    goal.update_progress(
        5.0,
    )

    assert goal.progress == 1.0

    assert goal.completed

    goal = Goal(
        description="Negative progress",
    )

    goal.update_progress(
        -2.0,
    )

    assert goal.progress == 0.0

    assert not goal.completed
