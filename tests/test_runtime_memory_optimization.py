from datetime import datetime, timedelta

from aura.memory.in_memory import InMemoryMemory
from aura.memory.optimization import MemoryOptimizer


def test_runtime_memory_optimizer_can_remove_expired():

    memory = InMemoryMemory()

    old = (
        datetime.now()
        - timedelta(
            days=120,
        )
    ).isoformat()

    memory.add(
        "assistant",
        ("task=test; " "success=False; " f"timestamp={old};"),
    )

    optimizer = MemoryOptimizer()

    expired = optimizer.find_expired(
        memory,
    )

    assert len(expired) == 1
