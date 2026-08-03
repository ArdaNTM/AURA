from datetime import datetime, timedelta

from aura.memory.in_memory import InMemoryMemory
from aura.memory.optimization import MemoryOptimizer


def test_optimizer_finds_old_low_value_memory():

    memory = InMemoryMemory()

    old = (
        datetime.now()
        - timedelta(
            days=120,
        )
    ).isoformat()

    memory.add(
        "assistant",
        ("task=test; " "success=False; " f"timestamp={old}; "),
    )

    optimizer = MemoryOptimizer()

    result = optimizer.find_expired(
        memory,
    )

    assert len(result) == 1


def test_optimizer_ignores_successful_memory():

    memory = InMemoryMemory()

    old = (
        datetime.now()
        - timedelta(
            days=120,
        )
    ).isoformat()

    memory.add(
        "assistant",
        ("task=test; " "success=True; " f"timestamp={old}; "),
    )

    optimizer = MemoryOptimizer()

    result = optimizer.find_expired(
        memory,
    )

    assert result == []
