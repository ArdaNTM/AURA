from aura.memory.in_memory import InMemoryMemory


def test_memory_search_finds_matching_messages():
    memory = InMemoryMemory()

    memory.add(
        "user",
        "AURA projesine devam ediyoruz",
    )

    memory.add(
        "assistant",
        "Sprint 3 tamamlandı",
    )

    result = memory.search(
        "AURA",
    )

    assert result == [
        (
            "user",
            "AURA projesine devam ediyoruz",
        )
    ]


def test_memory_search_is_case_insensitive():
    memory = InMemoryMemory()

    memory.add(
        "user",
        "Jarvis benzeri AI yapıyoruz",
    )

    result = memory.search(
        "jarvis",
    )

    assert result == [
        (
            "user",
            "Jarvis benzeri AI yapıyoruz",
        )
    ]


def test_memory_search_returns_empty_when_not_found():
    memory = InMemoryMemory()

    memory.add(
        "user",
        "AURA memory sistemi",
    )

    result = memory.search(
        "Unity",
    )

    assert result == []