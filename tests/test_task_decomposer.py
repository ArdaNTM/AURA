from aura.brain.goal import Goal
from aura.brain.task_decomposer import TaskDecomposer


def test_game_goal_is_decomposed():

    goal = Goal(
        description="Mobil oyun yap",
    )

    decomposer = TaskDecomposer()

    plan = decomposer.decompose(
        goal,
    )

    assert len(plan.steps) == 5

    assert plan.steps[0].action == "concept"

    assert plan.steps[-1].action == "build"


def test_generic_goal_is_decomposed():

    goal = Goal(
        description="Bir şey yap",
    )

    decomposer = TaskDecomposer()

    plan = decomposer.decompose(
        goal,
    )

    assert len(plan.steps) == 2