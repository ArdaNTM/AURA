from aura.brain.improvement_memory import ImprovementMemory


def test_improvement_memory_tracks_success():

    memory = ImprovementMemory()

    memory.add(
        "safe_tool_execution",
        0.5,
        0.9,
        True,
    )

    assert memory.best_strategy() == "safe_tool_execution"

    assert (
        memory.success_rate(
            "safe_tool_execution",
        )
        == 1.0
    )
