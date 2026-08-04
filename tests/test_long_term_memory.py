from aura.memory.long_term import LongTermMemory
from aura.memory.models import (
    MemoryItem,
    MemoryType,
)


def test_long_term_memory_ranking():

    memory = LongTermMemory()

    memory.remember(
        MemoryItem(
            content="AURA projesi Python ile yapılıyor",
            memory_type=MemoryType.PROJECT,
            importance=0.9,
        )
    )

    result = memory.recall("AURA")

    assert result[0].memory_type == MemoryType.PROJECT
