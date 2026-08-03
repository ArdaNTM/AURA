from aura.brain.brain import Brain
from aura.brain.experience_planner import ExperiencePlanner
from aura.brain.models import PlanStep


def test_experience_failure_adds_recovery_step():

    planner = ExperiencePlanner()

    plan = [
        PlanStep(
            description="Execute tool",
            action="tool",
        ),
    ]

    learning = {
        "task_failures": [
            "Missing package",
        ],
    }

    updated = planner.modify_plan(
        plan,
        learning,
    )

    assert len(updated) == 2

    assert updated[0].action == "experience_recovery"

    assert "Missing package" in updated[0].metadata["reason"]


def test_previous_experience_changes_plan():
    brain = Brain()

    decision, _ = brain.think(
        "5+5 hesapla",
        memories=[
            (
                "assistant",
                (
                    "task=calculation;"
                    "task_success=True;"
                    "strategy=safe_tool_execution;"
                ),
            )
        ],
    )

    assert decision.plan
    assert "experience" in decision.metadata
