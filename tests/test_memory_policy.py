from aura.brain.memory_policy import MemoryPolicy
from aura.brain.observation import Observation


def test_memory_policy_accepts_successful_observation() -> None:
    policy = MemoryPolicy()

    observation = Observation(
        source="calculator",
        output="4",
        success=True,
    )

    assert policy.should_store(
        observation,
    )


def test_memory_policy_rejects_failed_observation() -> None:
    policy = MemoryPolicy()

    observation = Observation(
        source="calculator",
        output="error",
        success=False,
    )

    assert not policy.should_store(
        observation,
    )


def test_memory_policy_rejects_empty_observation() -> None:
    policy = MemoryPolicy()

    observation = Observation(
        source="calculator",
        output="",
        success=True,
    )

    assert not policy.should_store(
        observation,
    )
