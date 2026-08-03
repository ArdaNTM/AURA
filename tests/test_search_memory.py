from aura.memory.in_memory import InMemoryMemory
from aura.tools.search import SearchTool


def test_search_stores_research_memory():

    memory = InMemoryMemory()

    tool = SearchTool(
        memory=memory,
    )

    tool.execute(
        "Unity 6 features",
    )

    history = memory.history()

    assert history[0][0] == "research"

    assert "Unity 6 features" in history[0][1]
