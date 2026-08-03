from datetime import datetime, timedelta

from aura.memory.in_memory import InMemoryMemory


def test_new_successful_strategy_beats_old_memory():

    memory = InMemoryMemory()

    old_time = (
        datetime.now()
        - timedelta(
            days=100,
        )
    ).isoformat()

    memory.add(
        "assistant",
        (
            "intent=calculation; "
            "strategy=tool_execution; "
            "confidence=0.9; "
            "success=True; "
            f"timestamp={old_time};"
        ),
    )

    memory.add(
        "assistant",
        (
            "intent=calculation; "
            "strategy=safe_tool_execution; "
            "confidence=0.8; "
            "success=True; "
            f"timestamp={datetime.now().isoformat()};"
        ),
    )

    ranked = memory.rank_experiences(
        "calculation",
    )

    assert "safe_tool_execution" in ranked[0][1]
