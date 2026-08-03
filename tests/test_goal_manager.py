from aura.brain.goal_manager import GoalManager


def test_goal_manager_creates_goal():
    manager = GoalManager()

    goal = manager.create_goal(
        "Build game",
    )

    assert goal.description == "Build game"

    assert len(manager.list_goals()) == 1


def test_goal_manager_updates_progress():
    manager = GoalManager()

    goal = manager.create_goal(
        "Write code",
    )

    manager.update_progress(
        goal.goal_id,
        0.5,
    )

    assert goal.progress == 0.5


def test_goal_manager_completes_goal():
    manager = GoalManager()

    goal = manager.create_goal(
        "Finish project",
    )

    manager.complete_goal(
        goal.goal_id,
    )

    assert goal.completed


def test_goal_manager_active_goals():
    manager = GoalManager()

    active = manager.create_goal(
        "Active",
    )

    finished = manager.create_goal(
        "Finished",
    )

    manager.complete_goal(
        finished.goal_id,
    )

    goals = manager.active_goals()

    assert active in goals

    assert finished not in goals
