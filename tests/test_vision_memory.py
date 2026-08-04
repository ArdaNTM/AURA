from aura.memory.in_memory import InMemoryMemory
from aura.vision.memory import VisionMemory
from aura.vision.models import VisionResult


def test_vision_memory_stores_screen_state():

    memory = InMemoryMemory()

    vision_memory = VisionMemory(
        memory,
    )

    vision_memory.store(
        VisionResult(
            description="Unity editor",
            objects=["window"],
            confidence=0.9,
        ),
        context="game development",
    )

    result = vision_memory.recall(
        "Unity",
    )

    assert len(result) == 1

    assert "Unity editor" in result[0][1]
