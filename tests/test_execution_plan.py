from aura.brain.execution_plan import ExecutionPlan
from aura.brain.models import PlanStep


def test_execution_plan_defaults():
    plan = ExecutionPlan(
        goal="Build calculator",
    )

    assert plan.goal == "Build calculator"

    assert plan.steps == []

    assert plan.current_step == 0

    assert plan.completed


def test_execution_plan_advances():
    plan = ExecutionPlan(
        goal="Build calculator",
        steps=[
            PlanStep(
                description="Analyze",
                action="analyze",
            ),
            PlanStep(
                description="Calculate",
                action="calculator",
            ),
        ],
    )

    step = plan.next_step()

    assert step is not None

    assert step.action == "analyze"

    assert plan.current_step == 1

    assert not plan.completed


def test_execution_plan_finishes():
    plan = ExecutionPlan(
        goal="Build calculator",
        steps=[
            PlanStep(
                description="Analyze",
                action="analyze",
            ),
        ],
    )

    plan.next_step()

    assert plan.completed

    assert plan.remaining_steps == 0


def test_execution_plan_reset():
    plan = ExecutionPlan(
        goal="Task",
        steps=[
            PlanStep(
                description="Step",
                action="run",
            ),
        ],
    )

    plan.next_step()

    assert plan.completed

    plan.reset()

    assert not plan.completed

    assert plan.current_step == 0
